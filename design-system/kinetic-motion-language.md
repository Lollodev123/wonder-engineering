# Kinetic motion language — observed vocabulary

What the reference videos actually show, distilled into reusable patterns. This is the *visual lexicon* every concept draws from.

> The original reference media is intentionally excluded from this public snapshot. An anonymized description of the observations lives in [`reference/visual-anchors.md`](./reference/visual-anchors.md).

---

## Scene grammar

### Dark gallery, never white

Every video is set in a **dark matte gallery**. Walls are charcoal. Lighting is dramatic, soft-volumetric, with cool fill from one side and a warm rim from the other. Ground has a subtle reflection.

- The gallery scene and the screen-content palette are separate systems: the room remains dark while color lives on the monitors.
- Black background isolates the screen content's vibrancy.
- Soft lighting gives depth and "real installation" feel.

### Person silhouette for scale

Several videos include a real photographic human figure interacting with or standing beside the wall. This sells two things instantly: (a) physical scale of the installation, (b) "live event in progress" feel.

- Default: include a silhouette (navy on dark) standing to the right at ~70% canvas width.
- Optional override: omit when the brief specifies "totem" or "kiosk" (single-monitor exhibits don't need a scale figure — the kiosk's dimensions read).

---

## Screen-content vocabulary

### Vibrant gradient backgrounds

Tile screens are filled with **bold gradient washes** in the brand palette: violet→magenta, blue→cyan, magenta→orange, amber→cream, teal→electric. Never flat colors. Never white.

- Idle ambient: each tile carries one gradient. Adjacent tiles use *different* gradients to create a mosaic of color. The wave brings them gently in and out of sync.
- Gradient angle drifts slowly with the loop time (e.g. 360° rotation across 12 s) — adds an "alive" quality without distracting motion.

### Tile-spanning imagery

In *Product Exploration Step 1*, a single product image (eyewear) spans roughly 5 tiles in the middle row. The wall reads as one fragmented hero image, not 15 independent tiles.

- Use when the brief has a strong central product visual (a piece of hardware, a hero portrait, a chart).
- Map: choose a contiguous block of 3–6 tiles, slice the source image, render each slice on its own tile. As tiles wave, the image fragments slightly — that's the kinetic-art signature.

### Big numerics + minimal text

Reveal moments surface single big numbers (`5×`, `50×`, `240+`) with one short sub-label. Not paragraphs. The screens display *one idea*.

- Type: weight 300, white or accent color, fills 50–60% of the tile.
- Sub-label: 13 px, 60% opacity white, below the number.

### Floating callout pills

In *Client Voices Gallery*, role-tag pills (`Software Engineer`, `Marketing & Brand Strategist`) hover near the detached portrait monitors. Pills are translucent black with white text, ~120×40 px.

- Use during Stage ③ to caption the focused feature with one or two role / category labels.
- Often paired with a thin dashed connection line linking the pill to the tile it describes.

### Connection lines

Dashed thin white lines (`rgba(255,255,255,0.35)`, 1.5 px, 4-px dash) connect callout pills to monitor tiles. Imply "this tag describes this tile". Used sparingly — never more than 3 lines on screen at once.

---

## Motion-pattern vocabulary

### Slow gradient drift (idle)

The screens themselves animate even when tiles are still. Gradient rotation: 360° over 12 s. Gives the wall an "alive" quality that doesn't compete with the wave.

### Vertical sine wave (Rule 2)

Tiles bob up/down only. Phase-shifted across columns + rows for a left-to-right travelling sine. See [`motion-principles.md`](./motion-principles.md) for the math.

### Tap-pulse trigger

A subtle radial pulse expands from canvas center at `t = 2.5 s` (200 ms, opacity 0.3 → 0, scale 0 → 1.4× monitor width). Cues the viewer that Stage ② just happened.

### Detach-and-land (Stage ②)

6 outer-ring tiles **lift, travel along an eased arc, land in a new outer-ring slot**. Lift gives weight; travel uses cinematic curve; land is firm (no bounce-back). All 6 share the timeline within 80 ms.

### Fragment + zoom (Stage ③)

One tile zooms 4× to canvas center. Others recede in scale + opacity. Wall (anchors) stays in wave but at 40% amplitude. Reference: *Product Exploration Step 3* shows this with feature callouts (5×, "optical zoom", "Next-Gen Camera") laid in among receding tiles.

### Loop seam invisibility

The 6.0-s loop must seam. Last frame at `t = 6.0` = first frame at `t = 0.0`. The reference videos do this; if our seam is visible, the rubric flags axis 3.

---

## Out of scope (for now)

This repository is scoped exclusively to a 5×3 wall with an idle/reveal/focus choreography. Other hardware formats are not generated here. If a future brief targets one, `product-mapper` should refuse rather than silently rendering the wall template.

---

## Anti-patterns (what the videos do *not* do)

- **No swirl, no parallax-pan, no camera tumble.** The camera is locked.
- **No tile rotation.** Tiles stay axis-aligned. (The screen *content* may rotate as a gradient angle, but the tile frame doesn't.)
- **No 3D tilt of tiles.** Tiles are flat planes facing camera. (Three.js renders them as `PlaneGeometry`, but z-rotation is 0.)
- **No mid-flight content swap.** Tiles change content only when they land or land-and-zoom.
- **No more than 6 detaching tiles.** Reference compositions hold to 4–6 detachers; more becomes noise.
- **No bright-saturated background.** Background is dark. Vibrancy lives only on the screens.
