---
description: Concept analysis (arc / bridge / ghost / stress-test)
---

Read `## Vault Structure` from `~/.claude/CLAUDE.md` to get the vault path, the research folder location, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Analyse the input and automatically select a mode based on its shape.

Input: $ARGUMENTS
- If $ARGUMENTS is empty, ask: "Explore what? (concept, two topics, question, or test: argument)" and wait for the answer before continuing. Ask in the language specified in `## Vault Structure` → `language`.

## Mode detection

| Input shape | Mode | Example |
|-------------|------|---------|
| Single concept or word | **Arc** — concept evolution timeline | `explore agency` |
| Two topics separated by `and`, `與`, or `と` | **Bridge** — hidden connections between two topics | `explore design and engineering` |
| Ends with `?` or `？` | **Ghost** — answer in your voice | `explore how much autonomy should AI have?` |
| Starts with `test:` | **Stress-test** — pressure-test the argument | `explore test: the limits of prompt engineering` |

Append `save` to any input to write the result to a file.

---

## Arc mode — concept evolution tracking

Scan scope: entire vault, prioritising daily and content folders.

Logic:
1. Check `{research}/arc/` for an existing file about the same concept today (match by filename keyword)
2. If found → append mode
3. If a possibly related file is found but uncertain → list candidates and ask whether to append or create new
4. If not found → create mode

Output structure:

```
# Concept tracking: {concept}

> Analysis time: YYYY-MM-DD HH:MM

## First appearance
Earliest file where this concept appeared, and the context. Quote up to 3 sentences.
Date: YYYY-MM-DD

## Evolution timeline
- YYYY-MM-DD | [[filename]] | How this concept was used or positioned in this file (one line)

## Current state
Which topics this concept connects to now, any contradictory uses, any drafts developing it.

## Unexplored angles
Aspects of this concept not yet addressed anywhere in the vault.
```

Append mode adds to the existing file:

```
---

## Tracking update [HH:MM]

### Timeline additions
- [New mentions since last analysis]

### State changes
- [What changed since last analysis. If nothing, write "No significant change"]

### Unexplored angles (updated)
- [Re-evaluate what remains unexplored]
```

Write target (when saving): `{research}/arc/YYYY-MM-DD-{concept}.md`

---

## Bridge mode — hidden connections between two topics

Scan scope: entire vault.

Logic:
1. Check `{research}/bridge/` for an existing file about the same pair today (match by keywords, order-independent)
2. If found → append mode; if not → create mode

Output structure:

```
# Bridge analysis: {topic A} and {topic B}

> Analysis time: YYYY-MM-DD HH:MM

## Direct intersections
Files that mention both topics. For each: [[filename]], how the two topics are related there.
If none, write "No direct intersections."

## Bridge notes
Files that mention only one topic but could form a connection. Explain why each might be a bridge.
Limit: 5 files.

## Connection hypotheses
1–3 hypotheses about deeper connections between the two topics.
For each: hypothesis, confidence level (strong / medium / weak), evidence.
```

Append mode adds to the existing file:

```
---

## Tracking update [HH:MM]

### New intersections
- [New intersections or bridge notes since last analysis]

### Hypothesis validation
- [New evidence supporting or contradicting earlier hypotheses]
```

Write target (when saving): `{research}/bridge/YYYY-MM-DD-{topic-A}-and-{topic-B}.md`

---

## Ghost mode — answer in your voice

Scan scope: all completed articles in content folders (exclude drafts/ and thoughts/ subdirectories).

Steps:
1. Analyse writing style: sentence patterns, vocabulary, argument structure, recurring rhetorical moves
2. Extract existing positions and arguments relevant to the question
3. Compose an answer using that style and those positions

Output structure:

```
[Answer]
Answer the question in the author's voice. Match the length of a typical paragraph from their writing.

[Evidence]
List the notes referenced: [[filename]], the specific passage or position drawn from. Limit: 5.

[Confidence annotation]
Note which parts of the answer have direct vault support, and which are style-inferred extensions.
```

Write target (when saving): `{research}/ghost/YYYY-MM-DD-{question-summary}.md`

---

## Stress-test mode — pressure-test the argument

Input: strip the leading `test:` — the remainder is the topic.

Scan scope: all files in the vault that mention the topic.

Steps:
1. Collect all claims and arguments about the topic from the vault
2. Examine the logical structure and evidence base of each claim

Output structure:

```
[Claim list]
All major claims about this topic found in the vault. For each: claim (one sentence), source [[filename]].

[Weakness analysis]
For each claim, check the following (only list what applies):
- Internal contradiction: conflicting statements across vault files
- Unverified assumption: claim rests on an unproven premise
- Logic gap: missing steps in the argument
- Evidence gap: claim lacks supporting data or examples
Cite specific [[filename]] and passage for each weakness.

[Overall assessment]
How solid is the overall argument for this topic: solid / mostly solid with gaps / needs major work.
List the 1–3 weaknesses most worth addressing first.
```

Write target (when saving): `{research}/stress-test/YYYY-MM-DD-{topic-summary}.md`

---

## Shared rules

- If search results exceed 20 files, list only the 20 most relevant and note the total count
- Use [[wiki link]] format for all file references
- Timestamps use local time in HH:MM format (24-hour)
- Always print the full analysis output to the terminal
- Show the filename, mode (create / append), content summary, and full path, then wait for confirmation before writing
- Print the full path after writing
- Create the folder if it does not exist, and print the full path

Write output in the language specified in `## Vault Structure` → `language`.
