# Brief — `<slug>`

The product-mapper expands this input into a three-stage concept and monitor map. Keep committed examples fictional or anonymized; put client-specific context in a gitignored `*.local.md` file.

```yaml
project:               # short internal label; no client name in public snapshots
campaign:              # e.g. "athlete analysis — live-event monitor wall"
source_article:        # optional private/local source; omit from public snapshots

hero_headline:         # concise pitch headline
hero_subdeck:          # optional one-sentence explanation

brand_colors:
  primary:             # hex, dominant screen accent
  secondary:           # hex, supporting screen accent
  tertiary:            # optional accent for the final beat

gradient_palette:
  - ["#start", "#end"]

hero_visual:           # one-line description of the tile-spanning image
include_person:        # boolean, adds a silhouette for physical scale

hero_metrics:
  - { type: NUMBER, value: "...", sub: "..." }

top_features:          # 4–6 items used in the reveal stage
  - { id: <id>, type: NUMBER, headline: "<headline>", sub: "<copy>", value: "<numeric>" }
  - { id: <id>, type: ICON, headline: "<headline>", sub: "<copy>", glyph: "<glyph>" }

stage_3_callouts:      # optional, 1–3 short labels
  - "..."

stage_3_quote:         # optional; use fictional copy in committed examples
  text:
  attrib:

mood:                  # short comma-separated descriptors
tech: gsap-three       # gsap-three | gsap-dom | p5
references:            # local, shareable references only
  - design-system/reference/visual-anchors.md
```

## Notes

- A source can ground feature copy, but the public brief must not expose confidential URLs or identities.
- The mapper proposes a layout. It does not provide continuous-path or hardware-safety validation.
- Rendered motion is reviewed against `design-system/rubric.md`; a high score is a quality gate, not a safety certificate.
- Built-in glyphs include `chat`, `phone`, `sun`, `lightning`, `play`, `mountain`, and `clock`.
