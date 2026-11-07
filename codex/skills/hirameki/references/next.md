---
description: >
  Orient after resuming: what was done, what is still open, what to do next.
  Use at the start of a session when the user asks where they left off, or says
  "我做到哪", "上次進度", "接下來做什麼", "回顧一下",
  "where was I", "what's the state", "catch me up", "what should I do next".
  Also use for task inventories and stuck work; keep the requested scope.
---

For a natural-language request, apply `references/capabilities/natural-routing.md` under the currently loaded skill root; do not require the user to name this capability. Preserve the actual request as input.

Only before vault access, resolve vault configuration through the umbrella Hirameki adapter for the needed folders from `## Vault Structure` in `<vault>/AGENTS.md`; this reference does not read Claude configuration.
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
`references/capabilities/tasks.md` under the actually loaded skill root.
For `week`, use the same effective view with the requested date window; compare evidenced intentions, actions and blockers. File mtime is activity context, not task state or proof of priority.
For an explicit `lucky` request use the lens random contract, not the removed constellation appendix. Bare next never runs random exploration.

## Task view (shared step)

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

Read this reference, vault AGENTS.md and scripts/TASK_GATE_VERSION explicitly as
UTF-8. On Windows PowerShell use `Get-Content -LiteralPath <path> -Encoding utf8`.
If a read is garbled, reread that same file with UTF-8 before interpreting it;
do not replace the contract with remembered or guessed text. Preserve exact zh-TW
labels in the final response: 「有效待辦」, 「狀態未確認」, 「例外」,
「取回申請待整合」 and 「來源已變更」. Treat them as literal status labels,
including inside Open/Next sections; do not paraphrase them as 待排程整合 or 狀態待確認.

Resolve vault and `{research}` through the umbrella adapter. When `<vault>/<research>/tidy/tasks/index.json` exists, resolve `<HIRAMEKI_TASK_ROOT>` from an explicitly configured machine-local `task_view_root`, otherwise the directory containing the actually loaded Hirameki SKILL.md when it contains the bundled scripts, otherwise the verified source checkout containing this loaded reference. Check that both `scripts/task_view_cli.py` and `scripts/TASK_GATE_VERSION` exist there. Do not use Claude configuration, CLAUDE_PLUGIN_ROOT, a guessed cache path, or a recursive filesystem search. If an explicit root is invalid, report unavailable rather than silently switching roots. A plugin-only payload without these files is not yet wired; report that limitation.

`python3 -X utf8 "<HIRAMEKI_TASK_ROOT>/scripts/task_view_cli.py" --vault <vault> --data <research>/tidy/tasks --gate-version <G> --page-size 20 --offset 0`

This is a bounded preview, not a complete baseline when `pagination.all_displayed` is false. For each of active, uncertain and exceptions, retain the total, returned, earlier_not_displayed, remaining and next_offset in the report; do not claim all done, no exceptions or a complete inventory from an incomplete page. Totals describe the full validated view, not just the displayed items. Unshown uncertain items remain explicitly visible as a count, not silently discarded or promoted to active tasks.

For further pages, replace --offset with a reported next_offset and include --expected-revision <index_revision> and --expected-view-revision <view_revision> from the first response. Both tokens must match; index, source or restore-overlay changes invalidate a combined inventory. Report that change and discard any combined completeness claim; do not combine incompatible pages, retry via another interpreter, or silently fall back to old notes. A later empty page never proves an empty task list.

Read further pages when needed for the requested scope; a requested comprehensive inventory requires all relevant pages. A bounded orientation/checkpoint may report a preview with totals and deferred next offsets, but must not rank unseen tasks or conclude they are finished. If an individual page is too large for the output channel, reduce page size and read complete records; tool truncation is not successful inspection. This presentation option does not reduce full reader validation or change the writer/dry-run archive gate.

Read `<G>` from that root's `scripts/TASK_GATE_VERSION`; missing/blank/multiline version is unavailable, never a hard-coded fallback. Use a verified Python 3.10+ executable: python3 then python only when the first cannot launch (including a Store stub). Do not retry a real CLI data/schema failure as an interpreter failure. On Windows use PowerShell native argument arrays, not cmd wrappers. This step is read-only.

Invoke the script directly with that interpreter; do not nest interpreter subprocesses or replace the CLI with runpy. A policy or access denial makes this launch unavailable: report it, do not rewrite the launch to evade the denial. The missing-command/Store-stub fallback above is not permission to bypass an access restriction.

A valid restore_pending task is visible and actionable now; do not require waiting for scheduled integration before the task can resume. Only the designated writer integrates the formal index; do not suggest that this reader performs that operation. Restoring visibility does not grant permission to execute the underlying task or its external actions.

Show three separately labelled lists: 「有效待辦」 (active), 「狀態未確認」 (uncertain), 「例外」 (exceptions). Do not blend uncertain items into the active list; these lists may be nested inside the entry's normal output sections. Mark restore_pending as 「取回申請待整合」, source_changed as 「來源已變更」, and partial/unavailable explicitly. Retain all in-scope uncertainty and exception paths. An empty partial/unavailable result never means all done. Archived indexed items are not reopened by old note text. Raw notes may add context or identify unindexed candidates, not override existing dispositions.

If no index exists, print 「尚無有效待辦索引，以下由原始紀錄推導，未經歸檔驗證。」 and use the existing raw-note flow. If an existing index/CLI cannot be read, print 「待辦索引無法讀取」; any raw-note fallback is explicitly unverified candidates, not authoritative active or completed state. Do not write an index or add confirmation stops.

Raw-note fallback must respect explicit task dispositions: exclude the same item marked finished (已完成, 完成, [x], ✓ Done), withdrawn (撤回, withdrawn), or superseded (已取代, superseded), including a later closing Wrap block in the scanned window. Interpret the mark in context, not by substring: 未完成 is not closed; a replacement remains a separate open item. Unmarked items without explicit status evidence are `status uncertain`, not confirmed active tasks. Keep them visible in a separate uncertain list in default and stuck modes; never automatically archive them. Explicit unfinished or reopened evidence may establish active status; missing an index or repeating an Open item does not. Repetition does not reopen a closed item; only newer explicit reopening does.


- When valid, the shared task view supplies Open and Next; raw sources only add context or explicitly unindexed candidates.

## Relevant sources

- Owning project task authority and current status for the requested scope
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
