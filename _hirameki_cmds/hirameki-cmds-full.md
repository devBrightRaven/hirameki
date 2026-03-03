# Hirameki Commands — Full Specification

Complete prompt specifications for all Hirameki commands. This is a human-readable reference — the actual command prompts live in `commands/`.

---

## Shared: `__init`

All commands begin by reading from `~/.claude/CLAUDE.md` under `## Vault Structure`.

### Vault Detection

1. Check if current working directory contains `.obsidian/` — if yes, that's the vault
2. If not, read `~/.claude/CLAUDE.md` for a `## Vault` section with `path` setting
3. If neither found, ask the user for the vault path, confirm it contains `.obsidian/`, then save to `~/.claude/CLAUDE.md`

### Language Detection

Check `~/.claude/CLAUDE.md` for `language` under `## Vault Structure`. All output uses this language.

### Folder Detection

For each purpose, match the first existing folder from candidates:

| Purpose | Candidates |
|---------|------------|
| daily-notes | `Daily/`, `_daily/`, `daily/`, `Journal/`, `journal/` |
| inbox | `Inbox/`, `_inbox/`, `inbox/`, `_Capture/`, `Capture/` |
| analysis | `_hirameki_analysis/`, `_agent_analysis/`, `_claude_code_analysis/`, `Analysis/`, `_analysis/`, `analysis/` |
| logs | `_hirameki_logs/`, `_claude_code_feedback/`, `Logs/`, `_logs/`, `logs/` |
| templates | `Templates/`, `_templates/`, `templates/` |

If not found: ask the user, create the folder, print the full path, save to `~/.claude/CLAUDE.md` under `## Vault Structure`.

On subsequent runs, read cached config from `## Vault Structure` — skip detection.

### Content Folders

"Content folders" = all root-level vault folders EXCLUDING:
- Dot-prefixed folders (`.obsidian/`, `.claude/`, `.git/`, etc.)
- `_hirameki_cmds/`
- System folders listed in `## Vault Structure`

If no content folders exist, scan root-level `.md` files instead.

---

## Session Start

### `/hirameki:catchup [days]`

**Purpose:** Progress catchup.
**Input:** Optional number of days (default 1).
**Folders needed:** daily-notes, inbox.

Reads:
- Recent daily note(s) (default: yesterday, or N days if specified)
- All inbox files

Logic: Find the last Wrap block in each daily note. Extract "In Progress" and "Next Steps".

Output:

**Recent Progress** — Last Wrap's in-progress and next-steps. If no daily note or no Wrap block, note "No progress record found." Multi-day: list each day's last Wrap, reverse chronological.

**Inbox Pending** — Inbox files: filename, creation date, one-sentence summary. Limit 10. If empty: "Inbox clear."

**Suggested Focus** — 1-3 items worth pushing forward today. Each with reasoning (why today, not later). Max 3.

---

## Session End

### `/hirameki:wrap [description]`

**Purpose:** Progress snapshot written to daily note.
**Input:** Optional focus description.
**Folders needed:** daily-notes, templates.

Scans:
- Current session's file operations (created, modified, deleted)
- Today's daily note

Write target: `{daily-notes}/YYYY-MM-DD.md`
- If file doesn't exist and `templates/daily.md` exists: use template
- If file doesn't exist and no template: create with `# YYYY-MM-DD` header
- If file exists: append new Wrap block at end, separated by horizontal rule

Format per Wrap:

```
---

## Wrap [HH:MM]

### Completed
- [Specific items completed this period, one sentence each]

### In Progress
- [Started but unfinished items. If none, mark "None"]

### Next Steps
- [What to do next. If undecided, mark "TBD"]
```

Rules:
- Timestamps in local time HH:MM (24h)
- Never modify previous Wrap blocks, only append
- If input has a description, use it to organize the Wrap content
- Show preview + full path before writing, confirm before execution
- Print actual written path after execution

---

## Vault State Check

### `/hirameki:status [week|patterns]`

**Purpose:** Vault overview (three modes).
**Input:** None / `week` / `patterns`
**Folders needed:** daily-notes + all content folders (+ inbox for patterns mode).

#### No-argument mode — Immediate snapshot

Scans:
- All content folders (depth 2)
- daily-notes last 7 days

Output:

**Content Topics** — Each content folder and subfolders: name, note count, draft count, last modified date. Status: active (modified in 7 days) / dormant.

**Recent Activity** — Files modified in last 7 days, reverse chronological. Each: filename, parent folder, modified time, change type (new / modified / major rewrite). Limit 15.

**Vault Overview** — Total files, content folder count, active folders in last 7 days.

