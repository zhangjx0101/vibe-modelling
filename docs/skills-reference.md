# Skills Reference

All 18 slash commands, organized by workflow phase.

## Overview

```
Research    /idea → /study → /lit-review
Modeling    /model → /derive → /verify → /plot
Writing     /write → /compile → /export-word → /proofread
Quality     /check-refs → /check-facts
Workflow    /snapshot → /learn → /submit → /revision → /full-paper
```

---

## Research Phase

### `/idea` — Brainstorm Research Questions

| | |
|---|---|
| **Input** | Broad research direction (e.g., "AI in mixed duopoly") |
| **Output** | 3-5 concrete research questions with feasibility assessment |
| **Dependencies** | WebSearch |
| **Example** | `/idea how does AI affect public-private competition` |

Process: Literature scan → identify gaps → propose directions → assess feasibility.

### `/study` — Deep-Read a Paper

| | |
|---|---|
| **Input** | Paper file path (PDF/tex) or citation |
| **Output** | Study notes: model anatomy, techniques, Wolfram reproduction, gaps |
| **Dependencies** | Wolfram Engine (for reproducing key results) |
| **Example** | `/study references/Matsumura1998.pdf` |

Key step: Wolfram reproduction of the paper's main results — catches errors and builds understanding.

### `/lit-review` — Systematic Literature Search

| | |
|---|---|
| **Input** | Research topic or keywords |
| **Output** | Categorized literature list + Related Literature draft |
| **Dependencies** | WebSearch; `lit-verifier` agent for citation verification |
| **Example** | `/lit-review mixed duopoly corporate social responsibility taxation` |

Categories: directly relevant → methodological → background.

---

## Modeling Phase

### `/model` — Design Economic Model

| | |
|---|---|
| **Input** | Research problem description |
| **Output** | `Model_Setup.md` with players, timing, functions, assumptions, solution pathway |
| **Dependencies** | Wolfram Engine (tractability pre-check) |
| **Example** | `/model two-stage game: government sets tax, then Cournot competition` |

The Wolfram pre-check confirms the model is analytically solvable before you invest time in derivation.

### `/derive` — Symbolic Derivation

| | |
|---|---|
| **Input** | Model specification or derivation task |
| **Output** | Derivation results with LaTeX, Reduce[] verification, log file |
| **Dependencies** | **Wolfram Engine (mandatory)** |
| **Example** | `/derive solve the two-stage game and compute all comparative statics` |

This is the core skill. It writes `.wl` scripts following a 7-phase structure, executes them, and generates `derivation_log.txt`. Every sign claim has `Reduce[]` support. Every formula has `Simplify[derived - paper] == 0` verification.

### `/verify` — Numerical Verification

| | |
|---|---|
| **Input** | Formulas to verify, or script path |
| **Output** | `Verification_Report.md` with parameter tables |
| **Dependencies** | **Wolfram Engine (mandatory)** |
| **Example** | `/verify check Proposition 3 with c=0.3,0.5,0.7 and gamma=0.3,0.5,0.7` |

Substitutes 3+ parameter combinations. Checks: FOC=0, SOC<0, sign of comparative statics, boundary conditions.

### `/plot` — Academic Figures

| | |
|---|---|
| **Input** | What to plot, parameter values, plot type |
| **Output** | PDF vector figures in `figures/` |
| **Dependencies** | **Wolfram Engine (mandatory)** |
| **Example** | `/plot SW* as function of phi for different gamma values` |

Plot types: `Plot`, `RegionPlot`, `ContourPlot`, `Plot3D`. All figures use Frame, FrameLabel, proper font sizes, and export to PDF.

---

## Writing Phase

### `/write` — Paper Section Writing

| | |
|---|---|
| **Input** | Section name and available derivation results |
| **Output** | LaTeX section with embedded formulas and economic interpretation |
| **Dependencies** | Wolfram results (.mx or log files) |
| **Example** | `/write Section 3: Equilibrium Analysis` |

