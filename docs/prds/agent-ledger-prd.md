# PRD: Agent Ledger

日期：2026-06-29  
状态：v0.1 产品草案  
产品类型：Personal Agent Governance / Audit Tool

## 1. 产品定位

Agent Ledger 是面向个人 power user、freelancer、小团队和企业前哨用户的 AI agent 风险发现、审计台账与合规报告工具。

它不是先让用户填写治理表、权限矩阵或审批流程，而是先自动发现用户已经在使用的 agent、automation、API key、OAuth app、脚本和敏感操作风险，并生成可读、可导出的治理报告。

一句话定位：

> A personal AI agent audit ledger that discovers shadow agents before they become incidents.

## 2. 背景与机会

agent 工具正在从开发者实验进入个人工作流、小团队运营和客户交付。用户会给 agent 访问 repo、shell、邮箱、Google Drive、Slack、CRM、GitHub、浏览器自动化、付费 API 的权限，但缺少统一台账和审计。

企业级 AI governance、SIEM、IAM、DLP、GRC 工具门槛高，个人和小团队通常不会先采购这些平台。Agent Ledger 的机会是做轻量、local-first、报告导向的前哨工具：先发现、再解释、再建议策略，最后才进入审批和阻断。

## 3. 真实需求证据

证据强度：**High for risk visibility; Medium for personal/freelancer paid product**  
完整来源映射见 [market-demand-evidence.md](./market-demand-evidence.md)。

公开需求信号：

- Reddit SaaS/sysadmin/infosec 讨论集中在 AI agent governance owner、spend controls、approval thresholds、audit trails、shadow AI visibility。  
  Sources: https://www.reddit.com/r/SaaS/comments/1rwngan/who_owns_ai_agent_governance_at_your_company_and/, https://www.reddit.com/r/sysadmin/comments/1s6wkpi/this_latest_ai_tools_wave_is_the_new_shadow_it/, https://www.reddit.com/r/Information_Security/comments/1rv1kgq/ai_agents_starting_to_feel_like_the_new_shadow_it/
- Reddit 出现 agent runaway cost 案例，例如 AI agent 烧掉 700+ 美元、Replit Agent 10 天扣费 355 美元，说明 budget/cap/alert 是真实痛点。  
  Sources: https://www.reddit.com/r/AI_Agents/comments/1qvcpkf/trusting_my_ai_agent_cost_me_over_usd_700/, https://www.reddit.com/r/replit/comments/1ryocv7/i_am_a_beginner_developer_facing_a_financial/
- Reddit 用户担心 destructive actions、wrong emails、deleted data、client data exposure、tiered permission/human approval。  
  Sources: https://www.reddit.com/r/AI_Agents/comments/1rz0gyr/things_nobody_warns_you_about_when_you_give_an/, https://www.reddit.com/r/openclaw/comments/1rb84h4/ways_openclaw_has_changed_my_life/, https://www.reddit.com/r/fintech/comments/1sz5ktl/are_fintech_teams_actually_blocked_from_putting/
- Microsoft 官方已有组织级 agent governance/security 指南，行业资料也在讨论 agentic AI oversight。  
  Sources: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization, https://www.datagrail.io/blog/ai-governance/ai-agent-policy/

PRD 调整结论：

- MVP 必须从 scan and report 切入，不要先做复杂策略配置。
- 报告和 evidence bundle 是核心价值，不是附属导出。
- Personal/freelancer 付费需验证；更稳的首批付费场景可能是 freelancer-client report、小团队 shadow agent scan、enterprise pilot。

## 4. 目标用户

### 个人 power user

- 使用 Codex、Claude Code、Cursor、ChatGPT Tasks、browser agent、n8n、Zapier、Make、自写脚本。
- 关心哪些工具有 token、哪些能改文件、哪些能发邮件、哪些会花钱。

### freelancer / consultant

- 同时服务多个客户，agent 可能接触客户 repo、文档、邮箱、CRM。
- 需要向客户证明“我使用 AI 工具但有边界、有记录、有审计”。

### 小团队 founder / ops / engineering lead

- 成员各自接入 AI 工具，缺少全局权限视图。
- 希望低成本建立 AI 使用台账和风险周报。

### 企业前哨用户

- AI task force、security champion、innovation team。
- 在正式采购企业治理平台前，先摸清 shadow agent、权限暴露、敏感数据风险。

## 5. 核心痛点

