# Orchestration — PRD phases, agents, and what is reused

This skill is a **multi-agent pipeline** that extends the same engine as
origination-brainstorm, readiness-package, and tech-assessment. The conversation you
(the orchestrator) run is Layer 0 — the only layer that talks to the **PO** (owner of
the PRD) and, for the technical-half sign-off, the **CTO**. Everything else is a
specialized subagent you spawn with a focused prompt and tear down. This file is the
**narrative** view of *who runs when, who may write what, and what runs in parallel* in
the PRD flow; the **machine** view — validated ordering + the single-writer/single-decider
invariants — is declared in [`../pipeline.yaml`](../pipeline.yaml) and checked by
`tools/pipeline_graph.py` (see
[`../../tech-assessment/references/scheduling.md`](../../tech-assessment/references/scheduling.md)).
When the prose and the graph disagree, the graph wins.

The PRD is the **merge** of two frozen upstream artifacts: the **Readiness Package**
(product, PO) and the **Technical Assessment** (technical, CTO). It **stitches,
reconciles, and exposes** them to the PM — it **never re-authors either half**
(`personas/02-po.md` §2/§10/§11, `templates/04-prd.md`). It is the PRD — not the RP — that
opens the downstream.

## What this reuses (no duplication)

The following engine-level method documents apply **unchanged**. Do not copy their rules
here; cite and apply them:

| Reference | What it governs |
|---|---|
| [`../../origination-brainstorm/references/contract-and-template.md`](../../origination-brainstorm/references/contract-and-template.md) | Template annotation format (`origination:` markers, incl. `derived` + `inputs`), `contract.lock.md` derivation, template-hash restart policy |
| [`../../origination-brainstorm/references/ledger-schema.md`](../../origination-brainstorm/references/ledger-schema.md) | `qa-log.md` schema — `Q###` blocks, header summary, rationale/spawned-by fields |
| [`../../origination-brainstorm/references/initiatives.md`](../../origination-brainstorm/references/initiatives.md) | Initiatives root resolution, resolve-or-select, `.teamwork/<initiative>/` + phase-folder layout, works + definitions index, brokering |
| [`../../origination-brainstorm/references/writing-integrity.md`](../../origination-brainstorm/references/writing-integrity.md) | Single-writer rule, read-modify-write, queue/drain, `rev` marker, no-truncation sentinel |
| [`../../origination-brainstorm/references/grounding.md`](../../origination-brainstorm/references/grounding.md) | Quality calibration against the golden exemplar |
| [`../../origination-brainstorm/references/questioning-method.md`](../../origination-brainstorm/references/questioning-method.md) | Question rendering (`open` / `choice`), disposition routes, the `AskUserQuestion` protocol (fallback only — the PRD rarely asks) |
| [`../../readiness-package/references/escalation.md`](../../readiness-package/references/escalation.md) | The RP↔TA bridge (`TechAssessmentRef`) — how this skill reads whether a TA was owed, signed, or never requested |

**Carry-forwards that apply unchanged:** single-writer rule; read-modify-write;
initiative resolve-or-select; ledger schema; the `origination:` annotation marker.

## PRD-specific references

- [`merge.md`](merge.md) — the governing method: how the RP becomes Part A and the TA
  becomes Part B, authorship preservation, and the inherit-then-synthesize model.
- [`reconciliation.md`](reconciliation.md) — scope reconciliation, the consolidated risk
  view, the **no-escalation (RP-alone) path**, and the **veto halt** (no PRD on an
  `Infeasible as scoped` TA).
- [`inheritance.md`](inheritance.md) — the RP/TA → PRD section mapping: exactly which
  source section each PRD `id` is carried from.
- [`handoff.md`](handoff.md) — the PM Acceptance Gate, the dual sign-off, the
  `handoffReady` freeze gate, and the PM-rejection / version-bump loop.

## The agents you spawn (`subagent_type`)

