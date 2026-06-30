# Agent Patterns Skill Pack Technical Spec

日期：2026-06-29

## 1. 范围

先实现 skill-first 开源核心，不实现 marketplace、账号、远程执行或团队权限。

MVP 包含：

- `skills/agent-patterns` 元 skill。
- 3 个具体 workflow skills：`pr-review-risk-plan`、`ci-failure-diagnosis`、`context-handoff-pack`。
- 轻量 pattern manifest schema，作为元 skill reference。
- 每个具体 skill 自己持有 `references/pattern-manifest.json`。
- 元 skill helper：`list`、`search`、`validate`、`show`。
- deterministic verification：compile、unit tests、pattern validation。

## 2. 关键决策

- 产品表面是 `SKILL.md`，不是脚本。
- `SKILL.md` 是 workflow 主源；manifest 只是索引，不能重复 workflow/failure/input/output/gate 内容。
- manifest 源格式先用 JSON，不引入 YAML 依赖；后续可以加 YAML adapter。
- Python helper 只用标准库，避免空仓库阶段引入包管理复杂度。
- Validator fail closed：缺字段、未声明工具、高风险权限缺 human gate 都报错。
- Helper 不自动写入用户 repo；只做校验、检索和预览渲染。

## 3. 非目标

- 不做 hosted semantic search。
- 不做 GitHub login。
- 不托管任意代码执行。
- 不自动提交 PR 或发布外部评论。
- 不声称 community pattern verified。

## 4. Done When

- 4 个 skill folder 通过 `quick_validate.py`。
- `python3 skills/agent-patterns/scripts/pattern_tool.py validate` 对全部 skill manifests 返回 valid。
- `python3 -m unittest discover -s tests` 通过。
- `show` 至少能对一个 manifest 返回索引信息和 source skill path。
