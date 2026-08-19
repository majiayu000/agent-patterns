---
name: skill-lifeguard
description: "Create, audit, and harden skills so they become self-maintaining instead of cat-and-mouse. Use when designing new skills, reviewing existing ones for drift, or turning brittle workflows into reliable ones. Forces Negative Examples, Verification Checkpoints, machine-checkable Done conditions, Replay/smoke test hooks, and Drift signal detection. Do not use for one-off prompts."
---

# Skill Lifeguard (Reliable Skill Pattern)

Use this skill to stop the "today it works, tomorrow the model invents a new way to break the rules" problem.

Skills that only contain positive instructions rot. Reliable skills ship with explicit guardrails, objective verification, and self-diagnosis signals so they can be updated from their own failure logs instead of constant manual babysitting.

This pattern is the contract that every high-value skill in the library should follow.

## The Reliable Skill Contract (Mandatory Elements)

Every skill produced or audited under this pattern **must** contain all five elements. Absence of any element is a failure during audit.

1. **Explicit Negative Examples**
   - A dedicated section listing what the skill must **never** do.
   - Include real failure modes observed in the wild (e.g. "never rewrite tests to make the run pass", "never use full file content when path + summary is enough").
   - Format: bullet list with "FORBIDDEN" or "Negative:" prefix.

2. **Verification Checkpoints**
   - After every major phase or risky step, define a concrete pass/fail check.
   - Must be executable where possible (commands, file existence + content assertions, git status predicates).
   - Example: "After edits: run `python3 -m pyright src/` and `pytest tests/related_test.py::test_xxx -q --tb=line`. Both must be green before proceeding."

3. **Clear Done Conditions (Machine-Checkable)**
   - Explicit list of "Done When" criteria that can be verified without human narrative.
   - Prefer fresh command output over "the file looks correct".
   - Include both happy path and at least one failure-to-complete signal.
   - Must appear in the Done When section of the skill.

4. **Replay / Smoke Test Hooks + Log Analysis for Patch Suggestions**
   - Provide (or reference) a way to replay previous runs.
   - Include guidance on how to turn run logs / failure traces into concrete skill patches.
   - Recommended structure:
     - `scripts/replay-skill.sh <log-or-session>` (or equivalent)
     - A "From Failure to Patch" subsection that maps common log patterns → exact edits in the skill.
   - At minimum, the skill must say: "Collect the exact failing command + output. Add a Negative Example or Checkpoint. Update the Done When if the success criteria were too loose."

5. **Drift Signal Detection**
   - Define observable signals that this skill is starting to rot.
   - Examples:
     - Same failure pattern appears on 3+ independent runs without the skill catching it.
     - Agent starts ignoring a previously respected Negative Example.
     - Context bloat or repeated "I already did X" loops on tasks this skill governs.
     - Verification commands start failing in new environments while the skill claims success.
   - The skill must instruct the user/agent: "When any drift signal fires, run this skill again on itself and produce a patch proposal."

## Workflow (When Using This Pattern)

1. **Audit existing skill**
   - Check against the 5 elements above.
   - Score 0-5. Anything below 4 needs immediate hardening.

2. **Design / Harden a skill**
   - Start from the contract sections.
   - Write Negative Examples first (they are the cheapest guard).
   - Define 2-4 concrete checkpoints + Done conditions.
   - Add at least one smoke/replay path.
   - Document the 2-3 most likely drift signals.

3. **Make it self-updating**
   - Add a short "Maintenance" subsection:
     "After any run that required manual correction, append the correction as either a Negative Example or a new Checkpoint. Prefer editing the skill over editing the prompt in the session."

4. **Human gate for high-risk skills**
   - Skills that control writes, deploys, money, or production changes must declare `requires_human_gate: true` in their manifest and require explicit approval before the gate is passed.

## Template to Insert Into Any Skill (Copy & Adapt)

```markdown
## Negative Examples
- FORBIDDEN: Do not ...
- Never treat a previous verification as current truth.
- ...

## Verification Checkpoints
After <phase>:
- Command: `...`
- Must be: exit 0 + specific string in output
- On fail: stop and report raw output

## Done When
- All checkpoints green
- `git status --short` shows only the expected files
- `pytest ... -q` reports X passed
- Fresh evidence from this session only

## Replay & Patch Process
1. Collect the session log or failing commands.
2. Run the replay hook if available.
3. Map failure → exact addition to Negative Examples or Checkpoints.
4. Update Done When if the success bar was too low.
5. Re-test the skill on a similar task.

## Drift Signals
- The same wrong pattern is repeated 3 times.
- Agent starts skipping a checkpoint that used to be enforced.
- ...
```

## Integration With Other Patterns

- Use together with `context-handoff-pack`: every reliable skill checkpoint must be recorded in the handoff.
- Use with `review-gate` (see sibling pattern): before landing changes produced while following a skill, run the review gate.
- Use with `flowguard`: long-running reliable skills must declare their stop_conditions and objective re-verify rule.

## Done When (for this meta-skill itself)

- The audited or newly created skill contains all 5 contract elements in a machine-usable form.
- There is at least one concrete, runnable verification command or assertion.
- A drift signal + corresponding update path is documented.
- The resulting skill can be re-run on its own past failure logs to produce a non-trivial improvement without full manual rewrite.

## Failure Modes

- Skill only lists positive steps → treat as incomplete.
- Checkpoints are narrative only ("make sure it looks good") → force rewrite to executable form.
- No path from failure log → skill edit → mark as high babysitting risk.
- Ignores its own drift signals after 3 uses → this pattern must be re-applied to the skill.