The PRD reuses the **existing roster** — it introduces **no new agents** (the roster is
phase-agnostic; it specializes through the PRD template, guide, and references). The
merge maps cleanly onto three engine specialists already in the roster: the
**Inheritor** carries each half forward, the **Synthesizer** composes the `derived`
sections, and the **Reconciler** resolves the scope.

### Reused engine agents

| Agent | Writer? | When spawned |
|---|---|---|
| `hsb-template-validator` | read-only | Setup — audits the PRD template |
| `hsb-source-indexer` | **writer** (`sources/`, `sources-index.md`) | Setup, parallel after validator passes — indexes the **RP**, the **TA** (if escalated), and the **Intake Record** |
| `hsb-template-analyst` | **writer** (`contract.lock.md`) | Setup, parallel after validator passes |
| `hsb-stage-inheritor` | read-only proposer | Phase 2 — carries the RP forward into Part A and the TA forward into Part B; **fanned out one per part** |
| `hsb-synthesizer` | read-only proposer | Phase 3 — composes the `derived` sections (`exec-summary`, `consolidated-risk`, `inherited-readiness`) from the inherited halves; **fanned out one per derived section** |
| `hsb-reconciler` | read-only proposer | Phase 3 — produces `scope-reconciliation` (and resolves any RP↔TA conflict the Auditor flags) |
| `hsb-section-drafter` | read-only proposer | Phase 3 — drafts `handoff-gate` and any non-inherited prose; **fanned out one per `SECTION`** |
| `hsb-question-strategist` | read-only | Phase 4 confirm loop (**fallback only** — fired only on a genuine merge conflict or a missing source) |
| `hsb-evidence-extractor` | read-only | Confirm loop — satisfies an open question from the indexed RP / TA |
| `hsb-ledger-writer` | **writer** (`qa-log.md`) | Records questions, answers, proposed entries, and the sign-off |
| `hsb-doc-updater` | **writer** (`$DOC` = `prd.md`) | Sole writer of the PRD document |
| `hsb-glossary-keeper` | **writer** (initiative `glossary.md` + `decisions.md`) | Optional — records the PRD freeze + dual sign-off as a cross-phase decision; spawned with `DEFINITIONS_DIR` |
| `hsb-gap-reporter` | **writer** (`prd-report.md`) | Optional — live gap map for the PO |
| `hsb-confidence-auditor` | read-only | Confirm loop — re-scores sections (incremental via `SECTIONS`), flags conflicts/contradictions between the halves |
| `hsb-humanizer` | **writer** (`output/humanized.md`) | Phase 5 — must finish before translator/enricher/finalizer |
| `hsb-translator` | **writer** (`output/translated.<lang>.md`) | Phase 5, parallel |
| `hsb-visual-enricher` | **writer** (`output/enriched.md`) | Phase 5, parallel |
| `hsb-finalizer` | **writer** (`final/<project>-NNN.md`) | Phase 5, parallel — externalizes the clean, printable final |
| `hsb-packager` | **writer** (`output/manifest.md`) | Phase 5 (wrap) |

**`hsb-doc-updater` and `hsb-ledger-writer` are the only writers of `prd.md` and
`qa-log.md` respectively.** Every proposer above (Inheritor, Synthesizer, Reconciler,
Section Drafter, Auditor, Evidence Extractor, Question Strategist) is a **read-only
proposer** that returns structured proposals to you; you route them through the single
writers.

When spawning, inject the paths each agent needs: `SKILL_DIR`, `PHASE_DIR` (`prd/`),
`TEMPLATE` (`assets/target-template.prd.md`), `DOC` (`prd.md`), and the companion guide.
The Inheritor takes `PART` (`A` from the RP / `B` from the TA); the Synthesizer and
Section Drafter take `SECTION`; the Confidence Auditor takes `SECTIONS` (touched ids);
the Finalizer needs `PROJECT_SLUG` (from `initiative.json.project`). **Run independent
agents in the same turn** so they execute in parallel (Indexer ∥ Analyst at setup; the
Inheritor fan-out in Phase 2; the Synthesizer/Drafter/Reconciler fan-out in Phase 3;
Translator ∥ Visual Enricher ∥ Finalizer in Phase 5).

