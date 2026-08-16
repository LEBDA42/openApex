"""Core data model: a normalized view of one recorded activity.

Every parser (FIT, TCX, GPX) produces these structures; every metric
consumes them. Nothing here depends on any file format or vendor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Sport(str, Enum):
    CYCLING = "cycling"
    RUNNING = "running"
    SWIMMING = "swimming"
    OTHER = "other"


@dataclass(slots=True)
class ActivityStreams:
    """Per-sample time series. ``time`` is seconds elapsed since activity start.

    All other streams are either ``None`` (not recorded) or the same length
    as ``time``. Individual samples may be ``None`` when the sensor dropped out.
    """

    time: list[float]
    power: list[float | None] | None = None          # watts
    heart_rate: list[float | None] | None = None     # beats per minute
    speed: list[float | None] | None = None          # meters per second
    altitude: list[float | None] | None = None       # meters
    cadence: list[float | None] | None = None        # rpm or spm
    distance: list[float | None] | None = None       # meters, cumulative

    def __post_init__(self) -> None:
        n = len(self.time)
        for name in ("power", "heart_rate", "speed", "altitude", "cadence", "distance"):
            stream: list[float | None] | None = getattr(self, name)
            if stream is not None and len(stream) != n:
                raise ValueError(
                    f"stream '{name}' has {len(stream)} samples, expected {n} (same as 'time')"
                )


@dataclass(slots=True)
class Activity:
    """One recorded session, normalized and unit-consistent (SI + bpm/rpm)."""

    start: datetime
    sport: Sport
    streams: ActivityStreams
    name: str | None = None
    source: str | None = None  # e.g. the file path or connector it came from

    @property
    def duration_seconds(self) -> float:
        if not self.streams.time:
            return 0.0
        return self.streams.time[-1] - self.streams.time[0]


@dataclass(slots=True)
class AthleteProfile:
    """Physiological context needed by metrics.

    Metrics must degrade gracefully (raise ``MissingProfileData``) when a
    field they need is absent, so callers can decide what to require.
    """

    hr_rest: float | None = None      # bpm
    hr_max: float | None = None       # bpm
    ftp: float | None = None          # watts (functional threshold power)
    threshold_pace: float | None = None  # m/s
    sex: str | None = None            # "F" | "M" — some published models are sex-specific
    extra: dict[str, float] = field(default_factory=dict)


class MissingProfileData(ValueError):
    """A metric needs an :class:`AthleteProfile` field that is not set."""


class MissingStreamData(ValueError):
    """A metric needs an activity stream that was not recorded."""
