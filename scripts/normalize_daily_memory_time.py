#!/usr/bin/env python3
# [INPUT]: Depends on memory/YYYY-MM-DD.md and memory/shared/YYYY-MM-DD-discord-feed.md.
# [OUTPUT]: Emits memory/shared/YYYY-MM-DD-memory-quality.md and optionally rewrites wrong time-bucket words in daily memory.
# [POS]: Deterministic consistency guard for personal diary time labels using feed timestamps as ground truth.
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TIME_BUCKETS = {
    "凌晨": (0, 4),
    "清晨": (5, 6),
    "早上": (7, 8),
    "上午": (9, 11),
    "中午": (12, 12),
    "下午": (13, 17),
    "傍晚": (18, 19),
    "晚上": (20, 21),
    "夜里": (22, 23),
    "夜晚": (22, 23),
}

TIME_WORDS = set(TIME_BUCKETS.keys())
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{1,}|[\u4e00-\u9fff]{2,}")

STOPWORDS = {
    "今天",
    "昨天",
    "前天",
    "我们",
    "你们",
    "然后",
    "就是",
    "这个",
    "那个",
    "一个",
    "频道",
    "觉得",
    "说",
    "写",
    "讨论",
    "对话",
    "没有",
    "特别",
    "只是",
    "因为",
    "所以",
    "真的",
    "后来",
    "继续",
    "访客",
    "资源",
    "Nora",
    "nora",
    "pingping",
}