**You broker everything above `PHASE_DIR`** (the initiative-level `initiative.json`,
`glossary.md`, `decisions.md`). Read the works index to find the RP
(`artifacts.canonical`/`final` of the phase that `produces` `readiness-package`) and the
TA (the phase that `produces` `technical-assessment`), hand those to the Source Indexer;
seed the phase's read-only `PHASE_DIR/glossary.md`; spawn the Glossary Keeper with
`DEFINITIONS_DIR`; update the index when the front starts and freezes.

## Phase 0 — Locate the RP and the TA (you + the PO)

1. **Resolve-or-select the initiative** per
   [`initiatives.md`](../../origination-brainstorm/references/initiatives.md). The PRD
   runs as the **`prd/` phase** of that same initiative.
2. **Read `initiative.json` and discover the inputs from the works index.**
   - Find the phase whose `produces` is `readiness-package`; read its
     `artifacts.canonical` / `final` — that is the **linked RP**. It must be **frozen**
     (`state: frozen`). If no phase produces a `readiness-package`, say so and stop —
     there is nothing to merge.
   - Read the RP's `tech-assessment-ref` / the `phases.readiness.owes` entry to learn
     **whether a TA was owed**:
     - **`not_requested`** → **no-escalation path.** There is no TA; Part B is N/A. The
       PRD is `RP alone`. Proceed.
     - **owed and a phase `produces: technical-assessment` exists with the debt
       discharged `signed`** → **escalated path.** That phase's `artifacts.canonical` /
       `final` is the **linked TA**. Proceed with both halves.
     - **owed but the TA does not exist yet (debt still open)** → **stop.** The TA is a
       prerequisite — tell the PO to run `tech-assessment` first; the PRD cannot merge a
       half that has not been written.
     - **the TA was discharged `vetoed` (`Infeasible as scoped`)** → **stop — the veto
       halt.** There is no PRD on a veto: signal the PO to revise the RP scope and
       re-escalate. See [`reconciliation.md`](reconciliation.md) § The veto halt.
   - Also note the `intake/` phase's `intake-record.md` (for IDs and demand nature) and
     the shared `definitions`.
3. **Confirm output language** (default `en-US` when ambiguous; mirror the PO's
   language). Record it.

Do not ask a wall of questions here — select the initiative, resolve the RP + the TA
status, and confirm language.

## Phase 1 — Setup

1. **Resolve-or-resume the `prd/` phase** at `INITIATIVE_DIR/prd/`. Register it in
   `initiative.json.phases` (`started`, `state: active`,
   `consumes: ["readiness-package", "technical-assessment", "intake-record"]` — drop
   `technical-assessment` from `consumes` on the no-escalation path — `produces: "prd"`).
   Seed the brokered `PHASE_DIR/glossary.md`. Inject
   `TEMPLATE = assets/target-template.prd.md`, `DOC = prd.md`.
2. **`hsb-template-validator`** audits the PRD template; proceed once it passes.
3. Spawn **in the same turn** (independent → parallel):
   - **`hsb-source-indexer`** indexes the **RP** (primary product source) and the **TA**
     (primary technical source, when escalated), **plus the Intake Record** — into
     `prd/sources/`.
   - **`hsb-template-analyst`** derives `contract.lock.md` from the PRD template
     (hash-locked; restarts + supersedes stale ledger entries on a hash change).

Gate: `contract.lock.md` exists and the RP (+ TA, when escalated) are indexed.

## Phase 2 — Inherit both halves (carry forward, do not rewrite)

Spawn **`hsb-stage-inheritor` once per part, in the same turn** (independent → parallel):

- **`PART: A`** — carries the **frozen RP** forward into the Part A sections
  (`a-objectives`, `a-scope`, `a-personas`, `a-journey`, `a-business-rules`,
  `a-user-stories`, `a-nfrs`, `a-edge-cases`) at preserved confidence, tagged
  `Origin: inherited`. **Summaries, not copies** — the full RP stays the source. See
  [`inheritance.md`](inheritance.md).
