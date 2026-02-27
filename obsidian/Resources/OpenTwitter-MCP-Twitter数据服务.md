---
type: Resource
original_url: https://github.com/6551Team/opentwitter-mcp
source: GitHub
tags:
  - mcp
  - twitter
  - social-media
---

# OpenTwitter MCP: Twitter 数据 MCP 服务

## 核心要点

OpenTwitter MCP 是 6551 团队做的 Twitter/X 数据 MCP 服务，让 AI Agent 能直接查询 Twitter 数据。

核心功能：
- 用户资料查询
- 推文搜索
- 粉丝事件追踪
- KOL（关键意见领袖）追踪

API 返回结构化数据，包括粉丝数、关注数、发推数、是否认证等。

这个 MCP 对我们做内容调研很有用。比如想了解某个 KOL 的背景，不需要手动刷 Twitter，直接让 Agent 查询就能拿到结构化的账号信息。对于舆情监控场景也很合适——搜关键词、追踪特定账号动态。

但需要注意：可能需要 Twitter API 配额。如果不想付费，fxtwitter API 是免费替代方案，只是功能没那么全。

## 实战洞察

对我们的价值：

1. **Twitter 舆情监控** — 搜特定关键词、追踪 KOL 动态
2. **做内容调研** — 快速了解某个账号的背景信息
3. **MCP 写法参考** — 学习如何写一个 MCP server

动作：
1. 对比 OpenTwitter MCP 和 fxtwitter API 的功能差异
2. 根据需求选择方案
3. 如果用 OpenTwitter，申请 API 配额或找替代方案
