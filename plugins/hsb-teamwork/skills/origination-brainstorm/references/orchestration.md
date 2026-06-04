# Orchestration — phases, agents, and the single-writer guarantee

This skill is a **multi-agent pipeline**. The conversation you (the orchestrator)
run is **Layer 0** — the only layer that talks to the human. Everything else is a
**specialized subagent** you spawn with a focused prompt and tear down. This file
is the authoritative spec for *who runs when, who may write what, and what runs
in parallel*.

## The one rule that makes parallelism safe

**Every mutable file has exactly one writer agent.** Every other agent is
**read-only** and returns *proposals / findings / verdicts* to you (the
orchestrator), and **you** route them to the single writer. Two agents never hold
the pen on the same file, so concurrent writes are impossible by construction.

| Artifact | Sole writer | Everyone else |
|---|---|---|
| `contract.lock.md` | Template Analyst | read-only |
| `sources/`, `sources-index.md` | Source Indexer | read-only |
| `qa-log.md` | Ledger Writer | read-only |
| `target-document.md` | Doc Updater | read-only |
| `<initiative>/glossary.md`, `<initiative>/decisions.md` | Glossary Keeper | read-only |
| `readiness-report.md` | Gap Reporter | read-only |
| `output/humanized.md` | Humanizer | read-only |
| `output/translated.<lang>.md` | Translator | read-only |
| `output/enriched.md` | Visual Enricher | read-only |
| `final/<project>-NNN.md` | Finalizer | read-only |
| `output/manifest.md` | Packager | read-only |
| `<initiative>/initiative.json` | Orchestrator (you) | read-only |

The last two rows are **initiative-level** (above any `PHASE_DIR`): the shared
definitions store and the works+definitions index. Phase agents never reach up to
them — the orchestrator brokers reads down into each phase and the Glossary Keeper
is the one agent it hands the store path (`DEFINITIONS_DIR`) to. See
[`initiatives.md`](initiatives.md) §§ *Shared definitions* and *Brokering*.

**Serialize, queue, and merge — never clobber.** Beyond one-writer-per-file: you
never spawn two writers on the *same* file at once, you **queue** pending changes
and drain them through that single writer in one commit pass (nothing is dropped),
and every writer does **read-modify-write** (re-read the file, merge the batch
keyed by stable id, bump the `rev` marker) so no change is lost and overlapping
edits surface as conflicts for the Reconciler rather than silent overwrites. The
full protocol — queue, RMW, merge, conflict handling, the `rev` marker, and the
no-truncation rules — is in
[`writing-integrity.md`](writing-integrity.md); every writer agent reads it.

## Paths are passed in, never hardcoded (portability)

The skill ships in the **`hsb-teamwork` plugin** and is repo-independent. Its
base directory varies by install (the plugin cache, or `.claude/skills/...` when
symlinked in-repo), so you inject paths into every agent's spawn prompt — never let
an agent assume a location:

- `SKILL_DIR` — this skill's base directory (you are told it at launch).
- `PHASE_DIR` — `<INITIATIVE_DIR>/origination/`, resolved per [`initiatives.md`](initiatives.md) (resume if it exists). The origination front of the selected initiative.
- `TEMPLATE` — the target template file (default: `SKILL_DIR/assets/target-template.origination-record.md`, or a user-supplied template).
- `DEFINITIONS_DIR` — `<INITIATIVE_DIR>` — injected to the **Glossary Keeper only**,
  the sole writer of the shared `glossary.md` + `decisions.md`. No other agent
  receives it; readers get the brokered `PHASE_DIR/glossary.md` instead.

## The phase folder

Resolve-or-select the **initiative** at the start of every run, then resolve its
**origination phase** folder (see [`initiatives.md`](initiatives.md)):
`TEAMWORK_ROOT` anchors at `$TEAMWORK_HOME` or the project (git) root + `/.teamwork`,
**not** the cwd. You select the open initiative to run in (or start a new one), and
the origination front lives at `INITIATIVE_DIR/origination/`. If that phase folder
already exists you **resume** it rather than creating a duplicate.

