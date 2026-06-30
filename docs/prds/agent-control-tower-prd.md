# PRD: Agent Control Tower

日期：2026-06-29  
状态：v0.1 产品草案  
产品类型：本地优先 AI agent 运行指挥台

## 1. 产品定位

Agent Control Tower 是面向 AI agent 开发者、coding-agent power user 和小团队的本地优先运行指挥台。

它不是新的多 agent 框架，也不替代 Claude Code、Codex、Cursor、Warp、LangGraph、CrewAI 或 n8n。MVP 的核心是把用户已经在本地运行的 agent session、进程、日志、工作区、git 状态、命令、工具调用和风险事件收拢到一个可观察、可恢复、可审计的控制台。

一句话定位：

> Local-first control tower for people running too many coding agents.

## 2. 背景与机会

2026 年 agent 使用者的问题正在从“agent 能不能跑”变成“agent 是否可控、可审计、可恢复”。个人和小团队经常同时运行多个 Claude/Codex/Cursor/Warp/脚本型 agent，但真实状态分散在终端、JSONL、SQLite、浏览器标签、git diff 和临时日志里。

现有 agent observability 工具多面向线上 LLM app trace；现有 workflow/orchestration 工具又偏向开发框架或自动化平台。Agent Control Tower 切入中间层：不要求用户替换 agent，只读取和关联本地运行证据，先让用户看清楚“谁在做什么、在哪里做、改了什么、是否验证、是否危险”。

## 3. 真实需求证据

证据强度：**High for local multi-agent visibility; Medium for paid control-plane product**  
完整来源映射见 [market-demand-evidence.md](./market-demand-evidence.md)。

公开需求信号：

- Hacker News 用户明确描述同时运行 3-6 个 CLI agents，吞吐高但管理困难，现有工具不理解 worktrees 或工作流。  
  Source: https://news.ycombinator.com/item?id=47268777
- HN 上已有 FleetCode、ChatML、Agentastic、wt 等围绕 parallel coding agents、git worktrees、桌面 UI 的 Show HN/项目讨论，说明已有用户自建工具解决同类问题。  
  Sources: https://news.ycombinator.com/item?id=45518861, https://news.ycombinator.com/item?id=47303711, https://news.ycombinator.com/item?id=46765489, https://news.ycombinator.com/item?id=46501758
- Reddit 上 Claude Code 用户反复讨论 parallel agents、worktrees、port conflicts、same repo collisions。  
  Sources: https://www.reddit.com/r/ClaudeAI/comments/1qzduim/stop_running_multiple_claude_code_agents_in_the/, https://www.reddit.com/r/ClaudeAI/comments/1t9tolw/running_two_claude_code_agents_on_the_same_repo/, https://www.reddit.com/r/ClaudeAI/comments/1swlxqb/running_parallel_claude_code_agents_on_the_same/
- 官方生态也在支持 parallel/subagent workflows，例如 Codex subagents 和 Codex cloud background/parallel tasks。  
  Sources: https://developers.openai.com/codex/concepts/subagents, https://developers.openai.com/codex/cloud

PRD 调整结论：

- MVP 不能先做抽象 orchestration framework；应先做本地 agent 状态、worktree、cwd、port、diff、验证证据的运行真相层。
- 需求关键词从 “orchestration” 收敛为 “visibility, isolation, collision prevention, evidence, resume”。
- 付费假设仍需验证：用户可能愿意用开源工具解决 visibility，但小团队和 high-volume power users 可能愿为审计/冲突/验证付费。

## 4. 目标用户

### 核心用户

- **AI coding power user**：同时使用 Claude Code、Codex、Cursor、Warp、Aider、Gemini CLI、本地脚本。
- **AI agent 开发者**：开发 MCP、agent workflow、CLI、browser automation，需要观察和复盘运行过程。
- **小型 AI-native 团队**：2-10 人，依赖 agent 做开发、研究、QA、文档和运营。
- **技术负责人 / reviewer**：需要判断 agent 是否真的完成、是否跑测试、是否越界改文件。

### 非核心用户

- 只使用聊天机器人、没有本地 agent 工作流的普通用户。
- 已经有完整企业级 agent fleet 平台的大型平台团队。
- 只需要抽象 DAG 编排、不关心本地文件和运行证据的自动化用户。

## 5. 核心痛点

- 多个 agent 同时运行，用户不知道哪个在哪个 repo、哪个 branch、哪个 cwd。
- agent session 记录分散，失败后很难定位第一处错误。
- agent 声称完成，但没有明确测试、构建、运行时验证证据。
- 多个 agent 修改同一文件，容易互相覆盖或制造隐形冲突。
- agent 在错误 repo、错误 branch、错误工作区继续执行。
- 危险操作缺少统一提示：删除文件、force push、生产配置、secret、auth/payment 代码。
- 成功 workflow 无法沉淀，失败 session 无法快速复盘。

## 6. 产品目标

### MVP 目标

- 统一展示本地 agent session、运行状态、cwd、repo、branch、文件改动、命令和工具调用。
- 让用户在 30 秒内回答：哪个 agent 在跑、改了什么、是否失败、是否验证过。
- 自动标记 blocked、failed、needs review、unverified done、risk event。
- 提供 session summary、debug bundle、handoff/export。
- 对高风险行为提供本地可解释提示和审计记录。

