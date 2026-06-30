# PRD: Agent Patterns

日期：2026-06-29  
状态：v0.1 产品草案  
产品类型：可执行 AI agent workflow / pattern library

## 1. 产品定位

Agent Patterns 是面向 AI agent 开发者、coding-agent power user、小团队和开源维护者的可执行 agent workflow library。

它不是 prompt 库，也不是静态 cheatsheet。核心价值是把高质量 agent 工作流沉淀为可搜索、可理解、可 fork、可导出、可运行、可验证的 pattern。

一句话定位：

> GitHub + npm + runbook for executable agent workflows.

## 2. 背景与机会

AI agent 使用者已经从“复制 prompt”进入“沉淀 workflow”的阶段。Codex 支持 AGENTS.md、skills、workflows；Claude Code 支持 skills、slash commands、hooks；LangGraph、OpenAI Agents SDK 等框架把 routing、orchestration、guardrails、handoffs、state 变成一等概念。

但用户真实可复用的资产仍然分散在 prompt、README、Notion、Gist、Cursor rules、CLAUDE.md、AGENTS.md 和私人脚本里。Agent Patterns 的机会在于建立一个跨平台 schema 和导出器，让 workflow 从“文本提示词”升级成“可执行、可验证、可迁移的产品资产”。

## 3. 真实需求证据

证据强度：**High for reusable workflow need; Medium for marketplace monetization**  
完整来源映射见 [market-demand-evidence.md](./market-demand-evidence.md)。

公开需求信号：

- Reddit 用户讨论 AGENTS.md、CLAUDE.md、Gemini.md、skills、slash commands、subagents 标准碎片化，说明跨工具 workflow 复用存在真实摩擦。  
  Sources: https://www.reddit.com/r/ChatGPTCoding/comments/1plotfd/what_happened_with_standardization_amongst_ai/, https://www.reddit.com/r/ClaudeAI/comments/1ped515/understanding_claudemd_vs_skills_vs_slash/
- Reddit 上大量用户分享 Claude Skills、slash commands、AGENTS.md、PM OS、QA/review command packs，说明用户已经在自建 workflow assets。  
  Sources: https://www.reddit.com/r/ClaudeAI/comments/1or0idm/15_custom_slash_commands_turned_claude_code_into/, https://www.reddit.com/r/ClaudeAI/comments/1u87ww5/i_used_claude_code_to_build_a_product_management/, https://www.reddit.com/r/ClaudeAI/comments/1szwvf0/built_a_free_ai_library_100_prompts_120_claude/
- HN 有 “skills are becoming the unit of agent knowledge” 和 skill marketplace 讨论，明确把 skills 看成 tested workflow，而不只是 prompt。  
  Sources: https://news.ycombinator.com/item?id=47475832, https://news.ycombinator.com/item?id=46961474
- OpenAI Codex 官方文档把 skills 定义为 reusable workflows，并支持 AGENTS.md、skills、plugins、MCP。  
  Sources: https://developers.openai.com/codex/skills, https://developers.openai.com/codex/use-cases/reusable-codex-skills, https://developers.openai.com/codex/guides/agents-md, https://developers.openai.com/codex/plugins

PRD 调整结论：

- 首发应聚焦 coding/repo workflows，因为公开分享和实际摩擦最密集。
- 产品必须强调 executable workflow schema、exporter、fixture validation，避免退化成 prompt library。
- Marketplace 变现是中等置信假设；更稳的商业化是 private packs、team registry、verified workflows 和 export history。

## 4. 目标用户

- **AI agent 开发者**：用 LangGraph、OpenAI Agents SDK、Claude Code SDK、MCP、tool calling 搭建 agent 应用。
- **Coding-agent power user**：高频使用 Claude Code、Codex、Cursor、Aider、Warp、Gemini CLI。
- **小型工程团队**：想把团队内有效 agent 流程沉淀为可复用标准。
- **开源维护者**：希望复用 issue triage、PR review、release note、docs sync 等模式。
- **技术内容创作者**：发布 agent workflow 教程、模板、starter pack。
- **企业平台团队**：建立内部 agent pattern registry。

## 5. 核心痛点

- prompt 不稳定：缺少输入/输出契约、工具权限、失败处理和验证方式。
- workflow 难迁移：Claude Skill、Codex AGENTS.md、LangGraph、OpenAI Agents SDK、GitHub Actions 格式不同。
- 高质量 pattern 难发现：互联网上大量“神级 prompt”，但很少说明何时用、何时不用、怎么验证。
- 缺少 runnable proof：模板看起来合理，但没有 fixture、sample input、expected output、run evidence。
- 团队经验难沉淀：一个成员调好的 workflow 很难进入团队标准库。
- 安全边界不清：agent workflow 常涉及文件写入、shell、network、GitHub token、数据库、外发动作。

