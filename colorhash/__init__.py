from .colorhash import ColorHash

try:
    # py3.8+
    from importlib.metadata import version

except ImportError:
    # py3.6 - py3.7
    from importlib_metadata import version

__all__ = ["ColorHash"]
__version__ = version(__package__)
