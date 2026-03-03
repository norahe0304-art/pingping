---
title: Vibe Coding 10问 - AI生成代码后必问
source: The Neuron
original_url: https://www.theneuron.ai/explainer-articles/10-vibe-coding-questions-beginners-dont-know-to-ask-but-should/
date: 2026-02
tags: [tutorial, vibe-coding, AI, 安全]
---

# Vibe Coding 10问

## 核心观点
AI生成代码能跑 ≠ 代码安全。Veracode发现AI代码45%存在安全漏洞，Stanford研究显示用AI助手写的代码反而更不安全且更自信。

## 10个必问问题

### 1. 把我当成值班工程师来解释差异
Prompt: "总结改了什么、行为变了什么、什么会坏"

### 2. 代码做了什么假设？哪些没测过？
Prompt: "列出关于输入、顺序、时间、环境、外部服务的假设"

### 3. 这个改动的信任边界和威胁模型是什么？
Prompt: "入口点、角色、资产、攻击方式、缓解措施"

### 4. 展示每个端点/任务的认证授权规则
Prompt: "标记任何缺少服务端强制的路由"

### 5. 追踪不受信任的输入到敏感终点
Prompt: "DB写入、shell、模板、反序列化、HTML输出——展示路径"

### 6. 我们接触什么敏感数据？去哪里了？
Prompt: "收集/存储/返回/日志的字段；highlight过度收集和日志泄露"

### 7. 展示失败行为
Prompt: "超时、重试/退避、熔断——当X挂掉会发生什么？"

### 8. 生成测试证明核心承诺
Prompt: "快乐路径 + 主要边界情况 + 每个信任边界的恶意输入测试"

### 9. 找可维护性债务
Prompt: "建议复用/重构；识别可移除的新依赖"

### 10. 能安全部署/观察/回滚吗？
Prompt: "环境变量验证、迁移安全、日志/指标存在、回滚步骤文档化"

## 5问压缩版
1. 我理解它吗？
2. 它能被滥用吗？
3. 现实会打破它吗？
4. 负载会熔断吗？
5. 能安全跑吗？
