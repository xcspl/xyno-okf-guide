# OKF House Standard

A workspace-portable standard for keeping project knowledge as plain
markdown, built on the [Open Knowledge Format (OKF) v0.2
spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).

This guide **adopts OKF v0.2 upstream** (2026-08-03) and pins down all
the choices the spec deliberately leaves open — directory classes, a
house frontmatter schema, a 12-type base vocabulary, linking and
tiering rules, write-path sync, a workspace registry, a bootstrap
recipe, and mechanical validation. The `status` field keeps a
five-value house vocabulary (§2) because upstream's `draft | stable |
deprecated` cannot express the distinctions we need; the v0.2
`sources` field (now a list of provenance objects) replaces the v0.1
house `derived_from` key.

OKF itself standardizes almost nothing on purpose: markdown files with
YAML frontmatter, one required key (`type`), reserved `index.md` /
`log.md`, links as relationships. **This guide pins down everything the
spec leaves open** so that every project in a workspace speaks the same
dialect.

## Contents

- **[okf-guide.md](okf-guide.md)** — the standard. Start here.
- **[okf-validate.py](okf-validate.py)** — reference validator
  (`python3 okf-validate.py <bundle-root>`; needs PyYAML). Exits
  nonzero on standard violations; broken concept links and style drift
  are warnings only.

## The 12 base types

The default type vocabulary (workspaces may extend — see guide §3):

| Type | Use for |
|---|---|
| `Note` | General knowledge that fits nothing more specific. |
| `Decision` | A choice made, its alternatives, and why. |
| `Investigation` | A saga/debugging trail with timeline, evidence, and open/closed state. |
| `Playbook` | Step-by-step procedure to execute on demand (this guide is one). |
| `Reference` | Distilled external material; pointers to docs, articles, specs. |
| `Config` | Current-truth description of a configuration/state (`resource` → the file). |
| `Script` | Companion doc for an executable (`resource` → the script). |
| `Service` | A running service/daemon/container and its operational knowledge. |
| `Hardware` | A physical component and its history. |
| `Asset` | A data/media collection (datasets, image/video libraries). |
| `Change Record` | Historical record of a change made (what/why/commands/revert). |
| `Project` | A unit of work — its own bundle, with its own `index.md`. |

## Minimum frontmatter

Every doc must have (guide §2):

```yaml
---
type: <one of the 12, or your workspace extension>
title: <short, human-readable>
description: <one-sentence summary>
timestamp: <YYYY-MM-DD of last meaningful edit>   # mandatory
status: <active | dormant | in-progress | archived | rejected>   # mandatory
---
```

Plus, on a bundle root `index.md` (guide §1):

```yaml
okf_version: "0.2"
bundle: <work-dir | knowledge-dir>
```

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

## Known adoptions

Public bundles known to follow this house standard:

- [sumanta-okf](https://github.com/sumantagogoi/sumanta-okf) — personal
  OKF (philosophy, projects, finance, wedding plan).
- [xynocast-okf](https://github.com/xynocast/xynocast-okf) — primary
  corporate OKF (XCSPL, XFPL, partners, compliance, SOPs).
- [neet-astro](https://github.com/xcspl/neet-astro) — project repo with
  OKF-styled `docs/` and site modules (Astro + Cloudflare R2).

> Open a PR to add your bundle if it follows this standard.

## Changelog

- **2026-08-09** — README refreshed: adopt OKF v0.2 vocabulary, mandate
  `timestamp` and `status` in frontmatter, list 12 base types, surface
  the `sources` (was `derived_from`) shift. Rebased on top of three new
  upstream commits.
- **2026-08-03** — upstream OKF v0.2 adopted (`ed8bba0`,
  `6647e39`, `0b0ea88`).
- **2026-07-12** — initial house standard v0.1 (guide, validator,
  README).
