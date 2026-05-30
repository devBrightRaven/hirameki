#!/usr/bin/env python3
"""
Deterministic smoke tests for Hirameki's Codex adapter.

These tests do not try to prove LLM judgment quality. They cover the parts that
can be made deterministic: vault folder resolution, read-only scan behavior, and
write-command safety contracts.
"""

from __future__ import annotations

import os
import re
import tempfile
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from validate_commands import WRITE_COMMANDS, check_file


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "codex" / "skills" / "hirameki" / "references"
TODAY = date(2026, 5, 30)

FOLDER_CANDIDATES: dict[str, list[str]] = {
    "daily": ["_yorozuya/daily", "Daily", "_daily", "daily", "Journal", "journal"],
    "inbox": ["Inbox", "_inbox", "inbox", "_Capture", "Capture"],
    "research": [
        "_yorozuya/research",
        "_hirameki_analysis",
        "_agent_analysis",
        "_claude_code_analysis",
        "Analysis",
        "_analysis",
        "analysis",
    ],
    "journal": [
        "_yorozuya/journal",
        "_hirameki_logs",
        "_agent_logs",
        "_claude_code_logs",
        "Logs",
        "_logs",
        "logs",
    ],
    "handoff": ["_yorozuya/handoff", "Handoff", "_handoff", "handoff"],
    "templates": ["Templates", "_templates", "templates"],
}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def touch_mtime(path: Path, days_ago: int) -> None:
    when = datetime.combine(TODAY - timedelta(days=days_ago), datetime.min.time())
    os.utime(path, (when.timestamp(), when.timestamp()))


def resolve_system_folders(vault: Path) -> dict[str, dict[str, str | None]]:
    resolved: dict[str, dict[str, str | None]] = {}
    for purpose, candidates in FOLDER_CANDIDATES.items():
        match = next((candidate for candidate in candidates if (vault / candidate).exists()), None)
        resolved[purpose] = {"match": match, "suggested": candidates[0]}
    return resolved


def snapshot_files(vault: Path) -> set[str]:
    return {
        path.relative_to(vault).as_posix()
        for path in vault.rglob("*")
        if path.is_file()
    }


def extract_section_items(text: str, section_names: set[str]) -> list[str]:
    items: list[str] = []
    in_section = False
    for raw in text.splitlines():
        line = raw.strip()
        heading = re.match(r"^#{2,4}\s+(.+)$", line)
        if heading:
            title = heading.group(1).strip().lower()
            in_section = title in {name.lower() for name in section_names}
            continue
        if in_section and line.startswith("- "):
            items.append(line[2:].strip())
    return items


def normalize_task(item: str) -> str:
    item = re.sub(r"^\[[ xX]\]\s*", "", item.strip())
    item = item.replace("✓ Done", "").strip()
    return re.sub(r"\s+", " ", item).lower()


def build_fixture(vault: Path) -> None:
    for folder in ["Daily", "Inbox", "Analysis", "Logs", "Handoff", "Templates", "Notes", "Drafts"]:
        (vault / folder).mkdir(parents=True, exist_ok=True)
    (vault / ".obsidian").mkdir(exist_ok=True)

    write_text(
        vault / "Daily" / "2026-05-28.md",
        """
        ## Wrap

        ### Done
        - Finished previous adapter audit

        ### Next
        - Run Hirameki smoke tests
        - Review write workflow safety
        """,
    )
    write_text(
        vault / "Daily" / "2026-05-29.md",
        """
        ## Wrap

        ### Done
        - Confirmed init no longer forces _yorozuya

        ### In progress
        - Validate Codex adapter behavior

        ### Next
        - Run Hirameki smoke tests
        - Review write workflow safety
        """,
    )
    write_text(
        vault / "Daily" / "2026-05-30.md",
        """
        ## Wrap

        ### Done
        - Added Codex reference parity validation

        ### Next
        - Run Hirameki smoke tests
        - Document smoke-test status
        """,
    )

    write_text(
        vault / "Logs" / "2026-05-30-0915.md",
        """
        ## Open items
        - Run Hirameki smoke tests
        - Update CI validation
        - Completed old task ✓ Done
        """,
    )
    write_text(vault / "Inbox" / "adapter-question.md", "Should Codex references stay byte-identical to Claude commands?")
    write_text(vault / "Inbox" / "workflow-note.md", "Test read-only workflows before write workflows.")

    write_text(vault / "Notes" / "agency-map.md", "Agency needs human judgment and explicit boundaries.")
    write_text(vault / "Notes" / "decision-map.md", "Agency appears when decisions are reversible and visible.")
    write_text(vault / "Drafts" / "ai-boundaries.md", "AI boundaries preserve agency during workflow automation.")
    touch_mtime(vault / "Notes" / "agency-map.md", 1)
    touch_mtime(vault / "Notes" / "decision-map.md", 3)
    touch_mtime(vault / "Drafts" / "ai-boundaries.md", 5)