def is_ascii_word(token: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", token))


def extract_anchors(paragraph: str) -> list[str]:
    anchors: list[str] = []

    # Quoted phrases are high-precision anchors.
    for match in re.findall(r"[\"“”'‘’]([^\"“”'‘’]{4,})[\"“”'‘’]", paragraph):
        s = match.strip().lower()
        if s:
            anchors.append(s)

    # Strong English entities: Homebrew / OpenClaw / LinkedIn / Nolan...
    for token in TOKEN_RE.findall(paragraph):
        if token in STOPWORDS or token in TIME_WORDS:
            continue
        if is_ascii_word(token) and len(token) >= 4:
            anchors.append(token.lower())

    # Domain-specific connectors usually indicate concrete events.
    for token in ("我眼中的世界", "skill-from-masters", "orbitos", "homebrew", "openclaw"):
        if token in paragraph.lower():
            anchors.append(token)

    # Keep order and unique.
    seen = set()
    ordered = []
    for item in anchors:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


@dataclass
class FeedMessage:
    message_id: str
    timestamp: datetime
    text: str
    text_norm: str


@dataclass
class Issue:
    paragraph_index: int
    claimed: str
    actual: str
    evidence_count: int
    evidence_start: str
    evidence_end: str
    span_hours: float
    confidence: str
    paragraph: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize daily memory time labels")
    parser.add_argument("--workspace", default=str(Path.home() / ".openclaw" / "workspace"))
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--tz", default="America/New_York")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def parse_iso(ts: str) -> datetime | None:
    ts = ts.strip()
    if not ts:
        return None
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def extract_time_word(text: str) -> str | None:
    for word in TIME_BUCKETS.keys():
        if word in text:
            return word
    return None


def hour_to_bucket(hour: int) -> str:
    for word, (start, end) in TIME_BUCKETS.items():
        if start <= hour <= end:
            return word
    return "夜里"


def parse_feed(feed_text: str) -> list[FeedMessage]:
    lines = feed_text.splitlines()
    out: list[FeedMessage] = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("- message_id:"):
            message_id = line.split(":", 1)[1].strip()
            ts = ""
            text = ""

            j = i + 1
            while j < len(lines):
                nxt = lines[j].strip()
                if nxt.startswith("- message_id:") or lines[j].startswith("## "):
                    break
                if nxt.startswith("timestamp:"):
                    ts = nxt.split(":", 1)[1].strip()
                elif nxt.startswith("text:") and not text:
                    text = nxt.split(":", 1)[1].strip()
                j += 1

            parsed = parse_iso(ts)
            if parsed and text:
                out.append(
                    FeedMessage(
                        message_id=message_id,
                        timestamp=parsed,
                        text=text,
                        text_norm=normalize_text(text),
                    )
                )
            i = j
            continue

        i += 1

    return out


def tokenize_for_match(text: str) -> list[str]:
    tokens = []
    for token in TOKEN_RE.findall(text):
        if token in STOPWORDS:
            continue
        if token in TIME_WORDS:
            continue
        tokens.append(token.lower())
    return tokens


def match_messages(paragraph: str, feed: list[FeedMessage]) -> tuple[list[FeedMessage], int]:
    anchors = extract_anchors(paragraph)
    if anchors:
        scored = []
        for msg in feed:
            score = 0
            for anchor in anchors:
                if anchor in msg.text_norm:
                    score += 2
            if score > 0:
                scored.append((score, msg))

        scored.sort(key=lambda item: item[0], reverse=True)
        best = scored[0][0] if scored else 0
        return [msg for _, msg in scored[:12]], best

    tokens = tokenize_for_match(paragraph)
    if not tokens:
        return [], 0

    scored = []
    for msg in feed:
        score = 0
        for token in tokens:
            if token in msg.text_norm:
                score += 1
        if score >= 2:
            scored.append((score, msg))

    scored.sort(key=lambda item: item[0], reverse=True)
    best = scored[0][0] if scored else 0
    return [msg for _, msg in scored[:12]], best


def pick_actual_bucket(messages: list[FeedMessage], tz: ZoneInfo) -> tuple[str, str, str, float]:
    hours = [m.timestamp.astimezone(tz).hour for m in messages]
    hours.sort()
    pivot = hours[len(hours) // 2]
    bucket = hour_to_bucket(pivot)

    start = min(m.timestamp.astimezone(tz) for m in messages)
    end = max(m.timestamp.astimezone(tz) for m in messages)
    span_hours = round((end - start).total_seconds() / 3600, 2)
    return (
        bucket,
        start.strftime("%Y-%m-%d %H:%M:%S %Z"),
        end.strftime("%Y-%m-%d %H:%M:%S %Z"),
        span_hours,
    )


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def analyze(daily_text: str, feed: list[FeedMessage], tz: ZoneInfo) -> list[Issue]:
    issues: list[Issue] = []
    paragraphs = split_paragraphs(daily_text)

    for idx, paragraph in enumerate(paragraphs):
        claimed = extract_time_word(paragraph)
        if not claimed:
            continue

        matched, best_score = match_messages(paragraph, feed)
        if len(matched) < 2:
            continue

        actual, start_ts, end_ts, span_hours = pick_actual_bucket(matched, tz)
        if claimed == actual:
            continue

        # Confidence gating:
        # - high: clear anchor hits and tight time window
        # - medium: weaker but still narrow
        # - low: likely over-match, report only
        if best_score >= 4 and span_hours <= 4:
            confidence = "high"
        elif best_score >= 3 and span_hours <= 2:
            confidence = "medium"
        else:
            confidence = "low"

        if claimed != actual:
            issues.append(
                Issue(
                    paragraph_index=idx,
                    claimed=claimed,
                    actual=actual,
                    evidence_count=len(matched),
                    evidence_start=start_ts,
                    evidence_end=end_ts,
                    span_hours=span_hours,
                    confidence=confidence,
                    paragraph=paragraph,
                )
            )

    return issues


def apply_fixes(daily_text: str, issues: list[Issue]) -> tuple[str, int]:
    paragraphs = split_paragraphs(daily_text)
    changed = 0

    actionable = [item for item in issues if item.confidence in {"high", "medium"}]
    by_index = {item.paragraph_index: item for item in actionable}
    for idx, p in enumerate(paragraphs):
        item = by_index.get(idx)
        if not item:
            continue
        replaced = p.replace(item.claimed, item.actual, 1)
        if replaced != p:
            paragraphs[idx] = replaced
            changed += 1

    return "\n\n".join(paragraphs) + "\n", changed


def render_report(date_str: str, tz_name: str, issues: list[Issue], applied: bool, changed: int) -> str:
    lines = [
        f"# Daily Memory Time QA - {date_str}",
        "",
        f"- timezone: {tz_name}",
        f"- issues: {len(issues)}",
        f"- applied: {str(applied).lower()}",
        f"- changed_paragraphs: {changed}",
        "",
        "## Findings",
    ]

    if not issues:
        lines.append("- none")
    else:
        for i, item in enumerate(issues, start=1):
            lines.extend(
                [
                    f"### {i}. {item.claimed} -> {item.actual}",
                    f"- evidence_messages: {item.evidence_count}",
                    f"- evidence_window: {item.evidence_start} ~ {item.evidence_end}",
                    f"- span_hours: {item.span_hours}",
                    f"- confidence: {item.confidence}",
                    f"- paragraph: {item.paragraph}",
                    "",
                ]
            )

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace)

    daily_path = workspace / "memory" / f"{args.date}.md"
    feed_path = workspace / "memory" / "shared" / f"{args.date}-discord-feed.md"
    report_path = workspace / "memory" / "shared" / f"{args.date}-memory-quality.md"

    if not daily_path.exists():
        print(f"daily memory not found: {daily_path}")
        return 0

    if not feed_path.exists():
        print(f"discord feed not found: {feed_path}")
        return 0

    daily_text = daily_path.read_text(encoding="utf-8", errors="ignore")
    feed_text = feed_path.read_text(encoding="utf-8", errors="ignore")
    feed = parse_feed(feed_text)

    tz = ZoneInfo(args.tz)
    issues = analyze(daily_text, feed, tz)

    changed = 0
    if args.apply and issues:
        next_text, changed = apply_fixes(daily_text, issues)
        daily_path.write_text(next_text, encoding="utf-8")

    report = render_report(args.date, args.tz, issues, args.apply, changed)
    report_path.write_text(report, encoding="utf-8")

    if args.verbose:
        print(report.strip())
    else:
        print(
            {
                "date": args.date,
                "issues": len(issues),
                "applied": args.apply,
                "changed": changed,
                "report": str(report_path),
            }
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
