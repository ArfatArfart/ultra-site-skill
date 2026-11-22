# The premium pass

What turned the first ARFORGE build from "impressive" into "premium", in order of impact.

## 1. A product studio, not a gimmick

Replace effects that read as "techy" (holographic slices, HUD corners, marquees) with product photography:

- **Hero object people recognise.** A phone, a watch, a device. When no licensed scan exists (modern phones
  are all behind Sketchfab logins or paid stores), engineer it to real proportions: extruded rounded slab with
  8 bevel segments for the frame, ShapeGeometry glass with planar UVs, raised camera plateau, lens stacks
  (polished ring, iridescent glass disc, dark torus, glass cap), RoundedBox buttons, antenna bands, port and
  speaker holes. Physically based materials: `MeshPhysicalMaterial` with `anisotropy` on titanium, a
  roughness map that etches the brand mark in gloss on a matte back, `iridescence` on lenses.
  Say it is engineered in code; never pretend it is a scan.
- **Studio environment.** Build a PMREM from a scene of emissive panels (softbox, strips, warm kicker) at
  size 512 and use it as `envMap` on glass and metal. Crisp rectangular reflections read as photography.
- **Area lights.** `RectAreaLight` key, rim and top, plus a narrow sweep light that crosses every ~7 s.
- **Glossy floor.** A mirrored clone (`scale.y = -1` around the floor plane, sharing materials so it dissolves
  with the original) under a floor plane in the background colour that is 66% opaque near the object and
  opaque at the edges. Add an additive light pool and a soft volumetric cone with drifting motes.
- **Scroll turns the product.** 240vh hero with a sticky stage; `heroT` (0..1) rotates the group to show the
  back, swaps the headline for a second statement, and fades in callouts pinned to projected 3D anchors with
  a facing test (`normal · toCamera`).

## 2. Cinematic finish

EffectComposer on desktop only: `WebGLRenderTarget(…, { type: HalfFloatType, samples: 4 })` → RenderPass →
UnrealBloomPass (threshold ~0.96 so only speculars and hot edges bloom) → OutputPass → a final shader with
grain, vignette (weaker on light themes) and a little radial chromatic aberration. Use
`NeutralToneMapping` so screen content and brand colours survive. Set `renderer.info.autoReset = false` and
reset once per frame or your stats only count the last pass. Fall back gracefully: lower DPR first, then
disable bloom when fps stays under 42.

## 3. Damp everything

`damp(a, b, k, dt) = lerp(a, b, 1 - exp(-k·dt))` for the shot float, hero progress, pointer and object
rotations. Lenis `lerp: 0.075`. Nothing snaps.

## 4. Material typography

Fill headings with real photo textures (Poly Haven, re-graded per theme with a luminance → two-tone ramp;
brushed metals get a horizontal box blur). Avoid tile and ribbed sources: grout lines cut through the text.
Implementation: every glyph-holding element gets `.tx` with `background-clip: text`, the texture offset by its
own `--lx/--ly` so the material is continuous, and a specular band positioned by a per-heading `--sx`
updated on pointer move (auto sweep when idle). Pre-split letter effects before measuring, otherwise letters
split later lose the material.

## 5. Usable 3D UI

Render an app to a canvas on the phone's screen material. Anchor the phone to a DOM slot each frame (so it
scrolls with the layout), raycast pointer events from the slot onto the screen mesh, convert uv to canvas
pixels (`y = (1 - v) · height` because CanvasTexture flips), and keep a hidden `role="slider"` for keyboard
and screen reader users.

## 6. Small things people feel

Cursor lit hairline borders (`mask-composite: exclude` ring with a radial gradient at `--gx/--gy`), buttons
lit from above with an inner highlight, themes chosen by position every frame (pinned sections break
toggle based triggers when users jump), `align-content: normal` on tall sticky containers (Chrome now applies
`align-content` to block boxes).
