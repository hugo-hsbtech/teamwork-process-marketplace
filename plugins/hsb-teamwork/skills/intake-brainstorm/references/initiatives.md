# Initiatives — the unit of work, state, resume, and selection

**The plugin is stateless; the initiative is stateful.** The skill, agents, and
references never change between runs (they are read-only, and copied on install).
All run context — the contract, the questions and answers, the document, the
glossary — lives in an **initiative folder** in your project. An initiative is a
single demand carried across *fronts*: the intake front, the readiness front, and
whatever fronts come later. Each front (a "phase") is one or more runs of the
pipeline that **point at the same initiative**, so the initiative directory
accumulates the outputs of every run and every agent that touched it.

This is the rename that matters: **what we used to call a "session" is now an
"initiative."** A session was per-skill; an initiative is the shared home for all
fronts of one demand. The intake phase and the readiness phase are different
fronts of the *same* initiative, living side by side under it.

## Where initiatives live (stable, not cwd-relative)

Resolve the **initiatives root** in this order, so it is the same no matter which
subdirectory you invoke from:

1. `$TEAMWORK_HOME` if set (use it verbatim — lets you point at shared storage);
2. else the **project root** — the nearest enclosing git top-level
   (`git rev-parse --show-toplevel`) — plus `/.teamwork`;
3. else, only if neither exists, the current directory plus `/.teamwork`.

```
TEAMWORK_ROOT  = $TEAMWORK_HOME | <git-root>/.teamwork | <cwd>/.teamwork
INITIATIVE_DIR = TEAMWORK_ROOT/<YYYYMMDD>-<HHMM>-<project>-<hash6>
PHASE_DIR      = INITIATIVE_DIR/<phase>          # phase ∈ intake | readiness | …
```

### The initiative folder name

`<YYYYMMDD>-<HHMM>-<project>-<hash6>` — for example `20260603-1833-pokerplan-a8432a`:

- `YYYYMMDD-HHMM` — the creation date and time (local), so initiatives sort
  chronologically and the **latest** one is trivially the last by name.
- `<project>` — a deterministic kebab-case slug of the project / demand name
  (lowercased, spaces to `-`, punctuation dropped).
- `<hash6>` — six random lowercase hex characters generated **once** at creation,
  guaranteeing uniqueness even if two initiatives share a project and minute. It
  is an opaque id, not derived from content — never recompute it.

The name is assigned at creation and is immutable. Generate the hash with e.g.
`openssl rand -hex 3` (3 bytes → 6 hex chars).

### Phases share the initiative

Each front gets its **own phase subfolder** under the initiative, so fronts never
clobber each other but stay traceably linked:

```
.teamwork/20260603-1833-pokerplan-a8432a/
├── initiative.json            # the manifest (status, project, phases) — see below
├── intake/                    # the intake-brainstorm front
│   ├── contract.lock.md
│   ├── sources-index.md
│   ├── sources/
│   ├── qa-log.md
│   ├── target-document.md
│   ├── glossary.md
│   ├── readiness-report.md
│   └── output/
│       ├── humanized.md
│       ├── translated.<lang>.md
│       ├── enriched.md
│       └── manifest.md
└── readiness/                 # the readiness-package front (inherits intake/output)
    ├── contract.lock.md
    ├── qa-log.md
    ├── readiness-document.md
    └── output/…
```

`PHASE_DIR` is what every agent is handed; it is the working root for that front
(everything an agent reads or writes — `sources/`, `qa-log.md`, the document,
`output/` — is relative to `PHASE_DIR`). Agents never need to know the initiative
name; the orchestrator resolves it and injects the path.

## The initiative manifest — `initiative.json`

One JSON file at the initiative root records identity and **open/closed status**.
It is owned by the orchestrator (you), not by any agent.

```json
{
  "name": "20260603-1833-pokerplan-a8432a",
  "project": "pokerplan",
  "created": "2026-06-03T18:33:00-03:00",
  "status": "open",
  "language": "pt-BR",
  "phases": {
    "intake":    { "started": "2026-06-03T18:33:00-03:00", "state": "frozen" },
    "readiness": { "started": "2026-06-04T09:10:00-03:00", "state": "active" }
  }
}
```

- `status` — **`open`** while any front may still run; **`closed`** once the human
  declares the initiative finished. **Closed initiatives are ignored** when
  listing (see below). Only the human closes an initiative; never auto-close on a
  whim.
- `phases.<phase>.state` — `active` while the front is in progress; `frozen` once
  its terminal artifact (the packaged `output/manifest.md`) is produced. A frozen
  phase does **not** close the initiative — a later front (e.g. readiness) can
  still open against it.
- Write it on creation; update `phases` when a front starts or freezes; flip
  `status` to `closed` only when the human says the whole demand is done.

## Resolve-or-select (run this first, every invocation)

Because the initiative name is timestamped (not derived from the demand text),
you cannot recompute it — you **discover and select** it. Run this before any
agent:

1. Compute `TEAMWORK_ROOT`. List the initiative folders whose `initiative.json`
   has `status: open`. **Closed initiatives are omitted entirely.**
2. Identify the **latest open** initiative (the newest by folder timestamp).
   - If one exists, ask the human: *"Continue in initiative `<name>`?"* If yes →
     that is the `INITIATIVE_DIR`.
   - If the human says no, **list every open initiative** as selectable options
     (newest first; show project + date) plus a **"Start a new initiative"**
     choice, and let the human pick. Use `AskUserQuestion` so the choice is
     explicit — never guess.
3. If there are **no open initiatives**, or the human chose "Start a new
   initiative," **create one**: derive the `<project>` slug, generate `<hash6>`,
   build the `<YYYYMMDD>-<HHMM>-<project>-<hash6>` name, create `INITIATIVE_DIR`,
   and write `initiative.json` with `status: open`.
4. **Then resolve the phase.** `PHASE_DIR = INITIATIVE_DIR/<phase>` for the front
   you are running (`intake` for intake-brainstorm, `readiness` for
   readiness-package). **If `PHASE_DIR` already exists → RESUME it** (read
   `contract.lock.md`, `qa-log.md`, and the phase document, and continue — the
   *revisit* path). **If not → create it** and register the phase in
   `initiative.json.phases`. Never fork a second phase folder (`intake-2/`).

Resuming is always safe because of the idempotency rules below.

## Why re-running never duplicates (within a phase)

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

If the template hash changed since the phase's `contract.lock.md`, the Template
Analyst restarts the analysis and supersedes stale ledger entries (see
`contract-and-template.md` § Restart). The phase folder is reused; only the
contract and affected questions are refreshed.

## Batch mode

Each input signal gets its **own** `INITIATIVE_DIR` under the same
`TEAMWORK_ROOT`, with a freshly generated name and its own `initiative.json`.
Distinct signals never collide because each has its own random `<hash6>`. Re-running
a batch creates new initiatives for new signals; to *resume* a signal, select its
existing open initiative via the resolve-or-select flow rather than starting a new
one.

## Carrying an initiative across machines / checkouts

The initiative folder is plain files. To preserve context beyond one machine,
either commit the `.teamwork/` folder to the repo, or set `$TEAMWORK_HOME` to
shared storage. Because the plugin is stateless, any machine with the plugin
installed resolves and resumes the same initiative folder identically.

<!-- END OF DOCUMENT -->
