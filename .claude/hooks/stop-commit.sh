#!/usr/bin/env bash
# Stop hook — if there are uncommitted changes inside concepts/<slug>/ and
# concepts/<slug>/critique.md exists with score >= 24, auto-commit. Otherwise no-op.

set -u
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 0

# Bail if not a git repo (e.g. fresh clone before init).
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# Find changed concept slugs.
changed_slugs="$(git status --porcelain concepts/ 2>/dev/null \
  | awk '{print $2}' \
  | sed -E 's|^concepts/([^/]+)/.*|\1|' \
  | sort -u)"

[ -z "$changed_slugs" ] && exit 0

committed=0
for slug in $changed_slugs; do
  critique="concepts/${slug}/critique.md"
  if [ ! -f "$critique" ]; then
    echo "↩  ${slug}: no critique yet — leaving uncommitted"
    continue
  fi

  # Extract "Score: NN / 30" from the critique header.
  score="$(grep -m1 -oE 'Score: *[0-9]+ */ *30' "$critique" 2>/dev/null \
            | grep -oE '[0-9]+' | head -1)"

  if [ -z "$score" ]; then
    echo "↩  ${slug}: critique header missing score — leaving uncommitted"
    continue
  fi

  if [ "$score" -lt 24 ]; then
    echo "↩  ${slug}: score ${score}/30 below ship threshold (24) — leaving uncommitted"
    continue
  fi

  git add "concepts/${slug}/" >/dev/null 2>&1
  if git diff --cached --quiet; then
    continue
  fi
  msg="ship(${slug}): score ${score}/30"
  git commit -q -m "$msg" --no-gpg-sign >/dev/null 2>&1 \
    && { echo "✓ committed: ${msg}"; committed=$((committed+1)); }
done

[ "$committed" -gt 0 ] && echo "  ${committed} concept(s) auto-committed by Stop hook."
exit 0
