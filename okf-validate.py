#!/usr/bin/env python3
"""Reference validator for OKF bundles following the house standard
(okf-guide.md §9).

Usage:
    python3 okf-validate.py <bundle-root> [<bundle-root> ...]

Exits nonzero if any bundle has errors. Warnings never affect the exit
code. Requires PyYAML.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

RESERVED = {"index.md", "log.md"}
REQUIRED_KEYS = ("type", "title", "description", "timestamp")
STATUS_VOCAB = {"active", "idea", "superseded", "reverted", "archived"}
LINK_RE = re.compile(r"\]\(([^)#\s]+)\)")


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    """Return (frontmatter, body). frontmatter is None if absent/bad."""
    if not text.startswith("---\n"):
        return None, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None, text
    try:
        fm = yaml.safe_load(parts[0][4:])
    except yaml.YAMLError:
        return None, parts[1]
    return (fm if isinstance(fm, dict) else None), parts[1]


def validate_bundle(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def err(path: Path, msg: str) -> None:
        errors.append(f"{path.relative_to(root)}: {msg}")

    def warn(path: Path, msg: str) -> None:
        warnings.append(f"{path.relative_to(root)}: {msg}")

    md_files = sorted(root.rglob("*.md"))
    if not md_files:
        errors.append(f"{root}: no markdown files found")
        return errors, warnings

    for path in md_files:
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)

        if path.name == "index.md":
            # Bundle-root index must self-identify (§1).
            if path.parent == root:
                if not fm or not fm.get("okf_version") or not fm.get("bundle"):
                    err(path, "bundle-root index.md must carry okf_version "
                              "and bundle frontmatter (§1)")
            # Every index entry's link target must exist (§5, §9).
            for target in LINK_RE.findall(body if fm is not None else text):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (root / target.lstrip("/")) if target.startswith("/") \
                    else (path.parent / target)
                if not resolved.exists():
                    err(path, f"index entry links to missing target: {target}")
            continue

        if path.name == "log.md":
            continue

        # Concept doc (§2).
        if fm is None:
            err(path, "missing or unparseable YAML frontmatter")
            continue
        missing = [k for k in REQUIRED_KEYS if not fm.get(k)]
        if missing:
            err(path, f"missing required frontmatter keys: {', '.join(missing)}")

        status = fm.get("status")
        if status and status not in STATUS_VOCAB:
            warn(path, f"status '{status}' outside vocabulary "
                       f"{sorted(STATUS_VOCAB)} (§2)")
        for tag in fm.get("tags") or []:
            if not isinstance(tag, str) or tag != tag.lower() or "_" in tag:
                warn(path, f"tag '{tag}' should be lowercase, hyphenated (§2)")

        # Broken concept links are legal (spec §5.3) — warn only.
        for target in LINK_RE.findall(body):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not target.endswith(".md"):
                continue  # external file references (§4 rule 2) may point anywhere
            resolved = (root / target.lstrip("/")) if target.startswith("/") \
                else (path.parent / target)
            if not resolved.exists():
                warn(path, f"unresolved concept link (not-yet-written?): {target}")

    return errors, warnings


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    exit_code = 0
    for arg in argv[1:]:
        root = Path(arg).resolve()
        if not root.is_dir():
            print(f"error: {arg} is not a directory", file=sys.stderr)
            exit_code = 2
            continue
        errors, warnings = validate_bundle(root)
        print(f"== {root}")
        for e in errors:
            print(f"  ERROR   {e}")
        for w in warnings:
            print(f"  warning {w}")
        if errors:
            exit_code = 1
        print(f"  {len(errors)} error(s), {len(warnings)} warning(s)")
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
