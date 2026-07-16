---
description: Open a concept artifact in the Preview MCP — no LLM call
argument-hint: <slug>
---

# /preview $ARGUMENTS

Read-only inspection of an existing concept. No model calls, no prompt sent to Claude Design.

## Steps

1. Confirm `concepts/$ARGUMENTS/artifact.html` exists.
2. Call `mcp__Claude_Preview__preview_start` with the project root and the URL `preview/index.html?concept=$ARGUMENTS`.
3. Take a single `mcp__Claude_Preview__preview_screenshot`.
4. Print the preview URL and screenshot path.
5. Suggest the next move: open in browser for human eye-check, or `/diff-vs-reference $ARGUMENTS` for a critic-only score.

## Don't

- Don't write any new files (no critique, no commit).
- Don't replace existing media files — this is read-only.
