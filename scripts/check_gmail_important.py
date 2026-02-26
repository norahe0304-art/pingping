#!/usr/bin/env python3
# [INPUT]: 依赖 gog gmail search 的结构化结果与本地 state 文件。
# [OUTPUT]: 增量写入 memory/shared/YYYY-MM-DD-gmail-watch.md，并输出重要邮件摘要供上层转发。
# [POS]: scripts 同步链路中的 Gmail 重要邮件探针，避免 LLM 临场拼命令导致不稳定。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List


HIGH_KEYWORDS = [
    "urgent",
    "asap",
    "deadline",
    "interview",
    "offer",
    "contract",
    "invoice",
    "payment",
    "security",
    "verify",
    "reset",
    "账单",
    "面试",
    "合同",
    "付款",
    "报销",
    "紧急",
]

MEDIUM_KEYWORDS = [
    "meeting",
    "schedule",
    "follow up",
    "proposal",
    "demo",
    "partnership",
    "launch",
    "hiring",
    "合作",
    "日程",
    "安排",
    "确认",
]

NOISE_SENDERS = [
    "facebookmail.com",
    "news.us.shein.com",
    "mailer-daemon",
    "notification",
    "noreply",
    "no-reply",
]


@dataclass
class GmailItem:
    msg_id: str
    date: str
    sender: str
    subject: str
    labels: List[str]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Check important Gmail messages deterministically")
    p.add_argument("--workspace", default=str(Path.home() / ".openclaw" / "workspace"))
    p.add_argument("--hours", type=int, default=1, help="Look back N hours")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--account", default="", help="Gmail account; empty uses gog default")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def run_gog_search(hours: int, limit: int, account: str) -> List[Dict]:
    # Keep query deterministic and conservative; exclude heavy marketing categories.
    query = (
        f"newer_than:{hours}h in:inbox is:unread "
        "-category:promotions -category:social -category:forums"
    )
    cmd = [
        "gog",
        "gmail",
        "search",
        query,
        "--json",
        "--results-only",
        "--limit",
        str(limit),
    ]
    if account:
        cmd.extend(["--account", account])

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "gog gmail search failed")

    try:
        data = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid gog json: {exc}") from exc

    if not isinstance(data, list):
        return []
    return data


def normalize_item(raw: Dict) -> GmailItem:
    return GmailItem(
        msg_id=str(raw.get("id", "")).strip(),
        date=str(raw.get("date", "")).strip(),
        sender=str(raw.get("from", "")).strip(),
        subject=str(raw.get("subject", "")).strip(),
        labels=[str(x) for x in (raw.get("labels") or []) if isinstance(x, (str, int, float))],
    )


def score_item(item: GmailItem) -> tuple[int, str, List[str]]:
    text = f"{item.subject} {item.sender}".lower()
    score = 0
    reasons: List[str] = []

    for kw in HIGH_KEYWORDS:
        if kw in text:
            score += 3
            reasons.append(f"high:{kw}")
            break

    for kw in MEDIUM_KEYWORDS:
        if kw in text:
            score += 2
            reasons.append(f"mid:{kw}")
            break

    if "CATEGORY_PERSONAL" in item.labels or "IMPORTANT" in item.labels:
        score += 2
        reasons.append("label:important")

    if re.search(r"(github|notion|vercel|openai|anthropic|minimax)", text):
        score += 1
        reasons.append("sender/topic:work")

    if any(noise in text for noise in NOISE_SENDERS):
        score -= 3
        reasons.append("noise")

    if score >= 4:
        level = "high"
    elif score >= 2:
        level = "medium"
    else:
        level = "low"
    return score, level, reasons


def load_state(path: Path) -> Dict:
    if not path.exists():
        return {"seen_ids": [], "updated_at": ""}
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"seen_ids": [], "updated_at": ""}
    ids = obj.get("seen_ids")
    if not isinstance(ids, list):
        ids = []
    return {"seen_ids": [str(x) for x in ids], "updated_at": str(obj.get("updated_at", ""))}


def save_state(path: Path, state: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def append_report(report_file: Path, ts: str, new_items: List[GmailItem], important: List[tuple[GmailItem, int, str, List[str]]]) -> None:
    report_file.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = []
    lines.append(f"## run {ts}")
    lines.append(f"- new_unread: {len(new_items)}")
    lines.append(f"- important: {len(important)}")
    if important:
        lines.append("- items:")
        for item, score, level, reasons in important:
            reason_txt = ", ".join(reasons[:3]) if reasons else "n/a"
            lines.append(
                f"  - [{level}] ({score}) {item.subject} | {item.sender} | {item.date} | id={item.msg_id} | reason={reason_txt}"
            )
    lines.append("")
    with report_file.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace)
    memory_shared = workspace / "memory" / "shared"
    state_file = memory_shared / ".gmail_watch_state.json"
    report_file = memory_shared / f"{datetime.now().astimezone().strftime('%Y-%m-%d')}-gmail-watch.md"

    state = load_state(state_file)
    seen = set(state.get("seen_ids", []))

    raw_items = run_gog_search(hours=args.hours, limit=args.limit, account=args.account)
    items = [normalize_item(x) for x in raw_items]
    items = [x for x in items if x.msg_id]

    new_items = [x for x in items if x.msg_id not in seen]
    important: List[tuple[GmailItem, int, str, List[str]]] = []

    for item in new_items:
        score, level, reasons = score_item(item)
        if level in ("high", "medium"):
            important.append((item, score, level, reasons))

    now = datetime.now().astimezone().isoformat(timespec="seconds")
    append_report(report_file, now, new_items, important)

    # Keep bounded state; newest first by current fetch order.
    next_seen = [x.msg_id for x in items] + [x for x in state.get("seen_ids", []) if x not in {i.msg_id for i in items}]
    next_seen = next_seen[:2000]
    save_state(state_file, {"seen_ids": next_seen, "updated_at": now})

    if important:
        print(f"GMAIL_IMPORTANT count={len(important)}")
        for item, score, level, reasons in important[:10]:
            reason_txt = ",".join(reasons[:2]) if reasons else "n/a"
            print(f"- [{level}] ({score}) {item.subject} | {item.sender} | id={item.msg_id} | {reason_txt}")
    else:
        print(f"GMAIL_IMPORTANT count=0 new_unread={len(new_items)}")

    if args.verbose:
        print(f"report={report_file}")
        print(f"state={state_file}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"GMAIL_WATCH_ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
