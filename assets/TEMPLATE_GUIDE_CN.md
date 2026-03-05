# Word 模板自定义指南

## 原理

Pandoc 把 Markdown 转为 Word 时，每种元素都对应一个 **Word 样式**。你只要在模板里修改这些样式的字体、字号、行距，所有导出的文档就会自动继承。

---

## 一图看懂：完整论文 Markdown → Word 对应

下面是一篇完整论文的 Markdown 写法。每个部分右边的 `←` 注释告诉你它在 Word 里对应哪个样式。

```
# Moral Preferences, Taxation, and Welfare          ← Word 样式: Title
# in Mixed Duopoly                                     （论文大标题）

Author Name and Coauthor Name                        ← Word 样式: Normal
                                                       （作者，需手动居中）

University A; University B                           ← Word 样式: Normal

> **Abstract.** This paper examines how moral        ← Word 样式: Block Text
> preferences affect optimal taxation and welfare      （引用块，自动左右缩进）
> in a mixed duopoly where a public firm competes
> with a private firm under Cournot competition.
> We show that the optimal policy is a subsidy
> equal to the private firm's equilibrium output.
>
> **Keywords:** mixed duopoly, moral preferences     ← 还是 Block Text
>
> **JEL Classification:** H21, L13, L32             ← 还是 Block Text


## 1. Introduction                                   ← Word 样式: Heading 1
                                                       （一级章节标题）

The rapid adoption of artificial intelligence (AI)   ← Word 样式: Normal
has transformed production processes across            （正文段落）
industries. Recent estimates suggest that the
global AI market exceeded $150 billion in 2023.[^1]

This paper contributes to the literature on          ← Word 样式: Normal
**mixed duopoly** by incorporating *moral              （**加粗** 和 *斜体*
preferences* into firms' cost structures.               自动继承 Normal 样式）

### 1.1 Related Literature                           ← Word 样式: Heading 2
                                                       （二级标题）

De Fraja and Delbono (1989) established the          ← Word 样式: Normal
foundational framework for mixed oligopoly.


## 2. The Model                                      ← Word 样式: Heading 1

### 2.1 Demand and Cost                              ← Word 样式: Heading 2

We consider a market with a representative           ← Word 样式: Normal
consumer whose quasi-linear utility function is

$$U(Q, m) = (1+\gamma\phi)Q - \frac{Q^2}{2} + m    ← Word: 独立公式 (OMML)
\qquad\text{(1)}$$                                     （独占一行，可编辑）

where $Q = q_0 + q_1$ is total output and            ← Normal 段落中嵌入
$\gamma \in (0,1)$ is the moral preference              行内公式 (OMML)
parameter.

The inverse demand function is given by              ← Word 样式: Normal
$P = 1 + \gamma\phi - Q$. The private firm's
profit is

$$\pi_1 = (P - t)q_1 - \frac{1}{2}\phi q_1^2       ← Word: 独立公式 (OMML)
\qquad\text{(2)}$$

> **Assumption 1.** The marginal cost parameter      ← Word 样式: Block Text
> satisfies $0 < c < \bar{c}(\phi, \gamma)$,          （Assumption 用引用块
> ensuring both firms produce positive output.           会自动缩进，与正文区分）


## 3. Equilibrium Analysis                           ← Word 样式: Heading 1

### 3.1 Stage 2: Output Competition                  ← Word 样式: Heading 2

#### 3.1.1 Best Response Functions                    ← Word 样式: Heading 3
                                                       （三级标题，很少用）

> **Proposition 1.** *The optimal tax is a subsidy   ← Word 样式: Block Text
> equal to the private firm's equilibrium output:
> $t^* = -q_1^*$.*

The intuition behind Proposition 1 is                ← Word 样式: Normal
straightforward. The government...

The key results are summarized in Table 1:

: Table 1: Equilibrium Values                        ← Word 样式: Table Caption
                                                       （表格标题，写在表上方）

| $c$ | $\gamma$ | $\phi$ | $t^*$  | $SW^*$ |       ← Word: 表格 (Table)
|:---:|:---:|:---:|:------:|:------:|                   （自动转为 Word 表格，
| 0.3 | 0.5 | 1.0 | -0.500 | 0.681 |                   表内公式可编辑）
| 0.5 | 0.3 | 0.8 | -0.491 | 0.418 |
| 0.1 | 0.8 | 0.5 | -0.720 | 0.884 |


## 4. Welfare Analysis                               ← Word 样式: Heading 1

The main findings are:                               ← Word 样式: Normal

1. Consumer surplus increases with AI efficiency     ← Word 样式: Numbered List
2. Social welfare exhibits a U-shaped pattern          （有序列表）
3. Mixed duopoly dominates private duopoly

Key mechanisms:                                      ← Word 样式: Normal

- Cost reduction channel                             ← Word 样式: Bullet List
- Output reallocation channel                          （无序列表）
- Tax adjustment channel

![Figure 1: Social Welfare as a Function             ← Word: 嵌入图片
of AI Efficiency](figures/Figure1.png)                 + Image Caption 样式
                                                       （图片标题）


## 5. Conclusion                                     ← Word 样式: Heading 1

This paper has shown that moral preferences          ← Word 样式: Normal
fundamentally alter the optimal taxation policy
in mixed duopoly markets.

---                                                  ← Word: 分割线

## References                                        ← Word 样式: Heading 1

De Fraja, G. and Delbono, F. (1989). Alternative    ← Word 样式: Normal
strategies of a public enterprise in oligopoly.
*Oxford Economic Papers*, 41(2), 302-311.

Matsumura, T. (1998). Partial privatization in       ← Word 样式: Normal
mixed duopoly. *Journal of Public Economics*,
70(3), 473-483.


## Appendix A: Proof of Proposition 4                ← Word 样式: Heading 1

The numerator of $\partial SW^*/\partial\phi$ is     ← Word 样式: Normal
a quartic polynomial in $\phi$:

$$\phi^4 + 4\phi^3 + \alpha\phi^2                   ← Word: 独立公式 (OMML)
- \frac{c^2}{\gamma^2}\phi
- \frac{c^2}{\gamma^2}
\qquad\text{(A.1)}$$


[^1]: Stanford AI Index Report, 2024.                ← Word 样式: Footnote Text
                                                       （脚注，自动编号，
                                                        页面底部显示）
```

