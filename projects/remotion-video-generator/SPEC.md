# Remotion Video Generator Skill - 终极规格文档

## 设计原则
**必须融入 taste-skill 的设计规范：**
- DESIGN_VARIANCE: 8 (非对称艺术感)
- MOTION_INTENSITY: 6 (流畅动画)
- VISUAL_DENSITY: 4 (呼吸感空间)

**禁止 AI 设计痕迹：**
- 禁止 Inter 字体 → 用 Geist / Satoshi / Outfit
- 禁止紫色发光 → 用 Zinc + 单一强调色
- 禁止居中 Hero → 用非对称布局
- 禁止 3 列等宽卡片 → 用 Bento Grid

---

## 核心特性

### 1. 模板系统
- **模板分类**：b2b-showcase, social-ads, product-launch, explainer, testimonial, event-promo
- **模板数量**：至少 20+ 高质量模板
- **模板结构**：
  - variables（可替换变量）
  - scenes（场景序列）
  - animations（动画预设库）
  - brandPresets（一键品牌主题）

### 2. 品牌主题系统
预设品牌主题（开箱即用）：
- corporate-blue（企业蓝）
- startup-gradient（创业紫）
- luxury-gold（奢侈金）
- dark-tech（暗黑科技）
- minimal-white（极简白）
- vibrant-pop（活力撞色）
- retro-wave（复古波）
- nature-green（自然绿）

每个主题包含：
- primaryColor / secondaryColor / accentColor
- backgroundColor / textColor
- headingFont / bodyFont
- borderRadius / shadowStyle

### 3. AI 生成
- 输入标题/描述 → 自动生成视频内容
- 支持 Opus 4.6 / Claude / Gemini
- 生成 prompt 模板库

### 4. 实时预览
- 变量修改即时反映
- 播放/暂停/改速度
- 帧精确跳转

### 5. 导出
- MP4 1080p/4K
- GIF
- 社交媒体格式（9:16, 16:9, 1:1）

---

## Skill 结构

```
remotion-video-generator/
├── SKILL.md                    ← 主入口
├── SPEC.md                     ← 本规格文档
├── templates/
│   ├── schema.json             ← JSON Schema
│   └── examples/
│       ├── b2b-showcase.json
│       ├── social-ads.json
│       ├── product-launch.json
│       ├── explainer.json
│       ├── testimonial.json
│       └── event-promo.json
├── themes/
│   ├── corporate-blue.json
│   ├── startup-gradient.json
│   ├── luxury-gold.json
│   ├── dark-tech.json
│   ├── minimal-white.json
│   ├── vibrant-pop.json
│   ├── retro-wave.json
│   └── nature-green.json
├── prompts/
│   ├── video-generation.json   ← AI 生成 prompt
│   └── scene-templates.json    ← Scene 模板库
├── webapp/                     ← Next.js 模板项目
│   ├── components/
│   ├── hooks/
│   ├── styles/
│   └── lib/
└── README.md
```

---

## 模板规格

### 必需字段
```json
{
  "id": "template-id",
  "name": "模板名称",
  "category": "b2b-showcase",
  "description": "模板描述",
  "resolution": { "width": 1920, "height": 1080 },
  "fps": 30,
  "duration": 15,
  
  "variables": {
    "变量名": {
      "type": "text|color|image|font",
      "default": "默认值",
      "label": "显示名称",
      "description": "描述"
    }
  },
  
  "scenes": [
    {
      "id": "scene-id",
      "name": "场景名",
      "duration": 60,
      "animation": "fadeSlideUp",
      "elements": [...]
    }
  ],
  
  "animations": {
    "fadeSlideUp": {
      "type": "spring|ease|linear",
      "from": { "opacity": 0, "translateY": 28 },
      "to": { "opacity": 1, "translateY": 0 },
      "config": { "damping": 18, "stiffness": 120 }
    }
  },
  
  "brandPresets": { ... }
}
```

---

## 主题规格

```json
{
  "id": "corporate-blue",
  "name": "企业蓝",
  "colors": {
    "primary": "#0066FF",
    "secondary": "#0044CC",
    "accent": "#00CCFF",
    "background": "#0A0A0F",
    "surface": "#16161D",
    "text": "#FFFFFF",
    "textMuted": "#A0A0B0"
  },
  "fonts": {
    "heading": "Inter",
    "body": "Inter",
    "mono": "JetBrains Mono"
  },
  "spacing": {
    "borderRadius": 8,
    "padding": 24
  },
  "effects": {
    "shadow": "0 4px 24px rgba(0,102,255,0.15)",
    "glow": "0 0 40px rgba(0,102,255,0.3)"
  }
}
```

---

## 场景库

每个模板包含 3-10 个可组合场景：

| 场景 | 用途 |
|------|------|
| intro | 开场 logo + 标题 |
| hero | 主标题 + 副标题 |
| feature | 功能/产品展示 |
| benefit | 优势/收益 |
| testimonial | 用户评价 |
| cta | 行动号召 |
| outro | 结束 + 联系方式 |

---

## 使用流程

### 方式 1：Skill 初始化
```
用户：我要做一个产品介绍视频
Skill：选择模板 → 填写变量 → 预览 → 导出
```

### 方式 2：AI 生成
```
用户：帮我做一个 AI 工具的推广视频
Skill：分析需求 → 选择模板 → AI 填充内容 → 用户确认 → 预览
```

### 3：品牌换肤
```
用户：换个紫色主题
Skill：一键切换 → 所有颜色/字体跟着变
```

---

## UI 设计要求

- **风格**：Gamma / Linear 风格，暗色主题为主
- **交互**：丝滑流畅，0 延迟感
- **动画**：所有交互都有微动画反馈
- **字体**：Inter / Geist / Satoshi
- **圆角**：8-16px
- **阴影**：柔和彩色发光

---

## 验收标准

1. ✅ 模板可正常加载和渲染
2. ✅ 变量修改即时反映
3. ✅ 品牌主题一键切换生效
4. ✅ AI 生成内容合理
5. ✅ 导出视频清晰流畅
6. ✅ 20+ 模板可用
7. ✅ 8+ 品牌主题可用
8. ✅ Skill 一键安装即用
