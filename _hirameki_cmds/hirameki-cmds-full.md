# Hirameki Commands — Full Specification

Complete prompt specs for all Hirameki commands. This is a human-readable reference — the actual command prompts live in `commands/`.

---

## Shared: `__init`

Every command reads `vault:` from `~/.claude/vault-local.md` for the vault root, then the `## Vault Structure` section from `<vault>/AGENTS.md` for folder paths (fallback: `~/.claude/vault-local.md`, then `~/.claude/CLAUDE.md`).

### Vault detection

1. Current working directory contains `.obsidian/` → use as vault
2. Read `path` from `## Vault` section in `~/.claude/CLAUDE.md`
3. Read from Obsidian's `obsidian.json` (OS-specific location); filter out built-in sandbox paths; prompt if multiple vaults found
4. If none found → ask user, verify path contains `.obsidian/`, write to `~/.claude/CLAUDE.md`

### Language detection

Read `language` from `## Vault Structure` in `vault-local.md`. All output uses this language.

### Folder detection

Each purpose matches the first existing candidate folder:

| Purpose | Candidates |
|---------|-----------|
| daily | `_yorozuya/daily/`, `Daily/`, `_daily/`, `daily/`, `Journal/`, `journal/` |
| inbox | `Inbox/`, `_inbox/`, `inbox/`, `_Capture/`, `Capture/` |
| research | `_yorozuya/research/`, `_hirameki_analysis/`, `_agent_analysis/`, `Analysis/`, `_analysis/`, `analysis/` |
| journal | `_yorozuya/journal/`, `_hirameki_logs/`, `_agent_logs/`, `Logs/`, `_logs/`, `logs/` |
| handoff | `_yorozuya/handoff/`, `Handoff/`, `_handoff/`, `handoff/` |
| templates | `Templates/`, `_templates/`, `templates/` |

If no match: ask user, create folder, print path, write to `<vault>/AGENTS.md`.

### Content folders

"Content folders" = all top-level vault folders, excluding:
- Hidden folders starting with `.` (`.obsidian/`, `.git/`, etc.)
- `_hirameki_cmds/`
- System-folder subtrees listed in `## Vault Structure` (keep unrelated siblings under the same top-level folder)

Inside content folders, skip hidden directories, dependency/build directories such as `node_modules`, and files ignored by Git when the vault is a Git repository.

If no content folders: scan all `.md` files at vault root directly.

---

## Orchestrators

### `/hirameki:triage`

**Purpose:** End-of-session bundle — wrap, journal, and handoff in one guided flow.
**Input:** None. Run when wrapping up a session.

#### Shared state collection (runs once)

Before the first sub-flow, collect session context from:
- Files created or modified this session (Edit/Write history)
- Tasks completed and still open (TaskList)
- Key decisions made this session

All three sub-flows draw from this shared state.

#### [1/3] Wrap

Runs wrap logic (see `/hirameki:wrap` spec). Shows full draft and write target. Then:

```
[1/3] Wrap — Action? (save this / save all / skip / edit)
```

- `save this` → write only this draft to `{daily}/YYYY-MM-DD.md`, proceed to [2/3]
- `save all` → write this draft and batch-approve the remaining drafts; still show each full draft and path before writing, but do not pause again
- `skip` → skip write, proceed to [2/3]
- `edit` → ask "Edit which part?" → adjust draft → show updated draft → ask the same action menu
- Legacy `save` is an alias for `save this`

#### [2/3] Journal

Runs journal logic (see `/hirameki:journal` spec), inferring topic from session activity. Shows full draft and write target. Then:

```
[2/3] Journal — Action? (save this / save all / skip / edit)
```

Same action model. Proceeds to [3/3] regardless of choice.

#### [3/3] Handoff

Runs handoff logic (see `/hirameki:handoff` spec). Shows full draft and write target. Then:

```
[3/3] Handoff — Action? (save this / save all / skip / edit)
```

After this step, show completion summary:

```
Triage done: wrap ✓ / journal – / handoff ✓
```

**Rules:**
- Always show full draft for each step — never auto-skip based on content length
- An active `save all` is approval for every remaining triage draft; show each draft and path, then write without another prompt
- Skip does not interrupt the flow; always proceed to the next sub-flow
- Each sub-flow's write logic (same-day append vs. create) follows its primitive's rules

---

### `/hirameki:lens <concept>`

**Purpose:** Topic understanding — arc, positions, bridge, and challenge as a single flow.
**Input:** Single topic or concept (required). If empty, ask.

Print before starting:
```
Lens on: {concept}
```

#### Step 0 — Shared context (runs once)

Scan vault for the topic. Collect:
- All files mentioning the topic
- Earliest and most recent file dates (for arc timeline)
- Related topics that co-appear with this one (for bridge partner suggestion)

#### [1/4] Arc

Runs arc logic (see `/hirameki:arc` spec) using shared context. Then:

```
[1/4] Arc — Action? (save / skip / next)
```

- `save` → write to `{research}/lens/YYYY-MM-DD-{concept}-arc.md`
- `skip` or `next` → proceed to [2/4]

#### [2/4] Positions

