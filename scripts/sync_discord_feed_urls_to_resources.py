#!/usr/bin/env python3
# [INPUT]: 依赖 memory/shared/YYYY-MM-DD-discord-feed.md 的结构化消息文本。
# [OUTPUT]: 生成 Resources/*.md 资源笔记，并更新 memory/shared/.resource_url_sync_state.json。
# [POS]: scripts 同步链路中的 URL->Resources 落盘器，补齐 feed 与知识库之间的最后一跳。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""Sync URLs from shared discord feed files into Resources notes.

- Source: memory/shared/YYYY-MM-DD-discord-feed.md
- Target: Resources/YYYY-MM-DD-<slug>.md
- State:  memory/shared/.resource_url_sync_state.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.parse import urlparse


URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Keep strict signal quality for resource notes.
SKIP_HOSTS = {
    "localhost",
    "127.0.0.1",
    "discord.com",
    "tenor.com",
}

SKIP_SCHEMES = {"http"}


@dataclass
class FeedMessage:
    date: str
    channel: str
    message_id: str
    timestamp: str
    sender: str
    text: str


@dataclass
class ResourceHit:
    message: FeedMessage
    url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync discord feed URLs to Resources")
    parser.add_argument("--workspace", default=os.path.expanduser("~/.openclaw/workspace"))
    parser.add_argument("--days", type=int, default=2, help="Look back N days including today")
    parser.add_argument("--since", default="", help="Start date YYYY-MM-DD (overrides --days)")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def today_local() -> datetime:
    return datetime.now().astimezone()


def date_range(days: int) -> List[str]:
    base = today_local().date()
    out: List[str] = []
    for i in range(days):
        out.append((base - timedelta(days=i)).strftime("%Y-%m-%d"))
    out.sort()
    return out


def range_since(since: str) -> List[str]:
    if not DATE_RE.match(since):
        raise ValueError(f"Invalid --since: {since}")
    s = datetime.strptime(since, "%Y-%m-%d").date()
    e = today_local().date()
    if s > e:
        return []
    out: List[str] = []
    cur = s
    while cur <= e:
        out.append(cur.strftime("%Y-%m-%d"))
        cur += timedelta(days=1)
    return out


def parse_feed(path: Path, date_str: str) -> List[FeedMessage]:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    current_channel = ""
    messages: List[FeedMessage] = []

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
                nxt_str = nxt.strip()
                if nxt.startswith("## ") or nxt_str.startswith("- message_id:"):
                    break
                if nxt_str.startswith("timestamp:"):
                    ts = nxt_str.split(":", 1)[1].strip()
                elif nxt_str.startswith("sender:"):
                    sender = nxt_str.split(":", 1)[1].strip()
                elif nxt_str.startswith("text:") and not text:
                    text = nxt_str.split(":", 1)[1].strip()
                j += 1

            if current_channel and msg_id:
                messages.append(
                    FeedMessage(
                        date=date_str,
                        channel=current_channel,
                        message_id=msg_id,
                        timestamp=ts,
                        sender=sender,
                        text=text,
                    )
                )
            i = j
            continue

        i += 1

    return messages


def normalize_url(raw: str) -> str:
    url = raw.strip().rstrip(",.;>")
    return url


