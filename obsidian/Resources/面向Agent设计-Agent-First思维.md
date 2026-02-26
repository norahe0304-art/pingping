---
type: Resource
original_url: https://x.com/PleaseCallMeWhy/status/2026705456455102560
source: X (Twitter)
tags:
  - agent
  - design-pattern
  - agentcal
---

# 面向 Agent 设计：Agent First 思维

## 阅读理解

这篇文章核心讲的是"Agent First"思维——未来 Agent 才是互联网的一等公民，所有产品都应该面向 AI 来设计，而不是传统的 Mobile First。作者认为不应该简单丢给 Agent 一个 API 或文档就完事，而是要在架构层面让 Agent 能够自省、自发现。

具体做法有三个层面：一是增加自省接口（Introspection API），让 Agent 自己发现有哪些功能可用，而不是写死的 Skill 清单；二是 Skill 只教方法不列清单，告诉 Agent"怎么查"而不是"有什么"；三是用 Zod + tRPC + meta 让类型描述自动生成 API 文档。

作者用"授人以鱼不如授人以渔"来总结这个思路——让 Agent 自己发现问题，而不是喂答案。

## 实战洞察

对 AgentCal 的启发：

1. **加自省接口** — Agent 加载 skill 后能自己发现新功能，不需要手动配置
2. **Agent Ready 框架模板** — 以后包装 GitHub 项目时，可以提供这种面向 Agent 的框架
3. **过渡方案** — 用 A2UI 做 chatbot，人类直接说话就能操作产品

对包装 GitHub 项目的启发：不仅是给 API，还要给"自省"能力，让 Agent 能自己发现功能，不需要每个都手动适配。

---
