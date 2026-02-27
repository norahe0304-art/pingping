# webapp/
> L2 | 父级: /Users/nora/.openclaw/workspace/skills/remotion-video-generator/SKILL.md

成员清单
src/app/layout.tsx: Next.js 根布局，注入全局样式与文档壳。
src/app/page.tsx: 主交互页面，承载脚本输入、TTS 预览与执行建议。
src/app/api/tts/route.ts: 服务端 TTS 代理接口，封装上游凭据与错误处理。
src/app/globals.css: 全局视觉系统，提供 taste-skill 风格基础样式。

法则
- 禁止回到对称中轴 hero；保持非对称信息层次。
- 字体使用 Outfit/Satoshi/Geist 体系，禁用 Inter。
- UI 改动必须保证移动端与桌面端都可用。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
