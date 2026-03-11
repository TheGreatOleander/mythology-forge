import json
from pathlib import Path

INPUT = Path("input/episode_bundle")
OUTPUT = Path("output/media_bundle")
OUTPUT.mkdir(parents=True, exist_ok=True)
(OUTPUT / "scene_frames").mkdir(parents=True, exist_ok=True)
(OUTPUT / "teaser_clips").mkdir(parents=True, exist_ok=True)

bundle = json.load(open(INPUT / "bundle.json"))
metadata = json.load(open(INPUT / "metadata.json")) if (INPUT / "metadata.json").exists() else {}
script_text = (INPUT / "script.txt").read_text(encoding="utf-8") if (INPUT / "script.txt").exists() else ""
scene_prompts = json.load(open(INPUT / "scene_prompts.json")) if (INPUT / "scene_prompts.json").exists() else []

episode_id = bundle.get("episode_id", "unknown_episode")
title = bundle.get("title", "Untitled Episode")
topic = bundle.get("topic", title)

(OUTPUT / "final_video.mp4").write_bytes(b"PLACEHOLDER_VIDEO_V0_3")
(OUTPUT / "thumbnail.png").write_bytes(b"PLACEHOLDER_THUMBNAIL_V0_3")

# Create scene frames based on scene prompts
if scene_prompts:
    for i, scene in enumerate(scene_prompts, start=1):
        scene_id = scene.get("scene_id", f"scene_{i:02}")
        payload = f"FRAME::{scene_id}::{scene.get('prompt','')}".encode()
        (OUTPUT / "scene_frames" / f"{scene_id}.png").write_bytes(payload)
else:
    for i in range(1, 4):
        (OUTPUT / "scene_frames" / f"scene_{i:02}.png").write_bytes(f"FRAME_{i}".encode())

# Create teaser clips derived from scene count
teaser_count = 2 if len(scene_prompts) < 2 else min(3, len(scene_prompts))
for i in range(1, teaser_count + 1):
    (OUTPUT / "teaser_clips" / f"teaser_{i:02}.mp4").write_bytes(f"TEASER_{i}".encode())

manifest = {
    "bundle_version": "1.0",
    "source_episode_id": episode_id,
    "generated_by": "Mythology Forge",
    "title": title,
    "topic": topic,
    "derived_from": {
        "bundle": "input/episode_bundle/bundle.json",
        "metadata": "input/episode_bundle/metadata.json",
        "script": "input/episode_bundle/script.txt",
        "scene_prompts": "input/episode_bundle/scene_prompts.json"
    },
    "input_summary": {
        "series": metadata.get("series"),
        "tags": metadata.get("tags", []),
        "script_length_chars": len(script_text),
        "scene_prompt_count": len(scene_prompts)
    },
    "scene_summary": [
        {
            "scene_id": scene.get("scene_id", f"scene_{i+1:02}"),
            "prompt": scene.get("prompt", ""),
            "narration": scene.get("narration", "")
        }
        for i, scene in enumerate(scene_prompts)
    ],
    "paths": {
        "final_video": "final_video.mp4",
        "thumbnail": "thumbnail.png",
        "scene_frames_dir": "scene_frames",
        "teaser_clips_dir": "teaser_clips"
    },
    "counts": {
        "scene_frames": len(list((OUTPUT / "scene_frames").glob("*.png"))),
        "teaser_clips": len(list((OUTPUT / "teaser_clips").glob("*.mp4")))
    }
}
json.dump(manifest, open(OUTPUT / "media_manifest.json", "w"), indent=2)
print("media_bundle v0.3 created")
