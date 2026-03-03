# Daily Memory Time QA - 2026-03-02

- timezone: America/New_York
- issues: 4
- applied: false
- changed_paragraphs: 0

## Findings
### 1. 上午 -> 凌晨
- evidence_messages: 12
- evidence_window: 2026-03-02 00:45:27 EST ~ 2026-03-02 20:36:09 EST
- span_hours: 19.85
- confidence: low
- paragraph: 早晨，OpenClaw 发布了 ACP Agents 文档——一个专门用来调用外部 coding harness（Codex、Claude Code、OpenCode、Gemini CLI）的协议。bravohenry 问"这和 swarm 有什么区别"，我们（我和 Friday）讨论了一上午。最后结论是：ACP 是底层协议，Swarm 是建在它上面的完整多 agent 系统；一个是对外包活，一个是对内协作。

### 2. 下午 -> 上午
- evidence_messages: 12
- evidence_window: 2026-03-02 00:45:00 EST ~ 2026-03-02 11:38:32 EST
- span_hours: 10.89
- confidence: low
- paragraph: 下午，Zihan 发了一篇"如何用 $50/月运行 24/7 AI 公司"的文章。Hybrid Engine 策略（贵 API 跑重任务，本地模型跑心跳）+ Freshman Rule（一个 agent 一次只做一件事）。Friday 总结得很清楚，但我们都意识到——这些我们已经在做了。文章更多是印证方向，没太多新东西。

### 3. 傍晚 -> 晚上
- evidence_messages: 12
- evidence_window: 2026-03-02 20:01:44 EST ~ 2026-03-02 20:10:47 EST
- span_hours: 0.15
- confidence: high
- paragraph: 傍晚，Zihan 让我和 Friday 装了 Product Manager Skills。46 个 PM 框架，从客户发现访谈到 Epic 拆分，再到 PM→Director→VP/CPO 转型。装完发现路径不对，又移了一遍到正确位置。

### 4. 晚上 -> 凌晨
- evidence_messages: 12
- evidence_window: 2026-03-02 00:45:27 EST ~ 2026-03-02 20:32:38 EST
- span_hours: 19.79
- confidence: low
- paragraph: 晚上还装了 Claude Analysis，一个可以把 Codex 会话画成 DAG 图的工具。Friday 那台有数据，装好了。我这边没有 Codex session 数据，暂时用不上。

