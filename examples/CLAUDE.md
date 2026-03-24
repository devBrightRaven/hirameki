# Example Vault Configuration

Run `/hirameki:__init` to generate `~/.claude/vault-local.md` automatically. The file will look like this:

## Vault Structure

```
vault: /path/to/your/vault
language: 繁體中文
daily: _daily/
inbox: _inbox/
research: _analysis/
journal: _logs/
templates: _templates/
```

## How to customize

Change the paths to match your vault's directory structure. For example:

```
vault: D:/Obsidian/my-vault
language: English
daily: journal/daily/
inbox: inbox/
research: analysis/
journal: work-logs/
templates: templates/
```

All Hirameki commands read these paths from `~/.claude/vault-local.md` at runtime (falls back to `~/.claude/CLAUDE.md` for backwards compatibility).
If a path is not configured, the command will ask you where to read/write.

## Cross-machine sync

If you sync `~/.claude/` via git, add `vault-local.md` to `.gitignore` — vault paths are platform-specific. Each machine runs `/hirameki:__init` once to generate its local config.
