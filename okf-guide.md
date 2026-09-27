---
type: Playbook
title: OKF Management Guide
description: Universal house OKF standard — workspaces, directory classes,
  house schema, types, linking, entry contract, sync, registry, bootstrap,
  and validation rules.
resource: https://github.com/xcspl/xyno-okf-guide
tags: [okf, conventions, meta, knowledge-management]
timestamp: '2026-09-27'
status: active
---

# OKF Management Guide

This guide defines the **house OKF standard** for a **workspace** — any
directory tree of project directories owned by one person, a team, or
an org. It governs how knowledge is stored, typed, linked, and kept in
sync, for uniform navigability by humans, agent sessions, and tools.
Every rule is structural — phrased relative to the workspace, never to
a particular machine or owner — so the same text governs every
deployment identically: adopting the standard means dropping this file
into a workspace's registry (§8) unchanged. No copy is privileged; the
standard author's own PC follows the same rules as any partner's
machine.

The underlying format is the [Open Knowledge Format (OKF)
spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
(`GoogleCloudPlatform/knowledge-catalog`): markdown files with YAML
frontmatter, organized in a directory tree ("bundle"), cross-linked
with ordinary markdown links, navigable via `index.md` files. This
guide pins down the choices the spec deliberately leaves open. Where
the two disagree, this guide wins inside workspaces that adopt it; the
spec's *consumption* rules (tolerate unknown types, broken links, extra
keys) always apply.

**Upstream alignment: this standard adopts OKF v0.2** (adopted
2026-08-03, after an initial reserve-only review the same day). v0.2 is
additive and backward-compatible with v0.1. Two positions follow from
adoption:

