#!/usr/bin/env bash
# Compress every downloaded glTF into a meshopt + WebP GLB.
# Usage: optimize_models.sh DOWNLOAD_DIR OUTPUT_DIR [texture_size]
set -euo pipefail
IN="$1"; OUT="$2"; SIZE="${3:-1024}"
mkdir -p "$OUT"
for g in "$IN"/*/*.gltf; do
  name=$(basename "$(dirname "$g")")
  npx --yes @gltf-transform/cli optimize "$g" "$OUT/$name.glb" \
    --compress meshopt --texture-compress webp --texture-size "$SIZE" --simplify false
done
