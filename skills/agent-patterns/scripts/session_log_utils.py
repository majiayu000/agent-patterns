from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Iterable


SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*\S+"),
]


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.exists():
        return
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(row, dict):
                    yield row
    except OSError:
        return


def load_codex_session_meta(paths: Iterable[Path], max_header_lines: int = 80) -> dict[str, dict[str, str]]:
    meta: dict[str, dict[str, str]] = {}
    for path in paths:
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                for _, line in zip(range(max_header_lines), handle):
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if row.get("type") != "session_meta":
                        continue
                    payload = row.get("payload") or {}
                    session_id = str(payload.get("id") or "")
                    if session_id:
                        meta[session_id] = {
                            "cwd": str(payload.get("cwd") or ""),
                            "timestamp": str(row.get("timestamp") or ""),
                            "path": str(path),
                        }
                    break
        except OSError:
            continue
    return meta


def redact_secret_like_values(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def same_or_nested_path(first: str, second: str) -> bool:
    try:
        first_path = Path(first).resolve()
        second_path = Path(second).resolve()
    except OSError:
        return first == second
    return first_path == second_path or second_path.is_relative_to(first_path) or first_path.is_relative_to(second_path)


def utc_iso_from_timestamp(value: Any) -> str:
    if value in {None, ""}:
        return ""
    if isinstance(value, (int, float)):
        timestamp = value / 1000 if value > 10_000_000_000 else value
        try:
            return dt.datetime.fromtimestamp(timestamp, dt.timezone.utc).isoformat()
        except (OSError, OverflowError, ValueError):
            return str(value)
    return str(value)
