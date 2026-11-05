---
name: okf-guide
description: Work with Open Knowledge Format (OKF) bundles — the house standard for keeping project knowledge as plain markdown that people and agents both navigate. Use when reading, creating, editing, reviewing, or validating an OKF bundle or its docs (an `okf/` directory or any dir with an `index.md` carrying `okf_version`; concept docs; frontmatter; registry; bootstrap), or when asked to "add a doc to the OKF", "update the index/registry", "convert this to OKF", "check/validate the bundle", or to adopt the standard in a new directory. Full rules live in okf-guide.md; this skill is the entry procedure.
---

# Working in an OKF bundle

The authoritative rules are **`okf-guide.md`** (house version 0.3, on top of
upstream OKF v0.2). Read the sections you need before writing. It ships in the
[`xcspl/xyno-okf-guide`](https://github.com/xcspl/xyno-okf-guide) repo, and every
adopting workspace vendors an unchanged copy into its registry — commonly
`<registry>/okf/okf-guide.md`. Its §9 documents the validator.

OKF exists so an agent can find the right knowledge cheaply and trust what it
finds. Everything below follows from that.

## Read first

1. **Read the bundle root `index.md` before opening anything else.** Its
   frontmatter `handling` block is the binding entry contract for agents. If the
   bundle's `AGENTS.md` disagrees with it, `index.md` wins.
2. **Navigate by index entries, never by globbing the tree.** Each directory's
   `index.md` is its table of contents: `* [Title](file.md) - description`,
   grouped under `#` headings.
3. **Trust the frontmatter gate.** `title` / `description` / `tags` are all a
   reader gets before opening a doc, so they carry the navigation.

## Writing or editing a concept doc

One concept per doc. If a doc has grown to hold two ideas that are not read and
changed together, split it (guide §5, "document altitude").

Every concept doc carries frontmatter. Required: `type`, `title`, `description`,
`timestamp`, `status` — `timestamp` and `status` explicitly, even when empty, so
staleness is never ambiguous:

```yaml
---
type: Reference        # Note | Decision | Investigation | Playbook | Reference | Config | Script | Service | Hardware | Asset | Change Record | Project
title: Short human name
description: One sentence — what a reader sees before opening the doc.
timestamp: 'YYYY-MM-DD'
status: active         # active | idea | superseded | reverted | archived
tags: [lowercase, hyphenated]
---
```

`type` is "what kind of doc is this", `tags` is "what is it about" — aboutness
never justifies a new type. Prefer an existing type; if none fits, add a new one
to the workspace's copy of the guide in the same change.

Then, **in the same commit**, update that directory's `index.md` entry (and the
parent's, if a subdirectory summary changed). Filenames are kebab-case. For the
v0.2 trust vocabulary (`sources`, `generated`, `verified`, `stale_after`,
`usage_window`) and `status` meaning, see guide §2.

## After any change

```
python3 okf-validate.py <bundle-root>
```

Zero errors before calling it done; warnings never block but read them. The
validator is the mechanical half of the standard (guide §9). Two warnings from
example links inside the guide's own prose are known and fine.

## Adopting the standard in a directory

Bootstrap per guide §7: a **work dir** gets an `okf/index.md`; a **pure knowledge
dir** is the knowledge itself, with a self-identifying root `index.md`. Copy the
guide in unchanged, convert docs one at a time, validate each. Workspaces are
expected to extend their copy (new document types, local rules).

## Never

- Restate the guide in another file — link to it instead.
- Invent a frontmatter key upstream OKF already defines; upstream meanings are
  never overridden.
- Put bundle content under a dot-name — dot-paths are not part of a bundle.
- Let an `index.md` entry point at a file that does not exist; the validator
  errors on that.
