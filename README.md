# OKF House Standard

A shared standard for keeping project knowledge as plain markdown that
people and AI agents can both navigate. It builds on the [Open
Knowledge Format (OKF)
spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md),
which deliberately standardizes very little, and settles everything the
spec leaves open: where knowledge lives, what frontmatter every doc
carries, how docs are typed and linked, how bundles stay in sync, and
how a whole workspace of projects fits together.

**House version 0.3**, on top of OKF v0.2.

## What's here

- **[okf-guide.md](okf-guide.md)**: the standard. Start here.
- **[okf-validate.py](okf-validate.py)**: checks a bundle against the
  standard. Run `python3 okf-validate.py <bundle-root>`; needs PyYAML.
- **[log.md](log.md)**: what changed, when, and why.

This repo follows its own standard, so it doubles as a worked example.
AI agents should read [AGENTS.md](AGENTS.md).

## Adopting it

1. Pick your workspace root, the directory holding your projects. Its
   `okf/` directory becomes your **registry**.
2. Copy `okf-guide.md` into the registry unchanged.
3. Convert projects one at a time with the guide's bootstrap recipe,
   and run the validator on each.

Workspaces are expected to extend their copy, for example with their
own document types.

## Known adoptions

Private or internal bundles that follow this standard:

- **sumanta-okf**: personal knowledge.
- **xynocast-okf**: primary corporate knowledge.
- **neet-astro**: a project repo with an OKF-styled docs bundle.

Adopted it too? Send a PR adding your bundle once it validates.
