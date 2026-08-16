# Contributing to OpenApex

OpenApex is designed so that **one metric = one class = one pull request**. If you can
read a sports-science paper and write 50 lines of Python, you can contribute a metric.

## Ground rules

1. **Cite your source.** Every metric's docstring names the published paper or book
   it implements. We do not merge reverse-engineered proprietary formulas or
   trademarked metric names (TSS®, NP®, …) — open equivalents only.
2. **Fail loudly, never guess.** If the activity or profile lacks required data,
   raise `MissingStreamData` / `MissingProfileData`.
3. **Test against a closed form.** Each metric ships a test that checks the
   sample-wise computation against a hand-computable case (see `tests/test_trimp.py`).
4. **Core stays dependency-light.** File parsing and pure-Python math live here;
   vendor-cloud connectors, servers and UIs belong in separate packages.

## Adding a metric

1. Create `src/openapex/metrics/your_metric.py` with a `Metric` subclass.
2. Register it in `pyproject.toml` under `[project.entry-points."openapex.metrics"]`.
3. Add tests in `tests/test_your_metric.py`.
4. `pip install -e ".[dev]" && pytest && ruff check && mypy`

## Not sure where to start?

Issues labeled `good-first-metric` list formulas with their sources, waiting for an
implementation. Questions welcome in the issue tracker — in English or French.
