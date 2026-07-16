---
description: Start a new kinetic monitor-wall concept brief
argument-hint: <slug>
---

# /concept $ARGUMENTS

Start a new concept brief.

## Steps

1. **Validate the slug**. Must match `[a-z0-9-]+` and not yet exist as `briefs/$ARGUMENTS.md` or `concepts/$ARGUMENTS/`. If it's missing, ask the user for one.
2. **Read** `briefs/_template.md` and `briefs/_example-sports-tech.md` to load the schema and a worked example.
3. **Interactive intake**. Ask the user (use `AskUserQuestion` for the structured fields, free-text only for the headline + visual prose):
   - Client + campaign
   - Optional source-article URL (preferred — grounds the copy in something real)
   - Hero headline + sub-deck
   - Brand primary + secondary hex (and optional tertiary)
   - 3 hero metrics (idle wave top-row NUMBERs)
   - 3–6 top features (each: id, type, headline, sub, optional value/glyph)
   - Optional Stage ③ quote + attribution
   - Mood (short comma-separated descriptors)
4. **If `source_article` is provided**, fetch it with `WebFetch` and ground the headline / features in actual copy. If features were not fully provided, propose the top 6 from the article and confirm with the user.
5. **Write** `briefs/$ARGUMENTS.md` using the template structure verbatim, with all fields populated.
6. **Print** the resulting path and the next command: `/render $ARGUMENTS`.

## Don't

- Don't auto-create the `concepts/$ARGUMENTS/` directory yet — that's `/render`'s job.
- Don't include any audience PII (prospect names, LinkedIn URLs, etc.) in the committed brief. Tell the user to add a `briefs/$ARGUMENTS.local.md` (gitignored) for that.
- Don't run the renderer here. `/concept` is intake only.
