import json
import shutil
from pathlib import Path

MEDIA = Path("/sdcard/mythology-forge/output/media_bundle")
SHORTS = MEDIA / "shorts_bundle"

def main():
    scene_asset_map = MEDIA / "scene_asset_map.json"
    if not scene_asset_map.exists():
        print("scene_asset_map.json not found")
        return

    if SHORTS.exists():
        shutil.rmtree(SHORTS)
    SHORTS.mkdir(parents=True, exist_ok=True)

    scenes = json.loads(scene_asset_map.read_text(encoding="utf-8"))
    shorts = []

    for idx, scene in enumerate(scenes, start=1):
        short_name = f"short_{idx:02}_{scene['scene_id']}.mp4"
        short_path = SHORTS / short_name
        short_path.write_bytes(f"SHORT::{scene['scene_id']}".encode())
        shorts.append({
            "short_id": short_name.replace(".mp4", ""),
            "source_scene": scene["scene_id"],
            "path": f"shorts_bundle/{short_name}",
            "platform_targets": ["youtube_shorts", "tiktok", "instagram_reels"]
        })

    manifest = {"bundle_version": "1.0", "generated_by": "Mythology Forge", "shorts": shorts}
    (MEDIA / "shorts_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("shorts_bundle created")

if __name__ == "__main__":
    main()
