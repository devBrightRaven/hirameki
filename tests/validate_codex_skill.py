import re
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path

from validate_commands import REQUIRED_CONTENT, check_file, REDIRECTS


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from codex_reference_assets import render_asset
COMMANDS = ROOT / "commands"
SKILL = ROOT / "codex" / "skills" / "hirameki"
ASSETS = SKILL / "assets" / "_hirameki_cmds"

EXPECTED_REFERENCES = {f"{name}.md" for name in REQUIRED_CONTENT}
PLATFORM_DIVERGENT_REFERENCES = {
    "graduate.md",
    "next.md",
    "tasks.md",
    "__init.md",
    "critique.md",
    "decision-trace.md",
    "handoff.md",
    "journal.md",
    "mekiki.md",
    "pulse.md",
    "triage.md",
    # Codex-only task proposal adapter; Claude entry is outside this change's scope.
    "tidy.md",
}
ADAPTER_RESOLVED_REFERENCES = EXPECTED_REFERENCES - {"__init.md", "critique.md"}
EXPECTED_REFERENCE_ASSETS = {
    "hirameki-cmds-full-ja.md",
    "hirameki-cmds-full-zh-TW.md",
    "hirameki-cmds-full.md",
    "hirameki-cmds-short-ja.md",
    "hirameki-cmds-short-zh-TW.md",
    "hirameki-cmds-short.md",
}
FORBIDDEN_CODEX_GUIDANCE = {
    "allowed-mcp-server-names",
    "codex exec",
    "gemini -p",
    "~/.claude/rules",
    "project-level claude.md",
}


def extract_frontmatter(text: str) -> dict[str, str]:
    assert text.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    _, raw, _ = text.split("---\n", 2)
    frontmatter: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter


def test_codex_skill_shape() -> None:
    skill_md = SKILL / "SKILL.md"
    assert skill_md.exists(), "Codex Hirameki SKILL.md is missing"

    frontmatter = extract_frontmatter(skill_md.read_text(encoding="utf-8"))
    assert frontmatter["name"] == "hirameki"
    assert frontmatter["description"].startswith("Use when "), "Hirameki description must lead with trigger conditions"
    assert "Obsidian vault" in frontmatter["description"]
    assert len(frontmatter["description"]) <= 1024

    for language, phrases in {
        "English": ("should I", "which one", "torn between", "pros and cons"),
        "Traditional Chinese": ("要不要", "應該選", "該不該", "猶豫"),
        "Japanese": ("どうしよう", "どちら", "迷って", "比較"),
    }.items():
        assert all(phrase in frontmatter["description"] for phrase in phrases), (
            f"Codex discovery metadata lost {language} decision trigger"
        )

    openai_metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert "decision-trace" in openai_metadata
    assert "decide-like" not in openai_metadata


def test_codex_references_are_expected_set() -> None:
    references_dir = SKILL / "references"
    actual = {path.name for path in references_dir.glob("*.md")}
    assert actual == EXPECTED_REFERENCES


def test_concept_and_status_adapter_regression_guards() -> None:
    # Static instruction guards complement the independent fixture runs;
    # they do not claim to execute or prove model behavior.
    graduate = (SKILL / "references" / "capabilities/concept-card.md").read_text(encoding="utf-8")
    tasks = (SKILL / "references" / "capabilities/tasks.md").read_text(encoding="utf-8")
    router = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "{vault}/0 Material/" not in graduate
    assert "Check `{material}` for existing cards" in graduate
    assert "{material}/<Title>.md" in graduate
    assert "discovery-only request returns candidates without writing" in graduate
    assert "folder path or pasted text" in graduate
    assert "resolved scan scope" in graduate
    assert "one candidate across source files" in graduate
    assert "Insights note without a follow-up material card remains a candidate" in graduate
    assert "Insights coverage: unverified" in graduate
    assert "Do not invent an Insights path" in graduate
    assert "even without repeated wraps" in tasks
    assert "not as a required threshold for handoff actions" in tasks
    assert "Frontmatter alone is not task status" in tasks
    assert "shared task-status ordering rules" in tasks
    assert "Do not close unrelated subtasks" in tasks
    assert "status uncertain" in tasks
    assert "AND never appearing" not in tasks
    assert "If no recurring tasks found" not in tasks
    assert "finding concepts" in extract_frontmatter(router)["description"]
    assert "checking stuck work" in extract_frontmatter(router)["description"]
    assert "`/hirameki:__init`" in router and "`references/__init.md`" in router


