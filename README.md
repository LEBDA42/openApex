# OpenApex

**Open metrics for endurance sports.**

OpenApex is a Python library — not a platform — that turns raw activity files into
training insight. The apex is the top of your form curve: the peak that periodized
training builds toward. This library computes the curve.

- **Parse** FIT/TCX/GPX files locally. No cloud, no vendor API, no account.
- **Compute** training load with *open, documented* metrics — every formula cites its
  published source. No reverse-engineered proprietary scores, no trademarked names.
- **Model** fitness, fatigue and form over time (impulse-response models).
- **Estimate** thresholds and zones; predict race performance. *(roadmap)*
- **Extend** everything: one metric = one class = one entry point. Third-party
  packages plug into the same registry as built-ins.

OpenApex is the missing analytical brick for the self-hosted fitness ecosystem
(Endurain, FitTrackee, Dreeve, your own scripts) and for AI agents — an MCP server
package is on the roadmap so any assistant can analyze *your* data, locally.

## Status

Pre-alpha. The data model, the FIT reader, the plugin registry and the first metric
(Banister TRIMP) are in place and tested. API will move.

## Quick taste

```python
from openapex import read_fit, AthleteProfile
from openapex import metrics

activity = read_fit("morning_ride.fit")
profile = AthleteProfile(hr_rest=48, hr_max=188)

trimp = metrics.get("trimp").compute(activity, profile)
print(f"{activity.sport.value}, {activity.duration_seconds/60:.0f} min, TRIMP {trimp:.0f}")
```

## Writing your own metric

```python
from openapex.metrics.base import Metric

class MyMetric(Metric):
    """Cite your published source here — it's a hard rule."""
    key = "my_metric"

    def compute(self, activity, profile):
        ...
```

Register it in your package's `pyproject.toml`:

```toml
[project.entry-points."openapex.metrics"]
my_metric = "my_package.my_module:MyMetric"
```

That's the whole contract. `openapex.metrics.available()` now finds it.

## Why "open metrics" matters

The dominant training-load scores (TSS®, Normalized Power®…) are proprietary and
trademarked. OpenApex implements the peer-reviewed lineage instead — Banister's TRIMP,
impulse-response performance modeling, critical-power models — with sources cited in
every docstring, so athletes, coaches and researchers can read, verify and improve
the math that scores their training.

## Development

```
pip install -e ".[dev]"
pytest
```

## License

Apache-2.0 — see [LICENSE](LICENSE).
