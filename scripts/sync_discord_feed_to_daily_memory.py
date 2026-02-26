#!/usr/bin/env python3
"""Deterministically sync discord-feed into shared daily summary.

- Source: memory/shared/YYYY-MM-DD-discord-feed.md
- Target: memory/shared/YYYY-MM-DD-discord-daily.md
- State:  memory/shared/.discord_feed_to_shared_daily_state.YYYY-MM-DD.json
          (legacy fallback:
            memory/shared/.discord_feed_to_shared_daily_state.json,
            memory/.discord_feed_sync_state.json)
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync discord feed into shared daily summary")
    parser.add_argument("--workspace", default=os.path.expanduser("~/.openclaw/workspace"))
    parser.add_argument("--date", default="", help="YYYY-MM-DD, default local today")
    parser.add_argument("--sender", default="Nora", help="Primary sender name for highlight")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def resolve_date(date_arg: str) -> str:
    if date_arg:
        if not DATE_RE.match(date_arg):
            raise ValueError(f"Invalid --date: {date_arg}")
        return date_arg
    return datetime.now().astimezone().strftime("%Y-%m-%d")


def load_state(path: Path, date_str: str) -> Dict:
    if not path.exists():
        return {"date": date_str, "processed_ids": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"date": date_str, "processed_ids": []}

    if data.get("date") != date_str:
        return {"date": date_str, "processed_ids": []}

    ids = data.get("processed_ids", [])
    if not isinstance(ids, list):
        ids = []
    return {"date": date_str, "processed_ids": ids}


def save_state(path: Path, state: Dict) -> None:
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_feed(feed_text: str) -> List[Dict[str, str]]:
    lines = feed_text.splitlines()
    current_channel = ""
    messages: List[Dict[str, str]] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            current_channel = line[3:].strip()
            i += 1
            continue

        stripped = line.strip()
        if stripped.startswith("- message_id:"):
            msg_id = stripped.split(":", 1)[1].strip()
            ts = ""
            sender = ""
            text = ""

            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if nxt.startswith("## ") or nxt.strip().startswith("- message_id:"):
                    break
                s = nxt.strip()
                if s.startswith("timestamp:"):
                    ts = s.split(":", 1)[1].strip()
                elif s.startswith("sender:"):
                    sender = s.split(":", 1)[1].strip()
                elif s.startswith("text:") and not text:
                    text = s.split(":", 1)[1].strip()
                j += 1

            if current_channel and msg_id:
                messages.append(
                    {
                        "message_id": msg_id,
                        "timestamp": ts,
                        "channel": current_channel,
                        "sender": sender,
                        "text": text,
                    }
                )
            i = j
            continue

        i += 1

    return messages


def compact_time(ts: str) -> str:
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%H:%M:%S")
    except Exception:
        return ts


def ensure_target_file(target_path: Path, date_str: str) -> None:
    if target_path.exists():
        return
    target_path.write_text(f"# Discord Daily Summary - {date_str}\n\n", encoding="utf-8")


def append_summary(target_path: Path, date_str: str, feed_path: Path, new_msgs: List[Dict], sender_name: str) -> None:
    channel_counts = Counter(m["channel"] for m in new_msgs)
    top_channels = channel_counts.most_common(3)

    sender_aliases = {sender_name.lower(), "nora", "yixiaohe"}
    sender_msgs = [m for m in new_msgs if m.get("sender", "").lower() in sender_aliases]
    sender_latest = sorted(sender_msgs, key=lambda x: x.get("timestamp", ""), reverse=True)[:8]

    now_str = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    lines = []
    lines.append(f"## Discord Feed Sync - {now_str}")
    lines.append("")
    lines.append(f"- source: {feed_path}")
    lines.append(f"- new_messages: {len(new_msgs)}")
    lines.append(f"- {sender_name}_messages: {len(sender_msgs)}")

    if top_channels:
        joined = ", ".join([f"{c}({n})" for c, n in top_channels])
        lines.append(f"- top_channels: {joined}")
    else:
        lines.append("- top_channels: none")

    if sender_latest:
        lines.append(f"- {sender_name}_latest:")
        for m in sender_latest:
            t = compact_time(m.get("timestamp", ""))
            text = (m.get("text", "") or "").replace("\n", " ").strip()
            if len(text) > 120:
                text = text[:117] + "..."
            lines.append(f"  - [{t}][{m.get('channel','')}] {text}")
    else:
        lines.append(f"- {sender_name}_latest: none")

    lines.append("")
    with target_path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))
        f.write("\n")


def main() -> int:
    args = parse_args()
    date_str = resolve_date(args.date)

    workspace = Path(args.workspace)
    feed_path = workspace / "memory" / "shared" / f"{date_str}-discord-feed.md"
    target_path = workspace / "memory" / "shared" / f"{date_str}-discord-daily.md"
    state_path = workspace / "memory" / "shared" / f".discord_feed_to_shared_daily_state.{date_str}.json"
    legacy_shared_state_path = workspace / "memory" / "shared" / ".discord_feed_to_shared_daily_state.json"
    legacy_state_path = workspace / "memory" / ".discord_feed_sync_state.json"

    if not feed_path.exists():
        if args.verbose:
            print(f"feed file not found: {feed_path}")
        return 0

    feed_text = feed_path.read_text(encoding="utf-8", errors="ignore")
    all_msgs = parse_feed(feed_text)

    if state_path.exists():
        state = load_state(state_path, date_str)
    elif legacy_shared_state_path.exists():
        state = load_state(legacy_shared_state_path, date_str)
    else:
        # Compatibility: reuse previously processed IDs to avoid one-time flood.
        state = load_state(legacy_state_path, date_str)
    processed = set(state.get("processed_ids", []))

    new_msgs = [m for m in all_msgs if m["message_id"] not in processed]

    if args.verbose:
        print(f"parsed={len(all_msgs)} processed={len(processed)} new={len(new_msgs)}")

    if not new_msgs:
        return 0

    ensure_target_file(target_path, date_str)
    append_summary(target_path, date_str, feed_path, new_msgs, args.sender)

    for m in new_msgs:
        processed.add(m["message_id"])

    state = {
        "date": date_str,
        "processed_ids": list(processed),
        "last_sync": datetime.now().astimezone().isoformat(),
        "last_new_count": len(new_msgs),
    }
    save_state(state_path, state)

    if args.verbose:
        print(f"appended {len(new_msgs)} messages into {target_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
