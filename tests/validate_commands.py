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
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from workflow_routes import load_routes
REDIRECTS = load_routes()["redirects"]

COMMANDS_DIR = Path(__file__).parent.parent / "commands"

# Commands that write to vault files — must have confirm-before-write rules.
# Includes conditional writers (reflect, frame, harvest with `save`) because
# their confirm path should still be documented when the save flag is given.
WRITE_COMMANDS: set[str] = {
    "wrap", "journal", "decision-trace", "handoff",
    "triage", "lens", "compose",
    "mekiki", "tidy",
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
        "缺口判定",  # 2.1.0: gap check decides which artifacts are proposed
        "本次建議：",  # 2.1.0: plan line
        "lesson",  # 2.1.0: fourth artifact, proposed only when the gap check says so
        "本次沒有新增價值",  # 2.1.0: zero-artifact exit
        "未提",  # 2.1.0: completion summary distinguishes not-proposed from skipped
        "The plan line is information, not a question",  # 2.1.0 R1: no extra confirmation stop
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
        "Purpose modes", "capabilities/tasks.md",
    ],
    "wrap": [
        "## Wrap",
        "Done", "In progress", "Next",
        "templates",
        "daily",
        "撤回：",  # 2.1.0: withdrawal semantics
        "已撤回",  # 2.1.0: merge section shown only when a withdrawal exists
        "實際使用有效",  # 2.1.0: status suffix vocabulary
    ],
    "journal": [
        "HHMM",  # filename format
        "Create", "Append",  # modes
        "Background",
        "Open items",
        "{journal}/lessons/",  # 2.1.0: lesson entries live under journal
        "後續結果",  # 2.1.0: follow-up block links outcome back to the earlier judgment
        "範圍未定",  # 2.1.0: corrections scope tag with an explicit undecided value
        "行動狀態",  # 2.1.0: judgment vs action state kept apart
        "tidy review",  # shared review capability
        "capabilities/review.md",  # one review contract
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
        "lens", "review", "snapshot",  # specialized modes
    ],
}

COMMAND_ONLY_REQUIRED: dict[str, list[str]] = {
    "decision-trace": [
        "uses the same `save this` gate",
        "explicitly decided choices become decision nodes",
    ],
    "triage": [
        "`save all` authorizes only drafts whose full content and target path have been displayed in a visible reply",
        "the written bytes must equal the displayed draft",
        "before any further write, display every remaining proposed draft in full",
        "A remaining draft that was not displayed before its write is not covered by `save all`",
        "display the changed draft again before writing it",
        "A batch approval never hides a failure.",
    ],
}

