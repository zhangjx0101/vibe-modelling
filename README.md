<p align="center">
  <img src="assets/logo-placeholder.png" alt="Vibe Modelling" width="200">
</p>

<h1 align="center">Vibe Modelling</h1>

<p align="center">
  <strong>Claude Code workflow for theoretical economics papers — from idea to submission.</strong>
</p>

<p align="center">
  <a href="#installation"><img src="https://img.shields.io/badge/claude--code-workflow-blue?style=flat-square&logo=anthropic" alt="Claude Code"></a>
  <a href="https://www.wolfram.com/engine/"><img src="https://img.shields.io/badge/wolfram-engine%2014-red?style=flat-square&logo=wolfram" alt="Wolfram Engine"></a>
  <a href="#prerequisites"><img src="https://img.shields.io/badge/LaTeX-MikTeX%20%7C%20TeX%20Live-green?style=flat-square&logo=latex" alt="LaTeX"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square" alt="License"></a>
  <a href="https://github.com/zhangjx0101/vibe-modelling/stargazers"><img src="https://img.shields.io/github/stars/zhangjx0101/vibe-modelling?style=flat-square" alt="Stars"></a>
</p>

<p align="center">
  <a href="#what-it-does">What It Does</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#installation">Installation</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#customization">Customization</a>
</p>

---

## What is Vibe Modelling?

**Vibe Modelling = Vibe Coding for Economic Theory.**

Instead of writing code, you "vibe" your way through model design, symbolic derivation, and paper writing, with Claude Code orchestrating the entire process and Wolfram Engine handling all the math.

> **LLM thinks. CAS computes. Never the other way around.**

| Task | Who | Tool |
|---|---|---|
| Model design, assumptions, intuition | Claude | Natural language |
| Solve equations, simplify, derivatives | Wolfram Engine | `Solve[]`, `D[]`, `Simplify[]` |
| Sign determination, monotonicity | Wolfram Engine | `Reduce[expr > 0, ...]` |
| LaTeX formulas | Wolfram Engine | `ToString[TeXForm[...]]` |
| Economic interpretation | Claude | Paper writing |
| Adversarial review | Claude Agents | math-critic, referee-sim |

**Zero tolerance for hand-waving math.** Every sign claim must have `Reduce[]` output. Every formula must have `TeXForm[]` source. Every derivation must pass numerical verification.

## What It Does

```
/idea       →  Brainstorm research questions           💡
/study      →  Deep-read a paper, extract techniques   📖
/lit-review →  Systematic literature search             📚
/model      →  Design game-theoretic models             🏗️
/derive     →  Symbolic derivation (Wolfram Engine)     🔢
/verify     →  Numerical verification (3+ param sets)   ✅
/plot       →  Academic figures (PDF vector)             📊
/write      →  Write paper sections (journal norms)     ✍️
/compile    →  LaTeX → PDF compilation                  📄
/proofread  →  Academic English polish                  🔤
/check-refs →  Verify references aren't hallucinated    📎
/check-facts→  Fact-check empirical claims              🔍
/snapshot   →  Git version snapshots                    📦
/submit     →  Submission preparation                   📮
/revision   →  Referee response management              📝
/full-paper →  End-to-end pipeline                      🚀
```

## Quick Start

```bash
git clone https://github.com/zhangjx0101/vibe-modelling.git
cd vibe-modelling
mkdir "My New Paper"
cd "My New Paper"
claude
```

Then in Claude Code:

```
> /model Cournot duopoly with AI cost reduction
> /derive solve the two-stage game
> /write Section 3: Equilibrium Analysis
> /compile
```

## Workflow Overview

```
/idea → /study → /lit-review → /model → /derive → /verify → /plot
                                                        ↓
                            /submit ← quality-gates ← /write + /compile
                                                        ↓
                                        math-critic ↔ math-fixer (≤5 rounds)
                                        econ-reviewer
                                        referee-sim
                                        proofreader
                                        lit-verifier + fact-checker
                                        latex-auditor
```

## Architecture

