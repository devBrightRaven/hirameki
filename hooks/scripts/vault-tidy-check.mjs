#!/usr/bin/env node
// vault-tidy-check.mjs — Fast frontmatter health check for nightly-check.
// Pure Node.js — no shell forks per file.

import { readdirSync, readFileSync, statSync, existsSync } from 'fs';
import { join, extname } from 'path';

const VAULT = process.argv[2] || 'D:/Obsidian/br-os-vault';
const VALID_STATUS = new Set(['published', 'draft', 'reference', 'outline', 'spec', 'log', 'archive']);

const SCAN_DIRS = [
  'Project', '_inbox', '_agent_analysis', '_agent_logs', '_startup_radar'
].map(d => join(VAULT, d));

const SKIP = new Set(['_hirameki_cmds', '.git', 'node_modules', '.obsidian']);

let total = 0, noFrontmatter = 0, noTags = 0, noStatus = 0, invalidStatus = 0;

function walk(dir, depth = 0) {
  if (depth > 3) return;
  if (!existsSync(dir)) return;

  let entries;
  try { entries = readdirSync(dir, { withFileTypes: true }); }
  catch { return; }

  for (const entry of entries) {
    if (SKIP.has(entry.name)) continue;

    const full = join(dir, entry.name);

    if (entry.isDirectory()) {
      walk(full, depth + 1);
    } else if (entry.isFile() && extname(entry.name) === '.md') {
      checkFile(full);
    }
  }
}

function checkFile(filePath) {
  total++;

  let content;
  try {
    // Only read first 500 bytes — frontmatter is always at the top
    const buf = Buffer.alloc(500);
    const fd = require('fs').openSync(filePath, 'r');
    const bytesRead = require('fs').readSync(fd, buf, 0, 500, 0);
    require('fs').closeSync(fd);
    content = buf.toString('utf8', 0, bytesRead);
  } catch {
    return;
  }

  if (!content.startsWith('---')) {
    noFrontmatter++;
    return;
  }

  // Extract frontmatter between first --- and second ---
  const endIdx = content.indexOf('\n---', 4);
  if (endIdx < 0) {
    noFrontmatter++;
    return;
  }

  const fm = content.slice(4, endIdx);

  if (!/^tags:/m.test(fm)) {
    noTags++;
  }

  const statusMatch = fm.match(/^status:\s*(.+)/m);
  if (!statusMatch) {
    noStatus++;
  } else {
    const val = statusMatch[1].trim();
    if (!VALID_STATUS.has(val)) {
      invalidStatus++;
    }
  }
}

for (const dir of SCAN_DIRS) {
  walk(dir);
}

const issues = noFrontmatter + noTags + noStatus + invalidStatus;
const health = total > 0 ? Math.round((total - issues) * 100 / total) : 100;

console.log(`Scanned: ${total} files`);
console.log(`Health: ${health}%`);
if (noFrontmatter > 0) console.log(`  Missing frontmatter: ${noFrontmatter}`);
if (noTags > 0) console.log(`  Missing tags: ${noTags}`);
if (noStatus > 0) console.log(`  Missing status: ${noStatus}`);
if (invalidStatus > 0) console.log(`  Invalid status: ${invalidStatus}`);
if (issues === 0) console.log(`  All clean.`);
if (health < 90) console.log(`\nConsider running /hirameki:tidy fix`);
