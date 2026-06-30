# AI Agent Product PRD Pack

日期：2026-06-29

本目录包含 4 个可独立立项的 AI Agent 产品 PRD。它们可以借鉴 Stash 已有的 local-first、session parser、Claude/Codex 运行记录、evidence、workflow 经验，但默认不是 Stash 的功能模块。

这些 PRD 已补充真实网络需求证据，证据来源包括 Reddit、Hacker News、官方文档和行业治理资料。完整证据映射见 [market-demand-evidence.md](./market-demand-evidence.md)。

## 产品清单

| 文件 | 产品名 | 一句话定位 | 首选 MVP |
| --- | --- | --- | --- |
| [agent-control-tower-prd.md](./agent-control-tower-prd.md) | Agent Control Tower | 本地优先的多 agent 运行指挥台 | 发现本地 agent session，展示运行状态、cwd、文件改动、命令、风险和验证证据 |
| [agent-patterns-prd.md](./agent-patterns-prd.md) | Agent Patterns | 可搜索、可 fork、可导出的 executable agent workflow library | 30-50 个 curated patterns，支持导出 Claude/Codex/AGENTS.md/LangGraph/OpenAI Agents SDK |
| [contextops-prd.md](./contextops-prd.md) | ContextOps | 面向长期 agent 工作的上下文记忆与交接优化器 | 生成 Context Pack，检测 drift、loop、missing evidence |
| [agent-ledger-prd.md](./agent-ledger-prd.md) | Agent Ledger | 个人/小团队 agent 治理、审计、风险报告工具 | 自动发现 agent/automation/API key/OAuth 风险，生成 Agent Governance Report |
| [market-demand-evidence.md](./market-demand-evidence.md) | Evidence Map | 真实需求证据索引 | 将 Reddit/HN/官方资料映射到四个产品假设 |

## 产品边界

这四个方向应先作为独立产品验证，不建议一开始合并成一个大而全平台。

- Agent Control Tower 解决“我开的 agent 现在到底在干什么”。
- Agent Patterns 解决“我该用什么可复用 workflow 让 agent 做这件事”。
- ContextOps 解决“agent 如何不失忆、不漂移、不断上下文”。
- Agent Ledger 解决“这些 agent 是否有 owner、权限、预算、审计和报告”。

## 推荐验证顺序

1. **ContextOps**：Reddit/HN 上 context loss、context rot、compaction、persistent memory、handoff 的公开痛点最密集，MVP 也最小。
2. **Agent Patterns**：skills、AGENTS.md、CLAUDE.md、slash commands、workflow packs 的公开分享和标准化摩擦明显，适合开源传播。
3. **Agent Control Tower**：parallel agents、worktrees、terminal/tab sprawl 有真实需求，但需先做本地 visibility，不要过早做通用 orchestration。
4. **Agent Ledger**：shadow AI、budget runaway、敏感操作审计有强风险信号，但个人/小团队付费意愿需要重点验证。

## 共同原则

- local-first by default：默认不上传代码、日志、prompt、secret。
- evidence-first：完成声明、风险判断、上下文结论都要能追溯证据。
- no silent degradation：解析失败、权限不足、证据缺失必须显式展示。
- observe before control：先观察和报告，再做拦截、审批、自动调度。
- executable over static：不是静态 cheatsheet、prompt 库或治理文档，而是可执行、可验证、可导出的产品资产。