---

## 样式汇总表

你在模板里只需要改这 **10 个样式**：

| Word 样式名 | 对应的论文元素 | 推荐设置 |
|---|---|---|
| **Title** | `#` 论文标题 | 16号 Times New Roman 加粗，居中 |
| **Heading 1** | `##` 章节标题 | 14号 TNR 加粗，居中，段前 24磅 |
| **Heading 2** | `###` 子章节标题 | 12号 TNR 加粗，左对齐，段前 18磅 |
| **Heading 3** | `####` 三级标题 | 12号 TNR 加粗斜体，段前 12磅 |
| **Normal** | 正文、作者、参考文献 | 12号 TNR，双倍行距 |
| **Block Text** | `>` 摘要、Assumption、Proposition | 11号 TNR，左右缩进 0.5" |
| **Table Caption** | `: Table 1: ...` | 10号 TNR 加粗，居中 |
| **Image Caption** | `![Figure 1: ...]` | 10号 TNR，居中 |
| **Footnote Text** | `[^1]` 脚注 | 10号 TNR，单倍行距 |
| **Compact** | `1.` 和 `-` 列表 | 12号 TNR，悬挂缩进 |

---

## 操作步骤

### 第 1 步：打开模板

用 Word 打开 `assets/academic-template.docx`。

### 第 2 步：修改样式

**开始 → 样式面板 → 右键某个样式 → 修改**

按上面汇总表设置。最重要的 3 个：
- **Normal** → 12号 TNR，双倍行距（控制所有正文）
- **Heading 1** → 14号 TNR 加粗居中（控制章节标题）
- **Title** → 16号 TNR 加粗居中（控制论文大标题）

### 第 3 步：设置页面

**布局 → 页边距 → 自定义页边距：** 上下左右 2.54cm（1 英寸）

### 第 4 步：保存

直接保存，不改文件名。

---

## 导出命令

```bash
pandoc input.md -o output.docx \
  --reference-doc=assets/academic-template.docx \
  --from markdown+footnotes+pipe_tables+tex_math_dollars \
  --shift-heading-level-by=-1 \
  --standalone
```

| 参数 | 作用 |
|---|---|
| `--reference-doc=...` | 使用你的自定义模板 |
| `--shift-heading-level-by=-1` | **关键**：让 `#` → Title，`##` → Heading 1 |
| `--from markdown+...` | 启用脚注、管道表格、TeX 数学 |
| `--standalone` | 生成完整文档 |

---

## 数学公式说明

| 写法 | Word 里的效果 |
|---|---|
| `$P = 1 - Q$` | 行内公式，嵌在句子中间，可双击编辑 |
| `$$P = 1 - Q \qquad\text{(1)}$$` | 独立行公式，单独占一行，可双击编辑 |

- 公式格式是 **OMML**（Word 原生），不是图片，完全可编辑
- 公式渲染**不受模板影响**——模板只控制公式周围的文字
- `\tag{N}` 不兼容 pandoc，必须用 `\qquad\text{(N)}` 代替（预处理脚本自动处理）

---

## 注意事项

1. 样式名称保持英文（Pandoc 按英文名匹配）
2. 只改样式定义，不用管占位内容
3. 图片必须是 **PNG/JPG**（Word 不支持嵌入 PDF）
4. `\tag{}` 需要预处理（用 `derivations/preprocess_md.wl`）
5. 改好模板后先用短文档测试
