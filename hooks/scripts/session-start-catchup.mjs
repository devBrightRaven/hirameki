#!/usr/bin/env node
// SessionStart hook (hirameki 1.4.3): say what is waiting on a decision and what
// is new, nothing else.
//
// The previous version opened every session with a vault census — total note
// count, active/dormant folder tallies, the full inbox listing. All of it was
// constant between sessions, so it read as wallpaper, and wallpaper trains you
// to skip the whole block including the one line that mattered. The census now
// lives in `/hirameki:pulse snapshot`, on demand.
//
// Each part is guarded so one failure never suppresses the others, and each
// stays silent unless it has something concrete to report. An empty message is
// a correct outcome.

import { readFileSync, readdirSync, statSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { getVaultPath, getVaultFolder } from './lib/resolve-vault.mjs';
import { newestOpenHandoff, firstClause } from './lib/open-handoff.mjs';

const NEW_INBOX_DAYS = 7;
const HANDOFF_SCAN_LIMIT = 40;

// --- Handoff: the actions the last session left behind ---
function buildHandoffMessage() {
  const vault = getVaultPath();
  if (!vault) return '';
  const rel = getVaultFolder(vault, 'handoff');
  if (!rel) return '';

  const dir = join(vault, rel);
  if (!existsSync(dir)) return '';

  const files = readdirSync(dir)
    .filter(f => f.endsWith('.md') && !f.startsWith('_'))
    .map(name => {
      try {
        return {
          name,
          mtimeMs: statSync(join(dir, name)).mtimeMs,
          get content() { return readFileSync(join(dir, name), 'utf8'); },
        };
      } catch { return null; }
    })
    .filter(Boolean)
    .sort((a, b) => b.mtimeMs - a.mtimeMs)
    .slice(0, HANDOFF_SCAN_LIMIT);

  const open = newestOpenHandoff(files);
  if (!open) return '';

  const shown = open.actions.slice(0, 2).map(a => firstClause(a));
  const more = open.actions.length > shown.length ? ` (+${open.actions.length - shown.length})` : '';
  return `[Handoff ${open.name.replace(/\.md$/, '')}] ${shown.join(' / ')}${more}`;
}

// --- Inbox: only what arrived recently ---
// Listing the whole inbox every session buries a new capture among items that
// have sat there for months. Recency is the filter; no state file to drift.
function buildInboxMessage(now = Date.now()) {
  const vault = getVaultPath();
  if (!vault) return '';
  const rel = getVaultFolder(vault, 'inbox');
  if (!rel) return '';

  const dir = join(vault, rel);
  if (!existsSync(dir)) return '';

  const cutoff = now - NEW_INBOX_DAYS * 24 * 60 * 60 * 1000;
  const fresh = readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .map(f => {
      try {
        const st = statSync(join(dir, f));
        return { name: f.replace(/\.md$/, ''), at: Math.max(st.birthtimeMs || 0, st.mtimeMs) };
      } catch { return null; }
    })
    .filter(Boolean)
    .filter(f => f.at >= cutoff)
    .sort((a, b) => b.at - a.at);

  if (fresh.length === 0) return '';
  const shown = fresh.slice(0, 4).map(f => f.name);
  const more = fresh.length > shown.length ? ` (+${fresh.length - shown.length})` : '';
  return `[Inbox ${fresh.length} new] ${shown.join(', ')}${more}`;
}

// --- Sprint / philosophy: only when not on defaults ---
function buildSprintMessage() {
  const configPath = join(homedir(), '.claude', 'vault-local.md');
  let section;
  try {
    const match = readFileSync(configPath, 'utf8').match(/## Vault Structure[\s\S]*?(?=\n## |$)/);
    if (!match) return '';
    section = match[0];
  } catch { return ''; }

  const get = (key) => {
    const m = section.match(new RegExp(`^${key}:[ \\t]*(.*)$`, 'm'));
    return m ? m[1].trim() : '';
  };

  const sprint = get('current_sprint');
  const mode = get('philosophy_mode') || 'default';
  if (sprint) return `[Sprint ${sprint}] mode: ${mode}`;
  if (mode !== 'default') return `[Philosophy ${mode}]`;
  return '';
}

const parts = [];
for (const build of [buildHandoffMessage, buildInboxMessage, buildSprintMessage]) {
  try { const msg = build(); if (msg) parts.push(msg); } catch { /* one failure never silences the rest */ }
}

process.stdout.write(JSON.stringify({ systemMessage: parts.join(' | ') }));
