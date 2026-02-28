#!/usr/bin/env python3
# [INPUT]: 依赖 openclaw message read 的 Discord频道消息输出。
# [OUTPUT]: 增量写入 memory/shared/YYYY-MM-DD-discord-feed.md，并更新频道checkpoint状态。
# [POS]: scripts 同步链路中的频道流水采集器，替代高token LLM式全频道记忆任务。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List


CHANNELS = [
    ("1474154247070289993", "👋-欢迎"),
    ("1474184181570343108", "📢-公告"),
    ("1474184221416362157", "💬-吹水"),
    ("1474184255734022276", "🎲-瞎玩"),
    ("1474184292971319521", "💡-反馈"),
    ("1474465453442338988", "📦-资源"),
    ("1474605868992696320", "🔧-调试"),
    ("1474985896272203786", "🎮-访客"),
    ("1477148303534592062", "📚-学习"),
    ("1474471640854302911", "💙-精华"),
    ("1475004550737035354", "🤑-项目"),
]
RESOURCE_CHANNEL_ID = "1474465453442338988"
URL_RE = re.compile(r"https?://[^\s)>\]\"']+")


@dataclass
class Message:
    message_id: str
    timestamp: str
    sender: str
    text: str
    channel_id: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sync discord channels into shared feed")
    p.add_argument("--workspace", default=str(Path.home() / ".openclaw" / "workspace"))
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--date", default="")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def today_str(date_arg: str) -> str:
    if date_arg:
        return date_arg
    return datetime.now().astimezone().strftime("%Y-%m-%d")


def load_state(path: Path) -> Dict:
    if not path.exists():
        return {"channels": {}, "last_sync": ""}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"channels": {}, "last_sync": ""}
    if not isinstance(data.get("channels"), dict):
        data["channels"] = {}
    return data


