"""Metric discovery: built-ins and third-party plugins, one registry.

Any installed package exposing an ``openapex.metrics`` entry point that resolves
to a :class:`openapex.metrics.base.Metric` subclass is discovered here — OpenApex's
own built-ins register through the exact same mechanism (see pyproject.toml),
so there is no privileged path.
"""

from __future__ import annotations

from functools import cache
from importlib.metadata import entry_points

from openapex.metrics.base import Metric

__all__ = ["Metric", "available", "get"]


@cache
def available() -> dict[str, type[Metric]]:
    """All discovered metrics, keyed by their stable ``key``."""
    registry: dict[str, type[Metric]] = {}
    for ep in entry_points(group="openapex.metrics"):
        cls = ep.load()
        if not (isinstance(cls, type) and issubclass(cls, Metric)):
            raise TypeError(f"entry point 'openapex.metrics:{ep.name}' is not a Metric subclass")
        if cls.key in registry:
            raise ValueError(f"duplicate metric key '{cls.key}' from entry point '{ep.name}'")
        registry[cls.key] = cls
    return registry


def get(key: str) -> Metric:
    """Instantiate the metric registered under ``key``."""
    try:
        return available()[key]()
    except KeyError:
        raise KeyError(f"no metric '{key}' — installed metrics: {sorted(available())}") from None
