#!/data/data/com.termux/files/usr/bin/bash
set -e
EP_SRC="/sdcard/mythology-forge/input/episode_bundle"
MEDIA_SRC="/sdcard/mythology-forge/output/media_bundle"
EP_DST="/sdcard/mythology-herald/input/episode_bundle"
MEDIA_DST="/sdcard/mythology-herald/input/media_bundle"
ARCHIVE_ROOT="/sdcard/mythology-forge/output_archive"
TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
ARCHIVE_DST="$ARCHIVE_ROOT/media_bundle_$TIMESTAMP"
rm -rf "$EP_DST" "$MEDIA_DST"; mkdir -p "$EP_DST" "$MEDIA_DST"
cp -r "$EP_SRC"/. "$EP_DST"/; cp -r "$MEDIA_SRC"/. "$MEDIA_DST"/
[ -f "$EP_DST/bundle.json" ] || { echo "Missing bundle.json"; exit 1; }
[ -f "$MEDIA_DST/media_manifest.json" ] || { echo "Missing media_manifest.json"; exit 1; }
mkdir -p "$ARCHIVE_ROOT" "$ARCHIVE_DST"
cp -r "$MEDIA_SRC"/. "$ARCHIVE_DST"/
rm -rf "$MEDIA_SRC"; mkdir -p "$MEDIA_SRC"; touch "$MEDIA_SRC/.gitkeep"
echo "Media bundle sent to Herald"
echo "Archived to: $ARCHIVE_DST"
