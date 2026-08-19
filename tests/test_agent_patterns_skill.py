from __future__ import annotations

import json
import importlib.util
import os
import shutil
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
        self.assertTrue(QUICK_VALIDATE.is_file(), f"skill-creator quick_validate.py not found: {QUICK_VALIDATE}")
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
            aws_canary = "AKIAIOSFODNN7EXAMPLE"
            project = home / "work" / aws_canary / "repo"
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
            self.assertNotIn(aws_canary, result.stdout)

    def test_codex_handoff_probe_with_local_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            aws_canary = "AKIAIOSFODNN7EXAMPLE"
            jwt_canary = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwcml2YXRlIn0.signaturevalue"
            project = home / "work" / aws_canary / "repo"
            project.mkdir(parents=True)
            self.write_jsonl(
                home / ".codex/history.jsonl",
                [
                    {
                        "session_id": "codex-1",
                        "text": "continue and run pytest before publish",
                        "ts": jwt_canary,
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
            self.assertNotIn(aws_canary, result.stdout)
            self.assertNotIn(jwt_canary, result.stdout)

    def test_secret_redaction_covers_structured_and_text_corpus(self) -> None:
        secrets = {
            "api": "top-level-api-secret-value",
            "nested": "nested-password-secret-value",
            "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwcml2YXRlIn0.signaturevalue",
            "aws": "AKIAIOSFODNN7EXAMPLE",
            "aws_secret": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "cookie": "session-cookie-private-value",
            "url_user": "database-user-private",
            "url_password": "database-password-private",
            "pem_body": "MIIEvQIBADANBgkqhkiG9w0BAQEFAASC",
            "github_pat": "github_pat_11AAABBBCCCDDDEEEFFF111222333",
            "gitlab_pat": "glpat-abcdefghijklmnopqrstuvwxyz123456",
            "slack_token": "xox" + "b-123456789012-abcdefghijklmnopqrstuvwxyz",
        }
        text = json.dumps(
            {
                "api_key": secrets["api"],
                "nested": {"password": secrets["nested"]},
                "headers": {"Authorization": f"Bearer {secrets['jwt']}"},
                "aws": secrets["aws"],
            }
        )
        text += (
            f"\nDATABASE_URL=postgresql://{secrets['url_user']}:{secrets['url_password']}@db.example/app"
            f"\nAWS_SECRET_ACCESS_KEY={secrets['aws_secret']}"
            f"\nCookie: session={secrets['cookie']}; HttpOnly"
            f"\n-----BEGIN PRIVATE KEY-----\n{secrets['pem_body']}\n-----END PRIVATE KEY-----"
            f"\nGitHub={secrets['github_pat']} GitLab={secrets['gitlab_pat']} Slack={secrets['slack_token']}"
        )

        modules = [
            self.load_module("agent_patterns_session_log_utils", ROOT / "skills/agent-patterns/scripts/session_log_utils.py"),
            self.load_module(
                "handoff_redaction_session_log_utils",
                ROOT / "skills/context-handoff-pack/scripts/session_log_utils.py",
            ),
            self.load_module(
                "miner_session_log_utils",
                ROOT / "skills/agent-session-pattern-miner/scripts/session_log_utils.py",
            ),
        ]
        redacted_outputs = []
        sanitized_outputs = []
        for utils in modules:
            with self.subTest(module=utils.__name__):
                redacted = utils.redact_secret_like_values(text)
                redacted_outputs.append(redacted)
                for secret in secrets.values():
                    self.assertNotIn(secret, redacted)
                self.assertGreaterEqual(redacted.count("[REDACTED]"), 4)
                self.assertEqual(utils.redact_secret_like_values(redacted), redacted)

                output = utils.sanitize_output(
                    {
                        "session_id": f"session-{secrets['jwt']}",
                        "cwd": f"/workspace/{secrets['aws']}/repo",
                        "rollout": f"postgresql://{secrets['url_user']}:{secrets['url_password']}@db.example/app",
                        "timestamp": "sk-abcdefghijklmnopqrstuvwx",
                        "home": f"-----BEGIN PRIVATE KEY-----\n{secrets['pem_body']}\n-----END PRIVATE KEY-----",
                        "source": {"Cookie": f"session={secrets['cookie']}"},
                        "top_projects": [{"project": f"AWS_SECRET_ACCESS_KEY={secrets['aws_secret']}"}],
                        "credentials": {
                            "AWS_SECRET_ACCESS_KEY": secrets["aws_secret"],
                            "databaseUrl": f"postgresql://{secrets['url_user']}:{secrets['url_password']}@db.example/app",
                            "privateKey": secrets["pem_body"],
                            "setCookie": secrets["cookie"],
                        },
                    }
                )
                output_json = json.dumps(output)
                sanitized_outputs.append(output_json)
                for secret in secrets.values():
                    self.assertNotIn(secret, output_json)
        self.assertEqual(len(set(redacted_outputs)), 1)
        self.assertEqual(len(set(sanitized_outputs)), 1)

        structured = modules[0].redact_structured_secrets(
            {
                "apiKey": secrets["api"],
                "nested": [{"refresh-token": secrets["nested"]}],
                "message": f"Authorization: Bearer {secrets['jwt']} AWS={secrets['aws']}",
            }
        )
        serialised = json.dumps(structured)
        for secret in secrets.values():
            self.assertNotIn(secret, serialised)

    def test_redaction_happens_before_excerpt_truncation(self) -> None:
        utils = self.load_module(
            "handoff_session_log_utils",
            ROOT / "skills/context-handoff-pack/scripts/session_log_utils.py",
        )
        secret = "sk-" + "a" * 80
        text = "x" * 215 + f" api_key={secret} trailing"
        excerpt = utils.redact_and_truncate(text, 240)
        self.assertNotIn(secret, excerpt)
        self.assertNotIn("sk-", excerpt)
        self.assertIn("[REDACTED]", excerpt)

    def test_handoff_probe_excludes_unknown_and_other_cwd_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "work/repo"
            other = home / "work/other"
            child = project / "nested"
            project.mkdir(parents=True)
            other.mkdir(parents=True)
            child.mkdir(parents=True)
            (project / ".git").mkdir()
            (other / ".git").mkdir()
            self.write_jsonl(
                home / ".codex/history.jsonl",
                [
                    {"session_id": "known", "text": "known project marker", "ts": 1},
                    {"session_id": "unknown", "text": "unknown private marker", "ts": 2},
                    {"session_id": "other", "text": "other private marker", "ts": 3},
                    {"session_id": "parent", "text": "parent workspace private marker", "ts": 4},
                    {"session_id": "child", "text": "child project marker", "ts": 5},
                ],
            )
            self.write_jsonl(
                home / ".codex/sessions/rollout-known.jsonl",
                [{"type": "session_meta", "payload": {"id": "known", "cwd": str(project)}}],
            )
            self.write_jsonl(
                home / ".codex/sessions/rollout-other.jsonl",
                [{"type": "session_meta", "payload": {"id": "other", "cwd": str(other)}}],
            )
            self.write_jsonl(
                home / ".codex/sessions/rollout-parent.jsonl",
                [{"type": "session_meta", "payload": {"id": "parent", "cwd": str(project.parent)}}],
            )
            self.write_jsonl(
                home / ".codex/sessions/rollout-child.jsonl",
                [{"type": "session_meta", "payload": {"id": "child", "cwd": str(child)}}],
            )

            scoped = self.run_cmd(
                sys.executable,
                "skills/context-handoff-pack/scripts/codex_handoff_probe.py",
                "--home",
                str(home),
                "--cwd",
                str(project),
                "--include-text",
                "--format",
                "json",
            )
            self.assertEqual(scoped.returncode, 0, scoped.stderr)
            self.assertEqual(
                {row["session_id"] for row in json.loads(scoped.stdout)["sessions"]},
                {"known", "child"},
            )
            self.assertNotIn("unknown private marker", scoped.stdout)
            self.assertNotIn("other private marker", scoped.stdout)
            self.assertNotIn("parent workspace private marker", scoped.stdout)

            explicit = self.run_cmd(
                sys.executable,
                "skills/context-handoff-pack/scripts/codex_handoff_probe.py",
                "--home",
                str(home),
                "--cwd",
                str(project),
                "--session-id",
                "unknown",
                "--include-text",
                "--format",
                "json",
            )
            self.assertEqual(explicit.returncode, 0, explicit.stderr)
            self.assertEqual(json.loads(explicit.stdout)["sessions"][0]["session_id"], "unknown")

            cross_repository = self.run_cmd(
                sys.executable,
                "skills/context-handoff-pack/scripts/codex_handoff_probe.py",
                "--home",
                str(home),
                "--cwd",
                str(project),
                "--session-id",
                "other",
                "--include-text",
                "--format",
                "json",
            )
            self.assertEqual(cross_repository.returncode, 0, cross_repository.stderr)
            self.assertEqual(json.loads(cross_repository.stdout)["matching_sessions"], 0)
            self.assertNotIn("other private marker", cross_repository.stdout)

    def test_jsonl_readers_tolerate_malformed_scalars_arrays_and_null(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "work/repo"
            project.mkdir(parents=True)
            prefix = 'null\n[]\n"scalar"\n{malformed\n{"huge":' + "9" * 5000 + "}\n"
            history = home / ".codex/history.jsonl"
            history.parent.mkdir(parents=True, exist_ok=True)
            history.write_text(
                prefix + json.dumps({"session_id": "valid", "text": "continue pytest", "ts": ["odd"]}) + "\n",
                encoding="utf-8",
            )
            rollout = home / ".codex/sessions/rollout-valid.jsonl"
            rollout.parent.mkdir(parents=True, exist_ok=True)
            rollout.write_text(
                prefix
                + json.dumps({"type": "session_meta", "payload": []})
                + "\n"
                + json.dumps({"type": "session_meta", "payload": {"id": "valid", "cwd": str(project)}})
                + "\n",
                encoding="utf-8",
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
            self.assertEqual(json.loads(result.stdout)["matching_sessions"], 1)

    def test_claude_tool_results_are_not_mined_as_human_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.write_jsonl(
                home / ".claude/projects/example/session.jsonl",
                [
                    {
                        "type": "user",
                        "message": {
                            "role": "user",
                            "content": [
                                {"type": "tool_result", "content": "publish secret tool output"}
                            ],
                        },
                    },
                    {
                        "type": "user",
                        "message": {
                            "role": "user",
                            "content": [{"type": "text", "text": "review this PR"}],
                        },
                    },
                ],
            )
            result = self.run_cmd(
                sys.executable,
                "skills/agent-session-pattern-miner/scripts/mine_agent_sessions.py",
                "--home",
                str(home),
                "--source",
                "claude",
                "--include-examples",
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("secret tool output", result.stdout)
            self.assertEqual(json.loads(result.stdout)["totals"]["claude_user_messages"], 1)

    def test_single_project_evidence_is_not_high_confidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "work/one-repo"
            project.mkdir(parents=True)
            self.write_jsonl(
                home / ".codex/history.jsonl",
                [
                    {
                        "session_id": f"session-{index}",
                        "text": "continue context and turn this into a skill",
                    }
                    for index in range(60)
                ],
            )
            for index in range(60):
                self.write_jsonl(
                    home / f".codex/sessions/rollout-session-{index}.jsonl",
                    [
                        {
                            "type": "session_meta",
                            "payload": {"id": f"session-{index}", "cwd": str(project)},
                        }
                    ],
                )
            result = self.run_cmd(
                sys.executable,
                "skills/agent-session-pattern-miner/scripts/mine_agent_sessions.py",
                "--home",
                str(home),
                "--source",
                "codex",
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            candidates = json.loads(result.stdout)["candidates"]
            candidate = next(item for item in candidates if item["skill"] == "agent-session-pattern-miner")
            self.assertEqual(candidate["scope"], "project-specific")
            self.assertEqual(candidate["confidence"], "medium")

    def test_runnable_skills_work_when_copied_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            for skill_name, script_name in (
                ("context-handoff-pack", "codex_handoff_probe.py"),
                ("agent-session-pattern-miner", "mine_agent_sessions.py"),
            ):
                copied = destination / skill_name
                shutil.copytree(ROOT / "skills" / skill_name, copied)
                with self.subTest(skill=skill_name):
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(copied / "scripts" / script_name),
                            "--home",
                            str(destination / "empty-home"),
                            "--format",
                            "json",
                        ],
                        cwd=destination,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIsInstance(json.loads(result.stdout), dict)

    def load_module(self, name: str, path: Path):
        spec = importlib.util.spec_from_file_location(name, path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def write_jsonl(self, path: Path, rows: list[object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
