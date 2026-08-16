---
paths:
  - "src/openapex/metrics/**"
  - "tests/**"
---

# Rule: every metric cites its published source

**Rule.** A metric's class docstring states the formula AND its full citation:
author, year, title, pages.

**Why.** Trust is OpenApex's product — platforms embed this library only if the
science is verifiable line by line. Citations are also the legal shield: they
prove we implement public literature, not a competitor's proprietary score.

**Apply.**
- Good: `Banister, E.W. (1991). "Modeling Elite Athletic Performance." In
  Physiological Testing of the High-Performance Athlete (2nd ed.), pp. 403-424.`
- Not enough: "based on TRIMP", a blog URL, "the well-known formula".
- Cannot cite it? Do not write it — open an issue instead.
