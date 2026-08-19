#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

from session_log_utils import iter_jsonl, load_codex_session_meta, redact_and_truncate, sanitize_output


CATEGORY_SPECS = [
    ("threads_parallel", r"threads|parallel|worktree|multi.*agent|sub.?agent|并行|多.*agent|子agent"),
    ("feature_audit", r"go over every feature|feature inventory|user story|每个功能|所有功能|用户故事"),
    ("start_latest", r"update.*latest.*start|start.*latest|更新.*最新.*启动|启动.*最新|拉.*最新.*启动"),
    ("pr_gate_merge", r"merge-ready|merge ready|pr gate|review.*PR|PR.*review|能不能\s*merge|可以\s*merge|合并"),
    ("issue_closeout", r"issue.*fixed|close issue|fixed.*issue|真的修好|关闭\s*issue|这个 issue|修好了吗"),
    ("publish_release", r"publish|release|tag|public repo|GitHub public repo|发布|推送"),
    ("skill_creation", r"skill|SKILL\.md|Agent Patterns|agent patterns|做成.*skill|创建.*skill|沉淀|更新skill"),
    ("context_resume", r"handoff|compaction|resume|context|刚才|继续|之前|上下文|恢复|接着"),
    ("runtime_debug", r"localhost|127\.0\.0\.1|port|dev server|login|端口|启动|页面|浏览器|僵尸进程|服务"),
    ("memory_remem", r"remem|memory|记忆|召回|\bmem\b"),
    ("x_looper_content", r"looper|x-reply|reply queue|tweet|twitter|\bX\b|小红书|post"),
    ("prd_spec_arch", r"\bPRD\b|spec|design doc|roadmap|需求|产品|技术方案|方案|架构"),
    ("repo_onboarding", r"这个库|这个目录|这个 repo|有什么用|看下.*目录|看下.*库|readme|repo"),
    ("browser_chrome", r"chrome|browser|DevTools|playwright|screenshot|浏览器"),
    ("remote_deploy", r"\bssh\b|deploy|tunnel|服务器|VPS|远程|部署"),
    ("docs_report", r"Lark|wiki|docs|report|slides|ppt|pdf|excel|spreadsheet|飞书|文档|报告"),
    ("visual_media", r"image|video|screenshot|App Store|seedance|kling|VSR|SR|图片|视频"),
    ("config_logs", r"config\.toml|hooks\.json|logs_2\.sqlite|settings|popup|日志"),
    ("github_ops", r"GitHub|\bgh\s+|PR\s*#|repo create|pull request|issues?"),
]

CANDIDATE_SPECS = [
    {
        "skill": "agent-session-pattern-miner",
        "action": "new-skill",
        "categories": ["skill_creation", "repo_onboarding", "context_resume"],
        "risk_level": "medium",
        "reason": "The user repeatedly asks to inspect agent history and turn recurring work into reusable skills.",
    },
    {
        "skill": "context-handoff-pack",
        "action": "enhance-existing",
        "categories": ["context_resume"],
        "risk_level": "medium",
        "reason": "Resume and compaction requests need source-specific reconstruction from local session records.",
    },
    {
        "skill": "repo-publish-gate",
        "action": "new-skill",
        "categories": ["publish_release", "github_ops"],
        "risk_level": "high",
        "reason": "Publishing requires clean worktree, tests, remote visibility, tags, and live verification.",
    },
    {
        "skill": "github-closeout-audit",
        "action": "new-skill",
        "categories": ["pr_gate_merge", "issue_closeout", "github_ops"],
        "risk_level": "high",
        "reason": "PR and issue closeout work needs live GitHub, CI, review-thread, and remote SHA evidence.",
    },
    {
        "skill": "local-runtime-doctor",
        "action": "new-skill",
        "categories": ["runtime_debug", "browser_chrome", "config_logs"],
        "risk_level": "medium",
        "reason": "Local app failures recur around ports, browser state, services, logs, and runtime drift.",
    },
    {
        "skill": "multi-agent-lane-map",
        "action": "new-skill",
        "categories": ["threads_parallel"],
        "risk_level": "medium",
        "reason": "Parallel agent work needs explicit lane ownership, verification, and mergeback rules.",
    },
    {
        "skill": "repo-meaning-quickscan",
        "action": "new-skill",
        "categories": ["repo_onboarding"],
        "risk_level": "low",
        "reason": "Repository orientation requests recur and benefit from a compact evidence-first scan.",
    },
]

