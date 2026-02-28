---
type: resource
status: inbox
created_at: "2026-02-27"
captured_date: "2026-02-27"
source_channel: "📦-资源"
source_sender: "yixiaohe"
message_id: ""
original_url: "https://clawhub.com/skills/seedance-cog"
source_title: "Seedance Cog - 视频生成 Skill"
source_author: "ClawHub"
tags: [video, ai-video, seedance, cellcog, bytetdance, openclaw]
---

# Seedance × CellCog：字节视频生成 + 多Agent编排

## Source
- Main URL: https://clawhub.com/skills/seedance-cog

## 内容摘要

1. **Seedance 是字节旗下最强的 AI 视频生成模型**，主打电影级 1080p 物理真实感 motion
2. **CellCog 是多 Agent 编排框架**，负责脚本、语音、配音、口型、音乐、剪辑全流程
3. **两者结合可以实现"一句话生成完整视频"**，不只是片段，而是完整成品
4. **安装方式**：需要先装 cellcog skill (`clawhub install cellcog`)
5. **调用方式**：通过 client.create_chat 传入 prompt，支持 notify_session_key 回调
6. **支持的视频类型很广**：营销视频、产品演示、品牌故事、解释视频、短片、音乐视频、主持人视频、培训视频等
7. **视频规格**：最高 1080p，3秒到4分钟，支持写实/电影/动漫/纪实等多种风格
8. **生成质量取决于 prompt 描述的详细程度**，建议包含场景、情绪、音乐偏好、人物描述
9. **6-7 个基础模型协同工作**：Seedance + LLM脚本 + TTS + 口型同步 + 音乐生成 + 自动剪辑
10. **输出格式为 MP4**，自带语音、背景音乐、音效
11. **对比竞品（Runway、Pika、OpenAI Sora）**，Seedance 在动作自然度和画面质量上有优势

## 我们可以做什么

1. **去 xskill.ai 注册获取 500 积分测试额度**，选一个产品演示场景生成视频
2. **研究如何生成"油画风格动起来"而非真人人像**，建立自己的 prompt 模板库
3. **测试不同 prompt 风格对生成效果的影响**，记录最佳实践
4. **探索直接调用 Seedance API 而非通过 CellCog**，评估成本和灵活性
5. **评估产出质量是否达到"可对外"水平**，决定是否用于 LinkCard 营销
