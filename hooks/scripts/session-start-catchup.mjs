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
  systemMessage: [
    'SessionStart:catchup hook: Session started.',
    'Run /hirameki:catchup to check pending items and orient the user.',
    'Do this silently — just invoke the skill and present results.',
    'If the user has already given a task in their first message, skip catchup and address their request directly.'
  ].join(' ')
});

process.stdout.write(msg);
