# Brief — `_example-sports-tech`

Fictional, anonymized sports-tech concept included to exercise the workflow end to end. It is not a client deliverable and its metrics are illustrative visual content, not factual product claims.

```yaml
project: sports-tech demo
campaign: athlete analysis — live-event monitor wall

hero_headline: "See movement from a new angle"
hero_subdeck: "A kinetic story about video-based technique analysis."

brand_colors:
  primary: "#4858D3"
  secondary: "#CB395F"
  tertiary: "#D86937"

gradient_palette:
  - ["#1F46E5", "#5DD9F0"]
  - ["#5C68B5", "#FFFFFF"]
  - ["#1A1F4E", "#7B3DD9"]
  - ["#CB395F", "#F2A65A"]
  - ["#0FE5D2", "#FFFFFF"]

hero_visual: stylized silhouette of a freestyle athlete, sliced across three central tiles
include_person: true

hero_metrics:
  - { type: NUMBER, value: "33", sub: "joints tracked" }
  - { type: NUMBER, value: "5×", sub: "view comparison" }
  - { type: NUMBER, value: "7.8", sub: "rotation score" }

top_features:
  - { id: pose, type: IMAGE, headline: "3D Pose Estimation", sub: "movement reconstructed from a phone clip" }
  - { id: rotation, type: NUMBER, headline: "Rotational Metrics", sub: "velocity · air time · angle" }
  - { id: trim, type: TEXT, headline: "Automatic Clip Trim", sub: "isolates the movement window" }
  - { id: chat, type: ICON, headline: "Conversational Review", sub: "ask questions about the clip", glyph: "chat" }
  - { id: mobile, type: ICON, headline: "Mobile Capture", sub: "starts from a phone video", glyph: "phone" }
  - { id: compare, type: NUMBER, headline: "Technique Comparison", sub: "compare attempts over time", value: "5×" }

stage_3_callouts:
  - "Multimodal analysis"
  - "3D pose model"
  - "Phone video input"

stage_3_quote:
  text: "See the movement, compare the attempt, choose the next adjustment."
  attrib: "Demo narration"

mood: cold-mountain, clinical-cinematic, confident
tech: gsap-three
references:
  - design-system/reference/visual-anchors.md
```

## Delivery context

- Expected output: `concepts/_example-sports-tech/loop.mp4`, `hero.png`, and `pitch.md`.
- Review threshold: 24/30 on the visual rubric.
- If the result needs another pass: `/render _example-sports-tech --from _example-sports-tech`.