- **agent 无审计**：难以回答谁触发、用了什么模型、访问什么数据、调用什么工具、成本多少、是否敏感。
- **无所有者**：agent、automation、API key、OAuth app 没有明确 owner。
- **permission fatigue**：用户面对大量授权，最终全量允许，事后没有风险摘要。
- **shadow agent**：团队成员私自使用 browser agent、bot、script、workflow automation，组织无可见性。
- **预算失控**：agent loop、批处理、自动化任务持续消耗 API/SaaS/cloud 额度。
- **敏感操作失控**：删除文件、发邮件、git push、改 CRM、访问客户数据、调用 shell、生产配置。
- **合规证明困难**：freelancer、小团队和企业试点只能口头解释 AI 使用边界。

## 6. 产品目标

### MVP 目标

- 10 分钟内帮助用户发现至少一类 agent/automation/AI 工具风险。
- 自动生成 Agent Governance Report。
- 建立统一 Agent Ledger：agent、owner、权限、敏感操作、预算、审计事件。
- 用默认风险检测和报告替代复杂治理表单。

### 中期目标

- 成为个人和小团队的 AI agent 审计首页。
- 支持多源日志导入、连接器、策略建议、审批记录和报告导出。
- 让用户从“发现风险”自然过渡到“设置策略”。

### 长期目标

- 成为企业前哨级 agent governance layer，可与 SIEM、DLP、IAM、MDM、LLM observability、GRC 集成。

## 7. 非目标

- MVP 不做完整 IAM 替代品。
- MVP 不承诺拦截所有本地或云端 agent 行为。
- MVP 不做重型 GRC 工作流、复杂审批引擎或法规自动判责。
- MVP 不要求用户手动录入完整组织架构、权限矩阵、数据分类表。
- MVP 不做模型质量评测平台。
- MVP 不默认存储原始 prompt、文件内容或 secret。

## 8. MVP 范围

### 必须包含

1. Agent / automation 自动发现。
2. Agent inventory。
3. Owner / workspace / source 标记。
4. 审计事件 ingestion。
5. 风险评分。
6. Shadow agent 检测。
7. 敏感操作识别。
8. 预算/token/API cost 摘要。
9. 周报、客户报告、治理报告生成。
10. 本地优先隐私模式。
11. 基础策略建议。

### MVP 发现来源

- 本地配置：`.env`、agent config、MCP config、CLI config、automation config。
- 开发工具：Codex、Claude Code、Cursor、GitHub Copilot 类工具的配置或日志。
- API 使用：OpenAI、Anthropic、Google、Groq、OpenRouter key pattern，本地 fingerprint，不上传 secret。
- 自动化平台：Zapier、Make、n8n、GitHub Actions、cron、launchd。
- SaaS/OAuth：Google Workspace、Slack、GitHub、Notion 授权 app 清单，优先 read-only。
- 日志导入：JSONL、CSV、OpenTelemetry-style trace、LLM gateway logs。

### 暂不包含

- 不默认读取用户文件内容。
- 不自动撤销权限。
- 不主动修改 SaaS 配置。
- 不做强制阻断，除非用户使用官方 proxy/wrapper。

## 9. 核心用户故事

1. 作为个人用户，我要扫描本机和常用工具，看到哪些 agent 能访问文件、代码、邮箱或 API key。
2. 作为个人用户，我要知道过去一周有哪些敏感操作，例如 shell、git push、邮件发送、文件删除。
3. 作为 freelancer，我要为每个客户生成 AI 使用审计报告，说明接入了哪些 agent、访问哪些系统、是否有敏感操作。
4. 作为 freelancer，我要把客户 A 和客户 B 的 agent、文件、token、日志隔离。
5. 作为团队负责人，我要看到 shadow agent、无 owner API key、高风险 OAuth app。
6. 作为安全负责人，我要先用轻量工具摸清 agent 暴露面，再决定是否采购企业平台。

## 10. 信息架构

