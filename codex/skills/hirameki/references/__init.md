---
description: First-time Codex setup for Hirameki vault discovery and folder configuration
---

Configure Hirameki for Codex in `~/.codex/hirameki-local.md`. This file is machine-specific personal-layer data: never copy it into a repository or the vault.

## Existing configuration

Read `## Vault Structure` from `~/.codex/hirameki-local.md`. Claude configuration may be read only as a migration fallback described by the umbrella skill; do not modify or remove it.

If configuration exists, show its non-secret fields and ask which field to update. Change only the selected fields and wait for confirmation before writing.

## First-time setup

### 1. Detect the vault

Try in order:

1. Current working directory when it contains `.obsidian/`.
2. A valid vault found in the Obsidian application config:
   - Windows: `%APPDATA%/Obsidian/obsidian.json`
   - macOS: `~/Library/Application Support/obsidian/obsidian.json`
   - Linux: `~/.config/obsidian/obsidian.json`
3. Ask the user for the vault root.

Exclude Obsidian's built-in sandbox under its application-data directory. If several vaults remain, list them and let the user choose. Verify that the selected path exists and contains `.obsidian/`.

### 2. Choose language

Ask for Traditional Chinese, English, Japanese, or another user-specified language.

### 3. Resolve folders

For each purpose, use the first existing candidate:

- daily: `_yorozuya/daily/`, `Daily/`, `_daily/`, `daily/`, `Journal/`, `journal/`
- inbox: `Inbox/`, `_inbox/`, `inbox/`, `_Capture/`, `Capture/`
- research: `_yorozuya/research/`, `_hirameki_analysis/`, `_agent_analysis/`, `_claude_code_analysis/`, `Analysis/`, `_analysis/`, `analysis/`
- journal: `_yorozuya/journal/`, `_hirameki_logs/`, `_agent_logs/`, `_claude_code_logs/`, `Logs/`, `_logs/`, `logs/`
- handoff: `_yorozuya/handoff/`, `Handoff/`, `_handoff/`, `handoff/`
- templates: `Templates/`, `_templates/`, `templates/`

For a missing purpose, suggest the first candidate and ask where to create it. Create folders only after confirmation.

### 4. Confirm and write

Show the complete proposed configuration and wait for explicit approval. Then write:

```markdown
## Vault Structure
vault: {full vault path}
language: {language}
daily: {folder}/
inbox: {folder}/
research: {folder}/
journal: {folder}/
handoff: {folder}/
templates: {folder}/
```

Do not create symlinks, import policies, or edit `~/.codex/AGENTS.md` as part of initialization. Those are separate personal-layer operations requiring explicit user requests and the agent-document constitution.

## Reference doc sync

After configuration is approved, offer to sync the user-facing command references into `{vault}/_hirameki_cmds/`:

Resolve source files relative to this skill root under `assets/_hirameki_cmds/`; do not depend on the current working directory or a machine-specific checkout. Before proposing any vault write, verify that both files for the selected language exist. If the source assets are unavailable, report the missing filenames and do not write or create the target folder.

- Traditional Chinese: `hirameki-cmds-short-zh-TW.md` and `hirameki-cmds-full-zh-TW.md`
- Japanese: `hirameki-cmds-short-ja.md` and `hirameki-cmds-full-ja.md`
- English or another language without a dedicated translation: `hirameki-cmds-short.md` and `hirameki-cmds-full.md`

If the folder does not exist, create it only after confirmation. If it is empty, copy the selected reference docs after confirmation. If it is non-empty, show which files would be replaced and require explicit overwrite approval so local edits are not lost. Print the full paths after copying.

## Reconfigure

When configuration already exists, offer these choices:

1. Change language.
2. Change a selected vault or folder path.
3. Update reference docs in `_hirameki_cmds/`.
4. Start over completely.

Modify only the selected fields. `Start over completely` reruns the first-time setup and requires confirmation before overwriting `~/.codex/hirameki-local.md`. It still must not create Claude or Codex policy symlinks or modify personal guidance.

## Content folders

When another workflow needs content folders, take top-level vault folders and exclude hidden folders, `_hirameki_cmds/`, and configured system folders. If none remain, scan Markdown files directly under the vault root.

## Validation

After writing, parse the section again and verify each configured folder resolves under the selected vault. Report the config path and any missing folder; do not silently repair it.
