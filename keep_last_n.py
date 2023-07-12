import os
import shutil
from glob import glob
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("-n", required=True)
    args = parser.parse_args()

    for subfolder in os.listdir(args.in_dir):
        if subfolder.startswith("."):
            continue

        os.makedirs(os.path.join(args.out_dir, subfolder), exist_ok=True)

        to_keep = sorted(glob(os.path.join(args.in_dir, subfolder, "*")), reverse=True)[:int(args.n)]
        to_keep_names = [os.path.basename(x) for x in to_keep]

        for file in glob(os.path.join(args.out_dir, subfolder, "*")):
            if os.path.basename(file) not in to_keep_names:
                os.remove(file)

        for file in to_keep:
            out_file = os.path.join(args.out_dir, subfolder, os.path.basename(file))

            if not os.path.exists(out_file):
                shutil.copy(file, out_file)
