"""Bearing Register: an open-source, GRC-as-code risk register."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("bearing-register")
except PackageNotFoundError:  # pragma: no cover - only when run from an uninstalled source tree
    __version__ = "0.0.0"
