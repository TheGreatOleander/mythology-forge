#!/data/data/com.termux/files/usr/bin/bash

EP_SRC="/sdcard/mythology-forge/input/episode_bundle"
MEDIA_SRC="/sdcard/mythology-forge/output/media_bundle"

EP_DST="/sdcard/mythology-herald/input/episode_bundle"
MEDIA_DST="/sdcard/mythology-herald/input/media_bundle"

rm -rf "$EP_DST"
rm -rf "$MEDIA_DST"

mkdir -p "$EP_DST"
mkdir -p "$MEDIA_DST"

cp -r "$EP_SRC"/. "$EP_DST"/
cp -r "$MEDIA_SRC"/. "$MEDIA_DST"/

echo "Media bundle sent to Herald"