Empty sections show "None" instead of being omitted.

#### `status week` — Weekly gap analysis

Reads:
- All content folders' modification records (last 7 days)
- daily-notes from last 7 days

Output:

**This Week's Progress** — Each active content folder: name, what was pushed forward (based on file changes), next steps.

**Recent Activity** — Notes added or modified last week, which are near completion.

**Gap Analysis** — Compare daily note priorities vs actual file changes:
- Said important but didn't act (claimed priority, no corresponding file changes)
- Didn't mention but spent time on (file changes not referenced in daily notes)

If fewer than 3 daily notes, flag: "Insufficient records, gap analysis may be inaccurate."

#### `status patterns` — Undercurrents + clusters

Scans: all content folders, daily-notes (last 30 days), all inbox.

**Undercurrent Themes** — Recurring topics without a dedicated article. Criteria: appears in 3+ different files, no standalone article or draft. For each:
- Theme name
- Occurrence count and number of files (list up to 5 with [[wiki link]])
- Assessment: worth expanding? why?
Limit 10, sorted by frequency descending.

**Clusters** — Groups of 3+ notes on similar concepts without a shared parent category, written across different dates. For each:
- Suggested cluster name
- Notes involved ([[wiki link]], limit 5)
- Common theme (2-3 sentences)
- Maturity: high / medium / low
- Suggested direction: article / project / conceptual framework / keep accumulating
Limit 5, sorted by maturity descending.

---

## Deep Work on a Specific Idea

### `/hirameki:explore {input} [save]`

**Purpose:** Concept excavation — mode detected from input shape.
**Input:** Required. Shape determines mode. Append `save` to write to file.
**Folders needed:** analysis + all content folders.

#### Mode detection

| Input shape | Mode |
|-------------|------|
| Single concept or keyword | **Arc** |
| Two topics separated by `and` / `與` / `と` | **Bridge** |
| Ends with `?` or `？` | **Ghost** |
| Starts with `test:` | **Stress-test** |

#### Arc mode — Concept evolution tracking

Scans: Entire vault, prioritizing daily-notes and content folders.

Logic:
1. Check `{analysis}/arc/` for today's file matching the concept
2. Match found → append mode
3. Ambiguous match → list candidates, ask user
4. No match → create mode

**Create mode** — Write to `{analysis}/arc/YYYY-MM-DD-{concept}.md`:

```
# Concept Tracking: {concept}

> Analysis time: YYYY-MM-DD HH:MM

## First Appearance
Earliest file mentioning this concept, with context. Quote up to 3 sentences.

## Evolution Timeline
- YYYY-MM-DD | [[filename]] | One-sentence summary of usage/stance

## Current State
What topics this concept connects to, contradictory usage, any drafts developing it.

## Blind Spots
Aspects of this concept not yet explored in the vault.
```

**Append mode** — Add at end:

```
---

## Tracking Update [HH:MM]

### Evolution Timeline (New)
- [New mentions since last analysis]

### State Changes
- [What changed. If nothing, mark "No significant changes"]

### Blind Spots (Updated)
- [Re-evaluate unexplored aspects]
```

#### Bridge mode — Hidden connections

Scans: Entire vault.

Logic:
1. Check `{analysis}/bridge/` for today's file matching the topic pair (order-independent)
2. Match → append; no match → create

**Create mode** — Write to `{analysis}/bridge/YYYY-MM-DD-{topicA}-and-{topicB}.md`:

```
# Bridge Analysis: {topicA} and {topicB}

> Analysis time: YYYY-MM-DD HH:MM

## Direct Intersections
Files mentioning both topics. Each: [[filename]], how the two topics are connected in that file.
If none, mark "No direct intersections."

## Bridge Notes
Files mentioning only one topic but potentially forming a link. Explain why it could be a bridge.
Limit 5. Each with [[wiki link]].

## Potential Connection Hypotheses
1-3 hypotheses about deep connections. Each rated: strong / medium / weak, with evidence.
```

**Append mode:**

```
---

## Tracking Update [HH:MM]

### New Intersections
- [New intersections or bridge notes since last analysis]

### Hypothesis Validation
- [New supporting or contradicting evidence for previous hypotheses]
```

#### Ghost mode — Answer in your voice

Scans: All content folders, excluding `drafts/` and `thoughts/` subdirectories (finished articles only).

Input: Strip `save` from input if present, use remainder as the question.

Steps:
1. Analyze writing style: sentence patterns, word choices, argument structure, rhetorical habits
2. Extract existing stances and arguments related to the question
3. Compose an answer in that style and stance

Output:

**Answer** — In the user's voice. Length matching the user's typical article paragraph length.