def test_codex_payload_materializes_as_lf_on_windows() -> None:
    # Exercise Git's real checkout conversion, not a text-pattern assertion.
    relative = "codex/skills/hirameki/SKILL.md"
    with tempfile.TemporaryDirectory() as temporary:
        fixture = Path(temporary) / "source"
        checkout = Path(temporary) / "checkout"
        fixture.mkdir()
        checkout.mkdir()
        (fixture / relative).parent.mkdir(parents=True)
        shutil.copy2(ROOT / ".gitattributes", fixture / ".gitattributes")
        shutil.copy2(SKILL / "SKILL.md", fixture / relative)
        commands = (
            ["git", "init", "--quiet", str(fixture)],
            ["git", "-C", str(fixture), "-c", "core.autocrlf=true", "add", "--", ".gitattributes", relative],
            ["git", "-C", str(fixture), "-c", "core.autocrlf=true", "checkout-index", f"--prefix={checkout.as_posix()}/", "--", relative],
        )
        for command in commands:
            subprocess.run(command, check=True, capture_output=True)
        materialized = (checkout / relative).read_bytes()
        assert b"\r" not in materialized, "Codex plugin checkout must preserve LF"
        assert materialized == (SKILL / "SKILL.md").read_bytes()


def test_codex_router_mentions_every_reference() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for name in EXPECTED_REFERENCES:
        assert f"`references/{name}`" in text


def test_codex_reference_assets_are_exactly_bundled() -> None:
    actual = {path.name for path in ASSETS.glob("*.md")}
    assert actual == EXPECTED_REFERENCE_ASSETS
    for name in EXPECTED_REFERENCE_ASSETS:
        asset = ASSETS / name
        canonical = ROOT / "_hirameki_cmds" / name
        assert asset.is_file()
        expected = render_asset(name, canonical.read_text(encoding='utf-8'))
        actual = asset.read_text(encoding='utf-8')
        assert actual == expected, f"Bundled Codex asset projection drifted: {name}"
        assert '~/.claude/' not in actual and 'CLAUDE.md' not in actual
        assert '~/.codex/hirameki-local.md' in actual
        if '-full' in name:
            assert 'hirameki-local.md' in actual and '<vault>/AGENTS.md' in actual


def test_non_platform_codex_references_match_claude_commands() -> None:
    for name in EXPECTED_REFERENCES:
        if name in PLATFORM_DIVERGENT_REFERENCES:
            continue
        command = (COMMANDS / name).read_text(encoding="utf-8")
        reference = (SKILL / "references" / name).read_text(encoding="utf-8")
        def without_config_line(text):
            return '\n'.join(line.replace('`commands/', '`references/').replace(
                'under the currently loaded Hirameki skill root (the directory containing its SKILL.md)',
                'under the package root') for line in text.split('\n')
                             if not line.startswith(('Read `vault:` from',
                                                     'Resolve vault configuration through',
                                                     'For a natural-language request, apply')))
        assert without_config_line(reference) == without_config_line(command), \
            f"Codex workflow body drifted from commands/{name} beyond config resolution"


