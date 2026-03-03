#!/usr/bin/env python3
# [INPUT]: Filesystem tree rooted at openclaw home, plus AGENTS-based architecture contracts.
# [OUTPUT]: Deterministic markdown audit report for L1/L2 coverage, code size, fanout, and boundary hygiene.
# [POS]: Governance guardrail script for weekly workspace sustainability checks without L3 enforcement.
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# ============================================================
# Constants
# ============================================================

CODE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs"}
EXCLUDE_DIRS = {
    "node_modules",
    ".git",
    "dist",
    ".next",
    "venv",
    "__pycache__",
    ".pnpm-store",
    "browser",
    "agents",
    "logs",
}

LINE_LIMIT = 800
FANOUT_LIMIT = 8

LINE_EXCLUDE_PREFIXES = (
    "projects/rimbo-landing/src/framer/",
    "projects/pixel-agents-openclaw/webview-ui/src/office/sprites/",
)

FANOUT_EXCLUDE_EXACT = {
    ".",
    "projects",
}

FANOUT_EXCLUDE_PREFIXES = (
    ".openclaw/",
    "memory/shared/",
    "obsidian/Resources/",
    "video gen/",
    "projects/rimbo-landing/public/images/framer/",
    "projects/rimbo-landing/public/js/framer/",
    "projects/rimbo-landing/public/fonts/framer/",
    "projects/rimbo-landing/src/framer/chunks/",
)


@dataclass
class Finding:
    severity: str
    title: str
    detail: str


# ============================================================
# Filesystem helpers
# ============================================================

def should_skip_dir(name: str) -> bool:
    return name in EXCLUDE_DIRS


def iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        base = Path(dirpath)
        for file_name in filenames:
            yield base / file_name


