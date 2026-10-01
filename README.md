# Agent Patterns Skill Pack

Reusable workflow skills for Codex and Claude Code, covering PR review, CI
diagnosis, context handoff, session-history mining, and human review gates.
Use them to carry evidence, scope, failure handling, and verification through
repeatable coding-agent work.

Each skill keeps its workflow in `SKILL.md`, with bundled scripts and references
where needed. This repository is a skill pack; it does not run an agent service.

## Quick start

```sh
git clone https://github.com/majiayu000/agent-patterns.git
cd agent-patterns
python3 skills/agent-patterns/scripts/pattern_tool.py list
python3 skills/agent-patterns/scripts/pattern_tool.py search "pr review"
```

Read the selected skill's `SKILL.md` before using it. To install a skill, copy
its whole folder into your host's configured skill directory, preserving its
`scripts/` and `references/` resources. Invoke it through that host's skill
interface; the listing helper itself does not execute the workflow.

Start with [PR review](skills/pr-review-risk-plan/SKILL.md),
[CI failure diagnosis](skills/ci-failure-diagnosis/SKILL.md), or
[context handoff](skills/context-handoff-pack/SKILL.md).
See the [meta skill](skills/agent-patterns/SKILL.md) for the pattern contract and
[Spellbook mapping](docs/spellbook-mapping.md) for porting notes.

## Choose a skill for the problem

| Your task | Start with | Bring this evidence |
| --- | --- | --- |
| Review a PR before changing or merging it | [PR Review Risk Plan](skills/pr-review-risk-plan/SKILL.md) | PR URL or local diff, base/head, intended behavior, and relevant checks |
| Explain a red CI run before proposing a fix | [CI Failure Diagnosis](skills/ci-failure-diagnosis/SKILL.md) | Run URL, failing job/command, exact commit, and available logs |
| Resume after compaction or hand work to another agent | [Context Handoff Pack](skills/context-handoff-pack/SKILL.md) | Repo path, current goal, changed files, decisions, verification, and one next action |
| Require a human decision before changes land | [Review Gate](skills/review-gate/SKILL.md) | Proposed diff, risks, verification, and the exact action requiring approval |

After installing the whole skill folder, select it through your host's skill
interface and give it a concrete request, for example:

> Use CI Failure Diagnosis for this run: `<run URL>`. The repository is
> `<repo path>` and the failing head is `<commit SHA>`. Read the failing job
> evidence, identify the smallest defensible cause, and report which checks you
> completed before proposing a fix.

For a handoff, use Context Handoff Pack with the exact repository path and goal.
Its local-history probe can help find session evidence; historical logs remain
hints until current Git, runtime, and test state are verified. You can use it
with live workspace evidence when local history is unavailable.

`pattern_tool.py search` finds manifest metadata. It does not invoke an agent,
execute the selected workflow, grant approval, or prove a fix works. This is
**majiayu000/agent-patterns**, a workflow skill pack; each linked `SKILL.md`
defines its own evidence and failure contract.

For a reproducible script or packaging problem, open a
[repository issue](https://github.com/majiayu000/agent-patterns/issues) with the
skill, command, version or commit, and redacted error. See [LICENSE](LICENSE)
for reuse terms.

## Skills

- `skills/agent-patterns`: meta skill for creating, auditing, validating, and packaging executable workflow patterns.
- `skills/pr-review-risk-plan`: concrete PR review workflow skill.
- `skills/ci-failure-diagnosis`: concrete CI root-cause workflow skill.
- `skills/context-handoff-pack`: concrete long-session handoff workflow skill with a Codex local-history probe.
- `skills/agent-session-pattern-miner`: concrete workflow-mining skill that turns local Codex/Claude session history into new-skill and enhancement candidates.
- `skills/review-gate`: explicit human approval gate before agent-generated changes land.
- `skills/skill-lifeguard`: reliability contract for evolving skills from observed failures.

The scripts under `skills/agent-patterns/scripts/` are bundled skill resources. `pattern_tool.py` validates and searches lightweight manifests in each concrete skill's `references/pattern-manifest.json`. Each runnable session-history skill vendors its small utility module inside its own skill folder so copying the folder remains standalone. Scripts are not the main product surface.

`SKILL.md` is the source of truth for workflow behavior. Manifests are search/index metadata only.

## Checks

```sh
QUICK_VALIDATE="${SKILL_CREATOR_QUICK_VALIDATE:-${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py}"
python3 "$QUICK_VALIDATE" skills/agent-patterns
python3 "$QUICK_VALIDATE" skills/pr-review-risk-plan
python3 "$QUICK_VALIDATE" skills/ci-failure-diagnosis
python3 "$QUICK_VALIDATE" skills/context-handoff-pack
python3 "$QUICK_VALIDATE" skills/agent-session-pattern-miner
python3 "$QUICK_VALIDATE" skills/review-gate
python3 "$QUICK_VALIDATE" skills/skill-lifeguard
python3 skills/agent-patterns/scripts/pattern_tool.py validate
SKILL_CREATOR_QUICK_VALIDATE="$QUICK_VALIDATE" python3 -m unittest discover -s tests -v
```
