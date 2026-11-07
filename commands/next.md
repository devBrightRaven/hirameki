---
description: >
  Orient after resuming: what was done, what is still open, what to do next.
  Use at the start of a session when the user asks where they left off, or says
  "我做到哪", "上次進度", "接下來做什麼", "回顧一下",
  "where was I", "what's the state", "catch me up", "what should I do next".
  Also use for task inventories and stuck work; keep the requested scope.
---

For a natural-language request, apply `${CLAUDE_PLUGIN_ROOT}/references/capabilities/natural-routing.md`; do not require the user to name this capability. Preserve the actual request as input.

Only before vault access, read `vault:` from `~/.claude/vault-local.md` for the vault root, then read `## Vault Structure` from `<vault>/AGENTS.md` (fall back to `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md` for setups predating 1.4.3) to get the vault path and the locations of the wrap-log and inbox folders.
For a vault-dependent scope, if required configuration is missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

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
- Resume: locate the named project's handoff and owning task authority within the
  supplied scope. Check current task dispositions and repository evidence before
  choosing work; an older Next entry is context, not execution authority.
- Inventory: use the full validated task-view procedure below, including paging,
  uncertainty and exceptions. A bounded preview is not a comprehensive inventory.

Resolve vault configuration only before an actual vault read/write. If sources
are not named, search the authorized project/folder for the project name or task
ID with available file/search tools; read matching passages before expanding.
Do not enumerate the entire inbox or unrelated projects to orient one project.

For resume with an applicable existing task index, use the reader resolution and
validation rules below with `--task-id <exact-id>` for a known ID; otherwise use
its bounded preview to locate the item. Keep global diagnostics and completeness
limits. This is a read-only state check, not a restore: load the restore operation
guide only when restore is explicitly requested. A closed indexed disposition
cannot be reopened by an older handoff.

Once state is checked, continue the next action already authorized by the user,
subject to the owning project's rules and scope. A status-only question requires
an answer, not execution. If blocked, report the precise dependency and complete
independent authorized work; do not turn every pickup into another approval menu.

## Purpose modes

For `next tasks` and `next stuck`, load only the task capability and execute its matching mode, then return without running the orientation below. Preserve numeric windows and supplied scope:
Translate capability input once: `tasks N scope` becomes `N scope` in default mode; `stuck N scope` remains `stuck N scope`. Do not strip the numeric window or scope.
`${CLAUDE_PLUGIN_ROOT}/references/capabilities/tasks.md`.
For `week`, use the same effective view with the requested date window; compare evidenced intentions, actions and blockers. File mtime is activity context, not task state or proof of priority.
For an explicit `lucky` request use the lens random contract, not the removed constellation appendix. Bare next never runs random exploration.

## Task view (shared step)

A valid restore_pending task is visible and actionable now; do not require waiting for scheduled integration before the task can resume. Only the designated writer integrates the formal index; do not suggest that this reader performs that operation. Restoring visibility does not grant permission to execute the underlying task or its external actions.

### Read-only lookup before restore

For restore, read the delivered small operation guide in one separate tool call:
`references/task-restore/operation.md` under the resolved Codex skill root, or
`codex/skills/hirameki/references/task-restore/operation.md` under the package root.
Then call the bundled reader's `--restore-contract` separately for canonical
schemas, required field sources, matching rules and digest recipe. Use its
read-only `--validate-restore` stdin interface to check the in-memory pair before
native exclusive saves. Do not search implementation files or batch multiple
large documents to discover the schema. The procedure and public contract are
delivered with both runtime entries; no source checkout knowledge is required.

For an explicitly requested restore, use the same verified reader with
`--task-id <exact-id>` before creating any request or approval. Read the gate
version from its bundled file and use the resolved vault/data paths. This query
uses `python -B -X utf8 "<HIRAMEKI_TASK_ROOT>/scripts/task_view_cli.py" --vault <vault> --data <research>/tidy/tasks --gate-version <G> --task-id <exact-id>`
with the verified interpreter. Do not substitute a hard-coded gate version.
The existing user approval and immutable request/approval matching requirements
remain unchanged; neither this lookup nor a successful validation authorizes a write.
The reader
validates the entire index, sources and restore records first, then returns the
selected task (including archived tasks), index/view revision, expected/current
source digests and validation. Never print the full index to discover one task.
The task query is not a complete inventory; retain its global uncertainty count,
uncertain task IDs and all exceptions. A verified selected task does not erase
global anomalies or grant approval to restore or execute work.

