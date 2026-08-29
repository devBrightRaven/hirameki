---
description: >
  Unified decision-forming vault workflow: frame an unresolved choice, trace
  evidence and trade-offs, and optionally preserve an explicitly confirmed
  decision as a lifecycle-managed node. Use when the user is weighing options,
  asks whether they should do something, compares plausible approaches, or asks
  for help structuring an unresolved decision; or says "要不要", "應該選",
  "該不該", "猶豫", "should I", "which one", "torn between", "pros and cons",
  "どうしよう", "どちら", "迷って", "比較". Triggers on decision-forming intent even without explicit
  invocation. Not for passing preferences, mechanical actions with no meaningful
  choice, or requests only to record an already documented fact.
---

Resolve vault configuration through the umbrella Hirameki adapter. Use the journal
folder and language from the canonical `## Vault Structure` section. If setup is
incomplete, stop and respond: "Setup not complete. Please run `/hirameki:__init`
to configure the vault root or canonical folder layout."

Input: `$ARGUMENTS` (decision question or context — optional)

Explicit invocation accepts only `decision-trace`, `/decision-trace`, and
`hirameki:decision-trace`. All other decision-forming requests use the same
workflow through implicit intent triggering.

If the input is empty and no decision-forming topic is available, ask for the
decision question in the configured language and wait. Do not invent a decision
or infer that a candidate is decided.

## Establish the decision state

Determine the current state from what the user explicitly says and the available
evidence:

- `unresolved`: the user is still choosing among viable directions.
- `forming`: a direction is emerging, but material assumptions or trade-offs remain.
- `decided`: the user has explicitly selected or confirmed a choice.
- `reviewing`: an existing decision is being checked against new evidence, replaced,
  or closed.

Do not silently promote an inferred candidate into `decided`. A passing preference
or a mechanical action is not a decision-forming request.

## Build the trace

For `unresolved` or `forming`, scan all relevant content folders, recent daily and
journal records, and related decision nodes, handoffs, and research. Present only
information that changes the decision, in this order:

- decision question;
- viable options;
- evidence and its source;
- assumptions and unknowns;
- constraints and non-negotiables;
- consequences;
- reversal cost;
- one key unresolved question.

Keep observation, evidence, inference, assumption, preference, and decision
distinct. Preserve multiple plausible interpretations until evidence narrows them.
The agent may identify trade-offs and inconsistencies, but must not choose for the user,
recommend a direction, or turn a likely candidate into a conclusion.

Use this read-only shape:

```markdown
# Decision trace: {topic}

> Trace time: YYYY-MM-DD HH:MM
> State: unresolved / forming / decided / reviewing

## Decision question
{the choice being formed}

## Viable options
- {option}

## Evidence
- Observed: {traceable fact and source}
- Inferred: {bounded inference, only when needed}

## Assumptions and unknowns
- Assumption: {what must be true}
- Unknown: {what is not yet verified}

## Constraints
- {non-negotiable or bounded resource}

## Consequences
- {likely effect of each viable direction}

## Reversal cost
- {cost, risk, or disruption of changing direction later}

## Key unresolved question
{one question whose answer would materially change the choice}
```

## Capture an explicit decision

Only move to `decided` after the user states or confirms the choice. The agent must
not choose for the user. Record the chosen direction, the reasoning that actually
supported it, alternatives considered, consequences and accepted costs, evidence
still missing, and an observable revisit trigger. Do not manufacture rationale from
generic best practices or from an unconfirmed preference.

## Promotion gate

After the choice is explicit, assess whether it should constrain future work. Create
a decision node only when at least one condition is supported by session or vault
evidence:

- it constrains future work, architecture, scope, data, safety, cost, or product behavior;
- a reasonable collaborator could choose differently and needs the rationale;
- alternatives or trade-offs were explicitly considered;
- reversal would be costly, risky, or operationally disruptive;
- the same issue has caused repeated regressions or re-litigation;
- future sessions need the rationale to avoid silently changing direction.

If no condition applies, recommend `journal` for reasoning or `handoff` for pickup
context, but do not write. The promotion gate never turns an unresolved or forming
trace into a decided choice.

## Resolve existing state

Decision nodes use `{journal}/decisions/YYYY-MM-DD-{slug}.md`.

Search `{journal}/decisions/`, related journal notes, and handoffs for the same
decision. Keep observations, inferences, assumptions, decisions, and later outcomes
distinct.

- No matching decision node: create an `active` node.
- Matching active node, rationale unchanged: append a dated evidence/review entry
  only when new evidence matters; otherwise do not write.
- Matching active node, decision changed: create a new `active` node and mark the
  old node `superseded`, with reciprocal wiki links.
- Decision no longer constrains future work and has no replacement: mark it `closed`
  and append the reason.

Never silently overwrite the decision, rationale, alternatives, or earlier evidence.
Preserve `active`, `superseded`, and `closed` lifecycle behavior.

## Confirmation action model

After showing the promotion evidence, affected paths, complete draft, and proposed
status changes, ask:

```text
Action? (save this / skip / edit)
```

- `save this` applies only the shown decision changes and prints every written path.
- `skip` stops without writing.
- `edit` applies the user's requested draft changes, shows the complete revised draft
  and affected paths, then asks the same action menu again.

The `decision-trace` invocation selects this workflow; it does not authorize a write.
No durable write occurs before the user explicitly selects `save this`.

## Decision node

```markdown
---
tags:
  - decision
status: active
source: codex
decided: YYYY-MM-DD
reviewed: YYYY-MM-DD
---

# {decision title}

## Decision
{one concrete statement of what is now chosen or constrained}

## Why it matters
{future behavior, scope, or work this decision constrains}

## Context and evidence
- Explicitly stated: {traceable fact, quote, command output, or named file}
- Reasonably inferred: {only when needed}
- Insufficient data: {important unknowns}

## Alternatives considered
- {alternative} — {why it was not chosen}

## Consequences
- {what future work should do}
- {risk or trade-off accepted}

## Revisit when
- {observable reversal trigger}

## Related records
- Journal: [[...]]
- Handoff: [[...]]
- Supersedes / superseded by: [[...]]
```

Use links for journal and handoff provenance. Do not copy their narrative into the
node. Omit empty optional links instead of writing placeholders.

## Write safety

Before any create, append, status change, or folder creation:

1. Show the promotion-gate evidence.
2. Show every affected full path.
3. Show the complete new or appended content and every exact frontmatter status change.
4. Ask `Action? (save this / skip / edit)` and wait for one of those actions.

After `save this`, create `{journal}/decisions/` if required, apply only the shown
edits, and print every written full path. Do not move, delete, publish, or sync notes.

Write output in the language specified in `## Vault Structure` → `language`.
