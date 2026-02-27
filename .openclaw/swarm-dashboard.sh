#!/usr/bin/env bash
# [INPUT]: 可选 --once/--interval N/--repo PATH/--limit N。
# [OUTPUT]: 输出 swarm 派遣可视化面板（任务状态、运行中明细、僵尸检测、日志尾部）。
# [POS]: 人工巡检与实时观测入口，用于确认 codex/opencode 正在做什么。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="$(cd "$SCRIPT_DIR/.." && pwd)"
SWARM_BIN="${SWARM_BIN:-/Users/nora/.openclaw/swarm-core/swarm}"
ACTIVE_TASKS_JSON="$SCRIPT_DIR/active-tasks.json"
INTERVAL=3
TAIL_LIMIT=2
ONCE=0

usage() {
  cat <<'USAGE'
Usage: swarm-dashboard.sh [options]

Options:
  --once              Render once and exit.
  --interval <sec>    Refresh interval in seconds (default: 3).
  --repo <path>       Repo path for swarm status (default: parent dir).
  --limit <n>         Number of recent tasks/logs to show (default: 2).
  -h, --help          Show this help.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --once)
      ONCE=1
      shift
      ;;
    --interval)
      INTERVAL="${2:-}"
      shift 2
      ;;
    --repo)
      REPO_PATH="${2:-}"
      shift 2
      ;;
    --limit)
      TAIL_LIMIT="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ! -x "$SWARM_BIN" ]]; then
  echo "ERROR: swarm binary not found or not executable: $SWARM_BIN" >&2
  exit 1
fi

if ! [[ "$INTERVAL" =~ ^[0-9]+$ ]] || [[ "$INTERVAL" -lt 1 ]]; then
  echo "ERROR: --interval must be a positive integer" >&2
  exit 1
fi

if ! [[ "$TAIL_LIMIT" =~ ^[0-9]+$ ]] || [[ "$TAIL_LIMIT" -lt 1 ]]; then
  echo "ERROR: --limit must be a positive integer" >&2
  exit 1
fi

render_dashboard() {
  local status_json
  local status_file

  if ! status_json="$($SWARM_BIN status --repo "$REPO_PATH" --format json 2>/dev/null)"; then
    status_json='[]'
  fi

  status_file="$(mktemp)"
  printf '%s\n' "$status_json" > "$status_file"

  printf '\033[2J\033[H'
  echo "== Swarm Dispatch Dashboard =="
  echo "time: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "repo: $REPO_PATH"
  echo

  echo "[1] Status summary"
  jq -r '
    if length == 0 then
      "total=0"
    else
      "total=" + (length|tostring),
      (group_by(.status)
       | map(.[0].status + "=" + (length|tostring))
       | join("  "))
    end
  ' "$status_file"

  echo
  echo "[2] Driver split (codex/opencode)"
  jq -r '
    def cnt($d;$s): map(select(.driver==$d and .status==$s)) | length;
    ["driver","running","pending","failed","completed"],
    (["codex","opencode"][] as $d
      | [$d, cnt($d;"running"), cnt($d;"pending"), cnt($d;"failed"), cnt($d;"completed")])
    | @tsv
  ' "$status_file" | column -t -s $'\t'

  echo
  echo "[3] Running tasks"
  if [[ "$(jq 'map(select(.status=="running")) | length' "$status_file")" -eq 0 ]]; then
    echo "none"
  else
    jq -r '
      ["id","driver","model","started_at","tmux_session"],
      (map(select(.status=="running"))[]
      | [.id, .driver, (.model // ""), (.started_at // ""), (.tmux_session // "")])
      | @tsv
    ' "$status_file" | column -t -s $'\t'
  fi

  echo
  echo "[4] Zombie check (running task but tmux missing)"
  local zombies=0
  while IFS=$'\t' read -r task_id tmux_session; do
    [[ -n "$task_id" ]] || continue
    if [[ -z "$tmux_session" ]]; then
      echo "zombie: $task_id (no tmux session set)"
      zombies=$((zombies + 1))
      continue
    fi
    if ! tmux has-session -t "$tmux_session" 2>/dev/null; then
      echo "zombie: $task_id ($tmux_session missing)"
      zombies=$((zombies + 1))
    fi
  done < <(jq -r 'map(select(.status=="running"))[] | [.id, (.tmux_session // "")] | @tsv' "$status_file")

  if [[ "$zombies" -eq 0 ]]; then
    echo "none"
  fi

  echo
  echo "[5] Recent task updates"
  jq -r --argjson limit "$TAIL_LIMIT" '
    if length == 0 then
      "none"
    else
      ["updated_at","status","driver","id","reason"],
      (sort_by(.updated_at // .created_at) | reverse | .[0:$limit][]
      | [(.updated_at // .created_at // ""), .status, .driver, .id, (.last_error_reason // "")])
      | @tsv
    end
  ' "$status_file" | column -t -s $'\t'

  echo
  echo "[6] Log tail"
  local has_running="$(jq 'map(select(.status=="running")) | length' "$status_file")"
  if [[ "$has_running" -gt 0 ]]; then
    while IFS=$'\t' read -r task_id log_path; do
      [[ -n "$task_id" ]] || continue
      echo "--- $task_id ---"
      if [[ -n "$log_path" && -f "$log_path" ]]; then
        tail -n 6 "$log_path"
      else
        echo "(no log file)"
      fi
    done < <(jq -r 'map(select(.status=="running"))[] | [.id, (.log_path // "")] | @tsv' "$status_file")
  else
    jq -r --argjson limit "$TAIL_LIMIT" '
      sort_by(.updated_at // .created_at)
      | reverse
      | .[0:$limit][]
      | [.id, (.log_path // "")]
      | @tsv
    ' "$status_file" | while IFS=$'\t' read -r task_id log_path; do
      [[ -n "$task_id" ]] || continue
      echo "--- $task_id ---"
      if [[ -n "$log_path" && -f "$log_path" ]]; then
        tail -n 6 "$log_path"
      else
        echo "(no log file)"
      fi
    done
  fi

  if [[ -f "$ACTIVE_TASKS_JSON" ]]; then
    echo
    echo "[7] active-tasks.json projection"
    jq -r '
      if length == 0 then
        "none"
      else
        ["status","agent","model","id"],
        (sort_by(.startedAt) | reverse | .[0:8][] | [.status, .agent, .model, .id])
        | @tsv
      end
    ' "$ACTIVE_TASKS_JSON" | column -t -s $'\t'
  fi

  rm -f "$status_file"
}

while true; do
  render_dashboard
  if [[ "$ONCE" -eq 1 ]]; then
    exit 0
  fi
  sleep "$INTERVAL"
done
