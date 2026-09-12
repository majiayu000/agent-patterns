from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable


REDACTED = "[REDACTED]"
SECRET_KEY_NAMES = {
    "access_token",
    "accesstoken",
    "api_key",
    "apikey",
    "authorization",
    "auth_token",
    "authtoken",
    "aws_secret_access_key",
    "awssecretaccesskey",
    "client_secret",
    "clientsecret",
    "cookie",
    "database_url",
    "databaseurl",
    "password",
    "private_key",
    "privatekey",
    "refresh_token",
    "refreshtoken",
    "secret",
    "set_cookie",
    "setcookie",
    "token",
}
SECRET_KEY_PATTERN = re.compile(
    r"(?i)(?P<prefix>(?P<key_quote>['\"]?)"
    r"(?:access[_-]?token|api[_-]?key|apikey|authorization|auth[_-]?token|client[_-]?secret|"
    r"aws[_-]?secret[_-]?access[_-]?key|cookie|database[_-]?url|password|private[_-]?key|"
    r"refresh[_-]?token|secret|set[_-]?cookie|token)"
    r"(?P=key_quote)\s*[:=]\s*)"
    r"(?P<value>(?!\[REDACTED\])(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|[^\s,}\]]+))",
)
AUTHORIZATION_PATTERN = re.compile(
    r"(?i)(?P<prefix>['\"]?authorization['\"]?\s*[:=]\s*)"
    r"(?P<quote>['\"]?)(?:bearer|basic)\s+[A-Za-z0-9._~+/=-]{8,}(?P=quote)",
)
COOKIE_PATTERN = re.compile(
    r"(?i)(?P<prefix>['\"]?(?:cookie|set[_-]?cookie)['\"]?\s*[:=]\s*)"
    r"(?P<value>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|[^\r\n]+)",
)
URL_USERINFO_PATTERN = re.compile(
    r"(?i)(?P<scheme>\b[a-z][a-z0-9+.-]*://)(?:[^/\s]+@)",
)
PEM_PRIVATE_KEY_PATTERN = re.compile(
    r"-----BEGIN (?P<label>[A-Z0-9 ]*PRIVATE KEY)-----.*?-----END (?P=label)-----",
    re.DOTALL,
)
SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bxox[aboprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\b"),
    re.compile(r"(?i)(?<=\bbearer\s)[A-Za-z0-9._~+/=-]{8,}"),
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
                except (ValueError, RecursionError):
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
                    except (ValueError, RecursionError):
                        continue
                    if not isinstance(row, dict) or row.get("type") != "session_meta":
                        continue
                    payload = row.get("payload")
                    if not isinstance(payload, dict):
                        continue
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
    redacted = PEM_PRIVATE_KEY_PATTERN.sub(REDACTED, text)
    redacted = AUTHORIZATION_PATTERN.sub(_redact_authorization, redacted)
    redacted = COOKIE_PATTERN.sub(_redact_cookie, redacted)
    redacted = SECRET_KEY_PATTERN.sub(_redact_key_value, redacted)
    redacted = URL_USERINFO_PATTERN.sub(r"\g<scheme>[REDACTED]@", redacted)
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(REDACTED, redacted)
    return redacted


def redact_and_truncate(text: str, limit: int) -> str:
    """Redact the complete value before applying an output-size limit."""
    if limit < 0:
        raise ValueError("limit must be non-negative")
    return redact_secret_like_values(text).replace("\n", " ")[:limit]


def redact_structured_secrets(value: Any, key: str | None = None) -> Any:
    """Return a JSON-compatible copy with secret fields and tokens redacted."""
    if key is not None and _normalise_key(key) in SECRET_KEY_NAMES:
        return REDACTED
    if isinstance(value, dict):
        return {item_key: redact_structured_secrets(item_value, str(item_key)) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [redact_structured_secrets(item) for item in value]
    if isinstance(value, str):
        return redact_secret_like_values(value)
    return value


def sanitize_output(value: Any, key: str | None = None) -> Any:
    """Recursively sanitize every string and credential-bearing field before output."""
    if key is not None and _normalise_key(key) in SECRET_KEY_NAMES:
        return REDACTED
    if isinstance(value, dict):
        return {
            redact_secret_like_values(str(item_key)): sanitize_output(item_value, str(item_key))
            for item_key, item_value in value.items()
        }
    if isinstance(value, list):
        return [sanitize_output(item) for item in value]
    if isinstance(value, tuple):
        return [sanitize_output(item) for item in value]
    if isinstance(value, str):
        return redact_secret_like_values(value)
    return value


def _normalise_key(key: str) -> str:
    snake = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", key.strip().replace("-", "_"))
    snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", snake)
    return snake.lower()


def _redact_key_value(match: re.Match[str]) -> str:
    value = match.group("value")
    quote = value[0] if value[:1] in {"'", '"'} and value[-1:] == value[:1] else ""
    return f"{match.group('prefix')}{quote}{REDACTED}{quote}"


def _redact_authorization(match: re.Match[str]) -> str:
    quote = match.group("quote")
    return f"{match.group('prefix')}{quote}{REDACTED}{quote}"


def _redact_cookie(match: re.Match[str]) -> str:
    value = match.group("value")
    quote = value[0] if value[:1] in {"'", '"'} and value[-1:] == value[:1] else ""
    return f"{match.group('prefix')}{quote}{REDACTED}{quote}"


def same_repository_scope(session_cwd: str, requested_cwd: str) -> bool:
    try:
        session_path = Path(session_cwd).expanduser().resolve()
        requested_path = Path(requested_cwd).expanduser().resolve()
    except OSError:
        return session_cwd == requested_cwd
    session_root = discover_git_root(session_path)
    requested_root = discover_git_root(requested_path)
    if session_root is not None and requested_root is not None:
        return session_root == requested_root
    # When the requested cwd is outside a git work tree, require exact path
    # equality only. Prefix matching (is_relative_to) would treat every
    # descendant project session as in-scope from a parent like $HOME.
    return session_path == requested_path


def discover_git_root(path: Path) -> Path | None:
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return None
