from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

FILES = [
    # Root
    "bootstrap.py",
    "setup.bat",
    "README.md",
    "requirements.txt",

    # Bootstrap package
    "bootstrap/__init__.py",
    "bootstrap/result.py",
    "bootstrap/base.py",
    "bootstrap/context.py",
    "bootstrap/registry.py",
    "bootstrap/config.py",
    "bootstrap/environment.py",
    "bootstrap/structure.py",
    "bootstrap/dependencies.py",
    "bootstrap/git_setup.py",
    "bootstrap/verification.py",
    "bootstrap/mcp_setup.py",
    "bootstrap/project_scan.py",
    "bootstrap/ai_readiness.py",
    "bootstrap/report.py",

    # Config
    "config/bootstrap.yaml",
    "config/logging.yaml",

    # Documentation
    "docs/PROJECT_CONTEXT.md",

    # Templates
    "templates/.gitkeep",

    # Tests
    "tests/__init__.py",

    # Bootstrap State
    ".bootstrap/state.json",
    ".bootstrap/version.json",
    ".bootstrap/report.json",
    ".bootstrap/bootstrap.log",
]

print("=" * 60)
print("Creating Project Files")
print("=" * 60)

created = 0
skipped = 0

for file in FILES:
    path = PROJECT_ROOT / file

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        print(f"[SKIP] {file}")
        skipped += 1
    else:
        path.touch()
        print(f"[ OK ] {file}")
        created += 1

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print(f"Created : {created}")
print(f"Skipped : {skipped}")
print("=" * 60)

