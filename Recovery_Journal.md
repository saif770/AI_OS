# Recovery Journal

---

# Repository Stabilization — Test Collection Recovery

## Problem

The repository failed during pytest collection with
`ImportMismatchError`. Three test modules in
`tests/unit/verification_engine/` shared identical basenames with modules in
`tests/unit/execution_engine/`:

- `test_engine.py`
- `test_models.py`
- `test_report.py`

Because neither unit test subpackage contained a valid `__init__.py`
(both had a misnamed `init.py` lacking the dunder prefix), pytest fell back
to rootdir-based import mode, importing both files under the same bare
module name and raising `ImportMismatchError`.

## Root Cause

Two compounding defects:

1. **Colliding basenames**: the three verification test files had the same
   basename as their execution-engine counterparts.
2. **Invalid package markers**: `tests/unit/verification_engine/init.py` and
   `tests/unit/execution_engine/init.py` were named `init.py` instead of
   `__init__.py`, so Python did not recognize them as package markers.
   Additionally, the verification-engine `init.py` contained a stale copy of
   the production package exports (`from .engine import VerificationEngine`),
   which would fail once recognized as a package.

## Fix

Stabilization-only pass (no production code touched):

- Renamed the three colliding verification test files to unique names:
  - `test_engine.py` → `test_verification_engine.py`
  - `test_models.py` → `test_verification_models.py`
  - `test_report.py` → `test_verification_report.py`
- Renamed `init.py` → `__init__.py` in both unit test subpackages.
- Replaced the stale production-export content in the verification-engine
  `__init__.py` with a minimal package marker (matching the
  execution-engine package marker).
- Cleared stale `__pycache__` / `.pyc` artifacts.

All renames performed via `git mv` to preserve history. No imports required
updating (the test modules are not imported by name elsewhere).

## Tests

### Passed

```text
python -m compileall core tests

✅ Passed

pytest tests/unit --co -q

✅ 43 tests collected, 0 errors (ImportMismatchError resolved)

pytest tests/unit -x -vv

✅ 43 passed

pytest tests/integration -v

✅ 6 passed

pytest -v

47 passed, 2 failed (see Remaining Failures)
```

## Remaining Failures (reported, NOT fixed per task instructions)

Two failures surfaced in the full `pytest -v` run:

- `tests/integration/test_end_to_end.py::test_ai_os_end_to_end`
- `tests/integration/test_planning_engine.py::test_planning_engine_runs`

Both fail with `FileNotFoundError: [WinError 3] The system cannot find the
path specified: 'G:\\'`, raised from pytest's cache provider attempting to
write `.pytest_cache` at the G: drive root. These are environment /
infrastructure artifacts, not genuine test-logic failures: both tests
**pass** when run via `tests/integration -v` in isolation. They are
unrelated to the test-file renames and were not introduced by this
stabilization pass. Per task instructions, they are reported but not fixed.

## Files Changed

- `tests/unit/verification_engine/test_engine.py` → `test_verification_engine.py` (rename)
- `tests/unit/verification_engine/test_models.py` → `test_verification_models.py` (rename)
- `tests/unit/verification_engine/test_report.py` → `test_verification_report.py` (rename)
- `tests/unit/verification_engine/init.py` → `__init__.py` (rename + content fix)
- `tests/unit/execution_engine/init.py` → `__init__.py` (rename)

(5 stabilization files; no production code modified.)

## Confidence

High

The `ImportMismatchError` is fully resolved and pytest collection succeeds
repository-wide. No production code was touched. The two remaining failures
are pre-existing environment artifacts on the G: drive, reported per the
stop condition.

---

# Execution Engine Recovery Iteration 1 — Restore generated.py Output

## Problem

The Execution Engine integration test
(`tests/integration/test_execution_engine.py`) failed because `generated.py`
was not created at the expected location (`tmp_path / "generated.py"`).

A previous hypothesis had anchored the suspicion on `patch_applier.py`. This
iteration re-investigated the issue evidence-first, tracing the full
execution path through the knowledge graph and source code rather than
relying on that prior assumption.

## Root Cause

Evidence-based trace of the execution pipeline:

```
ExecutionEngine.execute()
  -> CodeGenerator.generate(response, filename="generated.py")
       returns GeneratedCode(filename="generated.py", source=...)   # no disk write
  -> PatchGenerator.generate(generated)
       returns CodePatch(target_file="generated.py", updated=...)   # no disk write
  -> PatchApplier.apply_many(bundle.patches)
       apply(): target = Path(patch.target_file)  # "generated.py" (RELATIVE)
               target.write_text(...)             # writes to CWD, NOT project_root
```

The fault spans the engine↔applier boundary, not the applier in isolation:

- `ReportWriter` (the sibling writer) was correctly anchored: constructed as
  `ReportWriter(self.project_root / "output")`, so its output landed at
  `tmp_path/output/execution_report.json` (test assertion passed).
