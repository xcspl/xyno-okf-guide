---
type: Investigation
title: Evolution of the house standard
description: History of the guide itself — what changed, when, why, and what
  is still open.
tags: [okf, meta, design, standard]
timestamp: '2026-09-27'
status: active
sources:
  - resource: okf-guide.md
  - resource: okf-validate.py
---

# Evolution of the house standard

This doc is the history of the house standard: what changed, when, and
why, plus the questions still open. One `##` entry per change, newest
first. Each entry opens with a summary of what changed, then gives the
reasoning and the alternatives rejected. Git history covers the
line-level detail, so this repo keeps no separate `log.md`. When a
single rationale outgrows an entry, split it into a `Decision` doc
under `decisions/` and link it from here.

# Open questions

- **Upstream v0.2 alignment.** Upstream v0.2 superseded `timestamp`
  with `generated: {by, at}` and moved the `# Citations` body list
  into `sources`. The guide still requires `timestamp`, still
  recommends `# Citations`, and wrongly calls v0.2 backward-compatible.
  Planned: accept either date field but never both; agents migrate
  flagged docs, taking the author from git history and asking when
  unsure; re-checks without changes go to `verified`.
- **Scope.** Need-to-know access for docs and directories. Design
  agreed in discussion (2026-09-13 to 2026-09-27), not yet written
  into the guide:
  - *Existence is open, content is scoped.* Frontmatter is visible to
    the whole bundle, so a scoped doc's title and description must be
    safe for everyone who can see the bundle. Only the body is scoped.
  - *Two keys, one shape.* `scope` governs reading and `write_scope`
    writing. Each holds `labels` (compartments, reader needs any one)
    and `level` (a set of allowed reader levels, as `allow` or `deny`
    lists or ranges). `scope: [a, b]` is shorthand for labels only.
    A reader holds many labels but exactly one level.
  - *Writers must be readers.* A writer passes both `scope` and
    `write_scope`. With no `write_scope`, every reader may write.
    Append-only (write without read) is not supported.
  - *Defaults.* No scope means open to everyone, unknown readers
    included. A declared rule fails closed for a reader who hasn't
    stated labels or level, deny lists included.
  - *Stacking.* Declarations intersect down the path from bundle root
    to doc, for both keys. A doc can tighten its directory, never
    loosen it. Directory rules live in the root index; the registry
    declares the labels and the range and meaning of levels.
  - *Out-of-scope is reported, not hidden.* Agents tell the user what
    exists and which scope it needs. Harnesses return a structured
    out-of-scope error naming the path and requirement.
  - *Three tiers.* 1: agents follow the guide (best effort; ask the
    user's scope on first contact with scoped content). 2: harnesses
    enforce from real identity at the filesystem view, not just the
    tool layer. 3: separately permissioned repos, linked by visible
    pointers that declare the target's scope. Choose by what a leak
    would cost.
  - *No write-down.* Content never moves from a narrower audience to a
    wider one: across repos, or within a bundle via `sources` (a doc
    must be at least as tight as every scoped doc it derives from).
    An answer drawing on several docs may go only to readers of all
    of them.
  - *Known limits.* A harness must hide git history, which otherwise
    exposes every scoped file; tightening a scope later doesn't hide
    old versions (retroactive secrecy needs a repo split). Scope is
    only as trustworthy as write access, so loosening needs review and
    the root index needs a tight `write_scope`. Git hosts can enforce
    write rules per path (code owners plus required review); mirror
    `write_scope` there for hard-scoped content.
  - *One doc, one scope.* No per-paragraph marking; split mixed docs.

# Timeline

## 2026-09-27 — house 0.3: root index as entry contract, self-hosting

**What changed.**

- Root `index.md` frontmatter carries `house_version` and a mandatory,
  canonical `handling` block: the bundle's entry contract for agents.
- Bundle roots may hold two non-conformant entry files: `README.md` for
  humans and `AGENTS.md` for agents. Tool files like `CLAUDE.md` only
  as pointers to `AGENTS.md`.
- No content lives under a dot-name; dot-paths are ignored.
- This repo became a pure knowledge dir: `index.md`, `AGENTS.md`, and
  this doc added; the README changelog moved here.
- The validator checks all of the above.

**Problem.** The guide is the rulebook, but nothing guaranteed an agent
ever read it. Tool-specific files live outside the bundle and differ
per harness. The one file every agent reads first is the bundle root
`index.md`, because that is how progressive disclosure works. OKF
exists to make knowledge cheap for agents to find and safe to use, so
the bundle itself should tell agents how to handle it.

**Decisions.**

1. *The root index is the bundle's entry contract.* Its YAML
   frontmatter carries a mandatory `handling` list: canonical lines,
   defined per `house_version`, checked verbatim by the validator.
   YAML was chosen over a body block so one parse gives a harness
   everything, the body stays a clean table of contents, and drift is
   a structured comparison rather than a prose diff.
2. *Optional clauses appear only when used.* Future features add their
   own canonical clause, present if and only if the bundle uses the
   feature, so bundles that don't use it look exactly as before.
3. *Local rules go in a linked Playbook* named by `local_rules`, so the
   canonical block stays verbatim-checkable.
4. *The `handling` block is a prompt-injection surface.* A harness
   honours only lines that match the registry's canonical text for the
   declared `house_version`; other prose in the head is informational.
5. *`house_version` is separate from `okf_version`.* The README had
   used "v0.2" for both. The house standard now numbers itself so the
   validator knows which canonical text to expect.
6. *This repo dogfoods the standard.* It is a pure knowledge dir: root
   `index.md` with the entry contract, and this doc for history and
   rationale. Two more docs were drafted and dropped. A `log.md`: git
   already records what changed, and a digest beside this timeline
   meant recording every change twice. A `Script` companion doc for
   the validator: guide §9 already describes and links it, so the
   companion only restated the guide.
7. *Two root entry files, one per audience.* `README.md` is a concise
   human introduction; `AGENTS.md` is the fuller AI-oriented briefing,
   which may expand on `handling` but never contradict it. Tool files
   like `CLAUDE.md` are tolerated only as one-line pointers to
   `AGENTS.md`. Every other `.md` follows the YAML schema. An earlier
   draft allowed all three files as bare pointers; that left agents
   without a place for working procedures and left humans with a
   README that had to serve both audiences.
8. *No content under dot-names.* Tool worktrees, caches, and `.git` can
   sit inside a bundle root and hold `.md` files. Content directories
   and docs must not start with a dot, and every consumer ignores
   dot-paths.

**Rejected.** A reserved body heading (`# Handling`): harder to check,
and it clutters the human view. Carrying the contract in `AGENTS.md`
alone: prose can't be checked verbatim, and not every tool reads it.

## 2026-08-09 — README refresh

README brought in line with house 0.2: v0.2 vocabulary, mandatory
`timestamp` and `status`, the 12 base types, and the `sources` rename.
No rule changes.

## 2026-08-03 — house 0.2: adopt upstream OKF v0.2

Upstream added a trust vocabulary (`sources` as provenance objects,
`generated`, `verified`, `stale_after`, `usage_window`). Adopted with
upstream meanings after a same-day reserve-only review. The house
`derived_from` key was retired in favour of `sources`; `status` kept
the five-value house vocabulary because `draft | stable | deprecated`
cannot express `superseded` or `reverted`. `timestamp` and `status`
became mandatory-even-if-empty keys to make knowledge decay visible.

## 2026-07-12 — house 0.1: initial standard

Guide, reference validator, README. Fixed the choices the spec leaves
open: two directory classes, house frontmatter schema, 12 base types,
three linking rules, write-path sync, a workspace registry, bootstrap
recipe, mechanical validation.

# Citations

1. OKF v0.2 spec — <https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>
