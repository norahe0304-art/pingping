# Obsidian SOP
> Purpose: capture high-value knowledge from DM/Discord into a durable vault structure.

## Vault Structure
- Projects/
- Areas/
- Resources/
- Archives/
- Social/LinkedIn/
- Social/小红书/
- Social/X/
- Inbox/

## Capture Flow
1. Fast capture to Inbox first.
2. Daily triage from Inbox into target folders.
3. Prefer updating existing note over creating duplicates.
4. Dedup by source_ref (message_id/url) + title similarity.

## High-Value Trigger (Any One)
- Clear decision
- Executable next action
- Reusable method/template
- High-value resource link
- Project milestone/change

## Classification Decision Tree (Mandatory)
1. If note has goal + actionable tasks + due/priority => type=project => Projects/
2. If note is reusable principle/framework/template (no active execution) => type=area => Areas/
3. If note is a learning link/material from DM/Discord/web => type=resource => Resources/
4. If note is publish draft/asset => type=social => Social/<platform>/
5. If project completed/inactive => type=archive => Archives/

Rule: when uncertain between Projects and Areas, choose Projects first.

## Routing Rules
- Projects/: active items with owner/status/next_action.
- Areas/: reusable principles and playbooks only.
- Resources/: learning links/materials from DM + resource channel.
- Social/: publish drafts and assets by platform.
- Archives/: completed/inactive projects.

## Required Frontmatter (Mandatory)
---
title:
date:
type: project|area|resource|archive|social
source_type: discord|dm|web
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

Validation constraints:
- type=project -> status/owner/next_action/due required
- type=area -> next_action and due should be empty
- source_ref must be present when source_type is discord/dm/web

## Note Body Minimum
- 3-line summary
- Why it matters (1-3 bullets)
- Next action (optional for non-project notes)
- Related links/context

## File Naming
- Projects/<project-name>.md
- Areas/<topic>.md
- Resources/YYYY-MM-DD-<short-title>.md
- Social/<platform>/YYYY-MM-DD-<topic>.md
- Archives/<project-name>-archive.md
- Inbox/YYYY-MM-DD-HHMM-<short-title>.md

## Boundaries with Existing Memory
- MemOS: semantic long-term recall layer.
- memory/YYYY-MM-DD.md: DM/personal timeline layer.
- memory/shared/YYYY-MM-DD-discord-feed.md: channel event stream.
- Obsidian vault: curated knowledge layer.

## Daily Job (21:30 local)
- Empty Inbox by routing all items.
- Output daily digest:
  - new notes count
  - updated notes count
  - top 3 important captures
  - suggested next actions

## Daily Classification Audit (Recommended)
- Scan Areas/ for project-like signals (status/next_action/due/priority).
- If found, move to Projects/ and convert type=project.
- Optionally extract reusable method summary to Areas/ as a separate note.
- Report moved files + changed fields.

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md


## Resource Note Depth Standard (Mandatory)
For notes under Resources/, do not write shallow summaries.

Minimum required sections:
1. Source metadata
- original_url
- source_title/source_author/published_at

2. Core content extraction
- 8-12 detailed bullets OR sectioned summary by article structure
- include concrete claims, data points, methods, and constraints

3. Key evidence / quotes
- at least 3 short quotes or precise evidence snippets with context

4. Nora-oriented value
- 3-5 actionable takeaways
- 1 suggested next action with expected outcome

Invalid note examples:
- "字体、配色、布局" only
- generic one-paragraph recap without source link

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
