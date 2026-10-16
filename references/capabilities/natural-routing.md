# Natural-language capability routing

The user does not need to know next, lens or compose. Treat these names as
capabilities, not a required menu. Explicit workflow requests take precedence.
Choose only what materially helps the current request; do not run all entries.

| Requested outcome | Capability |
|---|---|
| Resume recorded work, identify remaining tasks or examine stuck work | next; tasks or stuck mode when requested |
| Connect named notes, trace a viewpoint or distil reusable concepts | lens; choose only relevant modes |
| Select material across vault notes, assemble a sourced work, or manage author positions and a requested vault destination | compose; preserve edit versus outline versus review intent |

For natural input, pass the user's actual request and supplied scope into the
selected contract. Do not discard it as if only text after a command name counted.
Do not ask the user to select an internal capability or announce a routing menu.
Resolve vault configuration only if the selected operation needs a vault read/write.

Boundaries:
- A code-task status question that current repository evidence answers does not
  require a vault scan. next is useful for recorded continuity and task views.
- Ordinary supplied-text writing, outlines, edits and translations use the host's
  installed language-writing entry directly. compose is not an extra compulsory
  layer before writing; multiple pasted paragraphs alone do not require it.
  Use compose when requested source selection, cross-note assembly, author-position
  handling or vault artifact delivery adds an actual Hirameki-specific need.
- A technical explanation, ordinary calculation, or unrelated comparison is not
  automatically lens or decision-trace. Use lens for requested synthesis of
  supplied/recorded thinking, not every question containing "relationship".
- Missing material or materially ambiguous scope warrants a focused question,
  not guessed vault selection. Multi-purpose work may use several capabilities
  only when the requested outcome needs them; no automatic triage afterwards.
- Choosing a capability does not authorize saving, publishing, memory changes,
  independent model calls or background work. Preserve its native approval gates.

Descriptions enable discovery; these instructions govern once loaded. Neither
proves that a host automatically selects them. Fresh-host behavior and installed
payload loading must be verified separately. No hook is required by this contract.
