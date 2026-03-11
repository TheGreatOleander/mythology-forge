
import json, shutil
from pathlib import Path

INPUT = Path("input/episode_bundle")
OUT = Path("output/media_bundle")

# deterministic run: wipe old outputs
if OUT.exists():
    shutil.rmtree(OUT)

SCENE_FRAMES = OUT / "scene_frames"
TEASER = OUT / "teaser_clips"

SCENE_FRAMES.mkdir(parents=True, exist_ok=True)
TEASER.mkdir(parents=True, exist_ok=True)

bundle = json.load(open(INPUT/"bundle.json"))
metadata = json.load(open(INPUT/"metadata.json"))
scene_prompts = json.load(open(INPUT/"scene_prompts.json"))

episode_id = bundle["episode_id"]

(OUT/"final_video.mp4").write_bytes(b"VIDEO_PLACEHOLDER_V5")
(OUT/"thumbnail.png").write_bytes(b"THUMB_PLACEHOLDER_V5")

scene_asset_map = []

for i,scene in enumerate(scene_prompts,1):
    sid = scene["scene_id"]
    frame = f"{sid}.png"
    clip = f"teaser_{i:02}_{sid}.mp4"
    
    (SCENE_FRAMES/frame).write_bytes(f"FRAME::{sid}".encode())
    (TEASER/clip).write_bytes(f"TEASER::{sid}".encode())
    
    scene_asset_map.append({
        "scene_id":sid,
        "frame":f"scene_frames/{frame}",
        "teaser_clip":f"teaser_clips/{clip}",
        "prompt":scene["prompt"],
        "narration":scene["narration"]
    })

json.dump(scene_asset_map, open(OUT/"scene_asset_map.json","w"), indent=2)

manifest={
 "bundle_version":"1.0",
 "source_episode_id":episode_id,
 "generated_by":"Mythology Forge",
 "paths":{
  "video":"final_video.mp4",
  "thumbnail":"thumbnail.png",
  "scene_frames":"scene_frames",
  "teaser_clips":"teaser_clips",
  "scene_asset_map":"scene_asset_map.json"
 }
}

json.dump(manifest, open(OUT/"media_manifest.json","w"), indent=2)

print("media_bundle v0.5 created (deterministic)")