def test_codex_platform_adapters_exclude_claude_runtime_assumptions() -> None:
    texts = {
        "SKILL.md": (SKILL / "SKILL.md").read_text(encoding="utf-8").lower(),
        **{
            name: (SKILL / "references" / name).read_text(encoding="utf-8").lower()
            for name in EXPECTED_REFERENCES
        },
    }
    combined = "\n".join(texts.values())
    for forbidden in FORBIDDEN_CODEX_GUIDANCE:
        assert forbidden not in combined, f"Codex adapter contains Claude-specific runtime guidance: {forbidden}"

    for name in ADAPTER_RESOLVED_REFERENCES:
        assert "~/.claude/vault-local.md" not in texts[name]
        assert "~/.claude/claude.md" not in texts[name]
        assert "resolve vault configuration through the umbrella hirameki adapter" in texts[name]
        if name != "decision-trace.md":
            assert "source: claude-code" not in texts[name]

    assert "~/.codex/hirameki-local.md" in texts["__init.md"]
    assert "capabilities/review.md" in texts["journal.md"]
    review = (SKILL / 'references/capabilities/review.md').read_text(encoding='utf-8')
    assert "never the other agent's private configuration" in review
    assert "compose review" in texts["critique.md"]
    assert "not an independent workflow or a write authorization" in texts["critique.md"]
    for phrase in ("vault structure", "traditional chinese", "_yorozuya/daily/", "create folders only after confirmation", "parse the section again", "assets/_hirameki_cmds", "reference doc sync", "reconfigure", "start over completely", "source assets are unavailable", "do not write"):
        assert phrase in texts["__init.md"], f"Codex init lost workflow contract: {phrase}"
    assert "corrected the agent on" in texts["triage.md"]
    assert "corrected claude on" not in texts["triage.md"]
    assert "applicable codex personal and project guidance" in texts["mekiki.md"]
    assert "do not treat vault notes as runtime configuration" in texts["mekiki.md"]
    assert "tidy snapshot" in texts["pulse.md"]
    assert "lens patterns" in texts["pulse.md"]
    assert "next week" in texts["pulse.md"]


def test_codex_vault_resolution_has_one_layout_source() -> None:
    router = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    init = (SKILL / "references" / "__init.md").read_text(encoding="utf-8").lower()

    assert "{vault}/agents.md" in router
    assert "canonical source" in router
    assert "never read another agent's configuration" in router
    assert "~/.claude/" not in router
    assert "migration fallback" not in init
    assert "vault root and language only" in init
    assert "write folder layout only to `{vault}/agents.md`" in init
    assert "do not duplicate folder paths" in init


def test_judgment_trajectory_contract() -> None:
    journal_required = (
        "## 判斷與決策過程",
        "判斷的問題",
        "起點（原先判斷；尚未形成時寫「未形成判斷」）",
        "觀察",
        "推論",
        "尚未驗證的假設",
        "新出現的證據或經驗",
        "判斷結果（形成／改變／維持，以及原因）",
        "現場（原始素材）",
        "仍然不知道什麼",
        "什麼情況值得重新檢視",
        "本次沒有需要保存的判斷更新",
    )
    handoff_required = (
        "## 判斷更新",
        "- 原先判斷：",
        "- 改變依據：",
        "- 重新檢視條件：",
        "本次沒有需要接手的判斷更新",
        "Decisions made",
    )

    for root in (COMMANDS, SKILL / "references"):
        journal = (root / "journal.md").read_text(encoding="utf-8")
        handoff = (root / "handoff.md").read_text(encoding="utf-8")
        triage = (root / "triage.md").read_text(encoding="utf-8")
        for phrase in journal_required:
            assert phrase in journal, f"{root}/journal.md lost judgment field: {phrase}"
        for phrase in handoff_required:
            assert phrase in handoff, f"{root}/handoff.md lost judgment field: {phrase}"
        for phrase in ("## 判斷與決策過程", "## 判斷更新", "本次沒有需要保存的判斷更新", "本次沒有需要接手的判斷更新"):
            assert phrase in triage, f"{root}/triage.md drifted from direct workflows: {phrase}"
        judgment_rules = (
            "證據硬閘",
            "最多六個依 session 發生順序排列的原始證據單位",
            "由判斷導致的行動寫在 `What was done`",
        )
        for rule in judgment_rules:
            assert rule in triage, f"{root}/triage.md must carry the v3 rule standalone: {rule}"
            assert rule in journal, f"{root}/journal.md lost the v3 rule: {rule}"
        assert journal.count("## 判斷與決策過程") >= 2, f"{root}/journal.md must cover create and append modes"

    codex_handoff = (SKILL / "references" / "handoff.md").read_text(encoding="utf-8").lower()
    assert "source: codex" in codex_handoff
    assert "tasklist tool" not in codex_handoff
    assert "resolve vault configuration through the umbrella hirameki adapter" in codex_handoff


