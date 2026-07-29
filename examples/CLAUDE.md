# Example Vault Configuration

Run `/hirameki:__init` to generate both files automatically. The configuration is split by audience.

## Per-machine — `~/.claude/vault-local.md`

Where the vault is, and how you want Hirameki to talk to you. Platform-specific, Claude-private.

```
## Vault Structure

vault: /path/to/your/vault
language: 繁體中文
```

## Vault layout — `<vault>/AGENTS.md`

What is inside the vault. Agent-neutral, so Codex, Gemini, and any future agent resolve the same paths. It travels with the vault, so a second machine inherits it without reconfiguring.

````
## Vault Structure

```yaml
daily: _daily/
inbox: _inbox/
research: _analysis/
journal: _logs/
handoff: _handoff/
templates: _templates/
```
````

## How to customize

Change the folder paths in `AGENTS.md` to match your vault:

```yaml
daily: journal/daily/
inbox: inbox/
research: analysis/
journal: work-logs/
handoff: handoff/
templates: templates/
```

Commands resolve the vault root from `vault-local.md`, then read folder paths from `<vault>/AGENTS.md`, falling back to `vault-local.md` and `~/.claude/CLAUDE.md` for setups made before 1.4.3. A folder key that exists nowhere stops the command rather than defaulting to a guess.

## Cross-machine sync

If you sync `~/.claude/` via git, add `vault-local.md` to `.gitignore` — vault paths are platform-specific. Each machine runs `/hirameki:__init` once to generate its local config. `AGENTS.md` needs no per-machine step; it is already in the vault.
