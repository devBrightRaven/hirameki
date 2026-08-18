---
description: First-time setup and vault configuration
---

## Overview

`__init` handles first-time setup of the Hirameki environment. It writes a split configuration:

- **Per-machine** values (vault path, language, symlinked policy paths) → `~/.claude/vault-local.md`, which is Claude-private and gitignored.
- **Vault folder layout** (`daily`, `inbox`, `journal`, `research`, `handoff`, `templates`) → `{vault}/AGENTS.md`, which travels with the vault so Codex, Gemini, and any future agent resolve the same paths.

The split follows `~/.claude/rules/policies/agent-agnostic-docs.md`: facts describing the vault belong with the vault; facts describing this machine stay on this machine.

All other commands read the result directly — they do not call `__init` again.

## How other commands read configuration

Before executing, every other hirameki command:

1. Reads `vault:` from `~/.claude/vault-local.md` to locate the vault root. If absent, falls back to `## Vault Structure` then the `## Vault` section's `path:` in `~/.claude/CLAUDE.md`.
2. Reads the `## Vault Structure` section from `{vault}/AGENTS.md` for folder keys.
3. If a folder key is missing there, falls back to `## Vault Structure` in `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` — setups created before 1.4.3 kept the layout in those files.
4. If the vault root cannot be resolved, or a required folder key is found nowhere → stop and respond: "Setup not complete. Please run `/hirameki:__init` first."
5. If found → use as-is, no further validation.
6. If a path is invalid or unreadable during execution → respond: "Configuration error. Please run `/hirameki:__init` to reconfigure."

Never substitute a hardcoded default for a missing folder key. A guessed path reads the wrong folder silently; stopping is recoverable.

## Execution modes

### Mode A: First-time setup

Triggered when `## Vault Structure` does not exist in `{vault}/AGENTS.md`, `~/.claude/vault-local.md`, or `~/.claude/CLAUDE.md`, or when the user runs `/hirameki:__init` with no existing configuration.

**Step 1 — Vault detection**

Try in order:
1. Current working directory contains `.obsidian/` → use as vault
2. Read `path` from the `## Vault` section in `~/.claude/CLAUDE.md`
3. Read the Obsidian app's configuration file to get the list of known vaults:
   - Windows: `%APPDATA%\Obsidian\obsidian.json`
   - macOS: `~/Library/Application Support/obsidian/obsidian.json`
   - Linux: `~/.config/obsidian/obsidian.json`

   Before using results from `obsidian.json`, filter out any vault whose path is inside Obsidian's own AppData or Application Support folder — those are Obsidian's built-in Sandbox, not the user's vault.

   After filtering, if one vault remains → use it and confirm: "Found vault: {path}. Use this one?"
   After filtering, if multiple vaults remain → list them and let the user choose. Mark any with `open: true` as "currently open in Obsidian."

4. If reading fails or no vault is found → ask the user to provide the full path. Verify it exists and contains `.obsidian/`, then write to `~/.claude/CLAUDE.md`:
   ```
   ## Vault
   path: {path}
   ```

**Step 2 — Language setting**

Ask the user: "What language should Hirameki use for output?"
- Traditional Chinese
- English
- Japanese
- Other (user types freely)

**Step 3 — Folder resolution**

Match each purpose to the first existing candidate folder in the vault:

- **daily**: `_yorozuya/daily/`, `Daily/`, `_daily/`, `daily/`, `Journal/`, `journal/`
- **inbox**: `Inbox/`, `_inbox/`, `inbox/`, `_Capture/`, `Capture/`
- **research**: `_yorozuya/research/`, `_hirameki_analysis/`, `_agent_analysis/`, `_claude_code_analysis/`, `Analysis/`, `_analysis/`, `analysis/`
- **journal**: `_yorozuya/journal/`, `_hirameki_logs/`, `_agent_logs/`, `_claude_code_logs/`, `Logs/`, `_logs/`, `logs/`
- **handoff**: `_yorozuya/handoff/`, `Handoff/`, `_handoff/`, `handoff/`
- **templates**: `Templates/`, `_templates/`, `templates/`

If no match is found for a purpose → ask the user where to create it (suggest the first candidate name by default), then create it after confirmation.

**Step 4 — Write configuration**

Two writes, one per audience.

Per-machine → `~/.claude/vault-local.md` (create if it does not exist):

```
## Vault Structure
vault: {full vault path}
language: {language}
```

Vault layout → `{vault}/AGENTS.md`. If the file already exists, insert or replace only its `## Vault Structure` section and leave everything else untouched:

````
## Vault Structure

