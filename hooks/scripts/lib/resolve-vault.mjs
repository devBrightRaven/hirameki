/**
 * Resolve vault path and folder layout.
 *
 * Two different questions, two different sources:
 *   - Where is the vault?  Per-machine → ~/.claude/vault-local.md
 *   - What is inside it?   Travels with the vault → <vault>/AGENTS.md
 *
 * Usage:
 *   import { getVaultPath, getVaultFolders } from './lib/resolve-vault.mjs';
 */

import { readFileSync, existsSync } from "fs";
import { join } from "path";

const home = process.env.USERPROFILE || process.env.HOME;

// Pure: extract the vault path from a flat vault-local.md config.
// Direct ^vault: match — robust against HTML comments / other lines appearing
// before the key (the old section-slice regex truncated at the first `\n<`).
export function parseVaultLocal(content) {
  const m = content.match(/^vault:\s*(.+)/m);
  return m ? m[1].trim().replace(/\/+$/, "") : null;
}

export function getVaultPath() {
  if (!home) return null;

  const vaultLocal = join(home, ".claude", "vault-local.md");
  const claudeMd = join(home, ".claude", "CLAUDE.md");

  // vault-local.md is flat per-machine config — match the key directly.
  if (existsSync(vaultLocal)) {
    const path = parseVaultLocal(readFileSync(vaultLocal, "utf8"));
    if (path) return path;
  }

  // Fall back to CLAUDE.md
  if (existsSync(claudeMd)) {
    const content = readFileSync(claudeMd, "utf8");
    // Try ## Vault Structure section
    const path = extractVaultPath(content);
    if (path) return path;
    // Try <vault> path: field
    const match = content.match(/^path:\s*(.+)/m);
    if (match) return match[1].trim().replace(/\/+$/, "");
  }

  return null;
}

function extractVaultPath(content) {
  const section = content.match(/## Vault Structure[\s\S]*?(?=\n## |\n<|$)/);
  if (!section) return null;
  const match = section[0].match(/^vault:\s*(.+)/m);
  if (!match) return null;
  return match[1].trim().replace(/\/+$/, "");
}

// --- Folder layout -------------------------------------------------------

export function parseStructureSection(content) {
  const m = content.match(/## Vault Structure[\s\S]*?(?=\n## |$)/);
  if (!m) return null;
  const section = m[0];
  return (key) => {
    const hit = section.match(new RegExp(`^\\s*${key}:[ \\t]*(.+)$`, "m"));
    return hit ? hit[1].trim() : null;
  };
}

/**
 * Returns a reader `(key) => string | null` for folder keys such as
 * daily / inbox / journal / research / handoff / templates.
 *
 * Source order: <vault>/AGENTS.md, then vault-local.md, then CLAUDE.md
 * (the last two are legacy single-file setups from before 1.4.3).
 *
 * ponytail: no hardcoded folder defaults. An unresolved key returns null so
 * the caller skips that feature instead of scanning a guessed path — the old
 * '_yorozuya/daily/' default silently read the wrong folder after a rename.
 */
export function getVaultFolders(vaultPath = getVaultPath()) {
  return makeFolderReader(vaultPath);
}

// Single-key convenience over the same source order.
export function getVaultFolder(vaultPath, key) {
  if (!vaultPath) return null;
  const value = makeFolderReader(vaultPath)(key);
  return value ? value.replace(/\/+$/, "") : null;
}

function makeFolderReader(vaultPath) {
  const sources = [];
  if (vaultPath) sources.push(join(vaultPath, "AGENTS.md"));
  if (home) {
    sources.push(join(home, ".claude", "vault-local.md"));
    sources.push(join(home, ".claude", "CLAUDE.md"));
  }

  const readers = [];
  for (const p of sources) {
    try {
      if (!existsSync(p)) continue;
      const read = parseStructureSection(readFileSync(p, "utf8"));
      if (read) readers.push(read);
    } catch { /* unreadable source — try the next one */ }
  }

  return (key) => {
    for (const read of readers) {
      const value = read(key);
      if (value) return value;
    }
    return null;
  };
}

// node resolve-vault.mjs --selftest
if (process.argv[2] === "--selftest") {
  const assert = (label, cond) => {
    if (!cond) { console.error(`FAIL  ${label}`); process.exitCode = 1; }
    else console.log(`ok    ${label}`);
  };

  const agents = `# Vault\n\n## Vault Structure\n\n\`\`\`yaml\ndaily: _yorozuya/wrap/\ninbox: _inbox/\n\`\`\`\n\n## Other\ndaily: wrong/\n`;
  const local = `## Vault Structure\n\nvault: D:/v\nlanguage: x\njournal: _legacy/journal/\n`;

  const fromAgents = parseStructureSection(agents);
  assert("reads keys inside a yaml fence", fromAgents("daily") === "_yorozuya/wrap/");
  assert("stops at the next ## heading", fromAgents("daily") !== "wrong/");
  assert("missing key returns null", fromAgents("journal") === null);

  const fromLocal = parseStructureSection(local);
  assert("legacy vault-local keys still readable", fromLocal("journal") === "_legacy/journal/");
  assert("no ## Vault Structure returns null", parseStructureSection("# nothing here") === null);
}
