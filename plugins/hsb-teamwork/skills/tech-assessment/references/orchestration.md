# Orchestration — TA phases, agents, and what is reused

This skill is a **multi-agent pipeline** that extends the same engine as
origination-brainstorm and readiness-package. The conversation you (the
orchestrator) run is Layer 0 — the only layer that talks to the **CTO**.
Everything else is a specialized subagent you spawn with a focused prompt and
tear down. This file is the **narrative** view of *who runs when, who may write
what, and what runs in parallel* in the tech-assessment flow. The **machine** view —
the authoritative, validated ordering — is declared in
[`../pipeline.yaml`](../pipeline.yaml) and checked by `tools/pipeline_graph.py`; see
[`scheduling.md`](scheduling.md). When the prose and the graph disagree, the graph
wins and the prose is the bug. In particular, the parallel batches, the single-writer
and single-decider invariants, and the **provisional-then-reconcile** handling of the
draft-pass proposers (effort/ADRs drafted before the verdict) are derived from the
graph, not hand-maintained here.

The TA is the **CTO's** artefact — the persona's *technical-strategy* mandate
(`personas/03-cto.md` §2). It **responds** to the Readiness Package and is authored
**alone**; it **never edits the RP** (`personas/03-cto.md` §1/§10, `personas/02-po.md`
§2/§10, `interactions/05-po-to-cto.md`). It may **veto** feasibility — then the PO
revises the RP scope and re-escalates (see [`feasibility.md`](feasibility.md)).

## What this reuses (no duplication)

The following engine-level method documents apply **unchanged**. Do not copy their
rules here; cite and apply them:

| Reference | What it governs |
|---|---|
| [`../../origination-brainstorm/references/contract-and-template.md`](../../origination-brainstorm/references/contract-and-template.md) | Template annotation format (`origination:` markers), `contract.lock.md` derivation, template-hash restart policy |
| [`../../origination-brainstorm/references/ledger-schema.md`](../../origination-brainstorm/references/ledger-schema.md) | `qa-log.md` schema — `Q###` blocks, header summary, rationale/spawned-by fields |
| [`../../origination-brainstorm/references/initiatives.md`](../../origination-brainstorm/references/initiatives.md) | Initiatives root resolution, resolve-or-select, `.teamwork/<initiative>/` + phase-folder layout, works + definitions index, brokering |
| [`../../origination-brainstorm/references/writing-integrity.md`](../../origination-brainstorm/references/writing-integrity.md) | Single-writer rule, read-modify-write, queue/drain, `rev` marker, no-truncation sentinel |
| [`../../origination-brainstorm/references/grounding.md`](../../origination-brainstorm/references/grounding.md) | Quality calibration against the golden exemplar |
| [`../../origination-brainstorm/references/questioning-method.md`](../../origination-brainstorm/references/questioning-method.md) | Question rendering (`open` / `choice`), disposition routes, the `AskUserQuestion` protocol |
| [`../../readiness-package/references/escalation.md`](../../readiness-package/references/escalation.md) | The RP↔TA bridge (`TechAssessmentRef`), the architectural trigger list, and the handoff this skill consumes |

