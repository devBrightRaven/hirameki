---
description: Read-only task completion proposals and explicit content health checks
---

Resolve vault configuration through the umbrella Hirameki adapter. For task proposals,
require the vault root, research folder and language; content folders are not a task-reader prerequisite.
For explicit metadata/content modes, resolve content folders using the existing `references/__init.md`
rule: top-level folders minus hidden and configured system subtrees, then root Markdown if none remain.
Do not invent a required `content` field or persist setup during a read-only trial.
If the vault root or required research/language fields are missing, stop and
respond: "Setup not complete. Please run `/hirameki:__init` first."

## Review and snapshot modes

`tidy review` loads only `references/capabilities/review.md` under the loaded skill root. Preserve the requested scope and date window; report source-anchored corrections and lessons proposals without automatic rule promotion.

`tidy snapshot` gives a bounded read-only inventory of the explicitly selected scope, with file counts, roles, observed activity and coverage limits. Exclude generated/dependency and private runtime material. Dates and mtime describe activity, not task state or validity. Do not write a report, run another maintenance mode or add a startup hook.

Recognize these explicit modes before the default task proposals; return after their selected contract.

## Task proposals (default; `tidy tasks`)

This entry shares the effective task view with next/tasks/triage. Interactive tidy
only reports proposals; it never archives, integrates restores, creates authority,
or asks the user to save a dry-run report. Source narratives remain unchanged.

Read the loaded reference, vault AGENTS.md and gate as UTF-8. On Windows PowerShell
use `Get-Content -LiteralPath <path> -Encoding utf8`; do not read without an explicit
encoding, or reconstruct garbled Chinese labels from memory.

Resolve `<HIRAMEKI_TASK_ROOT>` from an explicitly configured machine-local
`task_view_root`, otherwise the directory containing the actually loaded Hirameki
SKILL.md when it contains bundled scripts, otherwise the verified source checkout
containing this loaded reference. If an explicit root is invalid, report unavailable
rather than silently switching roots. Do not guess cache paths, search recursively
for another root, or read another agent's settings. Require
`scripts/task_view_cli.py`, `scripts/tidy_dry_run.py` and `scripts/TASK_GATE_VERSION`.
Read the gate from this one version file; missing/blank/multiline is unavailable.
Use a verified Python 3.10+ executable: python3, then python only when python3 cannot
launch (including a Store stub). A real data/schema failure is not an interpreter
failure. Use native argument arrays on Windows; invoke the CLI directly, without
runpy or nested interpreter subprocesses. An access denial stops the invocation.

`python3 -B -X utf8 "<HIRAMEKI_TASK_ROOT>/scripts/tidy_dry_run.py" --vault <vault> --data <research>/tidy/tasks`

This CLI loads the full effective view without presentation paging and always
returns `write_authorized: false`. Read actual sources and completion evidence
before endorsing any completion_candidate: declaration consistency does not prove
semantic truth or human approval. Classifications: completion_candidate (candidate
only), incomplete, unknown, conflict. Show candidate IDs/source paths and reasons
for excluded tasks, including progress, deployment dependencies, missing/stale
evidence, changed sources, and pending restores. Historical unresolved records
remain uncertain, never become archival proposals or active tasks automatically.

Use these exact zh-TW section/status labels, preserving UTF-8: 「有效待辦」,
「狀態未確認」, 「例外」, 「取回申請待整合」, 「來源已變更」.
The proposal CLI returns assessments rather than full active source records; when
task details are needed, read the same root's task_view_cli with the same gate:

`python3 -X utf8 "<HIRAMEKI_TASK_ROOT>/scripts/task_view_cli.py" --vault <vault> --data <research>/tidy/tasks --gate-version <G> --page-size 20 --offset 0`

Pin additional pages using both --expected-revision and --expected-view-revision.
Do not combine different revisions or infer a complete inventory from a bounded
preview. Disclose all totals, remaining counts, partial/unavailable and exception
paths. A requested full inventory needs all pages. A valid restore_pending is
actionable now, labelled 「取回申請待整合」; formal integration belongs to the single
authorized writer and does not authorize executing the underlying task.

