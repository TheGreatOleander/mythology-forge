import json, os
INPUT="input/episode_bundle/bundle.json"
OUT="output/media_bundle"
os.makedirs(OUT,exist_ok=True)
with open(INPUT) as f: bundle=json.load(f)
open(f"{OUT}/final_video.mp4","wb").write(b"VIDEO")
open(f"{OUT}/thumbnail.png","wb").write(b"THUMB")
manifest={
 "bundle_version":"1.0",
 "source_episode_id":bundle["episode_id"],
 "generated_by":"Mythology Forge",
 "paths":{"final_video":"final_video.mp4","thumbnail":"thumbnail.png"}
}
json.dump(manifest,open(f"{OUT}/media_manifest.json","w"),indent=2)
print("media_bundle created")
