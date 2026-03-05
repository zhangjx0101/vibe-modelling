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
mkdir -p "project/my-paper-short-name"
cd "project/my-paper-short-name"
```

### Recommended Directory Structure

As your project grows, use this layout:

```
my-paper-short-name/
├── CLAUDE.md                    # Project context (Claude Code reads this automatically)
├── Manuscript.md                # Original manuscript (Markdown)
├── Manuscript_corrected.md      # Wolfram-verified corrected version
├── original-paper.docx          # Original Word file (if converting)
├── derivations/                 # Wolfram scripts and logs
│   ├── derive_all.wl            # Main derivation (backward induction)
│   ├── derivation_log.txt       # Auto-generated run log
│   ├── verify_*.wl              # Verification scripts
│   └── verification_log.txt     # Verification run log
├── quality_reports/             # Review and verification reports
│   └── verification_report.md   # Equation-by-equation PASS/FAIL
├── figures/                     # Generated figures
│   ├── Figure1.pdf              # Vector format for LaTeX
│   └── Figure1.png              # Raster format for Word
└── media/                       # Images extracted from docx
    └── image1.png
```

**You don't need to create all folders upfront.** Claude Code creates them as needed when you run `/derive`, `/verify`, `/plot`, etc.

**A template `CLAUDE.md`** is available at [`assets/project-claude-template.md`](../assets/project-claude-template.md). Copy it into your project and fill in the details — this helps Claude Code remember your project context across sessions.

### Working with a Private Git Repo

If you want version history for your research (recommended), create a separate **private** repo:

```bash
# In your project parent directory
cd project/my-author-name
git init
gh repo create my-research --private
git remote add origin https://github.com/you/my-research.git

# Copy workflow rules so they work inside the new git boundary
mkdir -p .claude/rules
cp ../../.claude/rules/*.md .claude/rules/

git add .
git commit -m "init: add research projects"
git push -u origin master
```

See [Troubleshooting > Nested git repos](troubleshooting.md#nested-git-repos-break-rules-inheritance) for why the rules copy is needed.

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
