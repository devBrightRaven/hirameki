#!/usr/bin/env python3
"""
Static validation for hirameki command files (v1.2.0).

Written as a spec: defines what each command file MUST contain.
Run manually before publishing a release, and automatically via
GitHub Actions on every push / PR (.github/workflows/validate.yml).

Checks:
1. YAML frontmatter with description field
2. Universal phrases present in every command
   (config path, Vault Structure section, recovery command reference)
3. Write commands have confirm-before-write and print-after-write safety language
4. Per-command required sections and concepts (the load-bearing parts)
5. Language output instruction
"""

from __future__ import annotations

import sys
from pathlib import Path

COMMANDS_DIR = Path(__file__).parent.parent / "commands"

# Commands that write to vault files — must have confirm-before-write rules.
# Includes conditional writers (reflect, frame, harvest with `save`) because
# their confirm path should still be documented when the save flag is given.
WRITE_COMMANDS: set[str] = {
    "wrap", "journal", "decision-trace", "handoff",
    "triage", "lens", "compose",
    "mekiki", "arc", "bridge", "challenge",
    "reflect", "frame", "harvest", "graduate",
    "tidy", "critique",
}

# Per-command required content (substring checks; case-insensitive fallback).
# Each entry encodes load-bearing structure for that command.
REQUIRED_CONTENT: dict[str, list[str]] = {
    "__init": [
        "Vault Structure",
        "vault-local.md",
        "obsidian.json",
        "_hirameki_cmds",
        "handoff",  # v1.1.0 added handoff folder resolution
    ],
    "triage": [
        "wrap", "journal", "handoff",  # the three sub-flows
        "save this", "save all", "skip",  # action prompts
    ],
    "lens": [
        "arc", "bridge", "challenge",  # three of four sub-flows
        "position",  # position extraction step
        "save", "skip",
    ],
    "compose": [
        "voice", "frame",  # two sub-flows
        "save", "skip",
    ],
    "mekiki": [
        "Repo branch", "Article branch",  # two branches
        "github.com",  # routing
        "research", "inbox",  # outputs
    ],
    "next": [
        "Done", "Inbox", "Next",  # output sections
        "lucky",  # lucky mode
    ],
    "wrap": [
        "## Wrap",
        "Done", "In progress", "Next",
        "templates",
        "daily",
    ],
    "journal": [
        "HHMM",  # filename format
        "Create", "Append",  # modes
        "Background",
        "Open items",
    ],
    "decision-trace": [
        "Establish the decision state",
        "Build the trace",
        "Only move to `decided`",
        "Promotion gate",
        "{journal}/decisions/YYYY-MM-DD-{slug}.md",
        "active", "superseded", "closed",
        "Action? (save this / skip / edit)",
    ],
    "handoff": [
        "Re-pickup",
        "deferred",
        "Decisions",
        "Traps",
        "handoff",  # write target
    ],
    "arc": [
        "first",
        "timeline",
        "current",
        "unexplored",
        "arc",  # write target folder
    ],
    "bridge": [
        "intersect",
        "bridge",
        "hypothes",
    ],
    "challenge": [
        "contradiction",
        "assumption",
        "logic",
        "evidence",
        "challenge",  # write target folder
    ],
    "reflect": [
        "style", "position", "voice",
        "save",
        "reflect",  # write target folder
    ],
    "frame": [
        "Only-I",
        "collision",
        "stakes",
        "tension",
        "evidence",
        "PROCEED", "RETHINK", "KILL", "CONSOLIDATE",
        "save",
    ],
    "critique": [
        "Opus", "Codex", "Gemini",
        "sensory", "tension", "resonance",
        "benchmark",
    ],
    "pulse": [
        "week", "patterns",
        "undercurrent",
    ],
    "harvest": [
        "Articles", "Tools", "Topics", "People",
        "medium",
        "value",
        "graduate",
        "save",
    ],
    "graduate": [
        "0 Material",  # target folder, distinctive
        "MOC",
        "atomic",
        "wiki",
    ],
    "tasks": [
        "stuck",
    ],
    "tidy": [
        "tags", "fix", "full", "lint",  # five modes
        "lens", "pulse", "graduate",  # lint cross-reference suggestions
    ],
}

COMMAND_ONLY_REQUIRED: dict[str, list[str]] = {
    "decision-trace": [
        "uses the same `save this` gate",
        "explicitly decided choices become decision nodes",
    ],
}