**Carry-forwards that apply unchanged:** single-writer rule; read-modify-write;
initiative resolve-or-select; ledger schema; the `origination:` annotation marker
(the engine's contract grammar — unchanged even in the TA template).

## The agents you spawn (`subagent_type`)

### Reused engine agents

Phase-agnostic specialists (`hsb-*`), shared with the other skills. They specialize
through the TA template and guide, not through code changes.

| Agent | Writer? | When spawned |
|---|---|---|
| `hsb-template-validator` | read-only | Setup — audits the TA template |
| `hsb-source-indexer` | **writer** (`sources/`, `sources-index.md`) | Setup, parallel after validator passes — indexes the RP, the Intake Record, and the `tech-landscape` (if it exists) |
| `hsb-template-analyst` | **writer** (`contract.lock.md`) | Setup, parallel after validator passes |
| `hsb-stage-inheritor` | read-only proposer | Phase 2 — carries RP/Intake material forward into the TA's inheritable sections |
| `hsb-section-drafter` | read-only proposer | Phase 3 (draft pass) — proposes `ai_drafted` technical sections; **fanned out one per `SECTION`** |
| `hsb-question-strategist` | read-only | Phase 2 (CTO-priority questions) and Phase 4 confirm loop (fallback) |
| `hsb-evidence-extractor` | read-only | Confirm loop — satisfies open questions from the indexed RP / tech-landscape |
| `hsb-reconciler` | read-only | Confirm loop — on conflicts (e.g. RP asserted X, the technical lens says Y) |
| `hsb-ledger-writer` | **writer** (`qa-log.md`) | Records questions, answers, proposed entries |
| `hsb-doc-updater` | **writer** (`$DOC` = `technical-assessment.md`) | Sole writer of the TA document |
| `hsb-glossary-keeper` | **writer** (initiative `glossary.md`) | Optional — canonical terms; spawned with `DEFINITIONS_DIR` |
| `hsb-decisions-keeper` | **writer** (initiative `decisions.md`) | Optional — records the feasibility verdict + hard constraints as cross-phase decisions; spawned with `DEFINITIONS_DIR` |
| `hsb-gap-reporter` | **writer** (`assessment-report.md`) | Optional — gap map for the CTO |
| `hsb-confidence-auditor` | read-only | Confirm loop — re-scores sections (incremental via `SECTIONS`), flags conflicts |
| `hsb-integrity-checker` | read-only | Confirm loop — mechanically verifies the TA is complete/untruncated (sentinel, no elision) |
| `hsb-language-auditor` | read-only | Phase 5 — verifies the humanized copy for language leaks; leaks route back to the Humanizer |
| `hsb-humanizer` | **writer** (`output/humanized.md`) | Phase 5 — must finish before translator/enricher |
| `hsb-translator` | **writer** (`output/translated.<lang>.md`) | Phase 5, parallel with visual-enricher |
| `hsb-visual-enricher` | **writer** (`output/enriched.md`) | Phase 5, parallel with translator |
| `hsb-finalizer` | **writer** (`final/<project>-NNN.md`) | Phase 5, parallel with translator/enricher — externalizes the clean, printable final |
| `hsb-packager` | **writer** (`output/manifest.md`) | Phase 5 (wrap) |

### Stage-specific agents this skill drives (the CTO roster)

Named for their function. The tech-assessment skill is their first consumer; later
stages may reuse them.

| Agent | Writer? | When spawned |
|---|---|---|
| `hsb-tech-classifier` | read-only proposer | **Phase 2** — confirms the demand nature under the technical lens, resolves the KB, and sets which path is required; the **governing** proposer (see [`classification.md`](classification.md)) |
| `hsb-feasibility-assessor` | read-only proposer | **Phase 3/4** — proposes the feasibility verdict (the CTO's first-class decision) and the veto path; the **gate** proposer (see [`feasibility.md`](feasibility.md)) |
| `hsb-adr-proposer` | read-only proposer | Phase 3 — arrives with suggested ADRs (reused from the KB where possible); the CTO approves/adjusts |
| `hsb-effort-estimator` | read-only proposer | Phase 3 — proposes the firm effort/cost decomposition |
| `hsb-landscape-keeper` | **writer** (`tech-landscape-<system>.md`) | Phase 4/5 — greenfield: **seeds** a new tech-landscape from the foundational ADRs; brownfield: **references/updates** it with what is specific to this demand |

**`hsb-doc-updater` and `hsb-ledger-writer` are the only writers of
`technical-assessment.md` and `qa-log.md` respectively.** Every CTO proposer above
(except the landscape-keeper, which owns the *persistent* `tech-landscape`, a
different file) is a read-only proposer that returns structured proposals to the
orchestrator, who routes them through the single writers.

When spawning, inject the paths each agent needs: `SKILL_DIR`, `PHASE_DIR`
(`assessment/`), `TEMPLATE` (`assets/target-template.technical-assessment.md`),
`DOC` (`technical-assessment.md`), and the companion guide. The Section Drafter also
takes `SECTION`; the Confidence Auditor takes `SECTIONS` (touched ids); the
Finalizer needs `PROJECT_SLUG` (from `initiative.json.project`); the Landscape
Keeper takes `LANDSCAPE_PATH` (the `tech-landscape-<system>.md` to seed or update)
and `NATURE`. **Run independent agents in the same turn** so they execute in
parallel (Indexer ∥ Analyst at setup; the Drafter fan-out in Phase 3; Translator ∥
Visual Enricher ∥ Finalizer in Phase 5).

**You broker everything above `PHASE_DIR`** (the initiative-level `initiative.json`,
`glossary.md`, `decisions.md`, and the persistent `tech-landscape`). Agents stay
`PHASE_DIR`-scoped except the Landscape Keeper, which writes the initiative/repo-level
`tech-landscape` you point it at.

## Phase 0 — Locate the RP (you + the CTO)

1. **Resolve-or-select the initiative** per
   [`initiatives.md`](../../origination-brainstorm/references/initiatives.md). The TA
   runs as the **`assessment/` phase** of that same initiative.
2. **Read `initiative.json` and discover the inputs from the works index.** Find the
   phase whose `produces` is `readiness-package` and read its `artifacts.canonical` /
   `final` — that path is the **linked RP**; do not assume `readiness/`. Also read the
   `intake/` phase's `intake-record.md` (for the demand nature + KB classification),
   and check `phases.*.owes` for the **`TechAssessmentRef` debt** the RP pushed (the
   signal that a TA is owed — this skill is what discharges it). Note the shared
   `definitions` and any existing `tech-landscape`. If no phase produces a
   `readiness-package`, say so and stop — there is nothing to assess.
3. **Confirm the TA is actually owed.** The RP must carry an escalation
   (`tech-assessment-ref` = requested/deferred). If the RP froze with
   `Status: not_requested`, there is no architectural impact and **no TA is needed** —
   say so and stop (`templates/03-technical-assessment.md` § "When there is NO TA").
4. **Confirm output language** (default `en-US` when ambiguous; mirror the CTO's language). Record it.

Do not ask a wall of questions here — select the initiative, confirm the RP + the
owed escalation, and confirm language.

## Phase 1 — Setup

1. **Resolve-or-resume the `assessment/` phase** at `INITIATIVE_DIR/assessment/`.
   Register it in `initiative.json.phases` (`started`, `state: active`,
   `consumes: ["readiness-package", "intake-record"]`, `produces: "technical-assessment"`).
   Seed the brokered `PHASE_DIR/glossary.md`. Inject
   `TEMPLATE = assets/target-template.technical-assessment.md`,
   `DOC = technical-assessment.md`.
2. **`hsb-template-validator`** audits the TA template; proceed once it passes.
3. Spawn **in the same turn** (independent → parallel):
   - **`hsb-source-indexer`** indexes the **RP** (the `artifacts.canonical` / `final`
     path) as the primary source, **plus the intake-record** (for the demand nature +
     KB) and the **`tech-landscape`** if one exists — into `assessment/sources/`.
   - **`hsb-template-analyst`** derives `contract.lock.md` from the TA template
     (hash-locked; restarts + supersedes stale ledger entries on a hash change).

Gate: `contract.lock.md` exists and the RP + Intake are indexed.

## Phase 2 — Classify & inherit (the governing decision first)

1. Spawn **`hsb-tech-classifier`** (read-only). It inherits the demand nature
   (Greenfield / Brownfield / Hybrid) and the KB reference from the **Intake
   Record**, **confirms them under the technical lens**, and proposes the
   `tech-classification` entry: the nature, the **path to fill**, and the KB
   resolution (`Exists` / `Partial` / `Does not exist → Discovery`). Ask the CTO **only
   what the classifier could not settle** (CTO-priority questions, engine
   `open`/`choice` protocol). Route the confirmed classification through
   `hsb-ledger-writer` → `hsb-doc-updater`. See [`classification.md`](classification.md).
   - **This decision governs the rest of the run:** it determines which of
     `current-state` / `tech-foundation` is a required (blocking) section and which is
     the honest-N/A `Disposition: decided` entry.
   - If the KB does **not** exist (brownfield/hybrid), record a documentation
     **Discovery spike** in `discovery-path` and plan to run `hsb-landscape-keeper` to
     create it (Phase 4/5).
2. Spawn **`hsb-stage-inheritor`** (read-only). It carries the RP/Intake material
   forward into the TA's inheritable sections — see [`inheritance.md`](inheritance.md)
   — tagged `Origin: inherited` at preserved confidence. Route proposals through
   `hsb-ledger-writer` → `hsb-doc-updater`.

## Phase 3 — Draft pass (fan-out) + the verdict proposal

1. Spawn **`hsb-section-drafter`** **once per technical section, all in the same turn**
   (independent → parallel), each injected with a single `SECTION` — drafting only the
   sections the classification put **in force**:
   - the path section(s): `current-state` (brownfield/hybrid) and/or `tech-foundation`
     (greenfield/hybrid); dispose the non-applicable path `decided` N/A;
   - `affected-systems` ∥ `architectural-impact` ∥ `integrations` ∥ `alternatives` ∥
     `nfr-feasibility` (one row per RP §8 NFR) ∥ `testability-observability` ∥
     `hard-constraints` ∥ `tech-risks` ∥ `build-vs-buy`.
   Each is a read-only proposer returning drafts for **its one section** at
   `Origin: ai_drafted`, partial confidence, with a hint. Route all to the single
   `hsb-doc-updater`.
2. Spawn **in the same turn** (independent → parallel) the specialized proposers:
   - **`hsb-adr-proposer`** → suggested ADRs (reused from the KB where possible,
     `Origin: reused_from_KB`); route to `hsb-doc-updater`.
   - **`hsb-effort-estimator`** → the firm `effort-cost` decomposition; route to
     `hsb-doc-updater`.
3. Once the impact/risk/NFR sections exist, spawn **`hsb-feasibility-assessor`**
   (read-only). It reads the drafted architectural impact, NFR feasibility, risks, and
   constraints and proposes the **feasibility verdict** with rationale (and, if
   warranted, the **veto** — `Infeasible as scoped`). Route to `hsb-doc-updater`. See
   [`feasibility.md`](feasibility.md).

At the end of Phase 3 every in-force section has an entry — `inherited`, `ai_drafted`,
`reused_from_KB`, or `decided` (N/A path / "none") — so the CTO never faces a blank
form.

## Phase 4 — Confirm loop (until signOffReady)

Repeats until the freeze gate clears:

1. **`hsb-confidence-auditor`** (read-only) re-scores against the rubric, flags
   conflicts, returns the gap verdict. First pass scores every section; later passes
   take `SECTIONS` (ids touched since the last audit) and re-score only those. Its
   verdict is the **single source** of the readiness number (`readiness` + `as-of-rev`):
   `hsb-ledger-writer` persists it in the qa-log header and `hsb-packager` quotes it —
   no other agent recomputes the score.
   - In the same turn, spawn **`hsb-integrity-checker`** (read-only, mechanical): it
     verifies the TA ends with the sentinel and has no truncation/elision;
     `integrity = fail` is a hard block on the gate.
   - On a flagged conflict: spawn **`hsb-reconciler`** (read-only); route to
     `hsb-ledger-writer`.
   - Optional: spawn **`hsb-gap-reporter`** for a live gap map.
2. **`hsb-question-strategist`** (read-only, **fallback only**) targets the
   lowest-confidence / unconfirmed blocking sections — questions fire only when a
   section could not be drafted confidently or the CTO asks to deepen it.
3. The **CTO** reviews the pre-filled document, edits sections, approves ADRs, firms
   the estimate, and **commits the feasibility verdict**. Each confirmed entry is
   recorded by **`hsb-ledger-writer`** (serial).
4. **`hsb-doc-updater`** promotes confirmed entries: `Origin: ai_drafted` /
   `inherited` / `reused_from_KB` → `cto_authored`, raising confidence to reflect the
   CTO's judgment.
5. **If the KB had to be created** (brownfield/hybrid, KB `Does not exist`): spawn
   **`hsb-landscape-keeper`** to produce/update the `tech-landscape-<system>.md` from
   the documented current state — feasibility cannot be signed on unknown terrain.
6. **Gate check:** `signOffReady = true` when:
   - the `feasibility-verdict` is committed (`cto_authored` at its threshold), **and**
   - every other `blocksFreeze` section is resolved (`cto_authored` / confirmed-
     `inherited`) or honestly disposed (`decided` N/A path / `discovery`), **and**
   - if the verdict is `Infeasible as scoped`, the **veto rationale** is recorded
     (the TA freezes as a signed veto; see [`feasibility.md`](feasibility.md) § The
     veto path).

**Verdict reconciliation (on a veto).** `effort-cost` and `adrs` are drafted in Phase 3
in parallel, **before** the verdict exists, so a committed `Infeasible as scoped` can
leave them holding a confident estimate / ADR set for a scope ruled unbuildable. Before
freeze, route both through `hsb-doc-updater` to be re-dispositioned `Disposition: decided`,
content "N/A — vetoed (see feasibility-verdict)". A signed veto carries no confident
effort or ADRs.

See [`feasibility.md`](feasibility.md) for the full gate and the Discovery exit.

## Phase 5 — Production & wrap

Once `signOffReady`:

1. **`hsb-humanizer`** writes `output/humanized.md` — the canonical clean copy all
   production agents read. Must finish first. Then spawn **`hsb-language-auditor`**
   (read-only) to verify it for language leaks; route any leaks back to the Humanizer
   before the rest read it.
2. Then spawn **in the same turn** (parallel, distinct files):
   - **`hsb-translator`** → `output/translated.<lang>.md` (the confirmed output
     language).
   - **`hsb-visual-enricher`** → `output/enriched.md` (a C4-style context sketch when
     greenfield, the NFR-feasibility table, the integrations map, the ADR list).
   - **`hsb-finalizer`** → `final/<project>-NNN.md` — the clean, **printable final
     deliverable** (strips authoring scaffold; counter-suffixed; idempotent). Inject
     `PROJECT_SLUG`.
   - **`hsb-landscape-keeper`** (greenfield) → seeds the new `tech-landscape-<system>.md`
     from the foundational ADRs, if not already created in Phase 4.
3. **`hsb-packager`** writes `output/manifest.md`: the feasibility verdict, sign-off
   status (Signed off / Vetoed), open `discovery` dispositions, template hash/version,
   the handoff note to the PRD (the technical half of `PRD = RP + TA`), the
   `tech-landscape` it seeded/updated, and an index entry for the Finalizer's `final/`
   deliverable.
4. **Record the front in the initiative index.** Update this phase's `initiative.json`
   entry: `state: frozen`, the `artifacts` paths (incl.
   `canonical: assessment/output/humanized.md` and `final:
   assessment/final/<project>-NNN.md`), `produces: technical-assessment`, the
   feasibility `verdict`, and — crucially — **discharge the RP's `TechAssessmentRef`
   debt**: resolve the `owes` entry the RP pushed (set its `status` to `signed` or
   `vetoed`, and link this TA). If the verdict is a veto, also push a
   `scope-revision-owed` note back to the `readiness/` phase so the PO re-escalates.
   If the Tech Classifier **overrode** the demand nature (a `nature-override` signal),
   write the corrected `nature`/`kbStatus` into this front's `initiative.json` and push
   a `nature-corrected` note to the `readiness/` front — the frozen RP/Intake keep the
   triage value, but the index carries the correction the next front reads.
5. Report to the CTO: the verdict, the artifacts produced, the `tech-landscape`
   seeded/updated, every item parked as `discovery`, and (if vetoed) the scope-revision
   signal to the PO.

## The phase folder layout

The CTO's assessment lives in the `assessment/` phase, beside the `readiness/` and
`intake/` phases it consumes:

```
INITIATIVE_DIR/                  # shared by every front
├── initiative.json             # orchestrator — works + definitions index
├── glossary.md                 # Glossary Keeper — shared canonical terms
├── decisions.md                # Glossary Keeper — shared cross-phase decisions (incl. the feasibility verdict + hard constraints)
├── tech-landscape-<system>.md  # Landscape Keeper — persistent KB (seeded greenfield / updated brownfield)
├── origination/                # the upstream origination-record
├── intake/                     # the Intake Record (demand nature + KB classification)
├── readiness/                  # the Readiness Package (the RP this TA responds to)
└── assessment/                 # PHASE_DIR for the CTO's Technical Assessment
    ├── contract.lock.md        # hsb-template-analyst
    ├── sources-index.md        # hsb-source-indexer
    ├── sources/                # hsb-source-indexer (incl. RP + intake-record + tech-landscape)
    ├── qa-log.md               # hsb-ledger-writer
    ├── technical-assessment.md # hsb-doc-updater (TA-AAAA-NNN)
    ├── glossary.md             # brokered read-only copy of the initiative glossary
    ├── assessment-report.md    # hsb-gap-reporter (optional)
    ├── output/
    │   ├── humanized.md        # hsb-humanizer
    │   ├── translated.<lang>.md # hsb-translator
    │   ├── enriched.md         # hsb-visual-enricher
    │   └── manifest.md         # hsb-packager
    └── final/                  # hsb-finalizer — clean, printable final deliverable(s)
        └── <project>-NNN.md    # externalized, scaffolding-stripped, counter-suffixed
```
