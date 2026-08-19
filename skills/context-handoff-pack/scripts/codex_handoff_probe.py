#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

from session_log_utils import (
    iter_jsonl,
    load_codex_session_meta,
    redact_and_truncate,
    same_repository_scope,
    sanitize_output,
    utc_iso_from_timestamp,
)


SIGNALS = [
    ("verification", r"pytest|unittest|cargo test|cargo check|go test|go build|tsc --noEmit|pnpm test|npm test|验证|测试"),
    ("blocker", r"blocked|blocker|failed|failure|error|exception|报错|失败|卡住|不行"),
    ("publish", r"publish|release|push|tag|GitHub public repo|发布|推送"),
    ("runtime", r"localhost|127\.0\.0\.1|port|dev server|login|端口|启动|服务|浏览器"),
    ("handoff", r"handoff|compaction|resume|continue|继续|刚才|上下文|恢复"),
    ("github", r"GitHub|\bgh\s+|pull request|PR\s*#|issue"),
    ("skill", r"skill|SKILL\.md|Agent Patterns|沉淀"),
]
COMPILED_SIGNALS = [(name, re.compile(pattern, re.IGNORECASE | re.DOTALL)) for name, pattern in SIGNALS]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Probe local Codex records for context handoff evidence.")
    parser.add_argument("--home", default=str(Path.home()), help="Home directory containing .codex")
    parser.add_argument("--cwd", default=str(Path.cwd()), help="Workspace cwd to match against Codex session metadata")
    parser.add_argument("--session-id", help="Limit to one Codex session id")
    parser.add_argument("--limit", type=int, default=8, help="Recent sessions to show")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--include-text", action="store_true", help="Include short redacted user text excerpts")
    args = parser.parse_args(argv)

    result = probe(Path(args.home).expanduser(), args.cwd, args.session_id, args.limit, args.include_text)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print_probe_text(result)
    return 0


def probe(home: Path, cwd: str, session_id: str | None, limit: int, include_text: bool) -> dict[str, Any]:
    codex = home / ".codex"
    history_path = codex / "history.jsonl"
    index_path = codex / "session_index.jsonl"
    rollout_paths = sorted((codex / "sessions").glob("**/rollout-*.jsonl"))
    meta = load_codex_session_meta(rollout_paths)
    titles = load_titles(index_path)
    events: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)

    for row in iter_jsonl(history_path):
        sid = str(row.get("session_id") or "")
        if not sid:
            continue
        if session_id and sid != session_id:
            continue
        session_cwd = meta.get(sid, {}).get("cwd", "")
        if not session_id and (not cwd or not session_cwd):
            continue
        if cwd and session_cwd and not same_repository_scope(session_cwd, cwd):
            continue
        text = str(row.get("text") or "")
        if not text.strip():
            continue
        events[sid].append(
            {
                "ts": row.get("ts") or row.get("timestamp") or "",
                "signals": classify_probe_signals(text),
                "text": redact_and_truncate(text, 240) if include_text else None,
            }
        )

    sessions = []
    for sid, rows in events.items():
        signal_counts = collections.Counter(signal for row in rows for signal in row["signals"])
        meta_row = meta.get(sid, {})
        title = titles.get(sid)
        sessions.append(
            {
                "session_id": sid,
                "cwd": meta_row.get("cwd", ""),
                "rollout": meta_row.get("path", ""),
                "updated_at": latest_probe_ts(rows) or meta_row.get("timestamp", ""),
                "history_rows": len(rows),
                "signals": dict(signal_counts.most_common()),
                "thread_title": redact_and_truncate(title, 240) if include_text and title else None,
                "recent": rows[-3:] if include_text else [],
            }
        )

    sessions.sort(key=lambda item: str(item.get("updated_at") or ""), reverse=True)
    result = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "cwd": cwd,
        "codex_home": str(codex),
        "sources": {
            "history": str(history_path),
            "session_index": str(index_path),
            "rollout_files": len(rollout_paths),
            "session_meta": len(meta),
        },
        "matching_sessions": len(sessions),
        "sessions": sessions[:limit],
    }
    return sanitize_output(result)


def load_titles(path: Path) -> dict[str, str]:
    titles: dict[str, str] = {}
    for row in iter_jsonl(path):
        sid = str(row.get("id") or "")
        title = str(row.get("thread_name") or "")
        if sid and title:
            titles[sid] = title
    return titles


def classify_probe_signals(text: str) -> list[str]:
    return [name for name, regex in COMPILED_SIGNALS if regex.search(text)]


def latest_probe_ts(rows: list[dict[str, Any]]) -> str:
    values = [row.get("ts") for row in rows if row.get("ts") is not None and row.get("ts") != ""]
    if not values:
        return ""
    return utc_iso_from_timestamp(values[-1])


def print_probe_text(result: dict[str, Any]) -> None:
    print("Codex handoff probe")
    print(f"cwd: {result['cwd']}")
    print(f"matching_sessions: {result['matching_sessions']}")
    print(f"rollout_files: {result['sources']['rollout_files']}")
    for session in result["sessions"]:
        signals = ", ".join(f"{key}:{value}" for key, value in session["signals"].items()) or "none"
        print("")
        print(f"- session: {session['session_id']}")
        print(f"  cwd: {session['cwd'] or 'unknown'}")
        print(f"  updated_at: {session['updated_at'] or 'unknown'}")
        print(f"  history_rows: {session['history_rows']}")
        print(f"  signals: {signals}")
        if session.get("rollout"):
            print(f"  rollout: {session['rollout']}")
        if session.get("thread_title"):
            print(f"  title: {session['thread_title']}")
        for row in session.get("recent", []):
            print(f"  recent: {row.get('text')}")


if __name__ == "__main__":
    raise SystemExit(main())
