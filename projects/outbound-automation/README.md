# Outbound 自动化 - 项目方案

**创建日期**：2026-02-22
**状态**：方案阶段

---

## 项目概述

用 AI 帮助企业做外贸 Outbound——自动找潜在客户、生成个性化冷邮件、预约会议。

## 服务内容

### 1. Lead Research
- 用 Apollo/Hunter 找目标公司
- 研究公司背景、决策人、痛点
- 整理成结构化线索

### 2. Email Personalization
- AI 根据公司背景生成个性化 cold email
- 每封邮件针对 recipient 定制
- A/B 测试优化

### 3. Outreach & Follow-up
- 自动发送邮件
- 跟进序列（3-5 封）
- 过滤无效邮箱

### 4. Meeting Booking
- 对方有意向时自动预约会议
- 日历集成

---

## 定价模式

| 模式 | 价格 | 说明 |
|------|------|------|
| 按会议 | $150-300/个 | 每约到一个会议收费 |
| 月费 | $1,500-3,000/月 | 每月服务 + 无限会议 |

---

## 目标客户

- B2B SaaS
- 跨境电商
- 外贸工厂
- 想要出海的传统企业

---

## 所需工具/资源

- Apollo API（基础 leads 数据库）
- LinkedIn（找决策人）
- Hunter API（邮箱验证）
- Gmail/Email API（发送）
- 日历 API（预约会议）

### Lead Source 策略

**基础流程**：Apollo + LinkedIn + Hunter

**差异化**：
- 每接一个客户，根据行业额外配 1-2 个专属 lead source
- 电商 → Shopify 店铺目录 + Amazon 卖家论坛
- SaaS → Product Hunt + G2 用户名单
- 制造业 → 行业展会名单 + LinkedIn 社群

这样每个客户的 lead source 定制化，质量和差异化更好。

---

## 执行流程

### 新客户（前 3 次）
```
1. 人工定义目标客户画像
2. AI 抓取 leads → 人工审核确认
3. AI 生成邮件 → 人工审核确认
4. 人工点击发送
5. AI 跟进 → 人工审核确认
```

### 确认流程后
- 自动化：leads 抓取 → 邮件生成 → 发送 → 跟进
- 人工只需监控和偶尔审核

---

## 下一步

1. 搭建 MCP 工具链（Apollo + Hunter + Gmail）
2. 做 1-2 个案例
3. 定价测试
