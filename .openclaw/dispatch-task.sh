#!/usr/bin/env bash
# [INPUT]: Free-form task text and optional task id.
# [OUTPUT]: Routes task to codex or opencode via spawn-agent.sh.
# [POS]: Messenger-layer hard router; enforces delegation-first execution.
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="$(cd "$SCRIPT_DIR/.." && pwd)"
SPAWN_SCRIPT="$SCRIPT_DIR/spawn-agent.sh"

usage() {
  cat <<'USAGE'
Usage:
  .openclaw/dispatch-task.sh --prompt "<task>" [--id <task-id>] [--driver auto|codex|opencode] [--dry-run]
  .openclaw/dispatch-task.sh "<task>" [codex|opencode|auto]

Behavior:
  - driver=auto: classify task and route
  - code-heavy / git-heavy tasks -> codex
  - general execution tasks -> opencode
USAGE
}

lower() {
  tr '[:upper:]' '[:lower:]' <<<"$1"
}

is_code_heavy() {
  local text_lc="$1"

  # Strong indicators for codex routing.
  local patterns=(
    'git '
    'pull request'
    'pr '
    'merge'
    'rebase'
    'conflict'
    'commit'
    'push'
    'checkout'
    'branch'
    'patch'
    'diff'
    'refactor'
    'bug'
    'fix '
    'unit test'
    'integration test'
    'e2e'
    'pytest'
    'jest'
    'vitest'
    'tsc'
    'lint'
    'build'
    'compile'
    'deploy'
    'api'
    'endpoint'
    'schema'
    'migration'
    'typescript'
    'javascript'
    'python'
    'go '
    'rust'
    'sql'
    'docker'
    'kubernetes'
    'openclaw config'
  )

  for p in "${patterns[@]}"; do
    if [[ "$text_lc" == *"$p"* ]]; then
      return 0
    fi
  done

  return 1
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

PROMPT=""
TASK_ID=""
DRIVER="auto"
DRY_RUN="false"

if [[ $# -gt 0 && "${1:-}" != -* ]]; then
  PROMPT="$1"
  shift
  if [[ $# -gt 0 && "${1:-}" != -* ]]; then
    case "$(lower "$1")" in
      codex|opencode|auto)
        DRIVER="$(lower "$1")"
        shift
        ;;
    esac
  fi
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)
      PROMPT="${2:-}"
      shift 2
      ;;
    --id|--task-id)
      TASK_ID="${2:-}"
      shift 2
      ;;
    --driver|--agent)
      DRIVER="$(lower "${2:-auto}")"
      shift 2
      ;;
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    *)
      if [[ -z "$PROMPT" ]]; then
        PROMPT="$1"
      fi
      shift
      ;;
  esac
done

if [[ -z "$PROMPT" ]]; then
  echo "ERROR: prompt is required" >&2
  usage >&2
  exit 1
fi

if [[ ! -x "$SPAWN_SCRIPT" ]]; then
  echo "ERROR: spawn script not executable: $SPAWN_SCRIPT" >&2
  exit 1
fi

if [[ "$DRIVER" != "codex" && "$DRIVER" != "opencode" && "$DRIVER" != "auto" ]]; then
  DRIVER="auto"
fi

if [[ "$DRIVER" == "auto" ]]; then
  prompt_lc="$(lower "$PROMPT")"
  if is_code_heavy "$prompt_lc"; then
    DRIVER="codex"
  else
    DRIVER="opencode"
  fi
fi

if [[ -z "$TASK_ID" ]]; then
  slug="$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9._-' '-' | sed 's/^-*//;s/-*$//')"
  slug="${slug:0:40}"
  [[ -z "$slug" ]] && slug="task"
  TASK_ID="${DRIVER}-${slug}-$(date +%s)"
fi

echo "dispatch driver=$DRIVER task_id=$TASK_ID"

if [[ "$DRY_RUN" == "true" ]]; then
  echo "dry-run: $SPAWN_SCRIPT --id $TASK_ID --agent $DRIVER --prompt <omitted>"
  exit 0
fi

exec "$SPAWN_SCRIPT" --id "$TASK_ID" --agent "$DRIVER" --prompt "$PROMPT"
