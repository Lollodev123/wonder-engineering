# Prompt template — p5.js monitor wall (FALLBACK)

> Use only when the user explicitly opts into `tech: p5`. The default for new concepts is `tech: gsap-three` (see [`gsap-three-monitor-wall.md`](./gsap-three-monitor-wall.md)). p5 lacks GSAP's timeline depth and Three's 3D scene; it's appropriate for fast prototypes only.

The chrome-pilot pastes this template into Claude Design after the `_design-context-block.md` preamble, then fills the `<<SLOT: ...>>` markers.

---

## Task

Generate a single self-contained HTML file that loads p5.js from CDN and runs a 6-second looping sketch implementing the kinetic monitor wall described in the design context block above.

## Slots

Same set as the GSAP template (see [`gsap-three-monitor-wall.md`](./gsap-three-monitor-wall.md)). The chrome-pilot fills them identically.

## Implementation requirements

- Single HTML file. Load p5.js from `https://cdn.jsdelivr.net/npm/p5@1.9.4/lib/p5.min.js`.
- **Background `#1A1A1F`** — never white. Render a subtle vignette around canvas edges.
- **State machine**: `IDLE | TRANSITIONING | REVEAL | RETURNING`, derived each frame from `loopT = (millis() / 1000) % 6.0`.
- **Wave**: `y_offset = 18 * sin(2π * t / 4.0 + col * 0.45 + row * 0.18)` px. Y-only. No x drift in idle.
- **Stage ② transitions**: 6 detaching tiles share one timeline (lift 0.45 → travel 0.75 → land 0.30 s) using a `cubic-bezier(0.16, 1, 0.3, 1)` easing function (implement as `t => 1 - Math.pow(1 - t, 4)` for close approximation).
- **Stage ③ zoom**: focused tile scales 1.10 → 4.0 over 1.6 s; others recede to 0.85 + opacity 0.30.
- **Tile content** painted with p5's `drawingContext` for gradient fills + image slices. Three font sizes: 60% tile-h for NUMBER, 20px for TEXT headline, 13 px for sub.
- **Tap pulse** at `t = 2.5` — radial expand from canvas center, 200 ms, opacity 0.45 → 0, scale 0 → 1.4×monitorW.
- **`#replay` button** at canvas bottom-center, same style as the GSAP version.
- **Public hooks**: `window.replayLoop()`, `window.setLoopT(t)`, `window.captureLoop(seconds)` — same contracts as the GSAP version. `captureLoop` records the p5 canvas via `canvas.captureStream(60)` + `MediaRecorder`.

## Three hard motion rules — same as GSAP version

1. No collision (geometric validator at sketch startup).
2. Vertical-or-sine motion only.
3. Phase-shifted but synchronized.

## Don't

- Don't use any p5 addon (no p5.sound, no p5.dom helpers — vanilla DOM is fine).
- Don't render against a white surface. Background is dark gallery `#1A1A1F`.
- Don't deviate from the 6.0 s loop, 5×3 grid, anchors, or the three hard motion rules.

## Deliverable

Return the entire HTML file in a single fenced ```html code block. No prose around it.
