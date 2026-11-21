"""Download Poly Haven glTF models (with every texture) and one HDRI.

Usage:
  python -I fetch_polyhaven.py OUT_DIR marble_bust_01:2k classic_laptop:1k --hdri studio_small_09:1k
All Poly Haven assets are CC0. Credit them anyway.
"""
import json, os, sys, urllib.request

UA = {"User-Agent": "site-builder/1.0"}

def get_json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA)))

def get(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA)) as r, open(dest, "wb") as f:
        f.write(r.read())

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    out = args.pop(0)
    hdri = None
    if "--hdri" in args:
        i = args.index("--hdri"); hdri = args[i + 1]; del args[i:i + 2]
    for spec in args:
        name, _, res = spec.partition(":"); res = res or "1k"
        e = get_json(f"https://api.polyhaven.com/files/{name}")["gltf"][res]["gltf"]
        base = os.path.join(out, name)
        get(e["url"], os.path.join(base, os.path.basename(e["url"])))
        for path, v in e.get("include", {}).items():
            get(v["url"], os.path.join(base, path))
        print("model", name, res)
    if hdri:
        name, _, res = hdri.partition(":"); res = res or "1k"
        h = get_json(f"https://api.polyhaven.com/files/{name}")["hdri"][res]["hdr"]
        get(h["url"], os.path.join(out, "hdri", f"{name}_{res}.hdr"))
        print("hdri", name, res)

if __name__ == "__main__":
    main()