- Bundles declare `okf_version: "0.2"` (§1), asserting use of the v0.2
  **trust vocabulary** with upstream meanings — see §2. The former
  house key `derived_from` is retired; its role is carried by upstream
  `sources` (each entry's `resource` is the staleness hook, §6).
- `status` keeps the house five-value vocabulary (§2), which encodes
  distinctions upstream's `draft | stable | deprecated` cannot express.
  Unknown `status` values are tolerated by the spec; the export mapping
  is documented in §2.

**This standard is published at
<https://github.com/xcspl/xyno-okf-guide>**, alongside its reference
validator
([`okf-validate.py`](https://github.com/xcspl/xyno-okf-guide/blob/main/okf-validate.py))
and an adoption README. That repo is the shared distribution point —
if you were handed only this file, everything else lives there. It is
not a privileged deployment: workspaces vendor this file into their
registry (§8) and may extend their copy (§3).

**House version: 0.3.** The house standard numbers itself independently
of upstream — every bundle root index carries `house_version` (§1) —
because it adds rules upstream does not have, chiefly the entry
contract (§5), and the validator must know which canonical text to
expect. Each change, and the reasoning behind it, is
recorded in [evolution.md](/evolution.md).

---

## 1. Directory classes

Every directory OKF cares about is one of two classes:

### Work dir
An active project producing something — code, images, video, documents.

- Knowledge lives in a bundle subdirectory named **`okf/`**
  (recommended; detection rule 2 below is the tolerated escape hatch
  for nonstandard names).
- A work dir has **exactly one bundle**. If knowledge wants to split,
  tier inside the bundle (§5) — never add a second bundle.
- **Only OKF-conformant files** live inside the bundle. Everything
  outside it is unregulated (READMEs, code docs, vendored files — no
  rules).
- The bundle is a **parallel knowledge layer** about the project:
  decisions, gotchas, sagas, operational knowledge. **Reference, don't
  restate** — link to the source of truth (code, README, config); only
  write what the repo can't say itself.

Example: a system-scripts repo (admin scripts, changelogs, package
logs) is a work dir — its bundle is `okf/`; the scripts and logs stay
exactly as they are.

### Pure knowledge dir
The directory *is* knowledge (notes collections, wikis). The **whole
directory is the bundle**; every `.md` in it is conformant. The
directory may be named anything — the class is declared by
self-identification, not by name.

### Self-identification

Every bundle root has an `index.md` whose frontmatter declares the
bundle (the only place the spec permits frontmatter in an `index.md`):

```yaml
---
okf_version: "0.2"
house_version: "0.3"
bundle: <dir-name>
handling:            # canonical entry contract for agents — §5
  - Read this index before opening any doc in this bundle.
  - Navigate by index entries; never glob the tree.
  - A write to any directory updates that directory's index.md in the same commit.
  - Full rules live in okf-guide.md in the workspace registry (Playbook at its bundle root).
---
```

`house_version` names the version of *this* standard the bundle
follows; `handling` is the mandatory entry contract for agents, whose
canonical lines and optional clauses are defined in §5. The workspace
registry's root index additionally carries `registry: true` (§8).

**Root entry files.** A bundle root may hold two non-conformant entry
files, one per audience:

- **`README.md` is for humans.** A concise introduction: what the
  bundle is, who it is for, where to start. Git hosting renders it.
- **`AGENTS.md` is for agents.** A fuller, AI-oriented briefing: what
  OKF is, how to navigate and write in this bundle, how to validate,
  and any bundle-specific working procedures. It may restate the
  `handling` block (§5) in prose and expand on it, but it never
  contradicts it — `index.md` frontmatter stays the binding contract.

Tool-specific files (`CLAUDE.md` and the like) are tolerated only as
one-line pointers to `AGENTS.md`, for tools that do not read it
natively. None of these are concept docs, and none are listed in an
index. Every other `.md` file in a bundle is a conformant concept doc
(or a reserved `index.md` / `log.md`).

**Content never lives under a dot-name.** No directory or file inside a
bundle whose name starts with a dot is part of the bundle: content
directories and concept docs MUST NOT be named that way. Dot-paths
(`.git`, tool worktrees, caches, editor state) are ignored by agents,
harnesses, and the validator alike.

Detection rule for any directory, in precedence order:

1. `okf/index.md` exists → **work dir** (bundle = `okf/`).
2. Its `AGENTS.md`, `CLAUDE.md`, or `README.md` contains a line of the exact form
   `OKF bundle: <relative-path>` → **work dir** with a nonstandard
   bundle location (tolerated, not recommended). The target must still
   self-identify per above — the declaration is a discovery aid, never
   the authority.
3. Root `index.md` carries `okf_version` frontmatter → **pure
   knowledge dir**.
4. None → **not yet converted**.

---

## 2. House schema

Stricter than the spec (which requires only `type`). Every concept doc
carries:

**Required frontmatter:**

| Key | Meaning |
|---|---|
| `type` | Kind of document — see §3. |
| `title` | Human-readable display name. |
| `description` | One sentence; used by indexes, search, previews. |
| `timestamp` | ISO 8601 date(-time) of last meaningful change/verification. |
| `status` | Lifecycle state — `active` \| `idea` \| `superseded` \| `reverted` \| `archived`. |

> **Explicit `timestamp` and `status` rule:**
> Knowledge decay is a primary cause of stale, unmaintained, or misleading
> documentation. To prevent outdated knowledge files from masquerading as
> current truth, **every concept doc MUST explicitly include both `timestamp`
> and `status` keys in its YAML frontmatter, even if empty** (e.g., `timestamp:`
> or `status:` when pending initial date or status assignment). `timestamp`
> records when the content was created or last verified, while `status`
> records its lifecycle state. Explicit keys ensure that recency and validity
> are never ambiguous to readers or automated agent sessions.

**Optional but standardized (use these names, not variants):**

| Key | Meaning |
|---|---|
| `tags` | YAML list; cross-cutting subjects ("what is it about"). |
| `resource` | URI/path of the underlying asset the doc describes. |
| `sources` | v0.2 provenance: YAML list of *objects*, each with required `resource` plus optional credibility signals — the staleness hook (§6). See below. |
| `generated` / `verified` / `stale_after` / `usage_window` | v0.2 trust keys, upstream meanings — see below. |

Extra keys are always allowed (the spec guarantees consumers tolerate
them). If a new key proves broadly useful, promote it into this table.

### Upstream v0.2 trust vocabulary — adopted

OKF v0.2 added a *trust vocabulary* — provenance, lifecycle, and
attestation fields — on top of v0.1. This standard **adopts it with
upstream meanings** (adopted 2026-08-03). All trust keys are optional
per doc; when present they MUST carry the upstream meaning — never a
house meaning.

**`sources` — provenance as a list of objects.** Each entry records
material the concept derives from: a required `resource` plus optional
`id`, `title`, `author`, `usage_count`, and `last_modified`. The extra
keys are credibility signals: v0.2 deliberately publishes signals
rather than a computed score, leaving consumers to judge
trustworthiness themselves. `resource` may be a URL or a repo path —
repo-path entries drive the staleness query (§6 rule 3).

```yaml
# upstream v0.2 shape — a list of objects
sources:
  - id: ga4-schema
    resource: https://developers.google.com/analytics/bigquery/export-schema
    title: GA4 BigQuery Export schema
    author: team:ga4-docs
    last_modified: 2026-05-30
  - resource: ~/xynocast-okf/company/overview.md   # repo path → staleness hook
```

History: before adoption this standard used a flat string list for the
same intent, briefly renamed `derived_from` to avoid clashing with the
upstream shape. Both forms are retired — docs were migrated to the
object shape; if a stray flat list or `derived_from` key surfaces,
migrate it on touch (`- <path>` → `- resource: <path>`).

The other trust keys: `generated: {by, at}` and `verified: [{by, at}]`
record who produced or confirmed content and when; `stale_after:
YYYY-MM-DD` declares an absolute expiry (a concept is stale when today
>= that date); `usage_window` bounds the period the content is intended
to be used within.

**`status` — same key, house vocabulary kept.** v0.2 defines `status` as
`draft | stable | deprecated`. This standard keeps its own five values
(§2 above), which encode distinctions upstream cannot express —
`superseded` and `reverted` are not the same event as `deprecated`, and
`superseded` carries a linking obligation (§6 rule 4). Unknown `status`
values are tolerated by the spec, so this costs no conformance. The
rough mapping, if a bundle is ever exported upstream: `idea`→`draft`,
`active`→`stable`, `superseded`/`reverted`/`archived`→`deprecated`.

**Naming conventions:**

- Concept filenames are **kebab-case** (`asus-mic-adapter.md`, not
  `AsusMicAdapter.md` or `asus_mic_adapter.md`).
- Tags are **lowercase**, hyphenated when multi-word
  (`knowledge-management`), no plural/singular mixing — reuse an existing
  tag's exact form before minting a variant.

**Body conventions:** the spec's conventional headings apply — `# Schema`
(structured description of an asset), `# Examples` (fenced code blocks),
`# Citations` (numbered external sources, spec §8). In particular,
`Reference` and `Investigation` docs SHOULD list where their claims came
from under `# Citations`; a claim with no source is a claim future
readers can't verify.

---

## 3. Types

`type` answers **"what kind of document is this?"** — two docs share a type
when they are *read and handled* the same way. `tags` answer **"what is it
about?"**. Aboutness never justifies a new type.

Default vocabulary:

| Type | Use for |
|---|---|
| `Note` | General knowledge that fits nothing more specific. |
| `Decision` | A choice made, its alternatives, and why. |
| `Investigation` | A saga/debugging trail with timeline, evidence, and open/closed state (drive `status`). |
| `Playbook` | Step-by-step procedure to execute on demand (this guide is one). |
| `Reference` | Distilled external material; pointers to docs, articles, specs. |
| `Config` | Current-truth description of a configuration/state (`resource` → the file). |
| `Script` | Companion doc for an executable (`resource` → the script). |
| `Service` | A running service/daemon/container and its operational knowledge. |
| `Hardware` | A physical component and its history. |
| `Asset` | A data/media collection (datasets, image/video libraries). |
| `Change Record` | Historical record of a change made (what/why/commands/revert). |
| `Project` | A project directory as a whole (`resource:` → its path) — what it is, stack, remotes, sub-repos. Lives in the registry (§8). |

> **This list is a default vocabulary, not a cage.** If no existing type
> genuinely fits, create an apt new one and add it to the workspace's
> copy of this guide in the same change — through whatever review that
> workspace's files normally get (solo: direct commit; team: the usual
> PR). Never force information into an ill-fitting type — the
> information comes first, the vocabulary adapts to it.

---

## 4. Linking rules

Three kinds of links, three rules:

1. **Concept → concept (same bundle):** bundle-absolute paths —
   `[mic saga](/hardware/asus-mic-adapter.md)`, resolved from the bundle
   root. Stable under reorganization; preferred.
2. **Concept → project file (work dirs):** relative paths that step out of
   the bundle — `[the script](../script-network/zt-vpn-toggle.sh)`. These
   are *external references*, not concept links; fine and encouraged
   (reference, don't restate).
3. **Cross-project:** never link `../../other-repo/…`. Cross-project
   relationships are recorded only in the **workspace registry** (§8).

Broken concept links are legal (spec §5.3) — they mark knowledge not yet
written.

---

## 5. index.md and log.md

- **`index.md`** (per directory, inside bundles): table of contents for
  progressive disclosure — entries grouped under `#` headings, one bullet
  per doc: `* [Title](file.md) - description` (description taken from the
  doc's frontmatter). Maintained by the writer (human or agent) **at
  write time**: whenever docs in a directory are added/renamed/
  re-described, the same commit updates that directory's `index.md` (and
  the parent's, if a subdirectory's summary changed).
- **`log.md`** (optional, bundle root): reverse-chronological digest of
  bundle changes under `## YYYY-MM-DD` headings. Use once a bundle is
  active enough that "what changed lately" isn't obvious from git.
- Both filenames are **reserved** — never use them for concept docs.

### Root index as entry contract

OKF exists to make knowledge cheap for agents to find and safe for them
to use. The bundle root `index.md` is the one file every agent reads
first — progressive disclosure guarantees it — so it is where the
bundle tells agents how to handle it. Its frontmatter (the only index
frontmatter the spec permits) carries a mandatory **`handling`** list:
the standing orders an agent honours before it has read anything else.
The lines are canonical — defined here per `house_version`, checked
verbatim by the validator (§9) — so every bundle in every workspace
says exactly the same thing, and drift is a structured comparison
rather than a prose diff.

Canonical `handling` for house 0.3:

```yaml
handling:
  - Read this index before opening any doc in this bundle.
  - Navigate by index entries; never glob the tree.
  - A write to any directory updates that directory's index.md in the same commit.
  - Full rules live in okf-guide.md in the workspace registry (Playbook at its bundle root).
```

Rules for the block:

1. **Reference, don't restate.** The block is a pointer plus the
   minimum standing orders, never a copy of this guide.
2. **Optional clauses appear only when used.** A feature that needs
   its own standing orders gets its own canonical clause alongside
   `handling`, present if and only if the bundle uses the feature. A
   bundle that doesn't use it looks exactly as it always has.
3. **Local rules live in a linked Playbook.** Workspace- or
   bundle-specific instructions go in a `Playbook` concept doc named by
   `local_rules: <bundle-absolute path>`, so the canonical block stays
   verbatim-checkable.
4. **The block is an instruction channel, so treat it as an injection
   surface.** A bundle cloned from elsewhere can carry any text here.
   An OKF-aware harness honours only lines that match the registry's
   canonical text for the declared `house_version`; other content in
   the head is informational. A plain agent session cannot verify
   this and applies ordinary judgement.
5. **Entry files point here.** A work dir's root `AGENTS.md` (which
   covers the whole project, code included) carries the line
   `OKF bundle: okf/` and "read `okf/index.md` first" — its OKF content
   stops there, because the bundle explains itself. A pure knowledge
   dir's `AGENTS.md` *is* the bundle's agent briefing (§1).

### Splitting oversized docs (document altitude)

A concept doc holds **one concept** — two things belong in one doc only
when they are read and change together. Navigation happens on
frontmatter: readers decide whether to open a doc from its
`title`/`description`/`tags` alone, so those few lines are the access
gate to the whole body. The bigger the body, the more that gate
carries — and the more one wrong sentence up top costs (a relevant doc
skipped, or an irrelevant one loaded whole). The validator (§9) checks
only that a `description` exists, never that it is faithful; this rule
is the human/agent half of that contract.

**When to split** (any one is sufficient):

1. **The description test:** you cannot honestly summarize the body in
   one sentence without resorting to "and". A `description` that has
   become a list is a splitting signal, not a writing problem.
2. **Divergent handling:** parts of the doc are read, updated, or
   consulted on different occasions (e.g. a setup procedure fused with
   an incident history — one is a `Playbook`, the other an
   `Investigation`).
3. **Section-as-doc:** a `#`/`##` section has grown to where it would
   stand alone with its own type, description, and inbound links.

**How to split:**

1. Extract each concept into its own doc — faithful frontmatter, correct
   `type` (pieces of one doc often want *different* types),
   `sources` entries carried to whichever piece derives from them.
2. Decide the old path's fate: keep it as the dominant concept
   (slimmed), or delete it. Either way, splitting changes concept IDs —
   grep the bundle for the old path and update every inbound link **and
   the directory's `index.md` in the same commit** (same discipline as
   re-tiering rule 4 below).
3. If the split produces a themed cluster, that may in turn trigger
   tiering (below) — splitting and tiering are the same pressure at two
   altitudes: doc → docs, then docs → subdirectory.

**Exception — genuinely indivisible bodies** (a licence agreement, a
transcript, a long specification): don't force a split that destroys
the artifact's integrity. Instead treat it like an asset: make the
`description` an abstract of *coverage* ("covers X, Y, Z"), load `tags`
with every subject it touches, and if needed add a small companion map
doc that points into its sections. A large doc that must exist should
be reachable through a small, well-described one.

### Tiering: subdirectories for compartmentalized knowledge (optional)

Subdirectories are the compartmentalization mechanism — each level is
one tier of progressive disclosure. **They are entirely optional and
scenario-dependent:** a flat bundle is perfectly valid OKF, and most
bundles should stay flat until their content demands tiers. When a
bundle does grow into them:

1. **Start flat; subdivide on pressure, not upfront.** Create a
   subdirectory when a cluster of concepts shares an obvious theme *and*
   the flat index no longer scans well (rough trigger: a heading with
   ~7+ entries sharing a common theme). Don't pre-create empty tiers.
2. **A parent index never lists files inside a subdirectory.** It lists
   the subdirectory as a single entry — a link to the child's
   `index.md` plus a one-line summary of what lives below. The detailed
   listing belongs to the child. Each level owns exactly its own
   listing, so adding a doc touches only that directory's index.
3. **Descriptions roll up, listings don't.** The parent's one-line
   summary for a subdirectory is derived from the child's contents;
   when regenerating, work deepest-first so child summaries exist
   before parents need them.
4. **Re-tiering changes concept IDs.** A doc's ID is its bundle path,
   so moving it into a subdirectory breaks inbound links — grep the
   bundle for the old path and update every link in the same commit.

The payoff is that navigation cost stays flat as a bundle grows: a
reader (human or agent) loads one small index per hop — root index →
relevant subdirectory index → the one concept needed — never the whole
bundle. Both end states are legitimate: a small work-dir bundle (a
handful of concepts) stays flat; a workspace registry with many
`Project` docs tiers into group subdirectories, each summarized in one
line at its root index.

---

## 6. Maintenance & sync

The rot-prevention rules — these are in the write path, not periodic
chores:

1. **Same-commit sync:** a change that alters something an okf doc
   describes updates that doc *in the same commit*. **Exception —
   registry:** a `Project` doc in the workspace registry (§8) lives in
   a different repo than the project it describes, so same-commit is
   impossible; sync it in the same *sitting* instead, as its own commit
   in the registry's repo.
2. **Reference, don't restate:** the less a doc duplicates, the less can
   go stale. Docs carry the knowledge the project can't express (why,
   decisions, gotchas, relationships) and link to everything else.
