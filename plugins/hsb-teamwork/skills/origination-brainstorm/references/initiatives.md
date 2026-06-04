# Initiatives — the unit of work, state, resume, and selection

**The plugin is stateless; the initiative is stateful.** The skill, agents, and
references never change between runs (they are read-only, and copied on install).
All run context — the contract, the questions and answers, the document, the
glossary — lives in an **initiative folder** in your project. An initiative is a
single demand carried across *fronts*: the origination front, the readiness front,
and whatever fronts come later. Each front (a "phase") is one or more runs of the
pipeline that **point at the same initiative**, so the initiative directory
accumulates the outputs of every run and every agent that touched it.

This is the rename that matters: **what we used to call a "session" is now an
"initiative."** A session was per-skill; an initiative is the shared home for all
fronts of one demand. The origination phase and the readiness phase are different
fronts of the *same* initiative, living side by side under it.

Because the fronts share a home, the initiative is also where a **new front
becomes aware of everything that came before it** — every definition the demand
has settled on, and every work prior fronts produced. Two initiative-level files
make that awareness concrete and machine-readable: the **manifest**
(`initiative.json`) is an *index of definitions and works*, and the **shared
definitions store** (`glossary.md` + `decisions.md`) is the single, non-drifting
home for terms and cross-phase decisions. Both are described below; the
orchestrator owns all three initiative-level files and **brokers** them to the
phase agents.

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
PHASE_DIR      = INITIATIVE_DIR/<phase>          # phase ∈ origination | readiness | …
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
├── initiative.json            # the works + definitions index (status, phases, artifacts, owes) — see below
├── glossary.md                # shared canonical terms — ONE per initiative (Glossary Keeper)
├── decisions.md               # shared cross-phase decisions ledger (Glossary Keeper)
├── origination/               # the origination-brainstorm front
│   ├── contract.lock.md
│   ├── sources-index.md
│   ├── sources/
│   ├── qa-log.md
│   ├── target-document.md
│   ├── glossary.md            # read-only copy the orchestrator BROKERS in from the initiative store
│   ├── readiness-report.md
│   └── output/
│       ├── humanized.md
│       ├── translated.<lang>.md
│       ├── enriched.md
│       └── manifest.md
└── readiness/                 # the readiness-package front (inherits origination/output)
    ├── contract.lock.md
    ├── qa-log.md
    ├── readiness-document.md
    ├── glossary.md            # the same brokered copy
    └── output/…
```

`PHASE_DIR` is what every agent is handed; it is the working root for that front
(everything an agent reads or writes — `sources/`, `qa-log.md`, the document,
`output/` — is relative to `PHASE_DIR`). Agents never need to know the initiative
name; the orchestrator resolves it and injects the path.

The three **initiative-level** files (`initiative.json`, `glossary.md`,
`decisions.md`) live *above* any `PHASE_DIR`. Phase agents stay `PHASE_DIR`-scoped
and never reach up to them; the orchestrator is the **broker** that reads the index
and seeds the shared definitions into each phase (see *Brokering* below). The one
exception is the Glossary Keeper, the sole content writer of the shared store,
which the orchestrator spawns with the store path injected as `DEFINITIONS_DIR`.

## The initiative manifest — `initiative.json` (index of definitions and works)

One JSON file at the initiative root is the initiative's **index**: identity,
open/closed status, pointers to the shared definitions, and — per phase — what that
front **produced** (its works), how ready it was, and what it still **owes**
downstream. It is owned by the orchestrator (you), not by any agent. A front that
is about to start reads this one file to discover everything prior fronts defined
and produced, instead of crawling each phase's documents or hard-coding paths.

```json
{
  "name": "20260603-1833-pokerplan-a8432a",
  "project": "pokerplan",
  "created": "2026-06-03T18:33:00-03:00",
  "status": "open",
  "language": "pt-BR",
  "definitions": {
    "glossary": "glossary.md",
    "decisions": "decisions.md"
  },
  "phases": {
    "origination": {
      "started": "2026-06-03T18:33:00-03:00",
      "state": "frozen",
      "templateHash": "74cd7c34…",
      "readiness": 100,
      "produces": "origination-record",
      "consumes": [],
      "artifacts": {
        "document": "origination/target-document.md",
        "canonical": "origination/output/humanized.md",
        "manifest": "origination/output/manifest.md"
      },
      "owes": []
    },
    "readiness": {
      "started": "2026-06-04T09:10:00-03:00",
      "state": "active",
      "templateHash": "74cd7c34…",
      "readiness": 78,
      "produces": "readiness-package",
      "consumes": ["origination-record"],
      "artifacts": {
        "document": "readiness/readiness-document.md",
        "canonical": "readiness/output/humanized.md",
        "manifest": "readiness/output/manifest.md"
      },
      "owes": [
        { "ref": "TechAssessmentRef", "to": "tech-assessment", "status": "deferred",
          "note": "TA pending — out of current tooling scope" }
      ]
    }
  }
}
```

**Identity / lifecycle**

- `status` — **`open`** while any front may still run; **`closed`** once the human
  declares the initiative finished. **Closed initiatives are ignored** when
  listing (see below). Only the human closes an initiative; never auto-close on a
  whim.
- `definitions` — pointers (relative to `INITIATIVE_DIR`) to the shared definitions
  store every front reads. See *Shared definitions* below.

**The works index — per `phases.<phase>` entry**

- `state` — `active` while the front is in progress; `frozen` once its terminal
  artifact (the packaged `output/manifest.md`) is produced. A frozen phase does
  **not** close the initiative — a later front can still open against it.
- `templateHash` — the locked template hash for that front (mirrors its
  `contract.lock.md`), so a downstream front can tell whether an upstream artefact
  was produced under a since-changed template.
- `readiness` — the front's readiness/confidence score (0–100): live while active,
  final when frozen.
- `produces` — the artefact kind this front yields (`origination-record`,
  `readiness-package`, …); `consumes` — the upstream artefact kinds it inherited.
  Together these let a new front discover *which* prior front to inherit from by
  kind, not by a hard-coded phase name.
- `artifacts` — the canonical paths (relative to `INITIATIVE_DIR`) of the front's
  works: the working `document`, the `canonical` clean copy (the humanized output —
  the one downstream fronts inherit), and the `manifest`.
- `owes` — outstanding **cross-phase debts**: handoffs a downstream front must pick
  up. Each is `{ ref, to, status, note }` (e.g. a readiness front owing a
  `TechAssessmentRef` to a future `tech-assessment` front). This is how a debt
  raised inside one front's document becomes a fact the *next* front reads.

**Maintaining it (orchestrator).** Write it on initiative creation. Update the
phase entry when a front **starts** (register `started`, `state: active`,
`consumes`, `templateHash`) and when it **freezes** (set `state: frozen`, final
`readiness`, the `artifacts` paths, and any `owes`). Flip `status` to `closed` only
when the human says the whole demand is done. All updates are read-modify-write,
keyed by phase name — never clobber a sibling phase's entry.

## The initiative as the index a new front reads

When a front starts, its first awareness step (part of resolve-or-select, step 5
below) is to **read `initiative.json`**:

- `phases.*.produces` + `artifacts` — *the works*: what every prior front produced
  and where its canonical copy lives. A readiness front finds the
  `origination-record` by looking for the phase whose `produces` is
  `origination-record` and reading its `artifacts.canonical`, rather than assuming
  `origination/`.
- `phases.*.owes` — *the debts*: anything a prior front parked for this one to
  resolve (e.g. an owed Technical Assessment).
- `definitions` — *the definitions*: the shared glossary and decisions the front
  must stay consistent with.

The orchestrator then **brokers** what the front needs into its phase (below).

## Shared definitions — `glossary.md` + `decisions.md`

Definitions belong to the **initiative**, not to a phase. A term coined during
origination is the same term readiness and every later front use; a cross-phase
decision is binding everywhere. So the canonical glossary and decisions live once,
at the initiative root, instead of being re-derived or copied per phase (which is
how terminology drifts).

- `glossary.md` — canonical terms: `term | canonical form | definition | do-not-use
  synonyms | notes`.
- `decisions.md` — cross-phase decisions ledger: one row per decision, keyed by a
  stable id (`D###`), recording the decision, its scope, the phase it was made in,
  date, and status; superseded rows are kept and marked.

