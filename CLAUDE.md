# CLAUDE.md — OpenApex

Source of truth for coding agents and contributors. Facts here are always true;
procedures live in the skills listed at the bottom and load on demand.

## What this is & why

OpenApex is a Python **library** (not a platform, not a service): open,
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
  `metrics.available()/get()`. Pre-1.0 breaking changes allowed but stated in
  the commit body.

## Agent toolbox — where each truth lives

| Outil | Rôle | Quand |
|---|---|---|
| Skill `/new-metric` (`.claude/skills/new-metric/`) | Doctrine complète de développement d'une métrique : papier d'abord, test en forme fermée avant le code, les 4 gardes, entry point, checklist de tests | Toute création/refonte sous `src/openapex/metrics/` |
| Skill `/release` (`.claude/skills/release/`) | Vérité de publication : versionnage, tag, pipeline trusted publishing, identité mainteneur | Release uniquement — déclenchement humain (`disable-model-invocation`) |
| Hook `block_force_push` (`.claude/hooks/`, câblé dans `.claude/settings.json`) | Historique append-only appliqué déterministiquement : tout `git push --force` est bloqué | Automatique, chaque commande Bash |
| `CONTRIBUTING.md` | Processus humain : étiquette de commit, checklist PR | Contributeurs |
| `docs/ROADMAP.md` | Feuille de route hiérarchisée | Choix du prochain chantier |
