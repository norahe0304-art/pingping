---
type: Resource
title: "面向Agent设计: Agent-First产品思维"
original_url: https://x.com/PleaseCallMeWhy/status/2026705456455102560
source_title: "面向 Agent 设计：Agent First 思维"
source_author: PleaseCallMeWhy
published_at: ""
captured_date: "2026-02-27"
source_channel: "📦-资源"
source_sender: "bravohenry"
message_id: ""
tags: [agent, design-pattern, agentcal, introspection, product-design]
---

# 面向Agent设计: Agent-First产品思维

## 内容摘要

1. **核心理念**：未来 Agent 才是互联网的一等公民，所有产品都应该面向 AI 来设计，而不是传统的 Mobile First
2. **自省接口**：增加 Introspection API，让 Agent 自己发现有哪些功能可用，而不是写死的 Skill 清单
3. **Skill 教方法不列清单**：告诉 Agent"怎么查"而不是"有什么"
4. **技术栈**：用 Zod + tRPC + meta 让类型描述自动生成 API 文档
5. **授人以渔**：让 Agent 自己发现问题，而不是喂答案
6. **产品设计转变**：现在产品是"给人用的"（需要 UI），以后是"给 Agent 用的"（需要自省接口）
7. **对 AgentCal 启发**：Agent 加载 skill 后能自己发现新功能，不需要手动配置
8. **过渡方案**：A2UI 做 chatbot，人类直接说话就能操作产品

## 我们可以做什么

1. **加自省接口**：在 AgentCal 中加入自省接口设计，让 Agent 能自己发现功能
2. **建立包装模板**：以后包装 GitHub 项目时，提供这种面向 Agent 的框架
3. **测试 A2UI**：测试 A2UI 作为过渡方案的可行性
4. **重新定义产品**：思考产品如何从"给人用"转向"给 Agent 用"