# Must appear in every command file (language-independent: paths and command names).
UNIVERSAL_REQUIRED: list[tuple[str, str]] = [
    ("vault-local.md", "config file path (vault root, per-machine)"),
    ("AGENTS.md", "folder layout source (1.4.3 split config)"),
    ("Vault Structure", "config section name"),
    ("/hirameki:__init", "recovery command reference"),
]

# Each safety property accepts ANY of these patterns (case-insensitive).
# Different v1.2.0 commands use different phrasings of the same safety contract:
# - wrap/journal/handoff use literal "confirm" prompts
# - bridge/frame/reflect/harvest use "do not write unless the user asks/saves"
# - triage uses "save this / save all / skip"; lens/compose use "save / skip" per step
# All are valid expressions of "ask before writing".
WRITE_SAFETY: list[tuple[list[str], str]] = [
    (
        [
            "confirm",
            "save this / save all",
            "save / skip", "save/skip", "save, skip",
            "unless the user",
            "ask:",
            "ask for",
            "Save as",  # graduate's pattern
            "Save to",  # handoff's pattern
        ],
        "confirm-before-write rule",
    ),
    (
        [
            "full path",
            "file path",
            "the path after",
            "print the path",
            "Print the file path",
            "the full path",
        ],
        "print-path-after-write rule",
    ),
]

# At least one of these must appear (language output instruction).
# Either the convention ("language specified in ## Vault Structure → language")
# or a hardcoded language directive (e.g., critique always outputs 繁體中文).
LANGUAGE_PHRASES: list[str] = [
    "language", "Language",
    "繁體中文",
    "Traditional Chinese",
    "日本語",
    "Japanese",
]


def has_any(content: str, patterns: list[str]) -> bool:
    """True if any pattern appears in content (case-insensitive)."""
    lower = content.lower()
    return any(p.lower() in lower for p in patterns)


def check_file(name: str, content: str) -> list[str]:
    errors: list[str] = []

    # 1. Frontmatter
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter")
    elif "description:" not in content:
        errors.append("Missing 'description' field in frontmatter")

    # 2. Universal required phrases (exempt __init from self-reference)
    for phrase, label in UNIVERSAL_REQUIRED:
        if name == "__init" and phrase == "/hirameki:__init":
            continue
        if phrase not in content:
            errors.append(f"Missing {label}: {phrase!r}")

    # 3. Write commands: confirm-before-write and print-after-write
    if name in WRITE_COMMANDS:
        for patterns, label in WRITE_SAFETY:
            if not has_any(content, patterns):
                errors.append(f"Write command missing {label}")

    # 4. Per-command required content (case-insensitive fallback)
    for phrase in REQUIRED_CONTENT.get(name, []):
        if phrase not in content and phrase.lower() not in content.lower():
            errors.append(f"Missing required content: {phrase!r}")

    # 5. Language output instruction
    if not has_any(content, LANGUAGE_PHRASES):
        errors.append("Missing language output instruction")

    return errors


def main() -> None:
    command_files = sorted(COMMANDS_DIR.glob("*.md"))

    if not command_files:
        print(f"ERROR: No command files found in {COMMANDS_DIR}")
        sys.exit(1)

    # Check command file set matches spec
    expected = set(REQUIRED_CONTENT.keys())
    found = {f.stem for f in command_files}
    missing_in_disk = expected - found
    missing_in_spec = found - expected

    results: list[tuple[str, list[str]]] = []
    for path in command_files:
        name = path.stem
        content = path.read_text(encoding="utf-8")
        errors = check_file(name, content)
        for phrase in COMMAND_ONLY_REQUIRED.get(name, []):
            if phrase not in content:
                errors.append(f"Missing command-only content: {phrase!r}")
        results.append((name, errors))

    for name, errors in results:
        if errors:
            print(f"FAIL  {name}.md")
            for e in errors:
                print(f"      - {e}")
        else:
            print(f"ok    {name}.md")

    if missing_in_disk:
        print(f"\nMISSING (in spec but not on disk): {sorted(missing_in_disk)}")
    if missing_in_spec:
        print(f"\nUNCOVERED (on disk but not in spec): {sorted(missing_in_spec)}")

    failed = sum(1 for _, e in results if e)
    total = len(command_files)
    print(f"\n{total - failed}/{total} passed")

    all_passed = failed == 0 and not missing_in_disk and not missing_in_spec
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
