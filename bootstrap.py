"""
bootstrap.py

Command-line entry point for the AI Operating System Bootstrap Engine.
"""

from __future__ import annotations

from bootstrap import BootstrapEngine


def print_header() -> None:
    print("=" * 70)
    print("AI Operating System")
    print(f"Bootstrap Engine v{BootstrapEngine.VERSION}")
    print("=" * 70)


def print_summary(engine: BootstrapEngine) -> None:
    summary = engine.summary

    print("\n" + "=" * 70)
    print("Execution Summary")
    print("=" * 70)

    print(f"Project        : {summary['project']}")
    print(f"Version        : {summary['version']}")
    print(f"Stages         : {summary['total_stages']}")
    print(f"Successful     : {summary['successful']}")
    print(f"Failed         : {summary['failed']}")

    print("=" * 70)


def main() -> int:
    print_header()

    engine = BootstrapEngine()

    engine.run()

    print_summary(engine)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())