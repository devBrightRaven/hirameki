---
name: hirameki
description: Use when the user invokes or mentions a Hirameki command such as /__init, /wrap, /journal, /handoff, /harvest, /mekiki, /next, /tasks, /tidy, /triage, /arc, /bridge, /challenge, /compose, /critique, /frame, /graduate, /lens, /pulse, or /reflect; or asks Codex to initialize, capture, summarize, route, tidy, journal, hand off, critique writing, or reason over Obsidian vault notes with Hirameki.
---

# Hirameki

Run Hirameki's Obsidian vault workflows in Codex while keeping Claude Code commands unchanged. This skill is an umbrella router: load only the one reference file that matches the requested Hirameki workflow.

## Vault Config Resolution

Before any workflow that reads or writes the vault, resolve vault configuration in this order:

1. Read `## Vault Structure` from `~/.codex/hirameki-local.md`.
2. If missing, fall back to `~/.claude/vault-local.md` for migration compatibility.
3. If still missing, fall back to `~/.claude/CLAUDE.md`.
4. If required fields are missing, stop and respond: `Setup not complete. Please configure ~/.codex/hirameki-local.md or run the Hirameki init flow in Claude first.`

Treat Claude config as a migration fallback only. Do not copy Claude local config into a repository.

When a reference says to read `~/.claude/vault-local.md`, substitute the config resolution above. Follow the reference's workflow after the vault path, daily folder, templates folder, content folders, and language are known.

For `__init`, keep Claude's folder resolution behavior exactly:

- Detect existing vault folders first.
- Use the same candidate folder order listed in `references/__init.md`.
- If no match is found, ask the user where to create that folder and suggest the first candidate as a default.
- Do not force `_yorozuya/` or any Codex-specific folder structure.
- The only Codex-specific difference is the per-machine config target: write `~/.codex/hirameki-local.md` instead of `~/.claude/vault-local.md`.

## Command Routing

Map the user's command name to the same-named reference. Accept forms such as `/wrap`, `wrap`, `hirameki wrap`, and `hirameki:wrap`.

| User intent | Load |
|---|---|
| `/__init`, `init`, `hirameki init` | `references/__init.md` |
| `/arc` | `references/arc.md` |
| `/bridge` | `references/bridge.md` |
| `/challenge` | `references/challenge.md` |
| `/compose` | `references/compose.md` |
| `/critique` | `references/critique.md` |
| `/frame` | `references/frame.md` |
| `/graduate` | `references/graduate.md` |
| `/handoff` | `references/handoff.md` |
| `/harvest` | `references/harvest.md` |
| `/journal` | `references/journal.md` |
| `/lens` | `references/lens.md` |
| `/mekiki` | `references/mekiki.md` |
| `/next` | `references/next.md` |
| `/pulse` | `references/pulse.md` |
| `/reflect` | `references/reflect.md` |
| `/tasks` | `references/tasks.md` |
| `/tidy` | `references/tidy.md` |
| `/triage` | `references/triage.md` |
| `/wrap` | `references/wrap.md` |

This Codex adapter covers the 20 Claude command names as same-name references.

## Execution Rules

- Load only the matching reference file, not every reference.
- Treat `$ARGUMENTS` in a reference as the text after the Hirameki command name in the user's message. If no text remains, follow the reference's empty-argument behavior.
- Use the language specified in `## Vault Structure` unless the user explicitly asks otherwise.
- Preserve Obsidian frontmatter, wiki links, and existing note style.
- Prefer reversible, append-only edits for journal, daily, handoff, and knowledge notes.
- Do not publish, sync, delete, or move vault content unless the chosen workflow explicitly requires it and the user confirms.
- If a reference asks for confirmation before writing, show the proposed content and wait.
- Treat the vault as human knowledge storage, never as Codex runtime configuration.
- A reference may propose changes to Codex personal guidance only in `~/.codex/AGENTS.md` or an existing owning Codex personal-layer file. Never edit personal guidance without the user's explicit approval, and never route Codex corrections into Claude config.
- Project-specific guidance belongs in the applicable project `AGENTS.md`, subject to that repository's instructions.
- If the user asks for several Hirameki commands at once, run them in the order requested. If order is unclear, use: scan/read first, write later.
- When a reference says `source: claude-code`, use `source: codex` for files created by Codex unless the user explicitly wants to preserve the Claude-origin label.

## Claude-Specific Feature Adaptation

Some references were originally written as Claude Code commands. Adapt them in Codex as follows:

- `__init`: write Codex per-machine config to `~/.codex/hirameki-local.md`. Do not migrate or remove Claude config unless the user explicitly asks.
- `__init` testing: never test initialization against a real user vault such as `br-os-vault` or `agents-vault`. Use a disposable fixture vault or a copied sandbox vault, and write config to a test-only location unless the user explicitly asks to configure the real machine.
- `critique`: run independent reviewers through native Codex subagents when available. An optional external reviewer may use the currently installed CLI only after checking its help, with read-only instructions and no unsupported flags. Do not invoke an external CLI merely to duplicate the current Codex reviewer, do not permit external side effects, and do not claim multi-model consensus unless the recorded reviewers actually used distinct models.
- Hooks: references to Claude SessionStart/SessionEnd hooks are informational only in Codex unless a Codex hook integration is explicitly implemented later.

## Maintaining This Adapter

Claude Code remains the command-native surface for Hirameki. Keep `commands/` intact.

Codex should use this umbrella skill plus `references/*.md`. When a Claude command changes, sync the corresponding Codex reference and keep the command name stable so migration muscle memory is preserved.
