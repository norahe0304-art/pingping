---
title: "X 洞察：Cloudflare MCP Code Mode——用极低 Token 成本调用 API 的创新"
original_url: "https://x.com/vikingmute/status/2025098635021877622?s=46&t=gC1r3zh0g-l5o215P0tIzg"
---

## 阅读理解

这条推文介绍了 Cloudflare 新推出的 MCP Code Mode，作者 @vikingmute 认为这是一个重大创新。传统 MCP 的做法是把所有 API endpoint 的描述全部塞进上下文，导致 token 消耗巨大。Code Mode 的做法是又包了一层，只暴露两个工具：search() 和 execute()。search 让 Agent 自己写代码搜索要用到的 endpoint，execute 直接运行并验证结果。这样 Agent 可以用大约 1000 个 token 的极低成本完成 API 调用，而不是把整个 API 文档塞进上下文窗口。

## 实战洞察

这个设计思路对 MCP 生态有深远影响。当前 MCP 最大的痛点之一就是 token 消耗——每个工具的描述都要占用上下文窗口，工具越多成本越高。Cloudflare 的 Code Mode 通过"搜索+执行"的两步模式，把 token 消耗从线性增长变成了常量级别。这个模式不仅适用于 Cloudflare 自己的服务，任何拥有大量 API endpoint 的 MCP 服务都可以借鉴这个架构。对于正在构建 MCP 服务的开发者来说，这提供了一个全新的设计范式：不要暴露所有工具，而是暴露"发现工具的工具"。

## 原文链接
https://x.com/vikingmute/status/2025098635021877622?s=46&t=gC1r3zh0g-l5o215P0tIzg
