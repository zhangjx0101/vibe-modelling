---
name: full-paper
description: 端到端论文生成。从研究方向到最终 PDF 的完整流程编排。
argument-hint: [研究方向描述]
---

# 端到端论文生成

编排完整的理论经济学论文生产流程，从研究方向到投稿就绪的 PDF。

## 总体流程

```
Phase 1: /idea       → 确定研究问题          💡 构想
Phase 2: /study      → 学习关键文献          📖 学习
Phase 3: /lit-review → 系统文献检索          📚 文献
Phase 4: /model      → 模型设计 → 用户确认   🏗️ 建模
Phase 5: /derive + /verify + /plot            🔢 推导
Phase 6: /write + /compile                    ✍️ 写作
Phase 7: 多 Agent 并行审查                    🔍 审查
Phase 8: 修复 → 重新审查（最多 3 轮）        🔧 修复
Phase 9: /snapshot                            📦 版本
Phase 10: /submit                             📮 投稿
```

## 各阶段详细说明

### Phase 1：研究构想（/idea）
- 输入：用户描述一个大方向
- 输出：3-5 个具体研究问题，每个附可行性评估
- 门控：用户选择并确认方向

### Phase 2：文献学习（/study）
- 输入：1-3 篇核心参考文献
- 输出：模型解剖报告、技术提取、定位分析
- 门控：用户确认学习成果

### Phase 3：文献检索（/lit-review）
- 输入：确定的研究问题
- 输出：分类文献列表 + Related Literature 草稿
- 门控：lit-verifier 验证引用真实性

### Phase 4：模型设计（/model）
- 输入：研究问题 + 文献学习成果
- 输出：完整模型设定（Spec 文档）
- 门控：用户确认模型设定 + Wolfram 可行性预检

### Phase 5：数学推导（/derive + /verify + /plot）
- 输入：确认的模型设定
- 步骤：
  1. `/derive` — Wolfram 符号推导（7 个 Phase）
  2. `/verify` — 数值验证（3+ 组参数）
  3. `/plot` — 图形生成（PDF 矢量图）
- 门控：
  - 所有 FOC = 0 ✓
  - 所有 SOC < 0 ✓
  - 所有比较静态有 Reduce 支撑 ✓
  - 数值验证全部通过 ✓

### Phase 6：论文撰写（/write + /compile）
- 输入：Wolfram 推导结果 + 文献 + 模型设定
- 步骤：
  1. `/write` — 逐章撰写（期刊规范）
  2. `/compile` — LaTeX 编译 → PDF
- 写作顺序：
  1. Model Setup (Section 2)
  2. Equilibrium Analysis (Section 3)
  3. Comparative Statics (Section 4)
  4. Welfare Analysis (Section 5)
  5. Extensions / Policy (Section 6)
  6. Conclusion (Section 7)
  7. Introduction (Section 1) — 最后写
  8. Abstract — 最最后写

### Phase 7：多 Agent 并行审查
- 并行启动以下 Agent：
  - `math-critic` — 数学正确性（最重要）
  - `econ-reviewer` — 经济学逻辑
  - `referee-sim` — 模拟审稿人
  - `proofreader` — 语言润色
  - `lit-verifier` — 文献真实性
  - `fact-checker` — 事实核查
  - `latex-auditor` — 格式审计
- 汇总所有报告

### Phase 8：修复循环（最多 3 轮）
- 按优先级处理：
  1. math-critic 的问题（用 math-fixer 修复）
  2. econ-reviewer 的问题
  3. referee-sim 的问题
  4. 其他问题
- 每轮修复后重新审查
- 运行 quality-gates 评分

### Phase 9：版本快照（/snapshot）
- 创建 Git commit
- 确保所有文件已保存

### Phase 10：投稿准备（/submit）
- 根据目标期刊调整格式
- 生成投稿材料清单
- quality-gates 最终评分 ≥ 85 方可投稿

## 关键检查点（需用户确认）

| 检查点 | 位置 | 内容 |
|---|---|---|
| CP1 | Phase 1 后 | 研究方向确认 |
| CP2 | Phase 4 后 | 模型设定确认 |
| CP3 | Phase 5 后 | 推导结果确认 |
| CP4 | Phase 6 后 | 论文初稿确认 |
| CP5 | Phase 8 后 | 审查通过确认 |

## 使用方式

完整流程：
```
/full-paper AI cost reduction in mixed duopoly
```

从中间阶段开始（已有部分成果）：
```
用户：我已经有了模型设定，请从推导阶段开始
→ Claude 从 Phase 5 开始
```

## 注意事项

- 每个 Phase 都可以独立使用对应的 Skill
- 用户可以随时中断和恢复
- 所有数学必须经过 Wolfram Engine
- 关键检查点必须等待用户确认后才能继续