def is_resource_url(url: str) -> bool:
    try:
        p = urlparse(url)
    except Exception:
        return False

    if p.scheme.lower() in SKIP_SCHEMES:
        return False
    host = (p.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if host in SKIP_HOSTS:
        return False
    if not host:
        return False
    return True


def url_fingerprint(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()


def load_state(path: Path) -> Dict:
    if not path.exists():
        return {"urls": {}, "last_sync": ""}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"urls": {}, "last_sync": ""}
    urls = data.get("urls")
    if not isinstance(urls, dict):
        urls = {}
    return {"urls": urls, "last_sync": data.get("last_sync", "")}


def save_state(path: Path, state: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def slug_from_url(url: str) -> str:
    p = urlparse(url)
    host = (p.netloc or "source").lower()
    if host.startswith("www."):
        host = host[4:]
    path = (p.path or "").strip("/")
    path = re.sub(r"[^a-zA-Z0-9/_-]", "", path)
    chunks = [c for c in path.split("/") if c]
    tail = "-".join(chunks[-2:]) if chunks else "link"
    slug = f"{host}-{tail}" if tail else host
    slug = slug.replace("/", "-")
    slug = re.sub(r"-+", "-", slug)
    slug = slug[:80].strip("-")
    return slug or "resource-link"


def first_nonempty(items: Iterable[str]) -> str:
    for it in items:
        if it:
            return it
    return ""


def build_note(hit: ResourceHit) -> str:
    now_iso = datetime.now().astimezone().isoformat()
    title = slug_from_url(hit.url)
    sender = hit.message.sender or "unknown"
    text = (hit.message.text or "").strip()

    lines: List[str] = []
    lines.append("---")
    lines.append("type: resource")
    lines.append("status: inbox")
    lines.append(f"created_at: \"{now_iso}\"")
    lines.append(f"captured_date: \"{hit.message.date}\"")
    lines.append(f"source_channel: \"{hit.message.channel}\"")
    lines.append(f"source_sender: \"{sender}\"")
    lines.append(f"message_id: \"{hit.message.message_id}\"")
    lines.append(f"original_url: \"{hit.url}\"")
    lines.append("source_title: \"\"")
    lines.append("source_author: \"\"")
    lines.append("published_at: \"\"")
    lines.append("tags: [resource, discord]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## Source")
    lines.append(f"- URL: {hit.url}")
    lines.append(f"- Captured from: {hit.message.date} | {hit.message.channel} | {sender}")
    lines.append(f"- Message ID: {hit.message.message_id}")
    lines.append("")
    lines.append("## Captured Context")
    if text:
        lines.append(f"> {text}")
    else:
        lines.append("- (no text body)")
    lines.append("")
    lines.append("## Notes To Expand")
    lines.append("- [ ] Read source and extract 8-12 key points")
    lines.append("- [ ] Add 3+ direct quotes")
    lines.append("- [ ] Add 3-5 actionable takeaways")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace)
    resources_dir = workspace / "Resources"
    shared_dir = workspace / "memory" / "shared"
    state_path = shared_dir / ".resource_url_sync_state.json"

    resources_dir.mkdir(parents=True, exist_ok=True)

    dates = range_since(args.since) if args.since else date_range(max(1, args.days))
    if not dates:
        if args.verbose:
            print("no date range")
        return 0

    all_messages: List[FeedMessage] = []
    for d in dates:
        fp = shared_dir / f"{d}-discord-feed.md"
        if not fp.exists():
            continue
        all_messages.extend(parse_feed(fp, d))

    if args.verbose:
        print(f"dates={dates}")
        print(f"messages_parsed={len(all_messages)}")

    state = load_state(state_path)
    seen = state.get("urls", {})
    if not isinstance(seen, dict):
        seen = {}

    hits: List[ResourceHit] = []
    for msg in all_messages:
        urls = [normalize_url(u) for u in URL_RE.findall(msg.text or "")]
        for u in urls:
            if not is_resource_url(u):
                continue
            hits.append(ResourceHit(message=msg, url=u))

    # Newest first, then keep first url occurrence.
    hits.sort(key=lambda h: first_nonempty([h.message.timestamp, h.message.date]), reverse=True)
    picked: Dict[str, ResourceHit] = {}
    for h in hits:
        fp = url_fingerprint(h.url)
        if fp in picked:
            continue
        picked[fp] = h

    created = 0
    skipped = 0
    for fp, h in picked.items():
        if fp in seen:
            skipped += 1
            continue

        date_part = h.message.date
        slug = slug_from_url(h.url)
        out = resources_dir / f"{date_part}-{slug}.md"

        # Avoid accidental overwrite collisions.
        if out.exists():
            suffix = fp[:8]
            out = resources_dir / f"{date_part}-{slug}-{suffix}.md"

        out.write_text(build_note(h), encoding="utf-8")
        seen[fp] = {
            "url": h.url,
            "file": str(out),
            "message_id": h.message.message_id,
            "channel": h.message.channel,
            "timestamp": h.message.timestamp,
            "synced_at": datetime.now().astimezone().isoformat(),
        }
        created += 1

    state["urls"] = seen
    state["last_sync"] = datetime.now().astimezone().isoformat()
    save_state(state_path, state)

    print(json.dumps({
        "dates": dates,
        "messages_parsed": len(all_messages),
        "url_hits": len(hits),
        "unique_urls": len(picked),
        "created": created,
        "skipped_existing": skipped,
        "resources_dir": str(resources_dir),
        "state": str(state_path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
