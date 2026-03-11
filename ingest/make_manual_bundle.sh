#!/data/data/com.termux/files/usr/bin/bash
set -e

FORGE_ROOT="/sdcard/mythology-forge"
OUT="$FORGE_ROOT/input/episode_bundle"

if [ $# -lt 2 ]; then
  echo "Usage:"
  echo "  myth-import-video /sdcard/path/to/video.mp4 \"Title Here\""
  exit 1
fi

VIDEO="$1"
TITLE="$2"
EPISODE_ID="manual_$(date +%Y%m%d_%H%M%S)"

if [ ! -f "$VIDEO" ]; then
  echo "Video not found: $VIDEO"
  exit 1
fi

rm -rf "$OUT"
mkdir -p "$OUT"

cat > "$OUT/bundle.json" <<EOF
{
  "bundle_version": "1.0",
  "project": "manual_ingest",
  "episode_id": "$EPISODE_ID",
  "title": "$TITLE",
  "topic": "$TITLE",
  "paths": {
    "script": "script.txt",
    "metadata": "metadata.json",
    "scene_prompts": "scene_prompts.json",
    "episode_plan": "episode_plan.json"
  }
}
EOF

cat > "$OUT/metadata.json" <<EOF
{
  "series": "Manual Import",
  "tags": ["manual", "video", "forge"],
  "tone": "custom"
}
EOF

cat > "$OUT/script.txt" <<EOF
Manual source video imported for Mythology Forge.
Title: $TITLE
Source: $(basename "$VIDEO")
EOF

cat > "$OUT/scene_prompts.json" <<EOF
[
  {
    "scene_id": "scene_01",
    "prompt": "manual source video clip",
    "narration": "Imported external video asset."
  }
]
EOF

cat > "$OUT/episode_plan.json" <<EOF
{
  "hook": "$TITLE",
  "beats": [
    "import source video",
    "prepare forge processing",
    "create media bundle"
  ],
  "target_duration_sec": 60
}
EOF

cp "$VIDEO" "$OUT/source_video.mp4"

echo "Manual Forge input created at:"
echo "  $OUT"
echo ""
echo "Next step:"
echo "  myth-forge"
