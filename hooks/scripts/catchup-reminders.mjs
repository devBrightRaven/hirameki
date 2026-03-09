#!/usr/bin/env node
// catchup-reminders.mjs — Deterministic reminder checks for catchup.
// Outputs reminder lines to stdout. If nothing to report, outputs nothing.

import { readFileSync, existsSync, readdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || process.env.USERPROFILE;
const ACTIONS_FILE = join(HOME, '.claude', 'homunculus', 'actions.jsonl');
const SKILL_CHANGES_FILE = join(HOME, '.claude', 'homunculus', 'skill-changes.jsonl');
const STOCKTAKE_RESULTS = join(HOME, '.claude', 'skills', 'skill-stocktake', 'results.json');

// Read vault path from CLAUDE.md
function getVaultConfig() {
  const claudeMd = join(HOME, '.claude', 'CLAUDE.md');
  if (!existsSync(claudeMd)) return null;
  const content = readFileSync(claudeMd, 'utf8');
  const vaultMatch = content.match(/^vault:\s*(.+)/m);
  const logsMatch = content.match(/^logs:\s*(.+)/m);
  if (!vaultMatch) return null;
  return {
    vault: vaultMatch[1].trim(),
    logs: logsMatch ? logsMatch[1].trim() : '_agent_logs/'
  };
}

const reminders = [];
const now = new Date();
const thirtyDaysAgo = new Date(now - 30 * 24 * 60 * 60 * 1000);

// --- Check 1: High-frequency action patterns (past 30 days) ---
if (existsSync(ACTIONS_FILE)) {
  const lines = readFileSync(ACTIONS_FILE, 'utf8').trim().split('\n').filter(Boolean);
  const counts = {};

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      const entryDate = new Date(entry.date);
      if (entryDate < thirtyDaysAgo) continue;

      const key = entry.action;
      if (!counts[key]) counts[key] = { count: 0, dates: new Set() };
      counts[key].count++;
      counts[key].dates.add(entry.date);
    } catch { /* skip */ }
  }

  for (const [action, info] of Object.entries(counts)) {
    if (info.dates.size >= 5) {
      reminders.push(`⚠ ${action}: ${info.dates.size} 天 / ${info.count} 次 — 考慮自動化？`);
    }
  }
}

// --- Check 2: Skill files changed since last stocktake ---
if (existsSync(SKILL_CHANGES_FILE)) {
  let lastStocktake = '2000-01-01T00:00:00Z';
  if (existsSync(STOCKTAKE_RESULTS)) {
    try {
      const results = JSON.parse(readFileSync(STOCKTAKE_RESULTS, 'utf8'));
      lastStocktake = results.evaluated_at || lastStocktake;
    } catch { /* ignore */ }
  }

  const lines = readFileSync(SKILL_CHANGES_FILE, 'utf8').trim().split('\n').filter(Boolean);
  const changedFiles = new Set();
  for (const line of lines) {
    try {
      const e = JSON.parse(line);
      if (e.timestamp > lastStocktake) changedFiles.add(e.file);
    } catch { /* skip */ }
  }

  if (changedFiles.size >= 3) {
    reminders.push(`⚠ ${changedFiles.size} 個 skill 自上次 stocktake 後被修改 — 考慮跑 /skill-stocktake`);
  }
}

// --- Check 3: Journal corrections not yet reviewed ---
const config = getVaultConfig();
if (config) {
  const logsDir = join(config.vault, config.logs);
  if (existsSync(logsDir)) {
    const files = readdirSync(logsDir).filter(f => f.endsWith('.md'));
    let recent = 0;   // 1-7 days
    let aging = 0;     // 8-14 days
    let critical = 0;  // 15-30 days

    for (const file of files) {
      const dateMatch = file.match(/^(\d{4}-\d{2}-\d{2})/);
      if (!dateMatch) continue;

      const fileDate = new Date(dateMatch[1]);
      const daysAgo = Math.floor((now - fileDate) / (24 * 60 * 60 * 1000));
      if (daysAgo > 30) continue;

      // Read first 500 bytes for frontmatter
      const filePath = join(logsDir, file);
      let content;
      try {
        const buf = Buffer.alloc(500);
        const fd = require('fs').openSync(filePath, 'r');
        const bytesRead = require('fs').readSync(fd, buf, 0, 500, 0);
        require('fs').closeSync(fd);
        content = buf.toString('utf8', 0, bytesRead);
      } catch { continue; }

      const corrMatch = content.match(/^corrections:\s*(\d+)/m);
      if (!corrMatch || parseInt(corrMatch[1]) === 0) continue;

      if (daysAgo <= 7) recent++;
      else if (daysAgo <= 14) aging++;
      else critical++;
    }

    if (critical > 0) {
      reminders.push(`🔴 ${critical} 個 corrections 已超過兩週未 review — 請跑 /corrections-review 並將重要的加進 CLAUDE.md`);
    } else if (aging > 0) {
      reminders.push(`⚠ ${aging} 個 corrections 已超過一週未 review — 建議今天跑 /corrections-review`);
    } else if (recent > 0) {
      reminders.push(`⚠ 本週 ${recent} 個 session 有 corrections 未 review — 考慮跑 /corrections-review`);
    }
  }
}

// --- Check 4: Recent pitfalls from auto-learn ---
const PITFALLS_FILE = join(HOME, '.claude', 'homunculus', 'pitfalls.jsonl');
if (existsSync(PITFALLS_FILE)) {
  const pitfallLines = readFileSync(PITFALLS_FILE, 'utf8').trim().split('\n').filter(Boolean);
  const sevenDaysAgo = new Date(now - 7 * 24 * 60 * 60 * 1000);

  // Count pitfall types in past 7 days
  const typeCounts = {};
  let totalSessions = 0;

  for (const line of pitfallLines) {
    try {
      const record = JSON.parse(line);
      if (new Date(record.timestamp) < sevenDaysAgo) continue;
      totalSessions++;
      for (const p of record.pitfalls) {
        typeCounts[p.type] = (typeCounts[p.type] || 0) + (p.count || 1);
      }
    } catch { /* skip */ }
  }

  if (totalSessions >= 2) {
    const parts = [];
    if (typeCounts['user-correction']) parts.push(`${typeCounts['user-correction']} corrections`);
    if (typeCounts['retry']) parts.push(`${typeCounts['retry']} retries`);
    if (typeCounts['back-and-forth']) parts.push(`${typeCounts['back-and-forth']} back-and-forth edits`);
    if (parts.length > 0) {
      reminders.push(`⚠ Past 7 days pitfalls (${totalSessions} sessions): ${parts.join(', ')} — check pitfalls.jsonl or run /corrections-review`);
    }
  }
}

// --- Output ---
if (reminders.length > 0) {
  console.log('**提醒**');
  console.log('');
  for (const r of reminders) {
    console.log(`- ${r}`);
  }
}
