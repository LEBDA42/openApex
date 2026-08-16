---
name: fix-issue
description: Fix a GitHub issue end to end — reproduce with a failing test, fix, verify the gates, prepare the commit.
disable-model-invocation: true
argument-hint: <issue-number-or-url>
---

# Fixing issue $ARGUMENTS

1. Read the issue: `gh issue view $ARGUMENTS` (or fetch the URL if `gh` is not
   installed).
2. **Reproduce first**: write a failing test that captures the reported
   behavior. No fix without a red test.
3. Fix with the smallest change that respects CLAUDE.md and `.claude/rules/`.
   If the fix touches a metric, follow the `new-metric` skill doctrine.
4. Run the three gates (commands in CLAUDE.md) — all green.
5. Ask the `code-reviewer` subagent (and `science-reviewer` if a metric
   changed) to review the diff; address findings.
6. Commit: imperative subject, body explains the root cause and references the
   issue (`Fixes #N`).
