from pathlib import Path

from validate_commands import REQUIRED_CONTENT, check_file


ROOT = Path(__file__).resolve().parents[1]
COMMANDS = ROOT / "commands"
SKILL = ROOT / "codex" / "skills" / "hirameki"

EXPECTED_REFERENCES = {f"{name}.md" for name in REQUIRED_CONTENT}


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


def test_codex_references_match_claude_commands() -> None:
    for name in EXPECTED_REFERENCES:
        command = (COMMANDS / name).read_text(encoding="utf-8")
        reference = (SKILL / "references" / name).read_text(encoding="utf-8")
        assert reference == command, f"Codex reference drifted from commands/{name}"


def test_codex_references_satisfy_command_spec() -> None:
    for name in EXPECTED_REFERENCES:
        content = (SKILL / "references" / name).read_text(encoding="utf-8")
        errors = check_file(Path(name).stem, content)
        assert not errors, f"{name}: {'; '.join(errors)}"


if __name__ == "__main__":
    test_codex_skill_shape()
    test_codex_references_are_expected_set()
    test_codex_router_mentions_every_reference()
    test_codex_references_match_claude_commands()
    test_codex_references_satisfy_command_spec()
    print("Codex Hirameki skill adapter validation passed")
