"""Smoke tests for package initialization and version."""

def test_package_imports():
    import pumpfail

    assert pumpfail.__version__ == "0.1.0"