#!/usr/bin/env node
// SessionStart hook: instruct Claude to run catchup on session start.
// Outputs a systemMessage that Claude will see and act on.

import { readFileSync } from 'fs';

// Read stdin (hook input JSON)
let input = '';
try {
  input = readFileSync(0, 'utf8');
} catch {
  // stdin may be empty
}

const msg = JSON.stringify({
  systemMessage: '>>> Hey, have you checked if there are pending items? Run /hirameki:catchup to find out — unless you already have a task to work on. <<<'
});

process.stdout.write(msg);