def save_state(path: Path, data: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_once(channel_id: str, limit: int, after: str) -> Dict:
    cmd = [
        "openclaw",
        "message",
        "read",
        "--channel",
        "discord",
        "--target",
        f"channel:{channel_id}",
        "--limit",
        str(limit),
        "--json",
    ]
    if after:
        cmd += ["--after", after]

    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        return {"ok": False, "error": (p.stderr or b"").decode("utf-8", "ignore")[:4000]}

    out = (p.stdout or b"").decode("utf-8", "ignore")
    idx = out.find("{")
    if idx < 0:
        return {"ok": False, "error": "no json output"}

    try:
        obj = json.loads(out[idx:])
    except Exception as e:
        return {"ok": False, "error": f"json parse failed: {e}"}

    payload = obj.get("payload", {})
    msgs = payload.get("messages", [])
    if not isinstance(msgs, list):
        msgs = []
    return {"ok": True, "messages": msgs}


def run_read(channel_id: str, limit: int, after: str) -> Dict:
    # Retry with smaller limits when plugin JSON output is truncated on large payloads.
    attempts = []
    for l in [limit, max(5, limit // 2), 8, 5]:
        if l in attempts:
            continue
        attempts.append(l)
        res = _read_once(channel_id, l, after)
        if res.get("ok"):
            return res
        err = str(res.get("error") or "")
        if "json parse failed" not in err:
            return res
    return {"ok": False, "error": "json parse failed after retries"}


def run_reads_parallel(channels: List[tuple[str, str]], limit: int, after_map: Dict[str, str], workers: int) -> Dict[str, Dict]:
    max_workers = max(1, min(workers, len(channels)))
    out: Dict[str, Dict] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {}
        for channel_id, _name in channels:
            future = pool.submit(run_read, channel_id, limit, after_map.get(channel_id, ""))
            future_map[future] = channel_id
        for future, channel_id in [(f, cid) for f, cid in future_map.items()]:
            try:
                out[channel_id] = future.result()
            except Exception as e:
                out[channel_id] = {"ok": False, "error": f"parallel read failed: {e}"}
    return out


def compact_text(content: str, max_len: int = 300) -> str:
    t = " ".join((content or "").split())
    if len(t) <= max_len:
        return t
    return t[: max_len - 3] + "..."


def normalize_messages(raw: List[Dict], channel_id: str) -> List[Message]:
    items: List[Message] = []
    for x in raw:
        msg_id = str(x.get("id") or "").strip()
        if not msg_id:
            continue
        sender = (x.get("author") or {}).get("username") or "unknown"
        ts = x.get("timestampUtc") or x.get("timestamp") or ""
        text = compact_text(x.get("content") or "")
        items.append(Message(msg_id, ts, sender, text, channel_id))

    items.sort(key=lambda m: (m.timestamp, m.message_id))
    return items


def append_feed(feed_path: Path, channel_name: str, messages: List[Message], errors: str) -> None:
    lines: List[str] = []
    lines.append(f"## {channel_name}")
    lines.append("")

    if errors:
        lines.append(f"error: {errors}")
        lines.append("")
    elif not messages:
        lines.append("no new messages")
        lines.append("")
    else:
        for m in messages:
            lines.append(f"- message_id: {m.message_id}")
            lines.append(f"  timestamp: {m.timestamp}")
            lines.append(f"  channel_id: {m.channel_id}")
            lines.append(f"  sender: {m.sender}")
            lines.append(f"  text: {m.text}")
            lines.append("")

    with feed_path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def ensure_feed_header(feed_path: Path) -> None:
    if feed_path.exists() and feed_path.stat().st_size > 0:
        return
    now = datetime.now().astimezone().isoformat()
    title = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    with feed_path.open("w", encoding="utf-8") as f:
        f.write(f"# Discord 频道消息汇总 - {title}\n\n")
        f.write(f"记录时间: {now}\n")
        f.write("本轮新增消息数: pending\n\n")


def main() -> int:
    args = parse_args()
    ws = Path(args.workspace)
    date_s = today_str(args.date)

    shared_dir = ws / "memory" / "shared"
    shared_dir.mkdir(parents=True, exist_ok=True)

    feed_path = shared_dir / f"{date_s}-discord-feed.md"
    state_path = shared_dir / ".discord_channels_last_ids.json"

    state = load_state(state_path)
    channels_state = state.get("channels", {})

    ensure_feed_header(feed_path)

    summary = {}
    total_new = 0
    appended_sections = 0
    resource_url_new = 0

    after_map: Dict[str, str] = {}
    for channel_id, _name in CHANNELS:
        after_map[channel_id] = str(channels_state.get(channel_id, {}).get("last_id") or "")

    read_results = run_reads_parallel(CHANNELS, args.limit, after_map, args.workers)

    for channel_id, name in CHANNELS:
        last_id = str(channels_state.get(channel_id, {}).get("last_id") or "")
        res = read_results.get(channel_id, {"ok": False, "error": "missing parallel result"})
        err = ""
        messages: List[Message] = []

        if not res.get("ok"):
            err = str(res.get("error") or "read failed")
            summary[name] = {"new": 0, "error": True}
        else:
            messages = normalize_messages(res.get("messages", []), channel_id)
            # Guard: if API ignored --after and returned old messages, keep only > last_id lexicographically.
            if last_id:
                messages = [m for m in messages if m.message_id > last_id]

            new_count = len(messages)
            total_new += new_count
            summary[name] = {"new": new_count, "error": False}

            if messages:
                channels_state[channel_id] = {
                    "last_id": messages[-1].message_id,
                    "last_sync": datetime.now().astimezone().isoformat(),
                    "channel_name": name,
                }
                if channel_id == RESOURCE_CHANNEL_ID:
                    resource_url_new += sum(1 for m in messages if URL_RE.search(m.text or ""))

        # Performance: avoid ballooning feed files with repeated "no new messages"
        # blocks every 15 minutes. Persist only new messages or read errors.
        if err or messages:
            append_feed(feed_path, name, messages, err)
            appended_sections += 1

    state["channels"] = channels_state
    state["last_sync"] = datetime.now().astimezone().isoformat()
    save_state(state_path, state)

    resource_sync_invoked = False
    resource_sync_error = ""
    if resource_url_new > 0:
        # Event-style trigger: only compile resources when new URL appears in resource channel.
        script = ws / "scripts" / "sync_discord_feed_urls_to_resources.py"
        if script.exists():
            p = subprocess.run(
                [
                    "python3",
                    str(script),
                    "--workspace",
                    str(ws),
                    "--vault",
                    "obsidian",
                    "--days",
                    "30",
                ],
                capture_output=True,
                text=True,
            )
            resource_sync_invoked = True
            if p.returncode != 0:
                resource_sync_error = (p.stderr or p.stdout or "").strip()[:800]
        else:
            resource_sync_error = f"missing script: {script}"

    result = {
        "date": date_s,
        "feed": str(feed_path),
        "state": str(state_path),
        "total_new": total_new,
        "appended_sections": appended_sections,
        "resource_url_new": resource_url_new,
        "resource_sync_invoked": resource_sync_invoked,
        "resource_sync_error": resource_sync_error,
        "channels": summary,
    }
    print(json.dumps(result, ensure_ascii=False))

    if args.verbose:
        print("sync completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