## 6. 产品目标

### MVP 目标

- 用户 5 分钟内能从任务意图找到一个 pattern，并导出到目标工具。
- 建立统一 workflow schema，覆盖输入、输出、步骤、状态、工具、权限、human gate、failure modes、eval fixture。
- 提供 30-50 个 curated patterns，优先覆盖 coding/repo workflows。
- 支持 fork、配置、导出、dry-run validation。
- 让 pattern 有 provenance、version、risk level、verified status。

### 长期目标

- 成为 AI agent workflow 的公共 registry 和团队私有 registry。
- 形成开源 schema + exporter + curated pack，商业化 team/private workspace。
- 从社区 pattern 扩展到 verified marketplace 和 enterprise internal registry。

## 7. 非目标

- 不做通用 prompt marketplace。
- 不做完整 agent runtime，不替代 LangGraph、Agents SDK、Claude Code、Codex。
- MVP 不托管任意远程代码执行。
- 不保证任意 pattern 在任意模型上成功。
- 不做全功能 eval 平台。
- 不做企业 RPA/iPaaS 全链路自动化。

## 8. MVP 范围

### 必须包含

1. **Pattern Library**：30-50 个 curated patterns。
2. **Search + Filter**：场景、工具、复杂度、导出目标、风险、是否 verified。
3. **Pattern Detail**：用途、适用/不适用场景、workflow、输入输出、工具权限、风险、样例、版本。
4. **Fork + Configure**：修改变量、步骤、工具映射、输出格式、人类确认点。
5. **Export Engine**：
   - Codex `AGENTS.md` 片段。
   - Claude Code Skill (`SKILL.md` + supporting files)。
   - Claude slash command markdown。
   - LangGraph Python skeleton。
   - OpenAI Agents SDK Python/TypeScript skeleton。
   - Generic Markdown runbook。
   - JSON/YAML pattern spec。
6. **Validation**：schema validation、export validation、fixture dry-run。
7. **Community Submission**：schema 校验、unverified 标记、review 流程。

### 暂不包含

- 全量 marketplace 结算。
- 企业 SSO/RBAC。
- 任意远程代码执行托管。
- 自动写入用户 repo 或自动提交 PR。
- 所有 agent 工具的一键同步。

## 9. 核心用户故事

1. 作为 Codex 用户，我想搜索 repository onboarding workflow，并导出为 `AGENTS.md`。
2. 作为 Claude Code 用户，我想把 PR review 风险排序和验证流程导出成 Skill。
3. 作为 LangGraph 开发者，我想把 planner-worker-reviewer pattern 导出成 Python skeleton。
4. 作为团队负责人，我想 fork docs sync pattern，改成团队内部规范并放进 private pack。
5. 作为开源维护者，我想发布 issue triage pattern，并附带 fixture 和 expected labels。
6. 作为安全敏感用户，我想在导出前看到 workflow 会使用哪些权限和 human gate。
7. 作为 pattern 作者，我想知道 pattern 被 fork、导出、运行和失败的情况。

## 10. 信息架构

- **Discover**：搜索和浏览 pattern。
- **Patterns**：分类库、排行榜、verified collections。
- **Builder**：创建、fork、编辑 pattern。
- **Validate**：schema 校验、fixture dry-run、export validation。
- **Exports**：导出历史、目标平台配置。
- **Collections**：个人/团队 pattern pack。
- **Community**：提交、review、讨论、贡献指南。
- **Docs**：schema、exporter、CLI、API。

Pattern detail 页面：

- Header：标题、摘要、成熟度、兼容目标、风险等级。
- Use Case：解决什么问题，何时使用，何时不要使用。
- Workflow：步骤图、agent roles、state、human gates。
- Inputs/Outputs：字段、类型、示例。
- Tools & Permissions：工具、权限、风险。
- Execution：sample input、expected output、run evidence。
- Export：目标平台按钮和配置项。
- Versions/Forks：版本历史、热门 fork、变更说明。

## 11. 关键功能

### 10.1 Pattern Discovery

- 自然语言搜索：例如“让 Codex review PR 并生成修复计划”。
- 标签过滤：coding、research、QA、docs、triage、release、security、multi-agent。
- Badge：verified、runnable、has fixture、high-risk tools、local-first。

### 10.2 Pattern Builder

