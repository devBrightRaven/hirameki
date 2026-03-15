---
description: First-time setup and vault configuration
---

## Overview

`__init` handles first-time setup of the Hirameki environment. Once complete, the result is written to `~/.claude/CLAUDE.md`. All other commands read from there directly — they do not call `__init` again.

## How other commands read configuration

Before executing, every other hirameki command:

1. Reads the `## Vault Structure` section from `~/.claude/CLAUDE.md`
2. If not found or missing required fields → stop and respond: "Setup not complete. Please run `/hirameki:__init` first."
3. If found → use as-is, no further validation
4. If a path is invalid or unreadable during execution → respond: "Configuration error. Please run `/hirameki:__init` to reconfigure."

Vault root resolution: use the `vault:` field in `## Vault Structure` if present; otherwise read `path` from the `## Vault` section in `~/.claude/CLAUDE.md`.

## Execution modes

### Mode A: First-time setup

Triggered when `## Vault Structure` does not exist in `~/.claude/CLAUDE.md`, or when the user runs `/hirameki:__init` with no existing configuration.

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
- **templates**: `Templates/`, `_templates/`, `templates/`

If no match is found for a purpose → ask the user where to create it (suggest the first candidate name by default), then create it after confirmation.

**Step 4 — Write configuration**

Write the following to `~/.claude/CLAUDE.md` (create if it does not exist):

```
## Vault Structure
vault: {full vault path}
language: {language}
daily: {folder name}/
inbox: {folder name}/
research: {folder name}/
journal: {folder name}/
templates: {folder name}/
```

**Step 5 — Reference doc sync**

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

Triggered when `## Vault Structure` already exists and the user runs `/hirameki:__init`.

Read the existing configuration, then ask the user what to update:
1. Language setting
2. A specific folder path
3. Update reference docs (`_hirameki_cmds/`)
4. Start over completely

Only modify what the user selects — leave all other fields unchanged.

"Start over completely" runs the full Mode A flow and asks for confirmation before overwriting the existing configuration.

## Content folder resolution

When commands need to scan the user's content folders, the scope is determined as follows:

Take all top-level folders in the vault root, then exclude:
- Hidden folders starting with `.` (`.obsidian/`, `.claude/`, `.git/`, `.smart-env/`, etc.)
- `_hirameki_cmds/`
- All system folders recorded in `## Vault Structure`

Everything remaining is treated as a user content folder. If no content folders remain, scan all `.md` files in the vault root directly.
