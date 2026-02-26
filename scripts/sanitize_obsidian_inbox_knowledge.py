#!/usr/bin/env python3
# [INPUT]: 依赖 obsidian/Inbox/*.md 的现有文本内容。
# [OUTPUT]: 移除“原文摘录”式聊天转录段落，保留知识化结构与行动建议。
# [POS]: scripts 同步链路中的知识库质量守门器，防止原文转录污染沉淀层。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

from __future__ import annotations

import argparse
from pathlib import Path
import re


SECTION_HEADERS = (
    "## 最近 20 条消息（原文摘录）",
    "## 最近20条消息（原文摘录）",
    "## 最近 20 条消息",
    "## 最近20条消息",
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sanitize raw transcript sections in Obsidian Inbox notes")
    p.add_argument("--workspace", default=str(Path.home() / ".openclaw" / "workspace"))
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def strip_raw_excerpt_sections(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    removed = 0

    while i < len(lines):
        line = lines[i]
        if any(line.strip().startswith(h) for h in SECTION_HEADERS):
            removed += 1
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if re.match(r"^##\s+", nxt):
                    break
                i += 1
            continue
        out.append(line)
        i += 1

    cleaned = "\n".join(out).rstrip() + "\n"
    return cleaned, removed


def main() -> int:
    args = parse_args()
    ws = Path(args.workspace)
    inbox = ws / "obsidian" / "Inbox"
    if not inbox.exists():
        print('{"updated":0,"files":0,"removed_sections":0}')
        return 0

    updated = 0
    files = 0
    removed_sections = 0

    for note in sorted(inbox.glob("*.md")):
        if note.name == "_TEMPLATE.md":
            continue
        files += 1
        raw = note.read_text(encoding="utf-8", errors="ignore")
        cleaned, removed = strip_raw_excerpt_sections(raw)
        if removed > 0 and cleaned != raw:
            note.write_text(cleaned, encoding="utf-8")
            updated += 1
            removed_sections += removed
            if args.verbose:
                print(f"updated: {note}")

    print(f'{{"updated":{updated},"files":{files},"removed_sections":{removed_sections}}}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
