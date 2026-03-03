# projects/
> L2 | 父级: /Users/nora/.openclaw/workspace/AGENTS.md

成员清单
AGENTS.md: `projects/` 模块地图，定义独立仓与工作区项目的统一拓扑。
REPO_TOPOLOGY.toml (位于父目录): 仓库放置策略和兼容软链接清单。
LinkCard/: 独立业务仓（card builder/mobile web）。
agentcal/: 独立业务仓（multi-agent calendar/orchestration UI）。
brand-extractor/: 独立业务仓。
eleven-tts/: 工作区项目（含本地依赖目录）。
llm-chronicles/: 工作区项目。
nora-excalidraw-drawer/: 独立业务仓。
pixel-agents-openclaw/: 独立业务仓。
rimbo-landing/: 独立业务仓。
star-office-ui/: 工作区项目（当前无独立 git 元数据）。
ai-ads-format/: 工作区项目。
ai-content-marketplace/: 工作区项目。
outbound-automation/: 工作区项目。
remotion-video-generator/: 工作区项目。
seo-automation/: 工作区项目。
ugc-ai-batch/: 工作区项目。

仓库策略
- 独立 git 仓必须统一放在 `projects/` 下，禁止散落在 `workspace/` 根层。
- `workspace/` 根层的同名路径仅允许作为兼容软链接存在。
- 用脚本校验：
  `python3 /Users/nora/.openclaw/workspace/scripts/repo_topology_guard.py --strict`

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