```
.claude/
├── skills/          17 slash commands (invoked on demand)
│   ├── derive/      Wolfram symbolic derivation
│   ├── verify/      Numerical verification
│   ├── write/       Paper writing
│   └── ...
│
├── agents/          8 specialized reviewers
│   ├── math-critic  Read-only math auditor (finds errors)
│   ├── math-fixer   Read-write math repair (fixes errors)
│   ├── econ-reviewer Economics logic review
│   ├── referee-sim  Simulated Referee 2 (adversarial)
│   ├── proofreader  Academic English
│   ├── lit-verifier Reference authenticity
│   ├── fact-checker Empirical claims
│   └── latex-auditor LaTeX format audit
│
├── rules/           8 governance policies
│   ├── wolfram-first       All math through Wolfram
│   ├── verify-before-claim Reduce[] before sign claims
│   ├── quality-gates       100-point scoring system
│   └── ...
│
└── hooks/           4 automatic triggers
    ├── verify-reminder     Post-Wolfram verification nudge
    ├── pre-compact         Save state before compression
    └── ...
```

### Adversarial Math Review

Inspired by [Sant'Anna's workflow](https://github.com/pedrohcgs/claude-code-my-workflow), the math review uses a **critic-fixer loop**:

```
math-critic (read-only, finds problems)
    ↕  up to 5 rounds
math-fixer  (read-write, fixes problems with Wolfram verification)
```

The critic cannot fix. The fixer cannot self-approve. Neither can skip Wolfram verification.

### Quality Gates

100-point scoring system. Every paper is scored before submission:

| Violation | Penalty |
|---|---|
| Unverified sign claim (no `Reduce[]`) | −50 |
| LaTeX compilation failure | −100 |
| Missing numerical verification | −20 |
| Proposition without economic interpretation | −15 |
| Math symbols in Abstract/Introduction | −10 |
| Fabricated reference | −30 |
| Unverified SOC | −20 |

**≥ 85** → ready to submit · **70–84** → submit with warnings · **< 70** → blocked

## Prerequisites

| Tool | Purpose | Install |
|---|---|---|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | AI orchestration | `npm install -g @anthropic-ai/claude-code` |
| [Wolfram Engine](https://www.wolfram.com/engine/) | Symbolic computation | Free for developers |
| [MikTeX](https://miktex.org/) or TeX Live | LaTeX compilation | Platform-specific |

## Installation

### Option A: Clone as project parent (recommended)

Clone this repo and put your economics projects inside it:

```bash
git clone https://github.com/zhangjx0101/vibe-modelling.git
cd vibe-modelling

# Your projects go here as subfolders:
mkdir "20260301 My New Paper"
cd "20260301 My New Paper"
claude   # Skills, agents, rules automatically available
```

### Option B: Copy to existing project

```bash
git clone https://github.com/zhangjx0101/vibe-modelling.git
cd vibe-modelling
./install.sh /path/to/your/project
```

### Option C: Global installation

Copy to `~/.claude/` for all projects:

```bash
git clone https://github.com/zhangjx0101/vibe-modelling.git
cd vibe-modelling
./install.sh ~/.claude
```

### Configure Wolfram Engine path

Edit your project's `CLAUDE.md` to set the Wolfram Engine path:

```markdown
## Wolfram Engine
- Path: `"/path/to/wolframscript" -code "..."`
- Script execution: `"/path/to/wolframscript" -file "script.wl"`
```

## Target Journals

The writing rules are calibrated for top IO/micro theory journals:

- **AER** (American Economic Review)
- **RAND** (RAND Journal of Economics)
- **JIE** (Journal of Industrial Economics)
- **JET** (Journal of Economic Theory)
- **GEB** (Games and Economic Behavior)
- **IJIO** (International Journal of Industrial Organization)

## Customization

### Add a new Skill

Create `.claude/skills/my-skill/SKILL.md`:

```yaml
---
name: my-skill
description: What this skill does
argument-hint: [expected input]
---

# My Skill

Instructions for Claude...
```

### Add a new Agent

Create `.claude/agents/my-agent.md`:

```yaml
---
model: haiku
tools: Read, Grep, Glob
---

# My Agent

Role and instructions...
```

### Add a new Rule

Create `.claude/rules/my-rule.md`:

```yaml
---
description: What this rule enforces
---

# My Rule

Rules and constraints...
```

## Acknowledgments

- Inspired by [Pedro Sant'Anna's Claude Code workflow](https://github.com/pedrohcgs/claude-code-my-workflow) for empirical economics
- Built with [Claude Code](https://claude.ai/claude-code) and [Wolfram Engine](https://www.wolfram.com/engine/)

## License

MIT
