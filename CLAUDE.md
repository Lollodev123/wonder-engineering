# Kinetic Monitor Pre-vis workspace

## Mission

Generate reviewable pre-visualization concepts for one exhibit format: a 5×3 wall of luminous monitors in a dark gallery. The wall begins in synchronized vertical motion, reveals feature content, and finishes on a focused visual beat.

This repository is an anonymized R&D snapshot. Do not add client, partner, prospect, or individual names to committed files. Project-specific context belongs in gitignored `*.local.md` files.

The deliverable for a concept is:

```text
concepts/<slug>/loop.mp4
concepts/<slug>/hero.png
concepts/<slug>/pitch.md
```

## Scope

This workspace produces pitch-quality pre-vis. It does not build:

- a marketing website;
- broadcast-ready motion graphics;
- physical hardware controls or safety systems;
- a general brief-to-choreography generator.

The Python composer currently contains hand-authored choreography examples. Keep that distinction explicit in code and documentation.

## Design contract

The detailed contract lives in `design-system/`. Its core rules are:

1. Idle motion is vertical and deterministic.
2. Tiles share timing and amplitude with per-position phase offsets.
3. A concept must be rendered and reviewed; a plausible specification is not sufficient evidence of visual quality.
4. The sampled Python collision check is diagnostic. It checks vertical neighbours at discrete instants and is not hardware certification.

## Workflow

| Command | Responsibility | Writes |
|---|---|---|
| `/concept <slug>` | guided brief intake | `briefs/<slug>.md` |
| `/render <slug> [--from <slug>]` | map, generate, render, critique | `concepts/<slug>/...` |
| `/preview <slug>` | open the existing artifact | read-only |
| `/diff-vs-reference <slug>` | score a rendered concept | `critique.md` |
| `/ship <slug>` | package an approved concept | `pitch.md`, `loop.mp4`, local commit |

The working loop is:

```text
brief → map → render → capture → critique → revise → human review
```

## Fast local automation boundary

This experiment intentionally grants the coding agent broad permissions inside the repository so it can iterate quickly. The hooks keep the automated commit narrow:

- pre-render lint rejects missing inputs;
- post-write capture only nudges the media-review step;
- the stop hook stages `concepts/<slug>/` only;
- it commits only when `critique.md` contains a score of at least 24/30;
- it never pushes or publishes.

Do not widen the auto-commit path beyond a single concept. A person reviews local commits before any remote operation.

## Active public example

The included example is `_example-sports-tech`, a fictional athlete-analysis concept used to exercise the workflow without publishing a client identity.

```sh
cd preview
npm install
npm run dev

# Then, from the repository workflow:
/render _example-sports-tech
/ship _example-sports-tech
```

## Conventions

- Keep client and prospect identifiers out of committed files.
- Do not hand-edit generated artifacts unless the workflow explicitly enters a debugging pass.
- Comments should explain non-obvious decisions, not narrate the code.
- Slash commands use `$ARGUMENTS`.
- Agent roles use YAML-frontmatter Markdown in `.claude/agents/`.
- Claims in public documentation must match the implementation and its current limits.
