# 批量广告素材自动化 - 研究笔记

## 核心参考方案

### 1. n8n + Gemini + Nano Banana (最推荐!)
**来源**: Reddit r/n8n

**架构**:
1. **Brand Guidelines Generator**
   - 用 Firecrawl 爬网站 (homepage, about, product pages)
   - Gemini 2.5 Pro 分析并生成品牌指南文档
   - 输出: Google Doc (品牌调性、目标受众、价值主张等)

2. **Ad Variation Generator**
   - 输入: 一个 winning ad image
   - Gemini 分析原图 → 生成 10 个变体 concept
   - Nano Banana 生成实际图片
   - 输出: Google Drive

**成本**: $0.04/图, 10个 = $0.40

**关键 prompt**: 见原帖

**资源**:
- YouTube 演示: https://www.youtube.com/watch?v=eQsIHh_WDHU
- n8n workflow JSON: https://github.com/lucaswalter/n8n-ai-automations/blob/main/nano_banana_static_ad_variation_generator.json

---

### 2. instant-ugc.com
**来源**: Reddit r/Businessowners

**方案**: 上传产品照片 → AI 生成 UGC 视频
- 成本: $5/视频 (vs 以前 $600)
- 适用: 实物产品 / DTC 品牌

---

## 市面工具清单

### 视频生成
| 工具 | 特点 | 价格 |
|------|------|------|
| Funnel Ads | 快速生成视频广告,根据描述生成脚本 | - |
| Tagshop AI | AI UGC 视频,TikTok/Reels/Shorts | - |
| Runway ML | text-to-video | $15-95/月 |
| Pika Labs | 图生视频 | $10-58/月 |
| Synthesia | AI avatar | $30-90/月 |

### 图片生成
| 工具 | 特点 |
|------|------|
| AdCreative.ai | 生成高转化广告素材+copy+受众建议 |
| Pencil | 根据历史数据生成和优化广告 |
| Nano Banana | $0.04/图,图片编辑/变体生成 |
| DALL-E / Midjourney | 通用图片生成 |

### 批量自动化平台
| 工具 | 特点 |
|------|------|
| Smartly.io | 动态模板,Meta/TikTok/LinkedIn,AI预算分配 |
| Shakr | 短视频广告,一个概念生成数百变体 |
| AdGen AI | 生成式AI创建+自动调整尺寸 |
| Hunch | 本地化动态信息流,高批量定制 |
| Predis.ai | AI+UGC风格,整合调度 |
| Didoo AI | 每日生成新素材,自动测试扩展 |
| Pixelripple | 产品链接→提取卖点→生成内容 |

### 工作流自动化
| 平台 | 特点 |
|------|------|
| n8n | 开源,支持连接AI、社交平台API |
| Make.com | 可视化工作流,批量生成发布 |
| Zapier | 简单工作流 |
| Gumloop | AI自动化平台,可构建复杂工作流 |

### 文案生成
- Copy.ai / Jasper
- Predis.ai
- Make.com + ChatGPT
- n8n + AI (连接多种LLM)

### 小红书专用
- 影刀RPA — 国产自动化工具
- XHS-Auto — 小红书自动化工具
- n8n + MCP (go-rod库)
- GitHub: YYH211/xiaohongshu

---

## 典型工作流架构

```
输入源 → AI处理 → 格式适配 → 发布 → 分析
```

1. **输入**: RSS/文章/产品信息
2. **AI**: ChatGPT/Claude生成文案 + DALL-E/Midjourney生成图片
3. **适配**: 自动调整比例 (9:16 TikTok, 1:1 IG, 4:5 小红书)
4. **发布**: 定时多平台发布
5. **分析**: 汇总各平台数据

---

## 推荐组合

| 场景 | 组合 |
|------|------|
| 企业级 | Smartly.io + Adobe Creative Cloud |
| 中小团队 | Predis.ai + Zapier/Make |
| 技术团队 | n8n + ChatGPT API + 各平台MCP |
| 小红书专注 | 影刀RPA + Make/n8n + AI文案 |
| 自建(最便宜) | n8n + Gemini + Nano Banana |

---

## 关键洞察

1. **不是用AI生成完整广告,而是用它来放大变体**
   - 团队聚焦在 "0→1" 创造新概念
   - AI 负责 "1→10" 批量生成测试变体

2. **变体测试维度**:
   - 模特人种/性别/年龄
   - CTA 按钮颜色
   - Headline copy
   - 背景颜色/纹理
   - 元素位置
   - 配色方案

3. **3天交付几百组素材的可行性**:
   - 核心是自动化 + 批量生成
   - 需要好的"种子"创意(人+产品图)
   - 用 AI 扩展变体而不是从零生成
