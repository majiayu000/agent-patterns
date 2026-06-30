# PRD: ContextOps

日期：2026-06-29  
状态：v0.1 产品草案  
产品类型：Agent Memory & Context Optimizer

## 1. 产品定位

ContextOps 是面向重度 AI agent 用户、长期软件项目和 AI-native 工程团队的本地优先上下文运营工具。

它不是普通 summarizer。它把 agent 工作中的事实、决策、证据、任务状态、失败循环、上下文漂移和交接信息结构化沉淀，并在下一次 session、下一个 agent、下一位团队成员接手时，生成可信、可追溯、不过载的 Context Pack。

一句话定位：

> Turn messy agent transcripts into verified, portable, minimal context packs.

## 2. 背景与机会

AI agent 在短任务里越来越强，但长任务、跨 session、跨 repo、跨成员协作时仍然容易失忆、漂移、重复探索和错误交接。用户通常通过复制聊天记录、手写总结、临时 Markdown 或手动维护 memory 来解决，但这些方法缺少证据、失效条件和质量控制。

ContextOps 的机会是成为 agent 工作的“上下文层”：不替代 agent 执行，而是管理 agent 可依赖的当前事实、历史决策、失败路径、验证证据和下一步 handoff。

## 3. 真实需求证据

证据强度：**High**  
完整来源映射见 [market-demand-evidence.md](./market-demand-evidence.md)。

公开需求信号：

- Reddit 反复出现 Claude/Codex/LLM context compaction、context loss、context rot、persistent memory、long-session drift 的讨论。  
  Sources: https://www.reddit.com/r/ClaudeAI/comments/1lw56i2/context_loss_on_claude_code_after_context/, https://www.reddit.com/r/LocalLLaMA/comments/1u6356v/do_long_agent_sessions_get_context_rot_for_you_too/, https://www.reddit.com/r/ClaudeAI/comments/1q1c063/got_tired_of_claude_code_forgetting_everything/, https://www.reddit.com/r/ClaudeAI/comments/1r06z4r/i_built_a_claudemd_that_solves_the/
- Reddit 用户讨论使用 session-summary、CLAUDE.md template、external memory、structured state 来避免 compaction 后丢失上下文。  
  Sources: https://www.reddit.com/r/ClaudeAI/comments/1plgyff/how_to_prevent_claude_code_from_losing_its_focus/, https://www.reddit.com/r/ClaudeAI/comments/1r43dzl/new_claudemd_that_solves_the_compactioncontext/
- HN 上多次出现 persistent memory、external context layer、memory for Claude Code、context compression、tool output bloat 等项目和讨论。  
  Sources: https://news.ycombinator.com/item?id=46426624, https://news.ycombinator.com/item?id=45516584, https://news.ycombinator.com/item?id=48622590, https://news.ycombinator.com/item?id=47193064, https://news.ycombinator.com/item?id=45418251
- 官方/行业资料也在强调 context engineering、traces、tool calls、reusable context。  
  Sources: https://developers.openai.com/codex/learn/best-practices, https://sourcegraph.com/blog/context-engineering, https://opentelemetry.io/docs/specs/semconv/gen-ai/

PRD 调整结论：

- 这是四个方向里公开需求证据最强的一条。
- MVP 应聚焦 Context Pack、evidence coverage、drift/loop detection、handoff，而不是泛化成知识库或 summarizer。
- 最小验证路径应是 CLI：导入 session -> 生成 handoff pack -> 下一轮 agent 是否减少重复解释和重复探索。

## 4. 目标用户

- **重度 AI agent 个人用户**：每天使用 Codex、Claude Code、Cursor、Warp、Aider、Devin 等工具。
- **长期项目维护者**：项目周期超过数月，存在历史决策、遗留问题、PR/issue 背景、部署差异。
- **AI-native 工程团队**：多人协作使用 agent，需要统一当前事实源和交接格式。
- **Agent workflow / 平台团队**：需要 memory governance、context policy、evidence tracking、loop detection。

## 5. 核心痛点

### 4.1 上下文爆炸

- 项目积累大量 chat、terminal log、PR、issue、design doc、test output。
- 直接喂模型会超上下文窗口。
- 粗暴总结会丢掉路径、命令、失败原因和证据。

### 4.2 Context Drift

- agent 长任务中逐渐偏离原目标。
- 把旧 session 结论当成当前事实。
- 混淆 repo、branch、runtime、端口、PR 状态。
- 从“修 bug”漂移成大规模重构。

### 4.3 重复劳动

- 每个新 session 都重新搜索文件、重新理解架构、重新定位 bug。
- 已证伪路径、失败命令、根因假设没有沉淀。
- 团队成员反复问同样问题。

### 4.4 Handoff 失败

接手者缺少：

