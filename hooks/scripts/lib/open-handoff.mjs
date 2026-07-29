/**
 * Surface the next actions from the most recent handoff.
 *
 * Detecting "what keeps slipping" from prose does not work: the same item gets
 * reworded every time it is written down, so text matching either finds nothing
 * or matches generic words. Handoffs already carry the answer as structure —
 * the author wrote the next actions down deliberately. Read those instead.
 */

const HEADING = /^#{1,6}\s/;
const NEXT_ACTIONS = /^#{2,4}\s*(next actions?|下一步|next)\s*$/i;
const LIST_ITEM = /^\s*(?:[-*]|\d+\.)\s+(?:\[[ xX]\]\s*)?(.+)$/;

// Pure: list items sitting under a "Next actions" heading.
export function extractNextActions(content) {
  const items = [];
  let inSection = false;
  for (const line of content.split(/\r?\n/)) {
    if (NEXT_ACTIONS.test(line)) { inSection = true; continue; }
    if (inSection && HEADING.test(line)) break;
    if (!inSection) continue;
    const m = line.match(LIST_ITEM);
    if (m) items.push(m[1].trim());
  }
  return items;
}

// Trim to one scannable line: first sentence, hard-capped.
// Full-width stops end a sentence on their own; ASCII ones need trailing space
// so that `config.toml` and `1.` survive intact.
export function firstClause(text, max = 70) {
  const m = text.match(/^[\s\S]*?(?:[。．！？；]|[.!?;](?=\s))/);
  const cut = (m ? m[0] : text).trim();
  return cut.length > max ? cut.slice(0, max - 1) + '…' : cut;
}

/**
 * files: [{ name, content, mtimeMs }] — every handoff note.
 * Returns { name, actions } for the newest handoff written within maxAgeDays,
 * or null when there is nothing recent enough to be worth interrupting for.
 */
export function newestOpenHandoff(files, now = Date.now(), maxAgeDays = 14) {
  const cutoff = now - maxAgeDays * 24 * 60 * 60 * 1000;
  const recent = files
    .filter(f => f.mtimeMs >= cutoff)
    .sort((a, b) => b.mtimeMs - a.mtimeMs);

  for (const f of recent) {
    const actions = extractNextActions(f.content);
    if (actions.length) return { name: f.name, actions };
  }
  return null;
}
