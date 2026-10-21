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