**Sources** — Notes referenced: [[filename]], specific passage or stance cited. Limit 5.

**Confidence Markers** — Which parts have clear vault evidence vs which are style-extrapolated speculation.

Write to: `{analysis}/ghost/YYYY-MM-DD-{question-summary}.md`
Same day, same question: append with `## Follow-up Answer [HH:MM]` block.

#### Stress-test mode — Pressure-test arguments

Input: Strip `test:` prefix, use remainder as the topic. Strip `save` if present.

Scans: All vault files mentioning the topic.

Steps:
1. Collect all arguments and claims about the topic
2. Examine each claim's logic and evidence

Output:

**Claims List** — All major claims found. Each: one-sentence claim, source [[filename]].

**Weakness Analysis** — For each claim, check (list only applicable):
- Internal contradiction: different files say different things
- Unverified assumption: claim built on unproven premise
- Logic gap: missing intermediate steps
- Evidence gap: claim lacks supporting data or examples
Each weakness cites specific [[filename]] and passage.

**Overall Assessment** — Solidity rating: solid / mostly solid with gaps / needs major reinforcement. Top 1-3 weaknesses to address first.

Write to: `{analysis}/stress-test/YYYY-MM-DD-{topic-summary}.md`
Same day, same topic: append with `## Tracking Update [HH:MM]` block.

#### Common rules

- If >20 files found, list top 20 and note total count
- All file references use [[wiki link]] format
- Timestamps in local time HH:MM (24h)
- Print full analysis to terminal in all cases
- Write (when save is requested): show preview + full path before writing, confirm, print path after
- Create folder if it doesn't exist, print path

---

## Action Planning

### `/hirameki:harvest [save]`

**Purpose:** Harvest actionable ideas from existing content.
**Input:** Optional `save` to write to file.
**Folders needed:** analysis, daily-notes, inbox + all content folders.

Scans: all content folders, daily-notes (last 30 days), all inbox.

Output — seven categories, limit 5 each:

**Articles to Write** — Topics with enough material to develop into articles. Each: suggested title, source material ([[filename]] list), what's missing before writing.

**Tools or Projects to Build** — Tool needs, workflow pain points, or explicit product ideas. Each: description, source, estimated complexity (small / medium / large).

**Topics to Research** — External concepts, theories, or technologies mentioned but not explored. Each: topic, vault context, why it's worth researching.

**People or Communities to Contact** — People, organizations, or communities mentioned and relevant to current direction. Each: name, vault context, reason to reach out. If none, mark "None."

**Ideas for Different Media** — Content better suited to a different format (video, visual, talk, newsletter, podcast). Each: idea summary, suggested medium, why that format fits better than text.

**Value Not Transacted** — Expertise or capabilities not yet converted to revenue. Each: skill or knowledge description, possible monetization form (course, consulting, product, licensing), vault evidence. If none, mark "None."

**Ideas Ready to Graduate** — Half-formed ideas with enough density to become standalone notes. Each: source location ([[filename]] + paragraph description), core claim (one sentence), suggested destination content folder, related existing notes.

Criteria for graduation: has a clear core claim (not just a question), relates to at least one existing vault topic, has sufficient content density (more than one sentence).

### Graduate phase (always two-phase, regardless of `save`)

After listing graduate candidates, pause and wait for user to select which ideas to execute.

For each confirmed idea:
1. Show full file path, wait for confirmation
2. Create new markdown file in the chosen content folder:
   - Title
   - Core claim
   - Origin context (which daily note or inbox item)
   - Related vault notes ([[wiki link]])
   - Directions to expand
3. Print actual created path after execution

### Write logic (when `save` is in input — covers main harvest summary only, not graduate)

1. Check `{analysis}/harvest/` for today's file
2. Exists → append with `## Tracking Update [HH:MM]` block
3. Doesn't exist → create `{analysis}/harvest/YYYY-MM-DD.md`

File structure:

```
# Idea Harvest

> Analysis time: YYYY-MM-DD HH:MM
> Scan scope: [list scanned directories]

## Articles to Write
[list]

## Tools or Projects to Build
[list]

## Topics to Research
[list]

## People or Communities to Contact
[list]

## Ideas for Different Media
[list]

## Value Not Transacted
[list]

## Ideas Ready to Graduate
[list]
```

---

## Maintenance

### `/hirameki:tidy [fix]`

**Purpose:** Frontmatter properties audit and cleanup.
**Input:** Optional — `fix` to auto-correct after confirmation.
**Folders needed:** All content folders + inbox + daily-notes.

Scans:
- All content folders (recursive)
- inbox — all files
- daily-notes — last 30 days

