# Example Vault Configuration

Add this section to your project's `CLAUDE.md` to configure BRW commands.

## Vault Structure

```
daily-notes: _daily/
daily-template: _templates/daily.md
analysis: _claude_code_analysis/
writing: $ Writing/
projects: $ Project/
feedback: _claude_code_feedback/
inbox: _inbox/
language: 繁體中文
```

## How to customize

Change the paths to match your vault's directory structure. For example:

```
daily-notes: journal/daily/
analysis: .analysis/
writing: writing/
projects: projects/
feedback: work-logs/
inbox: inbox/
language: English
```

All BRW commands read these paths from your CLAUDE.md at runtime.
If a path is not configured, the command will ask you where to read/write.