- 当前目标。
- 修改文件。
- 约束条件。
- 验证命令。
- 已证伪假设。
- 下一步和 blocker。

### 4.5 记忆断裂

- chat history、terminal logs、git diff、PR comments、local notes 分散。
- AI 工具自带 memory 更偏通用偏好，不适合项目级事实管理。
- 缺少 durable decisions 和失效条件。

## 6. 产品目标

### MVP 目标

- 生成高质量 Context Pack，包含事实、目标、状态、证据、约束、风险和下一步。
- 检测 context drift、agent loop、missing evidence、stale memory。
- 自动抽取 durable decisions、pitfalls、verified commands、failed attempts。
- 降低下一轮 agent 重新探索成本。
- 支持 local-first，默认不上传代码和原始日志。

### 长期目标

- 成为团队的 agent context memory layer。
- 支持跨工具、跨 session、跨 repo 的可信上下文。
- 与 Agent Control Tower、Agent Patterns、Agent Ledger 形成互补，但独立可用。

## 7. 非目标

- 不做通用笔记软件。
- 不做普通聊天总结器。
- MVP 不做完整 agent IDE。
- MVP 不做云端全量代码索引。
- 不自动执行危险操作，不自动 merge/push/deploy。
- 不把无证据结论伪装成事实。

## 8. MVP 范围

### 必须包含

1. 本地 workspace 注册。
2. Session log 导入与解析。
3. Git/file/terminal evidence 关联。
4. Durable decisions 管理。
5. Context Pack 生成。
6. Drift 检测。
7. Loop 检测。
8. Evidence coverage 检测。
9. Handoff 模板。
10. CLI + 本地 Web UI。
11. 隐私和敏感信息过滤。

### 暂不包含

- 多租户 SaaS 云协作。
- 自动代码修改。
- 深度 IDE 插件生态。
- 全自动长期任务调度。
- 复杂权限审批流。

## 9. 核心用户故事

1. 作为重度 agent 用户，我要生成昨天任务的 handoff pack，包含目标、已完成内容、失败路径、修改文件和下一步。
2. 作为工程师，我要检查当前 cwd、branch、HEAD、dirty diff 是否和历史 context 一致。
3. 作为维护者，我要把长期有效的架构决策保存为 durable decision，并带证据和失效条件。
4. 作为团队负责人，我要识别 agent 是否重复尝试同一失败方案。
5. 作为 teammate，我要把一个 agent session 转成 Markdown/JSON 交接包。
6. 作为 reviewer，我要看到 pack 中每个关键声明是 verified、memory-derived、inferred 还是 unverified。

## 10. 信息架构

顶层对象：

- **Workspace**：本地项目或 monorepo。
- **Session**：一次 agent 对话、terminal 执行或任务过程。
- **Task**：一组 session 对应的工作目标，可关联 issue/PR/spec/branch。
- **Memory Item**：decision、constraint、pitfall、command、environment、architecture、handoff。
- **Evidence**：文件路径、行号、命令输出、git commit、PR comment、issue、日志片段。
- **Context Pack**：面向下一次 agent 或人类交接的上下文包。
- **Signal**：drift、loop、missing evidence、stale fact、scope mismatch。

主导航：

- Workspaces。
- Sessions。
- Memory。
- Context Packs。
- Signals。
- Evidence。
- Settings。

## 11. 关键功能

### 10.1 Session Parser

解析来源：

- Codex/Claude/Cursor/Warp/Aider session。
- terminal command history。
- git status/diff/log。
- PR/issue text。
- test output。
- local Markdown notes。

抽取目标：

- 目标。
- 约束。
- 修改文件。
- 命令。
- 失败。
- 根因假设。
- 结论。
- 下一步。
- 证据。

### 10.2 Durable Decisions

每条 durable decision 包含：

- 决策内容。
- 为什么做这个决策。
- 适用范围。
- 证据来源。
- 创建时间。
- 最后验证时间。
- 失效条件。
- 来源 session 或负责人。

```json
{
  "type": "decision",
  "title": "Context Pack default is local-first",
  "decision": "MVP does not upload full source code or raw agent logs.",
  "scope": ["mvp", "privacy", "team-edition"],
  "evidence_refs": ["prd:privacy-requirements", "interview:team-security-01"],
  "created_at": "2026-06-29",
  "invalidates_when": "team explicitly enables private cloud deployment"
}
```

### 10.3 Context Pack Generator

Pack 类型：

- Resume Pack：同一人继续任务。
- Handoff Pack：另一个人或 agent 接手。
- Review Pack：reviewer 快速理解变更。
- Debug Pack：聚焦失败命令、日志、假设和证据。
- Onboarding Pack：新 agent 理解项目约束。

### 10.4 Drift Detector

检测类型：

