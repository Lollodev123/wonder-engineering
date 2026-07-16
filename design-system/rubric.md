# Critic rubric — kinetic monitor wall

The design-critic agent scores every rendered concept against these 6 axes. Each axis 1–5. Total /30. **Ship threshold = 24.**

The critic must score the **6-second `loop.webm`** — not just stills. A pretty hero frame with broken motion fails axis 2 and axis 3 even if axes 1, 4, 5, 6 are perfect.

---

## Axis 1 — Scene fidelity (1–5)

Does the artifact look like it was filmed in a dark gallery, with luminous monitors and the lighting language of the reference videos?

| Score | Description |
|---|---|
| 1 | White or default-page background. No room. Reads as a webpage demo. |
| 2 | Dark background but flat — no depth, no lighting cues. |
| 3 | Dark gallery wall present; lighting is uniform, not directional. |
| 4 | Three-point lighting: cool fill + warm rim + key. Ground reflection ≥ subtle. Tiles read as luminous panels, not flat rectangles. |
| 5 | A first-time viewer reads "this is a real installation." Light wraps the tiles. Optional person silhouette is integrated and selling scale. Matches `product-exploration_Step1` mood. |

## Axis 2 — Motion rule compliance (1–5)

The three hard rules: **no collision · vertical-or-sine only · phase-shifted-but-synchronized**. Each violation drops a point.

| Score | Description |
|---|---|
| 1 | Multiple collisions per loop, or wholly random motion, or chaotic detach paths. |
| 2 | Idle has lateral drift (Rule 2 broken) OR phase looks random (Rule 3 broken). |
| 3 | Idle obeys Rules 2+3 but a transition path clips through a tile (Rule 1 broken). |
| 4 | All three rules hold across the loop. Wave reads as travelling sine. Detach paths are clean. |
| 5 | Rules are honored *and* used artfully — phase progression reads as the monitors "breathing in sync"; transitions feel choreographed, not mechanical. |

## Axis 3 — Cinematic motion quality (1–5)

| Score | Description |
|---|---|
| 1 | Choppy. Position pops. Linear motion only. ≤ 30 fps. |
| 2 | Easing applied but inconsistent. Detach feels mechanical. |
| 3 | Cinematic easing on detach + zoom. 60 fps held *most* of the time but the loop seam is visible. |
| 4 | 60 fps held. Cinematic easing throughout. Loop seam is clean. Tap pulse is snappy and visible. |
| 5 | The whole loop has the *weight* of a real camera move. Subtle overshoot on detach + zoom. The seam is invisible — could play forever. |

## Axis 4 — Screen-content vibrancy (1–5)

Are the screens themselves alive — gradients flowing, image-slices spanning tiles, callouts integrated?

| Score | Description |
|---|---|
| 1 | Tiles are solid colors or white. No gradient. No animation on screens. |
| 2 | Static gradients per tile. No idle screen motion. |
| 3 | Gradients per tile + slow drift in angle/hue. No tile-spanning imagery. |
| 4 | Gradients + drift + at least one tile-spanning IMAGE-SLICE in idle (a product image fragmented across 3+ tiles). Reveal callouts use translucent pills. |
| 5 | The wall reads as a *kinetic art piece* — gradients sing, the spanned image is unmistakable, callouts + connection lines in Stage ③ feel composed, not pasted. |

## Axis 5 — Narrative clarity — 3 stages legible (1–5)

| Score | Description |
|---|---|
| 1 | Cannot tell where Stage ① ends and Stage ② begins. |
| 2 | Three stages exist but transition is abrupt. |
| 3 | Each stage recognizable but pacing off (a stage too short or too long). |
| 4 | All three stages clearly readable. Pacing matches `tokens.json` durations within ±200 ms. Tap pulse is unmistakable. |
| 5 | A first-time viewer can describe what they saw and *why* — "the wall idles with the product, then six tiles peel to show features, then this one zooms with the headline number". |

## Axis 6 — Brand fit (1–5)

| Score | Description |
|---|---|
| 1 | Could be any random demo. No client signal. |
| 2 | Client name appears once, no further connective tissue. |
| 3 | Brand colors mapped, but the rest is generic. |
| 4 | Hero copy + brand color mapping + appropriate gradient palette. The mood (e.g. "cold-mountain clinical-cinematic") is felt. |
| 5 | A pitch viewer recognizes the client world inside the first second of the loop. The piece would belong on the client's own brand site. |

---

## Output format

The critic writes `concepts/<slug>/critique.md` as:

```markdown
# Critique — <slug>

**Score: 26 / 30** — *ship*

<one-sentence overall: what worked, what didn't>

| Axis | Score | Notes |
|---|---|---|
| 1. Scene fidelity              | 5 | … |
| 2. Motion rule compliance       | 5 | three rules clean; collision validator passed |
| 3. Cinematic motion quality     | 4 | seam at 5.95 s shows a 2-frame jitter |
| 4. Screen-content vibrancy      | 4 | gradients flow; pose-image spans 3 tiles cleanly; callouts a touch generic |
| 5. Narrative clarity            | 4 | tap pulse could be 1.2× scale to read better |
| 6. Brand fit                    | 4 | mood right; bring crimson saturation up on safety NUMBER |

## Top 3 actionable revisions
1. Fix the 2-frame seam jitter at t = 5.95 s — likely `t` not exactly modular by 6.0.
2. Scale the tap-pulse to 1.4× monitor width and bump opacity peak to 0.45.
3. On safety NUMBER tile, change accent from `#9A2D45` to `#CB395F` (full crimson).
```

Numbers in the table feed `concepts/_index.json` for the ledger; the "Top 3 actionable revisions" feeds the next `/render --from <slug>`.
