#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


META_SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = META_SKILL_ROOT.parent
MANIFEST_NAME = "pattern-manifest.json"
REQUIRED_MANIFEST_FIELDS = {
    "id",
    "skill",
    "title",
    "summary",
    "category",
    "tags",
    "maturity",
    "risk_level",
    "capabilities",
    "requires_human_gate",
    "source",
    "maintained_as",
}
FORBIDDEN_MANIFEST_FIELDS = {
    "problem",
    "compatibility",
    "inputs",
    "outputs",
    "workflow",
    "tools",
    "human_gates",
    "failure_modes",
    "evals",
    "exports",
    "provenance",
}
VALID_MATURITY = {"draft", "community", "runnable", "verified", "deprecated"}
VALID_RISK_LEVEL = {"low", "medium", "high", "critical"}
REQUIRED_SKILL_SECTIONS = ("## Workflow", "## Failure Modes", "## Done When")


class PatternToolError(ValueError):
    pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pattern_tool.py")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List skill-first pattern manifests")

    search_parser = subparsers.add_parser("search", help="Search skill-first pattern manifests")
    search_parser.add_argument("query")

    subparsers.add_parser("validate", help="Validate manifests and their source skills")

    show_parser = subparsers.add_parser("show", help="Show a pattern manifest and source skill path")
    show_parser.add_argument("pattern_id")

    args = parser.parse_args(argv)

    try:
        if args.command == "list":
            return list_patterns()
        if args.command == "search":
            return search_patterns(args.query)
        if args.command == "validate":
            return validate_patterns()
        if args.command == "show":
            return show_pattern(args.pattern_id)
    except PatternToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2


def load_patterns() -> list[dict[str, Any]]:
    manifests = sorted(SKILLS_ROOT.glob(f"*/references/{MANIFEST_NAME}"))
    patterns: list[dict[str, Any]] = []
    for path in manifests:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise PatternToolError(f"{path}: invalid JSON: {exc}") from exc
        if not isinstance(data, dict):
            raise PatternToolError(f"{path}: root must be an object")
        skill_dir = path.parents[1]
        data["_manifest_path"] = str(path)
        data["_skill_dir"] = str(skill_dir)
        data["_skill_path"] = str(skill_dir / "SKILL.md")
        patterns.append(data)
    if not patterns:
        raise PatternToolError(f"no {MANIFEST_NAME} files found under {SKILLS_ROOT}")
    return patterns


def list_patterns() -> int:
    for pattern in load_patterns():
        print(f"{pattern['id']}\t{pattern['maturity']}\t{pattern['skill']}\t{pattern['title']}")
    return 0


def search_patterns(query: str) -> int:
    terms = [term.lower() for term in query.split() if term.strip()]
    if not terms:
        raise PatternToolError("search query must not be empty")
    for pattern in load_patterns():
        skill_description = read_skill_description(Path(pattern["_skill_path"]))
        haystack = " ".join(
            [
                pattern.get("id", ""),
                pattern.get("skill", ""),
                pattern.get("title", ""),
                pattern.get("summary", ""),
                pattern.get("category", ""),
                skill_description,
                " ".join(pattern.get("tags", [])),
                " ".join(pattern.get("capabilities", [])),
            ]
        ).lower()
        if all(term in haystack for term in terms):
            print(f"{pattern['id']}\t{pattern['skill']}\t{pattern['summary']}")
    return 0


def validate_patterns() -> int:
    failed = False
    for pattern in load_patterns():
        errors = validate_pattern(pattern)
        path = pattern.get("_manifest_path", pattern.get("id", "<unknown>"))
        if errors:
            failed = True
            print(f"{path}: invalid", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"{path}: valid")
    return 1 if failed else 0


def show_pattern(pattern_id: str) -> int:
    pattern = find_pattern(pattern_id)
    errors = validate_pattern(pattern)
    if errors:
        raise PatternToolError("cannot show invalid pattern: " + "; ".join(errors))
    public = {key: value for key, value in pattern.items() if not key.startswith("_")}
    print(json.dumps(public, indent=2, ensure_ascii=False))
    print(f"source_skill: {pattern['_skill_path']}")
    return 0


def find_pattern(pattern_id: str) -> dict[str, Any]:
    full_id = pattern_id if pattern_id.startswith("agent-pattern.") else f"agent-pattern.{pattern_id}"
    for pattern in load_patterns():
        if pattern["id"] in {pattern_id, full_id} or pattern["id"].removeprefix("agent-pattern.") == pattern_id:
            return pattern
    raise PatternToolError(f"pattern not found: {pattern_id}")


def validate_pattern(pattern: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    manifest_keys = {key for key in pattern if not key.startswith("_")}
    for field in sorted(REQUIRED_MANIFEST_FIELDS - manifest_keys):
        errors.append(f"missing required manifest field: {field}")
    for field in sorted(FORBIDDEN_MANIFEST_FIELDS & manifest_keys):
        errors.append(f"manifest must not duplicate SKILL.md workflow field: {field}")

    if not str(pattern.get("id", "")).startswith("agent-pattern."):
        errors.append("id must start with agent-pattern.")
    if pattern.get("maturity") not in VALID_MATURITY:
        errors.append(f"maturity must be one of {sorted(VALID_MATURITY)}")
    if pattern.get("risk_level") not in VALID_RISK_LEVEL:
        errors.append(f"risk_level must be one of {sorted(VALID_RISK_LEVEL)}")
    if pattern.get("source") != "SKILL.md":
        errors.append("source must be SKILL.md")
    if pattern.get("maintained_as") != "skill-first":
        errors.append("maintained_as must be skill-first")
    if pattern.get("risk_level") in {"high", "critical"} and pattern.get("requires_human_gate") is not True:
        errors.append("high and critical risk manifests must require a human gate")

    skill_dir = Path(pattern.get("_skill_dir", ""))
    skill_path = Path(pattern.get("_skill_path", ""))
    if pattern.get("skill") != skill_dir.name:
        errors.append(f"skill field must match folder name: {skill_dir.name}")
    errors.extend(validate_source_skill(skill_path, str(pattern.get("skill", ""))))
    return errors


def validate_source_skill(skill_path: Path, expected_name: str) -> list[str]:
    errors: list[str] = []
    if not skill_path.exists():
        return [f"missing source skill: {skill_path}"]
    text = skill_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    if frontmatter.get("name") != expected_name:
        errors.append(f"SKILL.md name must be {expected_name}")
    if not frontmatter.get("description"):
        errors.append("SKILL.md description must not be empty")
    for section in REQUIRED_SKILL_SECTIONS:
        if section not in text:
            errors.append(f"SKILL.md missing required section: {section}")
    return errors


def read_skill_description(skill_path: Path) -> str:
    if not skill_path.exists():
        return ""
    return parse_frontmatter(skill_path.read_text(encoding="utf-8")).get("description", "")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


if __name__ == "__main__":
    raise SystemExit(main())
