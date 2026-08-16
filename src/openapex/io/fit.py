"""FIT file parsing — the universal, vendor-neutral ingestion path.

FIT is the native format of Garmin, Wahoo, Coros, Suunto and Hammerhead
devices, and of the Strava/Garmin GDPR bulk exports. Parsing files locally is
OpenApex's zero-cloud, zero-API-risk ingestion strategy; connectors to vendor
clouds belong in separate optional packages, never in the core.

Built on ``fitdecode`` (MIT).
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import fitdecode

from openapex.models import Activity, ActivityStreams, Sport

_SPORT_MAP = {
    "cycling": Sport.CYCLING,
    "running": Sport.RUNNING,
    "swimming": Sport.SWIMMING,
}

# FIT record fields -> stream name (first non-empty variant wins per sample)
_FIELDS: dict[str, str] = {
    "power": "power",
    "heart_rate": "heart_rate",
    "enhanced_speed": "speed",
    "speed": "speed",
    "enhanced_altitude": "altitude",
    "altitude": "altitude",
    "cadence": "cadence",
    "distance": "distance",
}


def read_fit(path: str | Path) -> Activity:
    """Parse one FIT activity file into a normalized :class:`Activity`."""
    path = Path(path)
    start: datetime | None = None
    sport = Sport.OTHER
    times: list[float] = []
    raw: dict[str, list[float | None]] = {name: [] for name in set(_FIELDS.values())}

    with fitdecode.FitReader(path) as reader:
        for frame in reader:
            if not isinstance(frame, fitdecode.FitDataMessage):
                continue
            if frame.name == "session":
                value = _field(frame, "sport")
                if isinstance(value, str):
                    sport = _SPORT_MAP.get(value, Sport.OTHER)
            elif frame.name == "record":
                timestamp = _field(frame, "timestamp")
                if not isinstance(timestamp, datetime):
                    continue
                if start is None:
                    start = timestamp
                times.append((timestamp - start).total_seconds())
                seen: set[str] = set()
                for fit_name, stream_name in _FIELDS.items():
                    if stream_name in seen:
                        continue
                    value = _field(frame, fit_name)
                    if isinstance(value, (int, float)):
                        raw[stream_name].append(float(value))
                        seen.add(stream_name)
                for stream_name, values in raw.items():
                    if stream_name not in seen:
                        values.append(None)

    if start is None:
        raise ValueError(f"{path}: no record messages found — not an activity FIT file?")

    def stream(name: str) -> list[float | None] | None:
        values = raw[name]
        return values if any(v is not None for v in values) else None

    return Activity(
        start=start,
        sport=sport,
        streams=ActivityStreams(
            time=times,
            power=stream("power"),
            heart_rate=stream("heart_rate"),
            speed=stream("speed"),
            altitude=stream("altitude"),
            cadence=stream("cadence"),
            distance=stream("distance"),
        ),
        source=str(path),
    )


def _field(frame: fitdecode.FitDataMessage, name: str) -> object | None:
    try:
        value: object = frame.get_value(name)
    except KeyError:
        return None
    return value