- **`PART: B`** — when **escalated**, carries the **signed TA** forward into the Part B
  sections (`b-feasibility`, `b-nature-landscape`, `b-arch-impact`, `b-nfr-feasibility`,
  `b-alternatives`, `b-hard-constraints`, `b-adrs`) at preserved confidence, tagged
  `Origin: inherited`. The verdict is **carried, never re-decided**. When **not
  escalated**, the Inheritor instead returns the honest-N/A dispositions for every Part B
  section (`Disposition: decided`, "N/A — no architectural escalation").

Also carry forward `effort-cost` (firm from TA, or preliminary from RP) and
`success-metrics` (from the RP). Route all proposals through `hsb-ledger-writer` →
`hsb-doc-updater`.

At the end of Phase 2, both halves are present — Part A from the RP, Part B from the TA
(or N/A-disposed). The PO/CTO never face a blank Part A/B.

## Phase 3 — Synthesize & reconcile (the PRD's own work)

Spawn **in the same turn** (independent → parallel):

1. **`hsb-reconciler`** → `scope-reconciliation`: compares the RP scope (`a-scope`)
   against the TA verdict/caveats (`b-feasibility`) and hard constraints
   (`b-hard-constraints`). Records what changed (or "RP scope maintained in full") and,
   if anything changed, **proposes the reconciled `a-scope`** so Part A reflects the
   final scope. See [`reconciliation.md`](reconciliation.md).
2. **`hsb-synthesizer`**, fanned out one per derived section:
   - `SECTION: consolidated-risk` — merges the RP's product/business risks with the TA's
     technical risks into one tagged table + explicit external dependencies.
   - `SECTION: inherited-readiness` — carries forward the open assumptions / Discovery
     unknowns / delegated answers from the RP/TA dispositions.
   - `SECTION: exec-summary` — composes the 2–4 paragraph one-pager (run **after** Part A,
     Part B, and `effort-cost` exist so it summarizes settled content).
3. **`hsb-section-drafter`** → `SECTION: handoff-gate`: drafts the delivery checklist + the
   priority/business context (the boxes are asserted, not invented — each must be checkable
   from the merged document).

Route all proposals to the single `hsb-doc-updater`. The synthesized sections arrive
`Origin: synthesized` at partial confidence with a hint.

At the end of Phase 3 every section has an entry — `inherited`, `synthesized`, or
`decided` (the N/A Part B path) — so neither the PO nor the CTO faces a blank form.

## Phase 4 — Confirm loop (until handoffReady)

Repeats until the freeze gate clears:

1. **`hsb-confidence-auditor`** (read-only) re-scores against the rubric, **flags
   contradictions between the two halves** (e.g. an NFR in A.7 with no matching B.4 row,
   or a scope item the TA constrained but `a-scope` still lists unchanged), and returns
   the gap verdict. First pass scores every section; later passes take `SECTIONS` (ids
   touched since the last audit).
   - On a flagged contradiction: spawn **`hsb-reconciler`** (read-only); route to
     `hsb-ledger-writer` → `hsb-doc-updater`.
   - Optional: spawn **`hsb-gap-reporter`** for a live gap map.
2. **`hsb-question-strategist`** (read-only, **fallback only**) — the PRD rarely asks,
   because both halves are frozen. A question fires only when the Auditor surfaces a
   genuine conflict the sources cannot settle, or a source section is missing.
3. The **PO** reviews the merged document and confirms the product half (Part A,
   `scope-reconciliation`, `consolidated-risk`, `inherited-readiness`, `success-metrics`,
   `exec-summary`, `handoff-gate`); the **CTO** co-signs the technical half (Part B,
   `effort-cost` when firm) and the feasibility verdict carried into `sign-off`. Each
   confirmation is recorded by **`hsb-ledger-writer`** (serial).
4. **`hsb-doc-updater`** promotes confirmed entries: `inherited` / `synthesized` →
   `po_authored` (product half) / `cto_authored` (technical half), raising confidence to
   reflect the sign-off.
