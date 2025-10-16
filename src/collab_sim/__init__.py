"""CollabLLM-inspired healthcare conversation simulation framework."""

from importlib.metadata import version

__all__ = [
    "__version__",
]

try:
    __version__ = version("collab-sim")
except Exception:
    __version__ = "0.1.0"
