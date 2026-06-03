# Sessions — state, resume, and idempotency

**The plugin is stateless; the session is stateful.** The skill, agents, and
references never change between runs (they are read-only, and copied on install).
All run context — the contract, the questions and answers, the document, the
glossary — lives in a **session folder** in your project. Preserving work across
runs means always resolving to the *same* session folder and resuming it, never
starting a parallel one. This file defines how.

## Where the session lives (stable, not cwd-relative)

Resolve the **session root** in this order, so it is the same no matter which
subdirectory you invoke from:

1. `$INTAKE_HOME` if set (use it verbatim — lets you point at shared storage);
2. else the **project root** — the nearest enclosing git top-level
   (`git rev-parse --show-toplevel`) — plus `/intake`;
3. else, only if neither exists, the current directory plus `/intake`.

```
SESSION_ROOT = $INTAKE_HOME | <git-root>/intake | <cwd>/intake
SESSION_DIR  = SESSION_ROOT/<demand-slug>
```

The **slug** is a deterministic kebab-case of the demand name (lowercased, spaces
to `-`, punctuation dropped). The same demand always maps to the same slug, so the
same `SESSION_DIR`.

## Resolve-or-resume (run this first, every invocation)

1. Compute `SESSION_ROOT` and the `<demand-slug>`.
2. **If `SESSION_DIR` already exists → RESUME it.** Read `contract.lock.md`,
   `qa-log.md`, and `target-document.md`, and continue from there (this is the
   *revisit* path). Do **not** create `<slug>-2/` or a fresh folder.
3. **If it does not exist → CREATE it** and start fresh.
4. **If the demand is ambiguous** (the statement could match an existing session,
   or several do), list the candidates and ask the human whether to resume one or
   start new. Never guess in a way that silently forks a second session.

Resuming is always safe because of the idempotency rules below.

## Why re-running never duplicates (within a session)

Every writer agent obeys `writing-integrity.md`:

- **Read-modify-write:** re-read the file before editing; merge into current
  content.
- **Key by stable id:** questions by `Q###`, sections by `id`, glossary by term.
  Re-applying the same change updates in place instead of appending a duplicate.
- **Supersede, never delete:** obsolete entries are marked `superseded`, kept for
  the audit trail.
- **`rev` marker:** detects whether the file moved underneath a change, so
  overlaps become conflicts (for the Reconciler), not blind double-writes.

So running the loop again, re-spawning an agent, or resuming a day later **merges**
into the existing artifacts. It does not re-ask answered questions, re-create
sections, or emit duplicate files.

## Template changes

If the template hash changed since the session's `contract.lock.md`, the Template
Analyst restarts the analysis and supersedes stale ledger entries (see
`contract-and-template.md` § Restart). The session folder is reused; only the
contract and affected questions are refreshed.

## Batch mode

Each input signal gets its **own** `SESSION_DIR` under the same `SESSION_ROOT`,
keyed by its own slug. Deterministic slugs mean re-running a batch **resumes** each
signal's session rather than producing a second copy. Distinct signals never
collide because their slugs differ.

## Carrying a session across machines / checkouts

The session folder is plain files. To preserve context beyond one machine, either
commit the `intake/` folder to the repo, or set `$INTAKE_HOME` to shared storage.
Because the plugin is stateless, any machine with the plugin installed will resume
the same session folder identically.

<!-- END OF DOCUMENT -->
