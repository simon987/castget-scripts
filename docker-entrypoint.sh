#!/usr/bin/env bash

CONFIG_FILE=/home/castget/.castget/config.ini

echo "Creating folders..."

for dir in $(awk -F "=" '/spool/ {print $2}' "${CONFIG_FILE}")
do
	echo $dir
	mkdir $dir -p &>/dev/null
done

castget -p --resume --rcfile "${CONFIG_FILE}"

python3 transcode.py --mp3-dir /podcasts/ --out-dir /podcasts_transcoded/ --bitrate 18k
python3 keep_last_n.py --in-dir /podcasts_transcoded/ --out-dir /podcasts_shared/ -n 32