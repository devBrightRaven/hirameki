#!/usr/bin/env node
// Extract structured actions from today's latest Wrap block in the daily note.
// Append to ~/.claude/homunculus/actions.jsonl and report patterns appearing 3+ times.

import { readFileSync, appendFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || process.env.USERPROFILE;
const VAULT = 'D:/Obsidian/br-os-vault';
const DAILY_DIR = join(VAULT, '_daily');
const ACTIONS_FILE = join(HOME, '.claude', 'homunculus', 'actions.jsonl');

// Ensure directory exists
mkdirSync(join(HOME, '.claude', 'homunculus'), { recursive: true });

// Get today's date
const now = new Date();
const today = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
const dailyFile = join(DAILY_DIR, `${today}.md`);

if (!existsSync(dailyFile)) {
  // No daily note today — nothing to extract
  process.exit(0);
}

const content = readFileSync(dailyFile, 'utf8');

// Find the LAST Wrap block (most recent)
const wrapMatches = [...content.matchAll(/^## Wrap \[(\d{2}:\d{2})\]/gm)];
if (wrapMatches.length === 0) {
  process.exit(0);
}

const lastWrap = wrapMatches[wrapMatches.length - 1];
const wrapTime = lastWrap[1];
const wrapStart = lastWrap.index;

// Extract content from last wrap to next --- or end of file
const afterWrap = content.slice(wrapStart);
const nextSeparator = afterWrap.indexOf('\n---', 10);
const wrapContent = nextSeparator > 0 ? afterWrap.slice(0, nextSeparator) : afterWrap;

// Find the "完成" / "Done" section (handle \r\n on Windows)
const doneMatch = wrapContent.match(/###\s*(?:完成|Done)\r?\n([\s\S]*?)(?=###|$)/);
if (!doneMatch) {
  process.exit(0);
}

const doneSection = doneMatch[1];

// Extract inline tags from each top-level item
const tagRegex = /`#([a-z0-9-]+)`/g;
const items = doneSection.split(/\n(?=- )/);

const actions = [];
const seen = new Set();

for (const item of items) {
  if (!item.trim().startsWith('- ')) continue;

  const tags = [...item.matchAll(tagRegex)].map(m => m[1]);

  // Separate action tags from project tags
  const ACTION_TYPES = new Set([
    'test-rewrite', 'test-fix', 'code-review', 'config-update', 'hook-setup',
    'automation', 'feature', 'bug-fix', 'refactor', 'research', 'vault-write',
    'git-ops', 'design', 'infra', 'skill-dev', 'debug',
    'migration', 'cleanup', 'setup', 'optimization', 'docs'
  ]);

  const actionTags = tags.filter(t => ACTION_TYPES.has(t));
  const projectTags = tags.filter(t => !ACTION_TYPES.has(t));

  // Extract title (bold text or first line)
  const titleMatch = item.match(/- \*\*(.+?)\*\*/);
  const title = titleMatch ? titleMatch[1] : item.split('\n')[0].replace(/^- /, '').replace(/`#[a-z0-9-]+`/g, '').trim();

  for (const action of actionTags) {
    const key = `${today}:${action}:${projectTags[0] || 'unknown'}`;
    if (seen.has(key)) continue;
    seen.add(key);

    actions.push({
      date: today,
      time: wrapTime,
      action,
      project: projectTags[0] || 'unknown',
      detail: title.slice(0, 80)
    });
  }

  // If no action tags found, try to infer from keywords
  if (actionTags.length === 0 && title.length > 0) {
    const inferred = inferAction(title);
    if (inferred) {
      const key = `${today}:${inferred}:${projectTags[0] || 'unknown'}`;
      if (!seen.has(key)) {
        seen.add(key);
        actions.push({
          date: today,
          time: wrapTime,
          action: inferred,
          project: projectTags[0] || 'unknown',
          detail: title.slice(0, 80)
        });
      }
    }
  }
}

// Keyword-based inference for items without tags (backward compat with old wraps)
function inferAction(text) {
  const lower = text.toLowerCase();
  if (/test|測試/.test(lower)) return 'test-rewrite';
  if (/review|審查/.test(lower)) return 'code-review';
  if (/claude\.md|settings\.json|gitignore|config/.test(lower)) return 'config-update';
  if (/hook/.test(lower)) return 'hook-setup';
  if (/skill|command|plugin/.test(lower)) return 'skill-dev';
  if (/commit|push|merge|pr|合併/.test(lower)) return 'git-ops';
  if (/研究|research|分析|analysis/.test(lower)) return 'research';
  if (/refactor|重構|精簡/.test(lower)) return 'refactor';
  if (/fix|修復|修正/.test(lower)) return 'bug-fix';
  if (/feat|功能|實作|建立/.test(lower)) return 'feature';
  if (/自動化|automation|排程/.test(lower)) return 'automation';
  return null;
}

if (actions.length === 0) {
  process.exit(0);
}

// Dedup: check if this wrap block was already extracted
const existingKeys = new Set();
if (existsSync(ACTIONS_FILE)) {
  for (const line of readFileSync(ACTIONS_FILE, 'utf8').trim().split('\n').filter(Boolean)) {
    try {
      const e = JSON.parse(line);
      existingKeys.add(`${e.date}:${e.time}:${e.action}`);
    } catch { /* skip */ }
  }
}

const newActions = actions.filter(a => !existingKeys.has(`${a.date}:${a.time}:${a.action}`));

if (newActions.length === 0) {
  process.exit(0);
}

// Append to actions.jsonl
for (const a of newActions) {
  appendFileSync(ACTIONS_FILE, JSON.stringify(a) + '\n');
}

// Scan for patterns (3+ occurrences)
if (!existsSync(ACTIONS_FILE)) {
  process.exit(0);
}

const allLines = readFileSync(ACTIONS_FILE, 'utf8').trim().split('\n').filter(Boolean);
const counts = {};

for (const line of allLines) {
  try {
    const entry = JSON.parse(line);
    const key = entry.action;
    if (!counts[key]) counts[key] = { count: 0, dates: [], projects: new Set() };
    counts[key].count++;
    if (!counts[key].dates.includes(entry.date)) counts[key].dates.push(entry.date);
    counts[key].projects.add(entry.project);
  } catch {
    // skip malformed lines
  }
}

// Only report patterns that span 5+ different days (not just raw count)
const patterns = Object.entries(counts)
  .filter(([, v]) => v.dates.length >= 5)
  .sort((a, b) => b[1].dates.length - a[1].dates.length);

if (patterns.length > 0) {
  process.stderr.write(`[pattern-tracker] 高頻操作（跨 5+ 天）：\n`);
  for (const [action, info] of patterns) {
    const projects = [...info.projects].join(', ');
    process.stderr.write(`  ${action}: ${info.dates.length} 天 / ${info.count} 次 (${projects})\n`);
  }
}
