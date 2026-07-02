# Recovery Journal

## Iteration 1 — Verification Engine runner path stabilization
- **Problem:** `VerificationEngine` imported `.test_runner`, but the actual production runner module is `pytest_runner.py`. `pytest_runner.TestRunner` also duplicated subprocess execution instead of using `ToolRunner`.
- **Root Cause:** Partial V1→V2 refactor left stale module imports and incomplete adoption of the shared execution abstraction.
- **Fix:** Updated the engine import to `pytest_runner` and refactored `pytest_runner.TestRunner` to delegate command execution to `ToolRunner`.
- **Tests:**
  - `pytest tests/unit/verification_engine/test_runner.py -x -vv` ✅
  - `pytest tests/unit/verification_engine/test_engine.py -x -vv` ⚠️ import mismatch resolved; test now fails later in `linter.py` because Iteration 2 subprocess consolidation is not yet done.
  - `python -m compileall core tests` ✅
- **Commit:** Pending
- **Remaining Issues:**
  - `linter.py` still calls `subprocess.run()` directly and fails in `VerificationEngine.run()` test flow on this machine.
  - MCP `trace_path` caller/callee relationship for verification runner remains inconsistent with source.
  - Root `docs` path is a file, not a directory, so ADRs cannot yet be stored under a docs tree without separate cleanup.
- **Confidence:** High for Iteration 1 scope.

## Technical Debt Register
### TD-001 — MCP graph inconsistency for verification runner relationships
- **Severity:** Medium
- **Root Cause:** Stale or polluted graph relationships, likely influenced by verification test-package drift.
- **Location:** Codebase Memory MCP trace for `core.verification_engine.engine.VerificationEngine.run`
- **Impact:** MCP caller/callee traces are not fully trustworthy for this slice unless validated against source.
- **Recommended Fix:** Clean verification test-package drift and reindex after the next structural iteration.
- **Estimated Effort:** Small to Medium
- **Dependencies:** Verification test cleanup and MCP reindex

### TD-002 — Root `docs` path is a file, not a directory
- **Severity:** Medium
- **Root Cause:** Repository structure drift
- **Location:** `docs`
- **Impact:** Blocks normal ADR/documentation directory structure
- **Recommended Fix:** Convert `docs` into a directory in a dedicated recovery slice if approved
- **Estimated Effort:** Small
- **Dependencies:** Review for references to the current `docs` file
