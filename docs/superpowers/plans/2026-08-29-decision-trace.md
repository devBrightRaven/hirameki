# Decision Trace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Hirameki's split `decide` and `decision` surfaces with one `decision-trace` workflow that supports decision formation and optional lifecycle-managed storage.

**Architecture:** Claude exposes one auto-triggerable `decision-trace` skill plus one thin same-name command. Codex keeps its single Hirameki umbrella skill and routes `decision-trace` to one host-adapted reference. Contract tests prohibit discoverable legacy `decide` or `decision` surfaces and preserve the existing save and lifecycle safeguards.

**Tech Stack:** Markdown plugin commands and skills, Python 3.12 contract tests, Node 22 handoff test, npm validation wrapper.

**Spec:** `docs/superpowers/specs/2026-08-29-decision-trace-design.md`

## Global Constraints

- The only command and canonical skill is `decision-trace`.
- Do not retain `decision` or `decide` aliases, redirects, deprecated stubs, or discoverable surfaces.
- Implicit decision-language triggering belongs to `decision-trace`; explicit invocation accepts only `decision-trace`, `/decision-trace`, and `hirameki:decision-trace`.
- The agent must not choose for the user or infer that an unresolved candidate is decided.
- No vault write occurs before the user selects `save this` from the complete draft and affected-path review.
- Preserve `active`, `superseded`, and `closed` decision-node lifecycle semantics.
- Claude and Codex remain independently valid in their host-native surfaces.
- Do not bump a version, commit, push, tag, release, or deploy until the user separately authorizes that action.

---

### Task 1: Lock the unified discovery and behavior contract

**Files:**
- Modify: `tests/validate_commands.py`
- Modify: `tests/validate_codex_skill.py`
- Modify: `tests/smoke_hirameki_workflows.py`

**Interfaces:**
- Consumes: current command inventory, Codex reference inventory, and workflow smoke fixture.
- Produces: failing assertions for the exact `decision-trace` surface and unified workflow phrases.

- [ ] **Step 1: Rename the command contract key and write-command entry**

In `tests/validate_commands.py`, replace `decision` with `decision-trace` in `WRITE_COMMANDS` and `REQUIRED_CONTENT`. Require these load-bearing phrases:

```python
"decision-trace": [
    "Establish the decision state",
    "Build the trace",
    "Only move to `decided`",
    "Promotion gate",
    "active", "superseded", "closed",
    "Action? (save this / skip / edit)",
],
```

- [ ] **Step 2: Replace the Codex decision-history test with a unified trace test**

In `tests/validate_codex_skill.py`, rename `decision.md` set entries to `decision-trace.md`, read that filename from both command/reference roots, and assert the formation and lifecycle contract:

```python
for phrase in (
    "Establish the decision state",
    "unresolved", "forming", "decided", "reviewing",
    "Build the trace",
    "viable options",
    "assumptions and unknowns",
    "reversal cost",
    "must not choose for the user",
    "Only move to `decided`",
    "Promotion gate",
    "status: active",
    "superseded", "closed",
    "Action? (save this / skip / edit)",
    "does not authorize a write",
):
    assert phrase in trace
```

Add a discovery assertion scoped to runtime surfaces rather than historical prose:

```python
assert not (COMMANDS / "decision.md").exists()
assert not (ROOT / "skills" / "decide").exists()
assert not (SKILL / "references" / "decision.md").exists()
assert (COMMANDS / "decision-trace.md").is_file()
assert (ROOT / "skills" / "decision-trace" / "SKILL.md").is_file()
assert (SKILL / "references" / "decision-trace.md").is_file()
```

- [ ] **Step 3: Update the smoke workflow inventory**

Replace the `decision` workflow name with `decision-trace` wherever the smoke fixture enumerates conditional writers or expected commands. Do not change ordinary prose such as `Decisions made`.

- [ ] **Step 4: Run the contract tests and verify RED**

Run:

