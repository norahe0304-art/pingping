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
- 该条资源当前无法稳定抓取正文，已保留来源链接并等待下次自动补抓。
- 建议先把这条资源归档到对应项目，再补正文事实。

### Links
- Primary: https://github.com/user/repo.git
- Related: https://github.githubassets.com
- Related: https://avatars.githubusercontent.com
- Related: https://github-cloud.s3.amazonaws.com
- Related: https://user-images.githubusercontent.com/
- Related: https://github.githubassets.com/assets/global-banner-disable-8a300af6d815087d.js

### What We Can Do
- 当前源站不可达；先基于上下文推进事项，后续由流水线自动二次抓取补全。
- 把本条内容转成一个可执行任务：owner、截止时间、下一步动作。