def count_lines(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fp:
            return sum(1 for _ in fp)
    except Exception:
        return 0


def to_relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def should_skip_line_file(rel_path: str, file_name: str) -> bool:
    if ".generated." in file_name:
        return True
    return any(rel_path.startswith(prefix) for prefix in LINE_EXCLUDE_PREFIXES)


def should_skip_fanout_dir(rel_dir: str) -> bool:
    if rel_dir in FANOUT_EXCLUDE_EXACT:
        return True
    return any(rel_dir.startswith(prefix) for prefix in FANOUT_EXCLUDE_PREFIXES)


# ============================================================
# Audit checks
# ============================================================

def check_l1(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    root_agents = root / "AGENTS.md"
    if not root_agents.exists():
        findings.append(
            Finding(
                severity="critical",
                title="Missing L1 Map",
                detail=f"Missing root AGENTS.md at {root_agents}",
            )
        )
    return findings


def check_l2_workspace(workspace: Path) -> list[Finding]:
    findings: list[Finding] = []
    missing: list[str] = []

    for child in sorted(workspace.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if should_skip_dir(child.name):
            continue

        has_files = any(p.is_file() for p in child.iterdir())
        if has_files and not (child / "AGENTS.md").exists():
            missing.append(str(child))

    if missing:
        preview = "\n".join(f"- {p}" for p in missing[:20])
        extra = "" if len(missing) <= 20 else f"\n- ... and {len(missing)-20} more"
        findings.append(
            Finding(
                severity="high",
                title="L2 Coverage Gaps",
                detail=f"Directories with files but no AGENTS.md: {len(missing)}\n{preview}{extra}",
            )
        )

    return findings


def check_line_limits(workspace: Path) -> list[Finding]:
    findings: list[Finding] = []
    offenders: list[tuple[int, Path]] = []

    for path in iter_files(workspace):
        if path.suffix.lower() not in CODE_EXTS:
            continue
        rel_path = to_relative_posix(path, workspace)
        if should_skip_line_file(rel_path, path.name):
            continue
        lines = count_lines(path)
        if lines > LINE_LIMIT:
            offenders.append((lines, path))

    offenders.sort(reverse=True, key=lambda x: x[0])
    if offenders:
        preview = "\n".join(f"- {lines:>5} {p}" for lines, p in offenders[:20])
        extra = "" if len(offenders) <= 20 else f"\n- ... and {len(offenders)-20} more"
        findings.append(
            Finding(
                severity="high",
                title="File Length Overflow",
                detail=f"{len(offenders)} files exceed {LINE_LIMIT} lines.\n{preview}{extra}",
            )
        )

    return findings


def check_fanout(workspace: Path) -> list[Finding]:
    findings: list[Finding] = []
    offenders: list[str] = []

    for dirpath, dirnames, filenames in os.walk(workspace):
        rel_dir = to_relative_posix(Path(dirpath), workspace)
        if should_skip_fanout_dir(rel_dir):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        file_count = len([f for f in filenames if not f.startswith(".")])
        dir_count = len([d for d in dirnames if not d.startswith(".")])
        if file_count > FANOUT_LIMIT or dir_count > FANOUT_LIMIT:
            offenders.append(f"- {dirpath} (files={file_count}, subdirs={dir_count})")

    if offenders:
        preview = "\n".join(offenders[:30])
        extra = "" if len(offenders) <= 30 else f"\n- ... and {len(offenders)-30} more"
        findings.append(
            Finding(
                severity="medium",
                title="Fanout Pressure",
                detail=f"{len(offenders)} directories exceed fanout {FANOUT_LIMIT}.\n{preview}{extra}",
            )
        )

    return findings


def check_runtime_boundary(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    workspace = root / "workspace"
    if not workspace.exists():
        return findings

    heavy_runtime = []
    for name in ("browser", "agents", "logs", "venv"):
        p = root / name
        if not p.exists():
            continue
        if p.is_symlink():
            target = p.resolve()
            expected = (root / "runtime" / name).resolve()
            if target == expected:
                continue
            heavy_runtime.append(f"{p} -> {target} (unexpected symlink target)")
            continue
        if p.is_dir():
            heavy_runtime.append(str(p))

    if heavy_runtime:
        lines = "\n".join(f"- {p}" for p in heavy_runtime)
        findings.append(
            Finding(
                severity="medium",
                title="Runtime / Source Boundary",
                detail=(
                    "Runtime-heavy directories should live under root/runtime with compatibility symlinks at root.\n"
                    f"{lines}"
                ),
            )
        )

    return findings


# ============================================================
# Render
# ============================================================

def severity_rank(sev: str) -> int:
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return order.get(sev, 9)


def render_report(root: Path, findings: list[Finding]) -> str:
    ordered = sorted(findings, key=lambda f: (severity_rank(f.severity), f.title))

    lines = []
    lines.append("# OpenClaw Sustainability Audit")
    lines.append("")
    lines.append(f"- Root: `{root}`")
    lines.append(f"- Findings: `{len(ordered)}`")
    lines.append("")

    if not ordered:
        lines.append("No findings. Structure is currently within configured guardrails.")
        return "\n".join(lines)

    for idx, f in enumerate(ordered, start=1):
        lines.append(f"## {idx}. [{f.severity.upper()}] {f.title}")
        lines.append("")
        lines.append(f.detail)
        lines.append("")

    lines.append("## Next Actions")
    lines.append("")
    lines.append("1. Fix CRITICAL findings before feature work.")
    lines.append("2. Burn down HIGH findings in weekly cleanup batches.")
    lines.append("3. Keep MEDIUM findings monitored by recurring audits.")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenClaw sustainability governance audit")
    parser.add_argument("--root", default="/Users/nora/.openclaw", help="OpenClaw root path")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when critical/high findings exist",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    workspace = root / "workspace"

    findings: list[Finding] = []
    findings.extend(check_l1(root))
    if workspace.exists():
        findings.extend(check_l2_workspace(workspace))
        findings.extend(check_line_limits(workspace))
        findings.extend(check_fanout(workspace))
    findings.extend(check_runtime_boundary(root))

    report = render_report(root, findings)
    print(report)

    if args.strict and any(f.severity in {"critical", "high"} for f in findings):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
