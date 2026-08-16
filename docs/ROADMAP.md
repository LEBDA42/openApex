# Roadmap

Order of battle — each stage builds on the previous one.

1. **Real FIT fixtures & `read_fit` hardening** — multi-session files, pauses,
   developer fields, smart recording. Anonymized fixtures in `tests/fixtures/`.
2. **Banister impulse-response model** → fitness/fatigue/form curves. The
   flagship feature; what the project will be judged on.
3. **Threshold estimation** from the literature (Critical Power model,
   eFTP-style estimates under open names).
4. **Race prediction** (Riegel, VDOT, CP-based).
5. **`openapex-mcp` satellite** — expose activities and metrics to AI agents.

Satellite packages use the French endurance lexicon: `openapex-seuil`
(thresholds), `openapex-forme` (fitness/fatigue/form), `openapex-cadence`,
`openapex-allure` (pacing), `openapex-tempo` (planning).
