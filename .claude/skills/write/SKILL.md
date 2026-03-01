---
name: write
description: 按期刊规范撰写论文章节。嵌入 Wolfram 生成的 LaTeX 公式，附经济学解释。
argument-hint: [章节名称，如 "Section 3: Equilibrium Analysis"]
---

# 论文撰写

按照目标期刊（JIE/AER/RAND）的学术规范撰写论文章节。

## 核心原则

1. **所有数学公式来自 Wolfram**：使用 `ToString[TeXForm[]]` 生成的 LaTeX，不手写复杂公式
2. **每个 Proposition 必须有经济学解释**：2-3 段直觉性解释
3. **论文结构遵循期刊规范**

## 论文标准结构

```
1. Introduction（引言）
   - 动机和研究问题（无数学符号）
   - 主要发现摘要（用文字描述）
   - 贡献和文献定位
   - 论文结构路线图

2. Model（模型）
   - 基本设定（参与人、时序、信息）
   - 需求/效用函数
   - 成本结构
   - 均衡概念
   - 关键假设（Assumption 1, 2, ...）

3. Benchmark / Baseline（基准模型）
   - 简化版模型的均衡
   - 作为后续比较的参照

4. Equilibrium Analysis（均衡分析）
   - 后向归纳求解过程
   - Proposition 1, 2, ... （均衡性质）
   - 每个 Proposition 的经济学解释

5. Comparative Statics（比较静态）
   - 关键参数的影响
   - Proposition（比较静态结论）
   - 图形辅助说明

6. Welfare Analysis（福利分析）
   - 消费者剩余、生产者剩余、社会福利
   - 最优政策分析
   - Proposition（福利结论）

7. Extensions / Robustness（扩展）
   - 放松某个假设
   - 替代模型设定
   - 结果的稳健性

8. Conclusion（结论）
   - 主要发现总结
   - 政策含义
   - 局限性和未来方向

Appendix（附录）
   - 长证明
   - 补充计算
   - 额外图表
```

## 各章节写作规范

### Abstract（摘要）
- **严禁数学符号**
- 150-200 词
- 结构：动机 → 方法 → 主要发现 → 政策含义
- 不引用文献

### Introduction（引言）
- **严禁数学符号**
- 开头用 1-2 个事实或现象引入
- 明确说明"本文做了什么"
- 预览主要结论（用文字）
- Related Literature 可以是子节或独立章节
- 最后一段说明论文结构

### Proposition 格式

```latex
\begin{proposition}\label{prop:X}
[数学陈述，来自 Wolfram TeXForm]
\end{proposition}

\begin{proof}
See Appendix \ref{app:proof-propX}.
\end{proof}

[经济学解释：2-3 段]
- 第1段：核心直觉（为什么会有这个结论？）
- 第2段：机制分析（通过什么渠道/效应？）
- 第3段：与文献的联系或政策含义
```

### 图表规范
- 每张图有详细 caption，无需看正文即可理解
- 图表编号连续（Figure 1, 2, 3...）
- 使用 `\label{}` 和 `\ref{}` 交叉引用
- 图形来自 Wolfram Export 的 PDF 矢量图

## 写作风格

### 推荐用语
- "We show that..." / "We find that..."
- "It follows from Proposition X that..."
- "The intuition is as follows."
- "This result is driven by..."
- "Consistent with [Author (Year)], we find..."

### 避免用语
- "We can see that..." → "We observe that..."
- "It is obvious that..." → "It follows that..."
- "It is easy to show..." → 直接给出结果
- "Interestingly,..." → 删除，直接说结论
- 过度使用被动语态

## 工作流程

1. **确认章节**：明确要写哪一节，需要哪些 Wolfram 结果
2. **加载结果**：`Get["results.mx"]` 加载之前的推导
3. **生成公式**：用 `ToString[TeXForm[]]` 获取所有需要的 LaTeX
4. **撰写文本**：围绕公式写经济学分析
5. **交叉引用**：确保所有 `\ref{}` 和 `\cite{}` 正确
6. **编译检查**：用 `/compile` 检验排版效果