- 表单 + YAML/JSON 双模式。
- 自动校验必填字段。
- 检查缺失输入、未声明输出、未配置工具权限、无 failure mode。
- 支持从 `AGENTS.md` / `CLAUDE.md` / `SKILL.md` 反向导入为 draft pattern。

### 10.3 Executable Workflow Model

支持 pattern 类型：

- sequential。
- routing。
- parallel review。
- orchestrator-worker。
- evaluator-optimizer。
- human-in-the-loop。
- incident/debug loop。

### 10.4 Export Engine

- 将统一 schema 编译成目标平台文件树。
- 导出前展示 diff 和文件列表。
- 对目标平台不支持的能力显式降级，例如 no state persistence、no subagent。
- 每个 exporter 有 fixture test。

### 10.5 Safety Layer

权限风险等级：

- read-only。
- write-files。
- shell。
- network。
- secrets。
- external side effects。

高风险 pattern 必须声明 human gate。社区 pattern 默认不能标为 verified。

## 12. Pattern Schema v0.1

```yaml
id: agent-pattern.pr-review-risk-plan.v1
title: PR Review Risk Plan
summary: Review a pull request, rank risks, propose fixes, and produce verification commands.
category: coding.pr_review
maturity: verified # draft | community | runnable | verified | deprecated

problem:
  statement: Maintainers need repeatable PR review beyond generic comments.
  when_to_use:
    - Reviewing non-trivial code changes
    - Need ranked findings with file references
  when_not_to_use:
    - Pure style review
    - No repository access

compatibility:
  exports:
    - codex.agents_md
    - claude.skill
    - claude.slash_command
    - langgraph.python
    - openai_agents_sdk.python
  required_capabilities:
    - tool_calling
    - structured_output
    - file_access

inputs:
  - name: pr_url
    type: string
    required: true
  - name: repo_path
    type: path
    required: false

outputs:
  - name: findings
    type: array
  - name: verification_plan
    type: markdown
  - name: residual_risks
    type: markdown

workflow:
  type: evaluator_optimizer
  steps:
    - id: collect_context
      role: reviewer
      action: inspect_diff
      tools: [git, github]
      outputs: [diff, changed_files]
    - id: identify_risks
      role: reviewer
      action: analyze
      guardrails:
        - cite_file_lines
        - no_style_only_comments
    - id: verify_findings
      role: tester
      action: run_relevant_checks
      tools: [shell]
      human_gate: before_shell_if_destructive
    - id: produce_review
      role: reviewer
      action: structured_output

tools:
  - name: git
    permission: read
  - name: shell
    permission: read_execute
    constraints:
      - no_destructive_commands
  - name: github
    permission: read

human_gates:
  - id: approve_external_comment
    required_before:
      - post_github_review

failure_modes:
  - condition: tests_unavailable
    behavior: report_unverified_findings
  - condition: diff_too_large
    behavior: summarize_scope_and_request_narrowing

evals:
  fixtures:
    - name: simple_backend_pr
      input: fixtures/simple_backend_pr.json
      expected:
        min_findings: 1
        requires_file_references: true

exports:
  codex.agents_md:
    template: exports/codex-agents-md.md
  claude.skill:
    template: exports/claude-skill/
  langgraph.python:
    template: exports/langgraph-python/

license: Apache-2.0
version: 1.0.0
provenance:
  source: curated
```

必填字段：`id`、`title`、`summary`、`problem`、`inputs`、`outputs`、`workflow.steps`、`tools`、`failure_modes`、`exports`、`license`、`version`。

## 13. 导出目标

### MVP

- **Codex AGENTS.md**：setup、workflow、done-when、verification commands、constraints。
- **Claude Code Skill**：`SKILL.md`、frontmatter、supporting files、examples。
- **Claude Slash Command**：适合轻量过程调用。
- **LangGraph Python Skeleton**：StateGraph、state schema、nodes、edges、tool stubs、fixture。
- **OpenAI Agents SDK Skeleton**：agent definitions、handoffs、guardrails、tools、structured output。
- **Generic Markdown Runbook**：适合 README/wiki/internal docs。
- **JSON/YAML Spec**：portable source of truth。

### 后续

- GitHub Actions agentic workflow。
- Cursor rules。
- MCP server/tool config。
- CrewAI/AutoGen/Semantic Kernel skeleton。
- n8n/Zapier agent workflow draft。

## 14. 社区与开源策略

推荐 open-core。

开源：

- Pattern schema。
- 官方基础 pattern pack。
- Export templates。
- CLI validator。
- Example fixtures。
- Contribution guide。

商业：

