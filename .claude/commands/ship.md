---
description: Finalize a concept — generate pitch.md, convert loop, commit
argument-hint: <slug>
---

# /ship $ARGUMENTS

Take an approved concept (rubric ≥ 24/30) from "rendered" to "client-ready".

## Pre-flight

1. Confirm `concepts/$ARGUMENTS/artifact.html` exists.
2. Confirm `concepts/$ARGUMENTS/loop.webm` and `hero.png` exist (re-run `/render` first if not).
3. Read `concepts/$ARGUMENTS/critique.md`. If total < 24, **stop** and tell the user to iterate first (`/render $ARGUMENTS --from $ARGUMENTS`). Override only if the user explicitly says "ship anyway".

## Steps

1. **Generate pitch**: dispatch the **`pitch-curator`** subagent with the brief + spec + critique. It writes `concepts/$ARGUMENTS/pitch.md` — a single-page narrative ready to drop into a deck. References the local `loop.webm` and `hero.png` paths.

2. **Convert media for PowerPoint compatibility**:
   ```sh
   ffmpeg -y -i concepts/$ARGUMENTS/loop.webm \
     -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
     -an concepts/$ARGUMENTS/loop.mp4
   ```
   PowerPoint chokes on VP9, so always emit H.264 yuv420p with `+faststart`. Strip audio (the loop has none).

3. **Append to ledger**: read `concepts/_index.json` (create as `[]` if missing), append:
   ```jsonc
   {
     "slug": "$ARGUMENTS",
     "client": "<from brief>",
     "score": <from critique>,
     "axes": [<6 numbers>],
     "tech": "p5",
     "shipped_at": "<ISO 8601 UTC>",
     "git_sha": "<HEAD short>"
   }
   ```
   Write back with stable formatting (2-space indent, sorted keys).

4. **Print** the deliverables list:
   - `concepts/$ARGUMENTS/loop.mp4`  ← drop in pitch deck
   - `concepts/$ARGUMENTS/hero.png`  ← deck cover
   - `concepts/$ARGUMENTS/pitch.md`  ← narrative copy

5. The `Stop` hook will auto-commit if the score is on the ledger.

## Don't

- Don't push to a remote — committing locally is enough; pushing is a separate human decision.
- Don't delete prior renders. Iteration history stays under `concepts/$ARGUMENTS/`.
- Don't ship below threshold without explicit user override.
