---
name: pr-review-risk-plan
description: Review pull requests by collecting diff context, ranking behavioral risks, identifying missing tests, and producing verification commands. Use for non-trivial PR review, merge-readiness checks, review comment preparation, or turning review findings into a focused fix plan. Do not use for pure formatting review or to approve/merge without a human gate.
---

# PR Review Risk Plan

Use this skill for code-review stance work. Findings lead; summaries are secondary.

## Workflow

1. Collect context:
   - Identify repo root, branch, diff base, changed files, and relevant tests.
   - Read nearby code before claiming behavior is missing.
   - Preserve unrelated user changes.
2. Identify risks:
   - Prioritize bugs, regressions, security issues, data loss, missing validation, and missing tests.
   - Avoid style-only comments unless style causes behavior or maintenance risk.
   - Cite precise file lines when findings depend on code.
3. Verify findings:
   - Run focused checks when safe and available.
   - Do not run destructive commands without explicit human approval.
   - If checks cannot run, report exactly what remains unverified.
4. Produce review:
   - Findings first, ordered by severity.
   - Then open questions or assumptions.
   - Then brief change summary and test gaps.

## Inputs

- Local repo path or current working directory.
- PR URL or local diff, when available.
- User-stated review scope, if any.

## Tools And Gates

- `git`: read-only diff/status/log commands.
- `repo_read`: read changed files and related implementation.
- `github`: read metadata/comments only unless the user explicitly asks to post.
- `shell`: focused verification commands only.

Require human approval before posting a GitHub review, approving a PR, merging, force pushing, or running destructive shell commands.

## Failure Modes

- If the diff is too large, summarize the reviewable scope and ask for narrowing.
- If tests are unavailable, report unverified findings and missing commands.
- If GitHub is unavailable, continue from local diff and mark remote metadata missing.

## Done When

- Ranked findings include concrete evidence or state that no issues were found.
- Verification commands and results are fresh from the current session, or explicitly marked not run.
- Residual risks and assumptions are visible.

This skill is typically invoked **inside** the `review-gate` pattern when an agent wants to land changes. Use review-gate for the human approval orchestration.
