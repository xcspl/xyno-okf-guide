# Log

History of the house standard, newest first. Each entry gives when (its
date heading), what changed, and optionally why.

## 2026-09-27

**Update: `evolution.md` becomes `log.md`.**

**What.** `evolution.md` renamed to the reserved `log.md`, with its
frontmatter removed as the spec requires for log files. Guide §5 now
defines `log.md` as when, what, and optionally why, not a terse
digest, and adds `open-questions.md` as an optional convention for
work that is undecided or not yet done. This repo keeps none: its two
open items, upstream v0.2 alignment and scope, are decided and land
next. The full scope design is in `evolution.md` at commit 28d3f4e.

**Why.** `log.md` is the spec's reserved file for a bundle's change
history, and `evolution.md` was a house invention doing the same job.
Spec log entries are prose, so an entry can carry its reasoning. This
reverses the earlier decision to drop `log.md`: the objection was
recording every change twice, and with one file there is no second
copy.

**Update: house 0.3, root index as entry contract; this repo becomes its own bundle.**

**What.**

- Root `index.md` frontmatter carries `house_version` and a mandatory,
  canonical `handling` block: the bundle's entry contract for agents.
- Bundle roots may hold two non-conformant entry files: `README.md` for
  humans and `AGENTS.md` for agents. Tool files like `CLAUDE.md` only
  as pointers to `AGENTS.md`.
- No content lives under a dot-name; dot-paths are ignored.
- This repo became a pure knowledge dir: `index.md`, `AGENTS.md`, and
  `evolution.md` added; the README changelog moved there.
- The validator checks all of the above.

**Why.** The guide is the rulebook, but nothing guaranteed an agent
ever read it. Tool-specific files live outside the bundle and differ
per harness. The one file every agent reads first is the bundle root
`index.md`, because that is how progressive disclosure works. OKF
exists to make knowledge cheap for agents to find and safe to use, so
the bundle itself should tell agents how to handle it.

Decisions:

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
   `index.md` with the entry contract, and `evolution.md` for history
   and rationale. Two more docs were drafted and dropped. A `log.md`: git
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

Rejected: a reserved body heading (`# Handling`): harder to check,
and it clutters the human view. Carrying the contract in `AGENTS.md`
alone: prose can't be checked verbatim, and not every tool reads it.

## 2026-08-09

**Update: README refresh.**

**What.** README brought in line with house 0.2: v0.2 vocabulary, mandatory
`timestamp` and `status`, the 12 base types, and the `sources` rename.
No rule changes.

## 2026-08-03

**Update: house 0.2, adopt upstream OKF v0.2.**

**What.** Upstream
([spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md))
added a trust vocabulary (`sources` as provenance objects,
`generated`, `verified`, `stale_after`, `usage_window`). Adopted with
upstream meanings after a same-day reserve-only review. The house
`derived_from` key was retired in favour of `sources`; `status` kept
the five-value house vocabulary because `draft | stable | deprecated`
cannot express `superseded` or `reverted`. `timestamp` and `status`
became mandatory-even-if-empty keys to make knowledge decay visible.

## 2026-07-12

**Creation: house 0.1, initial standard.**

**What.** Guide, reference validator, README. Fixed the choices the spec leaves
open: two directory classes, house frontmatter schema, 12 base types,
three linking rules, write-path sync, a workspace registry, bootstrap
recipe, mechanical validation.
