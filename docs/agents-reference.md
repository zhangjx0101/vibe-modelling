# Agents Reference

All 8 specialized reviewing agents. Agents are automated reviewers — they read your work and produce reports. Some are triggered automatically, others can be invoked manually.

## Overview

| Agent | Role | Model | Access | Auto-triggered by |
|---|---|---|---|---|
| `math-critic` | Adversarial math auditor | Opus | Read + Wolfram | `/full-paper` Phase 7 |
| `math-fixer` | Math error repair | Sonnet | Read-Write + Wolfram | After `math-critic` finds issues |
| `econ-reviewer` | Economic logic review | Opus | Read-only | `/full-paper` Phase 7 |
| `referee-sim` | Simulated Referee 2 | Opus | Read + WebSearch | `/full-paper` Phase 7 |
| `proofreader` | Academic English | Haiku | Read-only | `/full-paper` Phase 7 |
| `lit-verifier` | Reference authenticity | Haiku | Read + WebSearch | `/check-refs`, `/full-paper` |
| `fact-checker` | Empirical claims | Haiku | Read + WebSearch | `/check-facts`, `/full-paper` |
| `latex-auditor` | LaTeX formatting | Haiku | Read + limited Bash | `/full-paper` Phase 7 |

## Automatic Selection Rules

The orchestrator auto-selects agents based on what files were modified:

| Modified files | Agents triggered |
|---|---|
| `.wl` scripts | `math-critic` → `math-fixer` |
| `.tex` paper | `econ-reviewer` + `proofreader` + `latex-auditor` |
| `.tex` + `.wl` together | `math-critic` + `econ-reviewer` + `latex-auditor` |
| Contains `\cite{}` | `lit-verifier` |
| Contains factual claims | `fact-checker` |
| Full paper pre-submission | All agents + `referee-sim` |

---

## Detailed Descriptions

### `math-critic` — Adversarial Math Auditor

**Purpose**: Find mathematical errors before a referee does.

**How it works**:
1. Reads your `.wl` scripts and `.tex` paper
2. Independently re-derives key results using Wolfram (does NOT rely on your .mx files)
3. Checks a 10-item hard gate:
   - FOC at equilibrium = 0
   - SOC at equilibrium < 0
   - Equilibrium uniqueness + feasibility
   - Comparative statics have `Reduce[]` support
   - Welfare function consistency
   - Cost structure consistency
   - Assumption sufficiency
   - Corner solution checks
   - Numerical verification (3+ parameter sets)
   - LaTeX formula matches Wolfram output

**Output**: `Math_Critique_Report.md`
- Verdict: **APPROVED** or **NEEDS REVISION**
- Issues classified: BLOCKING / MAJOR / MINOR
- Each issue includes the Wolfram command and output

**Key design**: The critic **cannot fix** anything — it can only identify problems. This prevents self-approval bias.

**How to invoke manually**:
```
You: 请 math-critic 审查推导
You: Launch math-critic agent to review my derivations
```

---

### `math-fixer` — Mathematical Error Repair

**Purpose**: Fix errors identified by `math-critic`.

**How it works**:
1. Reads the `Math_Critique_Report.md` from the critic
2. For each issue, modifies the `.wl` script and/or `.tex` file
3. Re-verifies with Wolfram after each fix
4. Documents every change with before/after Wolfram output

**Constraint**: Only fixes issues from the critic's report. Cannot self-approve — the critic re-reviews after fixes.

**The critic-fixer loop**:
```
math-critic identifies 3 issues
    ↓
math-fixer fixes issue #1, re-verifies with Wolfram ✓
math-fixer fixes issue #2, re-verifies with Wolfram ✓
math-fixer fixes issue #3, re-verifies with Wolfram ✓
    ↓
math-critic re-reviews → finds 1 new issue
    ↓
math-fixer fixes → re-verifies ✓
    ↓
math-critic re-reviews → APPROVED
```

**Hard limit**: Maximum 5 rounds to prevent infinite loops.

---

### `econ-reviewer` — Economic Logic Review

**Purpose**: Check that the economics makes sense — assumptions are realistic, intuitions are correct, contributions are clear.

**7 review dimensions**:
1. Model assumption realism — are they justified?
2. Economic intuition — does each result make sense?
3. Comparative statics — do directions match intuition?
4. Welfare analysis — is it complete?
5. Contribution clarity — what's new vs. prior work?
6. Policy implications — are they valid?
7. Internal consistency — do sections agree?

