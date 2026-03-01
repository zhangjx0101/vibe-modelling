#!/usr/bin/env python3
"""
Stop hook: Remind to log session findings before ending.
"""
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        input_data = {}

    result = {
        "reason": "[log-reminder] Session ending. "
                  "Before closing: did you discover anything non-obvious this session? "
                  "If so, consider using /learn to save it to MEMORY.md. "
                  "Key things to log: Wolfram tips, parameter constraints, model insights, dead ends."
    }
    json.dump(result, sys.stdout)

if __name__ == "__main__":
    main()