**One content writer: the Glossary Keeper.** It is the sole agent that authors the
shared store. The orchestrator spawns it with the store path injected as
`DEFINITIONS_DIR` (= `INITIATIVE_DIR`) — the single, deliberate exception to the
"agents are `PHASE_DIR`-scoped" rule, because definitions are inherently
cross-phase and need exactly one writer. It obeys `writing-integrity.md`
(read-modify-write, key by term/`D###`, supersede-never-delete, END sentinel).

## Brokering (how phase agents become aware, staying `PHASE_DIR`-scoped)

Phase agents never resolve the initiative or read above their `PHASE_DIR`. The
**orchestrator is the broker**: it reads the initiative-level index and definitions
and places into each phase exactly what that phase's agents need, *before* spawning
them.

1. **Seed definitions down.** Before spawning any reader (Doc Updater, Synthesizer,
   Humanizer, Translator, Packager), copy the current `INITIATIVE_DIR/glossary.md`
   (and, where relevant, `decisions.md`) into the phase as a read-only reference at
   `PHASE_DIR/glossary.md`. Agents keep reading `PHASE_DIR/glossary.md` exactly as
   before — they need not know it came from the initiative store.
2. **Merge keeper output up.** After the Glossary Keeper authors the shared store,
   nothing else is needed — it wrote `INITIATIVE_DIR` directly. Re-seed step 1 so
   downstream readers in this and other phases pick up the new terms.
3. **Inherit works across fronts.** When a front consumes an upstream artefact, the
   orchestrator reads the upstream phase's `artifacts.canonical` from the index and
   hands that path to the Source Indexer to index into the consuming phase's
   `sources/` — so the Stage Inheritor still works purely within its `PHASE_DIR`.
4. **Record on freeze.** When a front freezes, update its `initiative.json` entry
   with `artifacts`, final `readiness`, and any `owes`, so the *next* front can read
   them.

This keeps strict phase isolation (the chosen model): the only component aware of
more than one phase at a time is the orchestrator.

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
   and write `initiative.json` with `status: open` (empty `definitions` and
   `phases`); create empty `glossary.md` and `decisions.md` at the root.
4. **Read the index.** Load `initiative.json` and note what prior fronts produced
   (`phases.*.produces` + `artifacts`), what they owe (`phases.*.owes`), and the
   shared `definitions`. This is how the front you are about to run becomes aware of
   all definitions and works on the initiative (see *The initiative as the index a
   new front reads*).
5. **Then resolve the phase.** `PHASE_DIR = INITIATIVE_DIR/<phase>` for the front
   you are running (`origination` for origination-brainstorm, `readiness` for
   readiness-package). **If `PHASE_DIR` already exists → RESUME it** (read
   `contract.lock.md`, `qa-log.md`, and the phase document, and continue — the
   *revisit* path). **If not → create it** and register the phase in
   `initiative.json.phases` (`started`, `state: active`, `consumes`). Never fork a
   second phase folder (`origination-2/`). Then **broker** the shared definitions
   into the phase (seed `PHASE_DIR/glossary.md` from the store) before spawning any
   reader.

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