5. **Gate check:** `handoffReady = true` when:
   - `sign-off` is committed (PO: RP frozen; CTO: signed verdict **or** honest N/A), **and**
   - every other `blocksFreeze` section is resolved (`po_authored` / `cto_authored` /
     confirmed-`inherited`) or honestly disposed (`decided` N/A for the Part B no-escalation
     path), **and**
   - `scope-reconciliation` is recorded and `a-scope` reflects the reconciled result, **and**
   - the `handoff-gate` checklist is fully checkable from the document.

See [`handoff.md`](handoff.md) for the full gate and the PM-rejection loop.

## Phase 5 — Production & wrap

Once `handoffReady`:

1. **`hsb-humanizer`** writes `output/humanized.md` — the canonical clean copy all
   production agents read. Must finish first.
2. Then spawn **in the same turn** (parallel, distinct files):
   - **`hsb-translator`** → `output/translated.<lang>.md` (the confirmed output language).
   - **`hsb-visual-enricher`** → `output/enriched.md` (the consolidated risk table, the
     scope-reconciliation diff, the effort breakdown, an A→B NFR-feasibility map).
   - **`hsb-finalizer`** → `final/<project>-NNN.md` — the clean, **printable final
     deliverable** (strips authoring scaffold; counter-suffixed; idempotent). Inject
     `PROJECT_SLUG`.
3. **`hsb-packager`** writes `output/manifest.md`: the sign-off status (Accepted by PM /
   In PM Review / Returned), the escalation flag (RP+TA / RP alone), the feasibility
   verdict carried from the TA, open dispositions, template hash/version, the handoff note
   to the **PM** (this PRD opens the downstream), and an index entry for the Finalizer's
   `final/` deliverable.
4. **Record the front in the initiative index.** Update this phase's `initiative.json`
   entry: `state: frozen`, the `artifacts` paths (incl. `canonical: prd/output/humanized.md`
   and `final: prd/final/<project>-NNN.md`), `produces: prd`, the escalation flag, and the
   carried feasibility verdict. Push a `downstream-ready` / `delivered-to-pm` signal so the
   next front (PM execution planning) reads that the PRD is the open artifact.
5. Report to the PO (and CTO when escalated): the PRD is assembled, the sign-off status,
   the artifacts produced, and any open `assumption` / `discovery` disposition the PM must
   see before planning.

## The phase folder layout

The PRD lives in the `prd/` phase, beside the `readiness/` and `assessment/` phases it
merges:

```
INITIATIVE_DIR/                  # shared by every front
├── initiative.json             # orchestrator — works + definitions index
├── glossary.md                 # Glossary Keeper — shared canonical terms
├── decisions.md                # Glossary Keeper — shared cross-phase decisions (incl. the PRD freeze + dual sign-off)
├── origination/                # the upstream origination-record
├── intake/                     # the Intake Record (IDs + demand nature)
├── readiness/                  # the Readiness Package (Part A source)
├── assessment/                 # the Technical Assessment (Part B source — when escalated)
└── prd/                        # PHASE_DIR for the merge
    ├── contract.lock.md        # hsb-template-analyst
    ├── sources-index.md        # hsb-source-indexer
    ├── sources/                # hsb-source-indexer (incl. RP + TA + intake-record)
    ├── qa-log.md               # hsb-ledger-writer
    ├── prd.md                  # hsb-doc-updater (PRD-YYYY-NNN)
    ├── glossary.md             # brokered read-only copy of the initiative glossary
    ├── prd-report.md           # hsb-gap-reporter (optional)
    ├── output/
    │   ├── humanized.md        # hsb-humanizer
    │   ├── translated.<lang>.md # hsb-translator
    │   ├── enriched.md         # hsb-visual-enricher
    │   └── manifest.md         # hsb-packager
    └── final/                  # hsb-finalizer — clean, printable final deliverable(s)
        └── <project>-NNN.md    # externalized, scaffolding-stripped, counter-suffixed
```