Extract all explicit positions and claims about the topic from the vault.

Rules:
- Only claims directly about this topic — no tangential mentions
- One claim per source — the most specific or clearly-stated one
- Limit: 10 most relevant sources
- Pure extraction only — do NOT compose a voice answer

Output:

```
## Positions on: {concept}

> Analysis time: YYYY-MM-DD HH:MM

| Source | Claim |
|--------|-------|
| [[filename]] | The specific position or claim (one sentence) |

### Tensions
(If two or more claims contradict each other, name the tension.
If all claims align: "No significant tension found.")

### Gaps
(Angles on this topic not addressed anywhere in the vault.)
```

Then:

```
[2/4] Positions — Action? (save / skip / next)
```

- `save` → write to `{research}/lens/YYYY-MM-DD-{concept}-positions.md`

#### [3/4] Bridge

Auto-suggest the most likely partner topic (the one that co-appears most frequently from Step 0, or the most prominent gap from arc). Print suggestion before running:

```
[3/4] Bridge — Partner topic suggested: {suggested}
  Action? (save / skip / change-partner)
```

- `save` or enter → accept, run bridge logic, show output, prompt final save
- `skip` → proceed to [4/4]
- `change-partner` → ask "Bridge {concept} with which topic?" → run bridge

Bridge logic same as `/hirameki:bridge` spec. Save target: `{research}/lens/YYYY-MM-DD-{concept}-bridge.md`

#### [4/4] Challenge

Runs challenge logic (see `/hirameki:challenge` spec) using positions from [2/4]. Then:

```
[4/4] Challenge — Action? (save / skip / next)
```

- `save` → write to `{research}/lens/YYYY-MM-DD-{concept}-challenge.md`

After all four steps, show:

```
Lens done: arc {✓ saved | – skipped} / positions {✓ saved | – skipped} / bridge {✓ saved | – skipped} / challenge {✓ saved | – skipped}
```

---

### `/hirameki:compose <topic>`

**Purpose:** Topic creation — voice composition and frame test as a single flow.
**Input:** Topic or question (required). If empty, ask.
**Standalone:** Does not require `/hirameki:lens` to have run first.

Print before starting:
```
Compose on: {topic}
```

#### [1/2] Voice

Run full reflect logic (see `/hirameki:reflect` spec):
1. Analyse writing style from completed articles in content folders
2. Extract vault positions on the topic (limit: 5 sources)
3. Write an answer in the author's voice using identified style + positions

Output same as `/hirameki:reflect` spec (Answer / Sources / Confidence). Then:

```
[1/2] Voice — Action? (save / skip / edit-question)
```

- `save` → write to `{research}/compose/YYYY-MM-DD-{topic}-voice.md`
- `skip` → proceed to [2/2]
- `edit-question` → ask "Revised topic or question?" → rerun voice step

#### [2/2] Frame

Run frame logic (see `/hirameki:frame` spec) treating the voice output as the idea to evaluate. If [1/2] was skipped, ask "Frame which idea?" and wait for input.

Full five-question test + verdict output. Then:

```
[2/2] Frame — Action? (save / skip / next)
```

- `save` → write to `{research}/compose/YYYY-MM-DD-{topic}-frame.md`

After both steps:

```
Compose done: voice {✓ saved | – skipped} / frame {✓ saved | – skipped}
```

---

### `/hirameki:mekiki <input>`

**Purpose:** External resource capture — auto-detects repo vs. article.
**Input:** Required — GitHub URL, article URL, pasted text, or local file path.

#### Input routing

| Input shape | Branch |
|-------------|--------|
| Matches `github.com/[^/]+/[^/]+` or `^[^/]+/[^/]+$` | Repo branch |
| Other URL (`http(s)://`) | Article branch (URL) |
| Local file path (starts with `/`, drive letter, `./`, and exists on filesystem) | Article branch (file) |
| Otherwise | Article branch (paste) |

Detection order: repo pattern → URL → file path → paste.

#### Repo branch

**Phase 1 — Fetch (parallel):**
```bash
gh repo view owner/repo --json description,url,stargazerCount,primaryLanguage,updatedAt
gh api repos/owner/repo/readme -q .content | base64 -d
gh api repos/owner/repo/git/trees/HEAD?recursive=1 -q '.tree[].path' | head -150
```
Identify 3–5 key source files and fetch content.

**Phase 2 — Analysis:**

