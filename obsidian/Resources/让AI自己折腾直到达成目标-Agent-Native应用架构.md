---
type: resource
status: inbox
created_at: "2026-02-28"
captured_date: "2026-02-28"
source_channel: "discord"
source_sender: "Friday"
message_id: "1477148094322966659"
original_url: "https://every.to/guides/agent-native"
source_title: "Agent-native Architectures: How to Build Apps After Code Ends"
tags: [resource, agent-native, architecture, AI-agent]
---

# 让AI自己折腾直到达成目标

## 内容摘要

1. **核心理念转变**：从"写代码实现功能"变成"描述结果，AI 自己折腾直到达成"
2. **五大设计原则**：Parity（对等）、Granularity（原子化）、Composability（组合性）、Emergent Capability（涌现能力）、Improvement over time（持续优化）
3. **Parity 原则**：确保 AI 能做到 UI 能做的任何事，不被预设功能限制
4. **Granularity 原则**：工具要足够小，让 feature 是"描述结果"而非预设流程
5. **Composability 原则**：写新 prompt 就能创造新功能，不需要改代码
6. **Emergent Capability**：AI 能完成你没想到要设计的功能，带来惊喜
7. **文件是最佳接口**：AI 最擅长文件系统、用户看得懂能修改、跨设备同步天然支持
8. **工具分层实现**：基础工具（bash/文件操作）→ 领域工具 → 性能关键路径才写优化代码
9. **优先用文件而非数据库**：除非需要复杂查询或高并发
10. **不用发版，靠改 prompt 就能持续优化**

## 我们可以做什么

1. **用 Agent-Native 框架重新设计 30X 客服 agent**：确保 AI 能完成客服 UI 的任何操作
2. **工具原子化改造**：让业务逻辑不写死在代码里，AI 能自主组合处理方式
3. **建立"观察-涌现"机制**：通过观察用户实际让 agent 做什么来发现隐藏需求
4. **下次会议用这个框架评估现有客服 agent 的架构**
