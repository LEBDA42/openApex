---
paths:
  - "pyproject.toml"
  - "src/openapex/**"
---

# Rule: stdlib-first — fitdecode is the only runtime dependency

**Rule.** No new runtime dependency (numpy and pandas included) without an
issue that demonstrates the need and records the decision. Dev-dependencies
stay minimal (pytest, ruff, mypy).

**Why.** Lightness is part of the product: a platform hesitates to embed a
heavy dependency tree, and every dependency is supply-chain surface. The
current math is simple loops over samples — stdlib handles it.

**Apply.**
- Need vectorization? Prove it with a benchmark in the issue first.
- A new parser dependency (TCX/GPX) gets the same treatment: issue, decision,
  then code.