def collect_recent_tasks(vault: Path, days: int = 3) -> dict[str, list[str]]:
    sources: dict[str, list[str]] = defaultdict(list)
    for offset in range(days):
        day = TODAY - timedelta(days=offset)
        daily = vault / "Daily" / f"{day.isoformat()}.md"
        if daily.exists():
            for item in extract_section_items(daily.read_text(encoding="utf-8"), {"Next", "下一步"}):
                sources[normalize_task(item)].append(f"{day.strftime('%m-%d')} wrap")

    for path in sorted((vault / "Logs").glob("2026-05-*.md")):
        for item in extract_section_items(path.read_text(encoding="utf-8"), {"Open items"}):
            if "✓ done" not in item.lower():
                sources[normalize_task(item)].append(f"{path.stem[:10][5:]} journal")
    return sources


def collect_stuck_tasks(vault: Path, days: int = 7) -> dict[str, int]:
    next_counts: dict[str, int] = defaultdict(int)
    done: set[str] = set()
    for offset in range(days):
        day = TODAY - timedelta(days=offset)
        daily = vault / "Daily" / f"{day.isoformat()}.md"
        if not daily.exists():
            continue
        text = daily.read_text(encoding="utf-8")
        for item in extract_section_items(text, {"Next", "下一步"}):
            next_counts[normalize_task(item)] += 1
        for item in extract_section_items(text, {"Done", "完成"}):
            done.add(normalize_task(item))
    return {task: count for task, count in next_counts.items() if count >= 2 and task not in done}


def scan_week_activity(vault: Path) -> list[str]:
    cutoff = datetime.combine(TODAY - timedelta(days=7), datetime.min.time()).timestamp()
    active: list[str] = []
    for folder in ["Notes", "Drafts"]:
        if any(path.stat().st_mtime >= cutoff for path in (vault / folder).glob("*.md")):
            active.append(folder)
    return active


def scan_undercurrents(vault: Path) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for path in list((vault / "Notes").glob("*.md")) + list((vault / "Drafts").glob("*.md")):
        text = path.read_text(encoding="utf-8").lower()
        if "agency" in text:
            counts["agency"] += 1
    return dict(counts)


def append_wrap_sample(vault: Path) -> Path:
    target = vault / "Daily" / f"{TODAY.isoformat()}.md"
    if not target.exists():
        write_text(target, f"# {TODAY.isoformat()}")
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(
            "\n---\n\n"
            "## Wrap [12:00]\n\n"
            "### Done\n"
            "- Ran controlled write smoke test `#test-fix` `#hirameki`\n\n"
            "### In progress\n"
            "- None\n\n"
            "### Next\n"
            "- Review smoke-test status\n"
        )
    return target


def create_journal_sample(vault: Path) -> Path:
    target = vault / "Logs" / "2026-05-30-1200-hirameki-smoke-test.md"
    write_text(
        target,
        """
        ---
        tags:
          - journal
          - hirameki
        status: log
        source: codex
        actions:
          - type: test-fix
            project: hirameki
        corrections: 0
        ---

        # Hirameki smoke test

        > Created: 2026-05-30 12:00

        ## Background
        Controlled fixture write for the Codex adapter.

        ## What was done
        Created a deterministic journal sample.

        ## Why this approach
        It verifies that Codex-created files use source: codex.

        ## Inspiration connections
        None.

        ## Possible improvements
        None.

        ## Corrections
        None.

        ## Open items
        No open items.
        """,
    )
    return target


