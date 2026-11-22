---
description: >
  Orient after resuming: what was done, what is still open, what to do next.
  Use at the start of a session when the user asks where they left off, or says
  "我做到哪", "上次進度", "接下來做什麼", "回顧一下",
  "where was I", "what's the state", "catch me up", "what should I do next".
  Also use for task inventories and stuck work; keep the requested scope.
---

For a natural-language request, apply `${CLAUDE_PLUGIN_ROOT}/references/capabilities/natural-routing.md`; do not require the user to name this capability. Preserve the actual request as input.

Input: $ARGUMENTS (optional)
- Empty → default mode
- `tasks [N]` → task inventory; `stuck [N]` → unresolved work and status uncertainty.
- `week [N]` → bounded activity review; no archive or completion inference from file activity.
- `lucky` → compatibility request for `lens random`; use only that explicit exploration, not a default orientation plus exploration.
- A number (e.g. `3`) → look back N days for wrap logs context (default 1)

Recover enough context for the requested outcome; do not scan unrelated sources.

## Scope before tools

- Source-only: when asked to interpret supplied handoff material, answer from that
  material and label current task state unverified. No vault setup or index query
  is needed unless the request also requires current state.
- Resume: Start with the named project's current task authority and repository
  evidence within the supplied scope. Use a handoff when requested or needed to
  resolve a specific gap. If repository evidence suffices and the request needs
  no Vault work, skip Vault setup. Older Next entries provide context and cannot
  override completed, withdrawn or superseded dispositions.
- Inventory: use the full validated task-view procedure below, including paging,
  uncertainty and exceptions. A bounded preview is not a comprehensive inventory.

For Vault-dependent work only, read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and the locations of the wrap-log and inbox folders.
If required configuration is missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

If sources are not named, search the authorized project/folder for the project name or task
ID with available file/search tools; read matching passages before expanding.
Do not enumerate the entire inbox or unrelated projects to orient one project.

For resume with an applicable existing task index, follow Indexed tasks below.
Use the exact lookup for a known ID or a bounded preview to locate it. A closed
indexed disposition cannot be reopened by an older handoff.

Continue the next already authorized action when current evidence confirms that
it is still open, subject to the owning project's rules and scope. For a
status-only question, report the state and proposed next action. If the selected
task is unresolved or blocked, report the precise dependency and complete
independent authorized work.

## Purpose modes

For `next tasks` and `next stuck`, load only the task capability and execute its matching mode, then return without running the orientation below. Preserve numeric windows and supplied scope:
Translate capability input once: `tasks N scope` becomes `N scope` in default mode; `stuck N scope` remains `stuck N scope`. Do not strip the numeric window or scope.
`${CLAUDE_PLUGIN_ROOT}/references/capabilities/tasks.md`.
For `week`, use the same effective view with the requested date window; compare evidenced intentions, actions and blockers. File mtime is activity context, not task state or proof of priority.
For an explicit `lucky` request use the lens random contract, not the removed constellation appendix. Bare next never runs random exploration.

## Indexed tasks

When the request needs an indexed task or inventory, load only the
`## Task view (shared step)` section of `${CLAUDE_PLUGIN_ROOT}/references/capabilities/tasks.md`.
Use its exact-ID lookup or paged view; apply its validation, fallback, and
global diagnostics. Use that result in the requested next output.

For an explicit restore request, read `${CLAUDE_PLUGIN_ROOT}/codex/skills/hirameki/references/task-restore/operation.md`
in a separate tool call and follow its lookup, approval, validation, and
readback procedure.

## Relevant sources

- Owning project task authority and current status for the requested scope
- Task view (shared step): the effective todo view when an index exists
- Session activity: files created or modified, decisions made, commits pushed
- Any open items, blockers, or unresolved questions raised during the session
- Inbox: only when requested or linked to the current work
- Daily wrap/handoff: relevant project passages in the requested date window;
  yesterday is a starting point, not a reason to ignore a later disposition

## Output format

Use the requested language, otherwise the resolved vault language when applicable.
Lead with current position, the next action and any blocker. Cite relevant source
passages and distinguish recorded context from checked current state. For a
source-only answer, explicitly state that the owning task authority/index was
not checked; do not call an unchecked index absent.

For resumption, report the action actually continued and its verification, or
what specifically prevents it. Preserve the reader's required status labels,
uncertainties, exceptions and omitted counts whenever a task view was used.
For an inventory/week request, use its requested scope and the view above rather
than reducing it to one next action. Done, inbox and yesterday recaps appear only
when relevant or requested; never require a fixed menu or automatic wrap-up.

---

## Rules

- Infer scope from available context; ask only if a material ambiguity cannot be resolved safely.
- Keep each section tight: no padding, no filler
- Do not infer all work is done from an empty partial/unavailable view or minimal session activity
- Use [[wiki link]] format for all note references
- A file listing shows files only and can miss empty folders; never state or act on a folder or file being missing unless a direct check confirms it; otherwise say no files were found there.
