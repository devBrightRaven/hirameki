# Changelog

- **Breaking (unreleased):** remove the separate `decision` command and `decide` skill in favor of the automatically triggered `decision-trace` workflow; preserve optional `save this` storage and the existing `active`, `superseded`, and `closed` lifecycle-node behavior.

## [1.6.2] — 2026-08-23

### Bug Fixes

- make `save this / skip / edit` the explicit decision write actions; workflow command names no longer authorize writes

## [1.6.1] — 2026-08-18

### Bug Fixes

- add batch save to triage (c566c36)

## [1.6.0] — 2026-08-18

### Features

- add decision lifecycle and stronger vault review (2168000)

## [1.5.1] — 2026-08-11

### Bug Fixes

- carry the release version into the Codex plugin manifest and package.json (92429c5)

## [1.5.0] — 2026-08-11

### Features

- judgment formation and change trajectories in journal, handoff, and triage (67e8bc5)

### Chores

- commit the release engine config (45f8e28)

All notable changes to hirameki are documented here.
Versioning follows [Semantic Versioning](https://semver.org/): MAJOR = breaking changes, MINOR = new commands or modes, PATCH = bug fixes and docs.

---

## [1.4.4] — 2026-07-29

### Fixed
- `session-end-check.mjs` no longer leaks git's own `fatal: not a git repository` on every Stop outside a repo. The `try/catch` was already there, but `execFileSync` inherits stderr by default, so the message reached the terminal before the exception was caught. Now `stdio: ['ignore', 'pipe', 'ignore']`.

### Changed
- Prose calls the per-day file a **wrap log** instead of a daily note, matching what it actually holds. The `daily:` config key is unchanged, so no vault needs migrating — the key names the role, the folder keeps whatever name you gave it.

---

## [1.4.3] — 2026-07-29

### Fixed
- Claude commands and hooks now resolve the vault folder layout from `{vault}/AGENTS.md`, matching the Codex adapter. 1.4.2 migrated only the Codex side, so after a setup moved its layout out of `vault-local.md` the Claude commands lost every folder key and stopped with "Setup not complete."
- The SessionStart hook no longer falls back to a hardcoded `_yorozuya/daily/` and `_inbox/`. A renamed folder used to leave it scanning the old path with no error; an unresolved key now skips the scan.
- The Stop hook read Wrap blocks from a hardcoded `_daily/` that no configuration ever pointed at. It now uses the resolved `daily` folder.
- `__init` writes the split configuration it documents: vault path and language to `~/.claude/vault-local.md`, folder layout to `{vault}/AGENTS.md`, and migrates folder keys found in the old locations.

### Added
- `getVaultFolders()` in `hooks/scripts/lib/resolve-vault.mjs` — one resolver for all hooks, with a `--selftest` check for the parser and its fallback order.
- `validate_commands.py` requires every command to name `AGENTS.md`, so a command cannot silently drift back to reading the layout from Claude-private config.

---

## [1.4.2] — 2026-07-29

### Fixed
- Codex resolves machine-specific vault root and language separately from the canonical folder layout in `{vault}/AGENTS.md`.
- A valid migration fallback no longer forces users to create `~/.codex/hirameki-local.md` or rerun initialization.

---

## [1.4.1] — 2026-07-29

### Added
- Codex-native plugin manifest and marketplace entry for versioned installation and updates.
- Bundled Hirameki command-reference assets required by the Codex initialization workflow.

### Fixed
- Codex adapter boundaries now use Codex personal configuration, runtime-neutral review routing, and explicit Claude-only hook behavior.

---

## [1.4.0] — 2026-07-13

### Changed
- `hooks/scripts/session-start-catchup.mjs`: now emits the union of two SessionStart behaviors that previously lived in separate copies — the Vault Pulse snapshot (per-folder note counts, active/dormant folders, `_inbox/` scan) **and** the current-sprint / `philosophy_mode` surfacing read from `vault-local.md`'s `## Vault Structure` section. Each part is wrapped in its own guard, so a failure in one (unreadable vault, missing config) no longer suppresses the other. The two outputs are joined into one `systemMessage`.
- `hooks/scripts/extract-actions.mjs`: replaced the hardcoded `D:/Obsidian/br-os-vault` vault path with portable runtime resolution via `getVaultPath()`. When no vault is configured on the machine the hook exits cleanly (`process.exit(0)`) instead of scanning a path that only exists on one machine.
- `hooks/scripts/vault-tidy-check.mjs`: same portability fix — the `process.argv[2]` fallback now resolves via `getVaultPath()` instead of the hardcoded machine path. Also fixed a latent crash: the file is ESM (`.mjs`) but used `require('fs')` inside `checkFile()`, which throws `ReferenceError: require is not defined` on the first file scanned; now uses proper `openSync`/`readSync`/`closeSync` imports. (Script is bundled but unregistered in `hooks.json`; invoked manually or by nightly-check.)

### Added
- `hooks/scripts/lib/resolve-vault.mjs`: bundled portable vault resolver (reads `~/.claude/vault-local.md`, falls back to `~/.claude/CLAUDE.md` at runtime; depends only on `USERPROFILE`/`HOME`). Required by the portable `extract-actions.mjs` — the plugin previously shipped no `hooks/scripts/lib/`, so the relative import would ENOENT at runtime without it.
- `docs/release-1.4.0-cutover.md`: atomic release + hook-dedupe cutover runbook (preconditions, exact steps, rollback, and the "current duplicate state is safe" note).

---

## [1.3.0] — 2026-05-31

### Added
- Codex adapter at `codex/skills/hirameki/`: one umbrella `SKILL.md`, Codex UI metadata, and 20 same-name workflow references copied from Claude commands so Codex can use Hirameki without exposing 20 standalone skills.
- Codex validation in `tests/validate_codex_skill.py`: checks skill metadata, router coverage, reference set completeness, byte-for-byte parity with `commands/*.md`, and command-spec compliance for every reference.
- Workflow smoke tests in `tests/smoke_hirameki_workflows.py`: covers `__init` folder resolution, read-only behavior for `next` / `tasks` / `pulse`, write-command safety contracts, and controlled fixture writes for `wrap` / `journal` / `handoff`.

### Changed
- CI now validates the Codex adapter and runs the workflow smoke tests alongside the existing Claude command validator.
- README documents Codex compatibility, including `~/.codex/hirameki-local.md` as the Codex-local config target and Claude config as migration fallback.

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
- Configuration is now split across two files. `__init` writes the vault folder structure to `<vault>/AGENTS.md` (agent-neutral — it travels with the vault; Codex / Gemini can read it too) and per-machine values (vault path, language) to `~/.claude/vault-local.md`. All commands resolve config in the order `<vault>/AGENTS.md` → `~/.claude/vault-local.md` → `~/.claude/CLAUDE.md`. Single-file `vault-local.md` setups are migrated on the next `__init` run. Follows the agent-agnostic-docs policy: facts describing the vault live with the vault.
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
