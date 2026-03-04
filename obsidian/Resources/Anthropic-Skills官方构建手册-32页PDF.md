---
title: "32页官方手册：把Claude训练成你的团队成员"
type: Resource
original_url: https://www.theneuron.ai/explainer-articles/anthropic-just-dropped-a-32-page-playbook-for-teaching-claude-to-work-like-a-real-team-member/
source_title: "Anthropic Dropped a 32-Page Playbook to Teach Claude Skills"
source_author: The Neuron
published_at: "2026-02"
captured_date: "2026-03-03"
source_channel: "📦-资源"
source_sender: ""
message_id: ""
tags: [Anthropic, Claude, Skills, 官方指南, Agent-Skills]
---

# 32页官方手册：把Claude训练成你的团队成员

## 内容摘要

1. **核心问题**：每次打开新聊天都要从头解释偏好、公司风格、流程，Anthropic发布的32页手册就是解决这个痛点
2. **Skill定义**：Skill是一个文件夹，包含SKILL.md指令文件，告诉Claude如何处理特定任务，一次上传永久生效
3. **类比比喻**：MCP是厨房（工具），Skills是菜谱（步骤），有厨房没菜谱等于面对一堆电器发呆
4. **三种Skill类型**：文档资产创建、工作流自动化、MCP增强（如Sentry代码审查Skill）
5. **渐进式披露**：Claude只加载当前对话需要的指令，不让无关内容占用context window
6. **YAML frontmatter关键**：name和description（含触发短语）决定Claude何时加载该Skill
7. **Skill结构**：SKILL.md（必需）+ scripts/ + references/ + assets/（可选）
8. **构建步骤**：定义用例→写SKILL.md→测试→迭代，15-30分钟可完成
9. **五种模式**：顺序编排、多MCP协调、迭代精炼、上下文感知工具选择、领域特定智能
10. **开放标准**：Anthropic将Skills作为开放标准发布，与Asana、Canva、Figma、Sentry、Zapier等合作

## 我们可以做什么

1. **下载官方手册**：获取32页PDF原文，深入学习Skill构建方法
2. **构建个人Skill库**：按指南创建自己的常用Skill集合（如文档格式、工作流模板）
3. **使用Skill Creator**：让Claude帮你构建Skill，说"用skill-creator帮我创建一个XXX的Skill"
4. **团队级部署**：管理员可以workspace级别部署Skill，一人设置全队受益
5. **复用开源Skill**：GitHub上有Anthropic官方发布的各种Skill可定制使用
