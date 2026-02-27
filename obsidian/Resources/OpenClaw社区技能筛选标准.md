---
type: resource
status: inbox
created_at: "2026-02-26T12:27:06.651910-05:00"
captured_date: "2026-02-22"
source_channel: "📦-资源"
source_sender: "bravohenry"
message_id: "1475335797585608899"
original_url: "https://x.com/GoSailGlobal/status/2025402533972480275?s=20"
source_title: "X 推文洞察"
tags: [resource, discord]
---

# X 推文洞察

## Source
- Main URL: https://x.com/GoSailGlobal/status/2025402533972480275?s=20

## 核心要点

这是一次对 OpenClaw Skills 的深度调研，分析了从 ClawHub 5705 个 Skills 筛选到 3002 个的逻辑。排除率接近 48%，筛选标准值得研究。

排除的 2748 个 Skills 按原因分类：

1. **垃圾与低质量内容**（43%）：批量账户创建的测试 Skills、未正式发布的开发代码、功能相同但反复提交的重复版本。这个问题在开源生态不可避免，但 OpenClaw 社区选择了主动清理。

2. **加密与金融交易类**（24%）：所有虚拟货币、区块链、金融交易和投资工具被整体排除。这不是技术问题，而是风险规避——AI Agent 可以自主执行操作时，金融类工具天然带有更高的责任风险。

3. **功能重复**（18%）：当多个 Skills 实现相同功能时，保留更新最活跃或功能最完整的版本。这解决了选择困难问题。

这给我们的启示是：不是所有skill都值得用——质量比数量重要。对于金融类工具，尤其要谨慎。

## 实战洞察

动作：
1. 建立自己的"Skill 评估 checklist"
2. 金融类工具使用前必须人工审核
3. 定期清理长期不用的 Skills