### 长期目标

- 成为个人和小团队的本地 agent control plane。
- 从只读观察扩展到安全控制：pause、kill、handoff、approval、action cap、spend cap。
- 将成功 session 抽取为可复用 workflow/template。

## 7. 非目标

MVP 不做：

- 不自研完整 agent runtime。
- 不做复杂 BPMN/画布式 orchestration。
- 不默认自动调度多个 agent。
- 不替代 LangGraph、CrewAI、n8n、Temporal。
- 不默认上传本地代码、日志、prompt、secret。
- 不承诺自动修复所有失败。
- 不做企业 SSO、SCIM、复杂 RBAC。

## 8. MVP 范围

### 必须包含

1. 本地 session 发现与解析：Claude/Codex/通用 JSONL/terminal transcript。
2. Dashboard：running、blocked、failed、needs review、done、risk event。
3. Session Detail：目标、cwd、repo、branch、timeline、tool calls、commands、files changed、verification。
4. Workspace View：按 repo 聚合 active sessions、dirty files、branch、冲突风险。
5. Timeline：跨 session 展示用户输入、agent 输出、命令、工具调用、文件变更。
6. Evidence Panel：明确区分 agent claim、实际命令、测试结果、文件状态。
7. Safety Events：dangerous command、secret、sensitive file、cross-repo write、multi-agent conflict。
8. Local index：SQLite，默认只存本地。
9. Export：session summary、debug bundle、PR/issue handoff markdown。

### 暂不包含

- 跨机器同步。
- 团队实时协作。
- 自动创建/merge PR。
- 全自动多 agent 编排。
- 任意远程代码执行托管。

## 9. 核心用户故事

1. 作为同时运行多个 agent 的用户，我要看到所有 active sessions、cwd、repo、branch 和当前状态。
2. 作为开发者，我要打开失败 session，直接看到失败命令、错误摘要、最近文件改动和下一步建议。
3. 作为 reviewer，我要知道 agent 是否真的跑过测试，测试何时运行、退出码是什么。
4. 作为 power user，我要知道哪个 agent 修改了某个文件，避免互相覆盖。
5. 作为安全敏感用户，我要在 agent 修改 `.env`、auth、billing、CI、AGENTS.md 时看到明确风险提示。
6. 作为团队负责人，我要导出一个 session 复盘给 teammate 或下一轮 agent 接手。

## 10. 信息架构

- **Overview**：全局运行态、风险、待处理。
- **Sessions**：所有 agent session 列表和筛选。
- **Workspaces**：按 repo/cwd 聚合的工作区状态。
- **Timeline**：跨 session 事件流。
- **Changes**：文件改动、diff、冲突、未提交变更。
- **Safety**：危险事件、secret 扫描、权限、审计。
- **Templates**：从历史 session 抽取的任务模板。
- **Settings**：数据源、解析器、隐私、安全规则、集成。

## 11. 关键功能

### 10.1 Session Parser

将不同来源标准化为统一事件：

- `user_message`
- `agent_message`
- `tool_call`
- `command`
- `file_change`
- `test_result`
- `error`
- `state_change`

解析失败必须保留 raw reference 和 error，不静默吞掉。

### 10.2 Live Monitor

- 监听本地日志目录、workspace git 状态、活跃进程。
- 识别 cwd、repo、branch、dirty files、session source。
- 标记长时间无输出、重复失败、无验证完成声明。

### 10.3 Workspace Guard

- 检测 agent 是否跨 repo 修改。
- 检测多个 sessions 是否修改同一文件。
- 检测高风险文件：`.env`、密钥文件、AGENTS.md、CI、auth/payment/permission 代码。
- 检测危险命令：`rm -rf`、force push、credential dump、生产 DB 操作、curl pipe shell。

### 10.4 Evidence Panel

- 展示完成声明对应证据。
- 展示测试命令、退出码、运行时间和关键输出。
- 标记 `verified`、`unverified`、`failed`、`not run`。
- 明确区分 agent 叙述和本地事实。

### 10.5 Session Summary

自动生成四种导出：

- PR/issue summary。
- debug bundle。
- next-agent handoff。
- workflow/template candidate。

## 12. 数据模型草案

```text
Workspace
- id
- root_path
- repo_url
- current_branch
- dirty_state
- last_seen_at

AgentSession
- id
- agent_type: claude | codex | cursor | shell | browser | custom
- title
- objective
- workspace_id
- cwd
- branch
- status: running | blocked | failed | needs_review | done | ignored
- started_at
- ended_at
- source_path
- parser_version

SessionEvent
- id
- session_id
- event_type
- timestamp
- actor: user | agent | tool | system
- summary
- raw_ref
- severity

CommandRun
- id
- session_id
- command
- cwd
- exit_code
- duration_ms
- stdout_ref
- stderr_ref
- risk_level

FileChange
- id
- session_id
- workspace_id
- file_path
- change_type: create | modify | delete | rename
- diff_ref
- ownership_status
- risk_level

Verification
- id
- session_id
- command_run_id
- verification_type: build | test | lint | runtime_check | manual
- status
- evidence_summary

SafetyEvent
- id
- session_id
- workspace_id
- rule_id
- severity
- subject_type: command | file | secret | permission | repo
- subject_ref
- status: open | acknowledged | resolved | false_positive
```

