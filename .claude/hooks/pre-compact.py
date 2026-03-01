#!/usr/bin/env python3
"""
PreCompact hook: Before context compression, remind to save critical state.
"""
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        input_data = {}

    result = {
        "reason": "[pre-compact] Context compression imminent. "
                  "BEFORE compression, please: "
                  "(1) Save any non-obvious findings to ~/.claude/MEMORY.md using [LEARN:category] tags. "
                  "(2) If there's a multi-step derivation in progress, note the current step and remaining steps. "
                  "(3) If there are critical Wolfram variable states, DumpSave them to d:/Wolf/state.mx."
    }
    json.dump(result, sys.stdout)

if __name__ == "__main__":
    main()
