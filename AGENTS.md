# AGENTS.md

Briefing for AI agents working in this repo. Humans: see `README.md`.

## What this repo is

The **house OKF standard**: a set of rules on top of the Open Knowledge
Format (OKF) spec that workspaces adopt so every project speaks the
same knowledge dialect. The repo is also an OKF bundle itself, a pure
knowledge dir that follows its own standard. Every change here must
leave it passing its own validator.

## Binding contract

`index.md` frontmatter is authoritative. Its `handling` block says, in
short:

- Read `index.md` before opening any doc.
- Navigate by index entries, not by globbing the tree.
- A write to a directory updates that directory's `index.md` in the
  same commit.
- The full rules are in `okf-guide.md`.

If this file and `index.md` ever disagree, `index.md` wins and this
file has a bug.

## Map

| File | Role |
|---|---|
| `okf-guide.md` | The standard. `Playbook`. Adopters vendor it unchanged into their workspace registry. |
| `okf-validate.py` | Reference validator. Mechanical half of the standard; the guide's §9 is its documentation. |
| `log.md` | Dated history of the standard, newest first: a date heading per day, a title per entry, optional description. No frontmatter. |
| `index.md` | Bundle root: self-identification, entry contract, listing. |
| `README.md`, `AGENTS.md` | Root entry files. Not concept docs, not indexed. |

Every other `.md` must carry the house frontmatter: `type`, `title`,
`description`, `timestamp`, `status`.

## Changing the standard

A change to the rules touches several files, and they move together
in one commit:

1. **Edit `okf-guide.md`.** Keep every rule structural: phrased
   relative to a workspace, never naming a machine, person, or path
   outside the bundle. Bump its `timestamp`.
2. **Mirror it in `okf-validate.py`** if the rule is mechanically
   checkable, and in `okf-guide.md` §9, which lists what the validator
   checks and is its only documentation.
3. **If canonical text changes** (`handling`, or any future optional
   clause), bump `house_version`: add the new version to the
   validator's canonical tables without deleting old ones, then update
   the version and examples in `okf-guide.md` §1 and §5, `index.md`,
   and `README.md`.
4. **Record it in `log.md`.** Add an entry under today's `## YYYY-MM-DD`
   heading (create it at the top if missing): a `###` title, then an
   optional description with any detail, such as the reasoning and
   rejected alternatives. If an `open-questions.md` exists, remove anything that
   landed, and delete the doc once it is empty.
5. **Update `index.md`** if a doc was added, renamed, or re-described.
6. **Validate** from the repo root:

   ```
   python3 okf-validate.py .
   ```

   Expect zero errors. Two warnings are known and fine: example links
   inside the guide's prose that point at docs that don't exist here.

## Conventions

- **One concept per doc.** When a rationale in `log.md` outgrows
  its entry, split it into a `Decision` doc under `decisions/`, link it
  from the timeline, and add a `decisions/index.md`.
- **Filenames kebab-case, tags lowercase-hyphenated.**
- **Don't restate the guide elsewhere.** `README.md` introduces,
  `AGENTS.md` orients, the guide rules. Link rather than copy.
- **Upstream first.** Before proposing a new key, check the upstream
  spec does not already define one. Upstream meanings are never
  overridden.

## Upstream

The OKF spec lives at
<https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md>.
This standard currently adopts OKF v0.2. When upstream moves, record
the review in `log.md` whether or not anything is adopted.

## After a change lands

Adopting workspaces pick up changes by copying the new `okf-guide.md`
into their registry and bumping `house_version` in their bundles' root
indexes. Nothing here propagates on its own.
