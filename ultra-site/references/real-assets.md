# Real asset pipeline

## 1. Find models (Poly Haven, CC0)

```bash
curl -s -A "site-builder/1.0" "https://api.polyhaven.com/assets?type=models" -o models.json
python -I -c "import json;d=json.load(open('models.json'));[print(k,'|',','.join(v['categories'])) for k,v in d.items()]" | grep -iE "bust|laptop|circuit|watch|hammer|camera|chess|statue|clock"
```

Good picks by theme:

| Theme | Model ids |
|---|---|
| Craft, classical, premium | `marble_bust_01`, `lion_head`, `horse_head`, `gothic_statue` |
| Web, software | `classic_laptop` (its screen material is blank, perfect for a live canvas) |
| Backend, hardware | `circuit_board` |
| Mobile, wearables | `digital_wrist_watch` |
| Making, building | `cross_pein_hammer`, `Drill_01`, `flathead_screwdriver` |
| Strategy | `chess_set` |
| Media | `Camera_01`, `Television_01` |

## 2. Download glTF with all its files

```python
import json, urllib.request, os
def get(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "site-builder/1.0"})
    open(dest, "wb").write(urllib.request.urlopen(req).read())
info = json.load(urllib.request.urlopen(urllib.request.Request("https://api.polyhaven.com/files/marble_bust_01", headers={"User-Agent": "site-builder/1.0"})))
e = info["gltf"]["2k"]["gltf"]
get(e["url"], "dl/marble_bust_01/" + os.path.basename(e["url"]))
for path, v in e["include"].items():
    get(v["url"], "dl/marble_bust_01/" + path)
```

HDRI: `https://api.polyhaven.com/files/studio_small_09` then `["hdri"]["1k"]["hdr"]["url"]`.

## 3. Compress

```bash
npx @gltf-transform/cli optimize in.gltf public/models/name.glb \
  --compress meshopt --texture-compress webp --texture-size 1024 --simplify false
npx @gltf-transform/cli inspect public/models/name.glb --format md   # bounds, materials
```

Typical result: 2 to 4 MB of glTF becomes 200 to 850 KB. Load with
`new GLTFLoader().setMeshoptDecoder(MeshoptDecoder)`.

## 4. Learn orientation before coding layouts

Render front and side thumbnails headless with Blender (`blender -b --factory-startup --python thumbs.py -- dl out`),
import each glTF, frame its bounding box, render 512 px PNGs. glTF +Z is the front (Blender -Y).

## 5. Earth

`https://cdn.jsdelivr.net/gh/mrdoob/three.js@r170/examples/textures/planets/` →
`earth_atmos_2048.jpg`, `earth_lights_2048.png`, `earth_specular_2048.jpg`, `earth_clouds_1024.png`.
The clouds PNG is palette based with the clouds in alpha: convert it to a grayscale density map (luminance × alpha) before sampling `.r`.

## 6. Logos

`npm i simple-icons` then `import { siReact } from 'simple-icons'` → `si.path`, `si.hex`, `si.title`.

## 7. The client's real work

```bash
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
"$EDGE" --headless=new --hide-scrollbars --virtual-time-budget=9000 --window-size=1440,900 \
  --screenshot="C:\\path\\shot.png" "https://user.github.io/repo/"
```

Convert to 1200×750 WebP (Pillow, quality 80). Pull repo metadata from
`https://api.github.com/users/<user>/repos?per_page=100&sort=updated` and keep a JSON snapshot as an offline fallback.

## 8. Share image

Render the hero object in Blender Cycles with the same HDRI plus an accent rim light on a transparent film,
then compose 1200×630 with Pillow using the site's real typeface (Google Fonts serves TTF to an old user agent).
