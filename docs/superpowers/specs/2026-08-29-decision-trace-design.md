# Decision Trace Design

## Purpose

Replace the split `decide` and `decision` behaviors with one canonical workflow that helps a person form a decision, preserves the reasoning path, and only then offers to save a durable decision node.

The workflow must not assume that invoking `decision` means a decision has already been made.

## Public interface

- The only command and canonical skill is `decision-trace`.
- Remove `decision` and `decide`; do not retain aliases, redirects, deprecated stubs, or other Hirameki command or skill names beginning with `decision`.
- Move decision-language triggers into `decision-trace`, so normal decision-making requests can invoke it without typing the full command.
- There is no second decision-making implementation or compatibility surface.

## Triggering

Implicit invocation applies when the user is weighing options, asks whether they should do something, compares plausible approaches, or asks for help structuring an unresolved decision.

Explicit invocation accepts only `decision-trace`, `/decision-trace`, and `hirameki:decision-trace`.

Do not trigger for a passing preference, a mechanical action with no meaningful choice, or a request that only asks to record an already documented fact.

## Unified workflow

### 1. Establish the decision state

Determine whether the input is:

- unresolved: the user is still choosing;
- forming: a direction is emerging but material assumptions or trade-offs remain;
- decided: the user has explicitly selected an option;
- reviewing: an existing decision may need new evidence, replacement, or closure.

Do not silently promote an inferred candidate into the `decided` state.

### 2. Build the trace

For unresolved or forming decisions, present only information that changes the decision:

- the decision question;
- viable options;
- evidence and its source;
- assumptions and unknowns;
- constraints and non-negotiables;
- consequences and reversal cost;
- the key unresolved question.

Distinguish observation, evidence, inference, assumption, preference, and decision. Preserve multiple plausible interpretations until evidence narrows them.

The agent may identify trade-offs and inconsistencies, but must not choose for the user.

### 3. Capture an explicit decision

Only move to `decided` when the user states or confirms the choice. Record:

- the chosen direction;
- the reasoning that actually supported it;
- alternatives considered;
- consequences and accepted costs;
- evidence still missing;
- a revisit trigger.

Do not manufacture rationale from generic best practices.

### 4. Offer durable storage

After a decision is explicit, assess whether it should constrain future work. Offer a lifecycle-managed decision node only when the existing promotion gate is met.

Saving remains a separate action. Show the complete draft, affected paths, and lifecycle changes, then ask:

```text
Action? (save this / skip / edit)
```

`decision-trace` selects the workflow; it does not authorize a write. Until `save this`, the workflow is read-only.

An unresolved or forming trace may cross sessions only after `save this`, and then only as a journal note or handoff. It never enters `{journal}/decisions/`. Formation state and decision-node lifecycle remain separate: only an explicitly decided choice becomes a node; that node may be `active`, `superseded`, or `closed`, and decision-node frontmatter never gains `decision_state` or another formation-state field.

### 5. Maintain lifecycle history

Keep the existing `active`, `superseded`, and `closed` decision-node semantics. Link journal and handoff records instead of duplicating their narrative. Never overwrite earlier rationale or evidence silently.

## Runtime ownership

- Claude owns its command and skill surfaces.
- Codex owns the umbrella adapter and same-name references.
- Both surfaces must route to the same behavioral contract without depending on the other runtime's configuration.
- Before Codex shows or writes a decision-node draft, its adapter verifies `source: codex` and rejects `source: claude-code`.
- The repository is the canonical source; installed plugin caches are deployment outputs, not editing targets.

## Migration

- Move the useful pre-decision behavior from `skills/decide/SKILL.md` into the canonical `decision-trace` skill.
- Move the durable-node behavior from `commands/decision.md` into the same canonical workflow.
- Replace `commands/decision.md` and the Codex `decision` route with the `decision-trace` command/reference route.
- Remove the independent `decide` skill so it does not consume discovery budget or drift into a second behavior.
- Remove all old `decision` and `decide` aliases instead of keeping compatibility stubs.
- Update generated command catalogs, multilingual summaries, README, changelog, plugin metadata, and tests that enumerate commands or skills.

## Acceptance criteria

1. Invoking `decision-trace` with no explicit completed decision starts by framing the decision, not by asking `assess for promotion?`.
2. An unresolved decision produces options, evidence, unknowns, constraints, consequences, reversal cost, and one key unresolved question without choosing for the user.
3. A decision node cannot be drafted as final until the user explicitly confirms a choice.
4. No vault write occurs before `save this`.
5. `decision-trace` reaches the same canonical behavior in Claude and Codex.
6. No `decision` or `decide` command, skill, alias, or redirect remains discoverable.
7. Existing decision-node lifecycle behavior remains covered by contract tests.
8. Claude and Codex installed runtimes are updated only through their documented deployment paths after repository validation passes.
9. A persisted unresolved or forming trace uses `save this` and lands in journal or handoff, never in the decision-node directory.
10. A Codex-created decision node cannot be shown or written with Claude provenance.
