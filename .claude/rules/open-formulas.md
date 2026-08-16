---
paths:
  - "src/openapex/**"
  - "docs/**"
  - "README.md"
---

# Rule: open lineage only — no proprietary or trademarked formulas

**Rule.** Never implement, or name anything after, reverse-engineered
proprietary metrics: TSS®, NP®, IF®, rTSS, hrTSS, Stryd or WKO models.
Implement the published lineage instead (Banister TRIMP, Foster
monotony/strain, Critical Power…) under open, descriptive names.

**Why.** Those names are trademarks and their exact formulas trade secrets —
shipping look-alikes invites legal risk and betrays the mission. "Open
alternatives to TSS" is also the community's most-requested feature: the open
equivalent IS our differentiation, a clone would erase it.

**Apply.**
- If a user or issue asks for "TSS support", implement/point to the open
  equivalent and explain the substitution in one sentence.
- Trademarked names never appear in identifiers, docstrings or docs, except to
  say we do not implement them.
