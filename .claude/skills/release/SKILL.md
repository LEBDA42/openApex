---
name: release
description: Publish an OpenApex release to PyPI. Carries the publishing truth — versioning, tagging, trusted publishing pipeline, verifications.
disable-model-invocation: true
---

# Releasing OpenApex

Publishing is human-initiated only. Facts of the pipeline:

- Remote: https://github.com/LEBDA42/openApex — history is append-only, never
  force-push (a PreToolUse hook blocks it).
- PyPI publishing uses **trusted publishing** (OIDC): a GitHub release triggers
  `.github/workflows/publish.yml`, which builds and uploads. No tokens anywhere.
- The workflow's `publish` job runs in the GitHub environment **`pypi`** — it
  must exist in the repo settings, and the PyPI trusted-publisher entry must
  match owner `LEBDA42`, repo `openApex`, workflow `publish.yml`, env `pypi`.
- Maintainer commits use the identity already configured in `.git/config`
  (`LEBDA42 <LEBDA42@users.noreply.github.com>`) — never a personal or
  corporate email.

## Steps

1. Three gates green (commands in AGENTS.md). CI green on `main`.
2. Bump `version` in `pyproject.toml` (PEP 440; pre-1.0, breaking changes noted
   in the commit body). Commit: `Release X.Y.Z`.
3. Sanity-build locally: `.venv\Scripts\python.exe -m build` then
   `.venv\Scripts\twine.exe check dist\*` → both PASSED.
4. Push, then create the GitHub release: tag `vX.Y.Z` on `main`, release notes
   = what changed and why. Mark pre-releases (`.devN`, `aN`, `rcN`) as
   "pre-release".
5. Watch the `Publish to PyPI` workflow run; on success verify
   https://pypi.org/project/openapex/ shows the new version.
6. If the upload fails, fix and publish a **new** patch version — never delete
   or reuse a version number.
