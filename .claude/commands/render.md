---
description: Render a concept by driving Claude Design via the Chrome MCP
argument-hint: <slug> [--from <slug>]
---

# /render $ARGUMENTS

Drive Claude Design (Claude.ai in Chrome) to generate the p5 monitor-wall sketch for `<slug>`, then capture media + critique.

## Parsing $ARGUMENTS

- First positional argument = `<slug>` (required). Brief must exist at `briefs/<slug>.md`.
- Optional `--from <slug>` = iterate from a prior render. Loads the prior `concepts/<slug>/critique.md` and prepends its "Top 3 actionable revisions" to the prompt as a "Revisions for this iteration:" block.

## Steps

1. **Pre-flight checks**:
   - Confirm `briefs/<slug>.md` exists.
   - Confirm `mcp__Claude_in_Chrome__tabs_context_mcp` returns a tab group.
   - Confirm `mcp__Claude_Preview__preview_list` is callable.
   - If `--from <slug>` is set, confirm `concepts/<from-slug>/critique.md` exists.

2. **Spec generation**: dispatch the **`product-mapper`** subagent with the brief contents. It returns `concepts/<slug>/spec.md` containing:
   - Three concise stage paragraphs following `prompts/three-stage-choreography.md`.
   - A monitor map (15 tiles, 6 detachers, checked against the schema in `design-system/monitor-wall-spec.md`).
   - Color-mapping rationale.

3. **Build the prompt bundle** (in memory, ~5–8 KB):
   - Open with `prompts/_design-context-block.md` (verbatim).
   - Read brief.tech (default `gsap-three`). Append the matching template:
     - `gsap-three` → `prompts/gsap-three-monitor-wall.md`
     - `gsap-dom`   → `prompts/gsap-three-monitor-wall.md` with a "DOM only, no Three.js" override note prepended
     - `p5`         → `prompts/p5-monitor-wall.md`
   - Fill the `<<SLOT: ...>>` placeholders from the brief and the spec's monitor map.
   - Append `prompts/three-stage-choreography.md` for narrative reference.
   - If `--from <slug>` is set, append a `## Revisions for this iteration` block with the prior critique's top 3.

4. **Send to Claude Design** via the **`chrome-pilot`** subagent. The pilot:
   - Locates or opens a claude.ai conversation tab.
   - Pastes the prompt bundle into the composer.
   - Submits and polls for artifact completion.
   - Extracts the HTML code block (preferring the Artifacts panel; falling back to fenced ```html in the message body).
   - Saves the result to `concepts/<slug>/artifact.html`.

5. **Capture & critique**: dispatch the **`design-critic`** subagent. It:
   - Boots `mcp__Claude_Preview__preview_start` against `preview/index.html?concept=<slug>`.
   - Captures `concepts/<slug>/hero.png`, `loop.webm`, `stage-1.png`, `stage-2.png`, `stage-3.png`.
   - Scores against `design-system/rubric.md`.
   - Writes `concepts/<slug>/critique.md`.

6. **Report**:
   - Print the rubric total + per-axis scores.
   - If total ≥ 24 → suggest `/ship <slug>`.
   - Else → suggest `/render <slug> --from <slug>` to iterate.

## Don't

- Don't run ffmpeg here — that's `/ship`'s job.
- Don't auto-commit — the `Stop` hook handles that conditionally.
- Don't retry chrome-pilot more than twice in one render; if both fail, surface the error verbatim and stop.
