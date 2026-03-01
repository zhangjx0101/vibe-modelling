---
description: "会话日志：关键决策和发现记录到 MEMORY.md"
---

# Session Logging 规则

## 核心原则

**关键决策和非显而易见的发现必须持久化，防止被上下文压缩遗忘。**

## 必须记录的事项

| 事项 | 示例 | 记录位置 |
|---|---|---|
| 模型修改决策 | "改用二次成本而非线性成本" | MEMORY.md |
| 参数约束发现 | "γ > 2 时才有内点解" | MEMORY.md |
| Wolfram 技巧 | "FullSimplify 对 Abs[] 超时" | MEMORY.md |
| 推导死路 | "尝试 Bertrand 竞争，无法解析" | MEMORY.md |
| 论文结构决策 | "将 benchmark 移到 Section 3" | MEMORY.md |
| 审稿人反馈要点 | "Referee 2 要求放松 Assumption 1" | 项目 MEMORY_LOCAL.md |

## 记录格式

使用 `[LEARN:category]` 标签：

```
[LEARN:model] 线性需求 + 二次成本时，混合寡头必定有内点解
  → 无需额外 Assumption 约束参数

[LEARN:wolfram] FullSimplify 对含 Abs[] 的表达式可能超时
  → 先用 PiecewiseExpand 展开，再 Simplify

[LEARN:derive] 当 Reduce 返回复杂条件而非 True/False
  → 添加更多参数约束，或用 3 组数值代入验证
```

## 记录时机

- 每次会话结束前检查是否有新发现
- 上下文压缩前自动保存关键信息
- 遇到非预期结果时立即记录

## 读取时机

- 新会话开始时读取 MEMORY.md
- 切换项目时读取项目 MEMORY_LOCAL.md
- 遇到类似问题时搜索 MEMORY.md