```
<INITIATIVE_DIR>/
├── initiative.json           # Orchestrator — works + definitions index
├── glossary.md               # Glossary Keeper — shared canonical terms (one per initiative)
├── decisions.md              # Glossary Keeper — shared cross-phase decisions
└── origination/              # PHASE_DIR for this front
    ├── contract.lock.md      # Template Analyst
    ├── sources-index.md      # Source Indexer
    ├── sources/              # Source Indexer (copies/links of inputs)
    ├── qa-log.md             # Ledger Writer
    ├── target-document.md    # Doc Updater
    ├── glossary.md           # brokered read-only copy of the initiative glossary
    ├── readiness-report.md   # Gap Reporter
    ├── output/               # Humanizer · Translator · Enricher · Packager
    └── final/                # Finalizer — the clean, printable final deliverable(s)
        └── <project>-NNN.md  # externalized, scaffolding-stripped, counter-suffixed
```

## Phase 0 — Origination (you + the human)

Collect, in the human's language: the opening statement, any **file references**,
the **desired output language(s)**, and (optional) a custom `TEMPLATE`. Decide the
**mode**: *fresh* (no `target-document.md` yet) or *revisit* (one exists — re-score
it). **Resolve-or-select** the initiative, then its origination `PHASE_DIR`
([`initiatives.md`](initiatives.md)): confirm the latest open initiative or pick
from the open list (or start a new one); **read `initiative.json`** to take in what
prior fronts defined, produced, and owe; if that initiative's `origination/` phase
already exists, resume it instead of creating a second one, otherwise register it in
the index. Seed the brokered `PHASE_DIR/glossary.md` from the initiative store
before spawning readers. Do not ask a wall of questions yet.

## Phase 1 — Setup (parallel, then gate)

First, **Template Validator** checks the template against the audit checklist;
proceed only once it passes (fix the template otherwise). Then spawn **in the same
turn** (independent → parallel):
- **Source Indexer** — only if files were referenced. Normalizes them into
  `sources/` and writes `sources-index.md`.
- **Template Analyst** — derives `contract.lock.md` (sections, rubrics, `blocks`,
  `min-confidence`) from the validated template and records the **template hash**.
  If a prior `contract.lock.md` exists with a *different* hash → it restarts
  analysis (see `contract-and-template.md` § Restart).

Gate: `contract.lock.md` must exist before looping.

## Phase 2 — Capture loop (iterate until the gate clears)

Each iteration:

1. Spawn **in the same turn** (both read-only proposers → parallel):
   - **Question Strategist** — reads contract + `qa-log.md` + `target-document.md`,
     returns the next batch of questions (≈1–3, one theme) each with rationale, the
     section it targets, a **`mode`** (`open` | `choice`), and — for `choice`
     questions — 2–4 hypothesis `options`, aimed at the lowest-confidence
     **blocking** gaps.
   - **Evidence Extractor** — reads `sources/` + `qa-log.md` + contract, returns
     *proposed answers* to open questions it can satisfy from the files
     (`inferred`, with `source` + confidence).
2. **Ledger Writer** (serial) commits: the new questions+rationale, and any
   file-derived proposed answers.
3. **You** present to the human only the questions *not* already satisfied by File
   Extraction, **rendering each by its `mode`** (see `questioning-method.md` §
   *Rendering the questions*): `open` questions as free-text prose; `choice`
   questions via `AskUserQuestion` — the Strategist's hypotheses as options, the
   disposition hatches appended, "Other" for the open answer, `multiSelect` where
   several apply. Collect answers (the chosen option label / `Other:` text, or the
   prose reply). Hand them to the **Ledger Writer** to record, including which option
   was picked and the disposition it maps to. An answer may spawn follow-up questions
   → Strategist proposes, Ledger Writer records them with `spawned-by`.
4. **Doc Updater** (serial) fills/updates the `capture` sections of
   `target-document.md` from the committed answers, preserving each section's
   confidence/disposition line. For `derived` sections (executive summary, triage
   draft), spawn the **Synthesizer** (read-only) to compose them from their declared
   `inputs` at a confidence bounded by those inputs, then route its proposals back to
   the Doc Updater, which writes them. (Skip it for trivial templates with no derived
   sections — the Doc Updater can compose inline.)
