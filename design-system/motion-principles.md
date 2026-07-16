# Motion principles — kinetic monitor wall

Parameter source: [`tokens.json`](./tokens.json) — `monitorWall.*` and `easing.*`. Anonymized visual observations live in [`reference/visual-anchors.md`](./reference/visual-anchors.md).

> **The deliverable is a kinetic-motion video, not a website.** This document codifies the *motion language* observed in the reference videos. It does not describe layout, typography, or web aesthetics.

---

## The three hard rules (locked, scored on the rubric)

These are design targets for generated concepts. Their enforcement differs by layer; see the implementation note under Rule 1.

### Rule 1 — No collision

> Monitors must never overlap or collide.

- **Python motion lab:** `collision_safe()` checks vertical neighbours at 60 evenly spaced samples. This catches sampled overlap for those primitives only.
- **HTML transition:** the mapper follows layout rules and the critic inspects the rendered loop. There is no continuous-path solver in this public snapshot.
- **Reveal and return:** scale, translation, and the loop seam require visual review.
- **Physical installation:** monitor thickness, motors, load, calibration, and emergency behavior are outside this repository.

The word “safe” in diagnostic output means “no sampled vertical overlap found,” not hardware certification.

### Rule 2 — Vertical-or-sine motion only

> Each monitor moves only vertically (y-axis) **or** in a way that follows a smooth sine wave motion.

- **Idle motion is y-only.** No drift in x. The wave is `y_offset(col, row, t) = amplitude * sin(2π * t / period + col * phaseStepCol + row * phaseStepRow)`. Lateral position is fixed at `gridX(col)`.
- **Transition** is the only stage where lateral motion is allowed, and only as a *deliberate one-shot eased path* from grid slot to landing slot. Once landed, the tile is again static in x.
- **Receded tiles in Stage ③** continue their wave (y-only) but at reduced amplitude (`× 0.4`) and longer period (`× 1.6`).
- **Return** reverses the deliberate lateral path. Once back in slot, tile is y-only again.
- **Forbidden everywhere**: idle drift, swirl, rotational tile motion, depth-axis motion (other than scale during reveal). The wall reads as a wall.

### Rule 3 — Phase-shifted but synchronized

> Motion should feel continuous, elegant, and synchronized — but slightly phase-shifted across the grid.

- **All tiles share one period** (`periodSec = 4.0`) and one amplitude (`amplitudePx = 18`).
- **Per-tile phase** = `col * 0.45 + row * 0.18` radians. Adjacent column ≈ 26° apart; adjacent row ≈ 10°. The wave reads as a *travelling sine from left to right* with a faint vertical lag — never as scattered noise.
- **No randomness.** Phase is deterministic from `(col, row)`. The same monitor in two different concepts uses the same phase. This is what gives the wall its "elegant + synchronized" character.
- **Stage transitions are also synchronized.** All 6 detaching tiles share one timeline (max ±80 ms phase variance — beyond that the eye reads broken sync).

---

## The 3-stage choreography (6.0 s loop)

| Stage | Window | Duration | Motion summary |
|---|---|---|---|
| ① Dynamic Product Showcase | 0.0 – 2.5 s | 2.5 s | All 15 monitors in sine wave (Rule 2). Gradients flow. Some tiles can collectively render one product image spanning multiple tiles (see "Tile-spanning imagery" below). |
| ② Interactive Exploration  | 2.5 – 4.0 s | 1.5 s | Tap pulse on canvas. 6 outer-ring tiles detach with eased path (cinematic curve) to landing positions. Anchor tiles continue wave at full amplitude. |
| ③ Deeper Product Layers    | 4.0 – 5.6 s | 1.6 s | One detached tile zooms 4× and centers; others recede to 30% opacity at 0.85× scale. Anchor wave dampens to 40% amplitude. Floating role-tag bubbles + connection lines may fade in (see kinetic-motion-language.md). |
| Return                     | 5.6 – 6.0 s | 0.4 s | Return through the same path; inspect the rendered seam. |

## Easing palette

- **`cinematic`** = `cubic-bezier(0.16, 1, 0.3, 1)` — gentle overshoot. Default for detach + zoom.
- **`snappy`** = `cubic-bezier(0.4, 0, 0.2, 1)` — material standard. UI affordances (tap pulse).
- **`wave`** = linear. Sine driver only.

## Cardinal motion rules (beyond the three hard rules)

1. **One axis at a time per tile per beat.** While a tile is moving (lateral travel), its content is static. While its content animates (gradient flow, callout fade-in), its position is still. The reference videos enforce this rigidly.
2. **Center monitors never detach.** Five anchors: `(1,1) (2,1) (3,1) (2,0) (2,2)`. They hold the wall together visually and provide the wave continuity through Stage ③.
3. **Detached tiles arrive together.** All 6 share one cinematic timeline (±80 ms variance).
4. **Stage ③ focus rotates.** `loopIndex % numFeatures` selects the focused feature deterministically. Two consecutive loop plays show different features.
5. **60 fps target, GPU-accelerated transforms.** If the chosen tech is DOM, use `transform: translate3d(...)` (compositor-only). If WebGL, use uniforms not geometry rebuilds.

## Capture for delivery

- 6.0 s, 60 fps, `MediaRecorder` on `canvas.captureStream(60)` → `loop.webm`.
- ffmpeg converts to H.264 yuv420p `loop.mp4` for PowerPoint.
- Hero still sampled at `t = 1.2 s` (mid-Stage ①), 1920×1080.
- Stage stills at `t = 1.2`, `3.2`, `4.8` for the three stages.

The checked-in worked artifact is an earlier 14-second state study. New concepts generated through the command workflow target the six-second timing above.
