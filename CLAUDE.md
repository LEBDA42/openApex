# CLAUDE.md — OpenApex

Read this before writing any code. It is the contract for every contribution,
human or AI-assisted.

## 1. Context & stakes

OpenApex is a **Python library** — deliberately not a platform, not a service,
not a UI. Tagline: *Open metrics for endurance sports*.

Why it exists: the dominant training-load metrics (TSS®, Normalized Power®…)
are proprietary and trademarked; intervals.icu — the reference analysis tool —
is closed source with a bus factor of one; and every open-source self-hosted
fitness platform (Endurain, FitTrackee, Dreeve) ships **zero training
intelligence** because the math is the hard part. OpenApex is that missing
brick: the analytical engine those platforms — and AI agents — can embed.

Strategy: *be the engine every boat embarks, not another boat.* Primary
adoption target: Endurain (FastAPI, Python — can import us natively). Secondary:
scripts and notebooks of data-minded athletes. Third: AI assistants via the
future `openapex-mcp` satellite. Everything below follows from this strategy:

- **Trust is the product.** Adopters embed us only if the science is verifiable:
  every formula cites its published source, every metric has a closed-form test.
- **Lightness is the product.** A platform hesitates to add a heavy dependency
  tree. Core stays stdlib + `fitdecode`, nothing else.
- **The plugin surface is the product.** Community growth = third parties
  shipping metrics without touching core. The entry-point registry is sacred.

## 2. Architecture & dependency rules

```
src/openapex/
├── models.py     # normalized vocabulary: Activity, ActivityStreams,
│                 # AthleteProfile, Sport, Missing*Data errors
├── io/           # file parsers -> Activity  (fit.py today; tcx, gpx later)
└── metrics/      # Metric ABC (base.py), entry-point registry (__init__.py),
                  # built-in metrics (one module each: trimp.py, ...)
```

Strict dependency direction — never violate it:

- `models` depends on **nothing** (stdlib only). It is the only vocabulary the
  rest of the world may rely on.
- `io` depends on `models` only. `fitdecode` is the **sole third-party runtime
  dependency of the project**; any new parser dependency needs explicit
  justification in the PR description.
- `metrics` depend on `models` only — never on `io`, never on each other.
  A metric is a pure function of `(Activity, AthleteProfile)`.
- Satellites are **separate packages**, never merged into core:
  `openapex-mcp` (AI agents), `openapex-seuil` (thresholds), `openapex-forme`
  (fitness/fatigue/form), `openapex-cadence`, `openapex-allure`,
  `openapex-tempo` (planning). Core never imports a satellite. Satellite names
  come from the endurance lexicon, in French — it is the project's signature.

## 3. Data-model invariants (never break these)

- **Units**: SI everywhere — meters, seconds, m/s, watts — plus bpm and rpm.
  State the unit in every docstring that mentions a quantity.
- `ActivityStreams.time` = seconds elapsed since activity start. Expected
  non-decreasing, but **never assume it**: guard every `dt`.
- Stream semantics: whole stream `None` = never recorded; one sample `None` =
  sensor dropout. All streams have exactly `len(time)` samples (validated in
  `__post_init__`).
- Datetimes are timezone-aware UTC (FIT timestamps already are).
- `AthleteProfile` fields are all optional. A metric that needs one raises
  `MissingProfileData`; a metric missing a stream raises `MissingStreamData`.
  **Never invent a default for physiological data.**

## 4. How to develop a metric (mandatory workflow, in this order)

1. **Read the published source first.** Put formula and citation (author, year,
   title, pages) in the class docstring before writing code.
2. **Write the closed-form test before the implementation**: a hand-computable
   case where the sample-wise result equals the paper's session-level formula
   (see `tests/test_trimp.py::test_steady_hour_matches_closed_form`).
3. **Implement sample-wise** (integrate over `dt` between consecutive samples)
   with the standard guards, all of them:
   - `dt <= 0` → skip the interval (non-monotonic or duplicate timestamps);
   - `dt > _MAX_SAMPLE_GAP_SECONDS` (60 s) → recording pause, skip — pauses
     must never accrue load (see `metrics/trimp.py` for the pattern);
   - sample is `None` → skip;
   - clamp physiological ratios to their valid range when the model defines one.
4. **Register the entry point** in `pyproject.toml` under
   `[project.entry-points."openapex.metrics"]`. Built-ins register exactly like
   third-party plugins — no privileged path. `key` is stable snake_case,
   unique, never renamed once released.
5. **Run the three quality gates** (§7). All green before any commit.

## 5. Science & legal rules (hard constraints)

- Published, citable sources only; peer-reviewed preferred. If you cannot cite
  it, you cannot merge it.
- **Banned**: trademarked metric names and reverse-engineered proprietary
  formulas — TSS®, NP®, IF®, rTSS, hrTSS, Stryd power metrics, WKO-specific
  models. We implement the open lineage (Banister, Foster, Critical Power…)
  under open names.
- **Never copy code from GPL/AGPL projects.** GoldenCheetah is GPL-2.0: read
  the papers it cites, never its source. OpenApex is Apache-2.0 and must stay
  license-clean.
- No athlete data in the repo except small, anonymized fixtures under
  `tests/fixtures/` (strip GPS traces unless the test needs them).

## 6. Testing doctrine

- Per metric: the closed-form test **plus** edge cases — empty streams,
  all-`None` stream, sensor dropouts, recording-pause gap, values below resting
  baseline, sex-specific coefficient variants when the model has them.
- Per parser: real anonymized fixture files in `tests/fixtures/`, asserting
  stream lengths, units and known values from the source device.
- Test through the public API; never mock our own models.

## 7. Quality gates & style

All three must pass before every commit (project venv, Windows paths):

```
.venv\Scripts\ruff.exe check src tests
.venv\Scripts\mypy.exe
.venv\Scripts\python.exe -m pytest -q
```

Style: Python ≥ 3.11, line length 100, `slots=True` dataclasses, strict typing
(mypy strict is non-negotiable), English identifiers and docstrings.
**Stdlib-first**: no numpy/pandas until a metric measurably needs them — open
an issue and decide there first.

Public API = names exported by `openapex/__init__.py`, the `Metric` contract,
and `metrics.available()/get()`. Everything else is internal and may change.
Pre-1.0: breaking changes allowed, but state them in the commit body.

## 8. Git & publishing

- Author identity: `LEBDA42 <LEBDA42@users.noreply.github.com>`. Never commit
  with a personal or corporate email.
- History is **append-only** since the 2026-08-16 reset. Never rewrite
  published history again.
- Commit style: imperative subject; body explains *why*, not *what*.
- Remote: https://github.com/LEBDA42/openApex. Publishing: GitHub release →
  `.github/workflows/publish.yml` → PyPI trusted publishing (OIDC, environment
  `pypi`, no tokens).

## 9. Roadmap (order of battle)

1. Real FIT fixtures + `read_fit` hardening: multi-session files, pauses,
   developer fields, smart recording.
2. **Banister impulse-response model** → fitness/fatigue/form curves. The
   flagship feature; what the project will be judged on.
3. Threshold estimation from the literature (Critical Power model, eFTP-style
   estimates under open names).
4. Race prediction (Riegel, VDOT, CP-based).
5. `openapex-mcp` satellite: expose activities and metrics to AI agents.
