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

## 7. The fluid hero (what finally landed with the client)

When the client shows a reference, extract frames with `ffmpeg -i ref.mp4 -vf "fps=4,scale=512:-1,tile=4x4" -frames:v 1 sheet.jpg`
and read the contact sheet before designing. The winning pattern:

- **Intro as a story, not a spinner.** One spark with a ring of real downloaded bytes; then a cross of dots, an
  iridescent dot field opening from the centre, and a diagonal metaball wave that melts into the hero colour.
  Canvas 2D is enough; finish on exactly the hero background so the hand off is seamless.
- **One bold flat colour** that means something for the brand (forge → molten orange), black type, black ink.
- **Wordmark inside WebGL.** Draw the giant word plus a handwritten script word (for example Yellowtail) into a
  canvas texture on a full screen quad, so the ink can flow over the letters. Render a background scene
  (aura, wordmark, ink) first, then the 3D scene with `clear = false, clearDepth = true`.
- **Real fluid, not a video.** Stable fluids on the GPU: splat, curl, vorticity, divergence, ~18 Jacobi pressure
  iterations, gradient subtract, advect velocity and dye. Velocity 128 px, dye 1024 px (512 on phones), half
  float targets. Shade the dye as glossy ink: alpha from density, normals from its gradient, a tight specular.
  The cursor splats with its real velocity; the object sheds swirling splats around its projected silhouette.
  Scale emission down on phones or the ink swallows the layout.
- **A real, licensed hero object.** Search GitHub for models already used in open tutorials and read the glTF
  `asset.extras` for author and licence (CC BY needs visible credit). Hide trademark logos, convert to meshopt,
  swap the screen material for a canvas, convert body materials to `MeshPhysicalMaterial` with iridescence for
  holographic chrome.
- **Real content on screens.** Capture full length mobile pages through the DevTools protocol
  (`Emulation.setDeviceMetricsOverride` 390×844, scroll once to trigger reveals, `captureBeyondViewport`), then
  scroll them inside a Safari style canvas with human pacing: hold, flick with momentum, settle, swipe tabs.

## 8. The second edition under the ink (v4)

The client's next step after the fluid hero: whatever the ink touches should show an
alternate version of the scene, not just a dark stain.

- **Reveal, don't paint.** Feed the fluid dye texture to every layer that should change.
  The wordmark shader mixes black to white letters where `dye > threshold`; the ink itself
  stays black, so the white letters read as "inside" the ink.
- **Only the content changes.** On a device, patch only the screen material (`onBeforeCompile`,
  replace `#include <emissivemap_fragment>`). Sample the dye with `gl_FragCoord.xy / drawingBufferSize`
  so the screen and the 2D fluid line up exactly. Never recolour the device body.
- **Pixel by pixel.** Quantise screen UVs into cells (about 64 columns). Each cell gets a hash, and
  its flip threshold is `0.1 + hash * 0.3`, so cells switch one at a time at the ink's edge
  instead of fading as a block. The alternate look is a duotone remap of the same page.
- **Site changes as VFX.** Keep the previous frame in a second canvas texture. A front sweeps
  down the screen with a jittered edge per cell and a hot scan band; above the front show the new
  page, below it the old one.
- **Chain shader patches.** If the material already has a dissolve patch, call
  `material.userData.extraPatch(shader)` from inside it and give it a distinct
  `customProgramCacheKey`. Rename any clashing local variables (`band` became `sband`).
- **One site, two screens.** A laptop behind a smaller phone, both driven by one `Pacer`
  (hold, flick, glide back to top), sells responsive design better than any claim. Use a
  real MIT or CC laptop model, replace its screen material, and set `flipY = false` on
  canvas textures that land upside down.
- **Size by feel.** The client asked for the hero phone at 70% of the first size; leave room for the
  wordmark to read around it.
