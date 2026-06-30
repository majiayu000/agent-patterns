from __future__ import annotations

import os
import subprocess
import sys
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
        for skill in (
            "skills/agent-patterns",
            "skills/pr-review-risk-plan",
            "skills/ci-failure-diagnosis",
            "skills/context-handoff-pack",
        ):
            with self.subTest(skill=skill):
                result = self.run_cmd(sys.executable, str(QUICK_VALIDATE), skill)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_pattern_manifests_validate(self) -> None:
        result = self.run_cmd(sys.executable, "skills/agent-patterns/scripts/pattern_tool.py", "validate")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count(": valid"), 3)

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


if __name__ == "__main__":
    unittest.main()