- **Dashboard**：总风险分、本周新增 agent、未归属 agent、shadow agent、高危权限、敏感操作、预算异常、最新报告。
- **Inventory**：Agents、Tools、Connectors、API keys、OAuth apps、Automations、Workspaces/Clients、Owners。
- **Risk Radar**：shadow agent、unowned agent、sensitive access、dangerous action、over-permissioned tool、budget anomaly、missing logs、unknown vendor。
- **Agent Ledger**：event timeline、run/session view、tool calls、policy evaluations、approvals、evidence hashes、export。
- **Policies**：default templates、approval rules、budget rules、sensitive action rules、data boundary rules、client/workspace rules。
- **Reports**：personal weekly、client audit、team governance、incident report、CSV/PDF/Markdown/JSON evidence bundle。
- **Integrations**：local scanner、CLI wrapper、browser extension、GitHub、Slack、Google Workspace、n8n/Zapier/Make、LLM gateway logs。
- **Settings**：privacy mode、retention、redaction、workspace members、export keys、billing。

## 11. 关键功能

### 10.1 自动发现

发现对象：

- 本地 agent 配置。
- MCP server 配置。
- API key pattern。
- OAuth app。
- automation job。
- browser extension。
- GitHub App / bot。
- Slack bot。
- scheduled job。
- LLM proxy/gateway。
- 未知脚本中的 LLM API 调用。

输出字段：

- agent 名称。
- 来源。
- 推断 owner。
- 权限范围。
- 访问系统。
- 风险等级。
- 是否需要用户确认。

### 10.2 Agent Inventory

每个 agent 记录：

- 名称。
- 类型：coding agent、browser agent、workflow agent、chat assistant、custom script、SaaS bot。
- owner。
- workspace/client。
- vendor/model provider。
- connected tools。
- granted permissions。
- budget profile。
- last seen。
- last sensitive action。
- logging coverage。
- status：active、inactive、unknown、shadow、archived。

### 10.3 Risk Scoring

风险维度：

- 无 owner。
- write/delete/send/execute 权限。
- 可访问敏感数据。
- 连接多个系统。
- 没有日志。
- 成本异常。
- 未知模型或 vendor。
- 跨 client/workspace。
- 长期未审查。
- 明文 secret 暴露。

等级：

- Low：只读、低敏、owner 明确、有日志。
- Medium：有限写权限、部分敏感数据、日志不完整。
- High：高敏数据、外发能力、执行能力、预算异常。
- Critical：无 owner + 高敏 + 可执行/可外发/可删除。

### 10.4 Agent Ledger

能力：

- 时间线查询。
- 按 agent、owner、workspace、client 过滤。
- 敏感操作高亮。
- 成本聚合。
- policy evaluation 记录。
- approval 记录。
- evidence hash。
- 导出审计包。

### 10.5 策略建议

MVP 不要求用户写策略，而是生成建议：

- “这个 GitHub bot 有 write 权限但没有 owner，建议指定 owner。”
- “这个 agent 可访问客户 A 和客户 B 的目录，建议分离 workspace。”
- “这个 API key 过去 7 天成本增长 320%，建议设置预算阈值。”
- “这个 automation 能发送邮件但没有审计日志，建议接入 wrapper 或关闭自动发送。”

### 10.6 报告生成

模板：

- Personal Agent Risk Weekly。
- Freelancer Client AI Usage Report。
- Team Shadow Agent Report。
- Sensitive Action Audit Report。
- Budget and Usage Report。
- Incident Evidence Packet。

格式：Markdown、PDF、CSV、JSON evidence bundle。

## 12. 审计事件 Schema v1

