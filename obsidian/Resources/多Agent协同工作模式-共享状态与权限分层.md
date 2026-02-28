---
type: resource
status: inbox
created_at: "2026-02-27"
captured_date: "2026-02-22"
source_channel: "📦-资源"
source_sender: "yixiaohe"
message_id: "1475256958666674329"
original_url: "https://x.com/0XBrianXYZ/status/2022488478953685247"
source_title: "X 推文洞察 - 多 Agent 协同"
source_author: "0XBrianXYZ"
tags: [openclaw, multi-agent, collaboration, workflow]
---

# 多 Agent 协同工作模式 - 共享状态与权限分层

## 内容摘要

1. **核心思路**：通过共享的 shared.json 文件实现多 Agent 间的状态同步和任务协调
2. **执行流程**：每个 Agent 执行前先读取最新状态，写入时只修改自己有权限的字段
3. **权限分层**：CEO（主 Agent）拥有全局写权限，可以重新分配、关闭、覆盖任何任务
4. **极简协议**："共享状态 + 权限分层"是极简的分布式协作协议
5. **无需复杂架构**：不需要复杂的消息队列或共识算法，用文件锁就能实现基本的并发控制
6. **边界划分**：Agent 协作最难的不是通信，而是"谁负责什么"的边界划分
7. **分配机制**：assignee_hint（分配暗示）和 claim（认领）机制解决了边界问题
8. **适用场景**：对一人团队略过度设计，但对多 Agent 分工场景很有价值
9. **协同模式**：不再是单独的 subagent 并行作战，而是多个 Agent 协同工作
10. **适合复杂项目的分工协作**

## 我们可以做什么

1. **尝试双 Agent 协作模式**——Pingping 先做一个改动，Nora 只批准影响最大的版本
2. **把执行拆分成两个 60 分钟内可完成的动作**，便于快速迭代
3. **建立简单任务看板**（Notion 或本地文件），记录谁在做什么
4. **记录每次协作的速度、质量和稳定性变化**，作为优化依据
5. **先从简单场景开始测试协作流程**
