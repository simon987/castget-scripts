#!/usr/bin/env bash

CONFIG_FILE=/home/castget/.castget/config.ini

echo "Creating folders..."

for dir in $(awk -F "=" '/spool/ {print $2}' "${CONFIG_FILE}")
do
	echo $dir
	mkdir $dir -p &>/dev/null
done

castget -p --rcfile "${CONFIG_FILE}"

python3 transcode.py --mp3-dir /podcasts/ --out-dir /podcasts_transcoded/ --bitrate 18k
