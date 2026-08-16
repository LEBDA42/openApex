from datetime import UTC, datetime

import pytest

from openapex import Activity, ActivityStreams, Sport


def test_stream_length_mismatch_is_rejected():
    with pytest.raises(ValueError, match="heart_rate"):
        ActivityStreams(time=[0.0, 1.0, 2.0], heart_rate=[120.0])


def test_duration():
    activity = Activity(
        start=datetime(2026, 8, 16, tzinfo=UTC),
        sport=Sport.CYCLING,
        streams=ActivityStreams(time=[0.0, 1.0, 2.5]),
    )
    assert activity.duration_seconds == 2.5
