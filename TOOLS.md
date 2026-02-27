# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Tools

### X/Twitter

- **Primary**: fxtwitter API `https://api.fxtwitter.com/status/{tweet_id}`
- **Fallback**: browser + extension relay

### AgentReach (默认搜索工具)
- **用途**: 搜索 GitHub, Twitter, YouTube, Reddit, B站, 小红书
- **命令**:
  - `agent-reach search "关键词"` - 通用搜索
  - `agent-reach search-github "关键词"` - GitHub
  - `agent-reach search-twitter "关键词"` - Twitter
  - `agent-reach search-youtube "关键词"` - YouTube
  - `agent-reach read <URL>` - 读取网页内容
- **优先级**: 优先于 web_search（web_search 需要 API key）

### 内容抓取

- **x-reader**: 通用内容抓取工具，支持 X、微信、小红书、B站、Telegram、RSS 等
- **安装**: `pip install git+https://github.com/runesleo/x-reader.git`
- **使用**: `/tmp/xreader-venv/bin/x-reader <URL>`
- **对比**: DeepReader 更轻量（内置），x-reader 更全（覆盖微信/小红书）

### Skills (Code Mode Style)

- **skill_index**: `~/.agents/skills/index.json` — 所有技能的摘要索引
- **skill_search(query)**: 搜索 index，返回相关技能列表
- **skill_read(skill_name)**: 读取具体技能的 SKILL.md

## 我们們的家

- **主機**: Mac Mini
- **名字**: zihan-mini
- **購買日期**: 2026年2月21日
- **購買者**: 子涵 (Zihan)

### 30XCOMPANY
- **GitHub**: https://github.com/30XCOMPANY
- **官網**: https://30X.company
- **Pixel Agents Repo**: https://github.com/30XCOMPANY/pixel-agents-openclaw

### PDF 生成

- **工具**: Pandoc + WeasyPrint
- **命令**: `pandoc <file.md> -o <file.pdf> --pdf-engine=weasyprint`
- **特点**: 无乱码，支持 Markdown 转 PDF