def test_decision_trace_contract() -> None:
    for root in (COMMANDS, SKILL / "references"):
        trace = (root / "decision-trace.md").read_text(encoding="utf-8")
        for phrase in (
            "Establish the decision state",
            "unresolved", "forming", "decided", "reviewing",
            "Build the trace",
            "viable options",
            "assumptions and unknowns",
            "reversal cost",
            "must not choose for the user",
            "Only move to `decided`",
            "Promotion gate",
            "{journal}/decisions/YYYY-MM-DD-{slug}.md",
            "status: active",
            "superseded",
            "closed",
            "Action? (save this / skip / edit)",
            "does not authorize a write",
        ):
            assert phrase in trace, f"{root}/decision-trace.md lost contract: {phrase}"

    command_trace = (COMMANDS / "decision-trace.md").read_text(encoding="utf-8")
    for phrase in ("uses the same `save this` gate", "explicitly decided choices become decision nodes"):
        assert phrase in command_trace, f"commands/decision-trace.md lost short persistence contract: {phrase}"

    assert not (COMMANDS / "decision.md").exists()
    assert not (ROOT / "skills" / "decide").exists()
    assert not (SKILL / "references" / "decision.md").exists()
    assert (COMMANDS / "decision-trace.md").is_file()
    assert (ROOT / "skills" / "decision-trace" / "SKILL.md").is_file()
    assert (SKILL / "references" / "decision-trace.md").is_file()

    router = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for legacy in ("/decision", "hirameki:decision"):
        assert re.search(rf"{re.escape(legacy)}(?![-\w])", router) is None, (
            f"Codex router exposes legacy invocation: {legacy}"
        )
    assert "references/decision.md" not in router
    assert "/decision-trace" in router
    assert "references/decision-trace.md" in router
    assert re.search(
        r"decision-trace.*?accepts only `decision-trace`, `/decision-trace`, and `hirameki:decision-trace`",
        router,
        re.IGNORECASE | re.DOTALL,
    ), "Codex router must reject `hirameki decision-trace` as an explicit invocation"


def test_canonical_decision_trace_behavior_contract() -> None:
    trace = (ROOT / "skills" / "decision-trace" / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "Explicit invocation accepts only",
        "`decision-trace`", "`/decision-trace`", "`hirameki:decision-trace`",
        "Establish the decision state",
        "unresolved", "forming", "decided", "reviewing",
        "Build the trace",
        "viable options", "evidence", "assumptions and unknowns",
        "constraints", "consequences", "reversal cost",
        "Only move to `decided`",
        "must not choose for the user",
        "Promotion gate",
        "An unresolved or forming trace may persist across sessions only after the user",
        "Do not add `decision_state` or another formation-state field",
        "{journal}/decisions/YYYY-MM-DD-{slug}.md",
        "status: active", "superseded", "closed",
        "Action? (save this / skip / edit)",
        "does not authorize a write",
        "No durable write occurs before the user explicitly selects `save this`.",
    ):
        assert phrase in trace, f"skills/decision-trace/SKILL.md lost behavior contract: {phrase}"

    codex_trace = (SKILL / "references" / "decision-trace.md").read_text(encoding="utf-8")
    canonical_reminder = trace.split("## Visible decision reminder\n", 1)[1].split("## Resolve existing state", 1)[0]
    adapter_reminder = codex_trace.split("## Visible decision reminder\n", 1)[1].split("## Resolve existing state", 1)[0]
    assert canonical_reminder == adapter_reminder, "Decision reminder differs across runtimes"
    assert "◆ **決策可記錄｜decision-trace**" in canonical_reminder
    assert "does not authorize a write" in canonical_reminder
    for phrase in (
        "An unresolved or forming trace may persist across sessions only after the user",
        "Do not add `decision_state` or another formation-state field",
        "Before showing a Codex-created decision-node draft and again before writing it",
    ):
        assert phrase in codex_trace, f"Codex decision-trace lost persistence/provenance guard: {phrase}"
    for phrase in ("どうしよう", "どちら", "迷って", "比較"):
        assert phrase in trace, f"canonical decision-trace lost Japanese trigger: {phrase}"
        assert phrase in codex_trace, f"Codex decision-trace reference lost Japanese trigger: {phrase}"


