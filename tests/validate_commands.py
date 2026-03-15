#!/usr/bin/env python3
"""
Static validation for hirameki command files.

Written as a spec: defines what the English versions of each command MUST contain.
Commands must be rewritten in English to pass these checks.

Checks:
1. YAML frontmatter (description field)
2. Universal phrases present in every command
3. Write commands have confirm-before-write and print-after-write rules
4. Per-command required sections and concepts
5. decide command explicitly states it does not write to file
"""

import sys
from pathlib import Path

COMMANDS_DIR = Path(__file__).parent.parent / "commands"

# Commands that write to files — must have confirm-before-write rules
WRITE_COMMANDS = {"wrap", "explore", "harvest", "tidy", "journal"}

# Per-command required content (substring checks).
# These define the ENGLISH spec — commands must contain these phrases.
REQUIRED_CONTENT = {
    "__init": [
        # Detection steps
        "Vault detection",
        "Language",
        "Folder",
        # Write output
        "Vault Structure",
        # Folder candidates
        "_agent_analysis",
        "_agent_logs",
        "_claude_code_logs",
        # Obsidian auto-detection
        "obsidian.json",
        # Ref doc sync
        "_hirameki_cmds",
    ],
    "catchup": [
        "daily-notes",
        "inbox",
        # Three output sections
        "progress",
        "Inbox",
        "focus",
    ],
    "wrap": [
        # Write target
        "daily-notes",
        # Block format
        "## Wrap [HH:MM]",
        "Done",
        "In progress",
        "Next",
        # Template handling
        "templates",
    ],
    "explore": [
        # Mode detection table
        "Mode detection",
        # Four modes
        "Arc",
        "Bridge",
        "Ghost",
        "Stress-test",
        # Save flag
        "save",
        # Write targets
        "analysis}/arc/",
        "analysis}/bridge/",
        "analysis}/ghost/",
        "analysis}/stress-test/",
    ],
    "pulse": [
        # Three modes
        "pulse week",
        "pulse patterns",
        # Patterns mode concepts
        "ndercurrent",        # matches "Undercurrent" or "undercurrent"
        # Week mode concept
        "gap",               # matches "gap analysis" or "Gap analysis"
    ],
    "harvest": [
        # Seven categories
        "Articles",
        "Tools",
        "Topics",
        "People",
        "medium",            # "different medium" or "Medium"
        "value",             # "Untransacted value" or "Value"
        "graduate",          # "Graduate" or "ready to graduate"
        # Two-phase graduation
        "graduation",
        # Write target
        "analysis}/harvest/",
    ],
    "tidy": [
        # Mode variants
        "tidy tags",
        "tidy fix",
        "tidy full",
        # Check blocks
        "Missing",           # "Missing field check"
        "Consistency",
        "Tag",
        # Fix logic
        "fix",
        # Write target
        "analysis}/tidy/",
    ],
    "journal": [
        # Filename format
        "HHMM",
        # Two modes
        "Create",
        "Append",
        # Language-based slug rules
        "Traditional Chinese",
        "Japanese",
        "English",
    ],
    "lucky": [
        # Random selection
        "random",
        "neglected",         # weighting toward old notes
        # Constellation concept
        "constellation",
        "hidden theme",
        # No pairwise bridge
        "one question",
        # No file write
        "does not write",
    ],
    "decide": [
        # Three-layer structure
        "Current state",     # or "Current State"
        "Friction",
        "Key question",      # or "Key Question"
        # Reversibility
        "two-way door",
        "one-way door",
        # Inversion method
        "inversion",
        # No file write
        "does not write",
        # One question only
        "one question",
    ],
}

# Must appear in every command file (language-independent — paths and command names)
UNIVERSAL_REQUIRED = [
    ("~/.claude/CLAUDE.md",  "config file path"),
    ("Vault Structure",       "config section name"),
    ("/hirameki:__init",      "recovery command reference"),
]

# Must appear in every command that writes files
WRITE_REQUIRED = [
    ("confirm",   "confirm-before-write rule"),   # "confirm before writing" etc.
    ("full path", "print-path-after-write rule"),  # "print full path after writing" etc.
]

# At least one of these must appear (language output instruction)
LANGUAGE_PHRASES = ["language", "Language"]


def check_file(name: str, content: str) -> list[str]:
    errors = []

    # 1. Frontmatter
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter")
    elif "description:" not in content:
        errors.append("Missing 'description' field in frontmatter")

    # 2. Universal required phrases
    for phrase, label in UNIVERSAL_REQUIRED:
        if phrase not in content:
            errors.append(f"Missing {label}: {phrase!r}")

    # 3. Write commands: confirm-before-write and print-after-write
    if name in WRITE_COMMANDS:
        for phrase, label in WRITE_REQUIRED:
            if phrase.lower() not in content.lower():
                errors.append(f"Write command missing {label}: {phrase!r}")

    # 4. decide must explicitly state no file write
    if name == "decide":
        if "does not write" not in content and "no file" not in content.lower():
            errors.append("decide must state it does not write to file")

    # 5. Per-command required content
    for phrase in REQUIRED_CONTENT.get(name, []):
        # Case-sensitive for paths and format strings; case-insensitive for concepts
        if phrase not in content and phrase.lower() not in content.lower():
            errors.append(f"Missing required content: {phrase!r}")

    # 6. Language output instruction
    if not any(p in content for p in LANGUAGE_PHRASES):
        errors.append("Missing language output instruction")

    return errors


def main() -> None:
    command_files = sorted(COMMANDS_DIR.glob("*.md"))

    if not command_files:
        print(f"ERROR: No command files found in {COMMANDS_DIR}")
        sys.exit(1)

    # Check no expected command is missing
    expected = set(REQUIRED_CONTENT.keys())
    found = {f.stem for f in command_files}
    missing_files = expected - found

    all_passed = True
    results = []

    for path in command_files:
        name = path.stem
        content = path.read_text(encoding="utf-8")
        errors = check_file(name, content)
        results.append((name, errors))
        if errors:
            all_passed = False

    for name, errors in results:
        if errors:
            print(f"FAIL  {name}.md")
            for e in errors:
                print(f"      - {e}")
        else:
            print(f"ok    {name}.md")

    if missing_files:
        all_passed = False
        print(f"\nMISSING command files: {sorted(missing_files)}")

    print()
    total = len(command_files)
    failed = sum(1 for _, e in results if e)
    print(f"{total - failed}/{total} passed")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
