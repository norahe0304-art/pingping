---
title: "OpenTwitter MCP——通过 ClawHub 访问 Twitter 数据的 API 服务"
original_url: "https://clawhub.ai/infra403/opentwitter-mcp"
---

## 阅读理解

这是 ClawHub 上的 OpenTwitter MCP 服务文档。该服务提供了一套通过 Bearer Token 认证的 Twitter 数据 API，包括：通过用户名获取用户信息、通过数字 ID 获取用户信息、获取用户最近推文、搜索推文（支持多种过滤条件）。所有端点都需要通过 `$TWITTER_TOKEN` 进行 Bearer 认证，API 基础地址为 `https://ai.6551.io/open/`。文档提供了完整的 curl 示例，可以直接复制使用。

## 实战洞察

OpenTwitter MCP 为 AI Agent 提供了一个轻量级的 Twitter 数据访问方案。相比官方 Twitter API 的复杂认证流程和高昂定价，这个 MCP 服务的接入成本更低。对于需要 Agent 具备 Twitter 数据获取能力的场景（如社交媒体监控、竞品分析、内容策展），这是一个值得评估的选项。需要注意的是，作为第三方服务，数据的完整性、延迟和稳定性需要实际测试验证，同时要关注其数据来源的合规性。

## 原文链接
https://clawhub.ai/infra403/opentwitter-mcp
