---
type: Resource
original_url: https://github.com/kevinho/clawfeed
source: GitHub
tags:
  - news
  - digest
  - automation
  - openclaw
---

# ClawFeed: AI 新闻摘要生成器

## 阅读理解

ClawFeed 是一个 AI 驱动的新闻摘要工具，从 Twitter、RSS 和网页来源自动抓取内容，生成结构化摘要。

核心功能：

- 从 Twitter/RSS/网页来源抓取
- AI 生成结构化摘要（4H 模式：Headlines, Highlights, Happend, Hooks）
- 支持日/周/月报
- 可独立运行，也可作为 OpenClaw/Zylos 的 skill
- 支持 cron 定时生成摘要
- 提供 Dashboard 展示
- 无 OAuth 时是只读模式

有 Demo: https://clawfeed.kevinhe.io

## 实战洞察

对你们的价值：

1. **每日资讯自动化** — 可以做成你们的"每日 AI 新闻"简报
2. **可作为 OpenClaw skill** — 直接集成到现有系统
3. **结构化输出** — 4H 模式便于消费

需要注意：

- 需要配置 OAuth 才能写 Twitter
- 只读模式已经够用（抓取 + 摘要）

---