- `PatchApplier` was constructed as `PatchApplier()` with **no `project_root`**.
  Its `apply()` resolved the relative `target_file` against the process
  current working directory, so `generated.py` was written to the repository
  root (CWD) instead of `tmp_path`.

Confirmation: the repository-root `generated.py` contained exactly
`print("AI_OS Execution Engine")` — the precise content the test's
`MockLLMClient` returns — proving it was a CWD-write artifact of the bug.

The unit tests for `PatchApplier` only ever exercised absolute paths
(`tmp_path / "hello.py"`), so they never caught the relative-path
regression.

## Fix

Minimal, API-preserving fix anchoring generated output to `project_root`:

- Added an optional `project_root: Path | None = None` field to `PatchApplier`.
  When set and the patch `target_file` is relative, the target is resolved
  against `project_root`; absolute targets pass through unchanged (preserving
  existing unit-test behavior).
- Wired `project_root` in `ExecutionEngine.__init__`:
  `PatchApplier(project_root=self.project_root)`.

No public API changed (additive optional field; existing `PatchApplier()`
callers and absolute-path callers behave identically).

## Tests

### Passed

```text
python -m compileall core tests

✅ Passed

pytest tests/unit/execution_engine/test_patch_applier.py \
       tests/unit/execution_engine/test_engine.py -v

✅ 4 passed

pytest tests/integration/test_execution_engine.py -x -vv

✅ 1 passed

generated.py is now created at tmp_path / "generated.py" (assertion
passes) alongside output/execution_report.json.
```

## Remaining Issues

- A stale, git-tracked `generated.py` remains at the repository root — a
  leftover artifact of the pre-fix CWD-write behavior. Not removed this
  iteration to respect the minimal-fix and file-budget constraints; tracked
  as TD-003.
- TD-001 (MCP graph inconsistency) and TD-002 (docs layout) carried forward.

## Confidence

High

The root cause was identified by tracing the actual execution path and
confirming the symptom with the on-disk artifact, rather than anchoring on
the earlier hypothesis. Although the fix touches `patch_applier.py`, the
evidence — not the prior suspicion — drove the conclusion, and the actual
fault was the missing `project_root` wiring at the engine↔applier boundary.

---

# Iteration 3 — Verification Engine ToolRunner Adoption Completion

## Problem

`SecurityScanner` and `BenchmarkRunner` each duplicated subprocess
execution logic (`subprocess.run`) instead of delegating to the shared
`ToolRunner` abstraction. This was the last remaining duplication in the
Verification Engine and the only thing blocking the Phase 1 criterion that
`subprocess.run` should appear only in `tool_runner.py`.

## Root Cause

The V1→V2 recovery left these two verification steps with their own
subprocess invocation paths, identical in shape to the steps consolidated in
Iteration 2. `SecurityScanner` additionally lacked the `module_fallback`
mechanism, causing `FileNotFoundError` when the `bandit` CLI binary was
absent from PATH even though the module was importable via `python -m`.

## Fix

- Refactored `SecurityScanner` to delegate execution through `ToolRunner`
  (`module_fallback="bandit"`).
- Refactored `BenchmarkRunner` to delegate execution through `ToolRunner`
  (`module_fallback="pytest"`).
- Injected `tool_runner: ToolRunner = field(default_factory=ToolRunner)` into
  each dataclass, mirroring the pattern established in Iterations 1 and 2.
- Removed direct `subprocess`/`time` imports from the two modules.

## Tests

### Passed

```text
python -m compileall core tests

✅ Passed

pytest tests/unit/verification_engine/test_security.py \
       tests/unit/verification_engine/test_benchmark.py -v

✅ 4 passed

pytest tests/unit/verification_engine -x -vv

✅ 20 passed

The full Verification Engine unit suite is now green end to end. The
`test_engine_run` failure that previously stopped in `security.py` is
resolved.
```

### Architecture Validation

`Get-ChildItem core\verification_engine\*.py | Select-String "subprocess.run"`
returns hits only in `tool_runner.py`, satisfying the Phase 1 checklist
criterion.

## Remaining Issues

- MCP `trace_path` caller/callee relationship remains inconsistent with
  source (carried forward as TD-001).
- Repository documentation layout inconsistency (carried forward as TD-002).
- The Execution Engine regression (`generated.py` not created) remains, as
  tracked in the Verification Engine V2 Recovery Checklist. This is out of
  Verification Engine scope and untouched this iteration.

## Confidence

High

ToolRunner adoption is now complete across all subprocess-owning
Verification Engine steps (`TestRunner`, `Linter`, `Formatter`,
`CoverageRunner`, `SecurityScanner`, `BenchmarkRunner`). The iteration
achieved its objectives within the approved recovery scope and, as a side
benefit, resolved the two previously-failing security unit tests via the
`module_fallback` mechanism.

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