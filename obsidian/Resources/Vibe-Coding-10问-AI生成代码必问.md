---
title: "AI生成代码后必问的10个安全问题"
type: Resource
original_url: https://www.theneuron.ai/explainer-articles/10-vibe-coding-questions-beginners-dont-know-to-ask-but-should/
source_title: "10 Vital Questions Vibe Coders Must Ask Before Shipping"
source_author: The Neuron
published_at: "2026-02"
captured_date: "2026-03-03"
source_channel: "📦-资源"
source_sender: ""
message_id: ""
tags: [vibe-coding, AI编程, 安全, 代码审查, 质量保证]
---

# AI生成代码后必问的10个安全问题

## 内容摘要

1. **核心警告**：AI生成代码能跑≠安全，Veracode数据显示45%的AI代码存在安全漏洞
2. **过度自信问题**：Stanford研究显示用AI助手写的代码反而更不安全且更自信
3. **问题1-差异解释**：让AI解释改了什么、行为变了什么、什么会坏
4. **问题2-隐藏假设**：列出代码关于输入、顺序、时间、环境、外部服务的假设
5. **问题3-威胁建模**：明确入口点、角色、资产、攻击方式和缓解措施
6. **问题4-认证授权**：检查每个端点的认证授权规则，标记缺失的路由
7. **问题5-数据追踪**：追踪不受信任输入到敏感终点的路径（DB写入、shell、模板等）
8. **问题6-敏感数据**：明确收集/存储/返回/日志的字段，识别过度收集
9. **问题7-失败行为**：展示超时、重试、退避、熔断机制
10. **问题8-测试证明**：生成测试覆盖快乐路径、边界情况、恶意输入
11. **问题9-可维护性债务**：建议复用/重构，识别可移除的新依赖
12. **问题10-部署安全**：环境变量验证、迁移安全、日志/指标存在、回滚步骤

## 我们可以做什么

1. **制作Prompt模板**：把10个问题做成标准Prompt，在AI编程时必问
2. **加入Code Review流程**：在v0/Claude Code生成后必问这10个问题
3. **建立安全清单**：创建团队级Vibe Coding安全检查清单
4. **5问压缩版**：紧急情况问5个核心问题——我理解它吗？它能被滥用吗？现实会打破它吗？负载会熔断吗？能安全跑吗？
5. **自动化测试**：生成测试覆盖快乐路径+边界情况+每个信任边界的恶意输入
