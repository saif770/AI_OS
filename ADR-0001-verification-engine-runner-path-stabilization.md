# ADR-0001: Stabilize Verification Engine Runner Path in Iteration 1

- **Status:** Accepted
- **Date:** 2026-07-02

## Title
Stabilize Verification Engine runner import path and delegate pytest execution through ToolRunner.

## Decision
Update `VerificationEngine` to import `TestRunner` from `core.verification_engine.pytest_runner`, and refactor `pytest_runner.TestRunner` to delegate command execution to `ToolRunner` instead of calling `subprocess.run()` directly.

## Alternatives
1. Keep direct subprocess logic in `pytest_runner` and only fix the import mismatch.
2. Reintroduce a separate `test_runner.py` production module to match the stale import.
3. Delay the import fix until all verification subprocess refactors are ready.

## Consequences
- Removes one duplicated subprocess implementation from Verification Engine.
- Stabilizes the runner path used by `VerificationEngine`.
- Preserves the current public API.
- Leaves remaining verification step consolidation to later frozen iterations.
- Keeps a known MCP caller/callee inconsistency recorded as debt until test-package drift is cleaned.
