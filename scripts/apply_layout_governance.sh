#!/usr/bin/env bash
# [INPUT]: openclaw home layout with runtime dirs and workspace repo directories.
# [OUTPUT]: applies idempotent physical isolation + repo canonicalization + compatibility symlinks.
# [POS]: one-shot governance executor for layout normalization without business-logic mutation.
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

set -euo pipefail

ROOT="${1:-/Users/nora/.openclaw}"
WORKSPACE="$ROOT/workspace"
SYNC_INDEX="${SYNC_INDEX:-1}"

ensure_runtime_isolation() {
  mkdir -p "$ROOT/runtime"

  local runtime_dirs=(browser logs agents venv)
  for d in "${runtime_dirs[@]}"; do
    if [[ -L "$ROOT/$d" ]]; then
      continue
    fi
    if [[ -d "$ROOT/$d" ]]; then
      if [[ ! -e "$ROOT/runtime/$d" ]]; then
        mv "$ROOT/$d" "$ROOT/runtime/$d"
      fi
      ln -s "runtime/$d" "$ROOT/$d"
    fi
  done
}

ensure_repo_canonicalization() {
  mkdir -p "$WORKSPACE/projects"

  local repos=(
    agentcal
    nora-excalidraw-drawer
    pixel-agents-openclaw
    rimbo-landing
    star-office-ui
  )

  for repo in "${repos[@]}"; do
    if [[ -L "$WORKSPACE/$repo" ]]; then
      continue
    fi
    if [[ -d "$WORKSPACE/$repo" ]]; then
      if [[ ! -e "$WORKSPACE/projects/$repo" ]]; then
        mv "$WORKSPACE/$repo" "$WORKSPACE/projects/$repo"
      fi
      ln -s "projects/$repo" "$WORKSPACE/$repo"
    fi
  done
}

ensure_workspace_gitignore_links() {
  local gitignore="$WORKSPACE/.gitignore"
  local entries=(
    "agentcal"
    "nora-excalidraw-drawer"
    "pixel-agents-openclaw"
    "rimbo-landing"
    "star-office-ui"
  )

  if [[ ! -f "$gitignore" ]]; then
    return
  fi

  for entry in "${entries[@]}"; do
    if ! grep -Fxq "$entry" "$gitignore"; then
      echo "$entry" >>"$gitignore"
    fi
  done
}

sync_workspace_index() {
  if [[ "$SYNC_INDEX" != "1" ]]; then
    return
  fi

  if [[ ! -d "$WORKSPACE/.git" ]]; then
    return
  fi

  (
    cd "$WORKSPACE"
    git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

    local standalone_gitlinks=(
      agentcal
      nora-excalidraw-drawer
      pixel-agents-openclaw
    )

    for repo in "${standalone_gitlinks[@]}"; do
      if git ls-files -s -- "$repo" | grep -q '^160000 '; then
        git rm --cached "$repo" >/dev/null 2>&1 || true
      fi
    done

    if git ls-files -- "star-office-ui/*" | grep -q .; then
      git rm --cached -r star-office-ui >/dev/null 2>&1 || true
    fi

    if [[ -d "projects/star-office-ui" ]]; then
      git add projects/star-office-ui >/dev/null 2>&1 || true
    fi
  )
}

main() {
  ensure_runtime_isolation
  ensure_repo_canonicalization
  ensure_workspace_gitignore_links
  sync_workspace_index

  echo "layout governance applied"
  echo "sync index: $SYNC_INDEX (1=enabled)"
  echo "next: python3 $WORKSPACE/scripts/repo_topology_guard.py --strict"
  echo "next: python3 $WORKSPACE/scripts/sustainability_audit.py --root $ROOT --strict"
}

main "$@"
