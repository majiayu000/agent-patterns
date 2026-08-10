# Mapping These Patterns to Spellbook

These patterns in the `be` workspace are designed to be turned into first-class skills in https://github.com/majiayu000/spellbook.

## 1. skill-lifeguard → Reliable Skill Contract

**Target in spellbook**: New or enhanced meta skill under AI & Agent Workflow, e.g. `skill-lifeguard` or integrated into `skill-audit` + `skill-creator`.

**Key contribution**:
- The 5-element Reliable Skill Contract (Negative Examples, Checkpoints, Done conditions, Replay hooks, Drift signals).
- Use as the required template when running `skill-audit` on agent-related skills.

**Recommended location after export**: `skills/skill-lifeguard/` (or merge key sections into existing `skill-audit` references).

## 2. context-handoff-pack (enhanced) → Context Engineering Guard

**Target in spellbook**: Strengthen `strategic-compact` and `flowguard`, or new lightweight `context-engineering` helper.

**Key additions**:
- Mandatory one-sentence primary objective + <=5 step plan re-statement.
- Context Audit step (garbage / conflict / stale detection).
- Explicit Compaction Policy table.
- External scratchpad / memory blocks recommendation.
- Integration points for calling as a guard from other skills.

**Recommended location**: Merge relevant sections into `strategic-compact/SKILL.md` and `flowguard` references, or keep as enhanced `context-handoff-pack`.

## 3. review-gate → Explicit Landing Gate

**Target in spellbook**: New skill `review-gate` under Delivery / Agent Workflows, or integrated with existing review flows.

**Key features**:
- Collect diff + originating handoff / skill.
- Delegate risk analysis (can call patterns similar to `pr-review-risk-plan`).
- Produce human-readable Review Pack.
- Hard human gate before commit / push / PR / apply.
- Records approval back into handoff.

**Recommended location**: `skills/review-gate/`

Complements `flowguard` (final checkpoint) and `skill-lifeguard` (the skill that produced the diff must survive this gate).

## How to Port

1. Copy the `SKILL.md` content (adapt frontmatter `description` for spellbook trigger style).
2. Create `references/` for any extra templates/checklists.
3. Add `scripts/` only if deterministic helpers are needed (e.g. diff collection wrapper).
4. Update spellbook's `Skill Quality Playbook` and `Operating Contract` to reference the new contracts (especially the 5 elements and review gate).
5. Add to the "Agent workflows" bundle in README.

These three directly address the top X-reported pains:
- Skills cat-and-mouse (skill-lifeguard)
- Context rot / drift (enhanced context-handoff-pack + objective re-verify)
- Unvetted agent changes landing (review-gate)

Run the local pattern validator after porting:
python3 scripts/validate_skills.py --check
python3 scripts/audit_skill_quality.py <new-skill>
