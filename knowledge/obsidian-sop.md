# Obsidian SOP
> Purpose: capture high-value knowledge from DM/Discord into a durable vault structure.

## Vault Root (Canonical)
- `/Users/nora/.openclaw/workspace/obsidian/`

## Vault Structure
- obsidian/Projects/
- obsidian/Areas/
- obsidian/Resources/
- obsidian/Archives/
- obsidian/Social/LinkedIn/
- obsidian/Social/小红书/
- obsidian/Social/X/
- obsidian/Inbox/

## Canonical Flow (Mandatory)
1. Capture first: write to Inbox.
2. Classify second: route to one target folder.
3. Deepen third: expand with quality standard for that folder.
4. Dedup always: prefer update existing note over creating duplicates.

## Template Mapping (Mandatory)
- obsidian/Projects/ -> `knowledge/templates/project-note-template.md`
- obsidian/Areas/ -> `knowledge/templates/area-note-template.md`
- obsidian/Resources/ -> `knowledge/templates/resource-note-template.md`
- obsidian/Archives/ -> `knowledge/templates/archive-note-template.md`
- obsidian/Social/* -> `knowledge/templates/social-note-template.md`
- obsidian/Inbox/ -> `knowledge/templates/inbox-capture-template.md`

## Classification Decision Tree (Mandatory)
1. goal + executable action + due/priority -> `type=project` -> Projects/
2. reusable principle/framework/template (non-active) -> `type=area` -> Areas/
3. external learning link/material -> `type=resource` -> Resources/
4. publish draft/asset -> `type=social` -> Social/<platform>/
5. completed/inactive project -> `type=archive` -> Archives/

Rule: when uncertain between Projects and Areas, choose Projects.

## Required Frontmatter (Mandatory)
---
title:
date:
type: project|area|resource|archive|social
source_type: discord|dm|web|internal
source_ref:
original_url:
source_title:
source_author:
published_at:
channel_or_dm:
tags: []
status: draft|active|done
owner:
next_action:
due:
priority: P0|P1|P2|P3
content_hash:
---

Validation rules:
- type=project -> status/owner/next_action/due required
- type=area -> next_action and due must stay empty
- source_type in {discord,dm,web} -> source_ref required

## Quality Floor by Section

### Projects (execution quality)
- Must include: goal, scope, milestones, active tasks, blockers, decisions.
- Minimum: 5 actionable bullets + explicit next 24h action.

### Areas (reusability quality)
- Must include: principles, framework/playbook, checklist, anti-patterns.
- Minimum: 3 principles + 1 reusable checklist.

### Resources (source quality)
- Must include: original_url + metadata + deep extraction.
- Minimum: 8-12 core bullets + 3 quotes/evidence + 3-5 takeaways.

### Archives (retrospective quality)
- Must include: outcome, what worked, what failed, lessons.
- Minimum: 2 lessons + 1 reusable asset.

### Social (publish quality)
- Must include: audience, intent, core message, draft, CTA.
- Minimum: 1 clear hook + 1 concrete example + 1 CTA.

### Inbox (capture quality)
- Must include: what happened, why it matters, suggested route.
- No polished writing needed, but route must be explicit.

## Daily Operations
- 21:30 local: Inbox triage + route all new captures.
- 21:35 local: classification audit for Areas->Projects misfiles.
- Output digest:
  - new notes count
  - updated notes count
  - moved notes count
  - top 3 captures
  - next actions

## Boundaries with Memory System
- MemOS: semantic long-term memory.
- memory/YYYY-MM-DD.md: DM/personal timeline.
- memory/shared/YYYY-MM-DD-discord-feed.md: channel event stream.
- Obsidian vault: curated knowledge + reusable artifacts.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
