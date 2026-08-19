---
name: context-handoff-pack
description: Create compact, evidence-backed handoff packs for long-running agent tasks. Use before context compaction, Codex/Claude session handoff, task resumption, or when the user asks for exact current status across files, constraints, tests, decisions, blockers, next action, and local session-history evidence. Do not use for trivial one-command tasks with no durable state.
---

# Context Handoff Pack

Use this skill to preserve exact task state without inventing progress.

## Workflow

1. Re-state objective + plan (mandatory before any state collection or major step):
   - Write one clear sentence of the **primary objective**.
   - Write a numbered plan of **no more than 5 steps**.
   - After each significant step or before compaction, re-verify that current work still supports the objective.
   - If the work has drifted, stop and clarify before continuing.

2. Collect state:
   - Confirm current cwd/repo root and whether it is a git repo.
   - List modified files, created files, deleted files, generated artifacts, and relevant untracked files.
   - Capture active constraints, user decisions, and current priority.
   - If resuming a Codex task, run the Codex probe helper to identify matching local sessions:

```sh
python3 skills/context-handoff-pack/scripts/codex_handoff_probe.py --cwd "$PWD" --limit 8
```

3. Collect evidence:
   - Record commands run in the current session and their results.
   - Record verification that passed, failed, or was not run.
   - Link exact local paths and line anchors when useful.
   - If local session-history evidence is used, cite the source paths and session ids, not raw transcripts.
4. Detect context risks + run Context Audit:
   - Identify missing evidence, stale assumptions, unresolved questions, repeated failure loops, and blocked external state.
   - Use blank/unknown when data is unavailable; do not infer state.
   - Treat historical Codex/Claude logs as hints only; verify live repo, runtime, GitHub, and tests before claiming current state.
   - **Context Audit**: explicitly list garbage (old failed attempts, full irrelevant tool output, contradictory summaries, bloated previous plans). Mark items for externalization or deletion.
5. Apply Context Engineering practices (when relevant):
   - Prefer external scratchpad or memory blocks for long-lived facts, decisions, and TODOs instead of keeping everything in the window.
   - Before compaction: decide what must be written out (scratchpad files, handoff, memory blocks).
   - Use compaction only at logical boundaries (see compaction policy below).
6. Assemble handoff:
   - Goal (with fresh one-sentence primary objective).
   - Current state.
   - Modified files.
   - Constraints and decisions.
   - Verification.
   - Blockers and next action.
   - Session-history evidence used, if any.
   - Context audit summary (what was cleaned or externalized).

## Codex Resume Adapter

Use the Codex adapter when the user says "continue", "what were we doing", asks after compaction, or asks for exact state from prior Codex sessions.

1. Run `scripts/codex_handoff_probe.py` with the current cwd.
2. Inspect the returned matching sessions, signal counts, and rollout paths.
3. If the match is ambiguous, narrow by `--session-id`, repo path, or timestamp before reading deeper.
4. Read only the smallest relevant rollout/history slice needed to recover state.
5. Keep raw user text out of the handoff unless the user explicitly needs it; use `--include-text` only for short redacted excerpts.

The probe can show likely verification, blocker, runtime, GitHub, publish, handoff, and skill signals. It does not prove current truth.

## Compaction Policy

Compact only at logical boundaries. Never mid-implementation.

| Boundary                  | Compact? | What to keep in window                  | What to externalize / drop                     |
|---------------------------|----------|-----------------------------------------|------------------------------------------------|
| Exploration → Planning    | Yes      | Primary objective + top decisions       | Full search history, raw tool output           |
| Planning → Implementation | Yes      | Plan + constraints + current files      | Detailed planning traces                       |
| Mid-implementation        | No       | All relevant implementation context     | —                                              |
| After verification        | Optional | Evidence + blockers                     | Old failed attempts (keep only root cause)     |
| Task complete → next task | Yes      | Summary handoff only                    | Everything else                                |

Always produce or update a handoff / scratchpad before compaction.

Recommended external forms:
- Scratchpad files in the repo (e.g. `.agent/scratchpad.md`)
- Memory blocks / long-term notes outside the active context
- The handoff pack itself

## Required Fields

- Goal (fresh one-sentence primary objective + <=5 step plan).
- Relevant paths/artifacts.
- Constraint set.
- Key decisions.
- Verification commands and results.
- Current priority and next action.
- Session id, rollout path, and local-history source when history was used.
- Context audit summary (garbage identified + externalized items).

## Safety

- Exclude secrets, tokens, cookies, and private keys.
- Preserve exact machine identifiers and paths.
- Do not claim completion without fresh verification.
- If there is no data for a field, leave it blank or mark it unknown.
- Redact raw local chat excerpts by default.

## Failure Modes

- If the workspace is unavailable, report blocked with the missing path.
- If Codex history files are unavailable, continue with live workspace evidence and mark session-history evidence unknown.
- If multiple Codex sessions match the same cwd, report ambiguity and use the most recent session only as a starting point.
- If verification was not run, list the required commands as pending.
- If a secret appears in context, redact it and report that redaction occurred.
- If objective re-statement or context audit was skipped on a long-running task, mark the handoff as high-drift-risk.

## Usage as Lightweight Guard

Other skills can call this pattern (or its logic) at key nodes:
- Before/after compaction
- At every major phase boundary
- Before handing off to another agent or session
- When the user says "continue", "what were we doing", or "compact"

It is intentionally lightweight so it can be embedded or referenced from flowguard-style long-task guards and review gates.

## Done When

- A new agent can continue the task without re-discovering basic state.
- The handoff distinguishes completed work from assumptions and pending work.
- The next action is singular, concrete, and testable.
- Any local-history evidence is scoped to exact session ids and source paths.
- Primary objective was re-stated and verified in the last checkpoint.
- Context audit was performed; garbage and externalized items are explicitly listed.

## Resources

- `scripts/codex_handoff_probe.py`: aggregate local Codex history for the current cwd without printing raw text by default.
