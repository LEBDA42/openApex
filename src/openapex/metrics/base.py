"""The metric plugin contract.

A metric is a small, pure computation over one activity plus the athlete's
physiological context. One metric = one class = one module = one pull request.

Every metric MUST cite its published source in the class docstring: OpenApex only
ships open, documented sports science — never reverse-engineered proprietary
formulas or trademarked metric names.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from openapex.models import Activity, AthleteProfile


class Metric(ABC):
    """Base class for all metrics, built-in or third-party.

    Third-party packages register subclasses under the ``openapex.metrics``
    entry-point group; they then appear in :func:`openapex.metrics.available`
    exactly like built-ins.
    """

    #: Stable identifier, lowercase snake_case, unique across the ecosystem.
    key: str

    #: Unit of the returned value, for display ("", "W", "bpm"...).
    unit: str = ""

    @abstractmethod
    def compute(self, activity: Activity, profile: AthleteProfile) -> float:
        """Return the metric value for one activity.

        Raise :class:`openapex.models.MissingStreamData` or
        :class:`openapex.models.MissingProfileData` when inputs are insufficient —
        never guess silently.
        """
