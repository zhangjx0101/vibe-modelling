# Quick Start

Get up and running in 5 minutes.

## Prerequisites

| Tool | Purpose | Install |
|---|---|---|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | AI orchestration | `npm install -g @anthropic-ai/claude-code` |
| [Wolfram Engine](https://www.wolfram.com/engine/) | Symbolic computation | Free for developers |
| [MikTeX](https://miktex.org/) or TeX Live | LaTeX compilation | Platform-specific |
| [Pandoc](https://pandoc.org/) | Word/PDF export | `choco install pandoc` or [download](https://pandoc.org/installing.html) |

## Step 1: Clone the Repo

```bash
git clone https://github.com/zhangjx0101/vibe-modelling.git
cd vibe-modelling
```

## Step 2: Configure Wolfram Engine Path

The default path is `/d/Wolf/wolframscript.exe`. If yours is different, update it in your project's `CLAUDE.md`:

```markdown
## Wolfram Engine
- Path: `/your/path/to/wolframscript`
```

## Step 3: Create Your Project

```bash
mkdir "project/My New Paper"
cd "project/My New Paper"
```

## Step 4: Launch Claude Code

```bash
claude
```

All skills, agents, and rules are automatically loaded from `.claude/`.

## Step 5: Start Working

Try these common commands:

```
> /model Cournot duopoly with AI cost reduction
> /derive solve the two-stage game
> /verify check all propositions with 3 parameter sets
> /write Section 3: Equilibrium Analysis
> /compile
```

Or simply describe what you want in natural language:

```
> Help me design a mixed duopoly model where a public firm competes with a private firm
> Verify that all formulas in my paper are correct
> Export my paper to Word for my coauthor
```

## Top 5 Commands for Daily Use

| Command | What it does |
|---|---|
| `/derive` | Run Wolfram Engine to solve your model symbolically |
| `/verify` | Numerically verify results with multiple parameter sets |
| `/write` | Write a paper section with embedded LaTeX formulas |
| `/compile` | Compile LaTeX to PDF |
| `/export-word` | Convert to editable Word document |

## What's Next?

- See [Scenarios](scenarios.md) to find the right tools for your specific task
- See [Examples](examples.md) for complete workflow walkthroughs
