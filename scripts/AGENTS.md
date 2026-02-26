# scripts/
> L2 | 父级: /Users/nora/.openclaw/workspace/AGENTS.md

成员清单
check-silence-and-save-memory.sh: 触发静默检测并写入 memory/shared 静默记录。
check_discord_silence.py: 读取 Discord 最近消息并判断频道是否静默。
sync_discord_feed_to_daily_memory.py: 将 shared discord-feed 增量摘要同步到 memory/shared/YYYY-MM-DD-discord-daily.md（不再写个人日记，按日期 state 去重）。
sync_discord_feed_urls_to_resources.py: 将 shared discord-feed 中 URL 增量落盘到 obsidian/Resources/ 并用 state 去重。
check_gmail_important.py: 增量读取 Gmail 未读邮件并按规则打分，写入 memory/shared/gmail-watch 与 state。
md2pdf.py: Markdown 转 PDF 的主入口。
md2pdf.sh: PDF 转换 shell 包装脚本。
md2pdf_apple.py: macOS 渲染兼容版本。
md2pdf_clean.py: 轻量清洗版 Markdown->PDF。
md2pdf_pro.py: 增强排版版 Markdown->PDF。
md2pdf_v2.py: 第二版转换实现。

法则
- 同步类脚本必须幂等：重复执行不能重复写入。
- 所有状态文件必须放在 memory/ 或 memory/shared/ 下，不能散落。
- 新增脚本时必须补充本文件成员清单与职责。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