Missing IDs return `task-not-found` and a nonzero exit; never treat this as a
normal empty list. `--task-id` cannot be combined with paging. Its default complete
UTF-8 response ceiling is 16384 bytes (`--max-output-bytes`, 1024..65536).
If the task or global diagnostics exceed that limit, the query returns nonzero
`output-limit-exceeded` with required bytes, counts and `details_returned=false`;
stop and report unavailable, never silently truncate or weaken validation.
Keep the query's revisions and source digests when constructing the immutable
restore request according to the shared restore contract. After each separately
approved request/approval pair, immediately run the same reader to confirm
effective visibility; do not wait for scheduled index integration.

Resolve `{research}` from `## Vault Structure`. If `<vault>/<research>/tidy/tasks/index.json` exists, run:

`python3 -B -X utf8 "${CLAUDE_PLUGIN_ROOT}/scripts/task_view_cli.py" --vault <vault> --data <research>/tidy/tasks --gate-version <G> --page-size 20 --offset 0`

This is a bounded preview when `pagination.all_displayed` is false. For active, uncertain and exceptions, report total, returned, earlier_not_displayed, remaining and next_offset. Unshown uncertain items stay visible as counts; never claim all done or a complete inventory from a partial page.

For subsequent pages use the reported next_offset and pin both --expected-revision <index_revision> and --expected-view-revision <view_revision> from the first response. Changed index, source or restore overlay invalidates the combined inventory: report it and stop. Discard the completeness claim, do not combine the pages, and do not retry through another interpreter or fall back to raw notes. A later empty page does not mean the full list is empty.

A comprehensive inventory requires all relevant pages. A bounded orientation may show a preview with totals and next offsets, but must not rank unseen tasks. If output is too large, reduce page size and read complete records; tool truncation is not successful inspection. “Every” below means every returned record plus explicit omitted counts until all requested pages have been read. Paging does not weaken full reader validation or the archive gate.


Before running, check that `${CLAUDE_PLUGIN_ROOT}/scripts/task_view_cli.py` exists. If it is missing, say so explicitly (「外掛目錄缺少任務檢視腳本」: the installed plugin payload does not yet ship the task-view scripts, a plugin payload limitation), then use the raw-note fallback below as unverified candidates only; never imply the task view ran or that nothing is open.

Run the line with `python3`; if it cannot start (command not found, or a Windows Store stub error / non-JSON output mentioning the Microsoft Store), run the same line with `python`. `<G>` is the single line of `${CLAUDE_PLUGIN_ROOT}/scripts/TASK_GATE_VERSION`. If that file is missing, empty or not exactly one line, the gate version is unavailable: report it, never substitute a remembered or hard-coded value, do not run the reader, and use the raw-note fallback below as unverified candidates only; never imply the task view ran or that nothing is open. The command is read-only. Parse its JSON (`active`, `uncertain`, `exceptions`) and show three sections:

- **有效待辦**: every `active` task with summary and source link. Mark `restore_pending` as 「取回申請待整合」 and `source_changed` as 「來源已變更」.
- **狀態未確認**: every `uncertain` task with its reason (the `exceptions` entry for that task_id) and source link. Keep each item's own reason visible (for example a stale gate version versus missing evidence); never merge uncertain items under one generic label.
- **例外**: every `exceptions` entry with its path.

Never hide uncertain tasks or exceptions, and never read an empty list as "all done" when `view_status` is not `complete`. A task the view lists as archived is not open: do not re-derive it from raw notes. List every returned record individually; never collapse records into ID ranges or "and N more" without the omitted counts above. A non-zero exit whose JSON exception reason is `page-index-revision-changed` or `page-effective-view-changed` (a revision mismatch on a later page) is not an unreadable index: report the mismatch and stop, with no raw-note fallback. Any other non-zero exit or unparseable output: say 「待辦索引無法讀取」 and fall back to the raw-note behavior below.

If no index exists, keep the raw-note behavior below unchanged and print exactly one line: 「尚無有效待辦索引，以下由原始紀錄推導，未經歸檔驗證。」

The raw-note fallback excludes items explicitly finished (「已完成」, 「完成」, `✓ Done`, `[x]`, `Done`), withdrawn (「撤回」, `withdrawn`) or superseded (「已取代」, `superseded`), including a later closing Wrap block in the scanned window. Interpret marks in context: 未完成 is not closed; a replacement is a separate item. Unmarked items without explicit status evidence are `status uncertain`, not confirmed active tasks. Keep them visible in a separate uncertain list in default and stuck modes; never automatically archive them. Explicit unfinished or reopened evidence may establish active status; missing an index or repeating an Open item does not. repetition cannot reopen a closed item, only newer explicit reopening does. If an existing index is unreadable, raw notes produce unverified candidates, not authoritative active or completed state; do not silently discard indexed closure or bypass a cross-page revision mismatch.

In this command the view supplies 還開著的 and 下一步 below.

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
