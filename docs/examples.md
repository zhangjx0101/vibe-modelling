# Real-World Examples

Complete workflow walkthroughs from actual projects. These show exactly what was said, what tools were used, and what problems were encountered.

---

## Example 1: Verify, Fix, and Export a Paper

**Project**: "Moral Preferences, Taxation, and Welfare in Mixed Duopoly"
**Goal**: Verify all math in a completed paper → fix errors → export to Word
**Duration**: ~2 hours
**Skills used**: `/derive`, `/verify`, `/export-word` (manual pandoc)
**Agents used**: None (manual verification was sufficient)

### The Conversation

**Step 1: Verify the math**

```
You: 帮我验证这篇论文的所有公式是否正确
     论文在 project/Moral Preferences.../Manuscript.md
```

Claude read the paper, then wrote a comprehensive `derive_all.wl` script (~280 lines) that independently derived every equation from the model definition. The script covers:
- Model setup (utility → demand → CS)
- Stage 2 equilibrium (FOC → BR → solve system)
- Optimal tax (FOC/SOC → t*)
- SPNE results (all welfare components)
- Private duopoly comparison
- Appendix verification
- Numerical tables

**Step 2: Discover errors**

Running the script revealed **3 errors** that were invisible to the human eye:

| Error | Location | What was wrong |
|---|---|---|
| Sign error in factorization | eq(18a) | `+c(1-phi)` should be `+c(1-phi)` in second factor, but first factor had wrong sign |
| Wrong numerical values | Table 1 | 3 out of 5 c-bar values were miscalculated |
| Wrong quartic coefficients | Appendix A | phi^1 and phi^0 coefficients displayed incorrectly |

```
Claude: 发现 3 处错误：
  1. eq(18a) pi0* 因式分解符号写反
  2. Table 1 中 c̄ 值：0.689→0.551, 0.870→1.140, 0.933→1.200
  3. Appendix A 四次方程的低阶系数显示错误
```

**Step 3: Fix errors**

```
You: 帮我修正这些错误
```

Claude corrected all errors in `Manuscript_corrected.md`, re-ran the script: **43/43 ALL PASS**.

**Step 4: Discover deeper problem in Appendix A**

```
You: Appendix 的推导和写法你是确定过没问题的吗？
```

Claude ran a dedicated `verify_appendices.wl` script and discovered the Ferrari closed-form solution for the threshold phi was **wrong for 6 out of 7 parameter combinations** — it produced complex numbers or incorrect values. The root cause: Ferrari's method has multiple branches depending on the discriminant sign, but the paper only showed one branch.

**Solution**: Replaced the Ferrari formula with a simpler, more robust proof:
- **Existence**: Intermediate Value Theorem (numerator is negative at phi=0, positive at phi→infinity)
- **Uniqueness**: Descartes' rule of signs (exactly 1 sign change → 1 positive root)

**Step 5: Export to Word**

```
You: 帮我导出为 Word 文件
```

First attempt failed — pandoc couldn't handle `\tag{}` in math blocks. After trying sed and perl (both failed due to backslash escaping), Claude used Wolfram's `StringReplace` to preprocess the file:

```mathematica
text = StringReplace[text, "\\tag{" ~~ n:Shortest[Except["}"]..] ~~ "}" :> "\\qquad\\text{(" <> n <> ")}"];
```

All 27 `\tag{}` replaced successfully. Pandoc then produced a clean 524KB .docx.

### Lessons Learned

1. **Human-derived formulas often have subtle errors** — factorization signs and numerical tables are high-risk areas
2. **Closed-form solutions aren't always better** — the Ferrari formula was elegant but wrong; IVT + Descartes is simpler and correct
3. **Use Wolfram for LaTeX text processing** — sed/perl can't reliably handle backslash-heavy LaTeX content
4. **Always save the derivation log** — `derivation_log.txt` is your reproducibility evidence

### Files Created

```
derivations/derive_all.wl          # Complete derivation (43 checks)
derivations/derivation_log.txt     # Log: 43/43 ALL PASS
derivations/verify_appendices.wl   # Appendix-specific verification
derivations/preprocess_md.wl       # Pandoc preprocessing
Manuscript_corrected.md            # Fixed manuscript
Manuscript_corrected.docx          # Word export
```

---

## Example 2: Full Paper Pipeline (Typical Flow)

**Goal**: Write a theory paper from idea to submission-ready draft
**Skills used**: `/idea` → `/study` → `/lit-review` → `/model` → `/derive` → `/verify` → `/plot` → `/write` → `/compile` → review agents → `/submit`