```json
{
  "event_id": "evt_01h...",
  "schema_version": "1.0",
  "occurred_at": "2026-06-29T10:20:30Z",
  "ingested_at": "2026-06-29T10:20:35Z",
  "source": {
    "type": "local_cli | browser_extension | llm_gateway | saas_connector | imported_log",
    "name": "codex-cli",
    "connector_version": "0.1.0"
  },
  "workspace": {
    "id": "ws_123",
    "name": "Client A",
    "environment": "local | dev | staging | production"
  },
  "actor": {
    "user_id": "user_123",
    "email_hash": "sha256:...",
    "role": "owner | member | external"
  },
  "agent": {
    "agent_id": "agent_123",
    "name": "Repo Coding Agent",
    "type": "coding_agent | browser_agent | workflow_agent | custom_script",
    "vendor": "OpenAI",
    "model": "gpt-5-codex",
    "owner_id": "user_123",
    "status": "known | shadow | unknown"
  },
  "run": {
    "run_id": "run_123",
    "session_id": "sess_123",
    "task_id": "task_123",
    "parent_event_id": "evt_parent"
  },
  "action": {
    "kind": "read | write | delete | execute | send | approve | spend | connect",
    "name": "git_push",
    "description": "Pushed branch to GitHub"
  },
  "target": {
    "system": "github",
    "resource_type": "repository",
    "resource_id_hash": "sha256:...",
    "resource_label": "private_repo_redacted",
    "sensitivity": "public | internal | confidential | restricted",
    "client_boundary": "client_a"
  },
  "tool_call": {
    "tool_name": "git",
    "arguments_hash": "sha256:...",
    "raw_arguments_stored": false
  },
  "data_exposure": {
    "input_classes": ["source_code", "customer_data"],
    "output_classes": ["code_patch"],
    "raw_content_stored": false,
    "redaction_applied": true
  },
  "cost": {
    "provider": "openai",
    "input_tokens": 12000,
    "output_tokens": 1800,
    "estimated_usd": 0.42
  },
  "policy_evaluations": [
    {
      "policy_id": "pol_sensitive_send",
      "result": "allow | warn | require_approval | block",
      "reason": "Sensitive external send requires approval"
    }
  ],
  "approval": {
    "required": true,
    "approved_by": "user_123",
    "approved_at": "2026-06-29T10:21:00Z",
    "approval_mode": "manual | preapproved | bypassed"
  },
  "outcome": {
    "status": "success | failed | blocked | partial",
    "error_code": null,
    "error_message_redacted": null
  },
  "risk": {
    "score": 82,
    "level": "high",
    "factors": ["write_permission", "confidential_data", "external_system"]
  },
  "evidence": {
    "event_hash": "sha256:...",
    "previous_event_hash": "sha256:...",
    "tamper_evident_chain": true
  },
  "retention": {
    "retain_until": "2027-06-29",
    "privacy_mode": "metadata_only"
  }
}
```

## 13. 策略与权限模型

原则：

- 默认先观察，再建议，再执行拦截。
- owner 必须明确。
- 权限按 workspace/client/environment 隔离。
- 高危动作需要 approval 或事后审计。
- 内容最小化采集，优先 metadata-only。

策略类型：

- Owner policy：所有 active agent 必须有 owner。
- Workspace policy：agent 不得跨 client 访问资源。
- Sensitive action policy：send、delete、execute、production write 需要审批。
- Data policy：restricted 数据不得发送到未批准 provider。
- Budget policy：按 agent/workspace/provider 设置阈值。
- Logging policy：高危 agent 必须开启 ledger logging。
- Vendor policy：限制未知模型、未知 SaaS、未批准 browser extension。

执行模式：

- Observe：只记录。
- Notify：记录并提醒。
- Require approval：需要用户确认。
- Block：通过官方 proxy/wrapper 阻断。
- Quarantine：标记为 shadow/disabled，需要人工处理。

MVP 以 Observe 和 Notify 为主。

## 14. 隐私与安全

- 不上传 secret。
- 不存原始文件内容。
- 不默认存 raw prompt/raw output。
- 对 email、路径、repo、文件名提供 hash/redaction。
- local-only 模式。
- 云同步显式开启。
- API key 只做本地 fingerprint。
- SaaS connector 默认 read-only。
- evidence hash 防篡改。
- retention policy。
- report watermark。

## 15. 技术集成边界

### MVP 集成

- Local scanner CLI。
- Desktop/local web app。
- JSONL log import。
- GitHub read-only connector。
- Slack app inventory。
- Google OAuth app inventory。
- n8n/Zapier/Make metadata import。
- LLM gateway log import。
- Basic browser extension。

### 后续集成

- SIEM：Splunk、Datadog、Elastic。
- IAM：Okta、Google Workspace、Microsoft Entra。
- DLP/CASB。
- MDM/endpoint security。
- LLM observability：LangSmith、Langfuse、Arize、Braintrust、Helicone。
- GRC：Vanta、Drata、Secureframe。

边界：不替代 SIEM、IAM、LLM observability、DLP、GRC；不声称自动合规，只提供审计证据和报告辅助。

## 16. 成功指标

### 激活指标

- 首次扫描完成率。
- 首次发现风险时间 < 10 分钟。
- 首次报告生成率。
- 用户连接 source 数量。

### 价值指标

- 每周发现 shadow agent 数。
- 无 owner agent 降低比例。
- 高风险权限降低比例。
- 敏感操作审计覆盖率。
- 预算异常发现数。

### 留存指标

- 周报打开率。
- 月度报告导出率。
- 每周 active workspace 数。
- 风险建议处理率。

