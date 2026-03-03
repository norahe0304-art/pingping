# pingping/
> L2 | 父级: /Users/nora/.openclaw/workspace/AGENTS.md

定位
- pingping 是 bot 执行与沉淀中枢，采用三层闭环：`Memory -> Swarm -> Obsidian -> Memory`。

成员清单
AGENTS.md: pingping 模块地图与三层工作协议。
lessons.md: 历史复盘摘录与行为校正记录。
knowledge/: pingping 业务知识附件区（PDF/参考资料）。

三层逻辑
- Memory（记忆层）:
  输入 `memory/`（个人记忆）、`memos`（任务便签）、`memory/shared/`（频道共享记忆）。
  目标是形成可执行上下文与优先级，不直接产出业务动作。
- Swarm（执行层）:
  负责调度执行器与工具链（如 opencode/codex/dispatch 脚本），把记忆层上下文转成可执行任务。
  只做执行编排与结果回收，不承担长期知识归档。
- Obsidian（沉淀层）:
  将执行结果沉淀到 `obsidian/Resources|Areas|Social`，形成可复用知识资产。
  沉淀后的结论必须回流到 Memory（daily/shared/lessons）指导下一轮执行。

闭环协议
1. 先读记忆：`memory + memos + memory/shared`。
2. 再执行：通过 swarm/dispatch 发起与跟踪任务。
3. 后沉淀：把结果写入 obsidian 对应分区。
4. 最后回写：把结论回写 memory/lessons，形成下一轮输入。

边界规则
- `pingping/` 只放角色知识资产与协议，不放运行日志与缓存。
- 角色行为源优先级：`PROMPT_BASE_FRACTAL.md -> PROMPT_PINGPING.md -> SOUL.md`。
- 新增知识文件时，必须更新本清单并注明用途。
- 禁止跳过沉淀回写，否则视为闭环中断。

[PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
