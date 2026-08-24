# Validation Contract

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

- `tests/validate_commands.py`: command structure and write safeguards.
- `tests/smoke_hirameki_workflows.py`: workflow routing and expected outcomes.
- `tests/test_open_handoff.mjs`: handoff action behavior.
- `tests/validate_codex_skill.py`: Codex adapter contract.
- `tests/validate_release_contract.py`: release and package test-chain parity.

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
