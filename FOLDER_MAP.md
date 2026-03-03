# Workspace Folder Map

> 目标：让每个 folder 的职责一眼可见，避免混放和误改。

核心控制层
- `.openclaw/`: 调度与执行控制脚本（dispatch、state、run artifacts）。
- `scripts/`: 治理与自动化脚本（审计、拓扑守卫、同步流程）。
- `config/`: 本地配置文件，不放业务逻辑。

知识与记忆层
- `obsidian/`: Canonical 知识库（Resources / Areas / Social）。
- `knowledge/`: 模板与知识流程规范。
- `memory/`: 会话记忆与共享状态日志。
- `research/`: 研究记录。
- `proposals/`: 提案文档。
- `reflections/`: 复盘模板与归档。

能力层
- `skills/`: 可加载能力包（每个技能以 `SKILL.md` 为入口）。
- `pingping/`: pingping bot 中枢协议层（Memory -> Swarm -> Obsidian -> Memory 闭环定义与知识资产）。

项目层
- `projects/`: 独立项目仓的规范根目录。
- `agentcal`, `nora-excalidraw-drawer`, `pixel-agents-openclaw`, `rimbo-landing`, `star-office-ui`: 指向 `projects/*` 的兼容软链接。

媒体与临时产物
- `video gen/`: 成片输出目录（仅视频，不放源码）。
- `*.png/*.jpg/*.mp4/*.json`（根层零散文件）: 历史产物，建议逐步迁入对应目录。

Obsidian 兼容软链接
- `Areas -> obsidian/Areas`
- `Resources -> obsidian/Resources`
- `Social -> obsidian/Social`
- `Inbox -> obsidian/Inbox`（保留兼容）
- `Archives -> obsidian/Archives`（保留兼容）
