# Obsidian SOP
> Purpose: keep one clean knowledge system centered on high-signal resources.

## Vault Root (Canonical)
- `/Users/nora/.openclaw/workspace/obsidian/`

## Active Folders
- `obsidian/Resources/` (primary, automatic): readable URL -> knowledge cards.
- `obsidian/Areas/` (manual/proposed): reusable SOP/framework/checklist only.
- `obsidian/Social/` (optional, manual): publish-ready output artifacts.

## Disabled by Default
- `obsidian/Projects/` is not part of the current pipeline.
- Do not auto-route resource notes into Projects.

## Resources Card Contract (Mandatory)
Every resource note must contain only these three body sections:
1. `## Source`
2. `## Key Points`
3. `## What Pingping + Nora Can Do`

Quality gate:
- `Key Points` must be 5-10 bullets.
- Summary must be understanding-level abstraction, not chat transcript dump.
- Source must keep one main URL as evidence.
- Unreadable sources are dropped, not stored.

## Areas Contract (Mandatory)
- Areas stores reusable knowledge only: SOP, playbook, framework, checklist, anti-pattern.
- No active project status/task tracking in Areas.
- New Areas entry should come from:
  - Resource pattern repeated >= 2 times, or
  - explicit Nora request to promote a method.
- Pingping can propose; Nora approves before merge.

## Canonical Flow
1. Memory pipeline writes channel facts to `memory/shared/*-discord-feed.md`.
2. Resource hook triggers on new URL events from `📦-资源` channel and compiles cards into `obsidian/Resources/`.
3. Pingping reviews resources and proposes reusable SOP candidates for `obsidian/Areas/`.
4. Nora approves/rejects Area proposals.

## Boundaries with Memory System
- MemOS: semantic recall (preferences, long-term facts).
- `memory/YYYY-MM-DD.md`: DM/personal daily memory.
- `memory/shared/*-discord-feed.md`: channel fact stream.
- Obsidian: compiled knowledge artifacts only (readable, reusable, reviewable).

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
