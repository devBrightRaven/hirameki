# Session-trace acceptance

Scope: source rules for triage, journal (create and append) and handoff, with
canonical/Codex capability parity. No installed-plugin deployment is implied.

## Targeted behavioral cases

Use synthetic conversation and saved records only. Start a fresh dialogue per
case and host; explicitly load the modified source rules and shared capability.
Record source hashes, host/model, complete inputs, outputs and tool events.
Injected-source acceptance proves these instructions' behavior, not installed
discovery. A failed invocation is unavailable evidence, not a behavior failure.

| Case | Fixture | Required outcome |
|---|---|---|
| Completed batch | Batch accepted; next session must validate runtime loading; deployment unauthorized; wrap says only “validate loading” | Handoff proposed with validation scope and authorization boundary; completed task remains complete |
| Single event | One reproducible synthetic fixture failure fixed by an explicit encoding; no recurrence evidence | Scoped lesson proposed with one-event limit, source and recheck condition; no global policy promotion |
| Emerging clue | User wonders whether showing consequences earlier might help, explicitly uncertain; no test or decision | Journal clue with quote/context and unknown, no fabricated judgment change, lesson or task |
| Full coverage | Complete saved journal/lesson/handoff sections cover the same source, rationale, limits and pickup context; no new event | Reference existing coverage, no duplicate artifacts; explain why |
| Empty | Routine acknowledgement only; no progress, clue or pickup need | Nothing proposed or saved; no invented material |

Additional checks: a named closeout containing only a final choice must not erase
an uncovered rejected alternative; an unavailable record means coverage unknown;
append mode retains prior text and adds only new clues. Verify save this, skip,
edit and save all with displayed-path/text-bound approval, including absence of
any write before approval. Deterministic contract checks alone do not prove these
interactive behaviors.

## Downstream reading audit

akegarasu-no-yume source audited at revision
`1cc3cb574bc4006eb50e1b9aebe0a13b16479b3e`:

- `akegarasu_no_yume/sources.py`: a notes source config chooses root, include,
  exclude, frontmatter filters and body/section claim mappings. Claim types are
  observation, interpretation, unknown and considered.
- `akegarasu_no_yume/scan.py`: only configured sources are scanned. Frontmatter
  filters and skip rules apply; source digest and locator identify evidence.
  Claim text is bounded by the configured max_chars and truncation is marked.
- `examples/decision-notes.sources.json` is an example decision-only mapping,
  not proof that any particular machine has registered journal clues.

Conclusion: human-readable clues can preserve suitable source material, but
adding a section does not enroll it in ingestion. A later, separately authorized
integration must inspect the owner's source config, include journal status log,
map the actual language-specific sections and preserve distinct claim types.
Mapping a mixed entire journal to observation would erase uncertainty. Append
sections and repeated headings also need explicit parser acceptance before
claiming complete ingestion. No private source config was read or modified in
this audit; deployed ingestion remains unverified.

## Source acceptance result (2026-10-22)

This initial checkpoint predates the filesystem lookup/append follow-up below.

The local full gate `npm test -- --run` passed (one existing skip in the
68-test task-view CLI group). The shared-contract and adapter checks passed again
after a path-markup correction and LF normalization; those final edits did not
change selection semantics.

Native Codex app-server (`gpt-6.1-sol`, low) and Claude Code
(`claude-opus-5-5`, low) each exercised the five cases above, plus the closeout
case with a same-day matching journal. Both proposed an append preserving the
uncovered alternative and doubt, without changing the accepted decision or
creating a task. Across the six cases per host, candidate selection met the
targeted expectations. Codex proposed journal before lesson in the single-event
case; the lesson selection passed, but its later draft was not exercised.

One additional Claude single-event invocation returned only
`<thinking_mode>auto</thinking_mode>` despite CLI success. That response failed
acceptance and is retained as a failed output, not a capacity exclusion. A fresh
same-condition invocation produced a scoped lesson with its one-event limit.
This is twelve usable case results plus one failed output, not thirteen passes.

Trials explicitly injected the modified source, complete synthetic baseline and
resolved folder configuration; tool execution was disabled. They verify selection
and first-draft behavior, not filesystem saves, installed discovery or background
ingestion. Existing save guards were retained and passed deterministic checks;
save-all byte equality was not newly exercised by these no-tool trials. Claude
also retained some English template headings in zh-TW drafts, and the hosts
differed in their task-status presentation for the fully covered fixture; neither
is evidence of new language/task-reader acceptance. No release readiness claim
is made from these targeted results.

## Filesystem lookup and append follow-up (2026-10-22)

The first review found that the saved baseline omitted older lessons and that
the lesson sub-flow had no append branch. Both hosts now load a shared bounded
lookup: up to three candidate-derived literal searches in journal/lessons across
dates, up to twenty fully read matching files, explicit incomplete/ambiguous
coverage, and new/append/reference-existing/unresolved dispositions. Append uses
the verified existing target instead of today's new-entry filename.

Native-host acceptance used actual synthetic files behind four restricted tools
(inspect, literal lesson search, complete read and approved append). The prompt
contained the source rules and current event, not the old lesson's filename or
contents. Both hosts had to discover an August lesson during an October session;
an unrelated matching file was present to require content/scope comparison.

| Case | Codex | Claude |
|---|---|---|
| Same old event, no new evidence | Searched and read old lesson; reference-existing; no write attempt or file change | Same |
| New independent counterexample | Found old target; displayed append; no preapproval write; after save this, re-read, append and read back | Same |

Byte checks independently compare every fixture file: only the old lesson changes
in append cases, its UTF-8/CRLF original without a final newline remains an exact
prefix, and the appended suffix equals the displayed approved block, including
the leading blank-line separator. No replacement frontmatter or new lesson file
is created. These are real synthetic filesystem writes, not just draft claims.

Claude's first append run incorrectly promised CRLF for the new block but wrote
the approved LF block, then disclosed the discrepancy. The contract was clarified:
append is supported only for verified UTF-8 targets; the displayed suffix is
UTF-8/LF, the original is never normalized, and mixed endings must be disclosed
before approval. A focused Claude rerun disclosed this correctly and preserved
the original prefix plus the exact 990-byte approved suffix. The earlier P3
reporting deviation remains part of the evidence, not a clean initial pass.

A final-contract Codex append rerun also disclosed the original CRLF and new LF
endings before approval, discovered the old target through file tools, and
preserved its exact original bytes plus the approved suffix. Both hosts therefore
have a focused successful rerun of the mixed-ending disclosure requirement.

An independent reviewer who did not author the change checked the source and
native transcripts, and independently compared actual file bytes and hashes.
The reviewer ran the same final regression test on an isolated pre-fix snapshot
(exit 1 for the missing lookup contract) and the repaired source (exit 0), without
reverting the worktree. All seven workflow-route tests passed. The full local
gate passed with its existing single skip; focused checks were repeated after
the encoding/newline clarifications.

Limits: this establishes explicit-source native-host discovery and approved
save-this append in synthetic UTF-8 fixtures. Installed-plugin discovery,
unsupported-encoding/BOM behavior, source-change conflict races, ambiguous or
truncated lookup outcomes, and save-all sequences were not exercised by these
new behavioral trials. Their written safeguards are structurally checked only.
No real vault, installed plugin, release version or ingestion configuration was
changed. The generic no-tool trial limitations above still apply to that earlier
set of trials, not to these filesystem tests.