### 商业指标

- Free -> Pro 转化率。
- Freelancer 报告导出付费率。
- Team workspace 付费率。
- 企业试点转化率。

## 17. 商业化

- **Free**：本地扫描、最多 5 个 agent、基础风险报告、metadata-only ledger、Markdown 导出。
- **Pro ($12-20/月)**：个人无限 agent、周报、客户 workspace、PDF 报告、预算监控、历史 ledger。
- **Freelancer ($29-49/月)**：多客户隔离、Client AI Usage Report、Evidence bundle、自定义品牌报告。
- **Team ($15-30/seat/月)**：多成员、owner 分配、team dashboard、shared policies、Slack alert、GitHub/Google/Slack connector。
- **Enterprise Pilot**：SSO、SIEM export、retention policy、audit role、private deployment、custom connector。

## 18. 竞品与替代方案

- **LLM observability**：LangSmith、Langfuse、Arize Phoenix、Braintrust、Helicone、Datadog LLM Observability。强 trace/eval/debug，弱个人 agent、shadow agent、OAuth、预算和客户报告。
- **企业 AI governance/security**：Zenity、Credo AI、DataGrail、Domo 等。强企业合规，弱个人/freelancer/小团队低摩擦。
- **IAM/SaaS 管理/CASB**：Okta、Microsoft Entra、Torii、BetterCloud。强身份和 SaaS 权限，弱 agent run/tool call/model cost。
- **手工替代**：Spreadsheet、Notion、手写 AI 使用政策。便宜但无法自动发现、持续审计和提供强证据。

差异化：personal/freelancer/small team first、自动发现优先、Agent Ledger 统一 owner/权限/事件/预算/报告、报告是核心产品。

## 19. 风险与缓解

- **隐私顾虑**：local-only、metadata-only、secret 不上传、内容采集显式开关。
- **自动发现误报**：透明解释，允许确认/忽略/合并 agent。
- **集成碎片化**：MVP 优先 local scanner、JSONL import、GitHub/Slack/Google read-only。
- **治理概念太重**：默认首页展示“发现了什么风险”和“可导出什么报告”。
- **无法真正 enforcement**：清晰区分 observe/notify/approval/block。
- **合规声明过度**：定位为 audit evidence/report，不声称自动满足 SOC 2、ISO、GDPR、EU AI Act。
- **企业平台下沉竞争**：坚持低摩擦个人和 freelancer 场景。

## 20. 里程碑

- **M0 用户验证 (2 周)**：访谈 20 个 power user/freelancer/小团队 lead，收集使用清单，确定 20 个风险 pattern，设计报告样张。
- **M1 Local Scanner + Report (4 周)**：扫描 CLI、API key fingerprint、agent config detection、automation detection、basic inventory、Markdown/PDF 报告。
- **M2 Agent Ledger (4-6 周)**：事件 schema、JSONL import、timeline、risk score、evidence hash、workspace/client 隔离。
- **M3 Connectors (6 周)**：GitHub、Slack、Google、n8n/Zapier/Make import、weekly report。
- **M4 Team Beta (6 周)**：多用户、owner assignment、shared policies、Slack alert、team report、billing。
- **M5 Governance Layer (8-12 周)**：CLI wrapper、LLM gateway integration、approval flow、SIEM export、enterprise pilot package。

## 21. 开放问题

- MVP 应优先桌面 app，还是 CLI + web dashboard？
- 首批重点用户是 freelancer，还是 AI-heavy engineering team？
- 浏览器扩展是否进入 MVP？
- Agent Ledger 是否默认本地存储，云端只同步摘要？
- 报告是否作为主要付费点？
- 是否优先深做 Codex/Claude Code/Cursor？
- tamper-evident hash chain 是否作为早期差异化？
- 第一版是否支持真正 block，还是只 observe/notify？
- 如何定义 shadow agent：未登记、无 owner、未知来源，还是任一即可？

## 22. 参考资料

- Microsoft agent governance and security guidance: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization
- OpenTelemetry Generative AI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- Arize AI agent observability: https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/
- Zenity AI agent governance: https://zenity.io/blog/security/ai-agent-governance
- DataGrail AI agent policy: https://www.datagrail.io/blog/ai-governance/ai-agent-policy/
- Microsoft Entra app governance overview: https://learn.microsoft.com/en-us/defender-cloud-apps/app-governance-manage-app-governance
