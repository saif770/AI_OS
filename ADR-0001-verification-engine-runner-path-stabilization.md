# ADR-0001: Stabilize Verification Engine Runner Path in Iteration 1

- **Status:** Accepted
- **Date:** 2026-07-02

---

## Title

Stabilize Verification Engine runner import path and delegate pytest execution through ToolRunner.

---

## Context

Verification Engine V2 recovery introduced **ToolRunner** as the intended shared
execution abstraction for all external verification tools.

However, the implementation was only partially completed.

The repository still contained:

- `VerificationEngine` importing a non-existent production module (`test_runner.py`)
  while the actual implementation existed in `pytest_runner.py`.
- `pytest_runner.TestRunner` executing commands directly through
  `subprocess.run()` instead of delegating to the shared `ToolRunner`.
- A partially completed V1→V2 migration that left duplicated execution logic
  and architectural drift.

The objective of this iteration was to stabilize the runner path and begin
adopting the shared execution abstraction without changing public APIs or
expanding beyond the Verification Engine recovery scope.

---

## Decision

Update `VerificationEngine` to import `TestRunner` from
`core.verification_engine.pytest_runner`, and refactor
`pytest_runner.TestRunner` to delegate command execution to `ToolRunner`
instead of calling `subprocess.run()` directly.

---

## Alternatives Considered

### Option 1

Keep direct subprocess logic in `pytest_runner` and only fix the import mismatch.

**Rejected**

Would preserve duplicated execution logic and delay the intended V2 architecture.

---

### Option 2

Reintroduce a production `test_runner.py` module to satisfy the stale import.

**Rejected**

Would recreate legacy architecture and increase long-term maintenance burden.

---

### Option 3

Delay both changes until all Verification Engine subprocess refactors were ready.

**Rejected**

Would continue blocking recovery while leaving an incorrect production import path.

---

## Consequences

### Positive

- Removes one duplicated subprocess implementation.
- Stabilizes the production runner import path.
- Begins adoption of the shared ToolRunner abstraction.
- Preserves the existing public API.
- Reduces architectural drift.

### Deferred

- Remaining verification step consolidation will be completed in later frozen
  recovery iterations.
- MCP caller/callee inconsistency remains tracked as technical debt until the
  verification test-package cleanup is complete.

---

## Status

Accepted

Implemented in commit:

**fad1526**

> Refactor: stabilize Verification Engine runner path

docs/adr/README.md

ADR-0001

Verification Engine ToolRunner adoption

## Consequences

### Positive

- Verification Engine imports are now consistent.
- Tool execution is centralized through ToolRunner.
- Duplicate subprocess logic begins to be eliminated.
- Public APIs remain unchanged.

### Negative

- The migration is only partially complete in this ADR.
- Remaining verification steps still require migration (completed later in Iterations 2 and 3).

## Follow-up

This ADR was fully implemented across three recovery iterations:

- Iteration 1 — Runner import stabilization
- Iteration 2 — Linter, Formatter, CoverageRunner migration
- Iteration 3 — SecurityScanner and BenchmarkRunner migration

After Iteration 3, ToolRunner became the sole owner of subprocess execution within the Verification Engine.