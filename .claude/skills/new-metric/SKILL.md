---
name: new-metric
description: Add a new training metric to OpenApex, or substantially modify an existing one. Carries the full metric-development doctrine — mandatory workflow order, numerical guards, testing checklist. Use whenever creating or reworking anything under src/openapex/metrics/.
---

# Adding a metric to OpenApex

Follow these steps **in this order**. The order is the doctrine: science first,
test second, code third.

## 1. Read the published source first

Find the paper or book chapter defining the metric. Put the formula and the
full citation (author, year, title, pages) in the class docstring **before
writing any code**. If you cannot cite it, stop — OpenApex does not ship
uncited or proprietary math (see AGENTS.md hard rules).

## 2. Write the closed-form test BEFORE the implementation

A hand-computable case where the sample-wise result must equal the paper's
session-level formula. Model:
`tests/test_trimp.py::test_steady_hour_matches_closed_form` — constant input
for one hour at 1 Hz, compared with `pytest.approx` against the closed form.

## 3. Implement sample-wise, with every guard

Integrate over `dt` between consecutive samples. All four guards, always:

- `dt <= 0` → skip (non-monotonic or duplicate timestamps);
- `dt > _MAX_SAMPLE_GAP_SECONDS` (60 s) → recording pause, skip — pauses must
  never accrue load (pattern: `src/openapex/metrics/trimp.py`);
- sample is `None` → skip (sensor dropout);
- clamp physiological ratios to their valid range when the model defines one.

Missing inputs raise `MissingStreamData` / `MissingProfileData` — never guess.
One metric = one module in `src/openapex/metrics/` = one `Metric` subclass.
`key` is stable snake_case, unique, never renamed once released. Set `unit`.

## 4. Register the entry point

In `pyproject.toml`:

```toml
[project.entry-points."openapex.metrics"]
your_key = "openapex.metrics.your_module:YourClass"
```

Built-ins register exactly like third-party plugins — no privileged path.

## 5. Test checklist, then gates

Beyond the closed-form test, cover: empty streams, all-`None` stream, sensor
dropouts, recording-pause gap, values below the resting baseline, sex-specific
coefficient variants when the model has them. Test through the public API;
never mock our own models.

Then run the three gates from AGENTS.md — all green before commit.