**Checks performed:**

1. **Missing fields** — files without frontmatter, missing `tags` or `status`
2. **Consistency** — invalid `status`/`source` values (source allows: self, claude-code, agent, external), tag casing mismatches, underscore vs hyphen inconsistency
3. **Redundancy** — tags used only once (possible typos), files with 6+ tags, `topic` duplicating a tag
4. **Tag convergence** — frequency stats, merge candidates for semantically similar tags, top 10 core tags, orphan tags

**Output:** Report with health score (clean files / total files).

```
# Frontmatter Audit Report

> Checked: YYYY-MM-DD HH:MM
> Scope: [directories scanned]
> Files scanned: N

## Missing Fields (N)
- [[file]] — missing frontmatter / missing tags / missing status

## Consistency Issues (N)
- [[file]] — status "xxx" not in allowed values
- Tag casing mismatch: `AI-alignment` (3) vs `ai-alignment` (5) → suggest `ai-alignment`

## Redundancy Issues (N)
- [[file]] — 8 tags, suggest trimming
- Tag `xxx` used only once, in [[file]]

## Tag Overview
### Core Tags (top 10)
| Tag | Count |

### Merge Candidates
- `ai_alignment` → `ai-alignment` (N files to update)

### Orphan Tags (used once)
| Tag | Found in |

## Summary
- Needs fix: N files
- Suggest trimming: N tags
- Health: N%
```

**Fix mode** (when input includes `fix`):

Auto-fixable (after showing full change list and confirmation):
- Add missing frontmatter skeleton (empty tags + `status: draft`)
- Normalize tag casing (majority wins)
- Normalize underscores to hyphens in tags
- Remove `topic` when it duplicates a tag

Requires per-item confirmation:
- Merge semantically similar tags
- Trim files with 6+ tags
- Delete orphan tags

After fixing, recalculate health score and output diff summary.

**Write behavior:** Always writes report to `{analysis}/tidy/YYYY-MM-DD.md`. Same day appends update with change summary and health score delta.

Max 50 issues reported per run.

---

## Work Reasoning Log

### `/hirameki:journal {description}`

**Purpose:** Work log and thinking article.
**Input:** Required — topic description.
**Folders needed:** logs + all content folders (for related note search).

Scans:
- Current session's operations
- Vault notes related to the topic
- Today's existing journal files in logs

Logic:
1. Scan `{logs}/` for `YYYY-MM-DD-*.md` files (today's date)
2. Compare filenames and titles against input topic keywords
3. Clear match → append mode
4. Ambiguous match → list candidates, ask user
5. No match → create mode

**Create mode** — Write to `{logs}/YYYY-MM-DD-{topic-summary}.md`:

```
# {topic}

> Created: YYYY-MM-DD HH:MM

## Background
Why this happened. If vault has prior notes, cite with [[wiki link]].

## What Was Done
Concrete operations and decisions, with causal narrative.

## Why This Approach
Key decision rationale. Trade-offs: what was chosen, what was dropped.

## Inspiration Links
Connections to other ideas, cross-topic links. [[wiki link]] to related notes. If none, mark "None."

## Possible Improvements
Unexplored directions, alternatives, potential risks. If none, mark "None."

## Unfinished and Follow-up
Items to follow up on. If all done, mark "No pending items."
```

**Append mode** — Add at end:

```
---

## Appended Record [HH:MM]

### What Was Done
[New operations and decisions]

### Why This Approach
[New decision rationale]

### Inspiration Links
[New connections. If none, mark "None"]

### Possible Improvements
[New directions. If none, mark "None"]
```

Also check "Unfinished and Follow-up" section — if items are now done, mark with completion timestamp.

---

## Write Behavior Overview

| Command | Writes to | Trigger | Same-day repeat |
|---------|-----------|---------|-----------------|
| `/hirameki:wrap` | daily-notes | Always | Appends new Wrap block |
| `/hirameki:journal` | logs | Always | Same topic appends, different topic creates new |
| `/hirameki:explore` | analysis/arc, bridge, ghost, stress-test | With `save` | Same concept/question appends |
| `/hirameki:harvest` | analysis/harvest | With `save` | Appends update |
| `/hirameki:harvest` (graduate) | content folder | After confirm | New file each time |
| `/hirameki:tidy` | analysis/tidy | Always | Appends update |

## Common Rules

- All timestamps use local time HH:MM (24-hour format)
- All file references use [[wiki link]] format
- All write commands show a preview and full path before writing, then confirm before execution
- All write commands print the actual written path after execution
- Output language is read from `~/.claude/CLAUDE.md` under `## Vault Structure`
