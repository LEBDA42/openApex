"""Banister TRIMP — the founding heart-rate training-load metric.

Source: Banister, E.W. (1991). "Modeling Elite Athletic Performance."
In *Physiological Testing of the High-Performance Athlete* (2nd ed.),
Human Kinetics, pp. 403-424.

TRIMP integrates, sample by sample:

    TRIMP = sum( dt_minutes * r * b * exp(k * r) )

where ``r`` is the heart-rate reserve ratio ``(hr - hr_rest) / (hr_max - hr_rest)``
clamped to [0, 1], and ``b``/``k`` are Banister's published coefficients,
sex-specific to reflect lactate-response differences:

    b = 0.64, k = 1.92  (male / default)
    b = 0.86, k = 1.67  (female)
"""

from __future__ import annotations

import math

from openapex.metrics.base import Metric
from openapex.models import Activity, AthleteProfile, MissingProfileData, MissingStreamData

_MALE = (0.64, 1.92)
_FEMALE = (0.86, 1.67)

# Gaps longer than this between samples are treated as recording pauses
# (auto-pause, timer stop) and contribute no load. Garmin "smart recording"
# writes samples at most every ~10-25 s; real pauses last minutes.
_MAX_SAMPLE_GAP_SECONDS = 60.0


class Trimp(Metric):
    key = "trimp"
    unit = ""

    def compute(self, activity: Activity, profile: AthleteProfile) -> float:
        hr = activity.streams.heart_rate
        if hr is None:
            raise MissingStreamData("TRIMP requires a heart_rate stream")
        if profile.hr_rest is None or profile.hr_max is None:
            raise MissingProfileData("TRIMP requires hr_rest and hr_max in the athlete profile")
        reserve = profile.hr_max - profile.hr_rest
        if reserve <= 0:
            raise MissingProfileData("hr_max must be greater than hr_rest")

        b, k = _FEMALE if profile.sex == "F" else _MALE
        time = activity.streams.time
        total = 0.0
        for i in range(1, len(time)):
            sample = hr[i]
            if sample is None:
                continue
            dt = time[i] - time[i - 1]
            if dt <= 0 or dt > _MAX_SAMPLE_GAP_SECONDS:
                continue
            dt_min = dt / 60.0
            r = (sample - profile.hr_rest) / reserve
            r = min(max(r, 0.0), 1.0)
            total += dt_min * r * b * math.exp(k * r)
        return total
