# Validation Contract

Restore operation delivery: the public `--restore-contract`/`--validate-restore`
interfaces use canonical reader validators; `tests/test_task_view_cli.py` checks
schema/digest/error consistency. `tests/test_codex_task_payload.py` exercises the
actual relocated package using only its delivered procedure and public CLI.

Read-only task-ID lookup: `tests/test_task_view_cli.py` covers archived tasks,
unknown IDs, changed sources, full/global validation and explicit UTF-8 size
limits; `tests/test_codex_task_payload.py` checks the actual relocated tarball's
root and Codex readers. Existing behavioral PASS is separate from these tests.

Hirameki is a released Tier 1 asset. A change is releasable only when the
command contract, Codex adapter, workflow smoke tests, local gate, and CI pass.

## Contract

- Every command keeps valid frontmatter, required workflow structure, language
  behavior, and confirm-before-write safeguards.
- Claude commands and the Codex skill adapter expose the same supported
  Hirameki workflow semantics within their host-specific mechanisms.
- Open-handoff behavior preserves the explicit save-action contract.
- `package.json` `scripts.test` mirrors `.release.json` `test` followed by
  `verify`; changing either side requires updating both in the same commit.

## Mapped tests

- `tests/fixtures/shared-workflow.json`: eight synthetic native-host acceptance
  cases for the shared improvement goal. These are test inputs and oracle criteria,
  not executed model evidence. The operator materializes `given` facts in an
  isolated fixture root; the agent receives the prompt and accessible evidence,
  never the `must`/`must_not` oracle. Approval in SW02/SW05 must occur after an
  actual frozen draft is displayed. Simulated GitHub responses in SW07 do not
  authorize or test live network mutation. Record per host the source/fixture
  hashes, actual tool loading, transcript locator, filesystem diff and outcome;
  missing approval, unavailable tools or unexercised branches remain BLOCKED or
  NOT-EXERCISED. Model runs and live deployment require their own authorization.
  SW03's cross-origin branch uses two sequential native contexts: an authorized
  origin writer followed by a read-only consolidation owner. Simulated machine
  labels on one filesystem test role/identity semantics, never actual sync safety.

  The same manifest's `adaptive_cases` adds AH01–AH12 for task H4. Initial
  `NOT-RUN` is fixture status, not a test result. Record every field listed in
  `evidence_required` per run; unknown model identity, usage or tool evidence stays
  unknown. Use PASS / FAIL / BLOCKED / NOT-EXERCISED / NOT-RUN and preserve earlier
  failures when a narrower follow-up passes. Fixture shape checks do not prove
  adaptive behavior.
  User-approved AH09 option A separates success-only assessment (no forced
  candidate) from `variants.actual_proposal` with a concrete synthetic gap.
  Materialize only the chosen branch's prompt/facts/evidence for each subject;
  never pass `variants`, `must` or `must_not` as task facts. Preserve earlier
  original-oracle failures under their original fixture digest.

  Materialize only synthetic `given` files in a disposable root, freeze hashes,
  and explicitly allowlist the necessary readset (including any applicable host
  policy prerequisites). Supply only prompt, task facts and available capability
  metadata to the subject; keep `must`, `must_not`, expected answers and prior
  verdicts outside its readset. Record actual tool/file access separately from
  agent self-report. Verify filesystem bytes and receipts independently wherever
  writes occur. Source-injected contracts test supplied-contract use, not installed
  discovery or fresh-runtime loading. AH10 requires separate native-runtime runs;
  an unavailable runtime remains NOT-RUN or BLOCKED with its reason.

  For A/B/C comparisons, freeze the same task inputs, tool permissions, model and
  effort where confirmable: A existing harness, B consolidated contracts without
  adaptive selection, C consolidated contracts with adaptive selection. Record
  differences in contract payload, tool availability, prompt and execution order;
  different prompts or uncontrolled environments cannot establish causal benefit.
  Record quality, calls, elapsed time, retries, intervention and side effects;
  unavailable token/billing/quota data stays unknown, never an estimated saving.
  Existing authorization and budget must cover each run before execution; adding
  fixtures does not grant paid experiments, live writes or deployment authority.

