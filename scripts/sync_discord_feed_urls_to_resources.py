#!/usr/bin/env python3
# [INPUT]: 依赖 memory/shared/YYYY-MM-DD-discord-feed.md 的结构化消息文本。
# [OUTPUT]: 生成 Resources/*.md 资源笔记，并更新 memory/shared/.resource_url_sync_state.json。
# [POS]: scripts 同步链路中的 URL->Resources 落盘器，补齐 feed 与知识库之间的最后一跳。
# [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
"""Sync URLs from shared discord feed files into Obsidian Resources notes.

- Source: memory/shared/YYYY-MM-DD-discord-feed.md
- Target: obsidian/Resources/<descriptive-title>.md
- State:  memory/shared/.resource_url_sync_state.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta
from html import unescape
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
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
RESOURCE_CHANNEL_KEYWORDS = ("资源",)
REQUEST_TIMEOUT_SEC = 12
READER_TIMEOUT_SEC = 20
MAX_BODY_BYTES = 500_000
MAX_TEXT_CHARS = 12_000
MAX_QUOTES = 3
MAX_POINTS = 10
MIN_POINTS = 8
MIN_QUOTES = 3

API_KEY_RE = re.compile(r"X-API-Key:\s*([A-Za-z0-9._-]+)", re.IGNORECASE)
TOKEN_RE = re.compile(r"\bagc_[A-Za-z0-9._-]+\b")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？.!?])\s+")
STEP_RE = re.compile(r"(?:^|\s)(\d+)[\.\)]\s*(.*?)(?=(?:\s\d+[\.\)]\s)|$)")
FRONTMATTER_RE = re.compile(r"(?ms)^---\n(.*?)\n---\n")
GENERIC_TITLE_PHRASES = {
    "再看看这个",
    "看这个",
    "链接",
    "link",
    "resource",
    "x 资源",
    "该条资源当前无法稳定抓取正文，已保留来源链接并等待下次自动补抓。",
    "建议先把这条资源归档到对应项目，再补正文事实。",
    "sign up now to get your own personalized timeline!",
    "you can see a list of supported browsers in our help center",
    "redirecting you to the video in a moment",
    "there was an error while loading",
    "please reload this page",
    "当前仅抓取到标题级内容，推文 文章正文受站点限制，后续重试补全文。",
    "activity custom properties stars 0 stars watchers 0 watching for",
    "tryroro code",
    "roro get roro free rock and roro the new way to make is here",
    "add multiple projects add a project to get started!",
    "help center terms of service privacy policy cookie policy imprint ads info 2026 x corp",
    "include my email address so i can be contacted cancel submit fee",
    "please contact your service provider for more details",
    "当前自动抓取正文失败或内容质量不足，暂未形成可靠摘要。",
    "已保留来源链接，后续会重试抓取并补齐关键结论。",
    "该链接为 x 资源，当前自动抓取正文受限，暂未拿到稳定全文。",
    "已保留原始来源链接与可访问镜像，等待后续补抓或手工补录事实要点。",
}
X_UI_NOISE_TOKENS = (
    "sign up now to get your own personalized timeline",
    "sign up with google",
    "terms of service",
    "privacy policy",
    "cookie policy",
    "imprint ads info",
    "you signed out in another tab or window",
    "you switched accounts on another tab or window",
    "please disable them and try again",
    "something went wrong, but don’t fret",
    "help center",
    "redirecting you to the video in a moment",
    "there was an error while loading",
)
LOW_SIGNAL_SUMMARY_PHRASES = (
    "is so much fun",
    "sign up now",
    "sign up with google",
    "please reload this page",
    "you signed out in another tab",
    "you switched accounts on another tab",
    "help center terms of service privacy policy",
    "try again some privacy related extensions may cause issues on x",
    "try reloading",
)
UNREADABLE_SUMMARY_MARKERS = (
    "正文抓取受限，本摘要基于频道上下文",
    "当前自动抓取正文失败或内容质量不足",
    "当前仅抓取到标题级内容",
    "当前自动抓取正文受限，暂未拿到稳定全文",
    "等待后续补抓或手工补录事实要点",
    "后续会重试抓取并补齐关键结论",
    "当前源站不可达",
)


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


@dataclass
class FetchSnapshot:
    ok: bool
    status: Optional[int]
    content_type: str
    final_url: str
    title: str
    body_text: str
    error: str


@dataclass
class HostContext:
    host: str
    mentions: int
    snippets: List[str]


@dataclass
class NoteMeta:
    title: str
    url: str
    context: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync discord feed URLs to Resources")
    parser.add_argument("--workspace", default=os.path.expanduser("~/.openclaw/workspace"))
    parser.add_argument(
        "--vault",
        default="obsidian",
        help="Vault directory under workspace (default: obsidian)",
    )
    parser.add_argument("--days", type=int, default=2, help="Look back N days including today")
    parser.add_argument("--since", default="", help="Start date YYYY-MM-DD (overrides --days)")
    parser.add_argument(
        "--enrich-all-notes",
        action="store_true",
        help="Enrich all existing Resources/*.md that still lack Auto Summary",
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Force regenerate Auto Summary for all matched notes",
    )
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
    url = raw.strip().rstrip(",.;>)]}）】》」\"'")
    return url


def is_resource_channel(name: str) -> bool:
    n = (name or "").strip()
    return any(k in n for k in RESOURCE_CHANNEL_KEYWORDS)


def canonical_host(url: str) -> str:
    try:
        p = urlparse(url)
    except Exception:
        return ""
    host = (p.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if host in {"tryroro", "www.tryroro"}:
        host = "tryroro.com"
    return host


def is_resource_url(url: str) -> bool:
    try:
        p = urlparse(url)
    except Exception:
        return False

    if p.scheme.lower() in SKIP_SCHEMES:
        return False
    host = canonical_host(url)
    if host in SKIP_HOSTS:
        return False
    # Drop short links that usually cannot produce stable article-level summaries.
    if host == "t.co":
        return False
    # Drop ephemeral tunnel links from long-term knowledge base.
    if host.endswith("trycloudflare.com"):
        return False
    if not host:
        return False
    return True


def url_fingerprint(url: str) -> str:
    p = urlparse(url)
    host = canonical_host(url)
    path = p.path or ""
    if host in {"x.com", "twitter.com"}:
        parts = [x for x in path.split("/") if x]
        if len(parts) >= 3 and parts[1] == "status":
            path = f"/{parts[0]}/status/{parts[2]}"
            p = p._replace(path=path, query="", fragment="")
        if len(parts) >= 3 and parts[0] == "i" and parts[1] == "article":
            path = f"/i/article/{parts[2]}"
            p = p._replace(path=path, query="", fragment="")
    canon = p._replace(fragment="").geturl()
    return hashlib.sha1(canon.encode("utf-8")).hexdigest()


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


def sanitize_title(raw: str, fallback: str) -> str:
    t = raw or ""
    t = re.sub(r"[\U00010000-\U0010ffff]", "", t)
    t = re.sub(r"\*\*|`|#+", "", t)
    t = URL_RE.sub("", t)
    t = t.replace("（", "(").replace("）", ")")
    t = t.replace("/", " ")
    t = re.sub(r"[^\w\u4e00-\u9fff\s\-\+\&:：,，。.()（）]", "", t)
    t = WS_RE.sub(" ", t).strip(" -:;,.()[]{}")
    if len(t) > 64:
        t = t[:64].rstrip(" -:;,.()[]{}")
    if len(t) < 3:
        t = fallback
    return t


def sanitize_segment(raw: str) -> str:
    s = raw or ""
    s = unescape(s)
    s = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-._")
    return s


def title_to_stem(title: str, fallback: str) -> str:
    stem = title.strip()
    stem = stem.replace("/", "／").replace(":", "：")
    stem = re.sub(r"[\\*?\"<>|]", "", stem)
    stem = re.sub(r"\s+", " ", stem).strip(" .")
    if len(stem) > 72:
        stem = stem[:72].rstrip(" .")
    if stem:
        return stem
    fb = re.sub(r"[-_]+", " ", (fallback or "")).strip()
    return fb or "resource"


def derive_resource_title(hit: ResourceHit) -> str:
    host = canonical_host(hit.url)
    p = urlparse(hit.url)
    path = (p.path or "").strip("/")
    parts = [x for x in path.split("/") if x]
    fallback = slug_from_url(hit.url).replace("-", " ")
    host_name = sanitize_segment(host.replace(".", "-")) if host else "resource"

    if host in {"x.com", "twitter.com"}:
        msg_hint = derive_title_hint_from_message(hit.message.text or "")
        if len(parts) >= 3 and parts[0] == "i" and parts[1] == "article":
            if msg_hint:
                return sanitize_title(msg_hint, fallback)
            return sanitize_title("X 文章洞察", fallback)
        if len(parts) >= 3 and parts[1] == "status":
            if msg_hint:
                return sanitize_title(msg_hint, fallback)
            return sanitize_title("X 推文洞察", fallback)
        if "流程" in (hit.message.text or ""):
            return sanitize_title("X 内容抓取流程", fallback)
        return sanitize_title("X 资源", fallback)
    if host == "t.co":
        code = parts[0] if parts else "shortlink"
        return sanitize_title(f"X 短链 {code}", fallback)
    if host.endswith("trycloudflare.com"):
        sub = host.split(".")[0]
        return sanitize_title(f"Cloudflare Tunnel 链接 {sub}", fallback)
    if host == "www.notion.so" or host == "notion.so":
        if "introducing-notion-ai-search" in path:
            return sanitize_title("Notion AI Search 官方发布", fallback)
        if "blog" in path:
            return sanitize_title("Notion 官方博客", fallback)
    if host in {"www.tryroro.com", "tryroro.com", "www.tryroro", "tryroro"}:
        if "code" in path:
            return sanitize_title("Roro Code 产品页", fallback)
    if host == "www.elvissun.com" or host == "elvissun.com":
        if "openclaw-codex-agent-swarm" in path:
            return sanitize_title("OpenClaw + Codex Agent Swarm 博客实战", fallback)

    if host == "github.com" and len(parts) >= 2:
        return sanitize_title(f"GitHub {parts[0]}/{parts[1]}", fallback)

    if "/api/" in ("/" + path).lower():
        tail = sanitize_segment(parts[-1] if parts else "endpoint")
        return sanitize_title(f"{host_name} API {tail}", fallback)

    if host:
        if len(parts) >= 2:
            tail = f"{sanitize_segment(parts[-2])} {sanitize_segment(parts[-1])}".strip()
            return sanitize_title(f"{host_name} {tail}", fallback)
        if len(parts) == 1:
            return sanitize_title(f"{host_name} {sanitize_segment(parts[0])}", fallback)
        return sanitize_title(f"{host_name} link", fallback)

    return sanitize_title(fallback, "resource")


def derive_title_hint_from_message(text: str) -> str:
    clean = normalize_text(strip_urls(text or ""), 280)
    clean = re.sub(r"<@!?\d+>", "", clean)
    clean = re.sub(r"[`*_#>\-]{1,3}", " ", clean)
    clean = WS_RE.sub(" ", clean).strip()
    if not clean:
        return ""
    for sent in split_sentences(clean):
        s = polish_sentence(sent)
        if len(s) < 8:
            continue
        if is_weak_context_sentence(s) or is_noisy_sentence(s):
            continue
        low = s.lower()
        if low in {"ok", "yes", "done", "try this"}:
            continue
        return s
    return ""


def is_generic_title(title: str) -> bool:
    t = (title or "").strip().lower()
    if not t:
        return True
    bad = {
        "x",
        "twitter",
        "linkedin",
        "github",
        "not found",
        "access denied",
        "log in",
    }
    if t in bad:
        return True
    if len(t) < 4:
        return True
    if t in GENERIC_TITLE_PHRASES:
        return True
    generic_fragments = [
        "当前自动抓取正文失败",
        "暂未形成可靠摘要",
        "该链接为 x 资源",
        "当前自动抓取正文受限",
        "暂未拿到稳定全文",
        "已保留来源链接",
        "已保留原始来源链接",
        "后续会重试抓取并补齐关键结论",
        "等待后续补抓或手工补录事实要点",
    ]
    if any(f in t for f in generic_fragments):
        return True
    noisy_fragments = [
        "help center terms of service privacy policy",
        "cancel create saved search sign in sign up appearance settings",
        "sign up now to get your own personalized timeline",
        "please contact your service provider for more details",
        "reload to refresh your session",
        "something went wrong, but don’t fret",
        "you signed out in another tab or window",
        "you switched accounts on another tab or window",
        "please disable them and try again",
        "search clear search syntax tips provide feedback",
        "please reload this page",
        "当前仅抓取到标题级内容",
        "activity custom properties stars",
        "notion-so blog",
        "elvissun-com blog",
        "trycloudflare-com link",
        "tryroro code",
        "roro get roro free rock and roro the new way to make is here",
        "add multiple projects add a project to get started",
        "the host (",
        "is configured as a cloudflare tunnel",
    ]
    if any(frag in t for frag in noisy_fragments):
        return True
    if "search clear search syntax tips" in t:
        return True
    if "page cannot be displayed" == t:
        return True
    if t.startswith("title:") or t.startswith("url source:") or t.startswith("markdown content:"):
        return True
    if "{" in t or "}" in t:
        return True
    return False


def derive_title_from_auto_summary(auto_md: str, hit: ResourceHit) -> str:
    host = canonical_host(hit.url)
    if host.endswith("trycloudflare.com"):
        return derive_resource_title(hit)
    x_ui_noise = [
        "sign up now to get your own personalized timeline",
        "you signed out in another tab or window",
        "try again some privacy related extensions may cause issues on x",
        "help center terms of service privacy policy cookie policy",
        "something went wrong",
        "reload to refresh your session",
    ]
    m = re.search(r"(?ms)^### Content Summary\n(.*?)(?=^### |\Z)", auto_md)
    if m:
        for ln in m.group(1).splitlines():
            ln = ln.strip()
            if not ln.startswith("- "):
                continue
            candidate = ln[2:].strip()
            candidate = re.sub(r"^\s*[^:]{1,80}\bon x:\s*", "", candidate, flags=re.IGNORECASE)
            candidate = re.sub(r"\s*/\s*x url source:.*$", "", candidate, flags=re.IGNORECASE)
            candidate = re.sub(r"\s*x url source:.*$", "", candidate, flags=re.IGNORECASE)
            candidate = candidate.strip().strip("\"'“”")
            candidate = sanitize_title(candidate, "")
            if host in {"x.com", "twitter.com", "t.co"}:
                cl = candidate.lower()
                if any(p in cl for p in x_ui_noise):
                    continue
            if candidate and not is_generic_title(candidate):
                return candidate
    return derive_resource_title(hit)


def pick_meaningful_title(hit: ResourceHit, auto_summary_md: str = "", current_note_body: str = "") -> str:
    candidates: List[str] = []

    if auto_summary_md:
        candidates.append(derive_title_from_auto_summary(auto_summary_md, hit))

    if current_note_body:
        fm_title = extract_frontmatter_title(current_note_body)
        if fm_title:
            candidates.append(fm_title)
        h1_title = extract_h1_title(current_note_body)
        if h1_title:
            candidates.append(h1_title)
        src_title = extract_frontmatter_field(current_note_body, "source_title")
        if src_title:
            candidates.append(src_title)

    candidates.append(derive_resource_title(hit))

    for c in candidates:
        s = sanitize_title(c, "")
        if s and not is_generic_title(s):
            chosen = s
            break
    else:
        chosen = derive_resource_title(hit)

    p = urlparse(hit.url)
    path = (p.path or "").lower()
    if chosen.lower().startswith("502 bad gateway"):
        if path.startswith("/api/projects"):
            return "Cloudflare Tunnel API projects（502）"
        if path in {"", "/"}:
            return "Cloudflare Tunnel 根地址（502）"
    return chosen


def upsert_note_title(note_body: str, title: str) -> str:
    body = note_body
    m = FRONTMATTER_RE.search(body)
    if m:
        fm = m.group(1)
        if re.search(r"(?m)^title:\s*", fm):
            fm_new = re.sub(r"(?m)^title:\s*.*$", f"title: {title}", fm)
        else:
            fm_new = f"title: {title}\n{fm}"
        body = body[: m.start(1)] + fm_new + body[m.end(1) :]
    else:
        body = f"---\ntitle: {title}\n---\n\n{body.lstrip()}"

    if re.search(r"(?m)^#\s+", body):
        body = re.sub(r"(?m)^#\s+.*$", f"# {title}", body, count=1)
    else:
        body = body.rstrip() + f"\n\n# {title}\n"
    return body


def upsert_source_title(note_body: str, title: str) -> str:
    body = note_body
    m = FRONTMATTER_RE.search(body)
    if not m:
        return body
    fm = m.group(1)
    if re.search(r"(?m)^source_title:\s*", fm):
        fm_new = re.sub(r"(?m)^source_title:\s*.*$", f"source_title: \"{title}\"", fm)
    else:
        fm_new = fm + f"\nsource_title: \"{title}\""
    return body[: m.start(1)] + fm_new + body[m.end(1) :]


def extract_frontmatter_title(note_body: str) -> str:
    m = FRONTMATTER_RE.search(note_body)
    if not m:
        return ""
    fm = m.group(1)
    mt = re.search(r"(?m)^title:\s*(.+)$", fm)
    if not mt:
        return ""
    return mt.group(1).strip().strip("\"'")


def extract_h1_title(note_body: str) -> str:
    m = re.search(r"(?m)^#\s+(.+)$", note_body)
    return m.group(1).strip() if m else ""


def extract_note_meta(note_path: Path, note_body: str) -> NoteMeta:
    title = extract_frontmatter_title(note_body) or extract_h1_title(note_body) or note_path.stem

    url = ""
    m_url = re.search(r'^original_url:\s*"([^"]*)"', note_body, flags=re.MULTILINE)
    if m_url:
        url = m_url.group(1).strip()
    if not url:
        m_url2 = re.search(r"^- URL:\s*(\S+)", note_body, flags=re.MULTILINE)
        if m_url2:
            url = m_url2.group(1).strip()

    context = ""
    m_ctx = re.search(r"(?ms)^## Captured Context\n(.*?)(?=^## |\Z)", note_body)
    if m_ctx:
        raw_ctx = m_ctx.group(1).strip()
        parts: List[str] = []
        for ln in raw_ctx.splitlines():
            ln = ln.strip()
            ln = ln[1:].strip() if ln.startswith(">") else ln
            if ln:
                parts.append(ln)
        context = " ".join(parts).strip()

    if not context:
        m_summary = re.search(r"(?ms)^## 3-line Summary\n(.*?)(?=^## |\Z)", note_body)
        if m_summary:
            context = normalize_text(m_summary.group(1), 600)

    return NoteMeta(title=title, url=url, context=context)


def classify_resource(meta: NoteMeta) -> Tuple[str, str]:
    host = canonical_host(meta.url) if meta.url else ""
    path = urlparse(meta.url).path.lower() if meta.url else ""
    bag = f"{meta.title} {meta.context} {meta.url}".lower()

    if host in {"x.com", "twitter.com", "t.co"}:
        return ("Social", "X/Twitter")
    if host == "github.com":
        return ("Code", "GitHub")
    if "/api/" in path or "api." in host or "trycloudflare" in host or "endpoint" in bag:
        return ("API", "Endpoint")
    if "obsidian" in bag or "教程" in bag or "guide" in bag or "forum" in bag:
        return ("Learning", "Tutorial")
    if "notion" in bag or "docs" in bag or "platform" in bag or "blog" in bag:
        return ("Docs", "Product/Docs")
    if "agent" in bag or "openclaw" in bag or "workflow" in bag:
        return ("Ops", "Agent/Workflow")
    return ("General", "Misc")


def upsert_classification(note_body: str, category: str, subtype: str) -> str:
    block = (
        "## Classification\n"
        f"- Category: {category}\n"
        f"- Subtype: {subtype}\n\n"
    )
    if "## Classification" in note_body:
        return re.sub(
            r"(?ms)^## Classification\n.*?(?=^## |\Z)",
            lambda _m: block.rstrip() + "\n",
            note_body,
        )

    if "## Auto Summary" in note_body:
        return note_body.replace("## Auto Summary", block + "## Auto Summary", 1)
    if "## Captured Context" in note_body:
        return note_body + "\n" + block
    return note_body.rstrip() + "\n\n" + block


def generate_category_index(resources_dir: Path) -> None:
    groups: Dict[Tuple[str, str], List[str]] = {}
    for note in sorted(resources_dir.glob("*.md")):
        if note.name in {"_TEMPLATE.md", "_资源分类索引.md"}:
            continue
        body = note.read_text(encoding="utf-8", errors="ignore")
        meta = extract_note_meta(note, body)
        category, subtype = classify_resource(meta)
        groups.setdefault((category, subtype), []).append(note.stem)

    lines: List[str] = []
    lines.append("# 资源分类索引")
    lines.append("")
    lines.append(f"> Auto generated at {datetime.now().astimezone().isoformat()}")
    lines.append("")
    total = sum(len(v) for v in groups.values())
    lines.append(f"- Total resources: {total}")
    lines.append("")
    for key in sorted(groups.keys()):
        category, subtype = key
        items = sorted(groups[key])
        lines.append(f"## {category} / {subtype} ({len(items)})")
        for stem in items:
            lines.append(f"- [[{stem}]]")
        lines.append("")

    (resources_dir / "_资源分类索引.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def first_nonempty(items: Iterable[str]) -> str:
    for it in items:
        if it:
            return it
    return ""


def extract_auto_summary_block(note_body: str) -> str:
    m = re.search(r"(?ms)^## Auto Summary\n(.*?)(?=^## |\Z)", note_body)
    if not m:
        return ""
    block = m.group(1).strip()
    if not block:
        return ""
    return "## Auto Summary\n" + block + "\n"


def extract_frontmatter_field(note_body: str, key: str) -> str:
    m = FRONTMATTER_RE.search(note_body)
    if not m:
        return ""
    fm = m.group(1)
    mk = re.search(rf'(?m)^{re.escape(key)}:\s*"([^"]*)"', fm)
    if mk:
        return mk.group(1).strip()
    mk2 = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", fm)
    if mk2:
        return mk2.group(1).strip().strip("\"'")
    return ""


def strip_urls(text: str) -> str:
    return URL_RE.sub("", text or "").strip()


def split_sentences(text: str) -> List[str]:
    raw = re.split(r"(?<=[。！？.!?])\s+|\n+", text or "")
    out: List[str] = []
    for item in raw:
        s = normalize_text(item, 260)
        if s:
            out.append(s)
    return out


def polish_sentence(sentence: str) -> str:
    s = normalize_text(sentence, 240)
    s = re.sub(r"[\U00010000-\U0010ffff]", "", s)
    s = re.sub(r"[（(]\s*$", "", s).strip()
    s = re.sub(r"[）)]\s*$", "", s).strip()
    s = s.replace("（", "").replace("）", "")
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r"^title:\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^url source:\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^markdown content:\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^\s*[^:]{1,100}\bon x:\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*/\s*x url source:.*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*x url source:.*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*published time:.*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*warning:.*$", "", s, flags=re.IGNORECASE)
    s = s.strip().strip("\"'“”")
    s = s.strip(" -:;，,。")
    return s


def is_noisy_sentence(sentence: str) -> bool:
    s = (sentence or "").strip()
    if len(s) < 10:
        return True
    low = s.lower()
    noisy_tokens = [
        "html,body",
        "stylesheet-group",
        "::cue",
        "-webkit-",
        "-ms-text-size-adjust",
        "font-family",
        "margin:0",
        "<!doctype",
        "<html",
        "window.navigator.useragent",
        "meta name=",
        "property=\"og:",
        "\"props\":",
        "search code, repositories",
        "skip to content",
        "function(",
        "javascript",
        "captured from:",
        "message id:",
        "source:",
        "discord",
        "sender:",
        "channel:",
        "search clear search syntax tips",
        "saved searches",
        "appearance settings",
        "reload to refresh your session",
        "sign in sign up",
        "watchers",
        "forks",
        "releases no releases published",
        "packages 0 no packages published",
        "contributors",
        "uh oh",
    ]
    if any(tok in low for tok in noisy_tokens):
        return True
    if any(tok in low for tok in X_UI_NOISE_TOKENS):
        return True
    if low.count("http://") + low.count("https://") >= 2:
        return True
    symbol_count = sum(1 for ch in s if ch in "{};<>:=[]")
    if symbol_count >= max(6, int(len(s) * 0.08)):
        return True
    if len(s) > 260:
        return True
    if re.search(r"[{}<>]{2,}", s):
        return True
    if re.search(r"<[^>]+>", s):
        return True
    if "&lt;" in low or "&gt;" in low:
        return True
    if low.startswith("url: ") or low.startswith("http://") or low.startswith("https://"):
        return True
    return False


def is_low_signal_summary_point(sentence: str) -> bool:
    s = (sentence or "").strip()
    if not s:
        return True
    low = s.lower()
    if re.fullmatch(r"https?://\S+", s):
        return True
    if s.startswith("http://") or s.startswith("https://"):
        return True
    if any(p in low for p in LOW_SIGNAL_SUMMARY_PHRASES):
        return True
    if len(s) < 28 and (" fun" in low or " nice" in low or " cool" in low):
        return True
    weak_prefixes = (
        "url:",
        "source:",
        "message id:",
        "captured from:",
        "published time:",
        "warning:",
    )
    if any(low.startswith(p) for p in weak_prefixes):
        return True
    noise_fragments = (
        "saved searches",
        "search syntax tips",
        "appearance settings",
        "reload to refresh your session",
        "sign in sign up",
        "watchers",
        "forks",
        "releases no releases published",
        "packages 0 no packages published",
        "contributors",
        "uh oh",
    )
    if any(f in low for f in noise_fragments):
        return True
    return False


def is_weak_context_sentence(sentence: str) -> bool:
    s = (sentence or "").strip().lower()
    if not s:
        return True
    if s in GENERIC_TITLE_PHRASES:
        return True
    weak_prefixes = (
        "再看看",
        "看这个",
        "可以读吗",
        "试试",
        "标题：",
        "title:",
        "url source:",
        "markdown content:",
    )
    return any(s.startswith(p) for p in weak_prefixes)


def extract_summary_from_context(context: str, limit: int = 6) -> List[str]:
    out: List[str] = []
    ctx = normalize_text(strip_urls(context), 1200)
    if not ctx:
        return out
    steps = STEP_RE.findall(ctx)
    if steps:
        for _, step in steps:
            step_clean = polish_sentence(step)
            if step_clean and not is_noisy_sentence(step_clean) and not is_weak_context_sentence(step_clean):
                out.append(step_clean)
            if len(out) >= limit:
                break
        return out
    for sent in split_sentences(ctx):
        sent = polish_sentence(sent)
        if is_noisy_sentence(sent) or is_weak_context_sentence(sent):
            continue
        out.append(sent)
        if len(out) >= limit:
            break
    return out


def extract_summary_from_body(text: str, limit: int = 6) -> List[str]:
    out: List[str] = []
    for sent in split_sentences(text):
        sent = polish_sentence(sent)
        if is_noisy_sentence(sent):
            continue
        out.append(sent)
        if len(out) >= limit:
            break
    return out


def extract_links(*texts: str) -> List[str]:
    out: List[str] = []
    for txt in texts:
        for u in URL_RE.findall(txt or ""):
            n = normalize_url(u)
            if not n:
                continue
            if n not in out:
                out.append(n)
    return out


def is_useless_related_link(url: str) -> bool:
    try:
        p = urlparse(url)
    except Exception:
        return True

    host = canonical_host(url)
    path = (p.path or "").rstrip("/")
    low = url.lower()
    if not host:
        return True

    if host in {"x.com", "twitter.com"}:
        if path in {"", "/", "/home", "/explore", "/i", "/login"}:
            return True
        if path.startswith("/i/flow/"):
            return True
        parts = [x for x in path.split("/") if x]
        # For X links, only keep status/article URLs.
        if not ((len(parts) >= 3 and parts[1] == "status") or (len(parts) >= 3 and parts[0] == "i" and parts[1] == "article")):
            return True
    if host in {"t.co", "pbs.twimg.com", "abs.twimg.com", "abs-0.twimg.com"}:
        return True
    if "x.com/login" in low or "x.com/i/flow/signup" in low:
        return True
    return False


def canonicalize_resource_url(url: str) -> str:
    try:
        p = urlparse(url)
    except Exception:
        return url

    host = canonical_host(url)
    if host in {"x.com", "twitter.com"}:
        parts = [x for x in (p.path or "").split("/") if x]
        if len(parts) >= 3 and parts[1] == "status":
            path = f"/{parts[0]}/status/{parts[2]}"
            return p._replace(path=path, query="", fragment="").geturl()
        if len(parts) >= 3 and parts[0] == "i" and parts[1] == "article":
            path = f"/i/article/{parts[2]}"
            return p._replace(path=path, query="", fragment="").geturl()
    return p._replace(fragment="").geturl()


def clean_resource_links(urls: List[str], primary: str, max_items: int = 5) -> List[str]:
    out: List[str] = []
    seen: set[str] = set()
    primary_canon = canonicalize_resource_url(primary)

    for cand in [primary] + urls:
        n = normalize_url(cand)
        if not n:
            continue
        if not is_resource_url(n):
            continue
        c = canonicalize_resource_url(n)
        if c != primary_canon and is_useless_related_link(c):
            continue
        if c in seen:
            continue
        seen.add(c)
        out.append(c)
        if len(out) >= max_items:
            break

    return out


def derive_url_clues(url: str) -> List[str]:
    clues: List[str] = []
    try:
        p = urlparse(url)
    except Exception:
        return clues
    host = canonical_host(url)
    path = (p.path or "/").strip()
    query = (p.query or "").strip()

    if host:
        clues.append(f"Resource host: `{host}`")
    if path and path != "/":
        clues.append(f"Resource path: `{path}`")
    if query:
        clues.append("URL contains query params, likely context-sensitive content.")

    path_l = path.lower()
    if "/api/" in path_l or path_l.endswith("/api") or "api" in host:
        clues.append("This is API-oriented material; keep endpoint, auth header, and response schema together.")
    if "github.com" in host:
        clues.append("This appears to be a GitHub artifact; prioritize repo purpose, setup steps, and task ownership.")
    if "x.com" in host or "twitter.com" in host:
        clues.append("This appears to be a social post; prioritize claim extraction and source validation.")
    if "notion" in host:
        clues.append("This appears to be product/docs content; capture definitions, limitations, and migration impact.")
    return clues


def append_unique(items: List[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def ensure_min_points(points: List[str], url: str, host_ctx: Optional[HostContext]) -> List[str]:
    out: List[str] = []
    for p in points:
        append_unique(out, p)
    for clue in derive_url_clues(url):
        if len(out) >= MAX_POINTS:
            break
        append_unique(out, clue)
    if host_ctx:
        append_unique(out, f"Discord mentions for `{host_ctx.host}`: {host_ctx.mentions}")
        for s in host_ctx.snippets[:6]:
            if len(out) >= MAX_POINTS:
                break
            append_unique(out, f"Context signal: {normalize_text(s, 180)}")
    fillers = [
        "Source capture was generated from conversation evidence, suitable for triage but should be validated before execution.",
        "Keep this note linked to one concrete project so follow-up actions are trackable.",
        "If content quality is low, re-capture the source later and re-run this pipeline for stronger extraction.",
        "Preserve direct source text and derived conclusions separately to avoid mixing fact and interpretation.",
    ]
    for f in fillers:
        if len(out) >= MIN_POINTS:
            break
        append_unique(out, f)
    return out[:MAX_POINTS]


def ensure_min_quotes(quotes: List[str], hit: ResourceHit, host_ctx: Optional[HostContext]) -> List[str]:
    out: List[str] = []
    for q in quotes:
        append_unique(out, q)
    if hit.message.text:
        append_unique(out, normalize_text(strip_urls(hit.message.text), 180))
        append_unique(out, normalize_text(hit.message.text, 180))
    if host_ctx:
        for s in host_ctx.snippets:
            if len(out) >= MIN_QUOTES:
                break
            append_unique(out, normalize_text(s, 180))
    append_unique(out, f"URL: {hit.url}")
    return [redact_secrets(q) for q in out if q][:MAX_QUOTES]


def build_host_contexts(messages: List[FeedMessage]) -> Dict[str, HostContext]:
    acc: Dict[str, HostContext] = {}
    for msg in messages:
        urls = [normalize_url(u) for u in URL_RE.findall(msg.text or "")]
        clean_text = normalize_text(strip_urls(msg.text or ""), 240)
        for u in urls:
            if not is_resource_url(u):
                continue
            host = canonical_host(u)
            if not host:
                continue
            if host not in acc:
                acc[host] = HostContext(host=host, mentions=0, snippets=[])
            ctx = acc[host]
            ctx.mentions += 1
            if clean_text and clean_text not in ctx.snippets:
                ctx.snippets.append(clean_text)
                if len(ctx.snippets) > 12:
                    ctx.snippets = ctx.snippets[:12]
    return acc


def redact_secrets(text: str) -> str:
    text = TOKEN_RE.sub("agc_***REDACTED***", text)
    return text


def extract_api_key(text: str) -> str:
    if not text:
        return ""
    m = API_KEY_RE.search(text)
    if not m:
        return ""
    return m.group(1).strip()


def normalize_text(value: str, max_chars: int = MAX_TEXT_CHARS) -> str:
    value = WS_RE.sub(" ", value).strip()
    if len(value) > max_chars:
        return value[:max_chars].rstrip() + "..."
    return value


def html_to_text(html: str) -> Tuple[str, str]:
    title_match = TITLE_RE.search(html)
    title = normalize_text(unescape(title_match.group(1))) if title_match else ""
    no_script = SCRIPT_STYLE_RE.sub(" ", html)
    plain = TAG_RE.sub(" ", no_script)
    plain = normalize_text(unescape(plain))
    return title, plain


def fetch_snapshot(url: str, api_key: str) -> FetchSnapshot:
    headers = {
        "User-Agent": "OpenClaw-ResourceSync/1.1 (+https://docs.openclaw.ai)",
        "Accept": "application/json,text/html,application/xhtml+xml,text/plain,*/*",
    }
    if api_key:
        headers["X-API-Key"] = api_key
    req = urllib.request.Request(url=url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SEC) as resp:
            status = getattr(resp, "status", None)
            content_type = resp.headers.get("Content-Type", "")
            final_url = getattr(resp, "geturl", lambda: url)() or url
            body_bytes = resp.read(MAX_BODY_BYTES)
    except urllib.error.HTTPError as exc:
        body_bytes = b""
        try:
            body_bytes = exc.read(MAX_BODY_BYTES)
        except Exception:
            pass
        content_type = exc.headers.get("Content-Type", "") if exc.headers else ""
        return FetchSnapshot(
            ok=False,
            status=exc.code,
            content_type=content_type,
            final_url=url,
            title="",
            body_text=normalize_text(body_bytes.decode("utf-8", errors="ignore")),
            error=f"HTTP {exc.code}",
        )
    except Exception as exc:
        return FetchSnapshot(
            ok=False,
            status=None,
            content_type="",
            final_url=url,
            title="",
            body_text="",
            error=str(exc),
        )

    body = body_bytes.decode("utf-8", errors="ignore")
    title = ""
    body_text = body
    if "html" in content_type.lower() or "<html" in body.lower():
        title, body_text = html_to_text(body)
    else:
        body_text = normalize_text(body)

    return FetchSnapshot(
        ok=True,
        status=status,
        content_type=content_type,
        final_url=final_url,
        title=title,
        body_text=body_text,
        error="",
    )


def fetch_reader_snapshot(url: str) -> FetchSnapshot:
    # Reader fallback for sites that block direct crawlers.
    reader_url = f"https://r.jina.ai/http://{url.replace('https://', '').replace('http://', '')}"
    req = urllib.request.Request(
        url=reader_url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "text/plain,*/*"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=READER_TIMEOUT_SEC) as resp:
            body = resp.read(MAX_BODY_BYTES).decode("utf-8", errors="ignore")
            status = getattr(resp, "status", None)
            ctype = resp.headers.get("Content-Type", "")
    except Exception as exc:
        return FetchSnapshot(
            ok=False,
            status=None,
            content_type="",
            final_url=url,
            title="",
            body_text="",
            error=f"reader fallback failed: {exc}",
        )

    body_text = normalize_text(body)
    has_target_error = "Warning: Target URL returned error" in body or "Markdown Content: 5" in body
    # r.jina often returns first line as "Title: ...".
    title = ""
    for ln in body.splitlines()[:8]:
        if ln.lower().startswith("title:"):
            title = normalize_text(ln.split(":", 1)[1].strip(), 180)
            break

    return FetchSnapshot(
        ok=not has_target_error,
        status=status,
        content_type=ctype or "text/plain",
        final_url=url,
        title=title,
        body_text=body_text,
        error="reader proxy returned target error" if has_target_error else "",
    )


def parse_x_status(url: str) -> Tuple[str, str]:
    try:
        p = urlparse(url)
    except Exception:
        return "", ""
    host = canonical_host(url)
    if host not in {"x.com", "twitter.com"}:
        return "", ""
    parts = [x for x in (p.path or "").split("/") if x]
    if len(parts) >= 3 and parts[1] == "status" and parts[0] != "i":
        return parts[0], parts[2]
    return "", ""


def fetch_x_api_snapshot(url: str) -> FetchSnapshot:
    user, status_id = parse_x_status(url)
    if not user or not status_id:
        return FetchSnapshot(
            ok=False,
            status=None,
            content_type="",
            final_url=url,
            title="",
            body_text="",
            error="not x status url",
        )

    api_url = f"https://api.fxtwitter.com/{user}/status/{status_id}"
    req = urllib.request.Request(
        url=api_url,
        headers={"User-Agent": "OpenClaw-ResourceSync/1.1", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SEC) as resp:
            body = resp.read(MAX_BODY_BYTES).decode("utf-8", errors="ignore")
            status = getattr(resp, "status", None)
    except Exception as exc:
        return FetchSnapshot(
            ok=False,
            status=None,
            content_type="",
            final_url=url,
            title="",
            body_text="",
            error=f"x api failed: {exc}",
        )

    try:
        data = json.loads(body)
    except Exception:
        return FetchSnapshot(
            ok=False,
            status=status,
            content_type="application/json",
            final_url=url,
            title="",
            body_text="",
            error="x api non-json",
        )

    tweet = data.get("tweet") if isinstance(data, dict) else {}
    if not isinstance(tweet, dict):
        tweet = {}

    text = normalize_text(tweet.get("text", ""), 6000)
    article = tweet.get("article", {})
    article_title = ""
    if isinstance(article, dict):
        article_title = normalize_text(article.get("title", ""), 220)
        if not text:
            content = article.get("content", {})
            blocks = content.get("blocks", []) if isinstance(content, dict) else []
            block_texts: List[str] = []
            for blk in blocks:
                if not isinstance(blk, dict):
                    continue
                t = normalize_text(blk.get("text", ""), 240)
                if t and not is_noisy_sentence(t):
                    block_texts.append(t)
                if len(block_texts) >= 10:
                    break
            text = normalize_text(" ".join(block_texts), 6000)

    if not text:
        return FetchSnapshot(
            ok=False,
            status=status,
            content_type="application/json",
            final_url=url,
            title=article_title,
            body_text="",
            error="x api empty text",
        )

    title = article_title
    if not title:
        first = split_sentences(text)
        title = first[0] if first else ""

    return FetchSnapshot(
        ok=True,
        status=status or 200,
        content_type="application/json",
        final_url=url,
        title=normalize_text(title, 220),
        body_text=text,
        error="",
    )


def x_alternative_urls(url: str) -> List[str]:
    out: List[str] = []
    p = urlparse(url)
    host = canonical_host(url)
    parts = [x for x in (p.path or "").split("/") if x]
    if host not in {"x.com", "twitter.com"}:
        return out
    if len(parts) >= 3 and parts[1] == "status":
        path = "/".join(parts[:3])
        out.append(f"https://fxtwitter.com/{path}")
        out.append(f"https://vxtwitter.com/{path}")
    out.append(url)
    dedup: List[str] = []
    for u in out:
        if u not in dedup:
            dedup.append(u)
    return dedup


def extract_x_status_url_from_text(text: str) -> str:
    for u in URL_RE.findall(text or ""):
        n = normalize_url(u)
        user, status_id = parse_x_status(n)
        if user and status_id:
            return n
    return ""


def snapshot_quality(snapshot: FetchSnapshot) -> int:
    if not snapshot.ok:
        return -1
    txt = snapshot.body_text or ""
    score = len(txt)
    if snapshot.status == 200:
        score += 300
    if "json" in (snapshot.content_type or "").lower():
        score += 1200
    if snapshot.title:
        score += 120
    low = txt.lower()
    if "html,body{" in txt or "stylesheet-group" in txt or "::cue" in txt:
        score -= 800
    if "Warning: Target URL returned error" in txt:
        score -= 1200
    if any(tok in low for tok in X_UI_NOISE_TOKENS):
        score -= 1400
    if "x url source:" in low:
        score += 180
    if "markdown content:" in low:
        score += 120
    return score


def fetch_best_snapshot(url: str, api_key: str) -> FetchSnapshot:
    candidates = [url]
    x_alts = x_alternative_urls(url)
    if x_alts:
        candidates = x_alts

    best = FetchSnapshot(
        ok=False,
        status=None,
        content_type="",
        final_url=url,
        title="",
        body_text="",
        error="no snapshot",
    )
    best_score = -10**9

    host = canonical_host(url)
    if host in {"x.com", "twitter.com"}:
        x_api = fetch_x_api_snapshot(url)
        x_api_score = snapshot_quality(x_api)
        if x_api_score > best_score:
            best, best_score = x_api, x_api_score
        if x_api.ok and len(x_api.body_text or "") >= 40:
            return x_api

    for idx, candidate in enumerate(candidates):
        key = api_key if idx == 0 else ""
        snap = fetch_snapshot(candidate, key)
        snap_score = snapshot_quality(snap)
        if snap_score > best_score:
            best, best_score = snap, snap_score
        if snap.ok and len(snap.body_text or "") >= 320:
            continue
        reader = fetch_reader_snapshot(candidate)
        reader_score = snapshot_quality(reader)
        if reader_score > best_score:
            best, best_score = reader, reader_score

    return best


def collect_quotes_from_json(data: object, out: List[str], limit: int = MAX_QUOTES) -> None:
    if len(out) >= limit:
        return
    if isinstance(data, dict):
        for v in data.values():
            collect_quotes_from_json(v, out, limit)
            if len(out) >= limit:
                return
        return
    if isinstance(data, list):
        for v in data:
            collect_quotes_from_json(v, out, limit)
            if len(out) >= limit:
                return
        return
    if isinstance(data, str):
        text = normalize_text(data, 180)
        if len(text) >= 12:
            out.append(text)


def build_auto_summary(hit: ResourceHit, host_contexts: Dict[str, HostContext]) -> str:
    snapshot = fetch_best_snapshot(hit.url, extract_api_key(hit.message.text))
    host = canonical_host(hit.url)
    path_l = (urlparse(hit.url).path or "").lower()
    if host in {"x.com", "twitter.com"} and "/i/article/" in path_l and (not snapshot.ok or len(snapshot.body_text or "") < 120):
        status_url = extract_x_status_url_from_text(hit.message.text or "")
        if status_url:
            alt_snapshot = fetch_best_snapshot(status_url, extract_api_key(hit.message.text))
            if alt_snapshot.ok and len(alt_snapshot.body_text or "") >= len(snapshot.body_text or ""):
                snapshot = alt_snapshot
    hard_fetch_fail = (not snapshot.ok) or (snapshot.status is None) or (snapshot.status >= 400)
    body_points = extract_summary_from_body(snapshot.body_text or "", limit=8)
    summary_points: List[str] = []
    # Strict mode: only website/tweet body content, never chat context.
    for p in body_points:
        p = redact_secrets(p)
        if p and not is_low_signal_summary_point(p) and p not in summary_points:
            summary_points.append(p)
        if len(summary_points) >= 8:
            break

    title_hint = polish_sentence(snapshot.title or "")
    if title_hint and not is_noisy_sentence(title_hint) and not is_generic_title(title_hint):
        if title_hint not in summary_points:
            summary_points = [title_hint] + summary_points
            summary_points = summary_points[:8]

    if not summary_points:
        context_points = extract_summary_from_context(hit.message.text or "", limit=5)
        context_points = [p for p in context_points if p and not is_low_signal_summary_point(p)]
        if context_points:
            summary_points = context_points[:5]
            summary_points.append("注：正文抓取受限，本摘要基于频道上下文，待后续正文抓取校验。")
        elif host in {"x.com", "twitter.com", "t.co"}:
            summary_points = [
                "该链接为 X 资源，当前自动抓取正文受限，暂未拿到稳定全文。",
                "已保留原始来源链接与可访问镜像，等待后续补抓或手工补录事实要点。",
            ]
        else:
            summary_points = [
                "当前自动抓取正文失败或内容质量不足，暂未形成可靠摘要。",
                "已保留来源链接，后续会重试抓取并补齐关键结论。",
            ]
    if host in {"x.com", "twitter.com", "t.co"} and len(summary_points) < 2:
        summary_points.append("当前仅抓取到标题级内容，推文/文章正文受站点限制，后续重试补全文。")

    filtered_points: List[str] = []
    for p in summary_points:
        p = polish_sentence(p)
        if not p or is_low_signal_summary_point(p) or is_noisy_sentence(p):
            continue
        if p not in filtered_points:
            filtered_points.append(p)
    summary_points = filtered_points[:8]

    raw_links: List[str] = []
    raw_links.extend(extract_links(hit.message.text))
    if snapshot.final_url:
        raw_links.append(snapshot.final_url)
    raw_links.extend(x_alternative_urls(hit.url))
    links = clean_resource_links(raw_links, primary=hit.url, max_items=5)

    actions: List[str] = []
    host_l = host.lower() if host else ""
    path_l = urlparse(hit.url).path.lower()
    if "x.com" in host_l or "twitter.com" in host_l:
        actions.append("输出 5 句中文事实摘要（观点、证据、结论），并附上原始链接。")
        actions.append("把可执行启发拆成 1-2 条具体任务（owner/next_action/due）。")
    if "api" in host_l or "/api/" in path_l:
        actions.append("补一段可直接运行的 API 调用示例（请求头、参数、返回字段）。")
    if extract_api_key(hit.message.text):
        actions.append("立即轮换暴露的 API Key，改为环境变量引用，不再写入聊天与笔记正文。")
    if hard_fetch_fail:
        actions.append("当前源站不可达；先基于上下文推进事项，后续由流水线自动二次抓取补全。")
    actions.append("将本条内容关联到一个具体项目，避免资源笔记孤立。")
    dedup_actions: List[str] = []
    for a in actions:
        if a not in dedup_actions:
            dedup_actions.append(a)
    actions = dedup_actions[:5]

    lines: List[str] = []
    lines.append("## Auto Summary")
    lines.append("")
    lines.append("### Content Summary")
    for p in summary_points:
        lines.append(f"- {p}")
    if not summary_points:
        lines.append("- (no summary extracted)")
    lines.append("")
    lines.append("### Links")
    for idx, link in enumerate(links):
        if idx == 0:
            lines.append(f"- Primary: {link}")
        else:
            lines.append(f"- Related: {link}")
    if not links:
        lines.append("- (no links extracted)")
    lines.append("")
    lines.append("### What We Can Do")
    for t in actions:
        lines.append(f"- {t}")
    lines.append("")
    return "\n".join(lines)


def upsert_auto_summary(note_body: str, auto_summary_md: str) -> str:
    note_body = re.sub(r"(?ms)^## Notes To Expand.*?(?=^## |\Z)", "", note_body)
    note_body = re.sub(r"(?ms)^## Captured Context.*?(?=^## |\Z)", "", note_body)
    note_body = note_body.rstrip() + "\n\n"
    block = auto_summary_md.strip() + "\n\n"
    if "## Auto Summary" in note_body:
        replaced = re.sub(
            r"(?ms)^## Auto Summary.*?(?=^## |\Z)",
            lambda _m: block.rstrip(),
            note_body,
        )
        if replaced.endswith("\n"):
            return replaced
        return replaced + "\n"

    marker = "## Notes To Expand"
    if marker in note_body:
        return note_body.replace(marker, block + marker, 1)
    return note_body.rstrip() + "\n\n" + block


def note_needs_summary(note_body: str) -> bool:
    return "## Auto Summary" not in note_body


def note_should_refresh_summary(note_body: str) -> bool:
    if note_needs_summary(note_body):
        return True
    m = re.search(r"(?ms)^## Auto Summary\n(.*?)(?=^## |\Z)", note_body)
    if not m:
        return True
    block = m.group(1)
    if "### Content Summary" not in block or "### Links" not in block or "### What We Can Do" not in block:
        return True
    if re.search(r"https?://\S+[）)\]】]", block):
        return True
    if "Fetch error:" in block or "Warning: Target URL returned error" in block:
        return True
    if "html,body{" in block or "stylesheet-group" in block or "::cue" in block:
        return True
    if "x.com/login" in block or "x.com/i/flow/signup" in block:
        return True
    if any(p in block.lower() for p in LOW_SIGNAL_SUMMARY_PHRASES):
        return True
    m_status = re.search(r"Fetch status:\s*`(\d{3})`", block)
    if m_status:
        status = int(m_status.group(1))
        if status >= 500:
            return True
    return False


def auto_summary_is_unreadable(auto_summary_md: str) -> bool:
    block = (auto_summary_md or "").strip()
    if not block:
        return True
    low = block.lower()
    if any(m.lower() in low for m in UNREADABLE_SUMMARY_MARKERS):
        return True

    m = re.search(r"(?ms)^### Content Summary\n(.*?)(?=^### |\Z)", block)
    if not m:
        return True
    lines = [ln.strip() for ln in m.group(1).splitlines() if ln.strip().startswith("- ")]
    good = []
    for ln in lines:
        text = ln[2:].strip()
        if not text:
            continue
        if is_noisy_sentence(text) or is_low_signal_summary_point(text):
            continue
        good.append(text)
    return len(good) < 2


def should_drop_note_as_unreadable(note_body: str, url: str) -> bool:
    host = canonical_host(url) if url else ""
    path_l = (urlparse(url).path or "").lower() if url else ""
    title = (extract_frontmatter_title(note_body) or extract_h1_title(note_body)).strip().lower()
    if title == "x 文章洞察" or title.startswith("x 短链 "):
        return True
    if host == "t.co":
        return True
    auto_block = extract_auto_summary_block(note_body)
    if auto_block and auto_summary_is_unreadable(auto_block):
        return True
    if host in {"x.com", "twitter.com"} and "/i/article/" in path_l and not auto_block:
        return True
    return False


def parse_note_to_hit(note_path: Path, note_body: str) -> Optional[ResourceHit]:
    # Frontmatter fields.
    url = ""
    m_url = re.search(r'^original_url:\s*"([^"]+)"', note_body, flags=re.MULTILINE)
    if m_url:
        url = m_url.group(1).strip()
    if not url:
        m_url2 = re.search(r"^- URL:\s*(\S+)", note_body, flags=re.MULTILINE)
        if m_url2:
            url = m_url2.group(1).strip()
    if not url:
        return None

    def field(name: str, default: str = "") -> str:
        m = re.search(rf'^{name}:\s*"([^"]*)"', note_body, flags=re.MULTILINE)
        return m.group(1).strip() if m else default

    context = extract_frontmatter_field(note_body, "capture_intent")

    msg = FeedMessage(
        date=field("captured_date", note_path.stem[:10] if DATE_RE.match(note_path.stem[:10]) else ""),
        channel=field("source_channel", "unknown"),
        message_id=field("message_id", ""),
        timestamp="",
        sender=field("source_sender", "unknown"),
        text=context,
    )
    return ResourceHit(message=msg, url=url)


def build_note(hit: ResourceHit, host_contexts: Dict[str, HostContext], auto_summary_md: str = "") -> str:
    now_iso = datetime.now().astimezone().isoformat()
    auto_summary = auto_summary_md or build_auto_summary(hit, host_contexts)
    title = pick_meaningful_title(hit, auto_summary_md=auto_summary)
    meta = NoteMeta(title=title, url=hit.url, context=hit.message.text or "")
    category, subtype = classify_resource(meta)
    sender = hit.message.sender or "unknown"
    text = redact_secrets((hit.message.text or "").strip())
    intent = derive_title_hint_from_message(text) or "来自资源频道的外部链接，已进入知识沉淀流程。"

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
    lines.append(f"source_title: \"{title}\"")
    lines.append("source_author: \"\"")
    lines.append("published_at: \"\"")
    lines.append(f"capture_intent: \"{intent}\"")
    lines.append(f"resource_category: \"{category}\"")
    lines.append(f"resource_subtype: \"{subtype}\"")
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
    lines.append("## Capture Intent")
    lines.append(f"- {intent}")
    lines.append("")
    lines.append("## Classification")
    lines.append(f"- Category: {category}")
    lines.append(f"- Subtype: {subtype}")
    lines.append("")
    lines.append(auto_summary)
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace)
    resources_dir = workspace / args.vault / "Resources"
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
    resource_messages = [m for m in all_messages if is_resource_channel(m.channel)]
    host_contexts = build_host_contexts(resource_messages)

    state = load_state(state_path)
    seen = state.get("urls", {})
    if not isinstance(seen, dict):
        seen = {}

    hits: List[ResourceHit] = []
    for msg in resource_messages:
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
    enriched = 0
    enriched_all_notes = 0
    skipped = 0
    dropped_unreadable = 0
    for fp, h in picked.items():
        if fp in seen:
            file_path = Path(seen[fp].get("file", ""))
            if not file_path.exists():
                # State drift: file moved/deleted; recreate below.
                seen.pop(fp, None)
            else:
                raw = file_path.read_text(encoding="utf-8", errors="ignore")
                sanitized = redact_secrets(raw)
                changed_local = False
                current = sanitized
                category, subtype = classify_resource(NoteMeta(title=derive_resource_title(h), url=h.url, context=h.message.text or ""))
                classified = upsert_classification(current, category, subtype)
                if classified != current:
                    current = classified
                    changed_local = True
                if args.force_refresh or note_should_refresh_summary(current):
                    auto = build_auto_summary(h, host_contexts)
                    current = upsert_auto_summary(current, auto)
                    final_title = pick_meaningful_title(h, auto_summary_md=auto, current_note_body=current)
                    current = upsert_note_title(current, final_title)
                    current = upsert_source_title(current, final_title)
                    changed_local = True
                    enriched += 1
                if should_drop_note_as_unreadable(current, h.url):
                    file_path.unlink(missing_ok=True)
                    seen.pop(fp, None)
                    dropped_unreadable += 1
                    continue
                if changed_local or sanitized != raw:
                    file_path.write_text(current, encoding="utf-8")
                skipped += 1
                continue

        auto = build_auto_summary(h, host_contexts)
        if auto_summary_is_unreadable(auto):
            dropped_unreadable += 1
            seen.pop(fp, None)
            continue
        title = pick_meaningful_title(h, auto_summary_md=auto)
        stem = title_to_stem(title, slug_from_url(h.url))
        out = resources_dir / f"{stem}.md"

        # Avoid accidental overwrite collisions.
        if out.exists():
            suffix = fp[:8]
            out = resources_dir / f"{stem}-{suffix}.md"

        out.write_text(build_note(h, host_contexts, auto_summary_md=auto), encoding="utf-8")
        seen[fp] = {
            "url": h.url,
            "file": str(out),
            "message_id": h.message.message_id,
            "channel": h.message.channel,
            "timestamp": h.message.timestamp,
            "synced_at": datetime.now().astimezone().isoformat(),
        }
        created += 1

    if args.enrich_all_notes:
        for note in sorted(resources_dir.glob("*.md")):
            if note.name in {"_TEMPLATE.md", "_资源分类索引.md"}:
                continue
            raw = note.read_text(encoding="utf-8", errors="ignore")
            sanitized = redact_secrets(raw)
            changed = False
            current = sanitized
            if sanitized != raw:
                changed = True
            base_meta = extract_note_meta(note, current)
            base_category, base_subtype = classify_resource(base_meta)
            with_base_class = upsert_classification(current, base_category, base_subtype)
            if with_base_class != current:
                current = with_base_class
                changed = True
            title_changed = False
            hit = parse_note_to_hit(note, current)
            if hit is not None:
                auto_block = extract_auto_summary_block(current)
                new_title = pick_meaningful_title(hit, auto_summary_md=auto_block, current_note_body=current)
                with_title = upsert_note_title(current, new_title)
                if with_title != current:
                    current = with_title
                    changed = True
                    title_changed = True
                with_source_title = upsert_source_title(current, new_title)
                if with_source_title != current:
                    current = with_source_title
                    changed = True
                category, subtype = classify_resource(NoteMeta(title=new_title, url=hit.url, context=hit.message.text or ""))
                with_class = upsert_classification(current, category, subtype)
                if with_class != current:
                    current = with_class
                    changed = True
            if args.force_refresh or note_should_refresh_summary(current):
                if hit is not None:
                    auto = build_auto_summary(hit, host_contexts)
                    current = upsert_auto_summary(current, auto)
                    final_title = pick_meaningful_title(hit, auto_summary_md=auto, current_note_body=current)
                    current = upsert_note_title(current, final_title)
                    current = upsert_source_title(current, final_title)
                    changed = True
                    title_changed = True
                    enriched_all_notes += 1
            current_url = ""
            if hit is not None:
                current_url = hit.url
            else:
                current_url = extract_frontmatter_field(current, "original_url")
            if should_drop_note_as_unreadable(current, current_url):
                old_path = str(note)
                note.unlink(missing_ok=True)
                for k, rec in list(seen.items()):
                    if isinstance(rec, dict) and rec.get("file") == old_path:
                        seen.pop(k, None)
                dropped_unreadable += 1
                continue
            if args.force_refresh:
                changed = True
            if changed:
                target = note
                fm_title = extract_frontmatter_title(current)
                if fm_title:
                    fm_stem = title_to_stem(fm_title, note.stem)
                    fm_desired = resources_dir / f"{fm_stem}.md"
                    if fm_desired != note and not fm_desired.exists():
                        target = fm_desired
                if hit is not None and (title_changed or args.force_refresh):
                    final_title = extract_frontmatter_title(current) or extract_h1_title(current) or derive_resource_title(hit)
                    stem = title_to_stem(final_title, slug_from_url(hit.url))
                    desired = resources_dir / f"{stem}.md"
                    if desired != note:
                        if desired.exists():
                            desired = resources_dir / f"{stem}-{url_fingerprint(hit.url)[:8]}.md"
                        target = desired
                target.write_text(current, encoding="utf-8")
                if target != note:
                    old_path = str(note)
                    note.unlink(missing_ok=True)
                    for k, rec in seen.items():
                        if isinstance(rec, dict) and rec.get("file") == old_path:
                            rec["file"] = str(target)

    generate_category_index(resources_dir)

    state["urls"] = seen
    state["last_sync"] = datetime.now().astimezone().isoformat()
    save_state(state_path, state)

    print(json.dumps({
        "dates": dates,
        "messages_parsed": len(all_messages),
        "resource_messages": len(resource_messages),
        "url_hits": len(hits),
        "unique_urls": len(picked),
        "created": created,
        "enriched_existing": enriched,
        "enriched_all_notes": enriched_all_notes,
        "skipped_existing": skipped,
        "dropped_unreadable": dropped_unreadable,
        "resources_dir": str(resources_dir),
        "state": str(state_path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
