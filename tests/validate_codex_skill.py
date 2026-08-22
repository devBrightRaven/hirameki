from pathlib import Path

from validate_commands import REQUIRED_CONTENT, check_file


ROOT = Path(__file__).resolve().parents[1]
COMMANDS = ROOT / "commands"
SKILL = ROOT / "codex" / "skills" / "hirameki"
ASSETS = SKILL / "assets" / "_hirameki_cmds"

EXPECTED_REFERENCES = {f"{name}.md" for name in REQUIRED_CONTENT}
PLATFORM_DIVERGENT_REFERENCES = {
    "__init.md",
    "critique.md",
    "decision.md",
    "handoff.md",
    "journal.md",
    "mekiki.md",
    "pulse.md",
    "triage.md",
}
ADAPTER_RESOLVED_REFERENCES = {"decision.md", "handoff.md", "journal.md", "mekiki.md", "pulse.md", "triage.md"}
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


def test_codex_references_are_expected_set() -> None:
    references_dir = SKILL / "references"
    actual = {path.name for path in references_dir.glob("*.md")}
    assert actual == EXPECTED_REFERENCES


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
        assert asset.read_bytes() == canonical.read_bytes(), f"Bundled reference asset drifted: {name}"


def test_non_platform_codex_references_match_claude_commands() -> None:
    for name in EXPECTED_REFERENCES:
        if name in PLATFORM_DIVERGENT_REFERENCES:
            continue
        command = (COMMANDS / name).read_text(encoding="utf-8")
        reference = (SKILL / "references" / name).read_text(encoding="utf-8")
        assert reference == command, f"Codex reference drifted from commands/{name}"


def test_codex_platform_adapters_exclude_claude_runtime_assumptions() -> None:
    texts = {
        "SKILL.md": (SKILL / "SKILL.md").read_text(encoding="utf-8").lower(),
        **{
            name: (SKILL / "references" / name).read_text(encoding="utf-8").lower()
            for name in PLATFORM_DIVERGENT_REFERENCES
        },
    }
    combined = "\n".join(texts.values())
    for forbidden in FORBIDDEN_CODEX_GUIDANCE:
        assert forbidden not in combined, f"Codex adapter contains Claude-specific runtime guidance: {forbidden}"

    for name in ADAPTER_RESOLVED_REFERENCES:
        assert "~/.claude/vault-local.md" not in texts[name]
        assert "~/.claude/claude.md" not in texts[name]
        assert "resolve vault configuration through the umbrella hirameki adapter" in texts[name]
        assert "source: claude-code" not in texts[name]

    assert "~/.codex/hirameki-local.md" in texts["__init.md"]
    assert "~/.codex/agents.md" in texts["journal.md"]
    assert "native codex reviewers" in texts["critique.md"]
    assert "read-only" in texts["critique.md"]
    assert "/hirameki:__init" in texts["critique.md"]
    for phrase in ("感官密度", "結構張力", "觸動力", "strongest sentences", "weakest sentences", "structural suggestion", "wait for confirmation", "final review"):
        assert phrase in texts["critique.md"], f"Codex critique lost workflow contract: {phrase}"
    for phrase in ("benchmark", "read-only", "consensus", "append it to the same benchmark file"):
        assert phrase in texts["critique.md"], f"Codex critique lost adapter contract: {phrase}"
    for phrase in ("vault structure", "traditional chinese", "_yorozuya/daily/", "create folders only after confirmation", "parse the section again", "assets/_hirameki_cmds", "reference doc sync", "reconfigure", "start over completely", "source assets are unavailable", "do not write"):
        assert phrase in texts["__init.md"], f"Codex init lost workflow contract: {phrase}"
    assert "corrected the agent on" in texts["triage.md"]
    assert "corrected claude on" not in texts["triage.md"]
    assert "applicable codex personal and project guidance" in texts["mekiki.md"]
    assert "do not treat vault notes as runtime configuration" in texts["mekiki.md"]
    assert "automatic sessionstart snapshot is claude-only" in texts["pulse.md"]
    assert "codex does not run it automatically" in texts["pulse.md"]
    for promise in (
        "default snapshot runs automatically via sessionstart hook",
        "default snapshot runs automatically at session start",
        "now runs automatically via the sessionstart hook",
    ):
        assert promise not in texts["pulse.md"], f"Codex pulse contains an unqualified auto-run promise: {promise}"

    command_pulse = (COMMANDS / "pulse.md").read_text(encoding="utf-8")
    reference_pulse = (SKILL / "references" / "pulse.md").read_text(encoding="utf-8")
    command_analysis = command_pulse.split("\n---\n\n## `pulse week`", 1)[1]
    reference_analysis = reference_pulse.split("\n---\n\n## `pulse week`", 1)[1]
    assert reference_analysis == command_analysis, "Codex pulse analysis workflow drifted beyond the platform note"


def test_codex_vault_resolution_has_one_layout_source() -> None:
    router = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
    init = (SKILL / "references" / "__init.md").read_text(encoding="utf-8").lower()

    assert "{vault}/agents.md" in router
    assert "canonical source" in router
    assert "do not require `~/.codex/hirameki-local.md`" in router
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


def test_decision_history_contract() -> None:
    for root in (COMMANDS, SKILL / "references"):
        decision = (root / "decision.md").read_text(encoding="utf-8")
        for phrase in (
            "Promotion gate",
            "status: active",
            "superseded",
            "closed",
            "Alternatives considered",
            "Revisit when",
            "Do not copy their narrative",
            "Show the complete new or appended content",
            "Action? (save this / skip / edit)",
            "legacy `save` as an alias for `save this`",
            "they are not save actions and never authorize a write",
            "does not carry into decision",
        ):
            assert phrase in decision, f"{root}/decision.md lost contract: {phrase}"


def test_triage_batch_save_contract() -> None:
    for root in (COMMANDS, SKILL / "references"):
        triage = (root / "triage.md").read_text(encoding="utf-8")
        for phrase in (
            "save this / save all / skip / edit",
            "grants batch approval for every remaining triage draft",
            "show the full draft and target path",
            "without another `Action?` pause",
            "legacy `save` as an alias for `save this`",
        ):
            assert phrase in triage, f"{root}/triage.md lost batch-save contract: {phrase}"


def test_codex_references_satisfy_command_spec() -> None:
    for name in EXPECTED_REFERENCES:
        if name in {"__init.md", "critique.md"}:
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
    test_codex_skill_shape()
    test_codex_references_are_expected_set()
    test_codex_router_mentions_every_reference()
    test_codex_reference_assets_are_exactly_bundled()
    test_non_platform_codex_references_match_claude_commands()
    test_codex_platform_adapters_exclude_claude_runtime_assumptions()
    test_codex_vault_resolution_has_one_layout_source()
    test_judgment_trajectory_contract()
    test_triage_batch_save_contract()
    test_codex_references_satisfy_command_spec()
    test_tidy_accepts_codex_source_and_skips_generated_content()
    print("Codex Hirameki skill adapter validation passed")
