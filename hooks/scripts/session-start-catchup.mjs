#!/usr/bin/env node
// SessionStart hook (hirameki 1.4.0): union of two behaviors, each guarded so
// failure of one never suppresses the other.
//   (1) Vault Pulse: vault snapshot (per-folder note counts, active/dormant) + inbox scan
//   (2) Sprint/philosophy surfacing from vault-local.md (## Vault Structure section)
// Emits a single systemMessage joining whatever each part produced.

import { readFileSync, readdirSync, statSync, existsSync } from 'fs';
import { join, resolve } from 'path';
import { homedir } from 'os';

// --- Read vault config (vault/daily/inbox from ## Vault Structure) ---
function readVaultConfig() {
  const paths = [
    join(homedir(), '.claude', 'vault-local.md'),
    join(homedir(), '.claude', 'CLAUDE.md'),
  ];

  for (const p of paths) {
    try {
      const content = readFileSync(p, 'utf8');
      const match = content.match(/## Vault Structure[\s\S]*?(?=\n## |$)/);
      if (!match) continue;

      const section = match[0];
      const get = (key) => {
        const m = section.match(new RegExp(`^${key}:\\s*(.+)$`, 'm'));
        return m ? m[1].trim() : null;
      };

      const vault = get('vault');
      if (!vault) continue;

      return {
        vault: resolve(vault),
        daily: get('daily') || '_yorozuya/daily/',
        inbox: get('inbox') || '_inbox/',
        language: get('language') || 'English',
      };
    } catch { continue; }
  }
  return null;
}

// --- Read sprint + philosophy mode (vault-local.md ## Vault Structure) ---
function readSprintPhilosophy() {
  const configPath = join(homedir(), '.claude', 'vault-local.md');
  try {
    const content = readFileSync(configPath, 'utf8');
    const match = content.match(/## Vault Structure[\s\S]*?(?=\n## |$)/);
    if (!match) return null;

    const section = match[0];
    const get = (key) => {
      const m = section.match(new RegExp(`^${key}:[ \\t]*(.*)$`, 'm'));
      return m ? m[1].trim() : null;
    };

    return {
      currentSprint: get('current_sprint') || '',
      philosophyMode: get('philosophy_mode') || 'default',
    };
  } catch { return null; }
}

// --- Scan content folders ---
function scanContentFolders(vaultPath) {
  const exclude = new Set(['.obsidian', '.trash', '_hirameki_cmds', '_templates', 'node_modules']);
  const results = [];

  try {
    const entries = readdirSync(vaultPath, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      if (entry.name.startsWith('.') || exclude.has(entry.name)) continue;

      const folderPath = join(vaultPath, entry.name);
      try {
        const files = readdirSync(folderPath, { recursive: true })
          .filter(f => typeof f === 'string' && f.endsWith('.md'));
        const count = files.length;

        // Check recent activity (7 days)
        const now = Date.now();
        const sevenDays = 7 * 24 * 60 * 60 * 1000;
        let recentCount = 0;
        for (const f of files.slice(0, 50)) {
          try {
            const st = statSync(join(folderPath, f));
            if (now - st.mtimeMs < sevenDays) recentCount++;
          } catch { /* skip */ }
        }

        const status = recentCount > 0 ? 'active' : 'dormant';
        results.push({ name: entry.name, count, recentCount, status });
      } catch { /* skip unreadable */ }
    }
  } catch { /* vault unreadable */ }

  return results;
}

// --- Scan inbox ---
function scanInbox(vaultPath, inboxRel) {
  const inboxPath = join(vaultPath, inboxRel);
  if (!existsSync(inboxPath)) return [];

  try {
    return readdirSync(inboxPath)
      .filter(f => f.endsWith('.md'))
      .slice(0, 10)
      .map(f => {
        try {
          const st = statSync(join(inboxPath, f));
          const date = st.birthtime.toISOString().slice(0, 10);
          return { name: f.replace('.md', ''), date };
        } catch {
          return { name: f.replace('.md', ''), date: '?' };
        }
      });
  } catch { return []; }
}

// --- Build Vault Pulse message (guarded) ---
function buildPulseMessage() {
  const config = readVaultConfig();
  if (!config) return '';

  const folders = scanContentFolders(config.vault);
  const inbox = scanInbox(config.vault, config.inbox);

  const totalFiles = folders.reduce((sum, f) => sum + f.count, 0);
  const activeFolders = folders.filter(f => f.status === 'active');
  const dormantFolders = folders.filter(f => f.status === 'dormant');

  let msg = `[Vault Pulse] ${totalFiles} notes | ${activeFolders.length} active / ${dormantFolders.length} dormant folders`;

  if (activeFolders.length > 0) {
    msg += ` | Active: ${activeFolders.map(f => `${f.name}(${f.recentCount})`).join(', ')}`;
  }

  if (inbox.length > 0) {
    msg += ` | Inbox(${inbox.length}): ${inbox.map(i => i.name).join(', ')}`;
  } else {
    msg += ' | Inbox clear';
  }

  return msg;
}

// --- Build sprint/philosophy message (guarded) ---
function buildSprintMessage() {
  const config = readSprintPhilosophy();
  if (!config) return '';

  const parts = [];
  if (config.currentSprint) {
    parts.push(`Sprint: ${config.currentSprint} [mode: ${config.philosophyMode}]`);
  } else if (config.philosophyMode !== 'default') {
    parts.push(`Philosophy mode: ${config.philosophyMode}`);
  }
  parts.push('Run /hirameki:next to orient for this session.');

  return parts.join(' | ');
}

// --- Main: run both parts independently, union the results ---
let pulseMsg = '';
try { pulseMsg = buildPulseMessage(); } catch { pulseMsg = ''; }

let sprintMsg = '';
try { sprintMsg = buildSprintMessage(); } catch { sprintMsg = ''; }

const systemMessage = [pulseMsg, sprintMsg].filter(Boolean).join(' | ');
process.stdout.write(JSON.stringify({ systemMessage }));
