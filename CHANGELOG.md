# Changelog

All notable changes to hirameki are documented here.
Versioning follows [Semantic Versioning](https://semver.org/): MAJOR = breaking changes, MINOR = new commands or modes, PATCH = bug fixes and docs.

---

## [1.2.0] — 2026-05-14

### Added
- `triage` command — end-of-session bundle: walks through wrap → journal → handoff in sequence. Each step shows a full draft with save / skip / edit. Shares a single session-state scan across all three sub-flows.
- `lens <concept>` command — topic understanding orchestrator: arc → position extraction → bridge → challenge. Bridge auto-suggests a partner topic from the arc step; each step can be saved or skipped individually. Saves to `{research}/lens/`.
- `compose <topic>` command — topic creation orchestrator: voice (drafts in your vault style, drawing on vault positions) → frame (five-question validation). Standalone — does not require lens first. Saves to `{research}/compose/`.
- `arc <concept>` command — concept evolution tracker, extracted from `explore` as a standalone. Same-concept same-day: appends. Saves to `{research}/arc/YYYY-MM-DD-{concept}.md`.
- `challenge <topic>` command — argument weakness analysis, extracted from `explore` as a standalone. Checks internal contradictions, unverified assumptions, logic gaps, evidence gaps. Saves to `{research}/challenge/YYYY-MM-DD-{topic}.md`.

### Changed
- `mekiki`: now handles article ingestion in addition to GitHub repos. Auto-detects input type — GitHub URL or `owner/repo` → repo analysis (unchanged); article URL, pasted text, or local file path → article capture + vault cross-reference + integration verdict (integrate / revisit-later / skip). Replaces `ingest`.
- `tidy lint` mode: added cross-reference suggestions at end of output — when contradictions, stale claims, or orphan notes are found, surfaces follow-up suggestions to run `lens`, `pulse`, and `graduate`.
- `critique`: reviewer 2 changed from Copilot CLI to Codex CLI (`codex exec`). Vault path resolution now uses `vault-local.md` → fallback `CLAUDE.md` (consistent with all other commands). Frontmatter `source` corrected from `agent` to `claude-code`. Model family labels simplified to `[opus, codex, gemini]`.
- `__init`: added `handoff` folder to detection list and `## Vault Structure` template (was missing since v1.1.0).
- Reference docs (`_hirameki_cmds/`): all six files (EN / zh-TW / ja × short / full) fully rewritten to reflect v1.2.0 command set.
- Tests: rewrote `tests/validate_commands.py` from the v1.0.0-era spec (catchup / explore / lucky / decide) to the v1.2.0 spec covering all 20 commands. New `WRITE_SAFETY` accepts the established v1.2.0 safety patterns (wrap-style `confirm` prompt, bridge-style `unless the user asks`, orchestrator-style `save / skip`). `LANGUAGE_PHRASES` accepts hardcoded language directives (for `critique`, which always outputs 繁體中文). `.github/workflows/validate.yml` was already wired but the validator was broken; this restores end-to-end CI for command-spec compliance.

### Fixed
- `commands/frame.md`: was reading config from `~/.claude/CLAUDE.md` directly; now follows v1.2.0 convention (`vault-local.md` primary, `CLAUDE.md` fallback). Caught by the v1.2.0 validator.
- `commands/handoff.md`: was missing the language output instruction; added the standard line consistent with all other commands. Caught by the validator.
- `commands/bridge.md` and `commands/reflect.md`: when invoked with `save`, the explicit "print full path after writing" safety instruction was missing; added. Caught by the validator.

### Removed
- `ingest` command — article ingestion merged into `mekiki` (article branch). Use `/hirameki:mekiki <URL-or-text>` instead.
- `explore` command — split into `arc` and `challenge` as independent standalone commands. Mode-detection design (`challenge:` prefix, `?` suffix) retired.
- `hooks/scripts/catchup-reminders.mjs` — orphan script from the retired `catchup` command (removed in v1.0.0). Never wired in `hooks.json`, references retired commands and outdated config paths.

### Migration
- `/hirameki:ingest <URL>` → `/hirameki:mekiki <URL>` (behavior identical)
- `/hirameki:explore <concept>` → `/hirameki:arc <concept>`
- `/hirameki:explore challenge: <argument>` → `/hirameki:challenge <argument>`
- Existing `vault-local.md` without a `handoff:` key: run `/hirameki:__init` (Mode B) to add it. `handoff` and `triage` will fall back gracefully until updated.

---

## [1.1.0] — 2026-05-14

### Added
- `handoff` command — snapshots session state into a structured handoff doc at `{handoff}/YYYY-MM-DD-{slug}.md`. Automatically collects incomplete tasks, edited files, decisions, and deferred items. Shows full draft before writing. Complementary to `wrap`: wrap logs what happened, handoff captures what's left and how to resume.

---

## [1.0.2] — 2026-04-23

### Fixed
- Manifest: removed explicit `"hooks": "./hooks/hooks.json"` reference. Claude Code 2.1.116+ auto-loads the standard `hooks/hooks.json` and rejects duplicate references with a validation error. `manifest.hooks` should only point to non-standard or additional hook files.

## [1.0.1] — 2026-04-11

### Changed
- `mekiki`: added real-frequency check — estimates weekly encounter rate of the problem a repo solves before issuing an adoption verdict. Downgrades `adopt` to `defer-with-test` when usage would be rare.

## [1.0.0] — 2026-04-11

### Added
- `ingest` command — structured ingestion of external content (URL, text, file) into vault with cross-reference scanning and human confirmation
- `tidy lint` mode — content-level health check: contradiction detection, stale claims, orphan notes, dead wiki links
- `decide` skill — converted from command to auto-triggered skill (activates when user is weighing options)
- `next` now includes inbox scan (from catchup) and optional `next lucky` constellation mode (from lucky)
- SessionStart hook — automatic vault pulse snapshot + inbox scan on session start
- PostToolUse hook — changelog append to `{_yorozuya}/changelog.md` after each hirameki command
- `skills/` directory added to plugin structure

### Changed
- `pulse` (formerly `status`) — default snapshot mode moved to SessionStart hook; command now requires `week` or `patterns` argument
- `pulse` renamed back from `status` to better reflect its nature (health check, not report)

### Removed
- `catchup` — inbox scan merged into `next`, vault snapshot merged into SessionStart hook
- `lucky` — constellation reading merged into `next lucky` mode
- `decide` command — replaced by auto-triggered skill

### Restored
- `mekiki` command — accidentally removed in a prior session
- `frame` command — accidentally removed in a prior session
- `tasks` command — accidentally removed in a prior session

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
