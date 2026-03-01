---
description: 承包商模式执行循环。用户描述目标后，自动完成 Plan→Implement→Verify→Review→Fix→Score。
---

# Orchestrator Protocol — 承包商模式

## 核心原则

**用户只描述目标，Claude 全权调度执行。** 用户不需要手动调用 agent 或选择 reviewer。

## 执行循环

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — 执行计划步骤（调用相应 Skill）
  │
  Step 2: VERIFY — 编译/运行验证输出正确
  │         失败 → 修复 → 重新验证（最多 2 次）
  │
  Step 3: REVIEW — 根据文件类型自动选择 Agent 审查
  │
  Step 4: FIX — 按 Blocking → Major → Minor 修复
  │
  Step 5: RE-VERIFY — 确认修复无误
  │
  Step 6: SCORE — 质量门控评分
  │
  +── Score ≥ 阈值? → YES: 向用户报告结果
                    → NO: 回到 Step 3（最多 3 轮）
```

## Agent 自动选择

| 修改的文件类型 | 自动触发的 Agent |
|---|---|
| `.wl` 推导脚本 | math-critic → math-fixer（对抗循环） |
| `.tex` 论文 | econ-reviewer + proofreader + latex-auditor |
| `.tex` + `.wl` 同时 | math-critic + econ-reviewer + latex-auditor |
| 含 `\cite{}` | lit-verifier |
| 含事实性声明 | fact-checker |
| 完整论文提交前 | 全部 Agent 并行 + referee-sim |

## 硬限制

- 主循环：最多 **3** 轮 review-fix
- Critic-Fixer 子循环：最多 **5** 轮
- 验证重试：最多 **2** 次
- 永远不要无限循环

## 报告格式

每次循环结束后向用户报告：
- 完成了什么
- 质量分数
- 剩余问题（如有）
- 下一步建议
