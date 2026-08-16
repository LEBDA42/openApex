import pytest

from openapex import metrics
from openapex.metrics.trimp import Trimp


def test_builtin_trimp_is_discovered_via_entry_points():
    assert metrics.available()["trimp"] is Trimp


def test_get_instantiates():
    assert isinstance(metrics.get("trimp"), Trimp)


def test_unknown_key_lists_installed_metrics():
    with pytest.raises(KeyError, match="trimp"):
        metrics.get("does-not-exist")
