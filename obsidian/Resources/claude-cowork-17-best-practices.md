---
title: Claude Cowork 17 Best Practices
tags: [AI, workflow, productivity, setup, context]
source: https://x.com/heynavtoor/status/2028148844891152554
author: Nav Toor
date: 2026-03-01
---

# Claude Cowork 17 Best Practices

> 核心：投资 setup，减少 prompting。ChatGPT 奖励 prompt engineering，Cowork 奖励 system engineering。

## Part 1: 上下文架构 (1-5)

1. **建 _MANIFEST.md** - 三层结构：Canonical / Domain / Archival
2. **Global Instructions** - 永久操作系统
3. **三个持久上下文文件** - about-me.md、brand-voice.md、working-style.md
4. **Folder Instructions** - 项目级上下文
5. **有意识地控制读取范围** - 别让 Claude 读全部

## Part 2: 任务设计 (6-10)

6. 定义 end state，而不是步骤
7. 执行前先 show plan
8. 告诉 Claude 不确定时怎么做
9. 批量相关任务放一个 session
10. 用 subagent 并行处理

## Part 3: 自动化 (11-13)

11. 用 /schedule 定时任务
12. 一次构建，多次运行 - 外置到文件
13. /schedule + connectors 组合实现真自动化

## Part 4: 插件和 skills (14-16)

14. 组合插件
15. 为特定工作流建 custom skills
16. 用 Plugin Management 插件对话式构建插件

## Part 5: 安全 (17)

17. 把 Cowork 当成强大的员工，不是玩具

---

## 对 OpenClaw/Swarm 的价值

这些 practice 很多可以直接用到 OpenClaw/Swarm：
- _MANIFEST.md、Global Instructions、context files → 我们已经在做
- 定义 end state → 对应任务设计
- 定时任务 + 外置文件 → 类似 cron + skills
- Custom skills → 正是我们沉淀的方向

**印证了我们之前的做法方向是对的。**