## 13. 隐私、安全与审计

- 默认 local-first，不上传代码、prompt、日志和命令输出。
- 原始日志优先引用，不强制复制。
- 敏感字段默认 hash/redact。
- 用户可配置监控目录白名单和忽略目录。
- Safety event 必须可解释，不能只显示“风险”。
- 导出前执行本地 secret scan。
- 高风险操作 MVP 只提示和审计，不默认强制拦截。

## 14. 技术集成边界

### MVP 输入

- Claude Code 本地 session/log。
- Codex 本地 session/log。
- 通用 JSONL/Markdown transcript。
- Shell command history 或 wrapper log。
- Git status/diff/log。

### 可选增强

- `actower run <command>` CLI wrapper。
- MCP server：agent 可主动写入 session metadata。
- VS Code/Cursor extension：只展示 workspace 状态。
- Git hook/preflight hook：默认关闭。

## 15. 成功指标

### 激活指标

- 首次启动后 10 分钟内成功展示历史 session。
- 用户连接至少 2 类数据源。
- 用户打开至少 1 个 failed session detail。
- 用户完成第一次 summary/export。

### 价值指标

- 失败定位时间下降。
- 未验证完成声明被发现次数。
- 高风险文件改动被提示次数。
- 多 agent 文件冲突被发现次数。
- session summary 被复用为 handoff/template 次数。

### 商业指标

- Free 到 Pro 转化率。
- Pro 用户每周活跃 session 数。
- Team workspace 数。
- 导出/审计/模板功能使用率。

## 16. 商业化

- **Free**：单用户、本地、基础 dashboard、session detail、有限历史、基础 safety rules。
- **Pro ($12-20/月)**：无限本地索引、高级搜索、长期归档、debug bundle、模板抽取、多数据源解析器。
- **Team ($20-40/seat/月)**：共享审计摘要、共享模板、统一安全规则、PR/issue handoff、私有同步。
- **Enterprise**：私有部署、SSO、保留策略、自定义解析器、合规审计。

## 17. 竞品与替代方案

- 终端历史 + grep：低成本，但无法结构化跨 agent 证据。
- Claude/Codex 原生日志：只覆盖单工具，缺少 workspace/git/safety 聚合。
- LangSmith/Langfuse/Helicone/Braintrust：偏线上 LLM app observability，不专注本地 agent workspace。
- Temporal/Airflow/Prefect/n8n：偏 workflow orchestration，不是本地 agent 审计台。
- Git UI：能看 diff，但不知道 agent 为什么改、怎么改、是否验证。

差异化：local-first、跨 agent、本地 workspace truth、evidence-first、无需替换现有 agent。

## 18. 风险与缓解

- **日志格式不稳定**：parser 插件化、版本化、保留 raw event。
- **隐私顾虑**：默认本地、可关闭全文索引、redaction、云端 opt-in。
- **scope 变成复杂 orchestration**：MVP 只做观察、审计、恢复、复盘。
- **归因不准**：用 cwd、timestamp、process、source_path、git diff 多信号，低置信度明确标记。
- **安全提示太吵**：规则分级、false positive、只默认提示关键风险。
- **ROI 难证明**：围绕失败定位时间、未验证完成、风险事件、复盘导出建指标。

## 19. 里程碑

- **M0 Discovery (2-3 周)**：收集 Claude/Codex session 样本，定义事件模型，输出 10 个真实 session summary。
- **M1 Local MVP (4-6 周)**：daemon + SQLite、sessions、workspace、file changes、search、safety events、markdown export。
- **M2 Power User Beta (4 周)**：live monitor、timeline、verification panel、conflict detection、template extraction。
- **M3 Pro Release (6-8 周)**：高级搜索、长期归档、debug bundle、CLI wrapper、license。
- **M4 Team Preview (8-12 周)**：共享审计摘要、共享模板、团队规则、PR/issue handoff。

## 20. 开放问题

- MVP 是否允许从 UI pause/kill 本地 agent，还是只读观察？
- 是否提供统一启动入口，还是只做被动发现？
- 默认是否索引完整 stdout/stderr？
- 原始日志是否复制到产品数据目录，还是只保存引用？
- 如何处理多个同名 repo、多个 worktree、symlink cwd？
- Team 版是否必须做云同步才能成立？

## 21. 参考资料

- OpenTelemetry Generative AI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- MLflow Tracing: https://mlflow.org/docs/latest/llms/tracing/index.html
- LangSmith observability: https://docs.smith.langchain.com/observability
- Langfuse tracing: https://langfuse.com/docs/tracing
- Braintrust observability: https://www.braintrust.dev/docs/guides/tracing
- OpenAI Codex docs: https://developers.openai.com/codex/
- Anthropic Claude Code docs: https://docs.anthropic.com/en/docs/claude-code/overview
