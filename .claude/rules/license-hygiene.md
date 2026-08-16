---
paths:
  - "src/**"
  - "tests/**"
---

# Rule: Apache-2.0 stays clean — never copy GPL/AGPL code

**Rule.** Never copy, translate or closely paraphrase code from GPL/AGPL
projects. GoldenCheetah (GPL-2.0) is the chief temptation: read the papers it
cites, never its source.

**Why.** The permissive Apache-2.0 license is OpenApex's adoption weapon —
platforms embed us because they can. A single copied GPL snippet contaminates
the whole library and destroys that strategy.

**Apply.**
- Allowed: reading published papers, reimplementing math from the literature,
  reading GPL projects' *documentation of which papers they use*.
- Forbidden: porting GPL source line by line, lifting constant tables that have
  no published origin, "just adapting" a GPL function.
- Unsure where a formula's constants come from? Track down the paper first.
