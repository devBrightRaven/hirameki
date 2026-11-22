---
description: >
  Explore a question using sourced history, positions, relationships, weaknesses,
  opportunities or recurring patterns; propose concept cards only when useful.
argument-hint: "[history|positions|bridge|challenge|opportunities|patterns|cards|random] <question or scope>"
---

For a natural-language request, apply `references/capabilities/natural-routing.md` under the currently loaded skill root; do not require the user to name this capability. Preserve the actual request as input.

Input: $ARGUMENTS. Infer the question and scope from the request and supplied
context. If a missing decision would materially change the answer or the
authorized sources, ask one focused question before retrieving material.
When supplied passages suffice, answer directly from them.

## Question-driven exploration

Choose only the capabilities needed for the question, not a fixed arc / position / bridge / challenge sequence. Do not generate four reports or require per-stage save prompts.

| Intent or optional mode | Work to perform |
|---|---|
| history | Source-anchored timeline: first evidenced appearance, changes, current position and unexplored angles. Dates establish provenance, not authority by themselves. |
| positions | Extract explicit claims; separate quotations, inferred positions and contradictions. |
| bridge | Compare the named topics using direct intersections and supporting notes; distinguish observed relationships from hypotheses. |
| challenge | Test stated claims for contradiction, assumptions, logic and evidence gaps; do not manufacture objections. |
| opportunities | Surface actionable articles, tools, research questions or collaborations supported by the supplied material; explain audience, usefulness and missing evidence. |
| patterns | Identify repeated themes and unnamed clusters; copies of one event are not independent occurrences. Frequency does not prove importance. |
| cards | Discover atomic, reusable claims and follow the concept-card contract below. |
| random | Only on an explicit request: sample a bounded set from configured content folders, state the selection and exclusions, and admit when no supported connection exists. |

State inspected scope, sources and coverage limits. Start with supplied notes, topics or folder paths; expand only as needed to answer the question. Do not silently scan the entire vault for a narrow question. An unreadable source is not an empty source.

For supplied passages and retrieved notes alike, identify who made each claim,
its scope and whether it records a decision. Attribute draft proposals and
third-party quotations to their sources. Treat explicit adoption or replacement
by the decision owner as evidence of change within its stated scope. A later
date alone leaves conflicting claims unresolved. State an unrecorded reason as
unknown, count repeated copies as one source event, and omit unrelated matches.

## Evidence retrieval

For Vault-dependent work only, resolve configuration before opening notes or saving.
Resolve vault configuration through the umbrella Hirameki adapter and use the needed folders from `## Vault Structure` in `<vault>/AGENTS.md`.
If required configuration is missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

When the user names a topic rather than every note, use available file/search or
Obsidian tools in the authorized folder with topic names, task IDs or distinctive
phrases. Read candidate passages and their dates/source links; a filename match
or search snippet is not evidence of the author's position. Follow relevant
links only as needed. If evidence is insufficient, expand within the authorized
scope or report the gap; do not silently search another vault.

## Integrated result

Give one coherent answer with relevant history, evidence, tensions, unknowns and next useful questions. Use `[[wiki links]]` plus passage anchors for vault sources; do not invent connections, references or the author's position. Persist only useful requested artifacts, not a report for every capability.

## Concept cards

For a card discovery or promotion request, load the delivered `capabilities/concept-card.md` (under package `references/` in Claude; under the loaded skill's `references/` in Codex). This is the shared atomic claim, source and existing-card check contract. A discovery-only request proposes candidates without writing.

A reusable lesson supported by at least two independent events may prompt manual graduation once; first check existing cards and previously recorded rejection or deferral within the relevant scope. Two agent reports of one event count once. Never create a card or change a MOC automatically.

## Saving

Analysis alone never authorizes a write. If saving is requested, show the full draft and target path, then ask `Action? (save this / skip / edit)`. Save only the displayed, approved content; changes require another display and approval. A new analysis note belongs at `{research}/lens/YYYY-MM-DD-{slug}.md`; preserve existing notes, naming and frontmatter. Card destinations follow the shared card contract.

Print the full path after each successful write. On failure, report what did and did not persist; do not claim completion. Use the requested language, otherwise the resolved vault language when applicable or the current conversation language.
