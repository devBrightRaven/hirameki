# Hirameki 1.4.0 — release + atomic hook-dedupe cutover runbook

This release folds two SessionStart/Stop hook behaviors that were being run twice
(once by the installed plugin, once by hand-registered `~/.claude/scripts/` copies)
into the plugin itself, then removes the now-redundant hand registrations so each
hook fires exactly once.

**Atomicity is the whole point.** Do not remove the `~/.claude/scripts/`
registrations before 1.4.0 is installed — the pre-1.4.0 plugin copies are
pulse-only and use a hardcoded vault path, so removing the hand copies first would
lose the sprint / `philosophy_mode` surfacing and the portable vault resolution.
Ship the plugin, verify it, *then* dedupe.

---

## 0. Current duplicate state is SAFE — there is no urgency

Until this cutover runs, three hooks are registered twice. That is harmless:

- **`session-end-check.mjs`** — the two copies are byte-identical; it only runs
  `git status --porcelain` and prints. Running it twice does nothing but print twice.
- **`extract-actions.mjs`** — appends to `~/.claude/homunculus/actions.jsonl` but
  dedups by `date:time:action` key, so a double run never double-appends.
- **`session-start-catchup.mjs`** — the plugin copy prints Vault Pulse, the hand
  copy prints Sprint/philosophy; running both is exactly the union 1.4.0 produces
  from one script. No state is written.

So the cutover can wait for explicit authorization. Do not rush it.

---

## 1. Preconditions (all must be explicitly authorized before starting)

This runbook performs irreversible / external actions. Do **not** begin until the
user has explicitly authorized each of:

- [ ] **Commit** the 1.4.0 working-tree changes in the canonical repo.
- [ ] **Tag** `v1.4.0`.
- [ ] **Push** commit + tag to `github.com/devBrightRaven/hirameki` (HTTPS origin).
- [ ] **Marketplace update + reinstall** of `hirameki@hirameki`.
- [ ] **Edit `~/.claude/settings.json`** to remove the three duplicate registrations.

Environment facts to confirm first:

- Canonical repo is **`C:/Code/hirameki`** (HTTPS origin, `.claude-plugin/` present).
  The clone at `C:/Code/plugins/hirameki` is **stale (1.2.0, SSH remote) — never
  release from it.**
- The marketplace is self-hosted: the repo *is* the marketplace
  (`.claude-plugin/marketplace.json`, `source: "./"`, no version field). It is
  registered in `~/.claude/settings.json` as marketplace `hirameki` →
  `{source: github, repo: "devBrightRaven/hirameki"}` with `autoUpdate: true`.
- Record `sha256(~/.claude/settings.json)` **now**, before any edit — it is the
  rollback anchor for step 6.

---

## 2. What 1.4.0 contains (already applied to the working tree, uncommitted)

- `hooks/scripts/session-start-catchup.mjs` — union of Vault Pulse + inbox scan
  **and** sprint / `philosophy_mode` surfacing; each part independently guarded.
- `hooks/scripts/extract-actions.mjs` — hardcoded `D:/Obsidian/br-os-vault`
  replaced by `getVaultPath()`; exits cleanly when no vault is configured.
- `hooks/scripts/lib/resolve-vault.mjs` — **newly bundled** portable resolver
  (the plugin shipped no `hooks/scripts/lib/` before; without it the relative
  import in `extract-actions.mjs` ENOENTs at runtime).
- `hooks/scripts/session-end-check.mjs` — unchanged (already byte-identical).
- Version bumped 1.3.0 → 1.4.0 in `.claude-plugin/plugin.json` and `package.json`;
  CHANGELOG entry added.

---

## 3. Release the plugin (canonical repo only)

Run from `C:/Code/hirameki`:

```
git add .claude-plugin/plugin.json package.json CHANGELOG.md \
        hooks/scripts/session-start-catchup.mjs \
        hooks/scripts/extract-actions.mjs \
        hooks/scripts/lib/resolve-vault.mjs \
        docs/release-1.4.0-cutover.md
git commit -m "feat: hirameki 1.4.0 — merge SessionStart hooks, portable vault resolution"
git tag v1.4.0
git push origin HEAD
git push origin v1.4.0
```

> Note: the working tree may also carry unrelated Codex-adapter changes under
> `codex/` and `tests/`. Stage only the 1.4.0 files listed above unless those are
> separately authorized.

---

## 4. Update the marketplace + reinstall

```
claude plugin marketplace update hirameki
claude plugin update hirameki@hirameki      # or: reinstall hirameki@hirameki
```

Verify the cache picked up 1.4.0:

- `~/.claude/plugins/cache/hirameki/hirameki/1.4.0/` exists.
- `installed_plugins.json` shows `hirameki@hirameki` → version **1.4.0** and a
  `gitCommitSha` equal to the pushed HEAD.

Restart the session so the new plugin hooks load, then smoke-test:

- SessionStart prints a `[Vault Pulse] … | Inbox(…)` segment **and** a
  `Sprint: … | Run /hirameki:next …` (or philosophy) segment from the single
  plugin hook.
- Trigger a Stop and confirm `extract-actions.mjs` resolves the vault via
  `getVaultPath()` (no `D:/Obsidian` ENOENT in stderr).

**Do not proceed to step 5 until the plugin hooks are confirmed working.**

---

## 5. Atomic settings.json dedupe (remove exactly three hand registrations)

Identify the entries to remove by **event + script basename content-match, not by
line number** (line numbers drift). In `~/.claude/settings.json`, remove exactly:

1. The **SessionStart** hook whose `command` runs `~/.claude/scripts/session-start-catchup.mjs`.
2. The **Stop** hook whose `command` runs `~/.claude/scripts/session-end-check.mjs`.
3. The **Stop** hook whose `command` runs `~/.claude/scripts/extract-actions.mjs`.

**Keep every sibling hook in those same event arrays**, specifically:

- SessionStart siblings to KEEP: `session-tracker`, `offer-watch`.
- Stop siblings to KEEP: `auto-learn`, `sync-dotclaude`, `session-analytics`.

Remove only the matcher/hook object that fires the three named scripts; if a
matcher group contains a kept sibling alongside a removed script, delete just the
removed script's hook object, not the whole group. After editing, confirm the file
still parses as JSON.

Restart the session.

---

## 6. Post-cutover verification

- [ ] `~/.claude/settings.json` parses (valid JSON).
- [ ] Effective registration count is **1 each** for SessionStart→catchup,
      Stop→session-end-check, Stop→extract-actions (only the plugin fires them now).
- [ ] All KEEP siblings still registered (`session-tracker`, `offer-watch`,
      `auto-learn`, `sync-dotclaude`, `session-analytics`).
- [ ] 20/20 hirameki command tests pass.
- [ ] Fresh-session smoke: SessionStart shows the union message once; Stop extracts
      actions once with vault resolved.

---

## 7. Rollback

If anything in step 4–6 misbehaves:

- **Settings**: restore `~/.claude/settings.json` from the pre-cutover backup taken
  in step 1 (a dated `hirameki-hook-dedupe-*` backup already exists under
  `~/.claude/backups/`). Confirm the restored file's SHA-256 matches the value
  recorded before editing. Restarting reinstates the (safe) duplicate state.
- **Plugin**: reinstall 1.3.0 from the git tag —
  `claude plugin update hirameki@hirameki` after
  `git -C C:/Code/hirameki checkout v1.3.0` (or point the marketplace at the
  1.3.0 tag), then `claude plugin marketplace update hirameki`. Duplicate-but-safe
  state resumes; no data is lost because the removed hand registrations only ever
  duplicated idempotent work.