- 私有 pattern workspace。
- 团队权限与审核流。
- Hosted semantic search。
- BYOK runner。
- Export history。
- Team analytics。
- Verified enterprise packs。
- 内部 registry 同步。

质量等级：

- Draft：个人草稿。
- Community：通过 schema，未验证。
- Runnable：有 fixture 和成功 dry-run。
- Verified：维护者审核，至少 2 个 export target 成功。
- Deprecated：平台 API 或安全原因不再推荐。

## 15. 成功指标

North Star Metric：Weekly Verified Pattern Exports。

### 激活指标

- 首次访问到首次 export 时间 < 5 分钟。
- 搜索到 fork 转化率。
- Pattern detail 到 export 点击率。
- 新用户 24 小时内导出成功率。

### 质量指标

- Verified pattern dry-run pass rate。
- Export failure rate。
- 用户报告“导出后跑不通”比例。
- Pattern 被重复使用次数。

### 社区指标

- 每周新增 community pattern。
- Community -> verified 转化率。
- Fork -> upstream PR 比例。
- 活跃贡献者数。

### 商业指标

- Free -> Pro 转化率。
- Team workspace 创建数。
- 每个 team 的 private pattern 数。
- 月活团队留存。

## 16. 商业化

- **Free**：公开 pattern library、搜索、查看、导出、有限个人 fork、本地 CLI validator。
- **Pro ($12-20/月)**：无限私有 fork、BYOK sample runner、高级导出、export history、collections、version pinning。
- **Team ($25-40/seat/月)**：团队 workspace、私有 packs、审核流、团队导出规范、usage analytics、GitHub repo sync。
- **Enterprise**：SSO、私有部署、内部 registry、自定义 exporters、审计日志、安全策略、专属 verified pack。

商业化原则：不卖 prompt，卖 workflow 资产管理、可运行验证、团队治理和跨平台导出。

## 17. 竞品与替代方案

- Prompt libraries / Prompt Hub：偏 prompt 管理，不是完整 workflow。
- LangGraph docs/examples：强框架，弱跨平台 marketplace。
- Claude Code Skills：平台内复用强，但缺少跨平台 schema 和 registry。
- Codex AGENTS.md：项目指令机制强，但不是完整 pattern registry。
- Cursor rules / community repos：轻量但碎片化。
- Notion/Gist/README：灵活但不可验证、不可导出、难版本化。

## 18. 风险与缓解

- **被误解成 prompt 库**：命名、页面、schema、badge 都强调 workflow/run/export/eval。
- **跨平台导出维护成本高**：MVP 只支持高价值目标，exporter 插件化。
- **社区内容质量低**：分级、verified badge、review、run evidence。
- **平台变化快**：schema 与 exporter 解耦，export target 版本锁定。
- **运行安全风险**：默认 dry-run，高风险工具显式标记，human gate。
- **pattern 过抽象**：首批 pattern 必须来自真实任务，带 sample run 和具体文件导出。

## 19. 里程碑

- **M0 需求验证 (2 周)**：访谈 15-20 个 power users，收集 50 个真实 workflows，确认 5 个高频场景。
- **M1 Schema + Curated Repo (3-4 周)**：schema v0.1、开源 repo、20 个 curated patterns、CLI validator、Codex/Claude exporter。
- **M2 Web MVP (4-6 周)**：Discover、Detail、Fork、Export、GitHub login、30-50 patterns、LangGraph/OpenAI exporter。
- **M3 Runnable Beta (6-8 周)**：fixture dry-run、export validation、BYOK sample runner、community submission。
- **M4 Public Beta (8-12 周)**：社区贡献、verified badge、collections、Pro 试点。
- **M5 Team/v1 (3-6 个月)**：team workspace、私有 pack、审核流、GitHub sync、analytics。

## 20. 开放问题

- MVP 是否只聚焦 coding agents？
- Hosted runner 要做到什么程度？
- Pattern 内容许可证如何设计？
- 是否需要浏览器扩展或 IDE 插件？
- Verified 标准由谁决定？
- Export 是否允许自动写入用户 repo？
- 是否支持非代码场景？
- 是否做 AI pattern advisor？

## 21. 参考资料

- OpenAI Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex reusable skills: https://developers.openai.com/codex/use-cases/reusable-codex-skills
- OpenAI Agents SDK: https://developers.openai.com/codex/guides/agents-sdk
- Claude Code Skills: https://docs.anthropic.com/en/docs/claude-code/skills
- LangGraph workflows and agents: https://docs.langchain.com/oss/python/langgraph/workflows-agents
- LangSmith prompt management: https://docs.smith.langchain.com/prompt-engineering
- AGENTS.md open format: https://agents.md/