def test_forming_persistence_is_present_in_shipped_guides() -> None:
    expected = {
        "hirameki-cmds-full.md": "An unresolved or forming trace may persist across sessions",
        "hirameki-cmds-short.md": "Unresolved or forming traces use `save this`",
        "hirameki-cmds-full-zh-TW.md": "未決或形成中的 trace 若需跨 session 保存",
        "hirameki-cmds-short-zh-TW.md": "未決或形成中的 trace 使用 `save this`",
        "hirameki-cmds-full-ja.md": "未解決または形成中の trace を session 間で保存する場合",
        "hirameki-cmds-short-ja.md": "未解決または形成中の trace は `save this`",
    }
    for name, phrase in expected.items():
        canonical = (ROOT / "_hirameki_cmds" / name).read_text(encoding="utf-8")
        bundled = (ASSETS / name).read_text(encoding="utf-8")
        assert phrase in canonical, f"canonical guide lost forming persistence: {name}"
        assert phrase in bundled, f"bundled guide lost forming persistence: {name}"

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in (
        "An unresolved or forming trace may persist across sessions",
        "未決或形成中的 trace 若需跨 session 保存",
        "未解決または形成中の trace を session 間で保存する場合",
    ):
        assert phrase in readme, f"README lost forming persistence guidance: {phrase}"


def test_triage_batch_save_contract() -> None:
    for root in (COMMANDS, SKILL / "references"):
        triage = (root / "triage.md").read_text(encoding="utf-8")
        for phrase in (
            "save this / save all / skip / edit",
            "without another `Action?` pause",
            "legacy `save` as an alias for `save this`",
        ):
            assert phrase in triage, f"{root}/triage.md lost batch-save contract: {phrase}"
        if "authorizes only drafts" in triage:
            for phrase in (
                "full content and target path have been displayed in a visible reply",
                "written bytes must equal the displayed draft",
                "before any further write, display every remaining proposed draft in full",
                "not displayed before its write is not covered by `save all`",
            ):
                assert phrase in triage, f"{root}/triage.md lost display-before-write contract: {phrase}"
        else:
            for phrase in ("grants batch approval for every remaining triage draft",
                           "show the full draft and target path"):
                assert phrase in triage, f"{root}/triage.md lost batch-save contract: {phrase}"


