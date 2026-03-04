---
name: skill-search
description: "按需搜索和读取技能。不把全部 skill 文档塞进上下文，而是按需读取。"
metadata:
  {
    "openclaw": {
      "emoji": "🔍"
    }
  }
---

<!--
[INPUT]: 依赖本地技能索引 JSON 与各技能目录下的 SKILL.md。
[OUTPUT]: 提供可执行的技能发现与读取顺序，避免盲目猜测技能存在性。
[POS]: workspace/skills 的技能发现入口协议，被 pingping 与本地 agent 复用。
[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
-->

# Skill Search - 按需搜索技能

## 核心思路
参考 Cloudflare MCP Code Mode：不给 AI 塞所有文档，而是给它搜索工具。

## 工具与路径优先级

### 1. 读索引 (替代 skill_search)
优先读取：
- `~/.openclaw/workspace/skills/index.json`（统一索引，推荐）
- `~/.agents/skills/index.json`（兼容索引）
- `~/.openclaw/skills/index.json`（全局技能索引）

如果索引不存在，先执行：
`bash ~/.openclaw/workspace/generate-skill-index.sh`

### 2. 读 Skill 文档 (替代 skill_read)
按顺序尝试：
- `~/.openclaw/workspace/skills/{skill_name}/SKILL.md`
- `~/.openclaw/skills/{skill_name}/SKILL.md`
- `~/.codex/skills/{skill_name}/SKILL.md`
- `~/.agents/skills/{skill_name}/SKILL.md`（兼容）

## 工作流程

```text
用户: "帮我发邮件"
↓
我: 读统一 index.json → 找到 "email-sequence"
↓
我: 依次尝试路径，读取 email-sequence/SKILL.md
↓
我: 根据文档执行
```

## 优势

| 塞文档进上下文 | 按需读取 |
|---|---|
| 高 token 消耗 | 低 token |
| 每次全加载 | 按需 |
| 慢 | 快 |

## 实际使用

由于我无法直接调用"函数"，我用自己的协议：

1. **不确定用哪个 skill** → 先读统一索引；没有就先生成索引
2. **确定目标 skill** → 走多路径 fallback 读取 SKILL.md
3. **若读取失败** → 明确报错并列出已尝试路径，不允许“假装 skill 不存在”
4. **执行任务** → 仅在读到 SKILL.md 后执行

这个协议让我不用每次都加载所有 skill 文档，按需取用。
