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

## 两级记忆体系

| 层级 | 文件 | 位置 | 内容 | 影响范围 |
|------|------|------|------|----------|
| **全局** | `MEMORY.md` | Claude auto-memory 目录 | 跨项目通用经验（Wolfram 技巧、常见错误模式、工作流心得） | 所有项目 |
| **项目** | `MEMORY_LOCAL.md` + `CLAUDE.md` | 项目根目录 | 本论文的模型、验算结果、下一步计划、待办事项 | 仅本项目 |

### 何时创建项目级记忆

当一个论文项目满足以下任一条件时，**必须**创建 `CLAUDE.md` + `MEMORY_LOCAL.md`：
- 验算/写作分多次会话完成（中间会离开几天）
- 需要等待外部输入（如老师确认投稿期刊）再继续
- 项目状态复杂（多个文件、多步骤进度）

### 项目级文件模板

**`CLAUDE.md`**（Claude Code 自动加载的指令文件）：
```markdown
# Project Instructions

## Quick Context
[一句话说明这是什么项目]

**On first interaction, read `MEMORY_LOCAL.md` for full project state.**

## Key Facts
- [验算状态]
- [关键文件列表]
- [待办事项]

## Workflow Rules
- Follow the parent project's rules in `../../.claude/rules/`
- Wolfram Engine path: `/d/Wolf/wolframscript.exe`
```

**`MEMORY_LOCAL.md`**（项目详细记忆）：
```markdown
# Project Memory — [Paper Short Name]

## Paper Info（论文基本信息）
## Model Summary（模型结构摘要）
## Verification Results（验算结果 + 错误清单）
## File Map（项目文件结构）
## Next Steps（下一步计划）
## Technical Notes（技术备忘）
```

### 内容分流原则

| 内容类型 | 放在哪里 | 示例 |
|----------|----------|------|
| 通用方法论 | 全局 MEMORY.md | "理性预期模型中 FOC 必须先求导再代入 y=q" |
| 通用 Wolfram 技巧 | 全局 MEMORY.md | "FullSimplify 对 Abs[] 超时，用 PiecewiseExpand" |
| 论文具体进度 | 项目 MEMORY_LOCAL.md | "Eq 1-27 验证完毕，Table 1 有 t* 常数化错误" |
| 论文待办事项 | 项目 MEMORY_LOCAL.md | "待确认投稿期刊后调整格式" |
| 模型参数/公式 | 项目 MEMORY_LOCAL.md | "ξ = ((c+ps)/β)^(1/(β-1))，基准参数下 ≈ 0.1736" |

### 清理规则

- 项目完成（投稿成功）后，将通用经验提炼到全局 MEMORY.md，删除项目级文件中的冗余信息
- 全局 MEMORY.md 中不保留项目特定的详细信息（如具体公式编号、文件路径）
- 保持全局 MEMORY.md 在 200 行以内

## 记录时机

- 每次会话结束前检查是否有新发现
- 上下文压缩前自动保存关键信息
- 遇到非预期结果时立即记录
- **项目阶段性完成时**（如验算完成、等待外部输入），创建或更新 MEMORY_LOCAL.md

## 读取时机

- 新会话开始时读取 MEMORY.md
- 进入项目目录时读取 CLAUDE.md → MEMORY_LOCAL.md
- 遇到类似问题时搜索 MEMORY.md
