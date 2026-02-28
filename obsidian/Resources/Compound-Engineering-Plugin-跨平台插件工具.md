---
original_url: https://github.com/EveryInc/compound-engineering-plugin
source_title: Compound Engineering Plugin
source_author: EveryInc
published_at: 2025-10-09
tags: [ai-coding, plugin, workflow, claude-code, opencode, codex]
---

# Claude Code 插件跨平台工具

## 内容摘要

- **核心功能**：Claude Code 插件市场 + 跨平台转换器
- **插件翻译**：写一次 Claude Code 插件，可自动转成 OpenCode、Codex、Cursor、Pi、Gemini CLI、GitHub Copilot、Kiro 等格式
- **工作流理念**：Plan → Work → Review → Compound → Repeat，每次循环让下次更容易
- **4 个核心命令**：
  - `/workflows:plan`：把功能想法变成详细实现计划
  - `/workflows:work`：用 worktree 执行计划，跟踪任务进度
  - `/workflows:review`：多 AI 代码审查
  - `/workflows:compound`：把经验写成文档供下次复用
- **核心理念**：每次工程工作应该让后续工作更容易，而不是更难
- **数据**：9663 stars，767 forks，MIT 许可证
- **安装**：Claude Code 用 `/plugin marketplace add`，其他平台用 `bunx @every-env/compound-plugin install`

## 我们可以做什么

- **30X 插件跨平台**：参考这个思路，把 OpenClaw 的 skill 转换成其他平台可用格式
- **工作流标准化**：借鉴 Plan→Work→Review→Compound 流程规范团队开发
- **插件市场思路**：做自己的插件库，积累可复用工具
- **Sync 个人配置**：用 `bunx @every-env/compound-plugin sync` 把 Claude Code 配置同步到其他工具
