# CLAUDE.md — OpenApex


## What this is & why

OpenApex is a Python **library** : open,
documented training metrics for endurance sports. Strategy: be the analytical
brick that self-hosted fitness platforms (Endurain first) and AI agents embed.
Three things are therefore the product itself: **trust** (verifiable, cited
science), **lightness** (minimal dependencies), and the **plugin surface**
(third parties ship metrics without touching core).

## Stack

- Python ≥ 3.11, typed strict, `slots=True` dataclasses, line length 100,
  English identifiers and docstrings.
- Build: hatchling. Runtime dependency: `fitdecode` **only**.
- Quality: pytest, ruff, mypy strict. CI: GitHub Actions (3.11/3.12/3.13).
- Publishing: PyPI trusted publishing (OIDC) via GitHub release — no tokens.

## Commands (project venv, Windows)

```
.venv\Scripts\pip.exe install -e ".[dev]"     # setup
.venv\Scripts\ruff.exe check src tests        # gate 1
.venv\Scripts\mypy.exe                        # gate 2 (strict)
.venv\Scripts\python.exe -m pytest -q         # gate 3
```

All three gates green before every commit. CI enforces them on push.

## Architecture & dependency rules

- `src/openapex/models.py` — normalized vocabulary (`Activity`,
  `ActivityStreams`, `AthleteProfile`, `Sport`, `Missing*Data`). Depends on
  nothing.
- `src/openapex/io/` — file parsers → `Activity`. Depends on `models` only.
  Adding any runtime dependency requires an issue and a decision first.
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

## Hard rules — each points to its rationale in `.claude/rules/`

Rules auto-load when you touch matching files; read the rule file for the why
and the do/don't examples before working around any of them.

- Every metric cites its published source. → `.claude/rules/cited-sources.md`
- Open lineage only; trademarked/proprietary formulas (TSS®, NP®, IF®…) are
  banned. → `.claude/rules/open-formulas.md`
- Never copy GPL/AGPL code (GoldenCheetah is GPL-2.0). →
  `.claude/rules/license-hygiene.md`
- Stdlib-first; `fitdecode` is the only runtime dependency. →
  `.claude/rules/dependencies.md`
- Public API = `openapex/__init__.py` exports + the `Metric` contract +
  `metrics.available()/get()`. Pre-1.0 breaking changes allowed but stated in
  the commit body.

## Agent toolbox — where each truth lives

| Tool | Carries | When it activates |
|---|---|---|
| Rules `.claude/rules/*.md` | One rule each: statement, rationale, do/don't examples | Auto-loaded when touching files matching their `paths` globs |
| Skill `/new-metric` | Full metric-development doctrine: paper first, closed-form test before code, the four guards, entry point, test checklist | Any creation or rework under `src/openapex/metrics/` |
| Skill `/release` | Publishing truth: versioning, tagging, trusted-publishing pipeline, maintainer identity | Releases only — human-invoked (`disable-model-invocation`) |
| Skill `/fix-issue` | Issue workflow: reproduce with a failing test, fix, gates, review, commit | Human-invoked with an issue number |
| Agent `code-reviewer` | Diff review: dependency direction, guards, typing, API surface, test coverage | Ask for it after writing code, before committing |
| Agent `science-reviewer` | Sports-science integrity: citation completeness, formula fidelity, banned names, coefficient provenance | Ask for it on any metric change |
| Hook `block_force_push` (`.claude/settings.json`) | Append-only history, enforced deterministically | Automatic, every Bash command |
| `CONTRIBUTING.md` | Human process: commit etiquette, PR checklist | Contributors |
| `docs/ROADMAP.md` | Prioritized roadmap | Choosing the next work item |
