#!/usr/bin/env python3
"""
PostCompact hook: After context compression, suggest restoring state.
"""
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        input_data = {}

    result = {
        "reason": "[post-compact] Context was compressed. "
                  "To restore state: "
                  "(1) Read ~/.claude/MEMORY.md for cross-session knowledge. "
                  "(2) Check if d:/Wolf/state.mx exists for Wolfram state. "
                  "(3) Review the todo list for pending tasks. "
                  "(4) Read the plan file if one exists."
    }
    json.dump(result, sys.stdout)

if __name__ == "__main__":
    main()
