---
name: ci-failure-diagnosis
description: Diagnose failing CI by collecting fresh check evidence, reproducing the smallest failing command locally when possible, identifying one defensible root cause, and proposing a minimal fix plan. Use when CI is red, tests differ between local and remote, or the user asks for root cause before code changes. Do not use to bypass, delete, or weaken tests.
---

# CI Failure Diagnosis

Use this skill to avoid speculative CI fixes. Fresh evidence comes before edits.

## Workflow

1. Collect fresh evidence:
   - Read current CI status, failing job names, failing commands, and relevant log excerpts.
   - Identify commit SHA/branch and changed files.
   - Do not rely on earlier passed checks as current truth.
2. Reproduce locally:
   - Run the smallest safe failing command first.
   - Keep commands focused; avoid full matrices until the failure is isolated.
   - Ask before destructive or unusually long-running operations.
3. Isolate root cause:
   - Form one hypothesis at a time.
   - Tie the failure to a specific code, config, dependency, or environment change.
   - After three failed fix attempts, stop and challenge the hypothesis.
4. Produce fix plan:
   - State root cause, evidence, minimal fix, and verification commands.
   - Preserve test integrity; fix production/config code instead of weakening assertions.

## Inputs

- Local repo path or current working directory.
- CI run URL, PR URL, failing command, or copied log excerpt.
- Expected target branch or SHA when relevant.

## Tools And Gates

- `github` or CI provider: read-only logs and check metadata.
- `git`: read-only status, diff, log, and branch commands.
- `shell`: focused reproduction commands.
- `repo_read`: inspect code and config.

Require human approval before destructive commands, force push, secret exposure, or disabling required checks.

## Failure Modes

- If CI logs are unavailable, stop and report missing remote evidence.
- If local reproduction is impossible, continue with remote evidence and mark confidence.
- If the likely fix touches tests, explain why test behavior is wrong before editing tests.

## Done When

- Root cause is specific and evidence-backed.
- Fix plan is minimal and ordered.
- Verification result is fresh from this session or explicitly marked unavailable.
