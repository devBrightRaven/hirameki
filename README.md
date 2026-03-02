# Glint

Obsidian vault knowledge management commands for [Claude Code](https://claude.com/claude-code).

Help you build a habit of using AI to review and excavate your accumulated thinking.

## Install

```bash
claude /plugin install glintstone
```

Then add your vault path to `~/.claude/CLAUDE.md`:

```markdown
## Vault
path: /path/to/your/obsidian/vault/
```

If you open Claude Code inside your vault directory, the path is auto-detected and you can skip this step.

## First run

Commands auto-detect your vault's folder structure. If a required folder doesn't exist, the command will ask where to create it and print the result. After the first run, your vault's `CLAUDE.md` will have a `## Vault Structure` section recording the folder mappings — you won't be asked again.

## Commands

### Daily Rhythm

| Command | What it does |
|---------|-------------|
| `/glint-status` | Vault overview — content topics, recent activity |
| `/glint-catchup [days]` | Progress catchup — recent progress, inbox, suggested focus |
| `/glint-wrap [description]` | Progress snapshot — appends to today's daily note |
| `/glint-weekreview` | Weekly review with gap analysis |

### Concept Archaeology

| Command | What it does |
|---------|-------------|
| `/glint-arc {concept}` | Track how a concept evolves across your vault |
| `/glint-bridge {A} and {B}` | Find hidden connections between two topics |
| `/glint-undercurrent [scope]` | Surface recurring themes that lack dedicated articles |
| `/glint-cluster [scope]` | Find groups of notes converging on unnamed themes |

### Thinking Tools

| Command | What it does |
|---------|-------------|
| `/glint-ghost {question} [save]` | Answer a question in your voice, based on your writing |
| `/glint-stress-test {topic} [save]` | Pressure-test your arguments on a topic |

### Maintenance

| Command | What it does |
|---------|-------------|
| `/glint-tidy [fix]` | Frontmatter properties audit — missing fields, inconsistent tags, cleanup |

### Action Output

| Command | What it does |
|---------|-------------|
| `/glint-harvest [save]` | Identify actionable ideas from existing content |
| `/glint-graduate` | Graduate half-formed ideas into standalone notes |
| `/glint-journal {topic}` | Work log with reasoning, connections, and follow-ups |

## How it works

1. **Vault detection**: Commands check for `.obsidian/` in the current directory, then fall back to `~/.claude/CLAUDE.md` for the vault path
2. **Folder detection**: Commands look for common folder names (e.g. `Daily/`, `_daily/`, `Journal/`). If not found, you'll be asked once and the mapping is saved
3. **Content scanning**: Commands scan all non-system folders in your vault as "content folders" — however you organize your notes, it works

Commands that write files always show a preview and the full target path before writing.

## License

MIT
