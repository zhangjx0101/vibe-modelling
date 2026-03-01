---
name: learn
description: 捕获经验教训为持久化知识。将非显而易见的发现写入 MEMORY.md 或创建新 Skill。
argument-hint: [要记录的经验或发现]
---

# 经验捕获

将非显而易见的经验教训持久化，防止被上下文压缩遗忘。

## 工作流程

### Phase 1：评估
- 这是否非显而易见？
- 未来的我（或下一个项目）会受益吗？
- 如果两个都是"否"，不需要记录。

### Phase 2：检查已有知识
- 搜索 `~/.claude/skills/` 是否已有相关 Skill
- 搜索 `~/.claude/MEMORY.md` 是否已有相关条目
- 避免重复记录

### Phase 3：决定存储位置

| 类型 | 存储位置 | 判断标准 |
|---|---|---|
| 通用经验 | `~/.claude/MEMORY.md` | 另一个项目也会受益 |
| 项目特定 | `项目/MEMORY_LOCAL.md` | 仅对当前项目有用 |
| 可复用流程 | 新 Skill `.claude/skills/xxx/SKILL.md` | 是一个可重复的多步骤流程 |

### Phase 4：写入

使用 `[LEARN:category]` 标签：

```
[LEARN:wolfram] FullSimplify 对含 Abs[] 的表达式可能超时
  → 先用 PiecewiseExpand 展开，再 Simplify

[LEARN:model] 线性需求 P=1-Q + 二次成本 γq²/2 时
  → 混合寡头必定有内点解，无需额外 Assumption

[LEARN:latex] Wolfram TeXForm 输出 (c-1)
  → 需手动转换为 -(1-c) 并调整外部符号

[LEARN:derive] 当 Reduce 返回复杂条件而非 True/False
  → 添加更多参数约束，或用 3 组数值代入验证
```

## 类别标签

| 标签 | 适用范围 |
|---|---|
| `[LEARN:wolfram]` | Wolfram Engine 使用技巧 |
| `[LEARN:model]` | 建模经验和技巧 |
| `[LEARN:derive]` | 推导过程中的技巧 |
| `[LEARN:latex]` | LaTeX 排版经验 |
| `[LEARN:workflow]` | 工作流改进 |
| `[LEARN:econ]` | 经济学理论知识 |
