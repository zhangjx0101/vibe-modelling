# Scenario Guide — "I want to do X"

Find your scenario, see which tools to use, and follow the dialogue examples.

## Quick Lookup

| # | Scenario | Skills | Agents | Difficulty |
|---|---|---|---|---|
| 1 | [Verify my math](#1-verify-my-math) | `/derive`, `/verify` | `math-critic` | Easy |
| 2 | [Write one section](#2-write-one-section) | `/write`, `/compile` | `proofreader` | Easy |
| 3 | [Export to Word](#3-export-to-word) | `/export-word` | — | Easy |
| 4 | [Draw figures](#4-draw-figures) | `/plot` | — | Easy |
| 5 | [Learn from a paper](#5-learn-from-a-paper) | `/study`, `/lit-review` | — | Easy |
| 6 | [Check quality before submission](#6-check-quality-before-submission) | `/check-refs`, `/check-facts` | `lit-verifier`, `fact-checker` | Medium |
| 7 | [Respond to referees](#7-respond-to-referees) | `/revision` | `referee-sim` | Medium |
| 8 | [Write a full paper from scratch](#8-write-a-full-paper-from-scratch) | `/full-paper` | All | Advanced |

---

## 1. Verify My Math

**When**: You have a paper (yours or someone else's) and want to check if all formulas are correct.

**Tools**: `/derive` + `/verify` + optionally `math-critic` agent

**Steps**:
1. Point Claude to your paper file
2. Claude writes a Wolfram script to independently derive every formula
3. Each formula is checked: `Simplify[derived - paper] == 0` → PASS/FAIL
4. A log file records all results

### Dialogue Examples

**Example A: Verify an entire paper**

```
You: 帮我验证这篇论文的所有公式
     论文在 project/My Paper/Manuscript.tex

Claude will:
  → Read the paper, identify all equations
  → Write derive_all.wl (derives every formula from scratch)
  → Run the script: wolframscript -file derive_all.wl
  → Report: "43/43 ALL PASS" or "FAIL at eq(18a): residual = ..."
  → Save derivation_log.txt
```

**Example B: Verify a specific section**

```
You: /derive 验证 Section 3 的均衡解，特别是 Proposition 2

Claude will:
  → Focus on Section 3 equations only
  → Derive equilibrium from FOC, check against paper
  → Verify Prop 2's claims with Reduce[]
```

**Example C: Run numerical spot checks**

```
You: /verify 用 c=0.3, gamma=0.5, phi=1.0 检验所有结果

Claude will:
  → Substitute parameters into all closed-form expressions
  → Check FOC = 0 at equilibrium
  → Check SOC < 0
  → Verify comparative statics signs
```

**Example D: Adversarial math review**

```
You: 请 math-critic 审查一下推导是否有问题

Claude will:
  → Launch math-critic agent (read-only, adversarial)
  → Agent independently re-derives key results
  → Reports: APPROVED or NEEDS REVISION with specific issues
  → If issues found, math-fixer agent fixes them
```

### Tips
- Always save the `derivation_log.txt` — it's your reproducibility evidence
- If a check FAILS, Claude will tell you which formula is wrong and what the correct version should be
- For large papers, the script may take 2-3 minutes to run

---

## 2. Write One Section

**When**: Derivations are done, you need to write prose with embedded formulas.

**Tools**: `/write` + `/compile` + optionally `/proofread`

**Steps**:
1. Tell Claude which section to write
2. Claude pulls formulas from Wolfram results and writes LaTeX
3. Each Proposition gets 2-3 paragraphs of economic interpretation
4. Compile to check formatting

### Dialogue Examples

**Example A: Write a section from derivation results**

```
You: /write Section 4: Welfare Analysis
     均衡解已经在 derivations/ 里推导完了

Claude will:
  → Load Wolfram results from .mx files or derive_all.wl output
  → Write LaTeX with proper equation numbering
  → Add economic interpretation for each Proposition
  → Follow journal-style rules (no "obviously", no "interestingly")
```

**Example B: Write with specific journal in mind**

```
You: 帮我写 Introduction，目标期刊是 RAND Journal of Economics

Claude will:
  → Follow RAND style: no math in Introduction
  → Start with real-world motivation
  → Preview main results in plain language
  → Include Related Literature subsection
```

**Example C: Polish existing text**

```
You: /proofread Section 3，检查语法和学术用语

Claude will:
  → Check grammar, tense consistency, academic style
  → Flag informal expressions
  → Suggest improvements without changing math content
```

---

## 3. Export to Word

**When**: Need to share with coauthors who don't use LaTeX, or journal requires .docx.

**Tools**: `/export-word` or manual pandoc command

### Dialogue Examples

**Example A: Simple export**

```
You: /export-word 把论文转为 Word

Claude will:
  → Preprocess LaTeX commands incompatible with pandoc (e.g., \tag{})
  → Run pandoc to convert .tex/.md → .docx
  → Math formulas → Word native editable formulas (OMML)
  → Figures embedded, footnotes converted
```

**Example B: From Markdown**

```
You: 帮我把 Manuscript_corrected.md 导出为 Word

Claude will:
  → Run preprocess_md.wl (replace \tag{} → \qquad\text{()})
  → Run pandoc with --from markdown+footnotes+pipe_tables+tex_math_dollars
  → Output: Manuscript_corrected.docx
```

### Tips
- Pandoc doesn't support all LaTeX commands — `\tag{}`, `\label{}`, `\eqref{}` need preprocessing
- Figures must be PNG/JPG (pandoc can't embed PDF images in Word)
- Use Wolfram `StringReplace` for preprocessing, not sed/perl (backslash escaping issues)

---

## 4. Draw Figures

**When**: Need publication-quality figures for comparative statics, welfare analysis, etc.

**Tools**: `/plot`

### Dialogue Examples

**Example A: Comparative statics plot**

```
You: /plot 画 SW* 关于 phi 的变化，固定 c=0.3, gamma=0.5

Claude will:
  → Write Wolfram Plot[] command with academic styling
  → Frame, FrameLabel, proper font sizes
  → Export as PDF vector figure
  → Save to figures/Figure1.pdf
```

**Example B: Multiple curves**

```
You: 在同一张图里画不同 gamma 值下的 CS* 曲线

Claude will:
  → Plot multiple curves with legend
  → Use distinguishable line styles (Dashing, Thickness)
  → Export as PDF
```

**Example C: Region plot**

```
You: 画出 dSW*/dphi > 0 的参数区域

Claude will:
  → Use RegionPlot[numerator > 0, {phi, 0, 5}, {c, 0, 1}]
  → Add proper labels and shading
```

### Tips
- Always export as PDF for LaTeX papers (vector graphics)
- For Word export, also generate PNG at 300 DPI

---

## 5. Learn From a Paper

**When**: Reading a reference paper, want to understand their model and find research gaps.

**Tools**: `/study` + `/lit-review`

### Dialogue Examples

**Example A: Deep-dive into a specific paper**

```
You: /study 帮我精读这篇论文
     paper.pdf 在 references/ 目录

Claude will:
  → Extract model structure: players, timing, utility functions
  → Identify modeling techniques
  → Reproduce key results with Wolfram (sanity check)
  → Identify contribution gaps: "They assume X, what if Y?"
```

**Example B: Literature survey**

```
You: /lit-review mixed duopoly with corporate social responsibility

Claude will:
  → Search for related papers via WebSearch
  → Classify: directly relevant / methodological / background
  → Group by theme
  → Draft a Related Literature section
```

---

## 6. Check Quality Before Submission

**When**: Paper is ready, need final quality checks before submitting.

**Tools**: `/check-refs` + `/check-facts` + agents

### Dialogue Examples

**Example A: Verify all references are real**

```
You: /check-refs 检查参考文献是否都是真实的

Claude will:
  → Search each citation via Google Scholar
  → Verify: author, year, journal, DOI
  → Report: VERIFIED / NEEDS CHECK / UNVERIFIED for each
  → Flag any potentially fabricated references
```

**Example B: Fact-check empirical claims**

```
You: /check-facts 检查 Introduction 里的事实性声明

Claude will:
  → Extract factual claims ("AI market reached $X billion...")
  → Search authoritative sources (government stats, World Bank, etc.)
  → Report accuracy and suggest corrections if needed
```

**Example C: Full pre-submission review**

```
You: 论文写完了，帮我做一个全面的投稿前审查

Claude will:
  → Run ALL agents in parallel:
    - math-critic: verify all math
    - econ-reviewer: check economic logic
    - lit-verifier: verify references
    - fact-checker: verify facts
    - proofreader: check English
    - latex-auditor: check formatting
    - referee-sim: simulate harsh reviewer
  → Compile quality score (100-point scale)
  → Report all issues by severity
```

---

## 7. Respond to Referees

**When**: Received R&R decision, need to address referee comments.

**Tools**: `/revision` + optionally `referee-sim`

### Dialogue Examples

**Example A: Parse and plan response**

```
You: /revision 收到审稿意见了，帮我分析和规划回复
     审稿意见在 referee_report.pdf

Claude will:
  → Parse each comment
  → Classify: Major (must fix) / Minor (should fix) / Optional
  → Plan response strategy for each comment
  → Create revision branch in git
```

**Example B: Simulate the next round**

```
You: 修改完了，帮我模拟一下 Referee 2 看到修改稿会怎么反应

Claude will:
  → Launch referee-sim agent (fresh eyes, adversarial)
  → Reviews your revised paper as if seeing it for the first time
  → Predicts: likely accept / needs more revision / still problematic
  → Identifies remaining weaknesses
```

---

## 8. Write a Full Paper From Scratch

**When**: Starting from a research idea, want the complete pipeline.

**Tools**: `/full-paper` (orchestrates everything)

### Dialogue Examples

**Example A: Start from an idea**

```
You: /full-paper I want to study how AI adoption affects competition
     in a mixed duopoly with a welfare-maximizing public firm

Claude will orchestrate 10 phases:
  Phase 1: /idea → brainstorm specific angles
  Phase 2: /study → deep-read 2-3 key papers
  Phase 3: /lit-review → systematic literature search
  Phase 4: /model → design game structure
  Phase 5: /derive + /verify + /plot → solve and verify
  Phase 6: /write + /compile → draft paper
  Phase 7: All agents review in parallel
  Phase 8: Fix issues by severity
  Phase 9: /snapshot → version control
  Phase 10: /submit → final preparation

  User checkpoints at: direction (CP1), model (CP2),
  derivation (CP3), draft (CP4), reviews (CP5)
```

**Example B: Resume from a specific phase**

```
You: 模型已经设计好了，从推导阶段开始

Claude will:
  → Skip Phases 1-4
  → Start from Phase 5: /derive
  → Continue through writing and review
```

### Tips
- `/full-paper` has 5 user checkpoints — you approve each major stage before proceeding
- You can always interrupt and resume from any phase
- The orchestrator follows the [Orchestrator Protocol](../.claude/rules/orchestrator-protocol.md) with max 3 review rounds

---

## Choosing Your Path: Decision Tree

```
Do you have a finished paper?
├── YES → "Verify math?" → /derive + /verify
│         "Export to Word?" → /export-word
│         "Submit?" → /check-refs + /check-facts + full review
│         "Respond to referees?" → /revision
│
├── PARTIALLY → "Need to write sections?" → /write + /compile
│               "Need figures?" → /plot
│               "Need to verify what you have?" → /verify
│
└── NO → "Have a research idea?" → /full-paper
         "Want to explore literature?" → /study + /lit-review
         "Want to brainstorm?" → /idea
```
