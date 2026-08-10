---
name: review-gate
description: "Force an explicit review step before any agent-generated diff is applied, committed, or landed. Collect diff, run risk analysis, produce a review pack, and require human approval of the plan and risks. Use before git commit, push, PR creation, or direct application of changes produced by long-running agent work. Strongly recommended together with skill-lifeguard and context-handoff-pack."
---

# Review Gate

"Diff first, review second, land only after explicit human gate."

Many users report that agent speed is high but review cost is even higher, and "just trusting the agent" leads to unmaintainable garbage or silent regressions. This gate makes the review step a first-class, enforceable part of the workflow.

## When To Use

- Agent has proposed or produced code changes.
- Before any commit, push, PR, or direct application of edits.
- After a flowguard / skill-lifeguard protected task reaches a "ready to land" checkpoint.
- When the user says "apply", "commit", "land", "push", or "make the PR".

Do **not** use for pure read-only or exploratory work.

## Workflow

1. **Freeze further edits**
   - Announce the review gate boundary.
   - Do not make additional changes until the gate is passed.

2. **Collect the diff and context**
   - Run `git diff` (staged + unstaged) and `git status`.
   - Capture the original goal / handoff (from context-handoff-pack if available).
   - Note which skill(s) drove the changes (from skill-lifeguard if used).

3. **Run risk analysis**
   - Prefer `pr-review-risk-plan` (or equivalent) on the changed surface.
   - Prioritize: behavior change, missing tests, security, data loss, breaking contracts, scope creep.
   - Cite exact files and lines.

4. **Produce Review Pack** (must be human-readable in one shot)
   - Summary of intent vs actual diff.
   - Ranked findings (high/medium/low).
   - Missing verification commands or tests.
   - Open questions and assumptions.
   - Recommended next action (apply as-is / fix specific items / discard).

5. **Human Gate**
   - Present the Review Pack.
   - Ask for explicit approval: "Approve this diff + plan?" or "Approve with these changes required first?"
   - Only after clear human "yes" (or edited approval) may the changes be committed/landed/applied.
   - Record the approval decision in the current handoff or session log.

6. **Record & resume**
   - Update the handoff with review outcome.
   - If fixes were required, loop back with the review findings as new constraints.

## Required Artifacts

- The raw diff at gate time.
- The Review Pack (findings + verification gaps).
- Human approval record (timestamp + decision + any required fixes).
- Link to the originating handoff / skill-lifeguard contract.

## Human Gate Rules

This skill **always** requires a human gate for the following actions:
- `git commit`
- `git push`
- Creating or updating a PR
- Directly applying edits that touch production paths, tests, or contracts

No silent application is allowed.

## Integration With Other Patterns

- **skill-lifeguard**: Skills that reach "done" must still pass this gate before their changes land.
- **context-handoff-pack**: The handoff at the time of the gate must be included or referenced.
- **pr-review-risk-plan**: This gate is the orchestration layer; delegate detailed risk ranking to it.
- **flowguard** / long tasks: Insert a review gate at the final "ready to land" checkpoint.

## Done When

- A complete Review Pack has been produced and shown to the human.
- Explicit human approval (or conditional approval) has been recorded.
- If fixes were required, they are either done or explicitly accepted as deferred.
- No further edits happen until the gate decision is made.

## Failure Modes

- Agent tries to commit/push without presenting a Review Pack → block and re-enter the gate.
- Human approval is vague ("looks ok") → ask for explicit "I approve the diff and plan as-is".
- Diff is too large for meaningful review → require narrowing scope or multiple gates.
- Review findings are ignored on subsequent runs → treat as drift signal for the driving skill.

## Recommended Invocation (for other skills)

When a skill reaches a point where it wants to apply changes:

```
1. Produce the intended changes (but do not commit/apply yet).
2. Call review-gate.
3. Only after human gate passes, perform the commit/land step.
4. Record the gate result in the handoff.
```

This turns "agent wrote it" into "agent wrote it + it survived explicit review".
