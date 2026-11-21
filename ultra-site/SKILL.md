---
name: ultra-site
description: Build an award level portfolio, studio or agency website where the whole page is one continuous hero. A fixed WebGL stage morphs between real photoscanned 3D models as you scroll, every section has its own theme, every headline word animates the way it means, a Why mode explains each motion, proof numbers are measured live, the footer is a hero of its own, and the result ships to GitHub Pages. Use when someone asks for an extremely advanced, premium, 3D, animated, "as advanced as possible" or "billion dollar" website, portfolio or landing page, or asks to recreate the ARFORGE approach.
---

# Ultra site

This skill builds a site that looks like a big company's flagship launch page, using only real assets and honest data. The reference build is ARFORGE (https://github.com/ArfatArfart/arforge, live at https://arfatarfart.github.io/arforge/). Read its source when you need working code for any step below.

## Non negotiables

1. **Real assets only in 3D.** Never model a "fake" hero object out of primitives. Use photoscanned CC0 models (Poly Haven), real HDRIs, real NASA textures, real logos (Simple Icons), real screenshots of the client's own live work. Credit every source in the footer.
2. **One stage, many shots.** A single fixed `<canvas>` sits behind the page. Each section declares `data-shot` and `data-theme`. Scroll position becomes a float (2.4 means 40% from shot 2 to shot 3).
3. **Every section is a hero.** Full viewport, display type, its own theme, its own 3D moment. The footer included.
4. **Semantic motion.** Every animated word moves the way it means. Each effect stores a one sentence reason. Ship a Why mode (`W` key) that pins those reasons on screen.
5. **Proof over claims.** Never invent stats, clients or testimonials. Show numbers the browser measures (fps, frame time, points drawn, draw calls, bytes, time to first frame) and data fetched live (GitHub repos, API latency).
6. **Ship it.** Vite build with `base` set to the repo path, a GitHub Actions Pages workflow, the repo created and Pages enabled, and a verified live URL.

## Workflow

1. **Concept (5 minutes, no questions unless blocked).** Pick a studio name and one metaphor that every visual decision can derive from (ARFORGE: a forge, so dissolves glow like hot metal, process steps are hammer strikes, embers rise). Write copy in sentence case, no filler words, no hyphens inside sentences.
2. **Source assets.** Follow `references/real-assets.md`. Query the Poly Haven API, download glTF at 1k (2k for the hero), compress with gltf-transform (meshopt + WebP), inspect bounds, render Blender thumbnails to learn each model's orientation. Screenshot the client's live projects with headless Edge or Chrome.
3. **Scaffold.** Vite + three + gsap (all plugins are free: SplitText, ScrambleText, ScrollTrigger) + lenis + @fontsource-variable/geist. One stylesheet of tokens, eleven themes as CSS variables tweened by GSAP.
4. **Build the stage.** Follow `references/stage-architecture.md`: morph field sampled from the real meshes, forge dissolve patched into the real PBR materials, procedural shots for sections without an object, embers, sparks, an Earth with the real subsolar point.
5. **Build the sections.** Hero (scan shader on the hero object, HUD with real mesh stats), tagline reveal, three service chapters (each with a real object and an interactive proof: live canvas screen, draggable phone demo, terminal of real requests), pinned process with impacts, live work grid, draggable tech sphere, live metrics, FAQ, footer hero with globe and heat type.
6. **Semantic words.** Use the catalog in `references/semantic-motion.md`. Every heading gets at least two effects; never reuse an effect within one heading.
7. **QA in the browser pane.** Check desktop and the mobile preset, read console errors, confirm no horizontal overflow at 375px. A hidden browser pane throttles requestAnimationFrame, so slow intros there are not bugs.
8. **Deploy.** See `references/deploy.md`. Create the repo, enable Pages with `build_type=workflow`, push, wait for the run, open the live URL and check the console there too.

## Quality bar

- Hero headline readable over the 3D object (text shadow or layout clearance).
- Motion uses `cubic-bezier(0.22, 1, 0.36, 1)` or GSAP expo/elastic, never linear for UI.
- `prefers-reduced-motion` turns effects into fades and disables smooth scroll.
- Adaptive pixel ratio: drop DPR when fps stays under 40.
- Skip link, focus rings, aria labels on split text, alt text on screenshots, privacy and terms dialogs, branded 404, OG image rendered from the real hero object.
- Mobile: 3D owns the top of the viewport, copy sits on frosted cards below.
