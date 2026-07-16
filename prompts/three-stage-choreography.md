# Three-stage choreography template

This document is a reference for the orchestrator (Claude Code) and the `product-mapper` agent when expanding a brief into a `spec.md`. It restates the temporal structure and the writing voice for the stage paragraphs.

## Timeline (locked)

```
t=0.0 ┬──────────────────────────────┐
      │ Stage ① Dynamic Product       │  idle wave, all 15 monitors
      │         Showcase              │  carrying one piece of content each
t=2.5 ├──────────────────────────────┤  ← tap pulse fires
      │ Stage ② Interactive           │  6 monitors detach, lift→travel→land
      │         Exploration           │  with cinematic easing
t=4.0 ├──────────────────────────────┤
      │ Stage ③ Deeper Product        │  one detached monitor zooms 4×
      │         Layers                │  others recede; quote overlay
t=5.6 ├──────────────────────────────┤
      │ Return                        │  snap back to idle
t=6.0 └──────────────────────────────┘  ← seamless loop
```

## Stage paragraph template (used in `spec.md` and `pitch.md`)

Each stage paragraph is **one sentence, ~30 words**, structured as:

```
<Subject = installation>  <verbs the mechanical motion>,
<connecting clause>  <verbs the synchronized screen content>,
<finishing clause>  <names the visitor interaction or payoff>.
```

**Worked examples (from the live reference site):**

> The installation continuously performs a choreographed kinetic sequence, highlighting product features through synchronized mechanical movement and motion content.

> Visitors freely navigate the experience through a touch interface, selecting features, stories, or product categories in real time.

> Zoom interactions unlock additional content, revealing technical details, applications, or hidden capabilities with cinematic transitions and layered storytelling.

## Choreography slot — what `product-mapper` fills in per stage

For each stage, the spec must specify:

| Field | Stage ① | Stage ② | Stage ③ |
|---|---|---|---|
| `kinetic` | wave parameters (default OK) | which 6 monitors detach + landing positions | which monitor zooms (rotates per loop), how others recede |
| `screen_content` | content per tile (NUMBER/ICON/IMAGE/TEXT/GRADIENT-FILL) | feature payload per detaching tile | focused tile content + optional quote overlay |
| `interaction` | none (ambient) | tap pulse trigger | none (autoplay) |
| `paragraph` | one sentence, 30 words, in the voice above | same | same |

## Constraint: tap trigger must be visually unmistakable

The tap pulse at `t = 2.5` is the storytelling beat. Without it, the viewer can't tell where Stage ① ends and Stage ② begins. Always render:

- A subtle radial pulse expanding from the canvas center over 200 ms (`#000000` 30% opacity → 0%, scale 0 → 1.4× monitor width).
- A faint `Tap` cursor or `Explore →` button highlight that flashes at the same instant.

This is what the rubric scores under axis 4 (narrative clarity).
