#!/usr/bin/env python3
# [INPUT]: Depends on workspace REPO_TOPOLOGY.toml and current filesystem .git/symlink layout.
# [OUTPUT]: Emits deterministic markdown findings for repo-placement and legacy-symlink policy checks.
# [POS]: Repository topology guardrail for enforcing canonical standalone-repo placement under workspace/projects.
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass
class Finding:
    severity: str
    title: str
    detail: str


def discover_git_dirs(workspace: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, _ in os.walk(workspace):
        if "node_modules" in dirpath.split(os.sep):
            continue
        if ".git" in dirnames:
            out.append(Path(dirpath) / ".git")
    return sorted(out)


def load_topology(path: Path) -> dict:
    with path.open("rb") as fp:
        return tomllib.load(fp)


def check_git_placement(workspace: Path, canonical_repos_root: Path, workspace_meta_git: Path) -> list[Finding]:
    findings: list[Finding] = []
    git_dirs = discover_git_dirs(workspace)

    misplaced = []
    for git_dir in git_dirs:
        if git_dir == workspace_meta_git:
            continue
        if not str(git_dir).startswith(str(canonical_repos_root)):
            misplaced.append(git_dir)

    if misplaced:
        detail = "\n".join(f"- {p}" for p in misplaced)
        findings.append(
            Finding(
                severity="critical",
                title="Misplaced Standalone Repositories",
                detail=(
                    "Standalone git repositories must live under canonical repos root.\n"
                    f"{detail}"
                ),
            )
        )
    return findings


def check_manifest_entries(config: dict) -> list[Finding]:
    findings: list[Finding] = []

    require_symlink = bool(config["policy"].get("require_legacy_symlinks", False))

    missing_paths = []
    bad_symlinks = []
    repos = config.get("repo", [])

    for repo in repos:
        path = Path(repo["path"])
        if not path.exists():
            missing_paths.append(path)

        legacy = repo.get("legacy_symlink")
        if require_symlink and legacy:
            legacy_path = Path(legacy)
            if not legacy_path.exists() and not legacy_path.is_symlink():
                bad_symlinks.append((legacy_path, "missing symlink"))
                continue
            if not legacy_path.is_symlink():
                bad_symlinks.append((legacy_path, "expected symlink"))
                continue
            target = legacy_path.resolve()
            if target != path.resolve():
                bad_symlinks.append((legacy_path, f"points to {target}, expected {path.resolve()}"))

    if missing_paths:
        detail = "\n".join(f"- {p}" for p in missing_paths)
        findings.append(
            Finding(
                severity="high",
                title="Manifest Path Missing",
                detail=f"Paths declared in REPO_TOPOLOGY.toml do not exist:\n{detail}",
            )
        )

    if bad_symlinks:
        detail = "\n".join(f"- {p}: {reason}" for p, reason in bad_symlinks)
        findings.append(
            Finding(
                severity="high",
                title="Legacy Symlink Drift",
                detail=f"Legacy compatibility symlinks are inconsistent:\n{detail}",
            )
        )

    return findings


def render(findings: list[Finding], config_path: Path) -> str:
    lines = [
        "# Repository Topology Guard",
        "",
        f"- Config: `{config_path}`",
        f"- Findings: `{len(findings)}`",
        "",
    ]

    if not findings:
        lines.append("No findings. Repository topology matches policy.")
        return "\n".join(lines)

    rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings = sorted(findings, key=lambda f: (rank.get(f.severity, 9), f.title))

    for idx, finding in enumerate(findings, 1):
        lines.append(f"## {idx}. [{finding.severity.upper()}] {finding.title}")
        lines.append("")
        lines.append(finding.detail)
        lines.append("")

    lines.append("## Next Actions")
    lines.append("")
    lines.append("1. Move misplaced repos under `workspace/projects`.")
    lines.append("2. Repair or remove stale legacy symlinks.")
    lines.append("3. Re-run this guard before large refactors.")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate workspace repository topology")
    parser.add_argument(
        "--config",
        default="/Users/nora/.openclaw/workspace/REPO_TOPOLOGY.toml",
        help="Path to repo topology TOML",
    )
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on critical/high findings")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).resolve()
    config = load_topology(config_path)

    workspace = Path(config["policy"]["workspace_root"]).resolve()
    canonical_repos_root = Path(config["policy"]["canonical_repos_root"]).resolve()
    workspace_meta_git = Path(config["policy"]["workspace_meta_git"]).resolve()

    findings: list[Finding] = []
    findings.extend(check_git_placement(workspace, canonical_repos_root, workspace_meta_git))
    findings.extend(check_manifest_entries(config))

    print(render(findings, config_path))

    if args.strict and any(f.severity in {"critical", "high"} for f in findings):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
