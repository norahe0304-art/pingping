# Product Marketing Context

## Product
Pingping (OpenClaw Discord agent) with tool-enabled workflow and memory support.

## Core Use Cases
- Read and summarize external links (e.g., X posts/articles) in Discord channels.
- Execute coding/content tasks via tools with high-permission profile.
- Persist useful operating knowledge into memory files for later recall.

## Current Model + Channel Policy
- Primary model: openai-codex/gpt-5.3-codex
- Discord group policy: open
- allowBots: true
- requireMention: false (main guild default)

## Reliability Notes
- DM path is usually more stable than noisy channels.
- Channel tool latency can spike under heavy event load.
- Keep config edits minimal and avoid frequent reload churn.

## Success Criteria
- Channel tool calls complete reliably.
- No unresolved Discord channel bindings.
- Memory and context files are present and writable.
