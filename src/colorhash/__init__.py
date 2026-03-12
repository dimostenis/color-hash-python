from .colorhash import ColorHash

try:
    from importlib.metadata import version
except ImportError:
    # Logic for Python < 3.8 (though no longer officially supported via pyproject.toml)
    try:
        from importlib_metadata import version  # type: ignore[import-not-found]
    except ImportError:
        version = None


def get_current_version() -> str:
    """Get the current version of the package."""
    if version:
        try:
            return version("colorhash")
        except Exception:  # noqa: BLE001
            pass
    return "0.0.0"


__version__ = get_current_version()
__all__ = ["ColorHash"]
