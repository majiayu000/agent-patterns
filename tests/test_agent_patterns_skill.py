from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUICK_VALIDATE = Path(
    os.environ.get(
        "SKILL_CREATOR_QUICK_VALIDATE",
        str(Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills/.system/skill-creator/scripts/quick_validate.py"),
    )
)


class AgentPatternsSkillTest(unittest.TestCase):
    def run_cmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            list(args),
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_all_skill_folders_validate(self) -> None:
        if not QUICK_VALIDATE.exists():
            self.skipTest(f"skill-creator quick_validate.py not found: {QUICK_VALIDATE}")
        for skill_path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            skill = str(skill_path.parent.relative_to(ROOT))
            with self.subTest(skill=skill):
                result = self.run_cmd(sys.executable, str(QUICK_VALIDATE), skill)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_pattern_manifests_validate(self) -> None:
        result = self.run_cmd(sys.executable, "skills/agent-patterns/scripts/pattern_tool.py", "validate")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count(": valid"), 6)

    def test_pattern_search(self) -> None:
        result = self.run_cmd(sys.executable, "skills/agent-patterns/scripts/pattern_tool.py", "search", "ci failure")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("agent-pattern.ci-failure-diagnosis.v1", result.stdout)
        self.assertNotIn("agent-pattern.context-handoff-pack.v1", result.stdout)

    def test_show_manifest_points_to_source_skill(self) -> None:
        result = self.run_cmd(
            sys.executable,
            "skills/agent-patterns/scripts/pattern_tool.py",
            "show",
            "pr-review-risk-plan.v1",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"skill": "pr-review-risk-plan"', result.stdout)
        self.assertIn("source_skill:", result.stdout)

    def test_agent_session_pattern_miner_with_local_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "work/repo"
            project.mkdir(parents=True)
            self.write_jsonl(
                home / ".codex/history.jsonl",
                [
                    {
                        "session_id": "codex-1",
                        "text": "continue this repo handoff and publish GitHub public repo",
                        "ts": 1782900000,
                    },
                    {
                        "session_id": "codex-2",
                        "text": "open parallel subagents to review PR and make a skill",
                        "ts": 1782900060,
                    },
                ],
            )
            self.write_jsonl(
                home / ".codex/session_index.jsonl",
                [{"id": "codex-1", "thread_name": "repo publish handoff"}],
            )
            self.write_jsonl(
                home / ".codex/sessions/2026/07/01/rollout-codex-1.jsonl",
                [{"type": "session_meta", "payload": {"id": "codex-1", "cwd": str(project)}}],
            )
            self.write_jsonl(
                home / ".claude/projects/example/session.jsonl",
                [{"message": {"role": "user", "content": "turn repeated context resume work into SKILL.md"}}],
            )

            result = self.run_cmd(
                sys.executable,
                "skills/agent-session-pattern-miner/scripts/mine_agent_sessions.py",
                "--home",
                str(home),
                "--source",
                "both",
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            category_ids = {item["id"] for item in data["categories"]}
            candidate_ids = {item["skill"] for item in data["candidates"]}
            self.assertIn("context_resume", category_ids)
            self.assertIn("skill_creation", category_ids)
            self.assertIn("agent-session-pattern-miner", candidate_ids)
            self.assertIn("context-handoff-pack", candidate_ids)

    def test_codex_handoff_probe_with_local_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "work/repo"
            project.mkdir(parents=True)
            self.write_jsonl(
                home / ".codex/history.jsonl",
                [
                    {
                        "session_id": "codex-1",
                        "text": "continue and run pytest before publish",
                        "ts": 1782900000,
                    }
                ],
            )
            self.write_jsonl(
                home / ".codex/session_index.jsonl",
                [{"id": "codex-1", "thread_name": "private task title"}],
            )
            self.write_jsonl(
                home / ".codex/sessions/2026/07/01/rollout-codex-1.jsonl",
                [{"type": "session_meta", "payload": {"id": "codex-1", "cwd": str(project)}}],
            )

            result = self.run_cmd(
                sys.executable,
                "skills/context-handoff-pack/scripts/codex_handoff_probe.py",
                "--home",
                str(home),
                "--cwd",
                str(project),
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["matching_sessions"], 1)
            self.assertEqual(data["sessions"][0]["session_id"], "codex-1")
            self.assertIn("verification", data["sessions"][0]["signals"])
            self.assertNotIn("private task title", result.stdout)

    def write_jsonl(self, path: Path, rows: list[dict[str, object]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
