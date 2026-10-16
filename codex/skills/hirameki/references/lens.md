---
description: >
  Explore a question using sourced history, positions, relationships, weaknesses,
  opportunities or recurring patterns; propose concept cards only when useful.
argument-hint: "[history|positions|bridge|challenge|opportunities|patterns|cards|random] <question or scope>"
---

For a natural-language request, apply `references/capabilities/natural-routing.md` under the currently loaded skill root; do not require the user to name this capability. Preserve the actual request as input.

Resolve vault configuration through the umbrella Hirameki adapter. Read `## Vault Structure` from `<vault>/AGENTS.md` only when this task needs vault material; use explicit supplied material without a vault scan.
If required configuration is missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first." Supplied text may be analysed without reading a vault; resolve configuration only before a vault read or write.

Input: $ARGUMENTS. Infer the question and requested scope from supplied context; if neither is identifiable, ask one focused question.

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

## Integrated result

Give one coherent answer with relevant history, evidence, tensions, unknowns and next useful questions. Use `[[wiki links]]` plus passage anchors for vault sources; do not invent connections, references or the author's position. Persist only useful requested artifacts, not a report for every capability.

## Concept cards

For a card discovery or promotion request, load the delivered `capabilities/concept-card.md` (under package `references/` in Claude; under the loaded skill's `references/` in Codex). This is the shared atomic claim, source and existing-card check contract. A discovery-only request proposes candidates without writing.

A reusable lesson supported by at least two independent events may prompt manual graduation once; first check existing cards and previously recorded rejection or deferral within the relevant scope. Two agent reports of one event count once. Never create a card or change a MOC automatically.

## Saving

Analysis alone never authorizes a write. If saving is requested, show the full draft and target path, then ask `Action? (save this / skip / edit)`. Save only the displayed, approved content; changes require another display and approval. A new analysis note belongs at `{research}/lens/YYYY-MM-DD-{slug}.md`; preserve existing notes, naming and frontmatter. Card destinations follow the shared card contract.

Print the full path after each successful write. On failure, report what did and did not persist; do not claim completion. Write output in the language specified in `## Vault Structure` → `language`.