3. **Staleness is a query, not a feeling:** a doc with `sources:` is
   stale if any repo-path `resource` changed (git log / mtime) after the
   doc's `timestamp`. Check per-repo when suspicious:
   ```
   git log --oneline --since=<doc timestamp> -- <each sources[].resource repo path>
   ```
   Any hits → review and refresh the doc (or mark it `status: archived`).
4. **Delete vs archive:** archive (`status: archived`) when the history
   has value; delete outright when it never did (drafts, duplicates,
   docs made wrong rather than obsolete). A doc marked `superseded` MUST
   link to its successor. Deleting or renaming a doc updates every
   inbound link and the directory's `index.md` in the same commit.

---

## 7. Bootstrap procedure (converting a directory)

Mechanical recipe, executable in any session:

1. **Classify** the dir: work dir or pure knowledge dir (§1).
2. **Create the bundle root** (`okf/` for work dirs) with its
   self-identifying `index.md` carrying `house_version` and the
   canonical `handling` block (§1, §5).
3. **Write concept docs** from existing material — README, docs, code
   layout, git history, changelogs. Obey reference-don't-restate; type per
   §3; house frontmatter per §2; set `sources:` on anything derived.
   Start small: only concepts with real content today.
4. **Build indexes** (§5) for every bundle directory.
5. **Validate** the bundle (§9) and fix every error.
6. **Register** the conversion in the dir's `Project` doc in the
   workspace registry (§8): set `okf_class: work-dir` or
   `okf_class: knowledge-dir` in its frontmatter.
