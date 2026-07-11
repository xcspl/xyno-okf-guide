# OKF House Standard

A workspace-portable standard for keeping project knowledge as plain
markdown, built on the [Open Knowledge Format (OKF) v0.1
spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).

OKF itself standardizes almost nothing on purpose: markdown files with
YAML frontmatter, one required key (`type`), reserved `index.md` /
`log.md`, links as relationships. **This guide pins down everything the
spec leaves open** so that every project in a workspace speaks the same
dialect: directory classes, a house frontmatter schema, a type
vocabulary (open-ended by rule), linking and tiering rules, write-path
sync, a workspace registry, a bootstrap recipe, and mechanical
validation.

## Contents

- **[okf-guide.md](okf-guide.md)** — the standard. Start here.
- **[okf-validate.py](okf-validate.py)** — reference validator
  (`python3 okf-validate.py <bundle-root>`; needs PyYAML). Exits
  nonzero on standard violations; broken concept links and style drift
  are warnings only.

## Adopting in a workspace

1. Designate your workspace root (the directory that holds your project
   dirs). Its `okf/` bundle is the **registry** (guide §8).
2. Drop `okf-guide.md` into the registry unchanged, listed as a
   `Playbook` in the registry's root `index.md` (which carries
   `registry: true`).
3. Convert directories as needed using the bootstrap recipe (guide §7),
   validating with `okf-validate.py` (guide §9).

Workspace-local type additions are expected (guide §3) — edit your
registry's copy of the guide through whatever review your workspace
normally uses. The guide is phrased structurally, so no deployment's
copy is privileged.
