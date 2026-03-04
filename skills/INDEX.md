# Skills Index

## Local Workspace Skills
- (moved) workspace 不再存放技能实体目录，仅保留索引与分类入口。

## Global Skills (marketing)
- root: /Users/nora/.openclaw/skills
- index: /Users/nora/.openclaw/skills/index.json

## Unified Runtime Index
- primary: /Users/nora/.openclaw/skills/index.json
- compat copy: /Users/nora/.openclaw/workspace/skills/index.json
- compat copy: /Users/nora/.agents/skills/index.json
- generate: `bash /Users/nora/.openclaw/workspace/generate-skill-index.sh`

## Global Skills (codex)
- root: /Users/nora/.codex/skills

## Maintenance Rule
- Keep all OpenClaw-local skills in ~/.openclaw/skills.
- PingPing 运行时不依赖 ~/.codex/skills；技能发现只走 ~/.openclaw/skills。