If no index exists, report 「尚無有效待辦索引，無法執行任務歸檔試算。」 and retain
raw notes as unverified candidates only. An unreadable existing index reports
「待辦索引無法讀取」, never all done. Old Wrap text cannot reopen indexed archives.
Do not create an index, run a writer or change notes as a fallback.

## Explicit content modes

## Modes

Select which checks to run based on $ARGUMENTS:

| Call | Runs |
|------|------|
| `tidy metadata` | Missing field check + Consistency check |
| `tidy tags` | Tag convergence analysis only |
| `tidy fix` | Missing + Consistency + Auto-fix |
| `tidy full` | All blocks |
| `tidy lint` | Content health check (contradictions, stale, orphans, dead links) |

Only run the blocks for the selected mode — omit all others from the report.

## Scan scope

- All content folders (recursive)
- All files in the inbox folder
- Last 30 days in the wrap folder
- Skip hidden directories, dependency/build directories such as `node_modules`, and files ignored by Git when the vault is a Git repository

## Check blocks

### Missing field check (tidy / fix / full)
- Files with no frontmatter
- Files with frontmatter but missing required fields (required: tags, status, source)
- `tags` is an empty array or blank
- `status` is blank
- `source` is blank

### Frontmatter review (tidy / fix / full)

First run a lightweight detection pass for files with missing, malformed, empty, type-invalid, or role-incoherent frontmatter.

- If the detection pass finds **50 or fewer** files needing frontmatter handling, review and process only those files. Do not expand into a full-vault review and do not produce a full-vault ledger.
- If it finds **more than 50** files, trigger a full review of every file in scope. For each file, compare `tags`, `status`, and `source` with its document role, path, and project vocabulary.

Classify each reviewed file as:

- `pass` — metadata is complete and coherent with the document role
- `pass-project-schema` — metadata is coherent but uses a project-specific vocabulary
- `auto-fixable` — the correct value follows deterministically from the document role
- `requires-judgment` — authorship, provenance, or semantic intent cannot be inferred safely
- `exclude-candidate` — generated/config/backup material that may not be a vault note

Do not claim that all files were reviewed unless the `> 50` threshold triggered and every file in scope has one classification. In full-review mode, write a CSV ledger beside the Markdown report with one row per file: path, role, current values, classification, issues, review basis, and recommendation. In bounded mode (`<= 50`), list only the affected files in the Markdown report.

### Consistency check (tidy / fix / full)
- `status` value is not in the allowed set (published, draft, reference, outline, spec, log, archive)
- `source` value is not in the allowed set (self, claude-code, codex, agent, external) — only if the field exists
- Case-inconsistent synonymous tags in `tags` (e.g. `AI-alignment` vs `ai-alignment`)
- Underscore vs hyphen inconsistency in `tags` (e.g. `ai_alignment` vs `ai-alignment`)
- Obvious duplication between `topic` and `tags`

Treat the status and source sets above as the default vocabulary, not proof that every other non-empty value is malformed. A project-declared vocabulary takes precedence. A URL in `source` is valid external provenance but indicates a schema choice; report a possible `source: external` + `source_url` migration without rewriting it automatically.

### Redundancy check (full only)
- Files with more than 6 tags
- `created` field format is inconsistent (should be YYYY-MM or YYYY-MM-DD)

### Tag convergence analysis (tags / full)
Count tag usage across the entire vault and surface:
- Top 10 most-used tags (core tags)
- Semantically similar but differently named tags (candidate merge groups)
- Tags that appear only once (isolated tags — list each one)

## Output format

Only include sections for blocks that were run. Omit sections for blocks that were not run.

```
# Frontmatter health report

> Mode: [tidy / tags / fix / full]
> Check time: YYYY-MM-DD HH:MM
> Scan scope: [list of folders scanned]
> Files scanned: N

## Missing fields (N)          ← missing check only
...

## Consistency issues (N)      ← consistency check only
...

## Redundancy issues (N)       ← full only
...

## Tag overview                ← tags / full only
### Core tags (top 10)
...
### Merge candidates
...
### Isolated tags (appear once)
...

## Summary
- Blocks run: [list]
- Files needing attention: N
- Health: N% (files with no issues / total files)
```