- `tests/test_exact_append.py`: private preparation/show without note writes,
  hash-bound apply, target/plan/content-hash receipts verified against saved bytes,
  exact BOM/CRLF/LF/no-final-newline preservation, safe replay,
  target/plan conflict refusal, local locking, linked-target rejection, partial
  write and readback failure reporting. Actual model approval and installed helper
  invocation remain separate native-host acceptance, not inferred from unit tests.
  New candidate mode additionally checks frozen full-note creation, collision
  before/after prepare, two actual competing processes (one winner), readback
  uncertainty, partial-write/fsync failure, linked target/parent and post-prepare
  link substitution, scope/plan rejection and refusal to infer replay from equal bytes.
  This is local filesystem evidence, not remote sync or event deduplication.

- `tests/test_workflow_routes.py`: five primary entries, permanent shortcuts,
  legacy redirects and argument preservation; canonical/adapter capability parity.
  This is deterministic contract validation, not fresh-dialogue acceptance.
  Also checks session-trace delivery, all three entrypoints, create/append clue
  sections, removal of premature skip rules and the unchanged batch-write gate.
  Behavioral acceptance must separately exercise completed-work pickup, one-event
  lessons, immature clues, verified full coverage and genuinely empty sessions.
  Lesson lookup/append checks require cross-date lesson discovery, explicit
  new/append/reference/unresolved branches, conflict refusal and byte preservation.
  Actual model/file acceptance must find a lesson not preloaded into the prompt,
  make no write before approval, and append only the displayed evidence block.
- Consolidation capabilities and routing metadata are delivered in `references/`
  and the Codex skill references. Actual relocated-package tests check delivery;
  installed host discovery and routing remain separate deployment checks.
  The relocated tarball checks exact SKILL/interface metadata bytes. The existing
  shared-workflow fixture also has HR01–HR06 natural-request inputs with three
  note-based outcomes and three direct/writing negative controls. Model pilots
  must keep these oracles outside the subject readset; catalog-only comparisons
  do not establish fresh-host discovery, usage savings or adoption benefit.
  Issue #3 extends those same cases with source-only/resume/inventory scopes,
  topic-based retrieval, an owning project task authority, retired/conflicting
  material and unrelated distractors. Keep variant oracles outside model inputs;
  execute the existing verifier only in the authorized resume branch. Source-copy
  parity and fixture integrity are deterministic checks; actual retrieval,
  continuation and artifact fidelity require separately retained model evidence.

- `tests/test_tidy_dry_run.py`: concrete synthetic A1 structural acceptance,
  A3 stale source despite preserved mtime, E1 conflict-copy paths, E2 gate
  invalidation, and E3 public CLI revision rejection. These are program evidence;
  assessor declarations and passing tests do not establish model semantics.

- `tests/test_vault_route.py`: optional agent-neutral multi-vault preflight,
  destination isolation and refusal to write under ambiguous context. Run it
  separately with Python3.10+ before deploying this optional helper. Personal
  adapter discovery and model context classification remain runtime checks.

- `tests/validate_commands.py`: command structure and write safeguards.
- `tests/smoke_hirameki_workflows.py`: workflow routing and expected outcomes.
- `tests/test_open_handoff.mjs`: handoff action behavior.
- `tests/validate_codex_skill.py`: Codex adapter contract.
  Includes canonical/adapter visible decision-reminder parity and its no-write boundary;
  static parity does not prove ordinary-work automatic triggering.
- `tests/validate_release_contract.py`: release and package test-chain parity.
- `tests/test_codex_task_payload.py`: acceptance payload and actual npm tarball
  delivery; bundled task readers and gate run from relocated package roots
  without source-checkout imports. Packing does not establish deployment.
  Requires the shared session-trace capability in both relocated host payloads.
  Both roots execute exclusive candidate creation, verify readback receipt hashes,
  and refuse a second create without changing either new or existing note bytes.

## Gates

- Local: `npm test -- --run` must pass before commit. The extra `--run` is
  accepted for compatibility with the Claude Code pre-commit hook. Codex must
  run the same command explicitly because that host does not execute Claude's
  hook.
- CI: `.github/workflows/validate.yml` validates release-chain parity and then
  runs `npm test -- --run` on every relevant push and pull request.
- Release: both local and CI gates must pass before tagging or deploying a new
  runtime copy.

## Update rule

Any behavior change must update its mapped test in the same change. When
`.release.json` changes its test or verify command, update
`package.json` `scripts.test` at the same time.
