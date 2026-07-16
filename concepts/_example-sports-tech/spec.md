# Spec — `_example-sports-tech`

Pre-built mapper output for the fictional sports-tech brief in [`briefs/_example-sports-tech.md`](../../briefs/_example-sports-tech.md).

## Visual mapping

- **Primary — `#4858D3`:** data and pose-analysis accents.
- **Secondary — `#CB395F`:** metrics and short labels.
- **Tertiary — `#D86937`:** used only in the final narration beat.
- **Hero:** an athlete silhouette is divided across the three centre tiles.
- **Environment:** a dark gallery and a person silhouette establish physical scale.

## Three-stage narrative

### Stage ① Movement in context

The wall opens as a cold-toned mosaic. A freestyle silhouette spans the centre row while metrics and gradients move on the same deterministic vertical rhythm.

### Stage ② Analysis appears

A pulse introduces six feature tiles. They lift and change content in place, surfacing pose, rotation, clip-trimming, conversational review, mobile capture, and comparison.

### Stage ③ One detail in focus

One feature fills the canvas while supporting labels connect the visual to the underlying workflow: video input, pose estimation, and multimodal analysis.

## Monitor map

```jsonc
{
  "tiles": [
    { "col": 0, "row": 0, "idle": { "type": "GRADIENT", "gradient": ["#1A1F4E", "#7B3DD9"] }, "detach": { "feature": "chat" } },
    { "col": 1, "row": 0, "idle": { "type": "NUMBER", "value": "33", "sub": "joints tracked" }, "detach": null },
    { "col": 2, "row": 0, "idle": { "type": "NUMBER", "value": "5×", "sub": "view comparison" }, "detach": null },
    { "col": 3, "row": 0, "idle": { "type": "NUMBER", "value": "7.8", "sub": "rotation score" }, "detach": null },
    { "col": 4, "row": 0, "idle": { "type": "GRADIENT", "gradient": ["#1F46E5", "#5DD9F0"] }, "detach": { "feature": "mobile" } },

    { "col": 0, "row": 1, "idle": { "type": "GRADIENT", "gradient": ["#5C68B5", "#FFFFFF"] }, "detach": { "feature": "trim" } },
    { "col": 1, "row": 1, "idle": { "type": "IMAGE-SLICE", "source": "pose_hero", "rect": [0.00, 0.00, 0.34, 1.00] }, "detach": null },
    { "col": 2, "row": 1, "idle": { "type": "IMAGE-SLICE", "source": "pose_hero", "rect": [0.34, 0.00, 0.66, 1.00] }, "detach": null },
    { "col": 3, "row": 1, "idle": { "type": "IMAGE-SLICE", "source": "pose_hero", "rect": [0.66, 0.00, 1.00, 1.00] }, "detach": null },
    { "col": 4, "row": 1, "idle": { "type": "GRADIENT", "gradient": ["#0FE5D2", "#FFFFFF"] }, "detach": { "feature": "compare" } },

    { "col": 0, "row": 2, "idle": { "type": "GRADIENT", "gradient": ["#1A1F4E", "#7B3DD9"] }, "detach": null },
    { "col": 1, "row": 2, "idle": { "type": "GRADIENT", "gradient": ["#1F46E5", "#5DD9F0"] }, "detach": { "feature": "pose" } },
    { "col": 2, "row": 2, "idle": { "type": "GRADIENT", "gradient": ["#CB395F", "#F2A65A"] }, "detach": null },
    { "col": 3, "row": 2, "idle": { "type": "GRADIENT", "gradient": ["#1F46E5", "#5DD9F0"] }, "detach": { "feature": "rotation" } },
    { "col": 4, "row": 2, "idle": { "type": "GRADIENT", "gradient": ["#5C68B5", "#FFFFFF"] }, "detach": null }
  ],

  "features": [
    { "id": "pose", "type": "IMAGE", "headline": "3D Pose Estimation", "sub": "from a phone clip" },
    { "id": "rotation", "type": "NUMBER", "headline": "Rotational Metrics", "sub": "velocity · air time · angle" },
    { "id": "trim", "type": "TEXT", "headline": "Automatic Clip Trim", "sub": "isolates the movement window" },
    { "id": "chat", "type": "ICON", "headline": "Conversational Review", "sub": "ask about the clip", "glyph": "chat" },
    { "id": "mobile", "type": "ICON", "headline": "Mobile Capture", "sub": "starts from phone video", "glyph": "phone" },
    { "id": "compare", "type": "NUMBER", "headline": "Technique Comparison", "sub": "compare attempts", "value": "5×" }
  ],

  "stage3_focus_order": ["pose", "rotation", "trim", "chat", "mobile", "compare"],
  "stage3_callouts": ["Multimodal analysis", "3D pose model", "Phone video input"],
  "include_person": true
}
```

## Constraint notes

- The six reveal tiles use a bloom-in-place treatment in this example, so Stage ② does not introduce lateral travel.
- Idle offsets are deterministic and vertical.
- The HTML render is checked visually against the design-system rubric.
- `motion-lab/collision_safe()` is a separate sampled diagnostic for Python primitives; it does not validate the HTML zoom stage or physical hardware.

## Iteration paths

- Add small, validated outward travel if the bloom-in-place reveal reads as too static.
- Strengthen the gallery lighting if the wall lacks depth.
- Reduce supporting labels if the final beat competes with the focused feature.