```powershell
python -X utf8 tests\validate_commands.py
python -X utf8 tests\validate_codex_skill.py
python -X utf8 tests\smoke_hirameki_workflows.py
```

Expected: failures name missing `commands/decision-trace.md`, missing `skills/decision-trace/SKILL.md`, missing Codex reference/router, or surviving legacy surfaces.

- [ ] **Step 5: Review the scoped diff**

Run `git diff -- tests/validate_commands.py tests/validate_codex_skill.py tests/smoke_hirameki_workflows.py`. Do not commit yet.

---

### Task 2: Implement the single Claude and Codex workflow

**Files:**
- Delete: `commands/decision.md`
- Create: `commands/decision-trace.md`
- Delete: `skills/decide/SKILL.md`
- Create: `skills/decision-trace/SKILL.md`
- Delete: `codex/skills/hirameki/references/decision.md`
- Create: `codex/skills/hirameki/references/decision-trace.md`
- Modify: `codex/skills/hirameki/SKILL.md`
- Modify: `commands/arc.md`
- Modify: `commands/challenge.md`
- Modify: `codex/skills/hirameki/references/arc.md`
- Modify: `codex/skills/hirameki/references/challenge.md`

**Interfaces:**
- Consumes: the approved state machine and existing lifecycle-node template.
- Produces: one Claude skill identity, one explicit Claude command, and one Codex umbrella route with equivalent behavior.

- [ ] **Step 1: Create the canonical Claude skill**

Create `skills/decision-trace/SKILL.md` with frontmatter name `decision-trace`. Its description must include the existing Chinese, English, and Japanese decision-language triggers while excluding passing preferences and mechanical actions.

The body must implement these sections in order:

```markdown
## Establish the decision state
unresolved / forming / decided / reviewing

## Build the trace
decision question / viable options / evidence / assumptions and unknowns /
constraints / consequences / reversal cost / one key unresolved question

## Capture an explicit decision
Only move to `decided` after the user states or confirms the choice.
The agent must not choose for the user.

## Promotion gate
retain the existing future-constraint and reversal-cost criteria

## Resolve existing state
retain active / superseded / closed behavior

## Confirmation action model
Action? (save this / skip / edit)

## Decision node
retain the existing frontmatter and sections

## Write safety
show evidence, affected paths, complete content, and status changes before save
```

Use Claude's existing vault-resolution contract at the top. Do not invent rationale or silently promote a candidate.

- [ ] **Step 2: Create the thin Claude command**

Replace `commands/decision.md` with `commands/decision-trace.md`. The command must pass `$ARGUMENTS` to the `decision-trace` skill and state that the skill owns the full workflow. Include the required setup, language, affected-path, complete-draft, and `save this` safeguards so command validation remains meaningful.

- [ ] **Step 3: Create the Codex reference and route**

Replace the Codex reference with `references/decision-trace.md`. Mirror the canonical workflow but resolve vault configuration through the umbrella adapter and use `source: codex` in new nodes. Update the umbrella description, command table, and command count from `/decision` to `/decision-trace`.

- [ ] **Step 4: Remove the old skill and stale cross-references**

Delete `skills/decide/SKILL.md`. Replace routing mentions in `arc` and `challenge` with `decision-trace` in both Claude and Codex files. Do not alter normal English verbs such as "the user decides" or document headings such as `Decisions made`.

- [ ] **Step 5: Run the focused tests and verify GREEN**

Run:

```powershell
python -X utf8 tests\validate_commands.py
python -X utf8 tests\validate_codex_skill.py
python -X utf8 tests\smoke_hirameki_workflows.py
```

Expected: all three exit 0.

- [ ] **Step 6: Verify runtime-surface uniqueness**

Run:

```powershell
Get-ChildItem commands -File | Where-Object Name -Match '^decision'
Get-ChildItem skills -Directory | Where-Object Name -Match '^(decision|decide)'
Get-ChildItem codex\skills\hirameki\references -File | Where-Object Name -Match '^decision'
```

