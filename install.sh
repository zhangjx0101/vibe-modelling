#!/bin/bash
# Vibe Modelling — Install Script
# Copies workflow files to your project directory's .claude/ folder.
#
# Usage:
#   ./install.sh                    # Install to current directory
#   ./install.sh /path/to/project   # Install to specified directory

TARGET="${1:-.}"

if [ ! -d ".claude" ]; then
  echo "Error: .claude/ not found. Run this script from the vibe-modelling repo root."
  exit 1
fi

mkdir -p "$TARGET/.claude/skills" "$TARGET/.claude/agents" "$TARGET/.claude/rules" "$TARGET/.claude/hooks"

cp -r .claude/skills/* "$TARGET/.claude/skills/"
cp .claude/agents/*.md "$TARGET/.claude/agents/"
cp .claude/rules/*.md "$TARGET/.claude/rules/"
cp .claude/hooks/*.py "$TARGET/.claude/hooks/"
cp .claude/WORKFLOW_QUICK_REF.md "$TARGET/.claude/" 2>/dev/null

echo "Vibe Modelling installed to $TARGET/.claude/"
echo ""
echo "Skills:  $(ls "$TARGET/.claude/skills/" | wc -l)"
echo "Agents:  $(ls "$TARGET/.claude/agents/" | wc -l)"
echo "Rules:   $(ls "$TARGET/.claude/rules/" | wc -l)"
echo "Hooks:   $(ls "$TARGET/.claude/hooks/" | wc -l)"
echo ""
echo "Note: You may need to configure hooks in your .claude/settings.json"
echo "See README.md for details."
