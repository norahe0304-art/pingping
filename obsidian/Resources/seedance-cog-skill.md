---
title: Seedance Cog - 视频生成 Skill
type: resource
source: ClawHub
original_url: https://clawhub.com/skills/seedance-cog
tags: [video, ai-video, seedance, cellcog, bytedance]
last_updated: 2026-02-27
---

# Seedance Cog - Seedance × CellCog

**Seedance × CellCog.** ByteDance's #1 video model meets the frontier of multi-agent coordination.

Seedance generates the smoothest motion in AI video — cinematic 1080p with physics that look real. CellCog orchestrates it with scripting, voice synthesis, lipsync, scoring, and editing to produce complete videos from a single prompt. Not just clips — full productions.

---

## Prerequisites

需要安装 cellcog skill：
```bash
clawhub install cellcog
```

Quick pattern (v1.0+):
```python
result = client.create_chat(
    prompt="[your video request]",
    notify_session_key="agent:main:main",
    task_label="video-task",
    chat_mode="agent"
)
```

---

## What You Can Create

### Marketing Videos
- **Product Demos**: "Create a 60-second product demo video for our project management app"
- **Brand Videos**: "Create a 30-second brand story video for a sustainable fashion startup"
- **Social Ads**: "Create a 15-second Instagram ad for our new coffee blend"

### Explainer Videos
- **Product Explainers**: "Create a 90-second explainer for how our API works"
- **Concept Videos**: "Create a video explaining blockchain in simple terms"

### Cinematic Content
- **Short Films**: "Create a 2-minute short film about a robot discovering nature"
- **Music Videos**: "Create a cinematic music video with dramatic landscapes"

### Spokesperson Videos
- **News Reports**: "Create a news-style report on recent AI developments"
- **Training Videos**: "Create a training video with a presenter explaining safety protocols"

---

## CellCog Video Orchestration

```
Script Writing → Scene Planning → Frame Generation → Voice Synthesis
     → Lipsync → Background Music → Sound Design → Editing → Final Output
```

**6-7 foundation models** work together:
- Seedance for video generation
- Frontier LLMs for scripting
- TTS models for voice synthesis
- Lipsync models for speaker alignment
- Music generation for scoring
- Automated editing

---

## Video Specifications

| Spec | Details |
|------|---------|
| **Resolution** | Up to 1080p |
| **Duration** | 3 seconds to 4 minutes |
| **Styles** | Photorealistic, cinematic, anime, stylized, documentary |
| **Audio** | Voice synthesis, background music, sound effects |
| **Output** | MP4 |

---

## Tips for Better Videos

1. **Describe the story**: "A video about our app" → "A 60-second video showing a stressed founder discovering our app, their workflow transforming, ending with them confidently presenting to investors"

2. **Specify duration**: "30-second social ad" vs. "2-minute explainer"

3. **Set the mood**: "Upbeat and energetic", "calm and professional", "dramatic and cinematic"

4. **Mention music preferences**: "Uplifting corporate background", "lo-fi beats", "cinematic orchestral"

5. **For spokesperson videos**: Describe the presenter's appearance and tone of voice

---

## 🎯 我们的改进方向

- [ ] 研究如何生成"油画风格动起来"而非真人人像
- [ ] 测试不同 prompt 风格对生成效果的影响
- [ ] 探索直接调用 Seedance API 而非通过 CellCog
- [ ] 建立自己的 prompt 模板库
