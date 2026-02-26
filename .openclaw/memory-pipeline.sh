#!/usr/bin/env bash
# [INPUT]: Depends on local sync scripts under workspace/scripts and shared memory state files.
# [OUTPUT]: Runs deterministic memory sync pipeline and writes execution logs.
# [POS]: Infrastructure scheduler entrypoint for memory pipeline; decouples periodic sync from LLM turns.
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
SCRIPTS_DIR="$WORKSPACE/scripts"
SHARED_DIR="$WORKSPACE/memory/shared"
LOG_DIR="$HOME/.openclaw/logs"
LOG_FILE="$LOG_DIR/memory-pipeline.log"
LOCK_DIR="$SHARED_DIR/.memory_pipeline.lock"
GMAIL_TS_FILE="$SHARED_DIR/.gmail_watch_last_run"

mkdir -p "$SHARED_DIR" "$LOG_DIR"

now_epoch() {
  date +%s
}

last_mtime_or_zero() {
  local f="$1"
  if [[ -f "$f" ]]; then
    stat -f %m "$f" 2>/dev/null || echo 0
  else
    echo 0
  fi
}

run_step() {
  local name="$1"
  shift
  printf '[%s] STEP %s: %s\n' "$(date '+%F %T')" "$name" "$*" >> "$LOG_FILE"
  "$@" >> "$LOG_FILE" 2>&1
}

run_step_capture() {
  local name="$1"
  shift
  local tmp
  tmp="$(mktemp)"
  printf '[%s] STEP %s: %s\n' "$(date '+%F %T')" "$name" "$*" >> "$LOG_FILE"
  if "$@" >"$tmp" 2>&1; then
    cat "$tmp" >> "$LOG_FILE"
    cat "$tmp"
    rm -f "$tmp"
    return 0
  fi
  cat "$tmp" >> "$LOG_FILE"
  cat "$tmp"
  rm -f "$tmp"
  return 1
}

extract_total_new() {
  python3 - "$@" <<'PY'
import json
import sys
raw = sys.stdin.read().splitlines()
value = 0
for line in raw:
    line = line.strip()
    if not line or not line.startswith("{"):
        continue
    try:
        obj = json.loads(line)
    except Exception:
        continue
    if isinstance(obj, dict):
        try:
            value = int(obj.get("total_new", value))
        except Exception:
            pass
print(value)
PY
}

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  printf '[%s] SKIP another pipeline run is active\n' "$(date '+%F %T')" >> "$LOG_FILE"
  exit 0
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT

printf '[%s] PIPELINE start\n' "$(date '+%F %T')" >> "$LOG_FILE"

DISCORD_OUT="$(run_step_capture "discord-feed" \
  "$SCRIPTS_DIR/sync_discord_channels_to_shared_feed.py" \
  --workspace "$WORKSPACE" --limit 30 --workers 6 --verbose)"
TOTAL_NEW="$(printf '%s\n' "$DISCORD_OUT" | extract_total_new)"
printf '[%s] STEP discord-feed result: total_new=%s\n' "$(date '+%F %T')" "$TOTAL_NEW" >> "$LOG_FILE"

if (( TOTAL_NEW > 0 )); then
  run_step "shared-daily" \
    "$SCRIPTS_DIR/sync_discord_feed_to_daily_memory.py" \
    --workspace "$WORKSPACE" --verbose

  run_step "resources" \
    "$SCRIPTS_DIR/sync_discord_feed_urls_to_resources.py" \
    --workspace "$WORKSPACE" --vault obsidian --days 2 --verbose
else
  printf '[%s] STEP shared-daily: skipped (no new discord feed messages)\n' "$(date '+%F %T')" >> "$LOG_FILE"
  printf '[%s] STEP resources: skipped (no new discord feed messages)\n' "$(date '+%F %T')" >> "$LOG_FILE"
fi

# Run Gmail watcher at most once per hour.
NOW="$(now_epoch)"
LAST="$(last_mtime_or_zero "$GMAIL_TS_FILE")"
if (( NOW - LAST >= 3600 )); then
  run_step "gmail-watch" \
    "$SCRIPTS_DIR/check_gmail_important.py" \
    --workspace "$WORKSPACE" --hours 1 --limit 30 --verbose
  : > "$GMAIL_TS_FILE"
else
  printf '[%s] STEP gmail-watch: skipped (cooldown %ss)\n' "$(date '+%F %T')" "$((3600 - (NOW - LAST)))" >> "$LOG_FILE"
fi

printf '[%s] PIPELINE done\n' "$(date '+%F %T')" >> "$LOG_FILE"