The canonical folder layout. Hirameki and other vault-aware tools resolve
their read/write paths from this block. Paths are relative to the vault root.

```yaml
daily: {folder name}/
inbox: {folder name}/
research: {folder name}/
journal: {folder name}/
handoff: {folder name}/
templates: {folder name}/
```
````

Note: `vault-local.md` is machine-specific (platform-dependent vault paths) and should be gitignored if `~/.claude/` is synced across machines. Each machine runs `/hirameki:__init` once to generate it locally. `AGENTS.md` is written once per vault and syncs with the vault itself.

**Migration.** If folder keys currently live in `~/.claude/vault-local.md` or `~/.claude/CLAUDE.md`, copy them into `{vault}/AGENTS.md`, then remove them from the source file and tell the user where the layout now lives. Keep `vault:` and `language:` in `vault-local.md`.

**Step 5 — Shared policies vault (optional)**

Ask the user: "Do you have a shared policies vault? (A vault containing agent-agnostic rules that all AI agents should follow — coding style, security, testing, etc.)"

- **Yes** → "What is the path to the policies directory?" (e.g. `~/Obsidian/agents-vault/openclaw/_takamagahara/policies/`)
  - Verify the path exists and contains `.md` files
  - Create symlink: `~/.claude/rules/policies/ → {policies path}`
  - If symlink already exists → ask whether to update or keep existing
  - Add to `vault-local.md`:
    ```
    shared-policies: {policies path}
    ```

- **No** → skip. No symlink created.

If the user provides a path that doesn't exist:
- Ask: "That path doesn't exist. Do you want to create it? What name?"
- Warn: "Note: the policies directory path will be referenced by symlinks on every machine. Changing this path later requires updating symlinks on all machines."
- If confirmed → create the directory

**Step 5b — Personal policies vault (optional)**

Ask the user: "Do you have personal policies? (Writing style, language preferences, AI philosophy — rules specific to you, not shared with other users)"

- **Yes** → "What is the path to the personal policies directory?" (e.g. `~/Obsidian/br-os-vault/_policies/`)
  - Verify the path exists
  - Create symlink: `~/.claude/rules/personal/ → {personal policies path}`
  - If symlink already exists → ask whether to update or keep existing
  - Add to `vault-local.md`:
    ```
    personal-policies: {personal policies path}
    ```

- **No** → skip.

Same path-doesn't-exist handling and rename cost warning as Step 5.

**Step 6 — Reference doc sync**

- Check whether `{vault}/_hirameki_cmds/` exists
- Does not exist → create folder, copy the reference docs for the chosen language, print: "Reference docs copied to _hirameki_cmds/"
- Exists and non-empty → ask the user whether to overwrite (they may have local edits)
- Exists and empty → copy directly

Language mapping:
- Traditional Chinese → `hirameki-cmds-short-zh-TW.md` + `hirameki-cmds-full-zh-TW.md`
- Japanese → `hirameki-cmds-short-ja.md` + `hirameki-cmds-full-ja.md`
- English or other → `hirameki-cmds-short.md` + `hirameki-cmds-full.md`

If the plugin source files are not found (cache cleared) → skip this step and tell the user to download manually from GitHub.

---

### Mode B: Reconfigure

Triggered when `## Vault Structure` already exists (in `{vault}/AGENTS.md`, `vault-local.md`, or `CLAUDE.md`) and the user runs `/hirameki:__init`.

Read the existing configuration, then ask the user what to update:
1. Language setting
2. A specific folder path
3. Shared policies symlink
4. Personal policies symlink
5. Update reference docs (`_hirameki_cmds/`)
6. Start over completely

Only modify what the user selects — leave all other fields unchanged. Route each write to its owner: language and vault path to `~/.claude/vault-local.md`, folder paths to `{vault}/AGENTS.md`.

"Start over completely" runs the full Mode A flow and asks for confirmation before overwriting the existing configuration.

## Content folder resolution

When commands need to scan the user's content folders, the scope is determined as follows:

Take all top-level folders in the vault root, then exclude:
- Hidden folders starting with `.` (`.obsidian/`, `.claude/`, `.git/`, `.smart-env/`, etc.)
- `_hirameki_cmds/`
- The system-folder subtrees recorded in `## Vault Structure`; do not exclude unrelated siblings when a configured path is nested under a top-level folder

When scanning inside content folders, skip hidden directories, dependency/build directories such as `node_modules`, and files ignored by Git when the vault is a Git repository.

Everything remaining is treated as a user content folder. If no content folders remain, scan all `.md` files in the vault root directly.
