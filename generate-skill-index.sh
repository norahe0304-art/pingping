#!/usr/bin/env bash
#
# [INPUT]: Reads SKILL.md files from multiple local skill roots.
# [OUTPUT]: Writes a merged skills index JSON for pingping/runtime discovery.
# [POS]: workspace bootstrap utility for skill discovery hygiene.
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
#
# Usage:
#   ./generate-skill-index.sh
#   ./generate-skill-index.sh /custom/output/index.json

set -euo pipefail

INDEX_FILE="${1:-$HOME/.openclaw/skills/index.json}"
GLOBAL_INDEX_FILE="$HOME/.openclaw/skills/index.json"
LEGACY_INDEX_FILE="$HOME/.agents/skills/index.json"
WORKSPACE_INDEX_FILE="$HOME/.openclaw/workspace/skills/index.json"

SKILL_ROOTS=(
  "$HOME/.openclaw/skills"
)

extract_description() {
  local skill_file="$1"
  local desc=""

  # Prefer YAML frontmatter description when present.
  desc="$(awk '
    NR == 1 && $0 == "---" { in_yaml = 1; next }
    in_yaml == 1 {
      if ($0 == "---") { exit }
      if ($0 ~ /^description:[[:space:]]*/) {
        sub(/^description:[[:space:]]*/, "", $0)
        gsub(/^"/, "", $0)
        gsub(/"$/, "", $0)
        print
        exit
      }
    }
  ' "$skill_file")"

  if [[ -z "$desc" ]]; then
    desc="$(awk '
      NR == 1 && $0 == "---" { in_yaml = 1; next }
      in_yaml == 1 {
        if ($0 == "---") { in_yaml = 0; next }
        next
      }
      {
        line = $0
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
        if (line == "") next
        if (line ~ /^#/) next
        print line
        exit
      }
    ' "$skill_file")"
  fi

  if [[ -z "$desc" ]]; then
    desc="No description available."
  fi

  # Keep descriptions compact and one-line.
  desc="${desc//$'\n'/ }"
  desc="${desc//$'\r'/ }"
  printf '%s' "${desc:0:220}"
}

escape_json() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/ }"
  s="${s//$'\r'/ }"
  printf '%s' "$s"
}

declare -a used_roots=()
SEEN_FILE="$(mktemp)"
ROWS_FILE="$(mktemp)"
ROWS_COUNT=0

cleanup() {
  rm -f "$SEEN_FILE" "$ROWS_FILE"
}
trap cleanup EXIT

for root in "${SKILL_ROOTS[@]}"; do
  [[ -d "$root" ]] || continue
  used_roots+=("$root")
  for skill_dir in "$root"/*; do
    [[ -d "$skill_dir" ]] || continue
    [[ -f "$skill_dir/SKILL.md" ]] || continue

    skill_name="$(basename "$skill_dir")"
    [[ -n "$skill_name" ]] || continue

    # First hit wins to keep source priority deterministic.
    if grep -Fxq "$skill_name" "$SEEN_FILE"; then
      continue
    fi
    printf '%s\n' "$skill_name" >> "$SEEN_FILE"

    description="$(extract_description "$skill_dir/SKILL.md")"
    path="$skill_dir/SKILL.md"

    printf '%s\n' "{\"name\":\"$(escape_json "$skill_name")\",\"description\":\"$(escape_json "$description")\",\"path\":\"$(escape_json "$path")\"}" >> "$ROWS_FILE"
    ROWS_COUNT=$((ROWS_COUNT + 1))
  done
done

mkdir -p "$(dirname "$INDEX_FILE")"
{
  printf '{\n'
  printf '  "generated_at": "%s",\n' "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  printf '  "sources": [\n'
  for i in "${!used_roots[@]}"; do
    comma=","
    [[ "$i" -eq "$((${#used_roots[@]} - 1))" ]] && comma=""
    printf '    "%s"%s\n' "$(escape_json "${used_roots[$i]}")" "$comma"
  done
  printf '  ],\n'
  printf '  "skills": [\n'
  current=0
  while IFS= read -r row; do
    current=$((current + 1))
    comma=","
    [[ "$current" -eq "$ROWS_COUNT" ]] && comma=""
    printf '    %s%s\n' "$row" "$comma"
  done < "$ROWS_FILE"
  printf '  ]\n'
  printf '}\n'
} > "$INDEX_FILE"

# Keep compatibility copies for old prompts.
mkdir -p "$(dirname "$GLOBAL_INDEX_FILE")"
if [[ "$INDEX_FILE" != "$GLOBAL_INDEX_FILE" ]]; then
  cp "$INDEX_FILE" "$GLOBAL_INDEX_FILE"
fi

mkdir -p "$(dirname "$LEGACY_INDEX_FILE")"
if [[ "$INDEX_FILE" != "$LEGACY_INDEX_FILE" ]]; then
  cp "$INDEX_FILE" "$LEGACY_INDEX_FILE"
fi

mkdir -p "$(dirname "$WORKSPACE_INDEX_FILE")"
if [[ "$INDEX_FILE" != "$WORKSPACE_INDEX_FILE" ]]; then
  cp "$INDEX_FILE" "$WORKSPACE_INDEX_FILE"
fi

echo "Done: generated merged skills index at $INDEX_FILE"
echo "Synced: copied index to $GLOBAL_INDEX_FILE"
echo "Compat: copied index to $WORKSPACE_INDEX_FILE"
echo "Compat: copied index to $LEGACY_INDEX_FILE"
echo "Total skills: $ROWS_COUNT"
