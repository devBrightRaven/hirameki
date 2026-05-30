---
description: >
  Find the logical weaknesses in an argument or position — scan your vault for
  all claims on the topic, then expose contradictions, unverified assumptions,
  logic gaps, and evidence gaps.
  For tracing concept evolution use /hirameki:arc.
  For the full understanding workflow use /hirameki:lens.
argument-hint: "<argument or topic>"
---

Read `## Vault Structure` from `~/.claude/vault-local.md` (fall back to `~/.claude/CLAUDE.md` if not found) to get the vault path, the research folder location, and the list of content folders.
If the section does not exist or required fields are missing, stop and respond: "Setup not complete. Please run `/hirameki:__init` first."

Input: $ARGUMENTS
- If $ARGUMENTS is empty, ask: "Challenge which argument or topic?" in the language specified in `## Vault Structure` → `language`. Wait for the answer.
- If $ARGUMENTS ends with `save`, strip `save` and write the result to a file after analysis.

Scan scope: all vault files that mention the topic.

---

## Analysis steps

1. Collect all claims and arguments about the topic from the vault
2. Examine the logical structure and evidence base of each claim
3. For each claim, check only what applies:
   - **Internal contradiction**: conflicting statements across vault files
   - **Unverified assumption**: claim rests on an unproven premise
   - **Logic gap**: missing steps in the argument
   - **Evidence gap**: claim lacks supporting data or examples
4. Cite `[[filename]]` and relevant passage for each weakness found

---

## Output structure

```
## Claims
All major claims about this topic found in the vault.
For each: claim (one sentence) — source [[filename]]

## Weaknesses
For each claim that has weaknesses:

### Claim: {claim}
- Internal contradiction: {details, cite [[filename]]} (omit if none)
- Unverified assumption: {details} (omit if none)
- Logic gap: {details} (omit if none)
- Evidence gap: {details} (omit if none)

(Omit entirely any claim with no weaknesses)

## Assessment
Overall: solid / mostly solid with gaps / needs major work
Top 1–3 weaknesses worth addressing first.
```

---

## Write logic

Write target: `{research}/challenge/YYYY-MM-DD-{topic-summary}.md`

Always print the full output to the terminal first.

If `save` was in the input (or user requests saving):
- Show filename and full path — wait for confirmation before writing
- Print the full path after writing

---

## Rules

- If search results exceed 20 files, list only the 20 most relevant
- Use `[[wiki link]]` format for all file references
- Timestamps use local time in HH:MM (24-hour)
- Write output in the language specified in `## Vault Structure` → `language`
