---
type: Resource
original_url: https://github.com/runesleo/x-reader
source: GitHub
tags:
  - content-reader
  - tool
  - mcp
---

# x-reader: 通用内容抓取工具

## 阅读理解

x-reader 是一个通用内容读取工具，支持 7+ 平台的内容抓取（微信、小红书、B站、Telegram、RSS 等），比 DeepReader 覆盖更广。

核心特点：

- 输入任意 URL（文章、视频、播客、推文），输出结构化内容
- 支持多种使用方式：CLI、Python 库、MCP server、Claude Code skill
- 可选：Whisper 视频/播客转录 + AI 内容分析

三层架构，可组合使用。

和 DeepReader 比，x-reader 覆盖更多国内平台（微信、小红书），但 DeepReader 更轻量。

## 实战洞察

对你们的价值：

1. **国内平台覆盖** — 微信、小红书这些 DeepReader 抓不了的，x-reader 可以
2. **MCP 集成** — 可以作为 MCP server 被各种 Agent 调用
3. **Claude Code 集成** — 可以用 skill 的方式调用

需要：

- 微信/小红书 Cookie（之前说还没配置）
- 某些平台可能需要登录态

---
