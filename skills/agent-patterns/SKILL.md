---
name: agent-patterns
description: Create, convert, audit, and package executable AI agent workflow patterns as Codex/Claude-style skills. Use when the user wants an agent workflow library, reusable workflow schema, pattern-to-skill conversion, skill pack design, exporter/validator behavior, curated coding-agent patterns, or wants to avoid prompt-library or hardcoded-script designs.
---

# Agent Patterns

Use this skill to turn repeatable agent workflows into first-class skills. A pattern is not a prompt: it must have a trigger, scope, workflow, inputs, outputs, tool permissions, human gates, failure modes, and verification.

`SKILL.md` is the workflow source of truth. A `pattern-manifest.json` is only a lightweight index for search, validation, and registry views; it must not duplicate workflow steps, failure modes, inputs, outputs, or gates.

## Route

1. Search first for existing skills, pattern manifests, and similar workflows before creating a new one.
2. Choose the smallest useful shape:
   - One skill when the workflow has a single clear trigger and procedure.
   - Multiple skills when patterns have different triggers, risk profiles, or verification loops.
   - A meta skill plus concrete skills when building a reusable pattern pack.
3. Write `SKILL.md` as the product surface. Put deterministic helpers under `scripts/`; put only lightweight manifests or schemas under `references/`.
4. Keep scripts generic. They may validate, list, search, or show manifests, but they must not be the only usable interface.
5. Validate each skill folder with the skill creator `quick_validate.py` script.

## Pattern Contract

Every concrete pattern skill should define in `SKILL.md`:

- Trigger and non-trigger in the frontmatter description.
- Required inputs and available evidence.
- Ordered workflow steps.
- Tool permissions and human gates.
- Failure modes with explicit stop/report behavior.
- Done-when and verification commands.

When the workflow uses high-risk operations such as shell, network, secrets, external comments, writes, payments, or destructive actions, require a human gate before that step.

Each concrete pattern skill may include `references/pattern-manifest.json` with only these index-level facts: id, skill, title, summary, category, tags, maturity, risk level, capabilities, whether a human gate is required, source, and maintenance mode.

## Resources

- `references/pattern-manifest.schema.json`: schema for lightweight pattern manifests.
- `../*/references/pattern-manifest.json`: per-skill manifests, each pointing back to its owning `SKILL.md`.
- `scripts/pattern_tool.py`: helper for listing, searching, validating, and showing pattern manifests.

Use the helper from the skill directory root:

```sh
python3 skills/agent-patterns/scripts/pattern_tool.py list
python3 skills/agent-patterns/scripts/pattern_tool.py search "pr review"
python3 skills/agent-patterns/scripts/pattern_tool.py validate
python3 skills/agent-patterns/scripts/pattern_tool.py show pr-review-risk-plan.v1
python3 skills/agent-patterns/scripts/pattern_tool.py show skill-lifeguard.v1
python3 skills/agent-patterns/scripts/pattern_tool.py show review-gate.v1
```

## Output Rules

- Prefer a skill folder over a standalone script.
- Do not create README, quick reference, changelog, or installation docs inside a skill folder.
- Do not put full workflow JSON in the meta skill. Keep workflows in concrete `SKILL.md` files.
- Do not mark a community or untested pattern as verified.
- Do not hide unsupported exporter behavior; report missing target support explicitly.
- Keep machine-facing IDs in English and stable across exports.
