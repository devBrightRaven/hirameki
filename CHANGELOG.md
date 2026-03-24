# Changelog

All notable changes to hirameki are documented here.
Versioning follows [Semantic Versioning](https://semver.org/): MAJOR = breaking changes, MINOR = new commands or modes, PATCH = bug fixes and docs.

---

## [0.5.0] — 2026-03-24

### Changed
- **Config location**: `__init` now writes `## Vault Structure` to `~/.claude/vault-local.md` instead of `~/.claude/CLAUDE.md`. This separates machine-specific vault paths from the shared global config, enabling cross-machine sync of `~/.claude/` via git.
- All commands now read from `vault-local.md` first, falling back to `CLAUDE.md` for backwards compatibility.
- `__init` Mode A (Step 4) migrates existing config from `CLAUDE.md` to `vault-local.md` if found.
- Updated README (EN/zh-TW/ja) and example CLAUDE.md.

---

## [0.4.0] — 2026-03-16

### Changed
- **BREAKING:** `status` command renamed to `pulse` to avoid confusion with system-level status commands. All subcommands preserved: `pulse`, `pulse week`, `pulse patterns`.
- Updated all command reference docs (6 files across EN/zh-TW/ja) and test validation.
- Added known limitations section to README in all three languages.

---

## [0.2.0] — 2026-03-04

### Added
- `decide` command — pre-decision vault scan with three-layer structure: Current State (vault context + reversibility check) / Friction (inversion: what guarantees failure) / Key Question (one question, not a recommendation). Does not write to file.
- Static CI validation — `tests/validate_commands.py` checks all command files for required sections and consistency. Runs automatically on GitHub Actions when `commands/` changes.

### Changed
- All 9 command files rewritten in English for maximum auditability and community accessibility. Output language is unchanged — still controlled by the `language` setting in `## Vault Structure`.
- `tidy` redesigned with four modes: `tidy` (missing + consistency, lightweight), `tidy tags` (tag convergence only), `tidy fix` (missing + consistency + auto-fix), `tidy full` (all blocks). Default no longer runs all blocks.
- `journal` filename now includes HHMM timestamp: `YYYY-MM-DD-HHMM-{slug}.md` for chronological sorting in Obsidian sidebar. Slug language follows `language` setting (Chinese/Japanese/English).
- `__init` vault detection now reads Obsidian's `obsidian.json` to auto-list known vaults, filters out built-in Sandbox vaults, and marks currently-open vaults with `open: true`.

### Removed
- Standalone commands: `arc`, `bridge`, `ghost`, `stress-test` → merged into `explore` with automatic mode detection based on input shape
- Standalone commands: `weekreview` → merged into `status week`
- Standalone commands: `cluster`, `undercurrent` → merged into `status patterns`
- Standalone command: `graduate` → merged into `harvest` as the seventh category with two-phase confirmation flow

### Fixed
- `_agent_analysis/` and `_agent_logs/` missing from folder candidate lists in all reference docs
- `_claude_code_feedback` renamed to `_claude_code_logs` across all files
- Greg Isenberg's URL and title in README

### Migration note
If you installed 0.1.x, the old commands (`arc`, `bridge`, `ghost`, `stress-test`, `weekreview`, `graduate`, `cluster`, `undercurrent`) will appear as phantom skills in your Claude Code skill list until you reinstall the plugin:
```
/plugin uninstall hirameki
/plugin install hirameki@hirameki
```

---

## [0.1.0] — 2026-02-xx

Initial release as hirameki plugin for Claude Code.

Commands: `__init`, `catchup`, `wrap`, `explore` (as arc/bridge/ghost/stress-test), `status` (as weekreview), `harvest` (as graduate), `tidy`, `journal`
