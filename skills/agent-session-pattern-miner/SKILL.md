---
name: agent-session-pattern-miner
description: Mine local Codex and Claude chat/session records into reusable agent workflow candidates. Use when the user asks to inspect agent chat history, find repeatable workflows, decide what should become a skill, compare new-skill candidates against existing skills, or avoid turning one-off logs into hardcoded scripts. Do not use to publish raw private conversations or secrets.
---

# Agent Session Pattern Miner

Use this skill to turn local agent history into a ranked skill backlog without exposing raw chat logs by default.

## Workflow

1. Define scope:
   - Confirm whether to inspect Codex, Claude, or both.
   - Use default local sources unless the user gives explicit alternate paths.
   - Treat local chats as private evidence; aggregate first, quote only when necessary.
2. Search first:
   - List existing repo skills and manifests.
   - List installed local skills if the user asks whether a candidate already exists.
   - Mark each finding as `new skill`, `enhance existing skill`, `reference-only`, or `not worth packaging`.
3. Mine local records:
   - Run the helper when available:

```sh
python3 skills/agent-session-pattern-miner/scripts/mine_agent_sessions.py --source both
```

   - Use `--source codex` or `--source claude` for a narrower pass.
   - Use `--format json` when another script or test needs structured output.
   - Do not use `--include-examples` unless raw excerpts are necessary and safe to show.
4. Normalize findings into workflow candidates:
   - Trigger phrase or task shape.
   - Repeat count and session spread.
   - Affected repos or project families.
   - Existing skill overlap.
   - Risk level, human gates, and verification needs.
5. Rank by leverage:
   - High frequency across repos beats one large session.
   - Workflows with repeated verification or release risk outrank content-only variants.
   - Enhance an existing skill when the trigger and procedure already match.
   - Create a new skill only when the trigger, workflow, gates, and done-when differ.
6. Report:
   - Start with the top 3-7 candidates.
   - For each, state `action`, `why now`, `suggested skill name`, and `first implementation slice`.
   - Separate evidence from interpretation.
   - Say when the scan is partial or a source was unavailable.

## Candidate Rules

- `new skill`: repeated task shape, clear trigger, reusable workflow, and a distinct done-when.
- `enhance existing skill`: same trigger and workflow family, but missing source adapter, gate, test, or helper.
- `reference-only`: useful background that does not need a separate invocation surface.
- `not worth packaging`: one-off task, project-specific detail, or unstable behavior that has not been manually validated.

## Local Sources

- Codex user history: `~/.codex/history.jsonl`.
- Codex thread titles: `~/.codex/session_index.jsonl`.
- Codex rollout metadata: `~/.codex/sessions/**/rollout-*.jsonl`.
- Claude Code project logs: `~/.claude/projects/**/*.jsonl`.
- Claude Code task records: `~/.claude/tasks/**/*.json`.

When a source format is unknown, inspect a small sample first and update the extraction logic only after confirming the actual fields.

## Safety

- Redact or omit secrets, tokens, cookies, keys, and private customer data.
- Aggregate by default; do not paste raw chat transcripts.
- Do not create or edit skills unless the user asks to implement the candidates.
- Do not treat historical logs as current truth; verify live repo, GitHub, runtime, and test state before claiming anything landed.

## Failure Modes

- If a history path is missing, report it as unavailable and continue with remaining sources.
- If records cannot be parsed, report the file count and parse error class without dumping file contents.
- If candidate evidence is dominated by one repo, label it project-specific until another repo confirms reuse.
- If an existing skill already covers the workflow, recommend enhancement instead of a duplicate.

## Done When

- The report identifies which workflows should become skills, which existing skills should be enhanced, and which findings should be ignored.
- Each recommended action has evidence counts, source scope, risk level, and a concrete first implementation slice.
- Raw private conversation text is excluded unless the user explicitly requested and it was redacted.

## Resources

- `scripts/mine_agent_sessions.py`: local Codex/Claude aggregate miner.
- `references/pattern-manifest.json`: lightweight Agent Patterns index metadata.