Rules: All LaTeX from `TeXForm[]`. Each Proposition gets 2-3 paragraphs of economic explanation. No "obviously", no "interestingly". Present tense for model, past tense for literature.

### `/compile` — LaTeX Compilation

| | |
|---|---|
| **Input** | `.tex` file path |
| **Output** | PDF + compilation log |
| **Dependencies** | MikTeX (pdflatex + bibtex) |
| **Example** | `/compile paper.tex` |

Runs 3-pass compilation: pdflatex → bibtex → pdflatex → pdflatex.

### `/export-word` — Word Export

| | |
|---|---|
| **Input** | `.tex` or `.md` file path |
| **Output** | `.docx` with editable formulas |
| **Dependencies** | Pandoc; optionally Wolfram (for preprocessing) |
| **Example** | `/export-word Manuscript.tex` |

Math formulas become Word-native OMML (editable, not images). Preprocessing handles incompatible LaTeX commands.

### `/proofread` — Academic English Polish

| | |
|---|---|
| **Input** | `.tex` file or section name |
| **Output** | `Proofread_Report.md` with grammar/style suggestions |
| **Dependencies** | None |
| **Example** | `/proofread Section 4` |

Checks grammar, tense consistency, academic phraseology, term consistency. Does not modify math content.

---

## Quality Phase

### `/check-refs` — Reference Verification

| | |
|---|---|
| **Input** | `.bib` file or citation list |
| **Output** | `Literature_Verification_Report.md` |
| **Dependencies** | WebSearch |
| **Example** | `/check-refs references.bib` |

Verifies each citation: author, year, journal, DOI, content alignment. Flags potentially fabricated references.

### `/check-facts` — Fact Verification

| | |
|---|---|
| **Input** | `.tex` file or specific claims |
| **Output** | `Fact_Check_Report.md` |
| **Dependencies** | WebSearch |
| **Example** | `/check-facts Introduction` |

Checks empirical claims against authoritative sources (government statistics, World Bank, academic research).

---

## Workflow Phase

### `/snapshot` — Git Version Control

| | |
|---|---|
| **Input** | Snapshot description |
| **Output** | Git commit with semantic prefix |
| **Dependencies** | git |
| **Example** | `/snapshot equilibrium derivation complete` |

Prefixes: `idea:`, `lit:`, `model:`, `derive:`, `write:`, `figure:`, `verify:`, `review:`, `compile:`, `submit:`, `revision:`, `backup:`.

### `/learn` — Capture Experience

| | |
|---|---|
| **Input** | Finding or experience to record |
| **Output** | Entry in `MEMORY.md` with `[LEARN:category]` tag |
| **Dependencies** | None |
| **Example** | `/learn FullSimplify on Abs[] expressions can timeout — use PiecewiseExpand first` |

Categories: `[LEARN:wolfram]`, `[LEARN:model]`, `[LEARN:derive]`, `[LEARN:latex]`, `[LEARN:workflow]`, `[LEARN:econ]`.

### `/revision` — Referee Response

| | |
|---|---|
| **Input** | Referee comments (PDF or text) |
| **Output** | Response plan + LaTeX Response Letter template |
| **Dependencies** | None (organizational + writing) |
| **Example** | `/revision referee_report.pdf` |

Parses comments → classifies (Major/Minor/Optional) → plans fixes → creates revision branch → generates Response Letter.

### `/submit` — Submission Preparation

| | |
|---|---|
| **Input** | Target journal name |
| **Output** | Formatted PDF + Cover Letter + `SUBMISSION_LOG.md` |
| **Dependencies** | Quality gate (must score >= 85) |
| **Example** | `/submit RAND Journal of Economics` |

### `/full-paper` — End-to-End Pipeline

| | |
|---|---|
| **Input** | Research direction |
| **Output** | Complete submission-ready paper |
| **Dependencies** | All other skills + all agents |
| **Example** | `/full-paper AI cost reduction in mixed duopoly` |

Orchestrates 10 phases with 5 user checkpoints. See [Scenarios: Full Paper](scenarios.md#8-write-a-full-paper-from-scratch) for details.
