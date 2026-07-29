#!/usr/bin/env node
// Session-end verification hook
// Runs when Claude Code session ends

import { execFileSync } from 'child_process';
import { readdirSync, statSync, existsSync } from 'fs';
import { join } from 'path';
import { getVaultPath, getVaultFolder } from './lib/resolve-vault.mjs';

let uncommitted = '';
try {
  uncommitted = execFileSync('git', ['status', '--porcelain'], {
    encoding: 'utf8',
    cwd: process.cwd(),
    // git writes "fatal: not a git repository" to its own stderr, which is
    // inherited by default — the catch below never sees it and the user gets
    // the noise on every Stop outside a repo. Discard it; keep stdout.
    stdio: ['ignore', 'pipe', 'ignore']
  }).trim();
  if (uncommitted) {
    process.stderr.write(`[session-end] Uncommitted changes detected:\n${uncommitted}\n`);
  }
} catch {
  // Not a git repo or git not available — skip silently
}

// Unrecorded-work nudge: work happened but no daily note was touched.
// mtime rather than today's filename on purpose — work that crosses midnight
// still wraps into the working day's file, so a date match false-fires.
const RECENT_MS = 12 * 60 * 60 * 1000;

function dailyTouchedRecently(now = Date.now()) {
  const vault = getVaultPath();
  if (!vault) return true; // no vault configured — never nag
  const daily = getVaultFolder(vault, 'daily');
  if (!daily) return true;
  const dir = join(vault, daily);
  if (!existsSync(dir)) return true;
  return readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .some(f => {
      try { return now - statSync(join(dir, f)).mtimeMs < RECENT_MS; } catch { return false; }
    });
}

try {
  if (uncommitted && !dailyTouchedRecently()) {
    process.stderr.write(
      '[hirameki] Work changed files but no daily note was touched in 12h. /hirameki:wrap\n'
    );
  }
} catch {
  // Vault unreadable — the git warning above already ran, stay quiet
}
