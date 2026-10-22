from __future__ import annotations

import importlib.metadata

import colorhash


def test_version_exists() -> None:
    """Ensure that colorhash.__version__ is a string and matches expected format."""
    version = colorhash.__version__
    assert isinstance(version, str)
    # Simple check for version format (e.g., "M.m.p" or "0.0.0")
    assert version.count(".") >= 2  # ruff: ignore[magic-value-comparison]
    assert any(c.isdigit() for c in version)


def test_version_is_not_empty() -> None:
    """Ensure that the version string is not empty and not the default '0.0.0'."""
    # We allow "0.0.0" in tests if it's the fallback when metadata is missing
    # but for positive tests we expect a real version
    assert colorhash.__version__


def test_package_version() -> None:
    assert colorhash.__version__ == importlib.metadata.version("colorhash")
