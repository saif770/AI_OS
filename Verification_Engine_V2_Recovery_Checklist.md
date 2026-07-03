# Verification Engine V2 Recovery & Refactor Checklist

## Current Status

The project is in a mixed **V1/V2** state. Do **not** add new features
until the Verification Engine is stable.

------------------------------------------------------------------------

# Phase 1 -- Verify V2 Replacement

Run:

``` powershell
Get-ChildItem core\verification_engine\*.py |
Select-String "subprocess.run"
```

## Expected

Only:

``` text
core\verification_engine\tool_runner.py
```

If any of these files appear, they are still V1 and must be replaced:

-   test_runner.py (or pytest_runner.py)
-   linter.py
-   formatter.py
-   coverage.py
-   security.py
-   benchmark.py

------------------------------------------------------------------------

# Phase 2 -- Resolve Pytest Collection Conflict

Rename:

``` text
core/verification_engine/test_runner.py
```

to

``` text
core/verification_engine/pytest_runner.py
```

Update imports in:

-   engine.py
-   **init**.py
-   unit tests
-   integration tests

Import should become:

``` python
from .pytest_runner import PytestRunner
```

------------------------------------------------------------------------

# Phase 3 -- Resolve Test Name Collisions

Rename Verification Engine test files so they are unique.

Suggested names:

-   test_verification_compiler.py
-   test_verification_runner.py
-   test_verification_linter.py
-   test_verification_formatter.py
-   test_verification_coverage.py
-   test_verification_security.py
-   test_verification_benchmark.py
-   test_verification_report.py
-   test_verification_models.py
-   test_verification_engine.py

This avoids collisions with Execution Engine tests.

------------------------------------------------------------------------

# Phase 4 -- Remove Old Files

Delete obsolete files if they exist:

-   tests/unit/verification_engine/test_test_runner.py

Ensure there is only one runner test.

------------------------------------------------------------------------

# Phase 5 -- Clear Python Cache

``` powershell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force

Get-ChildItem -Recurse -Filter *.pyc | Remove-Item -Force
```

------------------------------------------------------------------------

# Phase 6 -- Compile Check

``` powershell
python -m compileall core tests
```

Fix any syntax errors before running pytest.

------------------------------------------------------------------------

# Phase 7 -- Verification Engine Unit Tests

``` powershell
pytest tests/unit/verification_engine -x -vv
```

Fix failures one at a time.

------------------------------------------------------------------------

# Phase 8 -- Verification Integration Test

``` powershell
pytest tests/integration/test_verification_engine.py -x -vv
```

------------------------------------------------------------------------

# Phase 9 -- Full Integration Suite

``` powershell
pytest tests/integration -v
```

------------------------------------------------------------------------

# Phase 10 -- Full Project Test Suite

``` powershell
pytest -v
```

------------------------------------------------------------------------

# Remaining Known Issue

Execution Engine integration test:

    generated.py not created

Investigate:

-   ExecutionEngine.execute()
-   PatchApplier
-   Code generation pipeline
-   File writing logic

Do **not** modify Verification Engine while fixing this regression.

------------------------------------------------------------------------

# Completion Criteria

-   Verification Engine V2 fully replaces V1
-   Only ToolRunner uses subprocess.run()
-   No pytest collection errors
-   No import file mismatch errors
-   No duplicate tests
-   Verification unit tests pass
-   Verification integration tests pass
-   Full project test suite passes
-   Execution Engine regression fixed

Only after all of the above should work begin on the Reflection Engine.
