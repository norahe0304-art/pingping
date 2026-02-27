---
type: resource
status: inbox
created_at: "2026-02-26T12:27:05.384420-05:00"
captured_date: "2026-02-21"
source_channel: "📦-资源"
source_sender: "yixiaohe"
message_id: "1474823405562888146"
original_url: "https://x.com/elonmusk/status/2025068777971485083?s=20"
source_title: "多Agent架构与AI软件工厂"
tags: [resource, discord, agent, architecture]
---

# 多Agent架构与AI软件工厂

## 核心要点

多 Agent 架构让 AI 能够像人类团队一样分工协作。不同 Agent 可以专注于不同能力：规划、执行、验证。Agent 之间通过共享状态进行通信和协调。

Claude Code Teams 实现了类似团队的协作能力。核心机制是共享状态文件（shared.json）：
- 每次 heartbeat 检查共享状态，获取最新任务信息
- Agent 可以 claim 开放的任务，基于 assignee_hint 优先级分配
- CEO Agent 有全局写权限，可以 reassign、close、override 任务
- 读写规则需要明确：只能修改自己有权限的字段
- 消息系统允许 Agent 之间添加新消息进行沟通

这个模式实现了真正的并行工作，不再是单独作战。

多 Agent 架构的核心挑战是协调。单个 Agent 容易，两个以上就开始复杂——谁负责什么、谁先做谁后做、冲突了怎么办。shared.json 这个方案很聪明：用文件作为"事实来源"，不需要复杂的消息队列或共识协议。本质上是一个"状态机 + 权限控制"的简化版。

## 实战洞察

我们可以做什么：

1. **实现共享状态协调机制**：设计 shared.json 格式，定义任务结构和读写权限
2. **建立任务 claim 流程**：实现基于 heartbeat 的任务检查和 claim 逻辑
3. **添加 CEO 监督 Agent**：开发全局管理 Agent，负责任务分配和质量把控

动作：
1. 设计任务结构（Context/Plan/Output + 状态字段）
2. 实现简单的任务分配机制
3. 先从"一个 Agent 干活，另一个 Agent 审核"开始测试