def create_handoff_sample(vault: Path) -> Path:
    target = vault / "Handoff" / "2026-05-30-hirameki-smoke-test.md"
    write_text(
        target,
        """
        ---
        tags:
          - handoff
        status: reference
        source: codex
        created: 2026-05-30 12:00
        topic: Hirameki smoke-test handoff
        priority: low
        estimated_cost: 5 minutes
        ---

        # Handoff - Hirameki smoke test

        > Controlled fixture handoff for Codex adapter validation.

        ---

        ## Re-pickup checklist

        1. [ ] Read this handoff.

        ---

        ## What's done

        - Controlled write smoke test created this file.

        ---

        ## In flight

        None

        ---

        ## What's deferred

        None

        ---

        ## Decisions made

        - Codex-created files use source: codex.

        ---

        ## Next actions

        1. Remove fixture after test completion.

        ---

        ## Traps

        None

        ---

        ## Related artifacts

        ### Files
        None

        ### Vault notes
        None
        """,
    )
    return target


def test_init_resolution_prefers_existing_folders() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp)
        for folder in ["Daily", "Inbox", "Analysis", "Logs", "Handoff", "Templates"]:
            (vault / folder).mkdir(parents=True)
        result = resolve_system_folders(vault)
        assert result["daily"]["match"] == "Daily"
        assert result["research"]["match"] == "Analysis"
        assert result["journal"]["match"] == "Logs"
        assert result["daily"]["suggested"] == "_yorozuya/daily"


def test_init_resolution_empty_vault_only_suggests_defaults() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp)
        (vault / ".obsidian").mkdir()
        result = resolve_system_folders(vault)
        assert all(value["match"] is None for value in result.values())
        assert result["daily"]["suggested"] == "_yorozuya/daily"
        assert not (vault / "_yorozuya").exists()


def test_next_read_only_sources() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp)
        build_fixture(vault)
        before = snapshot_files(vault)
        yesterday = (vault / "Daily" / "2026-05-29.md").read_text(encoding="utf-8")
        inbox = sorted(path.name for path in (vault / "Inbox").glob("*.md"))

        assert "Run Hirameki smoke tests" in extract_section_items(yesterday, {"Next", "下一步"})
        assert inbox == ["adapter-question.md", "workflow-note.md"]
        assert snapshot_files(vault) == before


def test_tasks_default_and_stuck_modes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp)
        build_fixture(vault)
        before = snapshot_files(vault)
        recent = collect_recent_tasks(vault, days=3)
        stuck = collect_stuck_tasks(vault, days=7)

        assert len(recent["run hirameki smoke tests"]) == 4
        assert len(recent["review write workflow safety"]) == 2
        assert stuck["run hirameki smoke tests"] == 3
        assert snapshot_files(vault) == before


def test_pulse_week_and_patterns_sources() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp)
        build_fixture(vault)
        before = snapshot_files(vault)
        active = scan_week_activity(vault)
        undercurrents = scan_undercurrents(vault)

        assert active == ["Notes", "Drafts"]
        assert undercurrents["agency"] == 3
        assert snapshot_files(vault) == before


def test_write_references_keep_safety_contract() -> None:
    for command in sorted(WRITE_COMMANDS):
        content = (REFERENCES / f"{command}.md").read_text(encoding="utf-8")
        errors = check_file(command, content)
        assert not errors, f"{command}.md failed safety contract: {errors}"


def test_controlled_write_samples_stay_in_fixture_and_use_codex_source() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp)
        build_fixture(vault)
        before = snapshot_files(vault)
        wrap = append_wrap_sample(vault)
        journal = create_journal_sample(vault)
        handoff = create_handoff_sample(vault)
        after = snapshot_files(vault)

        added = after - before
        assert journal.relative_to(vault).as_posix() in added
        assert handoff.relative_to(vault).as_posix() in added
        assert "## Wrap [12:00]" in wrap.read_text(encoding="utf-8")
        assert "source: codex" in journal.read_text(encoding="utf-8")
        assert "source: codex" in handoff.read_text(encoding="utf-8")
        assert "source: claude-code" not in journal.read_text(encoding="utf-8")
        assert "source: claude-code" not in handoff.read_text(encoding="utf-8")


def main() -> None:
    tests = [
        test_init_resolution_prefers_existing_folders,
        test_init_resolution_empty_vault_only_suggests_defaults,
        test_next_read_only_sources,
        test_tasks_default_and_stuck_modes,
        test_pulse_week_and_patterns_sources,
        test_write_references_keep_safety_contract,
        test_controlled_write_samples_stay_in_fixture_and_use_codex_source,
    ]
    for test in tests:
        test()
        print(f"ok    {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} smoke tests passed")


if __name__ == "__main__":
    main()
