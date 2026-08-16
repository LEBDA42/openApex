import math
from datetime import UTC, datetime

import pytest

from openapex import (
    Activity,
    ActivityStreams,
    AthleteProfile,
    MissingProfileData,
    MissingStreamData,
    Sport,
)
from openapex.metrics.trimp import Trimp


def make_activity(hr: list[float | None], dt: float = 1.0) -> Activity:
    times = [i * dt for i in range(len(hr))]
    return Activity(
        start=datetime(2026, 8, 16, 7, 0, tzinfo=UTC),
        sport=Sport.RUNNING,
        streams=ActivityStreams(time=times, heart_rate=hr),
    )


PROFILE = AthleteProfile(hr_rest=50, hr_max=190, sex="M")


def test_steady_hour_matches_closed_form():
    # 60 minutes at constant HR: the sample-wise integral equals Banister's
    # session-level formula duration * r * b * exp(k * r).
    hr = [120.0] * 3601  # 1 Hz for one hour
    trimp = Trimp().compute(make_activity(hr), PROFILE)
    r = (120 - 50) / (190 - 50)
    expected = 60 * r * 0.64 * math.exp(1.92 * r)
    assert trimp == pytest.approx(expected, rel=1e-6)


def test_female_coefficients_differ():
    hr = [150.0] * 601
    male = Trimp().compute(make_activity(hr), PROFILE)
    female = Trimp().compute(make_activity(hr), AthleteProfile(hr_rest=50, hr_max=190, sex="F"))
    assert male != pytest.approx(female)


def test_hr_below_rest_contributes_nothing():
    hr = [40.0] * 601  # below hr_rest: reserve ratio clamps to 0
    assert Trimp().compute(make_activity(hr), PROFILE) == 0.0


def test_recording_pause_contributes_no_load():
    # Two samples one hour apart (watch paused at the café): the gap must not
    # be integrated as effort time.
    activity = make_activity([150.0, 150.0], dt=3600.0)
    assert Trimp().compute(activity, PROFILE) == 0.0


def test_sensor_dropouts_are_skipped():
    hr: list[float | None] = [120.0, None, 120.0, None, 120.0]
    trimp = Trimp().compute(make_activity(hr), PROFILE)
    assert trimp > 0


def test_missing_stream_raises():
    activity = make_activity([120.0] * 10)
    activity.streams.heart_rate = None
    with pytest.raises(MissingStreamData):
        Trimp().compute(activity, PROFILE)


def test_missing_profile_raises():
    with pytest.raises(MissingProfileData):
        Trimp().compute(make_activity([120.0] * 10), AthleteProfile())
