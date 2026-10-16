# Concept-card capability

This is the shared contract used by lens; it is not a separately advertised command.

## Scope and discovery

Resolve `{material}` from `## Vault Structure` in the selected vault's AGENTS.md. `0 Material/` is a conventional label, not a hardcoded destination. Stop before a write if the destination is unresolved; never copy another agent's settings.

Use the supplied source file, folder path or pasted text; state the resolved scan scope. A discovery-only request returns candidates without writing. Do not expand a narrow scope into a whole-vault scan. Treat unreadable coverage as unverified.

Extract one atomic, reusable claim per candidate with its passage provenance, supporting evidence, limitations and related cards. A question or observation alone is not a mature claim. Deduplicate by claim and evidence identity: one candidate across source files, retaining all sources; two copies of one event do not establish independent support.

Check `{material}` for existing cards before drafting. Existing full coverage means link to that card instead of making a duplicate; propose an update only for an explicit new difference. A missing or misspelled wiki link does not establish a missing card.

If an Insights folder is configured, inspect relevant existing notes without inventing its path. An Insights note without a follow-up material card remains a candidate. If not inspectable, say `Insights coverage: unverified`; do not claim comprehensive deduplication. Do not invent an Insights path.

## Draft and persistence

A card contains one atomic claim, provenance and an applicable limit or recheck condition. Match existing note structure and title language. Preserve required frontmatter, including tags, status, source, created, `says:` and relevant up/related links. `says:` states the claim, not a description of the document. Use the actual producing runtime's permitted source label.

Show the entire draft and proposed `{material}/<Title>.md`, then ask `Action? (save this / skip / edit)`. No write or directory creation before explicit approval of that content and path. Recheck for an existing target; never overwrite a card merely to save a candidate. After successful save print the full path. A MOC link is a separate displayed change requiring approval.

This capability neither changes rules nor promotes runtime memory. A source may yield multiple cards, but each must have a clear approved draft. Preserve original notes and evidence.
A file listing shows files only and can miss empty folders; never state or act on a folder or file being missing unless a direct check confirms it; otherwise say no files were found there.