If a block that was run has no issues, write "None" — do not skip it.

Write output in the language specified in `## Vault Structure` → `language`.

## Content health check (lint mode only)

Scan all content folders for content-level issues beyond frontmatter:

### Contradiction detection
Find pairs of notes that make conflicting claims about the same topic. For each:
- Note A: `[[filename]]` — claim
- Note B: `[[filename]]` — contradicting claim
- Severity: direct contradiction / tension / evolution (author changed mind over time)

### Stale claims
Notes where `status` is `published` or `reference` and the file has not been modified in 90+ days. For each:
- `[[filename]]` — last modified date — topic summary
- Question: is this still accurate?

### Orphan notes
Notes with zero incoming `[[wiki links]]` from other notes. Exclude wrap logs, inbox, and system folders. For each:
- `[[filename]]` — created date — topic
- Suggestion: connect to related note or archive

### Dead links
`[[wiki links]]` that point to non-existent files. For each:
- Source: `[[source-note]]` — the broken link text
- Suggestion: create the note, fix the link, or remove it

### Output (lint mode)

```
## Content health: lint

> Check time: YYYY-MM-DD HH:MM
> Files scanned: N

### Contradictions (N)
...

### Stale claims (N)
...

### Orphan notes (N)
...

### Dead links (N)
...
```

Lint mode is read-only — it reports issues but does not modify any files.

After the lint report, append a **Cross-reference suggestions** section. Only show a suggestion when that area has N > 0 issues. If all areas are 0, omit this section entirely.

```
## Cross-reference suggestions

### Dig deeper into contradictions
(Only if contradictions N > 0)
Run `/hirameki:lens <topic>` on the most-conflicted topic to examine the weaknesses in depth.
Most-conflicted topic found: {topic with the most contradictions}

### Surface vault patterns
(Only if isolated tags ≥ 5 or orphan notes ≥ 5)
Run `/hirameki:lens patterns` to see recurring themes and gaps across the full vault.

### Handle stale claims
(Only if stale claims N > 0)
For claims that are still valid: run `/hirameki:lens cards <note>` to promote to a stable concept card.
For claims that are outdated: update `status: archive` in frontmatter.
Stale files needing attention: N
```

Do not auto-execute any of these suggestions. Surface only — the user decides next steps.

## Fix logic (fix mode only)

Show the full list of all planned changes and wait for confirmation before executing.

Auto-fixable:
- Repair malformed frontmatter when the intended value is unambiguous
- Normalise tag casing (use whichever variant appears more often)
- Normalise underscore vs hyphen (use hyphen)
- Remove obvious duplication between `topic` and `tags` (keep the tags entry, remove topic)
- Add role-derived metadata only when the role makes the value deterministic (for example, wrap → `tags: [daily]`, `status: log`)

Requires per-item confirmation:
- Adding frontmatter when tags, status, or source cannot be derived safely
- Inferring `source` when original authorship or provenance is unknown
- Migrating custom status/source fields into a shared schema
- Deciding whether non-note artifacts should be excluded from the scan
- Merging semantically similar tags
- Trimming files with more than 6 tags
- Deleting isolated tags

After fixing, recalculate health score and output a diff summary.

## Write logic

Write the report to: `{research}/tidy/YYYY-MM-DD.md`
Create the folder if it does not exist.

If a report for today already exists, append:

```
---

## Follow-up update [HH:MM] [mode]

### Change summary
- [Which blocks were run, what was fixed, what remains]

### Health change
- Previous: N% → This run: N%
```

Rules:
- Use [[wiki link]] format for all file references
- Timestamps use local time in HH:MM format (24-hour)
- Show filename and full path, then wait for confirmation before writing
- Print the full path after writing
- Report at most 50 issues per run; if more exist, note the total and suggest processing in batches
