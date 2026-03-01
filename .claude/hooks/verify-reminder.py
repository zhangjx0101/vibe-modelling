#!/usr/bin/env python3
"""
PostToolUse hook: After Wolfram calls, remind about verification.
Triggers when Bash tool is used with wolframscript.
"""
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only trigger for Bash tool calls involving wolframscript
    if tool_name != "Bash":
        return

    command = tool_input.get("command", "")
    if "wolframscript" not in command:
        return

    # Check if this is a Solve/Reduce/derivation call
    derivation_keywords = ["Solve[", "DSolve[", "D[", "Integrate[", "FullSimplify["]
    is_derivation = any(kw in command for kw in derivation_keywords)

    if is_derivation:
        # Check if verification keywords are present
        has_verify = "Reduce[" in command or "verify" in command.lower()

        if not has_verify:
            result = {
                "reason": "[verify-reminder] Wolfram derivation detected. "
                          "Remember: use Reduce[] to verify sign claims, "
                          "and consider numerical verification with 3+ parameter sets."
            }
            json.dump(result, sys.stdout)

if __name__ == "__main__":
    main()
