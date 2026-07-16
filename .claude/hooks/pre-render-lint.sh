#!/usr/bin/env bash
# UserPromptSubmit hook — when the user submits a prompt that starts with /render,
# verify that the brief exists and a Chrome tab is open. Output guidance for Claude
# to surface to the user before the render attempt.

set -u
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

prompt_input="$(cat 2>/dev/null || true)"
prompt="$(echo "$prompt_input" | jq -r '.prompt // empty' 2>/dev/null || echo "")"

# If we couldn't parse JSON, exit cleanly — don't block.
[ -z "$prompt" ] && exit 0

# Only act on /render invocations.
case "$prompt" in
  /render*) ;;
  *) exit 0 ;;
esac

# Extract the first non-flag token after /render as the slug.
slug="$(echo "$prompt" | awk '{for(i=2;i<=NF;i++){if($i !~ /^-/){print $i; exit}}}')"

if [ -z "$slug" ]; then
  echo "ℹ️  /render needs a slug. Usage: /render <slug> [--from <slug>]"
  exit 0
fi

brief="${PROJECT_DIR}/briefs/${slug}.md"
if [ ! -f "$brief" ]; then
  echo "⚠️  Brief not found: ${brief}"
  echo "    Create it with /concept ${slug}, or pick from:"
  ls "${PROJECT_DIR}/briefs/" 2>/dev/null | grep -E '\.md$' | grep -v '^_template' | sed 's/^/      /'
  exit 0
fi

echo "✓ Brief found: briefs/${slug}.md"
echo "  Pre-flight: ensure a logged-in claude.ai tab is open in Chrome (Chrome MCP) and the preview server is reachable on http://localhost:4173/."
exit 0
