---
name: context-handoff-pack
description: Create compact, evidence-backed handoff packs for long-running agent tasks. Use before context compaction, model/session handoff, task resumption, or when the user asks for exact current status across files, constraints, tests, decisions, blockers, and next action. Do not use for trivial one-command tasks with no durable state.
---

# Context Handoff Pack

Use this skill to preserve exact task state without inventing progress.

## Workflow

1. Collect state:
   - Confirm current cwd/repo root and whether it is a git repo.
   - List modified files, created files, deleted files, generated artifacts, and relevant untracked files.
   - Capture active constraints, user decisions, and current priority.
2. Collect evidence:
   - Record commands run in the current session and their results.
   - Record verification that passed, failed, or was not run.
   - Link exact local paths and line anchors when useful.
3. Detect context risks:
   - Identify missing evidence, stale assumptions, unresolved questions, repeated failure loops, and blocked external state.
   - Use blank/unknown when data is unavailable; do not infer state.
4. Assemble handoff:
   - Goal.
   - Current state.
   - Modified files.
   - Constraints and decisions.
   - Verification.
   - Blockers and next action.

## Required Fields

- Goal or user request.
- Relevant paths/artifacts.
- Constraint set.
- Key decisions.
- Verification commands and results.
- Current priority and next action.

## Safety

- Exclude secrets, tokens, cookies, and private keys.
- Preserve exact machine identifiers and paths.
- Do not claim completion without fresh verification.
- If there is no data for a field, leave it blank or mark it unknown.

## Failure Modes

- If the workspace is unavailable, report blocked with the missing path.
- If verification was not run, list the required commands as pending.
- If a secret appears in context, redact it and report that redaction occurred.

## Done When

- A new agent can continue the task without re-discovering basic state.
- The handoff distinguishes completed work from assumptions and pending work.
- The next action is singular, concrete, and testable.