- 目标漂移：操作不再映射到 task goal/done-when。
- 范围漂移：修改非任务相关文件。
- 事实漂移：使用过期 memory 或旧分支结论。
- 环境漂移：cwd、branch、runtime、port、database 不一致。
- 证据漂移：声称完成但无当前 session 验证。
- 策略漂移：小修 bug 演变成大规模重构。

### 10.5 Loop Detector

检测信号：

- 同一失败命令重复 3 次且错误签名相同。
- 同一文件同一区域反复 patch 但测试仍失败。
- 多次切换方案但错误未变化。
- 反复读取同一批文件却没有新结论。
- 反复声称“应该好了”但没有通过验证。

### 10.6 Evidence Coverage

关键声明标签：

- `verified`：有当前 session 命令、文件、git 或日志证据。
- `memory_derived`：来自历史记忆，可能过期。
- `inferred`：系统推断。
- `user_provided`：用户口头提供。
- `unverified`：没有证据支撑。

原则：没有证据的结论可以存在，但必须显式标注。

## 12. Context Pack Schema v1

```json
{
  "context_pack_version": "1.0",
  "pack_type": "resume | handoff | review | debug | onboarding",
  "generated_at": "ISO-8601",
  "workspace": {
    "name": "string",
    "repo_root": "string",
    "current_branch": "string",
    "head_sha": "string",
    "dirty_files": ["string"],
    "runtime_state": {
      "servers": ["string"],
      "ports": ["number"],
      "env_notes": ["string"]
    }
  },
  "task": {
    "title": "string",
    "goal": "string",
    "current_priority": "string",
    "linked_issue": "string|null",
    "linked_pr": "string|null",
    "status": "not_started | in_progress | blocked | ready_for_review | done",
    "done_when": ["string"]
  },
  "constraints": [
    {
      "text": "string",
      "source": "user | repo | memory | policy",
      "evidence_refs": ["string"],
      "staleness": "fresh | possibly_stale | stale"
    }
  ],
  "modified_files": [
    {
      "path": "string",
      "change_summary": "string",
      "ownership": "agent | user | unknown",
      "risk": "low | medium | high"
    }
  ],
  "durable_decisions": [
    {
      "id": "string",
      "title": "string",
      "decision": "string",
      "scope": ["string"],
      "evidence_refs": ["string"],
      "invalidates_when": "string"
    }
  ],
  "evidence": [
    {
      "id": "string",
      "type": "file | command | git | issue | pr | log | screenshot | user_message",
      "locator": "string",
      "captured_at": "ISO-8601",
      "summary": "string"
    }
  ],
  "verification": {
    "commands_run": [
      {
        "command": "string",
        "result": "passed | failed | skipped",
        "evidence_ref": "string",
        "timestamp": "ISO-8601"
      }
    ],
    "required_before_done": ["string"]
  },
  "drift_signals": [
    {
      "type": "goal | scope | stale_fact | environment | evidence",
      "severity": "low | medium | high",
      "description": "string",
      "evidence_refs": ["string"]
    }
  ],
  "loop_signals": [
    {
      "type": "repeated_command | repeated_failure | repeated_patch | no_new_hypothesis",
      "count": "number",
      "description": "string",
      "evidence_refs": ["string"]
    }
  ],
  "next_actions": [
    {
      "action": "string",
      "owner": "human | agent | either",
      "priority": "p0 | p1 | p2",
      "requires_confirmation": "boolean"
    }
  ],
  "summary_for_human": "string",
  "prompt_for_next_agent": "string"
}
```

## 13. 检测逻辑

### Drift Detection

输入：原始目标、当前任务状态、最近 agent 动作、git diff、cwd、branch、HEAD、历史 packs、durable decisions。

规则：

- 最近操作无法映射到 `task.goal` 或 `done_when`。
- 修改文件不在预期模块或关联路径内。
- 引用旧 memory，且 repo HEAD 或关键文件已变化。
- 历史 context 指向 repo A，当前 cwd 是 repo B。
- 完成声明没有当前 session 验证命令。

### Loop Detection

输入：command history、test results、error messages、patch hunks、hypothesis text、file read history。

规则：

- 同一命令连续失败 3 次。
- 错误签名相同，期间没有新假设。
- 同一 patch region 反复修改。
- 反复读取文件但没有生成新 decision/hypothesis/next action。

### Evidence Coverage Score

```text
coverage = verified_claims / total_key_claims
```

等级：

- A：关键声明都有当前证据。
- B：大部分关键声明有证据，少数 memory-derived。
- C：依赖较多推断。
- D：大量无证据结论，不适合作为 handoff。

## 14. 隐私与安全