Expected: only `decision-trace.md`, `decision-trace`, and `decision-trace.md` respectively.

- [ ] **Step 7: Review the scoped diff**

Inspect `git diff -- commands skills/decision-trace skills/decide codex/skills/hirameki`. Do not commit yet.

---

### Task 3: Update public documentation and bundled catalogs

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `_hirameki_cmds/hirameki-cmds-full.md`
- Modify: `_hirameki_cmds/hirameki-cmds-full-zh-TW.md`
- Modify: `_hirameki_cmds/hirameki-cmds-full-ja.md`
- Modify: `_hirameki_cmds/hirameki-cmds-short.md`
- Modify: `_hirameki_cmds/hirameki-cmds-short-zh-TW.md`
- Modify: `_hirameki_cmds/hirameki-cmds-short-ja.md`
- Synchronize: `codex/skills/hirameki/assets/_hirameki_cmds/*`

**Interfaces:**
- Consumes: the implemented `decision-trace` behavior.
- Produces: discoverable English, Traditional Chinese, and Japanese documentation with byte-identical Codex bundled assets.

- [ ] **Step 1: Rewrite the README command and skill sections**

Replace the separate `decision` command and `decide` skill sections in all three languages with one `decision-trace` section. Explain: automatic decision-language triggering, the four states, trace fields, no agent choice, and optional `save this` lifecycle storage.

- [ ] **Step 2: Rewrite full and short command catalogs**

Rename only the workflow entry to `decision-trace`. Preserve ordinary words about decisions elsewhere. The entry must describe both the read-only formation phase and conditional write phase.

- [ ] **Step 3: Synchronize bundled catalog assets**

Copy the six canonical `_hirameki_cmds` files into `codex/skills/hirameki/assets/_hirameki_cmds/` using the repository's existing exact-copy convention.

- [ ] **Step 4: Add an unreleased changelog entry**

Record the breaking surface consolidation, removal of `decision`/`decide`, automatic triggering, and preservation of lifecycle nodes. Do not bump `1.6.2` or create a release heading without separate authorization.

- [ ] **Step 5: Run documentation and adapter validators**

Run:

```powershell
python -X utf8 tests\validate_commands.py
python -X utf8 tests\validate_codex_skill.py
```

Expected: both exit 0, including byte-identical asset checks.

---

### Task 4: Complete repository validation and review

**Files:**
- Modify if required by the changed contract: `VALIDATION.md`
- Verify only: `.release.json`, `package.json`, `.github/workflows/validate.yml`

**Interfaces:**
- Consumes: all prior tasks.
- Produces: a locally validated, reviewable worktree; no release side effects.

- [ ] **Step 1: Run the full Tier 1 gate**

Run:

```powershell
npm test -- --run
```

Expected: command validation, smoke workflows, handoff test, Codex adapter validation, and release-chain validation all pass.

- [ ] **Step 2: Check formatting and forbidden runtime surfaces**

Run:

```powershell
git diff --check
Get-ChildItem commands -File | Where-Object Name -Match '^decision'
Get-ChildItem skills -Directory | Where-Object Name -Match '^(decision|decide)'
Get-ChildItem codex\skills\hirameki\references -File | Where-Object Name -Match '^decision'
```

Expected: no diff errors and only the three `decision-trace` surfaces.

- [ ] **Step 3: Inspect the complete diff and worktree ownership**

Run `git status --short` and `git diff --stat`, then inspect every changed path. Confirm no version, credential, machine path, installed cache, or unrelated file entered the change.

- [ ] **Step 4: Obtain cross-runtime review**

Ask one reviewer to verify behavior/spec compliance and a second reviewer to verify command/reference/runtime ownership. Address findings with focused tests, then rerun `npm test -- --run`.

- [ ] **Step 5: Stop before release actions**

Report the validated diff, remaining limitations, and proposed semantic version. Wait for explicit authorization before commit, push, version bump, tag, GitHub release, or installed-runtime deployment.
