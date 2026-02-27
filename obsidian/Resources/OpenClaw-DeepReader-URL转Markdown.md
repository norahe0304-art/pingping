---
type: Resource
original_url: https://github.com/astonysh/OpenClaw-DeepReeder
source: GitHub
source_title: OpenClaw DeepReader
source_author: astonysh
tags: [openclaw, content-reader, tool, markdown, url]
---

# DeepReader: 任意URL自动转Markdown

## 核心要点

DeepReader 是 OpenClaw 内置的内容读取器，核心功能是把任意 URL 自动抓取、清洗、保存为高质量 Markdown。零配置、零 API Key，直接可用。

支持的来源：
- X (Twitter) 帖子和线程
- Reddit 帖子
- YouTube 字幕
- 任意网页内容

自动清洗 HTML，去除广告和噪音，保存为 Markdown 格式。

这个工具对"资源沉淀"工作流特别有用。之前我们处理资源频道的链接，要么手动复制粘贴，要么用各种奇怪的工具。DeepReader 负责抓取，Agent 负责理解沉淀——整个流程可以自动化。

而且它不需要任何 API Key，这对于我们这种"能省则省"的团队来说是加分项。测试了几个来源，效果比直接爬虫好很多，尤其是去广告和噪音这块。

## 实战洞察

我们可以做什么：

1. **自动化抓取**：配合 cron，定时抓取特定来源的更新
2. **每日资讯自动抓取**：建立自动化流程，每天自动抓取行业资讯
3. **内容清洗**：利用自动清洗功能，直接获得干净的内容用于分析
4. **全自动化沉淀**：看到资源频道的链接→自动抓取→自动沉淀，形成闭环

动作：
1. 在 OpenClaw 中配置 DeepReader skill
2. 设置几个重点来源的定时抓取
3. 测试抓取质量，优化清洗规则