Track A — Technique extraction (always runs): For each interesting pattern: name, what it is (1–2 sentences), why interesting, where it is transferable (user's actual projects), concrete next step.

Track B — Adoption evaluation (skips pure demo/pattern repos): Read user's CLAUDE.md and project memory. Classify repo as tool/framework/library/pattern. Build comparison table (feature / repo provides / we currently use / gap). Verdict: **adopt** (with next step + timeline) / **defer** (with trigger condition) / **reject** (with alternative).

**Phase 3 — Validation (Sonnet subagent):** Check completeness, credibility, actionability. Skip for repos with fewer than 10 files.

**Write:** `{research}/mekiki-{repo-name}.md` — frontmatter: `tags: [mekiki, {verdict}]`, `status: reference`, `source: claude-code`.

#### Article branch

**Phase 1 — Capture source:**
- URL → WebFetch
- File → Read
- Paste → use directly

Extract: title, author, date, core argument (1–3 sentences), key claims (bullet list), vocabulary/concepts new to vault.

Write source note to `{inbox}/YYYY-MM-DD-{slug}.md`:
```yaml
---
tags:
  - inbox
  - mekiki
status: draft
source: external
created: YYYY-MM-DD
url: {source url if applicable}
---
```

**Phase 2 — Cross-reference:** Scan content folders and recent wrap logs for vault notes touching the same claims or concepts. For each match: `[[filename]]` + how the vault note relates to this article (supports / contradicts / extends / is extended by).

**Phase 3 — Verdict:**

```
## Worth integrating?

**Verdict:** integrate / revisit-later / skip
**Reason:** one sentence
**Next step:** one concrete action (e.g., create a concept card, add to writing outline, no further action)
```

Print the inbox file path after writing.

---

## Session

### `/hirameki:next`

**Purpose:** Orient after resuming a session.
**Input:** None.
**Does not write to file.**

Scan this session's task list, file activity (created or modified files), decisions made, and commits pushed. Output a concise orientation summary: what was completed, what is open, what to do next.

---

### `/hirameki:wrap [description]`

**Purpose:** Progress snapshot, appended to wrap log.
**Input:** Optional focus description.
**Requires:** wrap folder, templates folder.

Scan session file operations (created, modified, deleted) and today's wrap log.

Write target: `{daily}/YYYY-MM-DD.md`
- File does not exist + `templates/daily.md` exists → use template
- File does not exist, no template → create `# YYYY-MM-DD` heading
- File exists → append new Wrap block with horizontal rule

Wrap format:

```
---

## Wrap [HH:MM]

### Done
- [Specific items completed this session, one sentence each]

### In Progress
- [Items started but not finished. If none: "None"]

### Next
- [What to do next. If undecided: "TBD"]
```

Rules:
- Timestamps use local time HH:MM (24-hour)
- Append only — never modify previous Wrap blocks
- Optional description input organises the Wrap content
- Show draft and full path before writing; print actual path after writing

---

### `/hirameki:journal <description>`

**Purpose:** Work log with reasoning.
**Input:** Topic description (required).
**Requires:** journal folder, content folders (for related note search).

Scan: this session's operations, vault notes related to the topic, today's existing journal files.

Logic:
1. Scan `{journal}/` for today's `YYYY-MM-DD-*.md` files
2. Match filenames and titles against input topic keywords
3. Clear match → append mode
4. Fuzzy match → list candidates, ask user
5. No match → create mode

**Create mode** — Write to `{journal}/YYYY-MM-DD-HHMM-{topic-slug}.md`:

```
# {topic}

> Created: YYYY-MM-DD HH:MM

## Background
Why this happened. Link to existing vault notes with [[wiki links]].

## What was done
Specific actions and decisions with causal narrative.

## Why this approach
Reasoning behind key decisions. Trade-offs: what was chosen and what was left out.

## Judgment and decision process
Record the question, earlier judgment, observations, inferences, unverified assumptions, new evidence, how the judgment changed, current action, unknowns, and revisit trigger. If there was no substantive update, say so; do not invent a trajectory.

## Inspiration links
Connections to other ideas. [[wiki link]] related notes. If none: "None".

## Possible improvements
Unexplored directions, alternatives, risks. If none: "None".

## Open items
Follow-ups needed. If all complete: "No open items".
```

**Append mode** — Add at end:

```
---

## Follow-up [HH:MM]

### What was done
[New actions and decisions]

### Why this approach
[New reasoning]

### Judgment and decision process
[Only new or changed judgment; keep observation, inference, and assumption distinct.]

### Inspiration links
[New connections. If none: "None"]

### Possible improvements
[New directions. If none: "None"]
```

Also check "Open items" — mark completed items with a timestamp.

---

### `/hirameki:decision-trace <decision question or context>`

**Purpose:** Form a decision without choosing for the user, then optionally preserve an explicit choice as a lifecycle-managed node.

**Read-only formation:** Identify `unresolved`, `forming`, `decided`, or `reviewing`. For unresolved or forming decisions, present the decision question, viable options, evidence and its source, assumptions and unknowns, constraints and non-negotiables, consequences, reversal cost, and one key unresolved question. Do not write or choose for the user.

An unresolved or forming trace may persist across sessions after `save this`; store it as a journal note in `{journal}` or as a handoff, never in `{journal}/decisions/`. Only explicitly decided choices become decision nodes.

**Conditional write:** After the user explicitly states or confirms a choice, apply the promotion gate. Show the evidence, affected paths, complete draft, and exact status changes; write only after `save this`. Preserve `active`, `superseded`, and `closed` lifecycle behavior.

**Writes to:** unresolved/forming traces → `{journal}` or `{handoff}` after `save this`; explicitly decided nodes → `{journal}/decisions/YYYY-MM-DD-{slug}.md` after `save this`.

---

### `/hirameki:handoff`

**Purpose:** End-of-session handoff document for the next session.
**Input:** None. Topic and slug inferred from session activity.
**Requires:** handoff folder.

Collect: files created or modified this session, tasks completed/open, key decisions, blockers encountered.

Infer topic from the dominant theme of session activity. If ambiguous, ask.

Write target: `{handoff}/YYYY-MM-DD-{slug}.md`

```yaml
---
tags:
  - handoff
status: log
source: claude-code
created: YYYY-MM-DD
---
```

```
# Handoff: {topic} — {YYYY-MM-DD}

> Session end: YYYY-MM-DD HH:MM

## What was accomplished
- [Completed items]

## Current state
[Where things stand right now — what is half-done, what is waiting]

## Open threads
- [Unfinished item] — [what remains]

## Key decisions made
- [Decision] — [rationale]

## Judgment updates
| Question | Earlier judgment | Change evidence | Current judgment | Unknowns | Revisit trigger |
|----------|------------------|-----------------|------------------|----------|-----------------|
Only changes that affect pickup. If none, state that there is no judgment update to hand off.

## Next session: start here
1. [First thing to pick up]
2. [Second thing, if relevant]

## Notes and warnings
[Anything the next session needs to know to avoid mistakes or re-work. If none: omit.]
```

Show full draft and write target before writing. Print path after writing.

---

## Understanding (standalone)

### `/hirameki:arc <concept>`

**Purpose:** Track how a concept has evolved across the vault.
**Input:** Concept or topic (required).
**Requires:** research folder, all content folders.

Logic:
1. Check `{research}/arc/` for an existing arc file for this concept today
2. Match found → append mode; no match → create mode

**Create mode output** — Write to `{research}/arc/YYYY-MM-DD-{concept}.md`:

```
# Concept tracking: {concept}

> Analysis time: YYYY-MM-DD HH:MM

## First appearance
Earliest file where this concept appeared. Quote up to 3 sentences.
Date: YYYY-MM-DD

## Evolution timeline
- YYYY-MM-DD | [[filename]] | How this concept was used or positioned (one line)

## Current state
Topics this concept connects to now, contradictory uses, drafts developing it.

## Unexplored angles
Aspects of this concept not addressed anywhere in the vault.
```

**Append mode** — Add at end:

```
---

## Tracking update [HH:MM]

### Timeline (new)
- [New mentions since last analysis]

### State change
- [What changed compared to last analysis. If unchanged: "No significant change"]

### Unexplored angles (updated)
- [Re-evaluated aspects not yet addressed]
```

Show draft and path before writing. Print path after writing.

---

### `/hirameki:bridge <A> and <B>`

**Purpose:** Find hidden connections between two topics.
**Input:** Two topics separated by "and", "與", or "と" (required).
**Requires:** all content folders.

Logic:
1. Check `{research}/bridge/` for an existing bridge file for this pair today (order-independent)
2. Found → append mode; not found → create mode

**Create mode** — Write to `{research}/bridge/YYYY-MM-DD-{A}-{B}.md`:

```
# Bridge: {A} × {B}

> Analysis time: YYYY-MM-DD HH:MM

## Direct intersections
Files mentioning both topics. Each: [[filename]] — how the two topics relate here.
If none: "No direct intersections."

## Bridge notes
Files mentioning one topic that could connect to the other. Why this file could link them.
Limit: 5, each with [[wiki link]].

## Hypotheses
1–3 hypotheses about deeper connections. Each: confidence level (strong/medium/weak) + evidence source.
```

**Append mode:**

```
---

## Tracking update [HH:MM]

### New intersections
- [New intersections or bridge notes since last analysis]

### Hypothesis check
- [New evidence supporting or contradicting previous hypotheses]
```

Show draft and path before writing. Print path after writing.

---

### `/hirameki:challenge <topic>`

**Purpose:** Analyse weaknesses in vault claims about a topic.
**Input:** Topic or argument (required). No prefix needed.
**Requires:** all content folders.

For each vault claim about the topic, check the following weakness types (only list those that apply):
- **Internal contradiction**: conflicting statements across vault files
- **Unverified assumption**: claim rests on an unproven premise
- **Logic gap**: missing steps in the argument
- **Evidence gap**: claim lacks supporting data or examples

Write to `{research}/challenge/YYYY-MM-DD-{topic-slug}.md`:

```
## Challenge: {topic}

> Analysis time: YYYY-MM-DD HH:MM

## Claims assessed
| Claim | Source |
|-------|--------|
| [claim text] | [[filename]] |

## Weaknesses

### Claim: {claim} — [[source]]
- Internal contradiction: [details] — see [[filename]]
- Logic gap: [details]
(Only list weakness types that apply. Omit claims with no weaknesses.)

## Assessment
Overall: solid / mostly solid with gaps / needs major work
Top 1–3 weaknesses worth addressing first.
```

Show draft and path before writing. Print path after writing.

---

### `/hirameki:reflect <question>`

**Purpose:** Answer a question in your own voice, drawing from vault positions.
**Input:** Question or topic (required). Add `save` to write result.
**Requires:** all content folders (style analysis + position extraction).

#### Step 1 — Analyse writing style

Scan completed articles in content folders (exclude `drafts/` and `thoughts/` subdirectories).

Extract: sentence patterns and typical length, vocabulary level and recurring phrasing, argument structure (how claims are introduced, supported, qualified), rhetorical moves that appear repeatedly.

#### Step 2 — Extract positions

Search the full vault for notes relevant to the question. Prioritise: notes directly addressing the topic, permanent concept cards, journal entries with a clear position, wrap logs with relevant observations. Limit: 5 most relevant sources.

#### Step 3 — Compose answer

Write an answer using the identified style and extracted positions:
- Match the length of a typical paragraph from their writing
- Use the author's own arguments, not general knowledge
- Do not introduce positions the vault does not support
- If the vault has contradictory positions, surface the tension rather than resolving it

Output:

```
[Answer]
The answer in the author's voice. One to three paragraphs.

[Sources]
- [[note-title]] — the specific position or passage drawn from
(Limit: 5 sources)

[Confidence]
- Vault-supported: which parts have direct evidence
- Style-inferred: which parts extend the style without direct backing
- Tensions: any contradictions found across vault notes
```

With `save`: write to `{research}/reflect/YYYY-MM-DD-{question-slug}.md`. Same question same day appends.

---

## Creation (standalone)

### `/hirameki:frame <idea>`

**Purpose:** Pre-creation checkpoint — evaluate whether an idea is worth pursuing.
**Input:** Required — article idea, product concept, design direction, or path to existing draft.
**Requires:** all content folders, wrap logs, journal folder.

#### Phase 1: Understand the idea

Determine type (Article / Product / Design). If input is a file path, read the file and extract the thesis. Print thesis and type, then proceed.

#### Phase 2: Five-question frame test

**Q1 — Only-I test:** What is this saying that only I can say?
Scan vault for personal experiences, unique perspectives, proprietary knowledge. Evaluate: Strong / Weak / None.

**Q2 — Collision scan:** Does something I have already made cover this?
- Tier 1 — Published work: absorbed / adjacent / superseded
- Tier 2 — Unpublished drafts: competing / adjacent / feeds

**Q3 — Stakes:** After encountering this, what changes for the reader?
Reframes / Equips / Provokes / None of the above.

**Q4 — Tension:** What is the surprising or counterintuitive part?
Contradiction the author is willing to sit with / Reversal / Confession.

**Q5 — Evidence:** What lived experience or data makes this credible?
Embodied / Researched / Speculative.

#### Phase 3: Verdict

| Verdict | Condition |
|---------|-----------|
| **PROCEED** | Q1 Strong + at least one of Q3/Q4 strong + no Tier 1 absorbed collision |
| **RETHINK** | Q1 Weak or adjacent collision or Q3 "informs only" |
| **KILL** | Q1 None or Tier 1 absorbed or both Q3 and Q4 empty |
| **CONSOLIDATE** | Q2 has multiple Tier 2 competing drafts |

```
## Frame: PROCEED
**Thesis**: [one sentence]
**Unique angle**: [from Q1]
**Core tension**: [from Q4]
**Key evidence**: [from Q5]
### Before starting
- [1–2 specific things to nail down]

## Frame: RETHINK
**Thesis**: [one sentence]
**Problem**: [which questions failed and why]
### What would make this worth doing
- [1–3 specific directions]
### Existing work to build on
- [[filename]] — [how it relates]

## Frame: KILL
**Thesis**: [one sentence]
**Reason**: [one sentence]
**Salvageable parts**: [fragments worth keeping, or "none"]

## Frame: CONSOLIDATE
**Thesis**: [one sentence]
**Competing drafts**:
- [[draft 1]] — strength: X, weakness: Y
**Recommended vessel**: [[strongest draft]] — because [reason]
**Parts to absorb from other drafts**: [specific content]
**Drafts to retire after consolidation**: [list]
```

Rules: Do not soften the verdict. KILL means stop. Add `save` to write to `{research}/frame/YYYY-MM-DD-{idea-slug}.md`. Frame does not generate content.

---

### `/hirameki:critique <file>`

**Purpose:** Multi-model writing review.
**Input:** Required — file path (relative paths resolved from vault root). If empty, check most recently modified draft and ask for confirmation.
**Requires:** vault root (resolve path), `_writing_lab/benchmark/` (output).

#### Phase 1: Three reviewers in parallel

Three dimensions, scored 1–10:
1. **Sensory density** (感官密度): How vivid and specific are physical details?
2. **Structural tension** (結構張力): Does tension build and release? Does the ending land?
3. **Emotional resonance** (觸動力): Does the reader feel something real?

Each reviewer also identifies: top 3 strongest sentences (with reason), top 3 weakest sentences (with reason), one structural suggestion.

**Reviewer 1 — Claude Opus (Agent, model: opus)**
Read file and evaluate. Score all three dimensions. Be brutally honest. Write in the vault language.

**Reviewer 2 — Codex GPT (Bash, codex CLI)**
```bash
codex exec "Read the essay below and evaluate it as a writing critic.
Score on three dimensions (1-10 each): sensory density, structural tension, emotional resonance.
Identify: Top 3 strongest sentences, Top 3 weakest sentences (and why), One structural suggestion.
Write in {vault language}. Be honest and critical.

$(cat '{file_path}')"
```

**Reviewer 3 — Gemini Pro (Bash, gemini CLI)**
```bash
gemini -p "$(cat <<'PROMPT'
Read the essay below and evaluate as a writing critic.
Score three dimensions (1-10): sensory density, structural tension, emotional resonance.
Identify: strongest sentences, weakest sentences, one structural suggestion.
Write in {vault language}.
$(cat '{file_path}')
PROMPT
)" --allowed-mcp-server-names none
```

If codex or gemini CLI is not available, skip that reviewer and note it in output.

#### Phase 2: Compile results

Comparison table (Opus / Codex GPT / Gemini Pro). Consensus (2/3+ agreement). Strongest sentences selected by 2+ reviewers. Weakest sentences flagged by 2+ reviewers. Unique perspectives per reviewer.

#### Phase 2.5: Write review file

Consensus score for each dimension = average of all three, rounded to one decimal.

Write to `{vault}/_writing_lab/benchmark/YYYY-MM-DD-{article-slug}-review.md`:

```yaml
---
tags:
  - writing-lab
  - review
status: reference
source: claude-code
created: YYYY-MM-DD
article: "{article filename}"
scores:
  sensory: {average}
  structure: {average}
  resonance: {average}
  overall: {average of three}
models:
  - opus
  - codex
  - gemini
phase: initial
---
```

Print file path. Ask: "Want to revise based on these notes? Or run the final review first?"

#### Phase 3: Final review (optional, on user request)

After edits are made, run final review with Opus + Codex GPT in parallel.

Both reviewers check: which initial issues are Fixed / Partially fixed / Not fixed / New issue introduced. Then fresh read: overall impression, all three dimension scores, any new weaknesses, top 3 strongest moments, one remaining fix.

Append final review results to the same benchmark file. Update frontmatter `phase` to `final` and update scores.

---

## Vault

### `/hirameki:pulse [week|patterns]`

**Purpose:** Vault state overview (three modes).
**Input:** None / `week` / `patterns`
**Does not write to file.**

#### Default mode — Instant overview

Scan: all content folders (depth 2), wrap logs (last 7 days).

**Content topics** — Each content folder and subdirectory: name, total notes, draft count, last modified date. Status: active (modified in last 7 days) / dormant.

**Recent activity** — Files modified in last 7 days, reverse chronological. Each: filename, folder, modification time, change type (new / modified / major rewrite). Limit: 15 entries.

**Vault overview** — Total file count, content folder count, active folders in last 7 days.

Empty sections: write "None", do not skip.

#### `pulse week` — Weekly gap analysis

Read: all content folder activity last 7 days, last 7 days of wrap logs.

**This week's progress** — Each active folder: name, what advanced, next step.

**Recent developments** — Notes added or modified this week, which are near completion.

**Gap analysis** — Compare wrap log stated priorities vs. actual file changes:
- Said important but did not touch (stated priority, no corresponding file change)
- Did work but did not mention (file changes without wrap log mention)

If fewer than 3 days of wrap logs: note "Insufficient records — gap analysis may be inaccurate."

#### `pulse patterns` — Undercurrents and clusters

Scan: all content folders, wrap logs (last 30 days), all inbox files.

**Undercurrent themes** — Recurring topics without standalone articles. Criteria: appears in 3+ different files, no standalone article or draft. Each: theme name, count and file list (max 5, [[wiki link]]), assessment (worth developing?). Limit: 10, reverse frequency order.

**Forming idea clusters** — 3+ notes covering similar concepts without a common parent, written on different dates. Each: suggested group name, notes (max 5, [[wiki link]]), shared theme summary (2–3 sentences), maturity (high/medium/low), suggested direction (article / project / framework / continue accumulating). Limit: 5, reverse maturity order.

---

### `/hirameki:harvest [save]`

**Purpose:** Harvest actionable ideas from existing content.
**Input:** Optional `save` to write summary.
**Requires:** research folder, wrap logs, inbox, all content folders.

Scan: all content folders, wrap logs (last 30 days), all inbox files.

Output — seven categories, max 5 each:

**Articles to write** — Topics with enough material to develop. Each: suggested title, source notes ([[filename]] list), what is still missing to start.

**Tools or projects to build** — Tool needs, process pain points, or clear product ideas. Each: description, source, estimated complexity (small / medium / large).

**Topics to research** — External concepts mentioned but not explored. Each: topic, vault context, why worth researching.

**People or communities to contact** — People or organisations mentioned and relevant to current direction. Each: name, vault context, reason. If none: "None".

**Ideas for different media** — Content better suited to video, visual diagram, talk, newsletter, podcast. Each: idea summary, suggested medium, why that format fits.

**Untransacted value** — Expertise or skills not yet converted to revenue. Each: skill or knowledge, possible monetisation, vault evidence. If none: "None".

**Ideas ready to graduate** — Half-formed ideas with enough density for a standalone note. Each: source location ([[filename]] + passage), core claim (one sentence), suggested destination folder, related existing notes.

Graduate criteria: clear core claim, relates to at least one existing vault theme, has enough density.

### Graduate flow (two-phase regardless of `save`)

List candidates → pause → wait for user to confirm which to graduate.

For each selected idea:
1. Show the full path to be created; wait for confirmation
2. Create markdown file with: title, core claim, source context, vault connections ([[wiki link]]), directions to develop
3. Print actual path created

With `save`: write main harvest summary to `{research}/harvest/`. Same day: append update.

---

### `/hirameki:graduate <note>`

**Purpose:** Promote a note to a stable, permanent concept card.
**Input:** Note title or [[wikilink]] (required).
**Requires:** all content folders.

Steps:
1. Find the note in the vault
2. Read and evaluate: does it have a clear core claim? Is it stable enough to be a reference?
3. Validate/add frontmatter: ensure `tags`, `status: reference`, `source` are present
4. Suggest links to related concept cards in the vault
5. Show proposed changes; wait for confirmation before writing
6. Print path after writing

---

### `/hirameki:tasks [days|stuck]`

**Purpose:** Aggregate next actions from wrap logs and journal.
**Input:** Optional — number of days (default 3) or `stuck` / `stuck N`.
**Does not write to file.**

#### Default mode

Scan last N days of `{daily}/YYYY-MM-DD.md` (extract "Next" items from each Wrap block). Scan today's and yesterday's `{journal}/YYYY-MM-DD-*.md` (extract uncompleted items from "Open items").

1. Collect next actions from past N days
2. Deduplicate and rank: normalise, group similar tasks, sort by frequency then recency
3. Output: ordered list with sources. Items appearing 3+ times get ⚠ prefix.

#### Stuck mode — `tasks stuck [N]`

Scan N days (default 7). Find tasks appearing 2+ times in "Next" blocks but never in "Done" blocks. Classify as: **blocked** / **deferred** / **forgotten** / **persistent**.

Rules: read-only, no file modifications.

---

## Maintenance

### `/hirameki:tidy [tags|fix|full|lint]`

**Purpose:** Frontmatter health check and cleanup.
**Input:** Optional mode argument.
**Requires:** all content folders, inbox, wrap logs.

**Modes:**

| Call | Runs |
|------|------|
| `tidy` (no arg) | Missing field check + Consistency check |
| `tidy tags` | Tag convergence analysis only |
| `tidy fix` | Missing + Consistency + Auto-fix |
| `tidy full` | All blocks |
| `tidy lint` | Content health check only |

**Scan scope:** All content folders (recursive), all inbox files, wrap logs (last 30 days). Skip hidden directories, dependency/build directories such as `node_modules`, and files ignored by Git when available.

#### Missing field check (tidy / fix / full)
- Files with no frontmatter
- Files with frontmatter but missing `tags`, `status`, or `source`
- Any required field is empty or has the wrong type

#### Per-file frontmatter review (tidy / fix / full)
Run a lightweight detection pass first. If 50 or fewer files need frontmatter handling, review and process only those files; do not expand to a full-vault review or ledger. More than 50 affected files triggers review of every file in scope and a CSV ledger beside the report, with one row per file. Classify reviewed files as `pass`, `pass-project-schema`, `auto-fixable`, `requires-judgment`, or `exclude-candidate`. A summary count alone is not a completed full review.

#### Consistency check (tidy / fix / full)
- `status` not in allowed set: `published`, `draft`, `reference`, `outline`, `spec`, `log`, `archive`
- `source` not in allowed set (if field exists): `self`, `claude-code`, `codex`, `agent`, `external`
- Case-inconsistent synonymous tags (e.g., `AI-alignment` vs `ai-alignment`)
- Underscore vs hyphen inconsistency in tags
- Obvious duplication between `topic` and `tags`

The listed status/source values are defaults, not proof that every project-specific value is malformed. Project vocabulary takes precedence. A URL in `source` is valid provenance; propose, but do not automatically perform, a `source: external` + `source_url` migration.

#### Redundancy check (full only)
- Files with more than 6 tags
- `created` field format inconsistent (should be YYYY-MM or YYYY-MM-DD)

#### Tag convergence analysis (tags / full)
Count tag usage across entire vault:
- Top 10 most-used tags (core tags)
- Semantically similar but differently named tags (candidate merge groups)
- Tags that appear only once (isolated tags — list each one)

#### Content health check — lint mode only

**Contradiction detection:** Pairs of notes making conflicting claims about the same topic. Each: Note A [[filename]] — claim; Note B [[filename]] — contradicting claim; Severity: direct contradiction / tension / evolution.

**Stale claims:** Notes with `status: published` or `reference` not modified in 90+ days. Each: [[filename]] — last modified — topic summary — question: is this still accurate?

**Orphan notes:** Notes with zero incoming [[wiki links]] from other notes (excluding daily, inbox, system folders). Each: [[filename]] — created date — topic — suggestion.

**Dead links:** [[wiki links]] pointing to non-existent files. Each: Source [[source-note]] — broken link text — suggestion.

Lint mode is read-only. After lint output, if any area has N > 0 issues, append:

```
## Cross-reference suggestions

### Dig deeper into contradictions
(Only if contradictions N > 0)
Run `/hirameki:lens <topic>` on the most-conflicted topic to examine weaknesses in depth.
Most-conflicted topic found: {topic}

### Surface vault patterns
(Only if isolated tags >= 5 or orphan notes >= 5)
Run `/hirameki:pulse patterns` to see recurring themes and gaps across the full vault.

### Handle stale claims
(Only if stale claims N > 0)
For claims that are still valid: run `/hirameki:graduate <note>` to promote to a stable concept card.
For claims that are outdated: update `status: archive` in frontmatter.
Stale files needing attention: N
```

If all areas = 0, omit the cross-reference section entirely.

#### Fix logic (fix mode only)

Show full list of all planned changes. Wait for confirmation before executing.

Auto-fixable:
- Add missing frontmatter skeleton (empty tags + `status: draft`)
- Normalise tag casing (use whichever variant appears more often)
- Normalise underscore vs hyphen (use hyphen)
- Remove obvious duplication between `topic` and `tags`

Requires per-item confirmation:
- Merging semantically similar tags
- Trimming files with more than 6 tags
- Deleting isolated tags

After fixing, recalculate health score and output a diff summary.

**Write:** `{research}/tidy/YYYY-MM-DD.md`. Same day: append update with health score change. Report at most 50 issues per run.

---

### `/hirameki:__init`

**Purpose:** First-time setup and vault configuration.
**Input:** None.

#### Mode A: First-time setup

Run when `## Vault Structure` does not exist in `<vault>/AGENTS.md`, `vault-local.md`, or `CLAUDE.md`.

**Step 1 — Vault detection:** Try CWD → CLAUDE.md path → obsidian.json (filter built-in sandbox). Prompt if multiple found. If nothing: ask user.

**Step 2 — Language:** Ask: Traditional Chinese / English / Japanese / Other.

**Step 3 — Folder resolution:** Match each purpose to first existing candidate (see folder table above). If no match: ask user where to create, then create after confirmation.

**Step 4 — Write config:** Two writes, one per audience.
```
# ~/.claude/vault-local.md  (per-machine)
## Vault Structure
vault: {full vault path}
language: {language}
```
```
# {vault}/AGENTS.md  (travels with the vault)
## Vault Structure
daily: {folder name}/
inbox: {folder name}/
research: {folder name}/
journal: {folder name}/
handoff: {folder name}/
templates: {folder name}/
```

**Step 5 — Shared policies vault (optional):** Ask. If yes: verify path, create symlink `~/.claude/rules/policies/ → {policies path}`, add `shared-policies: {path}` to vault-local.md.

**Step 5b — Personal policies vault (optional):** Ask. Same flow with `~/.claude/rules/personal/`.

**Step 6 — Reference doc sync:** Check `{vault}/_hirameki_cmds/`. Missing → create and copy reference docs for chosen language. Exists and non-empty → ask before overwriting.

Language mapping:
- Traditional Chinese → `hirameki-cmds-short-zh-TW.md` + `hirameki-cmds-full-zh-TW.md`
- Japanese → `hirameki-cmds-short-ja.md` + `hirameki-cmds-full-ja.md`
- English or other → `hirameki-cmds-short.md` + `hirameki-cmds-full.md`

#### Mode B: Reconfigure

Run when config already exists. Ask what to update (language / specific folder / shared policies / personal policies / reference docs / start over). Only modify selected items. Language and vault path go to `vault-local.md`; folder paths go to `<vault>/AGENTS.md`.

---

## Write Behavior Summary

| Command | Writes to | Trigger | Same-day repeat |
|---------|-----------|---------|-----------------|
| `triage` | daily + journal + handoff | Per step (save/skip) | Follows each primitive's behavior |
| `lens` | research/lens/ | Per step (save/skip) | Each step is a separate file |
| `compose` | research/compose/ | Per step (save/skip) | Each step is a separate file |
| `wrap` | daily | Always | Appends new Wrap block |
| `journal` | journal | Always | Same topic appends; different creates new |
| `handoff` | handoff | Always | Same date replaces |
| `arc` | research/arc/ | Always | Same concept appends |
| `bridge` | research/bridge/ | Always | Same pair appends |
| `challenge` | research/challenge/ | Always | Same topic appends |
| `reflect` | research/reflect/ | With `save` | Same question appends |
| `frame` | research/frame/ | With `save` | New file per idea |
| `mekiki` (repo) | research/ | Always | New file per repo |
| `mekiki` (article) | inbox/ | Always | New file per article |
| `graduate` | content folder | After confirm | New file each time |
| `harvest` | research/harvest/ | With `save` | Appends update |
| `tidy` | research/tidy/ | Always | Appends update |
| `critique` | _writing_lab/benchmark/ | Always | New file per critique |
| `tasks` | none | — | — |
| `next` | none | — | — |
| `pulse` | none | — | — |

## Shared rules

- All timestamps use local time HH:MM (24-hour)
- All file references use [[wiki link]] format
- All write commands show a preview and full path before executing; print actual path after
- Output language read from `~/.claude/vault-local.md` `## Vault Structure`
- Vault path always resolved at runtime from vault-local.md, folders from `<vault>/AGENTS.md` — never hardcoded
