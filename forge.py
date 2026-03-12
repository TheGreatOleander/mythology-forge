import json
import shutil
import subprocess
from pathlib import Path

INPUT = Path("input/episode_bundle")
OUT = Path("output/media_bundle")

UPSTREAM_VIDEO = INPUT / "episode.mp4"
UPSTREAM_FRAME = INPUT / "episode_frame.png"

if OUT.exists():
    shutil.rmtree(OUT)

SCENE_FRAMES = OUT / "scene_frames"
TEASER = OUT / "teaser_clips"

SCENE_FRAMES.mkdir(parents=True, exist_ok=True)
TEASER.mkdir(parents=True, exist_ok=True)

bundle = json.load(open(INPUT / "bundle.json"))
metadata = json.load(open(INPUT / "metadata.json"))
scene_prompts = json.load(open(INPUT / "scene_prompts.json"))

episode_id = bundle["episode_id"]

video_out = OUT / "final_video.mp4"
thumb_out = OUT / "thumbnail.png"

def is_real_png(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    try:
        with path.open("rb") as f:
            return f.read(8) == b"\x89PNG\r\n\x1a\n"
    except OSError:
        return False

def ffmpeg_available() -> bool:
    try:
        proc = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return proc.returncode == 0
    except FileNotFoundError:
        return False

HAS_FFMPEG = ffmpeg_available()

# ------------------------------------------------
# Prefer real upstream media
# ------------------------------------------------

used_real_video = False
used_real_thumb = False

if UPSTREAM_VIDEO.exists() and UPSTREAM_VIDEO.stat().st_size > 0:
    shutil.copy(UPSTREAM_VIDEO, video_out)
    used_real_video = True
else:
    video_out.write_bytes(b"VIDEO_PLACEHOLDER_V7")

if is_real_png(UPSTREAM_FRAME):
    shutil.copy(UPSTREAM_FRAME, thumb_out)
    used_real_thumb = True
else:
    thumb_out.write_bytes(b"THUMB_PLACEHOLDER_V7")

# ------------------------------------------------
# If we have real video + ffmpeg, derive thumbnail
# ------------------------------------------------

if used_real_video and HAS_FFMPEG:
    thumb_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_out),
        "-frames:v",
        "1",
        str(thumb_out),
    ]
    proc = subprocess.run(thumb_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if proc.returncode == 0 and is_real_png(thumb_out):
        used_real_thumb = True

# ------------------------------------------------
# Scene assets + teaser clips
# ------------------------------------------------

scene_asset_map = []

for i, scene in enumerate(scene_prompts, 1):
    sid = scene["scene_id"]
    frame_name = f"{sid}.png"
    clip_name = f"teaser_{i:02}_{sid}.mp4"

    frame_path = SCENE_FRAMES / frame_name
    clip_path = TEASER / clip_name

    # frame placeholders for now
    frame_path.write_bytes(f"FRAME::{sid}".encode())

    # If real video exists, try to slice a teaser clip
    if used_real_video and HAS_FFMPEG:
        start_sec = max(0, (i - 1) * 1)
        teaser_cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            str(start_sec),
            "-i",
            str(video_out),
            "-t",
            "2",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(clip_path),
        ]
        proc = subprocess.run(teaser_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if proc.returncode != 0 or not clip_path.exists():
            clip_path.write_bytes(f"TEASER::{sid}".encode())
    else:
        clip_path.write_bytes(f"TEASER::{sid}".encode())

    scene_asset_map.append({
        "scene_id": sid,
        "frame": f"scene_frames/{frame_name}",
        "teaser_clip": f"teaser_clips/{clip_name}",
        "prompt": scene["prompt"],
        "narration": scene["narration"],
    })

json.dump(scene_asset_map, open(OUT / "scene_asset_map.json", "w"), indent=2)

manifest = {
    "bundle_version": "1.0",
    "source_episode_id": episode_id,
    "generated_by": "Mythology Forge",
    "used_real_video": used_real_video,
    "used_real_thumbnail": used_real_thumb,
    "ffmpeg_available": HAS_FFMPEG,
    "paths": {
        "video": "final_video.mp4",
        "thumbnail": "thumbnail.png",
        "scene_frames": "scene_frames",
        "teaser_clips": "teaser_clips",
        "scene_asset_map": "scene_asset_map.json",
    },
}

json.dump(manifest, open(OUT / "media_manifest.json", "w"), indent=2)

print("media_bundle v0.7 created (real-media + teaser aware)")
