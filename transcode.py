import os
from collections import defaultdict
from functools import partial
from multiprocessing import Pool, cpu_count
from glob import glob
import argparse
import subprocess


def convert(mp3_filename, out_filename, bitrate):
    os.makedirs(os.path.split(out_filename)[0], exist_ok=True)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", mp3_filename,
        "-b:a", bitrate,
        out_filename,
    ])


def get_tasks(source, destination):
    mp3_files = glob(os.path.join(source, "**", "*.mp3"), recursive=True)

    out_files = [
        (destination + filename[len(source):].lower()).replace(".mp3", ".opus")
        for filename in mp3_files
    ]

    in_out_mapping = defaultdict(list)
    for in_file, out_file in zip(mp3_files, out_files):
        in_out_mapping[out_file].append(in_file)

    existing_out_files = glob(os.path.join(destination, "**", "*.opus"), recursive=True)

    for filename in existing_out_files:
        if filename not in out_files:
            yield "delete", (None, filename)

    for mp3_filename, out_filename in zip(mp3_files, out_files):
        if out_filename not in existing_out_files:
            yield "convert", (mp3_filename, out_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mp3-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--bitrate", required=True)
    args = parser.parse_args()

    SRC = args.mp3_dir
    DST = args.out_dir

    convert_tasks = []

    for task, (src, dst) in get_tasks(SRC, DST):

        if task == "delete":
            os.remove(dst)

        if task == "convert":
            convert_tasks.append((src, dst))

    print(convert_tasks)
    with Pool(processes=cpu_count()) as pool:
        pool.starmap(func=partial(convert, bitrate=args.bitrate), iterable=convert_tasks)