COMPILED_CATEGORIES = [(name, re.compile(pattern, re.IGNORECASE | re.DOTALL)) for name, pattern in CATEGORY_SPECS]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mine local agent session records into workflow-pattern candidates.")
    parser.add_argument("--home", default=str(Path.home()), help="Home directory containing .codex and .claude")
    parser.add_argument("--source", choices=["codex", "claude", "both"], default="both")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--include-examples", action="store_true", help="Include short redacted source excerpts")
    parser.add_argument("--limit-projects", type=int, default=12)
    args = parser.parse_args(argv)

    home = Path(args.home).expanduser()
    result = mine(home, args.source, args.include_examples, args.limit_projects)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print_mining_text(result)
    return 0


def mine(home: Path, source: str, include_examples: bool, limit_projects: int) -> dict[str, Any]:
    aggregate = empty_aggregate()
    if source in {"codex", "both"}:
        merge_aggregate(aggregate, mine_codex(home, include_examples))
    if source in {"claude", "both"}:
        merge_aggregate(aggregate, mine_claude(home, include_examples))

    categories = []
    for name, count in aggregate["category_counts"].most_common():
        categories.append(
            {
                "id": name,
                "messages": count,
                "sessions": len(aggregate["category_sessions"][name]),
                "projects": len(aggregate["category_projects"][name]),
                "examples": aggregate["examples"].get(name, []),
            }
        )

    candidates = rank_candidates(
        aggregate["category_counts"],
        aggregate["category_sessions"],
        aggregate["category_projects"],
    )
    result = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "home": str(home),
        "sources": aggregate["sources"],
        "totals": dict(aggregate["totals"]),
        "categories": categories,
        "candidates": candidates,
        "top_projects": [{"project": project, "messages": count} for project, count in aggregate["project_counts"].most_common(limit_projects)],
    }
    return sanitize_output(result)


def empty_aggregate() -> dict[str, Any]:
    return {
        "sources": {},
        "totals": collections.Counter(),
        "category_counts": collections.Counter(),
        "category_sessions": collections.defaultdict(set),
        "category_projects": collections.defaultdict(set),
        "project_counts": collections.Counter(),
        "examples": collections.defaultdict(list),
    }


def merge_aggregate(target: dict[str, Any], source: dict[str, Any]) -> None:
    target["sources"].update(source["sources"])
    target["totals"].update(source["totals"])
    target["category_counts"].update(source["category_counts"])
    target["project_counts"].update(source["project_counts"])
    for key, value in source["category_sessions"].items():
        target["category_sessions"][key].update(value)
    for key, value in source["category_projects"].items():
        target["category_projects"][key].update(value)
    for key, values in source["examples"].items():
        target["examples"][key].extend(values)


def mine_codex(home: Path, include_examples: bool) -> dict[str, Any]:
    agg = empty_aggregate()
    codex = home / ".codex"
    history_path = codex / "history.jsonl"
    index_path = codex / "session_index.jsonl"
    rollout_paths = sorted((codex / "sessions").glob("**/rollout-*.jsonl"))
    session_meta = load_codex_session_meta(rollout_paths)

    agg["sources"]["codex"] = {
        "history": str(history_path),
        "session_index": str(index_path),
        "rollout_files": len(rollout_paths),
        "session_meta": len(session_meta),
        "available": codex.exists(),
    }
    for row in iter_jsonl(history_path):
        text = str(row.get("text") or "")
        if not text.strip():
            continue
        session_id = str(row.get("session_id") or "codex-history")
        project = session_meta.get(session_id, {}).get("cwd") or "unknown"
        add_text(agg, "codex", session_id, project, text, include_examples)
        agg["totals"]["codex_history_rows"] += 1

    for row in iter_jsonl(index_path):
        title = str(row.get("thread_name") or "")
        if not title.strip():
            continue
        session_id = str(row.get("id") or "codex-thread")
        project = session_meta.get(session_id, {}).get("cwd") or "unknown"
        add_text(agg, "codex", session_id, project, title, include_examples)
        agg["totals"]["codex_thread_titles"] += 1
    return agg


def mine_claude(home: Path, include_examples: bool) -> dict[str, Any]:
    agg = empty_aggregate()
    claude = home / ".claude"
    project_files = sorted((claude / "projects").glob("**/*.jsonl"))
    task_files = sorted((claude / "tasks").glob("**/*.json"))
    agg["sources"]["claude"] = {
        "project_jsonl_files": len(project_files),
        "task_json_files": len(task_files),
        "available": claude.exists(),
    }
    for path in project_files:
        project = path.parent.name
        session_id = path.stem
        for row in iter_jsonl(path):
            if not is_user_record(row):
                continue
            for text in extract_texts(row, skip_non_human_content=True):
                add_text(agg, "claude", session_id, project, text, include_examples)
                agg["totals"]["claude_user_messages"] += 1
    for path in task_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError, RecursionError):
            agg["totals"]["claude_task_parse_errors"] += 1
            continue
        for text in extract_texts(data):
            add_text(agg, "claude", path.stem, "claude-tasks", text, include_examples)
            agg["totals"]["claude_task_texts"] += 1
    return agg