- 原始 session log 默认只存本地。
- 代码内容默认不上传。
- 云端功能显式 opt-in。
- 支持私有部署。
- 导出前 secret scan。
- 敏感信息本地 redaction。
- 每条 memory 有时间、scope、staleness、失效条件。
- 不直接执行 `git push --force`、deploy、secret rotation、DB migration 等高风险操作。

## 15. 技术集成边界

### MVP

- Git：status、diff、log、branch、HEAD。
- 文件系统：repo 配置、Markdown notes、session exports。
- CLI：
  - `contextops init`
  - `contextops import`
  - `contextops pack`
  - `contextops check`
  - `contextops handoff`
- Local Web UI：查看 workspace、session、memory、signals、context pack。
- Agent log adapters：Codex、Claude Code、generic JSONL/Markdown。

### 后续

- GitHub Issues/PRs。
- Linear/Jira。
- Slack handoff。
- VS Code/JetBrains 插件。
- OpenTelemetry-style agent traces。
- LangSmith/Langfuse。

## 16. 成功指标

### MVP 指标

- 每周生成 Context Pack 的活跃 workspace 数。
- 使用 pack 后下一轮 session 前 10 分钟重复询问背景次数下降。
- Handoff pack 平均 evidence coverage 达到 B 级以上。
- Loop 检测被用户认可为真实问题的比例。
- 7 日/30 日留存。

### 长期指标

- 团队任务交接时间下降。
- agent 修复同类问题平均时间下降。
- 用户手动粘贴上下文长度下降。
- durable decisions 数量和复用率增长。
- 错误 repo/branch 操作减少。

## 17. 商业化

- **Free**：单机 local-first、最多 3 个 workspaces、手动导入、基础 pack、基础 drift/loop 检测。
- **Pro ($12-20/月)**：无限 workspace、多 agent adapter、高级 pack 模板、durable decisions、evidence report、本地自动索引。
- **Team ($20-40/seat/月)**：私有团队 memory、RBAC、shared packs、GitHub/Linear/Slack 集成、审计日志、approval workflow。
- **Enterprise**：私有部署、SSO、数据保留策略、内部 agent 平台集成、自定义 adapter。

## 18. 竞品与替代方案

- 普通 summarizer：缺少证据结构，不理解 git/branch/task 状态。
- IDE/agent 自带 memory：绑定单工具，团队交接弱，缺少失效条件。
- LangSmith/Langfuse/Helicone/Braintrust：偏 LLM app observability，不专注软件工程 handoff。
- Notion/Obsidian/Confluence：需要手动维护，不解析 agent session，不检测漂移和循环。

差异化：local-first、Context Pack schema、durable decisions、drift/loop/evidence 检测、跨工具交接。

## 19. 风险与缓解

- **被认为只是 summarizer**：界面突出 evidence、drift、loop、handoff；pack 结构化。
- **日志解析成本高**：MVP 支持 generic Markdown/JSONL，adapter 插件化。
- **误报 drift/loop**：severity、证据解释、false positive 标记。
- **隐私顾虑**：默认 local-first、清晰数据目录、secret redaction、私有部署。
- **memory 过期误导**：每条 memory 有 staleness 和 invalidation rule。
- **用户不愿维护 memory**：自动抽取候选，用户 approve/reject。

## 20. 里程碑

- **M0 概念验证 (2-3 周)**：手动导入 session，生成 Context Pack，支持 git evidence，输出 5 个真实样例。
- **M1 MVP (6-8 周)**：workspace 管理、parser、durable decisions、drift/loop/evidence 检测、本地 UI。
- **M2 Private Beta (8-12 周)**：20-50 名重度用户，调优 signal precision，GitHub PR/issue 集成，secret redaction。
- **M3 Pro Release (12-16 周)**：billing、pack history、memory lifecycle、evidence dashboard。
- **M4 Team (16-24 周)**：team workspace、RBAC、shared decisions、Slack/Linear/GitHub 深集成。

## 21. 开放问题

- 首批支持 Codex、Claude Code、Cursor、Warp、Aider 中哪 2-3 个？
- Context Pack 默认写入 repo 的 `.contextops/`，还是只存在用户本地全局存储？
- 团队版 durable decisions 是否必须 review？
- Drift 检测是否阻断，还是只提示？
- 云端同步是否只同步结构化 memory，不同步原始代码和日志？
- monorepo 如何按 package/service 分层？
- 是否提供一键复制 `prompt_for_next_agent`？

## 22. 参考资料

- OpenAI Codex docs: https://developers.openai.com/codex/
- Anthropic Claude Code memory: https://docs.anthropic.com/en/docs/claude-code/memory
- Sourcegraph context engineering: https://sourcegraph.com/blog/context-engineering
- LangSmith observability: https://docs.smith.langchain.com/observability
- Langfuse tracing: https://langfuse.com/docs/tracing
- OpenTelemetry Generative AI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
