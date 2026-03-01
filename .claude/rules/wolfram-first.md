---
description: 所有数学推导必须通过 Wolfram Engine 完成，禁止仅凭文本推理进行符号计算。
---

# Wolfram First 规则

## 核心原则

**LLM 负责思考，CAS 负责计算。绝不手动进行符号推导。**

## 强制要求

以下操作**必须**通过 Wolfram Engine（`/d/Wolf/wolframscript.exe`）执行：

| 操作 | Wolfram 函数 | 禁止替代 |
|---|---|---|
| 解方程 | `Solve[]`, `DSolve[]` | 禁止手动代数推导 |
| 化简表达式 | `Simplify[]`, `FullSimplify[]` | 禁止"显然可化简为…" |
| 求导数 | `D[]` | 禁止手写导数结果 |
| 判断正负 | `Reduce[expr > 0, ...]` | 禁止"由于分母为正…所以…" |
| 比较大小 | `Reduce[a > b, ...]` | 禁止"容易看出 A > B" |
| 积分 | `Integrate[]` | 禁止手动积分 |
| 极限 | `Limit[]` | 禁止手动求极限 |
| LaTeX 公式 | `ToString[TeXForm[]]` | 禁止手写复杂 LaTeX |

## 允许 Claude 直接做的事

- 建立模型（定义效用/利润函数、博弈时序）
- 设定假设（参数范围、均衡概念）
- 解释 Wolfram 输出的经济学含义
- 撰写论文文本
- 设计推导策略和路线图

## 执行方式

- 推导不超过 5 步：使用 `-code` 内联执行
- 推导超过 5 步：编写 `.wl` 脚本，用 `-file` 执行
- 需要跨调用保留状态：使用 `DumpSave[]` / `Get[]`

## 违规处罚

在质量门控评分中，每个未经 Wolfram 验证的符号声明扣 **50 分**。