def add_text(agg: dict[str, Any], source: str, session_id: str, project: str, text: str, include_examples: bool) -> None:
    agg["totals"]["texts"] += 1
    agg["project_counts"][project] += 1
    for category in classify_categories(text):
        agg["category_counts"][category] += 1
        agg["category_sessions"][category].add(f"{source}:{session_id}")
        agg["category_projects"][category].add(project)
        if include_examples and len(agg["examples"][category]) < 3:
            agg["examples"][category].append(redact_and_truncate(text, 220))


def classify_categories(text: str) -> list[str]:
    return [name for name, regex in COMPILED_CATEGORIES if regex.search(text)]


def rank_candidates(
    counts: collections.Counter[str],
    sessions: dict[str, set[str]],
    projects: dict[str, set[str]],
) -> list[dict[str, Any]]:
    candidates = []
    for spec in CANDIDATE_SPECS:
        evidence = []
        score = 0
        session_ids: set[str] = set()
        project_ids: set[str] = set()
        for category in spec["categories"]:
            category_count = counts.get(category, 0)
            if category_count:
                evidence.append(
                    {
                        "category": category,
                        "messages": category_count,
                        "sessions": len(sessions[category]),
                        "projects": len(projects[category]),
                    }
                )
                score += category_count
                session_ids.update(sessions[category])
                project_ids.update(projects[category])
        if not evidence:
            continue
        confidence = "high" if score >= 100 and len(session_ids) >= 40 else "medium" if score >= 20 else "low"
        scope = "cross-project" if len(project_ids) > 1 else "project-specific"
        if scope == "project-specific" and confidence == "high":
            confidence = "medium"
        candidates.append(
            {
                "skill": spec["skill"],
                "action": spec["action"],
                "score": score,
                "sessions": len(session_ids),
                "projects": len(project_ids),
                "scope": scope,
                "confidence": confidence,
                "risk_level": spec["risk_level"],
                "evidence": evidence,
                "reason": spec["reason"],
            }
        )
    return sorted(candidates, key=lambda item: (item["confidence"] == "high", item["score"]), reverse=True)


def is_user_record(row: dict[str, Any]) -> bool:
    role = row.get("role")
    message = row.get("message") if isinstance(row.get("message"), dict) else {}
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    role = role or message.get("role") or payload.get("role")
    row_type = str(row.get("type") or payload.get("type") or "")
    return role == "user" or row_type in {"user", "human"} or row_type.endswith("user_message")


def extract_texts(value: Any, skip_non_human_content: bool = False) -> list[str]:
    texts: list[str] = []
    if isinstance(value, str):
        if value.strip():
            texts.append(value)
    elif isinstance(value, list):
        for item in value:
            texts.extend(extract_texts(item, skip_non_human_content))
    elif isinstance(value, dict):
        content_type = str(value.get("type") or "").lower()
        if skip_non_human_content and content_type in {"tool_result", "tool_use", "image", "document"}:
            return texts
        for key in ("text", "input_text", "content", "prompt", "summary", "thread_name"):
            if key in value:
                texts.extend(extract_texts(value[key], skip_non_human_content))
        if "message" in value:
            texts.extend(extract_texts(value["message"], skip_non_human_content))
        if "payload" in value:
            texts.extend(extract_texts(value["payload"], skip_non_human_content))
    return texts


def print_mining_text(result: dict[str, Any]) -> None:
    totals = result["totals"]
    print("Agent session pattern mining")
    print(f"home: {result['home']}")
    print(f"texts: {totals.get('texts', 0)}")
    print("")
    print("Top categories")
    for category in result["categories"][:15]:
        print(f"- {category['id']}: {category['messages']} messages, {category['sessions']} sessions")
    print("")
    print("Candidate actions")
    for candidate in result["candidates"][:10]:
        print(
            f"- {candidate['skill']} ({candidate['action']}): "
            f"score {candidate['score']}, {candidate['sessions']} sessions, {candidate['confidence']} confidence"
        )
    print("")
    print("Top projects")
    for item in result["top_projects"]:
        print(f"- {item['messages']}: {item['project']}")


if __name__ == "__main__":
    raise SystemExit(main())
