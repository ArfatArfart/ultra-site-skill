# ultra-site · a Claude Code skill

A skill that teaches Claude Code to build an award level portfolio or studio site where the whole
page is one continuous hero: real photoscanned 3D models on a single WebGL stage, a theme per section,
words that animate the way they mean, a Why mode that explains every motion, live measured proof,
a footer hero and a GitHub Pages deploy.

Reference build: **ARFORGE** · [live](https://arfatarfart.github.io/arforge/) · [source](https://github.com/ArfatArfart/arforge)

## Install

Personal (all projects):

```bash
git clone https://github.com/ArfatArfart/ultra-site-skill
cp -r ultra-site-skill/ultra-site ~/.claude/skills/
```

One project only: copy `ultra-site/` into that project's `.claude/skills/`.

Then ask Claude Code for "a website as advanced as possible" or run `/ultra-site`.

## Contents

```
ultra-site/
  SKILL.md                          the workflow and the quality bar
  references/real-assets.md         Poly Haven, HDRI, NASA, Simple Icons, screenshots, share image
  references/stage-architecture.md  scroll to shot mapping, morph field, forge dissolve, Earth
  references/semantic-motion.md     32 word effects with the reason for each
  references/deploy.md              Vite base, Pages workflow, gh commands
  scripts/fetch_polyhaven.py        download models and HDRIs
  scripts/optimize_models.sh        meshopt + WebP compression
  scripts/blender_thumbs.py         headless thumbnails to learn model orientation
```
