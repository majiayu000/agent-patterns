# Agent Patterns Skill Pack

This workspace now models Agent Patterns as skills, not as a standalone hardcoded product script.

## Skills

- `skills/agent-patterns`: meta skill for creating, auditing, validating, and packaging executable workflow patterns.
- `skills/pr-review-risk-plan`: concrete PR review workflow skill.
- `skills/ci-failure-diagnosis`: concrete CI root-cause workflow skill.
- `skills/context-handoff-pack`: concrete long-session handoff workflow skill with a Codex local-history probe.
- `skills/agent-session-pattern-miner`: concrete workflow-mining skill that turns local Codex/Claude session history into new-skill and enhancement candidates.

The scripts under `skills/agent-patterns/scripts/` are bundled skill resources. `pattern_tool.py` validates and searches lightweight manifests in each concrete skill's `references/pattern-manifest.json`; shared utilities support local session-history helpers. Scripts are not the main product surface.

`SKILL.md` is the source of truth for workflow behavior. Manifests are search/index metadata only.

## Checks

```sh
QUICK_VALIDATE="${SKILL_CREATOR_QUICK_VALIDATE:-${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py}"
python3 "$QUICK_VALIDATE" skills/agent-patterns
python3 "$QUICK_VALIDATE" skills/pr-review-risk-plan
python3 "$QUICK_VALIDATE" skills/ci-failure-diagnosis
python3 "$QUICK_VALIDATE" skills/context-handoff-pack
python3 "$QUICK_VALIDATE" skills/agent-session-pattern-miner
python3 skills/agent-patterns/scripts/pattern_tool.py validate
python3 -m unittest discover -s tests
```