7. Commit (in that repo) as a normal docs commit.

---

## 8. Workspace registry

Every workspace designates exactly one **registry** — the single home
for cross-project knowledge and the one place that knows what projects
exist and how they relate.

- **Location is fixed:** the workspace root is itself a work dir, and
  its `okf/` bundle is the registry. The registry does **not** get the
  nonstandard-name escape hatch (§1 rule 2) — walk-up detection stays
  mechanical only if it checks one fixed path per level.
- **Self-identification:** the registry's root `index.md` frontmatter
  carries `registry: true` alongside the usual keys (§1).
- **Finding it:** from anywhere, walk up parent directories until an
  `okf/index.md` with `registry: true` appears. Nested workspaces are
  legal; the **nearest ancestor registry wins**. No registry found →
  the directory is outside any workspace; cross-project features are
  simply unavailable there.
- **The registry is shared as a git repo.** In multi-member workspaces
  it MUST be its own repo, cloned at `<workspace>/okf/` on every
  member's machine — project bundles travel with their project repos,
  the registry travels as its own repo; that is the mechanism by which
  members share cross-project knowledge, and why no machine (including
  the standard author's) is special. A solo workspace MAY keep the
  registry inside the workspace's own repo until it is shared.
- **This guide lives in the registry**, as a `Playbook` concept at the
  bundle root. Everyone who clones the registry has the standard;
  updates propagate by pull; changes to the standard go through the
  registry repo's normal review.

Each project has a `Project` concept doc in the registry (`resource:` →
the repo path), grouped by org/purpose. A `Project` doc's frontmatter
records OKF conversion state via `okf_class: work-dir | knowledge-dir`
(absent = not yet converted) — this guide states the rules; the
registry tracks the state.

---

## 9. Validation

Conformance is checkable mechanically, not by eyeball. The reference
validator
([`okf-validate.py`](https://github.com/xcspl/xyno-okf-guide/blob/main/okf-validate.py),
in the standard's public repo alongside this guide; Python 3.10+,
stdlib + PyYAML)
checks a bundle root and exits nonzero on errors —
`python3 okf-validate.py <bundle-root>`:

**Errors (violate this standard):**

- A non-reserved `.md` file with missing/unparseable YAML frontmatter
  (root entry files and dot-paths excepted, §1).
- Required keys (§2) absent from frontmatter: `type`, `title`, `description`,
  `timestamp`, `status` (keys must be present; `type`, `title`, `description`
  must also be non-empty, while `timestamp` and `status` keys must be explicitly
  declared even if their values are temporarily empty).
- A bundle-root `index.md` without `okf_version` + `bundle` +
  `house_version` frontmatter, or with a `house_version` the validator
  does not know (§1).
- A `handling` block absent or differing from the canonical text for
  the declared `house_version` (§5).
- An `index.md` entry whose link target does not exist — indexes are
  *generated from* the directory, so a dead index link means the index
  wasn't regenerated (§5).

**Warnings (style drift, never fatal):**

- Broken concept-to-concept links in doc bodies — legal per spec §5.3
  (not-yet-written knowledge), but worth seeing listed.
- `status` outside the §2 vocabulary; uppercase or underscored tags.
- Frontmatter on a subdirectory `index.md` — upstream permits it only
  on the bundle root (§1).

Run it after any bootstrap (§7) or bulk edit, and before sharing a
bundle. Consumers stay permissive per the spec — validation gates what
*this workspace produces*, never what it accepts.