5. **Confidence Auditor** (read-only) re-scores sections against their rubric,
   checks the document for truncation, **flags** conflicts (it does not resolve
   them), and returns the **gap verdict** + readiness score. **Audit incrementally:**
   on the *first* audit it scores every section; on later loop iterations inject
   `SECTIONS` — the ids touched since the last audit (filled, answered, or
   reconciled) — so it re-scores **only those** and re-checks the gate using their
   new verdicts plus the carried-forward verdicts of the untouched sections. This is
   what keeps each loop iteration cheap; full re-grades of a settled document are the
   main avoidable cost in a long run.
   - On a flagged conflict, spawn the **Reconciler** (read-only): it recommends
     which value to keep (or a disambiguating question); you route that to the
     Ledger Writer.
   - To show the human where things stand and to keep terminology canonical, the
     **Gap Reporter** (writes `readiness-report.md`) and the **Glossary Keeper**
     (writes the shared store) read disjoint-from-each-other inputs and write
     **distinct files**, so when both are due you spawn them **in the same turn**
     (parallel). Spawn the **Gap Reporter** for the live gap map; and
   - when domain terms or cross-phase decisions accumulate (typically after the
     first capture rounds, and again before production), spawn the **Glossary
     Keeper** with `DEFINITIONS_DIR` injected: it reads `qa-log.md` and
     `target-document.md` and writes canonical terms to the initiative's shared
     `glossary.md` (and cross-phase decisions to `decisions.md`). You then **re-seed**
     the brokered `PHASE_DIR/glossary.md` so the **Doc Updater** (this phase) and the
     **Humanizer** and **Translator** (Phase 3) read the refreshed terms — and so do
     later fronts. Terminology never drifts because it is defined once, at the
     initiative. Optional for trivial demands with no special vocabulary.
6. Gate check: **stop** when every `blocks=true` section is either ≥ its
   `min-confidence` *or* honestly disposed (`assumption`/`discovery`/`deferred`).
   Otherwise loop — Strategist's next batch targets the Auditor's flagged gaps.

Parallelism inside the loop: Strategist ∥ Extraction (read-only proposers) go out
in **one turn**; likewise Gap Reporter ∥ Glossary Keeper (distinct files) when both
are due. Ledger Writer → Doc Updater run **serially** (each is a single-writer).
The Auditor is read-only after, and re-scores only the touched `SECTIONS` once the
document has settled — so later iterations cost a fraction of the first.

## Phase 3 — Production (isolated context, parallel variants)

Once the gate clears, hand off to isolated agents that need only the final doc —
this keeps your context lean ("isolate when satisfied"):

1. **Humanizer** writes `output/humanized.md` (must finish first — it is the
   canonical clean copy the others read).
2. Then spawn **in the same turn** (parallel variants, distinct files):
   - **Translator** → `output/translated.<lang>.md` for each requested language.
   - **Visual Enricher** → `output/enriched.md`.
   - **Finalizer** → `final/<project>-NNN.md` — the clean, **printable final
     deliverable**. It reads the canonical `output/humanized.md`, strips every
     authoring scaffold (HTML comments + `origination:` annotations, the rev/END
     markers, rubric/guidance blockquotes, and the per-section
     `Confidence/Source/Status/Disposition/Hint` lines), keeps all substantive
     content and ⚠️ warnings, and externalizes it under `final/` named
     `<PROJECT_SLUG>-<NNN>.md` (zero-padded per-phase counter; idempotency guard
     skips a new counter when the deliverable is unchanged). Inject `PROJECT_SLUG`
     (from `initiative.json.project`). This is the clearly-final document a human
     prints or hands off.

   *(Per project choice: translated, enriched, and the final deliverable are
   independent of each other; only the Finalizer's externalized copy is the
   printable final.)*

## Phase 4 — Wrap

- **Packager** assembles `output/`, writes `output/manifest.md` (artifact index,
  readiness score, open dispositions, template hash/version). It indexes the
  Finalizer's `final/<project>-NNN.md` deliverable too, marked as the printable
  final.
- **Record the front in the initiative index.** Update this phase's
  `initiative.json` entry: `state: frozen`, final `readiness`, the `artifacts` paths
  (including `canonical: origination/output/humanized.md` — the copy downstream
  fronts inherit — and `final: origination/final/<project>-NNN.md`, the printable
  deliverable), `produces: origination-record`, and any `owes`. This is what lets a
  later front (e.g. readiness) discover and inherit this work by reading one file.
- You report to the human: what was produced, the readiness score, and every item
  still parked as assumption/discovery/deferred.

## The full roster (each a standalone agent)

- **Setup:** Template Validator, Source Indexer, Template Analyst.
- **Loop:** Question Strategist, Evidence Extractor, Reconciler, Synthesizer
  (read-only proposers); Ledger Writer, Doc Updater, Glossary Keeper, Gap Reporter
  (writers); Confidence Auditor (read-only gate).
- **Production:** Humanizer, then Translator ∥ Visual Enricher ∥ Finalizer.
- **Wrap:** Packager.

Every writer obeys the single-writer + serialize/queue/merge/RMW rules in
`writing-integrity.md`. Add any future capability as its own agent under the same
rules rather than overloading an existing one.
