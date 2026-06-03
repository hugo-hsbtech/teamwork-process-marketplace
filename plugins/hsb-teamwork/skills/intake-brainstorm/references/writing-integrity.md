# Writing integrity and coordination — never truncate, never clobber

Agents in this pipeline write and rewrite documents that grow large (the target
document, its humanized / translated / enriched variants, the ledger). The
failure mode to design against is **truncation**: dropping the tail of a file,
or eliding existing content with placeholders like `...`, `(rest unchanged)`,
`[continues]`, `<!-- snip -->`. A truncated artifact silently loses captured
information. Every writer agent MUST follow this protocol.

## Hard rules

1. **Full content, never elided.** Write every section in full. Never emit
   `...`, `(unchanged)`, `[continues]`, `[remaining sections omitted]`, or any
   stand-in for content that should be there. If you are reproducing a document,
   reproduce all of it.
2. **Prefer targeted `Edit` over whole-file `Write` for updates.** To change a
   filled document, edit the specific section(s) in place. A section-scoped edit
   bounds the output size of each operation and removes the temptation to
   shorten the rest of the file. Use a full `Write` only to create a file from
   scratch.
3. **Build long documents incrementally.** When creating a long file, `Write`
   the skeleton or the first part, then add each remaining section with `Edit`.
   Do not try to emit a very large document in a single `Write` call.
4. **End every document with the sentinel.** The last line of every produced
   *document* artifact is:

   ```
   <!-- END OF DOCUMENT -->
   ```

   The bundled templates already include it; preserve it on every edit. Its
   presence at the end of the file is the cheap, machine-checkable proof that the
   write was not cut off.
5. **Verify before returning.** After writing, confirm the file is complete:
   - re-read the **last lines** and check the sentinel is present and is the
     final line;
   - `grep` the file for truncation markers (`\.\.\.`, `unchanged`, `continues`,
     `omitted`, `snip`, `TODO`) that you did not intend, and for any leftover
     unfilled `[placeholder]` you were supposed to fill;
   - count the document's sections against the contract/template and confirm none
     vanished.
   If any check fails, fix it (add the missing content) before you return.
6. **Report completeness.** Your return message states: sections written /
   expected, and "sentinel present: yes". This lets the orchestrator trust the
   artifact without re-reading the whole thing.

## For the ledger (`qa-log.md`)

The ledger only grows. **Append or edit individual `Q###` blocks; never rewrite
the whole ledger in one `Write`.** Editing one block at a time means a long
interview history can never be truncated by a single large write. Keep the header
summary current with a small targeted edit.

## Orchestrator-side check

After a writer returns, the orchestrator (or the Confidence Auditor) confirms the
artifact ends with the sentinel and has the expected number of sections before
moving on. A missing sentinel means the write was truncated: re-spawn the writer
to complete the file (pointing it at what is missing) rather than accepting a
partial document.

## Why edits beat rewrites here

Beyond truncation safety, section-scoped edits keep each operation small and
reviewable, make diffs meaningful, and let parallel-safe single-writers update
their file without ever re-emitting another agent's untouched content. Reach for
`Write` to create; reach for `Edit` to change.

---

# Write coordination — queue, merge, conflicts

Truncation loses content from *one* write. Coordination protects content across
*many* writes. The read-only proposers (Strategist, File Extraction, Reconciler,
Auditor) run in parallel and produce a *stream of proposed changes*; the single
writer must absorb all of them without losing or clobbering anything.

## The invariants

1. **One writer per artifact** (the ownership table in `orchestration.md`).
2. **Serialized.** The orchestrator never spawns two writers on the *same* file at
   the same time. Proposers parallelize; the writer for a given file runs alone.
3. **Queue, never drop.** Pending changes to an artifact accumulate (as proposals
   the orchestrator holds, or as entries in the ledger) and the single writer
   **drains the whole queue in one commit pass**. Proposals that arrive while a
   write is in flight wait for the next pass. Nothing is discarded; nothing spawns
   a competing writer.

## Read-modify-write (RMW) — the anti-clobber rule

A writer **always re-reads the current file immediately before editing** and
computes its changes against that latest on-disk content, never a stale copy or a
remembered version. This guarantees it merges *into whatever is actually there*,
so a change it didn't author is never overwritten.

## Merge, don't overwrite

- Apply the whole pending batch in **one coherent pass**, preserving all existing
  content **and** all new content. Additive by default; updates are section-scoped
  `Edit`s.
- **Key every change by a stable id** (question `Q###`, section `id`, glossary
  term). Keying makes writes **idempotent**: re-applying the same change updates in
  place instead of duplicating, and lets two batches merge deterministically.

## Write-time conflict handling (keep sanity)

When two pending changes target the **same id with incompatible content**, do not
pick one silently:

- **Record both** with their provenance and confidence.
- Keep as primary the value the **Reconciler** recommends (or, absent a ruling, the
  more recent / better-sourced / higher-confidence one); note the loser in the
  entry's `Hint`.
- If it is genuinely undecidable, do not guess — surface a disambiguating question
  to the human, or set an honest `assumption`/`discovery` disposition.
- Treat *replacing* existing substantive content with different content as a
  **conflict, not an update** — flag it rather than overwrite.

Derived sections (triage draft, readiness, escalation) are **recomputed from their
inputs** rather than merged, so they converge instead of conflicting.

## Revision marker (optimistic-concurrency sanity check)

Each writable artifact carries a marker near the top:

```
<!-- rev: N · updated: AAAA-MM-DD -->
```

The writer **bumps `N`** on every commit. A proposal records the `rev` it was based
on; if the file's current `rev` is higher, the file moved underneath the proposal,
so the writer treats any overlap as a write-time conflict (above) instead of a
blind apply. This is the cheap check that keeps concurrent activity sane even
though writes are serialized.
