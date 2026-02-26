---
title: GitHub user repo.git
type: resource
status: inbox
created_at: "2026-02-25T15:50:48.420950-05:00"
captured_date: "2026-02-25"
source_channel: "📦-资源"
source_sender: "Friday"
message_id: "1476090488200233054"
original_url: "https://github.com/user/repo.git"
source_title: "GitHub user repo.git"
source_author: ""
published_at: ""
tags: [resource, discord, search-backfill]
---

# GitHub user repo.git

## Source
- URL: https://github.com/user/repo.git
- Captured from: 2026-02-25 | 📦-资源 | Friday
- Message ID: 1476090488200233054

## Captured Context
> **场景 C：PR Review**
```bash
# 克隆到临时目录
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
exec pty:true workdir:$REVIEW_DIR command:"codex review --base origin/main"
```

## Classification
- Category: Code
- Subtype: GitHub
## Auto Summary

### Content Summary
- 当前自动抓取正文失败或内容质量不足，暂未形成可靠摘要。
- 已保留来源链接，后续会重试抓取并补齐关键结论。

### Links
- Primary: https://github.com/user/repo.git

### What We Can Do
- 当前源站不可达；先基于上下文推进事项，后续由流水线自动二次抓取补全。
- 将本条内容关联到一个具体项目，避免资源笔记孤立。
