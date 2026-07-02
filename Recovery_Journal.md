# Recovery Journal

---

# Iteration 2 — Verification Engine Tool Execution Consolidation

## Problem

`Linter`, `Formatter`, and `CoverageRunner` each duplicated subprocess
execution logic (`subprocess.run`) instead of delegating to the shared
`ToolRunner` abstraction adopted in Iteration 1.

## Root Cause

The V1→V2 recovery left these three verification steps with their own
subprocess invocation paths, creating duplicated execution logic and
architectural drift. The steps also lacked the `module_fallback` mechanism,
causing `FileNotFoundError` when the tool CLI binary (e.g. `ruff`, `black`)
was absent even when the module was importable via `python -m`.

## Fix

- Refactored `Linter` to delegate execution through `ToolRunner`
  (`module_fallback="ruff"`).
- Refactored `Formatter` to delegate execution through `ToolRunner`
  (`module_fallback="black"`).
- Refactored `CoverageRunner` to delegate execution through `ToolRunner`
  (`module_fallback="pytest"`).
- Injected `tool_runner: ToolRunner = field(default_factory=ToolRunner)` into
  each dataclass, mirroring the `TestRunner` pattern established in Iteration 1.
- Removed direct `subprocess`/`time` imports from the three modules.

## Tests

### Passed

```text
python -m compileall core tests

✅ Passed

pytest tests/unit/verification_engine/test_linter.py \
       tests/unit/verification_engine/test_formatter.py \
       tests/unit/verification_engine/test_coverage.py -v

✅ 6 passed

pytest tests/unit/verification_engine -x -vv

Forward progress: the engine suite now advances past linter, formatter, and
coverage (previously blocked in linter.py) and fails later in security.py,
which is explicitly out of scope for Iteration 2.
```

## Remaining Issues

- `security.py` still owns subprocess execution (deferred — out of scope).
- `benchmark.py` still owns subprocess execution (deferred — out of scope).
- MCP `trace_path` caller/callee relationship remains inconsistent with source
  (carried forward as TD-001).
- Repository documentation layout inconsistency (carried forward as TD-002).

## Confidence

High

The iteration achieved its objectives within the approved recovery scope,
following the exact delegation pattern established in Iteration 1. As a side
benefit, the `module_fallback` mechanism resolved four previously-failing
unit tests that depended on CLI binaries not present on PATH.

---

# Iteration 1 — Verification Engine Runner Path Stabilization

## Problem

`VerificationEngine` imported `.test_runner`, while the actual production
runner implementation existed in `pytest_runner.py`.

Additionally, `pytest_runner.TestRunner` duplicated subprocess execution
instead of delegating to the shared `ToolRunner`.

---

## Root Cause

Partial V1→V2 recovery left:

- stale production module imports
- incomplete ToolRunner adoption
- duplicated subprocess execution logic

---

## Fix

- Updated `VerificationEngine` to import `TestRunner` from `pytest_runner`.
- Refactored `pytest_runner.TestRunner` to delegate execution through
  `ToolRunner`.
- Replaced the incorrect production-like content in
  `tests/unit/verification_engine/test_runner.py`
  with a proper unit test validating delegation behavior.

---

## Tests

### Passed

```text
pytest tests/unit/verification_engine/test_runner.py -x -vv

✅ Passed

python -m compileall core tests

✅ Passed

Progress
pytest tests/unit/verification_engine/test_engine.py -x -vv

Import mismatch resolved.

Current failure now occurs later in linter.py, which is expected because
Iteration 2 has not yet consolidated the remaining subprocess execution.

This represents forward progress rather than a regression.

Commit

fad1526

Refactor: stabilize Verification Engine runner path

Remaining Issues
linter.py still owns subprocess execution.
formatter.py still owns subprocess execution.
coverage.py still owns subprocess execution.
security.py still owns subprocess execution.
benchmark.py still owns subprocess execution.
MCP trace_path caller/callee relationship remains inconsistent with source.
Repository documentation layout is inconsistent (docs exists as a file
rather than a directory). This is intentionally deferred because it is
outside the Verification Engine recovery scope.
Confidence

High

The iteration successfully achieved its objectives while remaining within the
approved recovery scope.

Technical Debt Register
TD-001 — MCP Graph Inconsistency
Severity

Medium

Root Cause

Stale or polluted graph relationships, likely influenced by verification
test-package drift.

Location

Codebase Memory MCP trace for

core.verification_engine.engine.VerificationEngine.run

Impact

Caller/callee relationships cannot yet be considered fully authoritative
without validating against the source code.

Recommended Fix

Complete verification test-package cleanup.

Re-index the repository.

Validate architecture again.

Estimated Effort

Small to Medium

Dependencies

Verification test cleanup

Repository re-index

TD-002 — Repository Documentation Layout
Severity

Medium

Root Cause

Repository structure drift.

The repository currently contains a file named docs where a documentation
directory would normally exist.

Impact

Prevents storing ADRs and future project documentation under a standard
documentation directory structure.

Recommended Fix

Convert docs into a directory during a dedicated repository cleanup slice
after Verification Engine recovery is complete.

Estimated Effort

Small

Dependencies

Review references to the existing docs file before conversion.