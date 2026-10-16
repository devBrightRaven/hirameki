---
name: hirameki
description: Use when invoking Hirameki workflows; capturing, organizing, finding concepts in, or checking stuck work from Obsidian vault notes; or preserving decisions, journals and handoffs. Also use for decision-forming intent such as "should I", "which one", "torn between", "pros and cons", "要不要", "應該選", "該不該", "猶豫", "どうしよう", "どちら", "迷って", or "比較". Not for passing preferences or mechanical actions with no meaningful choice.
---

# Hirameki

Run Hirameki's Obsidian vault workflows in Codex with the same shared capabilities as Claude Code commands. This skill is an umbrella router: load only the one reference file that matches the requested Hirameki workflow.

## Vault Config Resolution

Before any workflow that reads or writes the vault, resolve vault configuration in this order:

1. Use explicitly supplied current-task vault root and language when present.
2. Resolve missing values from Codex's own `~/.codex/hirameki-local.md`. Never read another agent's configuration, personal memory or runtime as a fallback.
3. After resolving the vault root, read folder paths from `## Vault Structure` in `{vault}/AGENTS.md`. This is the canonical source for daily, inbox, research, journal, handoff, templates, and content-folder resolution.
4. If the vault root or required canonical folder paths are still missing, stop and respond: `Setup not complete. Please run hirameki:init to configure the vault root or canonical folder layout.`

Explicit current-task settings may support an isolated trial without a machine-local file; they do not authorize persisting that configuration. Missing ordinary setup is handled by `hirameki:init`, not cross-agent discovery.

Machine-local config stores the vault root and language and may name an explicitly configured `task_view_root` for the verified shared reader checkout. That executable location is Codex runtime configuration, not vault folder layout. Never duplicate vault folder paths outside `{vault}/AGENTS.md`.

For `__init`, keep Claude's folder resolution behavior exactly:

- Detect existing vault folders first.
- Use the same candidate folder order listed in `references/__init.md`.
- If no match is found, ask the user where to create that folder and suggest the first candidate as a default.
- Do not force `_yorozuya/` or any Codex-specific folder structure.
- Write the vault root and language to `~/.codex/hirameki-local.md`; write the canonical folder layout to `{vault}/AGENTS.md`.

## Command Routing

Natural-language requests do not require command names. Apply `references/capabilities/natural-routing.md` when selecting next, lens or compose, loading only the selected operation. Resume recorded work, synthesize named notes, or develop supplied notes into a work without making the user choose a routing menu. Ordinary short edits still use the installed language-writing entry directly.

Five primary entries: **next, lens, compose, decision-trace, triage**.
Specialized entries: **tidy, mekiki, init**. Permanent direct recording shortcuts
**wrap, journal, handoff** stay available without requiring a full triage.

`decision-trace` accepts only `decision-trace`, `/decision-trace`, and `hirameki:decision-trace`.
Other workflows accept bare, slash, `hirameki name` or `hirameki:name` forms.
Load only the selected contract. No unsolicited vault-wide scan or startup hook.

| User intent | Load |
|---|---|
| `/__init`, `init`, `hirameki init`, `hirameki:init`, `/hirameki:__init` | `references/__init.md` |
| Continue, orient, list tasks or inspect stuck work | `references/next.md` |
| Explore history, positions, relationships, concepts or patterns | `references/lens.md` |
| Select vault notes, assemble a sourced work or prepare a requested vault artifact | `references/compose.md` |
| Form or preserve a consequential decision | `references/decision-trace.md` |
| Close the session with only useful artifacts | `references/triage.md` |
| Maintenance, task-archive proposals or rule review | `references/tidy.md` |
| External research intake | `references/mekiki.md` |
| Direct progress record | `references/wrap.md` |
| Direct journal or lesson record | `references/journal.md` |
| Direct handoff | `references/handoff.md` |

### Transitional names

The following are small compatibility redirects for the first consolidation release,
not parallel workflows. Their exact mapping is recorded in `references/workflow-routing.json`;
do not remove them until the following release and an authorized migration.
Metadata hiding is unverified; do not claim the host hides these commands.

| Old name | Reference | Destination |
|---|---|---|
| arc | `references/arc.md` | lens history |
| bridge | `references/bridge.md` | lens bridge |
| challenge | `references/challenge.md` | lens challenge |
| harvest | `references/harvest.md` | lens opportunities |
| graduate | `references/graduate.md` | lens cards |
| reflect | `references/reflect.md` | compose voice |
| frame | `references/frame.md` | compose frame |
| critique | `references/critique.md` | compose review |
| tasks | `references/tasks.md` | next tasks; stuck → next stuck |
| pulse | `references/pulse.md` | week/default → next week; patterns → lens patterns; snapshot → tidy snapshot |

Natural concept-discovery requests (including former `xuanniao-find-concepts`)
use lens cards. Stuck requests (including former `xuanniao-whats-stuck`) use
next stuck, not a recap. A mechanical typo is not a meaningful decision.
Preserve the requested project, input and scope; never run all five entries.

## Execution Rules

- Load only the matching reference file, not every reference.
- For explicit commands, `$ARGUMENTS` is the remaining text after the command name. For natural-language requests, it is the actual request and supplied scope, not an empty string. Only genuinely empty input uses empty-argument behavior.
- Use the language specified in `## Vault Structure` unless the user explicitly asks otherwise.
- Preserve Obsidian frontmatter, wiki links, and existing note style.
- Prefer reversible, append-only edits for journal, daily, handoff, and knowledge notes.
- Do not publish, sync, delete, or move vault content unless the chosen workflow explicitly requires it and the user confirms.
- If a reference asks for confirmation before writing, show the proposed content and wait.
- Treat the vault as human knowledge storage, never as Codex runtime configuration.
- A file listing shows files only and can miss empty folders; never state or act on a folder or file being missing unless a direct check confirms it; otherwise say no files were found there.
- A reference may propose changes to Codex personal guidance only in `~/.codex/AGENTS.md` or an existing owning Codex personal-layer file. Never edit personal guidance without the user's explicit approval, and never route Codex corrections into Claude config.
- Project-specific guidance belongs in the applicable project `AGENTS.md`, subject to that repository's instructions.
- If the user asks for several Hirameki commands at once, run them in the order requested. If order is unclear, use: scan/read first, write later.
- When a reference says `source: claude-code`, use `source: codex` for files created by Codex unless the user explicitly wants to preserve the Claude-origin label.

## Claude-Specific Feature Adaptation

Some references were originally written as Claude Code commands. Adapt them in Codex as follows:

- `__init`: write Codex per-machine config to `~/.codex/hirameki-local.md`. Do not migrate or remove Claude config unless the user explicitly asks.
- `__init` testing: never test initialization against a real user vault such as `br-os-vault` or `agents-vault`. Use a disposable fixture vault or a copied sandbox vault, and write config to a test-only location unless the user explicitly asks to configure the real machine.
- `compose review`: use the host's existing authorized independent-review pipeline; unavailable reviewers remain unavailable, not simulated consensus.
- Hooks: references to Claude SessionStart/SessionEnd hooks are informational only in Codex unless a Codex hook integration is explicitly implemented later.

## Maintaining This Adapter

Claude Code remains the command-native surface. Maintain the same five primary purposes, specialized entries, direct shortcuts and transitional redirects in both surfaces.

Codex should use this umbrella skill plus `references/*.md`. When a Claude command changes, sync the corresponding Codex reference and keep the command name stable so migration muscle memory is preserved.
