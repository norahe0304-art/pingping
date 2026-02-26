# Agent First - 让产品优先为 AI 服务

---
type: resource
status: inbox
created_at: "2026-02-26T13:57:00Z"
captured_date: "2026-02-26"
source_channel: "discord-资源"
source_sender: "Nora (yixiaohe)"
message_id: "1476654435747762267"
original_url: "https://x.com/PleaseCallMeWhy/status/2026705456455102560"
source_title: "Agent First - 让你的产品优先为 AI 服务"
tags: [resource, discord, agent, product-design]
---

## Source
- Main URL: https://x.com/PleaseCallMeWhy/status/2026705456455102560

## 阅读理解
未来 Agent 才是互联网的一等公民，所有的产品设计都应该从 "Mobile First" 转向 "Agent First"——优先为 AI Agent 服务，而不是为人类用户。

实现 Agent First 的关键不是简单提供 API 或 Markdown 文档，而是让整个软件架构天然支持 Agent 操作。具体做法：1）增加自省接口 (Introspection API)，让 Agent 自己发现有哪些接口可用；2）写一个通用 Skill 教 Agent "怎么查" 而不是 "有什么"，这样 Skill 写一次就固定，API 改动会自动被发现；3）利用 Zod + tRPC + meta 自动生成 API 文档。未来的产品，UI/UX 会越来越不重要，因为 Agent 可以直接调用接口，不需要通过浏览器。

## 实战洞察
这个思路和我们之前的 AgentCal 改造方向一致。可以给 AgentCal 增加自省接口，让加载了 skill 的 Agent 能自己发现新功能，而不是每次功能更新都需要手动适配 skill。后续包装 GitHub 项目时，可以提供"Agent Ready"的框架模板，加入 Introspection API 和通用 Skill，让项目天然支持 AI Agent 调用。
