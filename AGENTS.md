# AGENTS.md — OpenApex

OpenApex is a Python **library** (not a platform, not a service): open, documented
training metrics for endurance sports. Strategy: be the analytical brick that
self-hosted fitness platforms (Endurain first) and AI agents embed. Three things
are therefore the product itself: **trust** (verifiable, cited science),
**lightness** (stdlib + `fitdecode`, nothing else), and the **plugin surface**
(third parties ship metrics without touching core).

This file is the source of truth for coding agents. Do not grow CLAUDE.md.

## Commands (project venv, Windows)

```
.venv\Scripts\pip.exe install -e ".[dev]"     # setup
.venv\Scripts\ruff.exe check src tests        # gate 1
.venv\Scripts\mypy.exe                        # gate 2 (strict)
.venv\Scripts\python.exe -m pytest -q         # gate 3
```

All three gates green before every commit. CI enforces them on push.

## Architecture & dependency rules

- `src/openapex/models.py` — normalized vocabulary (`Activity`, `ActivityStreams`,
  `AthleteProfile`, `Sport`, `Missing*Data`). Depends on nothing.
- `src/openapex/io/` — file parsers → `Activity`. Depends on `models` only.
  `fitdecode` is the **sole runtime dependency**; adding any other requires an
  issue and a decision first.
- `src/openapex/metrics/` — `Metric` ABC, entry-point registry (group
  `openapex.metrics`), one module per metric. Metrics depend on `models` only —
  never on `io`, never on each other. Built-ins register like third-party
  plugins; no privileged path.
- Satellites (`openapex-mcp`, `openapex-seuil`, `openapex-forme`,
  `openapex-cadence`, `openapex-allure`, `openapex-tempo`) are separate
  packages, named from the French endurance lexicon. Core never imports them.

## Invariants (always true)

- SI units + bpm/rpm; state the unit in every docstring. `time` = seconds since
  activity start; datetimes are timezone-aware UTC.
- Whole stream `None` = never recorded; one sample `None` = sensor dropout;
  every stream has exactly `len(time)` samples.
- Never invent defaults for physiological data — raise `MissingStreamData` /
  `MissingProfileData`.
- Guard every `dt`: `dt <= 0` → skip; `dt > 60 s` → recording pause, skip.

## Hard rules

- Every metric cites its published source (author, year, title, pages) in the
  class docstring. No citation, no merge.
- Banned: trademarked or reverse-engineered proprietary formulas (TSS®, NP®,
  IF®, rTSS, hrTSS, Stryd/WKO models). Open lineage only (Banister, Foster,
  Critical Power…).
- Never copy GPL/AGPL code — GoldenCheetah is GPL-2.0: read the papers it
  cites, never its source. The project is Apache-2.0 and stays license-clean.
- Stdlib-first: no numpy/pandas until an issue decides a metric needs them.
- Public API = `openapex/__init__.py` exports + the `Metric` contract +
  `metrics.available()/get()`. Everything else may change; pre-1.0 breaking
  changes are allowed but stated in the commit body.

## Workflows — load on demand, do not inline here

- Adding or modifying a metric → use the **`new-metric`** skill.
- Publishing a release → use the **`release`** skill (human-invoked only).
- Human contribution process → `CONTRIBUTING.md`. Roadmap → `docs/ROADMAP.md`.
