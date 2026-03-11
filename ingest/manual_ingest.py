
import os
import json
import shutil
import datetime

def create_bundle(video_path, title, forge_root):
    episode_id = "manual_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(forge_root, "input", "episode_bundle")

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    os.makedirs(out_dir, exist_ok=True)

    bundle = {
        "bundle_version": "1.0",
        "project": "manual_ingest",
        "episode_id": episode_id,
        "title": title,
        "topic": title,
        "paths": {
            "script": "script.txt",
            "metadata": "metadata.json",
            "scene_prompts": "scene_prompts.json",
            "episode_plan": "episode_plan.json"
        }
    }

    with open(os.path.join(out_dir, "bundle.json"), "w") as f:
        json.dump(bundle, f, indent=2)

    metadata = {
        "series": "Manual Import",
        "tags": ["manual", "video", "forge"],
        "tone": "custom"
    }

    with open(os.path.join(out_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    with open(os.path.join(out_dir, "script.txt"), "w") as f:
        f.write(f"Manual video import: {title}")

    scene_prompts = [{
        "scene_id": "scene_01",
        "prompt": "manual source video clip",
        "narration": "Imported external video."
    }]

    with open(os.path.join(out_dir, "scene_prompts.json"), "w") as f:
        json.dump(scene_prompts, f, indent=2)

    episode_plan = {
        "hook": title,
        "beats": [
            "import video",
            "prepare forge processing",
            "render media bundle"
        ],
        "target_duration_sec": 60
    }

    with open(os.path.join(out_dir, "episode_plan.json"), "w") as f:
        json.dump(episode_plan, f, indent=2)

    shutil.copy(video_path, os.path.join(out_dir, "source_video.mp4"))

    print("Manual episode_bundle created:", out_dir)
