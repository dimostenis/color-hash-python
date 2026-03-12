from importlib.metadata import version

from .colorhash import ColorHash


def get_current_version() -> str:
    """Get the current version of the package."""
    try:
        return version("colorhash")
    except Exception:  # noqa: BLE001
        return "0.0.0"


__version__ = get_current_version()
__all__ = ["ColorHash"]
