// Self-check for the handoff parser behind the SessionStart nudge.
// Run: node tests/test_open_handoff.mjs
import assert from 'assert';
import { extractNextActions, firstClause, newestOpenHandoff }
  from '../hooks/scripts/lib/open-handoff.mjs';

const doc = (section) => `---
tags: [handoff]
---

# Handoff

## What's done

- shipped the thing

${section}

## Traps

- do not touch the mirror
`;

// Numbered and bulleted items both count; the next heading closes the section.
assert.deepStrictEqual(
  extractNextActions(doc('## Next actions\n\n1. decide the branch\n2. tell the other machine')),
  ['decide the branch', 'tell the other machine']
);
assert.deepStrictEqual(
  extractNextActions(doc('## Next actions\n\n- one\n- two')),
  ['one', 'two']
);
assert.deepStrictEqual(extractNextActions(doc('## 下一步\n\n- 裁決分支')), ['裁決分支']);

// Items from other sections never leak in.
assert.deepStrictEqual(extractNextActions(doc('## Decisions made\n\n- picked A')), []);

// Trailing prose after the list is ignored, but the list is kept.
assert.deepStrictEqual(
  extractNextActions('## Next actions\n\n1. do it\n\nsome closing prose\n'),
  ['do it']
);

// firstClause trims at the first sentence break and hard-caps length.
assert.strictEqual(firstClause('裁決那 21 個檔。建議提交。'), '裁決那 21 個檔。');
assert.strictEqual(firstClause('short one'), 'short one');
assert.strictEqual(firstClause('x'.repeat(100)).length, 70);

// Newest handoff wins; ones with no actions are skipped, not fatal.
const files = [
  { name: 'old.md', mtimeMs: 1000, content: doc('## Next actions\n\n- stale') },
  { name: 'new.md', mtimeMs: 3000, content: doc('## Next actions\n\n- fresh') },
  { name: 'empty.md', mtimeMs: 4000, content: doc('## Decisions made\n\n- none') },
];
assert.deepStrictEqual(
  newestOpenHandoff(files, 4000, 14),
  { name: 'new.md', actions: ['fresh'] }
);

// Anything older than the window stays silent rather than resurfacing.
const old = 4000 + 15 * 24 * 60 * 60 * 1000;
assert.strictEqual(newestOpenHandoff(files, old, 14), null);

console.log('ok — handoff parser');
