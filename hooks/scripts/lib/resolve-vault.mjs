/**
 * Resolve vault path from vault-local.md or CLAUDE.md.
 * Usage: import { getVaultPath } from './lib/resolve-vault.mjs';
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

// Folder layout lives in <vault>/AGENTS.md so any agent can resolve it without
// reading Claude-private config. Returns null when the key is absent.
export function getVaultFolder(vaultPath, key) {
  if (!vaultPath) return null;
  const agents = join(vaultPath, "AGENTS.md");
  if (!existsSync(agents)) return null;
  const m = readFileSync(agents, "utf8").match(new RegExp(`^${key}:\\s*(.+)`, "m"));
  return m ? m[1].trim().replace(/\/+$/, "") : null;
}

function extractVaultPath(content) {
  const section = content.match(/## Vault Structure[\s\S]*?(?=\n## |\n<|$)/);
  if (!section) return null;
  const match = section[0].match(/^vault:\s*(.+)/m);
  if (!match) return null;
  return match[1].trim().replace(/\/+$/, "");
}
