# Stage architecture

## Scene graph per shot

```
pivot (layout: position/scale per breakpoint, recomputed on resize)
 └─ spin (idle motion, cursor parallax, strikes)
     └─ norm (centres the model and scales it to unit height or unit max dimension)
         └─ gltf.scene
```

Particles for a shot are sampled in `spin` space, so `uFromM = A.spin.matrixWorld` and
`uToM = B.spin.matrixWorld` keep particles glued to the moving object.

## Scroll → shot float

Group consecutive `[data-shot]` elements with the same id. For pinned sections measure the
`.pin-spacer` parent. For each group: hold from `top - 0.15vh` to `bottom - 0.85vh`, then
interpolate to the next group's `top - 0.15vh`. Rebuild on `ScrollTrigger` refresh.

```js
const holdEnd = Math.max(cur.top - 0.15 * vh, cur.bottom - 0.85 * vh);
const nextStart = next.top - 0.15 * vh;
if (y <= holdEnd) return cur.index;
if (y < nextStart) return cur.index + (y - holdEnd) / (nextStart - holdEnd);
```

## Per frame, between shot A and B at t

- `morph = smoothstep(0.08, 0.92, t)`
- mesh A dissolve `smoothstep(0, 0.32, t)`, mesh B dissolve `1 - smoothstep(0.68, 1, t)`
- particle opacity `max(mix(restA, restB, t), sin(πt)^0.6)`; `rest` is 0 for meshes, 1 for procedural shots

## Morph field (one draw call)

- N = 256 × 112 desktop, 256 × 48 mobile. Targets live in `DataTexture`s (RGBA float positions with size in w,
  RGBA8 colours). Swapping shots is a uniform swap, zero uploads.
- Sample real meshes with `MeshSurfaceSampler.sample(p, n, c, uv)` and read the albedo at `uv`
  from a 256 px canvas copy of `material.map.image` (glTF textures are not flipped).
- Vertex shader: staggered departure `t = clamp((uMorph - rand * 0.45) / 0.55)`, curl noise only while
  `0 < uMorph < 1` (uniform branch keeps idle frames cheap), cursor repulsion on the z = 0 plane,
  colour runs hot (accent) mid flight, `uInkMix` darkens particles on light themes.

## Forge dissolve on real PBR materials

`material.onBeforeCompile`: add world position varying; at the top of `main` discard where
`snoise(worldPos * scale) < uDissolve`; after `emissivemap_fragment` add `uEdge * edge * 7.0` where
`edge = 1 - smoothstep(0, 0.07, n - uDissolve)`. Set `customProgramCacheKey`.

Hero scan variant: below `uScanY` discard everything except contour slices
`smoothstep(0.36, 0.47, abs(fract(y * 26) - 0.5))`, tint them with the accent and add fresnel.
The scan line follows the cursor's world Y over the hero and sweeps on its own otherwise.

## Live screen on a scanned laptop

Find the mesh whose material name contains `screen`. It has no UVs, so build planar UVs: area weighted normal
`n`, `v = normalize(up - n * dot(up, n))`, `u = cross(v, n)`, project and normalise. Material:
`MeshStandardMaterial({ color: black, emissive: white, emissiveMap: canvasTexture, roughness: 0.18 })`.
Redraw the canvas only while the laptop is visible.

## Earth that tells the truth

Subsolar point: declination `-23.44 * cos(2π/365 * (dayOfYear + 10))`, longitude `(12 - utcHours) * 15`.
Convert lat/lon with the SphereGeometry convention `phi = lon + 180`:
`(-cos φ cos θ, sin θ, sin φ cos θ)`. Light in Earth local space so geography and terminator agree.
Point the globe at the visitor with `-getTimezoneOffset()/60*15` longitude, no geolocation prompt.

## One clock

`lenis.raf` and `stage.update` both run on `gsap.ticker`; `lenis.on('scroll', ScrollTrigger.update)`;
`gsap.ticker.lagSmoothing(0)`. Adaptive DPR drops by 0.25 after two seconds under 40 fps.
