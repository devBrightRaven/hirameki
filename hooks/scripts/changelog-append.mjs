#!/usr/bin/env node
// PostToolUse hook: append changelog entry after hirameki command execution.
// Only triggers on hirameki skill invocations.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, resolve } from 'path';
import { homedir } from 'os';

// Read stdin
let input = '';
try {
  input = readFileSync(0, 'utf8');
} catch { process.exit(0); }

let parsed;
try {
  parsed = JSON.parse(input);
} catch { process.exit(0); }

// Only act on Skill tool calls for hirameki commands
const toolName = parsed.tool_name || '';
if (toolName !== 'Skill') process.exit(0);

const skillName = parsed.tool_input?.skill || '';
if (!skillName.startsWith('hirameki:')) process.exit(0);

const command = skillName.replace('hirameki:', '');

// Read vault config
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
      return { vault: resolve(vault) };
    } catch { continue; }
  }
  return null;
}

const config = readVaultConfig();
if (!config) process.exit(0);

// Append to changelog
const logsDir = join(config.vault, '_yorozuya', 'journal');
if (!existsSync(logsDir)) mkdirSync(logsDir, { recursive: true });

const changelogPath = join(config.vault, '_yorozuya', 'changelog.md');
const now = new Date();
const date = now.toISOString().slice(0, 10);
const time = now.toTimeString().slice(0, 5);
const args = parsed.tool_input?.args || '';

const entry = `- ${time} | ${command} | ${args || '(no args)'}\n`;

let content = '';
if (existsSync(changelogPath)) {
  content = readFileSync(changelogPath, 'utf8');
}

const dateHeader = `## ${date}`;
if (content.includes(dateHeader)) {
  // Append under existing date header
  content = content.replace(dateHeader, `${dateHeader}\n${entry}`);
} else {
  // Add new date header at the top (after frontmatter if present)
  const fmEnd = content.indexOf('---', content.indexOf('---') + 1);
  if (fmEnd > 0) {
    content = content.slice(0, fmEnd + 3) + `\n\n${dateHeader}\n${entry}` + content.slice(fmEnd + 3);
  } else {
    content = `${dateHeader}\n${entry}\n` + content;
  }
}

writeFileSync(changelogPath, content, 'utf8');
process.exit(0);
