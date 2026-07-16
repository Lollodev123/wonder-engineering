# Design context block (paste at top of every Claude Design prompt)

> You are designing a **kinetic monitor-wall pre-visualization video** from the local design contract and anonymized motion-reference notes. The output is a single self-contained HTML file that runs a 6-second looping animation on localhost. The animation is a procedural mock of a physical kinetic exhibit: a 5×3 wall of luminous monitors mounted in a dark gallery, idling in synchronized vertical motion before feature content and a focused final beat appear.

## Scene (the look)

- **Dark gallery space, never white.** Background `#1A1A1F` (charcoal). Mild vignette to edges. Subtle ground reflection ~18% under the wall.
- **Three-point lighting**: cool blue fill from upper-left (`#5C68B5` @ 0.20), warm orange rim from upper-right (`#D86937` @ 0.10), white key from above-front (`#FFFFFF` @ 0.45). Lights pick out monitor edges; the wall itself stays dim.
- **Tiles are luminous panels**, not framed boxes. No visible bezel — the screen's gradient *is* the boundary.
- **Optional person silhouette** standing right of the wall at ~70% canvas width, ~1.75 m tall, navy on dark. Toggle on for "live event" feel; off for product-only renders.

## Screen content (vibrant, never flat)

Each tile carries one of:
- **GRADIENT** — two-color vibrant wash (violet→magenta, blue→cyan, magenta→orange, amber→cream, teal→electric, navy→violet). Angle drifts slowly with loop time (360° over 12s).
- **IMAGE-SLICE** — one slice of a tile-spanning product image (e.g. eyewear across 3 tiles). The wall fragments to render one big visual.
- **NUMBER** — single big numeric in white or accent (`5×`, `240+`), fills 50–60% of tile.
- **TEXT** — short headline + sub. White text, 16 px padding.
- **ICON** — single white-stroke glyph centered.
- **CALLOUT** — Stage ③ only: floating translucent-black pill (`rgba(0,0,0,0.55)` bg, white text, ~120×40 px), often with a 1.5 px dashed connection line to the focused tile.

Tiles can collectively render one image (idle) or fragment with feature callouts (reveal). Mix forbidden — one tile, one type. Backgrounds are dark; vibrancy lives only on the screens.

## Geometric template (LOCKED)

- **Canvas**: 1920×1080 logical, responsive.
- **Grid**: 5 cols × 3 rows = 15 monitors. Aspect 16:9. Gap 24 px.
- **Anchors** (never detach): `(1,1) (2,1) (3,1) (2,0) (2,2)`.
- **Detach-eligible**: 12 outer-ring tiles. Stage ② peels exactly 6.
- **Loop**: 6.0 s exactly. Stage ① 0.0–2.5s · ② 2.5–4.0s · ③ 4.0–5.6s · return 5.6–6.0s.

## Three hard motion rules (NON-NEGOTIABLE — these are scored on the rubric)

1. **No visible collision.** Plan the layout so monitor bounding boxes do not overlap, add defensive runtime checks where practical, and surface any failed check instead of rendering through it.
2. **Vertical-or-sine motion only.** Idle motion is `y_offset = 18 * sin(2π * t / 4.0 + col * 0.45 + row * 0.18)` px. **No idle x-drift.** Lateral motion appears only during Stage ② transition or reverse Return — never as ambient. No tile rotation. No depth-axis motion (other than scale during reveal).
3. **Phase-shifted but synchronized.** All tiles share `period = 4.0 s` and `amplitude = 18 px`. Per-tile phase is deterministic: `phase = col * 0.45 + row * 0.18` rad. The wave reads as a *travelling sine from left to right* — never as scattered noise.

## Easing palette

- **`cinematic`** = `cubic-bezier(0.16, 1, 0.3, 1)` — gentle overshoot. Default for detach + zoom.
- **`snappy`** = `cubic-bezier(0.4, 0, 0.2, 1)` — UI affordances (tap pulse).
- Linear for the wave.

## Tech (default for new concepts: `gsap-three`)

- **GSAP timeline** (`gsap.timeline({ repeat: -1, defaults: { ease: 'power3.out' } })`) drives all animation. One timeline, three labels (`stage-1`, `stage-2`, `stage-3`). Use `gsap.registerEase('cinematic', cubicBezier(0.16, 1, 0.3, 1))`.
- **Three.js** renders the gallery: a `Scene` with a back wall plane, ground plane with reflection, 3-point lighting rig, and 15 `PlaneGeometry` meshes for the monitors. Optional `Mesh` for the person silhouette.
- **Tile screen content** is rendered to a per-tile canvas (HTML `<canvas>` or `THREE.CanvasTexture`) — gradients via `createLinearGradient`, image slices via `drawImage` of a generated/loaded source, text via `fillText` with Inter 300.
- CDN: `gsap@3.12.5` + `three@0.160.1`, both single-file, loaded from jsDelivr.

If the brief specifies `tech: gsap-dom`: use GSAP + DOM `<div>` tiles + CSS gradients/transforms instead. No Three.js. Lighter, simpler — but no real gallery depth.

If the brief specifies `tech: p5`: fall back to p5.js with hand-rolled state machine. Allowed only for explicit user opt-in.

## Output requirements

- Single self-contained HTML file. No external assets except CDN libraries.
- Loop length: exactly 6.0 s. Loop seam invisible.
- Expose:
  - `window.replayLoop()` — resets to t=0 for manual replay.
  - `window.captureLoop(seconds)` — returns `Promise<Blob>` of `MediaRecorder`-recorded WebM at 60 fps via `canvas.captureStream(60)`. The preview server's capture button calls this.
  - `window.setLoopT(t)` — for the design-critic to scrub to specific times for stage stills.
- A small `Explore →` pill button at canvas bottom-center for manual replay; auto-fires Stage ② at `t = 2.5` per loop regardless.
- 60 fps target. GPU-accelerated transforms (translate3d for DOM, uniforms for Three).

## Don't

- Don't use a white background.
- Don't add framework dependencies (no React, no Vue, no Tailwind).
- Don't add comments explaining the obvious; only comment a non-obvious *why* (a magic number, a workaround for a library quirk).
- Don't deviate from the 5×3 grid, 6-second loop, four state-machine states, three hard motion rules.