# Wording that must not return (save all covering drafts the user has not seen).
COMMAND_ONLY_FORBIDDEN: dict[str, list[str]] = {
    "triage": [
        "grants batch approval for every remaining triage draft",
        "An active `save all` is confirmation for the remaining triage drafts.",
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
            "save / skip", "save/skip", "save, skip", "save this / skip",
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


TASK_VIEW_COMMANDS = ("next", "tasks", "triage")
TASK_VIEW_REQUIRED = [
    'python3 -B -X utf8 "${CLAUDE_PLUGIN_ROOT}/scripts/task_view_cli.py" --vault <vault> --data <research>/tidy/tasks --gate-version <G>',
    "尚無有效待辦索引，以下由原始紀錄推導，未經歸檔驗證。",
    "待辦索引無法讀取",
    "Run the line with `python3`; if it cannot start (command not found, or a Windows Store stub error / non-JSON output mentioning the Microsoft Store), run the same line with `python`.",
    "TASK_GATE_VERSION",
    "有效待辦", "狀態未確認", "例外",
    "取回申請待整合", "來源已變更",
    "The raw-note fallback excludes items explicitly finished",
    "「已完成」", "「撤回」", "「已取代」", "repetition cannot reopen a closed item",
    "未完成 is not closed", "only newer explicit reopening",
    "unverified candidates", "not authoritative active or completed state",
    "not exactly one line",  # G1: gate file stop rule
    "never substitute a remembered or hard-coded value",  # G1
    "report the mismatch and stop, with no raw-note fallback",  # G3
    "`page-index-revision-changed` or `page-effective-view-changed`",  # G3: reader reason codes
    "do not run the reader, and use the raw-note fallback below as unverified candidates only",  # H2 unified
    "scripts/task_view_cli.py` exists. If it is missing",  # H2: scripts check no longer covers the gate file
    "plugin payload limitation",  # G4: scripts missing under the plugin root
    "never collapse records into ID ranges",  # every returned record individually
    "Keep each item's own reason visible",  # G5
]

TIDY_TASKS_REQUIRED = [
    "`tidy tasks`",
    'python3 -B -X utf8 "${CLAUDE_PLUGIN_ROOT}/scripts/tidy_dry_run.py" --vault <vault> --data <research>/tidy/tasks',
    "takes no `--gate-version`",
    "proposal only",
    "never writes any file",
    "never asks whether to save",
    "never archives",
    "never edits the formal index",
    "尚無有效待辦索引，無法執行任務歸檔試算。",
    "任務歸檔試算無法執行",
    "外掛目錄缺少任務歸檔試算腳本",
    "plugin payload limitation",
    "write_authorized: false",
    "restore-awaiting-integration",
    "gate_version", "index_revision",
]

# tasks.md must not treat repetition as a signal of unfinished work.
TASKS_FORBIDDEN = [
    "potential procrastination",
    "prepend ⚠",
    "Sort by: occurrence count",
    "Group items that refer to the same task (fuzzy match",
]
TASKS_REQUIRED = [
    "Current state outranks repetition", "status uncertain",
    "Status uncertain (recurrence only, no authoritative status):",
    "Total: X confirmed unresolved tasks; Y uncertain candidates",
]
TASKS_REQUIRED += [
    "Open items are discovery candidates only",
    "the latest authoritative status wins",
    "is not reopened by an older or unchecked Open item",
    "only a newer explicit reopening reopens",
    "Never reopen a task the task view lists as archived",
    "a bare old Open item is a candidate, not confirmed",
]
TASKS_REQUIRED += [
    "a completed-then-reopened task stays a candidate",
    "Status uncertain (missing or contradictory status evidence):",
    "Total: X tasks; Y status uncertain",
    "go only in the Status uncertain group",
]
TASKS_REQUIRED += [
    "Template headings and labels are structure: render them and all prose in the vault `language`",
    "Authority is per task identity and scope",
    "its effective view wins and raw notes add context only",
    "order events only by task revision/supersession or an unambiguous dated explicit event",
    "a filename, mtime, arrival time or copied text never establishes authority or order",
    "an unchecked Open item, even in the newest journal, is discovery evidence, not a reopening event",
    '"Old" means superseded for that same identity by an evidenced later event',
    "a replacement is a separate task",
    "Missing or conflicting identity, scope, order or evidence means `status uncertain`",
    "A handoff's frontmatter status is not task status unless its scope and an explicit task statement match",
    "by the order rule in Reconcile status",
    "a raw candidate and not validated indexed active state",
    "authoritative status evidence is an owner-approved status record, or an explicit completed, withdrawn, superseded or reopened event for the same task in a Wrap/Journal block",
    "└ Competing events: [source path of each competing or conflicting event]",
    "list the source paths of the competing or conflicting events, not only the missing evidence",
]
# Wording that would let file date, mtime or arrival order events.
TASKS_FORBIDDEN += [
    "latest authoritative source",
    "order by mtime",
    "order by file date",
    "order by filename",
    "by file modification time",
    "newest file wins",
    "latest file wins",
    "most recent file wins",
    "newer file",
    "older than a threshold wins",
]
TASKS_FORBIDDEN.append("AND never appearing in「完成」")
TASKS_FORBIDDEN.append("or an explicit open item in a source)")
TASKS_FORBIDDEN.append("Total: X stuck tasks")
TASKS_FORBIDDEN.append("Suggestion: Split into smaller tasks")


def has_any(content: str, patterns: list[str]) -> bool:
    """True if any pattern appears in content (case-insensitive)."""
    lower = content.lower()
    return any(p.lower() in lower for p in patterns)


def check_file(name: str, content: str) -> list[str]:
    errors: list[str] = []
    if name in REDIRECTS:
        route = REDIRECTS[name]
        for phrase in ('description:', 'compatibility redirect',
                       'preserving $ARGUMENTS', 'not an independent workflow or a write authorization',
                       route['target'] + ' ' + route['mode'],
                       "destination's display-before-write"):
            if phrase not in content:
                errors.append("Invalid migration redirect: " + phrase)
        if len(content.encode('utf-8')) > 2300:
            errors.append("Redirect retains an oversized parallel workflow")
        return errors

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
        if name == "tasks":
            capability = COMMANDS_DIR.parent / "references/capabilities/tasks.md"
            content = capability.read_text(encoding="utf-8")
            errors += check_file("task-capability", content)
        if name in TASK_VIEW_COMMANDS:  # Claude commands only; Codex adapter owns its own
            for phrase in TASK_VIEW_REQUIRED:
                if phrase not in content:
                    errors.append(f"Missing task view content: {phrase!r}")
        if name == "tidy":
            for phrase in TIDY_TASKS_REQUIRED:
                if phrase not in content:
                    errors.append(f"Missing tidy tasks content: {phrase!r}")
        if name == "tasks":
            for phrase in TASKS_FORBIDDEN:
                if phrase in content:
                    errors.append(f"Recurrence-as-signal wording present: {phrase!r}")
            for phrase in TASKS_REQUIRED:
                if phrase not in content:
                    errors.append(f"Missing tasks content: {phrase!r}")
        for phrase in COMMAND_ONLY_REQUIRED.get(name, []):
            if phrase not in content:
                errors.append(f"Missing command-only content: {phrase!r}")
        for phrase in COMMAND_ONLY_FORBIDDEN.get(name, []):
            if phrase in content:
                errors.append(f"Forbidden command-only content: {phrase!r}")
        results.append((name, errors))

    presence_rule = 'A file listing shows files only and can miss empty folders; never state or act on a folder or file being missing unless a direct check confirms it; otherwise say no files were found there.'
    for rel in ("commands/next.md", "commands/wrap.md", "commands/handoff.md",
                "references/capabilities/concept-card.md"):
        text = (COMMANDS_DIR.parent / rel).read_text(encoding="utf-8")
        if presence_rule not in text:
            results.append((rel, [f"Missing file-listing presence rule: {presence_rule!r}"]))

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
