# Verification Engine V2 Recovery & Refactor Checklist (Git Workflow)

## Before Making Changes

Create a safety branch:

``` powershell
git checkout -b verification-engine-v2-recovery
```

Commit the current state (even if broken):

``` powershell
git add .
git commit -m "Checkpoint before Verification Engine V2 recovery"
```

------------------------------------------------------------------------

# Phase 1 -- Verify V2 Replacement

``` powershell
Get-ChildItem core\verification_engine\*.py |
Select-String "subprocess.run"
```

Expected: only `tool_runner.py`.

After completing Phase 1:

``` powershell
git add .
git commit -m "Refactor: replace Verification Engine V1 modules with V2"
```

------------------------------------------------------------------------

# Phase 2 -- Resolve Pytest Collection Conflict

Rename `test_runner.py` to `pytest_runner.py` and update imports.

Commit:

``` powershell
git add .
git commit -m "Refactor: rename test_runner to pytest_runner"
```

------------------------------------------------------------------------

# Phase 3 -- Resolve Test Name Collisions

Rename verification test files to unique names.

Commit:

``` powershell
git add .
git commit -m "Test: rename Verification Engine test modules"
```

------------------------------------------------------------------------

# Phase 4 -- Remove Old Files

Delete obsolete files such as:

-   `tests/unit/verification_engine/test_test_runner.py`

Commit:

``` powershell
git add -A
git commit -m "Cleanup: remove obsolete Verification Engine files"
```

------------------------------------------------------------------------

# Phase 5 -- Clear Python Cache

``` powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter *.pyc | Remove-Item -Force
```

(No commit required.)

------------------------------------------------------------------------

# Phase 6 -- Compile Check

``` powershell
python -m compileall core tests
```

If fixes were required:

``` powershell
git add .
git commit -m "Fix: resolve compilation errors"
```

------------------------------------------------------------------------

# Phase 7 -- Verification Unit Tests

``` powershell
pytest tests/unit/verification_engine -x -vv
```

Fix failures until green.

``` powershell
git add .
git commit -m "Test: Verification Engine unit tests passing"
```

------------------------------------------------------------------------

# Phase 8 -- Verification Integration Test

``` powershell
pytest tests/integration/test_verification_engine.py -x -vv
```

Commit:

``` powershell
git add .
git commit -m "Test: Verification Engine integration passing"
```

------------------------------------------------------------------------

# Phase 9 -- Full Integration Suite

``` powershell
pytest tests/integration -v
```

------------------------------------------------------------------------

# Phase 10 -- Full Project Suite

``` powershell
pytest -v
```

When all tests pass:

``` powershell
git add .
git commit -m "Verification Engine V2 complete"
git tag verification-engine-v2
```

------------------------------------------------------------------------

# Remaining Issue

Fix the Execution Engine regression (`generated.py` not created) in a
separate commit.

``` powershell
git add .
git commit -m "Fix: restore Execution Engine generated file output"
```

------------------------------------------------------------------------

# Completion

Only begin the Reflection Engine after:

-   Verification Engine V2 stable
-   All tests passing
-   No duplicate test modules
-   No import conflicts
-   No V1 code remaining
