#!/usr/bin/env node
// Session-end verification hook
// Runs when Claude Code session ends

import { execFileSync } from 'child_process';

try {
  const status = execFileSync('git', ['status', '--porcelain'], {
    encoding: 'utf8',
    cwd: process.cwd()
  }).trim();
  if (status) {
    process.stderr.write(`[session-end] Uncommitted changes detected:\n${status}\n`);
  }
} catch {
  // Not a git repo or git not available — skip silently
}