**Output**: `Economic_Review_Report.md`
- Summary + strengths
- Major issues (must address)
- Minor issues (should address)
- Suggestions for improvement

**How to invoke**:
```
You: 请 econ-reviewer 检查模型假设是否合理
You: 经济学逻辑审查
```

---

### `referee-sim` — Simulated Referee 2

**Purpose**: The harshest possible reviewer. Reads your paper with completely fresh eyes and no sympathy.

**Key design**: **Fresh context mode** — no knowledge of your research process, earlier drafts, or intentions. Purely adversarial first read, simulating the famously harsh "Referee 2".

**5 attack dimensions**:
1. **Contribution**: "Is this really new, or just 'add one parameter to existing model'?"
2. **Critical assumptions**: "Which assumptions drive the results? What if they're relaxed?"
3. **Model choice**: "Why Cournot, not Bertrand? Why static, not dynamic?"
4. **Missing factors**: "What about entry? Uncertainty? Information asymmetry?"
5. **Empirical relevance**: "Are parameters realistic? Any testable predictions?"

**Output**: `Referee_Report.md` in real review format:
- Summary of the paper
- Overall assessment (accept / revise / reject)
- Major comments (numbered)
- Minor comments (numbered)
- Questions for authors

**When to use**:
- Before submission — catch weaknesses before real referees do
- After revision — check if your revisions would satisfy a skeptical reviewer

**How to invoke**:
```
You: 模拟 Referee 2 审稿
You: 帮我预判审稿人会提什么意见
```

---

### `proofreader` — Academic English Polish

**Purpose**: Grammar, vocabulary, and style review. Does NOT change mathematical content.

**Checks**:
- Grammar: subject-verb agreement, tense consistency, articles
- Academic phraseology: "We show that..." not "We can see that..."
- Terminology consistency: same term for same concept throughout
- Sentence structure: avoid run-on sentences, passive voice balance
- Math-text integration: equations flow naturally into prose

**How to invoke**:
```
You: /proofread
You: 帮我检查英语语法
```

---

### `lit-verifier` — Reference Authenticity

**Purpose**: Verify that every citation in your bibliography is a real, published work.

**What it checks**:
- Author name exists and is associated with the topic
- Publication year matches
- Journal name is correct
- Volume/page numbers match
- DOI resolves
- Content described in your paper actually matches the cited paper

**Why it matters**: LLMs can hallucinate references. This agent catches fabricated citations before they embarrass you.

**How to invoke**:
```
You: /check-refs
You: 检查参考文献是否真实
```

---

### `fact-checker` — Empirical Claims Validator

**Purpose**: Verify factual claims in your paper against authoritative sources.

**Source priority**:
1. Government statistics (BLS, Census, Eurostat)
2. International organizations (World Bank, IMF, OECD)
3. Academic research (peer-reviewed)
4. Industry reports (McKinsey, Stanford AI Index)
5. Quality news sources

**What it checks**:
- Industry trends ("AI market reached $X billion")
- Market structure claims ("The largest 4 firms control X%")
- Policy facts ("Country X implemented policy Y in year Z")
- Historical facts

**How to invoke**:
```
You: /check-facts
You: 检查论文中的事实性声明
```

---

### `latex-auditor` — LaTeX Format Inspector

**Purpose**: Audit LaTeX formatting quality and journal compliance.

**6 inspection categories**:
1. Compilation: errors, warnings, overfull hbox
2. Cross-references: unresolved `\ref{}`, `\cite{}` consistency
3. Math formatting: inline vs display, subscript brackets, operators
4. Figures: vector vs raster, captions, labels
5. Journal format: margins, font, spacing, section structure
6. Structure: Abstract position, JEL codes, Keywords, Appendix format

**How to invoke**:
```
You: 检查 LaTeX 格式
You: 审查论文排版
```

---

## Running Multiple Agents

You can run multiple agents simultaneously for a comprehensive review:

```
You: 帮我做投稿前全面审查

Claude will launch in parallel:
  ├── math-critic     (verifying math)
  ├── econ-reviewer   (checking economics)
  ├── lit-verifier    (verifying references)
  ├── fact-checker    (checking facts)
  ├── proofreader     (checking English)
  ├── latex-auditor   (checking format)
  └── referee-sim     (simulating harsh review)

→ Results compiled into unified quality report
→ Score: 87/100 (submission-ready)
→ 2 major issues, 5 minor issues listed
```
