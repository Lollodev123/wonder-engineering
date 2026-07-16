---
description: Re-score an existing concept against the design-system reference
argument-hint: <slug>
---

# /diff-vs-reference $ARGUMENTS

Run the **`design-critic`** subagent against an existing concept's media + artifact, comparing only against `design-system/reference/` and `design-system/rubric.md`. No new render — just a fresh score.

Useful for:
- Verifying a prior render still scores ≥ 24 after design-system tokens were edited.
- Reproducibility check: scores should be reproducible to within ±1 across two runs.

## Steps

1. Confirm `concepts/$ARGUMENTS/artifact.html` exists and at least `loop.webm` exists. If missing, suggest `/render $ARGUMENTS` instead.
2. Dispatch `design-critic` with the slug. It re-reads the existing media (does not re-capture) and re-scores against the rubric.
3. Write the new critique to `concepts/$ARGUMENTS/critique.md` (overwrites). Include a delta line vs. the prior score in the new critique header.
4. Print the new total and the delta.

## Don't

- Don't re-capture media. The point is to score the same artifact under the current rubric.
- Don't trigger `/ship` automatically.
