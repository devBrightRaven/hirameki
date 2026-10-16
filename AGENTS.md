# Hirameki

Hirameki is a plugin of Obsidian vault knowledge-management commands (daily wrap, journal, handoff, concept tools, decision trace) for Claude Code, with a Codex adapter. MIT licensed, current version 2.1.0.
Agent-agnostic project rules. Any AI agent should read this before changing the repo.

## Purpose / status
- Active. Released as a Tier 1 asset: a change is releasable only when the command contract, Codex adapter, workflow smoke tests, local gate, and CI pass (see `VALIDATION.md`).

## Stack and runtime
- Commands are markdown prompt files with frontmatter. Tooling is Python 3 (`-X utf8`) for tests and task/tidy scripts, and Node (ESM `.mjs`) for hooks and one test. CI uses Python 3.12 and Node 22.
- Package metadata: `package.json` (no dependencies, no lockfile). Plugin manifests: `.claude-plugin/plugin.json`, `codex/.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`.

## Commands
- Full test battery: `npm test -- --run` (the extra `--run` is accepted for compatibility with a pre-commit hook).
- Task-view subset: `npm run test:task-view`.
- Release-chain parity check: `python -X utf8 tests/validate_release_contract.py`.
- Release is config-driven by `.release.json` (version file `.claude-plugin/plugin.json`, tag prefix `v`, default branch `main`, GitHub release on).
- No separate build, lint, or dev server commands exist.

## Layout
- `commands/`: Claude Code slash commands (`wrap`, `journal`, `handoff`, `tidy`, `triage`, `tasks`, etc.).
- `skills/decision-trace/`: the decision-trace skill.
- `codex/skills/hirameki/`: Codex adapter (`SKILL.md`, `references/`, `assets/_hirameki_cmds/`, `agents/`).
- `_hirameki_cmds/`: command catalogs in English, zh-TW, and ja (full and short).
- `hooks/`: Claude Code hooks (`hooks.json`, `hooks/scripts/*.mjs`): session start catchup, session end check, changelog append, action extraction.
- `scripts/`: Python helpers (task view, tidy writer/dry run, archive gate, Codex payload builder).
- `tests/`: validation and unit tests; mapped to contract items in `VALIDATION.md`.
- `docs/`, `openspec/`, `examples/`: design docs, specs/change proposals, and example vault config.
- `.github/workflows/validate.yml`: CI.

## Conventions and red lines
- Behavior changes must update the mapped test in the same change (`VALIDATION.md` update rule).
- `package.json` `scripts.test` must equal `.release.json` `test` followed by `verify`, joined with `&&`; change both in the same commit (enforced by `tests/validate_release_contract.py`).
- Claude commands and the Codex skill adapter must expose the same supported workflow semantics. Keep both in step.
- Commands keep valid frontmatter, confirm-before-write safeguards, and language behavior (enforced by `tests/validate_commands.py`).
- `.gitattributes` forces LF for `codex/**` and `_hirameki_cmds/*.md`; preserve those bytes across Windows checkouts.
- The release version is owned by the release flow, not edited by hand; `.release.json` `readmeSync` updates `codex/.codex-plugin/plugin.json` and `package.json` from the plugin version.
- Vault folder structure is read from `<vault>/AGENTS.md` (`## Vault Structure`); per-machine values live in the user's own config files, never in this repo.

## Do not commit
- Secrets, `.env*`, personal vault paths or contents.
- Personal agent config: `.claude/`, `.codex/`, `.mcp.json`.
- Python bytecode (`__pycache__/`, `*.pyc`) and `node_modules/` (already in `.gitignore`).

## Unverified / open
- `.worktrees/` and `.pytest_cache/` exist locally and are not listed in `.gitignore`; their intended handling was not confirmed.
- Whether the test suite passes at the current working-tree state was not run.
- README is multilingual (en, zh-TW, ja); which translation is canonical for edits was not confirmed.
