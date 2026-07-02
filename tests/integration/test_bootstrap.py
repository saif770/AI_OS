"""
Integration test for the Bootstrap Framework.
"""

from bootstrap import BootstrapEngine


def test_bootstrap_engine_runs():

    engine = BootstrapEngine()

    context = engine.run()

    summary = context.summary()

    assert isinstance(summary, dict)

    assert summary["project"]
    assert summary["version"]

    assert summary["total_stages"] > 0
    assert summary["successful"] > 0
    assert summary["failed"] == 0

    assert engine.summary == summary