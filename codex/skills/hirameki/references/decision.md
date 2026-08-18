---
description: Promote a durable decision into a lifecycle-managed decision node without duplicating journal or handoff history.
---

Resolve vault configuration through the umbrella Hirameki adapter. Use the journal folder and language from the canonical `## Vault Structure` section. If setup is incomplete, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Promote one durable decision into `{journal}/decisions/YYYY-MM-DD-{slug}.md`.

Input: $ARGUMENTS (decision topic or statement — optional)

- If input is empty, infer one candidate from explicit decisions in the current session. Show `Candidate: {decision} — assess for promotion?` and wait for yes/no confirmation.
- If no explicit decision exists, stop. Do not invent one.

## Promotion gate

Create a decision node only when at least one condition is supported by session or vault evidence:

- it constrains future work, architecture, scope, data, safety, cost, or product behavior;
- a reasonable collaborator could choose differently and needs the rationale;
- alternatives or trade-offs were explicitly considered;
- reversal would be costly, risky, or operationally disruptive;
- the same issue has caused repeated regressions or re-litigation;
- future sessions need the rationale to avoid silently changing direction.

If none applies, recommend `journal` for reasoning or `handoff` for pickup context and stop without writing.

## Resolve existing state

Search `{journal}/decisions/`, related journal notes, and handoffs for the same decision. Keep observations, inferences, assumptions, decisions, and later outcomes distinct.

- No matching decision node: create an `active` node.
- Matching active node, rationale unchanged: append a dated evidence/review entry only when new evidence matters; otherwise do not write.
- Matching active node, decision changed: create a new `active` node and mark the old node `superseded`, with reciprocal wiki links.
- Decision no longer constrains future work and has no replacement: mark it `closed` and append the reason.

Never silently overwrite the decision, rationale, alternatives, or earlier evidence.

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

Use links for journal and handoff provenance. Do not copy their narrative into the node. Omit empty optional links instead of writing placeholders.

## Write safety

Before any create, append, status change, or folder creation:

1. Show the promotion-gate evidence.
2. Show every affected full path.
3. Show the complete new or appended content and any exact frontmatter status change.
4. Wait for explicit confirmation.

After confirmation, create `{journal}/decisions/` if required, apply only the shown edits, then print every written full path. Do not move, delete, publish, or sync notes.

Write output in the language specified in `## Vault Structure` → `language`.
