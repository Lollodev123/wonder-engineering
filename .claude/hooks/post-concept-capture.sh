#!/usr/bin/env bash
# PostToolUse:Write hook — when a concepts/<slug>/artifact.html is written,
# print a nudge to capture media + score it. We do not invoke MCP tools from here
# (hook scripts can only emit text to context).

set -u
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
input="$(cat 2>/dev/null || true)"

# Try to extract the file_path from the tool input JSON.
path="$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")"
[ -z "$path" ] && exit 0

# Only act on artifact.html writes inside concepts/.
case "$path" in
  *"/concepts/"*"/artifact.html") ;;
  *) exit 0 ;;
esac

slug="$(echo "$path" | sed -E 's|.*/concepts/([^/]+)/artifact\.html$|\1|')"
size_kb="$(wc -c < "$path" 2>/dev/null | awk '{printf "%.1f", $1/1024}')"

cat <<EOF
✓ artifact.html written for "${slug}" (${size_kb} KB)
  Next: dispatch the design-critic subagent to capture hero.png + loop.webm + 3 stage stills via Claude Preview MCP, then score against design-system/rubric.md.
  Preview URL once server is running: http://localhost:4173/preview/index.html?concept=${slug}
EOF
exit 0