### Phase 1: Research Direction

```
You: /idea I'm interested in how AI affects competition between public and private firms

Claude will:
  → Search recent literature on AI + mixed oligopoly
  → Propose 3-5 specific angles:
    1. AI as cost-reducing technology in mixed duopoly
    2. AI and data advantages in public-private competition
    3. AI-driven quality differentiation
    ...
  → Assess feasibility and contribution for each

You: 我喜欢方向1，用 AI 作为降低成本的技术

Claude will:
  → Narrow down: "How does AI adoption intensity affect optimal taxation
     and welfare in a mixed duopoly?"
```

### Phase 2: Literature Foundation

```
You: /study 帮我精读 Matsumura (1998) 和 De Fraja & Delbono (1989)

Claude will:
  → Extract model structure from each paper
  → Reproduce key results with Wolfram
  → Identify gaps: "Neither considers technology choice"

You: /lit-review mixed duopoly taxation AI technology

Claude will:
  → Find 20-30 related papers
  → Classify by relevance
  → Draft Related Literature section
```

### Phase 3: Model Design

```
You: /model 设计一个两阶段博弈：政府先选税率，然后公私企业进行产量竞争

Claude will:
  → Define players, timing, utility/profit functions
  → Set parameter assumptions
  → Wolfram pre-check: "Is this model analytically solvable?"
  → Output: Model_Setup.md with complete specification
```

### Phase 4: Derivation + Verification + Figures

```
You: /derive 求解完整的两阶段博弈

Claude will:
  → Write multi-phase .wl script
  → Solve Stage 2 (Cournot equilibrium as function of tax)
  → Solve Stage 1 (optimal tax)
  → Compute SPNE, welfare components
  → Run comparative statics
  → All with Reduce[] sign verification

You: /verify 用 5 组参数检验

Claude will:
  → Substitute parameters, check FOC=0, SOC<0
  → Generate verification tables

You: /plot 画 SW* 关于 phi 的变化

Claude will:
  → Generate PDF figures with academic styling
```

### Phase 5: Writing + Compilation

```
You: /write 按照 RAND Journal 风格写全文

Claude will:
  → Write each section following journal-style rules
  → Embed Wolfram-generated LaTeX formulas
  → 2-3 paragraphs economic interpretation per Proposition
  → No math in Abstract or Introduction

You: /compile

Claude will:
  → pdflatex → bibtex → pdflatex → pdflatex
  → Report any warnings
```

### Phase 6: Review + Quality Gate

```
You: 帮我做投稿前全面审查

Claude will:
  → Launch 7 agents in parallel
  → Compile quality score
  → Fix issues by severity (Blocking → Major → Minor)
  → Re-score until >= 85
```

---

## Example 3: Responding to Referee Comments

**Goal**: Address R&R referee comments systematically

```
You: /revision 收到 RAND 的 R&R，审稿意见在 referee_reports.pdf

Claude will:
  → Parse all referee comments
  → Classify each:
    - Major #1: "Relax Assumption 1 to allow c > c-bar"
    - Major #2: "Compare with Bertrand competition"
    - Minor #1: "Clarify notation in eq(7)"
    - Minor #2: "Add reference to Wang (2020)"
    ...
  → Plan response strategy for each
  → Create revision/r1 branch

You: 先处理 Major #1

Claude will:
  → Modify model to allow c > c-bar
  → Re-derive affected equations with Wolfram
  → Update paper text
  → Write response paragraph for Major #1

You: 修改完了，模拟一下 Referee 2 的反应

Claude will:
  → Launch referee-sim (fresh eyes, adversarial)
  → "The authors have adequately addressed most concerns,
     but the new extension feels rushed. I recommend..."
```

---

## Tips for Effective Prompting

### Be Specific About What You Want

```
Less effective: "帮我处理一下论文"
More effective: "帮我验证 Section 3 的均衡解是否正确，特别是 eq(8)-(10)"
```

### Tell Claude What Stage You're At

```
Less effective: "帮我写论文"
More effective: "推导已经完成（在 derivations/ 里），帮我写 Section 4: Welfare Analysis"
```

### Use Slash Commands for Specific Tasks

```
Natural language: "帮我检查参考文献是不是真的" → works, but less targeted
Slash command: "/check-refs" → triggers specialized workflow directly
```

### Combine Commands for Complex Workflows

```
You: 先 /derive 求解模型，然后 /verify 验证，最后 /plot 画图

Claude will:
  → Execute all three in sequence
  → Each step builds on the previous
```