def test_language_and_presence_rules_in_both_hosts() -> None:
    immediate_restore = 'A valid restore_pending task is visible and actionable now; do not require waiting for scheduled integration before the task can resume.'
    for path in (ROOT / 'commands/next.md', ROOT / 'commands/triage.md',
                 ROOT / 'references/capabilities/tasks.md',
                 SKILL / 'references/next.md', SKILL / 'references/triage.md',
                 SKILL / 'references/capabilities/tasks.md'):
        assert immediate_restore in path.read_text(encoding='utf-8'), f'{path}: approved restore must be actionable before index integration'
    template_rule = (
        "Template headings and labels are structure: render them and all prose in the vault `language`"
    )
    presence_rule = 'A file listing shows files only and can miss empty folders; never state or act on a folder or file being missing unless a direct check confirms it; otherwise say no files were found there.'
    for root in (ROOT, SKILL):
        tasks = (root / "references" / "capabilities/tasks.md").read_text(encoding="utf-8")
        assert tasks.count(template_rule) == 2, f"{root}: template language rule must precede both templates"
    for rel in (
        ROOT / "commands/next.md",
        ROOT / "commands/wrap.md",
        ROOT / "commands/handoff.md",
        ROOT / "references/capabilities/concept-card.md",
        SKILL / "SKILL.md",
        SKILL / "references/next.md",
        SKILL / "references/wrap.md",
        SKILL / "references/handoff.md",
        SKILL / "references/capabilities/concept-card.md",
    ):
        assert presence_rule in rel.read_text(encoding="utf-8"), f"{rel} lost the file-listing presence rule"


def test_codex_references_satisfy_command_spec() -> None:
    for name in EXPECTED_REFERENCES:
        if Path(name).stem in REDIRECTS:
            errors = check_file(Path(name).stem, (SKILL / "references" / name).read_text(encoding="utf-8"))
            assert not errors, errors
            continue
        if name == "__init.md":
            content = (SKILL / "references" / name).read_text(encoding="utf-8")
            frontmatter = extract_frontmatter(content)
            assert frontmatter.get("description"), f"{name}: missing description"
            assert any(phrase in content for phrase in ("language", "Language", "Traditional Chinese", "繁體中文")), f"{name}: missing language contract"
            assert "confirmation" in content.lower(), f"{name}: missing confirm-before-write contract"
            assert "path" in content.lower(), f"{name}: missing output-path contract"
            continue
        content = (SKILL / "references" / name).read_text(encoding="utf-8")
        errors = check_file(Path(name).stem, content)
        if name in ADAPTER_RESOLVED_REFERENCES:
            # The umbrella adapter resolves config for these; they name neither
            # the per-machine config file nor the <vault>/AGENTS.md layout source.
            errors = [
                error
                for error in errors
                if "config file path" not in error
                and "folder layout source" not in error
            ]
        assert not errors, f"{name}: {'; '.join(errors)}"


def test_tidy_accepts_codex_source_and_skips_generated_content() -> None:
    for path in (COMMANDS / "tidy.md", SKILL / "references" / "tidy.md"):
        content = path.read_text(encoding="utf-8")
        assert "self, claude-code, codex, agent, external" in content
        assert "node_modules" in content
        assert "ignored by Git" in content
        assert "full review of every file in scope" in content
        assert "CSV ledger" in content
        assert "pass-project-schema" in content
        assert "missing required fields (required: tags, status, source)" in content
        assert "50 or fewer" in content
        assert "more than 50" in content
        assert "lightweight detection pass" in content

    for path in (COMMANDS / "__init.md", SKILL / "references" / "__init.md"):
        content = path.read_text(encoding="utf-8")
        assert "system-folder subtrees" in content
        assert "unrelated siblings" in content


if __name__ == "__main__":
    test_canonical_decision_trace_behavior_contract()
    test_forming_persistence_is_present_in_shipped_guides()
    test_codex_skill_shape()
    test_codex_references_are_expected_set()
    test_concept_and_status_adapter_regression_guards()
    test_codex_payload_materializes_as_lf_on_windows()
    test_codex_router_mentions_every_reference()
    test_codex_reference_assets_are_exactly_bundled()
    test_non_platform_codex_references_match_claude_commands()
    test_codex_platform_adapters_exclude_claude_runtime_assumptions()
    test_codex_vault_resolution_has_one_layout_source()
    test_judgment_trajectory_contract()
    test_decision_trace_contract()
    test_triage_batch_save_contract()
    test_codex_references_satisfy_command_spec()
    test_language_and_presence_rules_in_both_hosts()
    test_tidy_accepts_codex_source_and_skips_generated_content()
    print("Codex Hirameki skill adapter validation passed")
