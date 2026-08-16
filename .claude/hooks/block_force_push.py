"""PreToolUse hook: OpenApex history is append-only — block any force push.

Receives the tool-call JSON on stdin; exit code 2 blocks the action and sends
stderr back to the model. AGENTS.md states the rule; this hook enforces it.
"""

import json
import re
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = data.get("tool_input", {}).get("command", "")
    if re.search(r"\bpush\b", command) and re.search(r"(--force(-with-lease)?\b|\s-f\b)", command):
        print(
            "Blocked: OpenApex history is append-only (see AGENTS.md). "
            "Force pushes are forbidden; add a new commit instead.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
