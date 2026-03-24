---
description: Frontmatter health check and cleanup
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

## Modes

Select which checks to run based on $ARGUMENTS:

| Call | Runs |
|------|------|
| `tidy` (no argument) | Missing field check + Consistency check |
| `tidy tags` | Tag convergence analysis only |
| `tidy fix` | Missing + Consistency + Auto-fix |
| `tidy full` | All blocks |

Only run the blocks for the selected mode — omit all others from the report.

## Scan scope

- All content folders (recursive)
- All files in the inbox folder
- Last 30 days in the daily folder

## Check blocks

### Missing field check (tidy / fix / full)
- Files with no frontmatter
- Files with frontmatter but missing required fields (required: tags, status)
- `tags` is an empty array or blank
- `status` is blank

### Consistency check (tidy / fix / full)
- `status` value is not in the allowed set (published, draft, reference, outline, spec, log, archive)
- `source` value is not in the allowed set (self, claude-code, agent, external) — only if the field exists
- Case-inconsistent synonymous tags in `tags` (e.g. `AI-alignment` vs `ai-alignment`)
- Underscore vs hyphen inconsistency in `tags` (e.g. `ai_alignment` vs `ai-alignment`)
- Obvious duplication between `topic` and `tags`

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

## Fix logic (fix mode only)

Show the full list of all planned changes and wait for confirmation before executing.

Auto-fixable:
- Add missing frontmatter skeleton (empty tags array and status: draft)
- Normalise tag casing (use whichever variant appears more often)
- Normalise underscore vs hyphen (use hyphen)
- Remove obvious duplication between `topic` and `tags` (keep the tags entry, remove topic)

Requires per-item confirmation:
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
