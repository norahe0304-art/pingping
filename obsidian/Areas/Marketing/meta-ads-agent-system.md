# Meta Ads Agent System (Stefan Luttik)

> AI Agent 系统实现 Meta Ads 自动化，替代手动创意流程

## 核心架构

### 1. Paid Media Lead Agent
- 直接连接 Meta Ads API
- 拉取实时广告系列数据
- 内置 A/B 测试评估技能
- 内置创意疲劳检测技能
- 发现表现不佳广告时，自动生成 performance brief 并传递给 Creative Director

### 2. Creative Director Agent
- 接收 brief 后，从 9,900+ prompt 模板库中选择
- 通过 NanoBanana 生成静态广告图片
- 通过 Remotion 生成视频广告变体
- 内置营销心理学技能
- 内置视觉设计质量检查技能

### 3. 上传准备
- 创意准备好后，返回给 Paid Media Lead 进行上传准备
- 所有内容需经人工审批后才能上线

## 效率对比

| 环节 | 传统方式 | Agent 系统 |
|------|---------|-----------|
| 报告拉取 | 人工 | 自动 |
| 创意 brief | 人工撰写 | 自动生成 |
| 设计排期 | 天/周 | 分钟级 |
| 决策依据 | 直觉 | 实际表现数据 |

## 关键洞察

- AI Agent 是"队友"而非单纯工具
- 能协作、交接工作、闭环
- 决策基于真实数据，而非猜测
- 在 Claude Code 中构建

## 来源

- LinkedIn: stefanluttik
- 日期: 2026-03-04
