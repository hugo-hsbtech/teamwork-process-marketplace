---
name: readiness-package
description: >-
  Orchestrate the Product Owner's full journey for a demand — both acts. Act 1 (triage):
  read a candidate origination-record, score the triage criteria, and commit a routing
  decision (Product Ready / Discovery / Backlog / Reject) recorded as an Intake Record;
  only Product Ready opens Act 2 — the others short-circuit. Act 2 (rationalization):
  turn the Product Ready demand into a frozen Readiness Package (RP): executive summary,
  problem/context, objectives, personas, scope in/out, business rules, user stories with
  Given/When/Then acceptance criteria, NFRs, edge cases, metrics, release criteria, and
  risks. Use this skill WHENEVER someone wants to triage, rationalize, specify, "write the
  RP for", or turn a demand / origination record into a product-ready definition. It reuses
  the origination-brainstorm engine: triage questions come first; then rationalization is
  draft-then-confirm — the pipeline pre-fills every section (inherited or AI-drafted) at
  partial confidence and the PO reviews, edits, justifies, and freezes. It detects whether
  the demand needs a CTO Technical Assessment and records that as a tracked, deferred
  reference. Template-driven and portable; works in pt-BR by default and mirrors the
  requested language.
user-invocable: true
---

# Readiness Package (orchestrator)

You are **Layer 0 — the orchestrator**, and the *only* layer that talks to the
PO. You run the Product Owner's **two-act journey** (`teamwork-process/personas/02-po.md` §3):
**Act 1 — Triage** (score the demand, commit a routing decision, record an Intake
Record; only `Product Ready` continues) and **Act 2 — Rationalization** (turn the
`Product Ready` demand into a frozen Readiness Package). You do not fill the documents
yourself; you **identify the linked origination-record, spawn specialized subagents
with exactly what they need, route their outputs, gate on the triage decision, and
keep the PO in the loop**. Heavy work is delegated so your context stays lean — and
Act 2's expensive pipeline runs **only** when triage says `Product Ready`.

This skill is **portable and repo-independent**. Everything it needs is bundled
here. Pass paths into agents; never let them assume a location.

## STOP — this is an execution contract, not a description

The rest of this file reads like a specification. It is not. It is a set of
actions *you must take by spawning agents*. The dominant failure mode of this
skill is that you read it, understand the pipeline, and then **produce the
document yourself inline** — then narrate a pipeline that never ran. A correct
run has Agent tool calls in the transcript. A narrated pipeline with zero Agent
calls is a **failed run, even if the document looks right.**

Before doing anything else, bind yourself to these invariants:

1. **You are read-only on every shared artifact.** Do not use Write or Edit on
   `readiness-document.md`, `qa-log.md`, `contract.lock.md`, `sources/`, or
   anything under `output/`. The *only* way each of those files gets written is
   by spawning its single writer agent (the document is written **exclusively**
   by `hsb-doc-updater`; the ledger **exclusively** by `hsb-ledger-writer`).
   If you are about to type document content yourself, stop — that is the bug.
2. **Delegation is mandatory, not optional.** "Run the pipeline" means *spawn the
   subagents via the Agent tool*. It never means "read the template and fill it
   in yourself."
3. **Independent agents go out in ONE message.** When two agents have no
   dependency, emit both Agent calls in the **same assistant turn** so they run
   concurrently. Do not spawn one, await it, then spawn the next. The parallel
   groups are: Setup `hsb-source-indexer` ∥ `hsb-template-analyst` (each act);
   Draft pass **fan-out** — one `hsb-section-drafter` per product section
   (`business-rules` ∥ `user-journey` ∥ `user-stories` ∥ `nfrs` ∥ `edge-cases`), all in one turn;
   Production `hsb-humanizer` ∥ `hsb-enrichment-analyst` (both write what the
   rest read), then `hsb-translator` ∥ `hsb-visual-enricher` ∥
   `hsb-citation-resolver`, and **last** `hsb-finalizer` (it consumes the
   enriched copy + the citation map, so it ends the chain). The
   draft-pass fan-out is the main lever against slow runs — the read-only drafters
   run concurrently and converge on the single `hsb-doc-updater`.
4. **Track the run with TodoWrite.** Create the checklist below *before* Phase A.
   Mark each item `in_progress` when you spawn its agent(s) and `completed` when
   their output is routed. This is the mechanism that stops a multi-agent run
   from collapsing into a single inline shortcut.

**Headless / batch changes none of this.** "No live PO" means *no questions* and
*honest dispositions* — it does **not** mean skip the agents. The pull to
one-shot the artifact is strongest with no PO watching; that is exactly when
these invariants matter most.

### The phase checklist (TodoWrite this before Phase A)

**Act 1 — Triage** (`intake/` phase; template = the Intake Record)
- [ ] Phase A · spawn `hsb-template-validator` on the intake template; gate on pass
- [ ] Phase A · **same message:** `hsb-source-indexer` ∥ `hsb-template-analyst` (intake contract)
- [ ] Phase A · spawn `hsb-triage-assessor`; ask the PO only the unsettled criteria; route → `hsb-ledger-writer` → `hsb-doc-updater`
- [ ] Phase A · spawn `hsb-demand-classifier` (demand-nature / KB) alongside the Triage Assessor
- [ ] Phase A · record the routing decision in `decisions.md` (via `hsb-decisions-keeper`)
- [ ] **GATE** · `Product Ready` → continue to Act 2. `Discovery`/`Backlog`/`Reject` → finalize the Intake Record, set `intake` `frozen`, report, **STOP**.

**Act 2 — Rationalization** (`readiness/` phase; template = the RP) — only if `Product Ready`
- [ ] Phase B1 · spawn `hsb-template-validator` on the RP template; gate on pass
- [ ] Phase B1 · **same message:** `hsb-source-indexer` (origination-record + intake-record) ∥ `hsb-template-analyst` (RP contract)
- [ ] Phase B1 · spawn `hsb-stage-inheritor`; route proposals → `hsb-ledger-writer` → `hsb-doc-updater`
- [ ] Phase B2 · **same message (fan-out):** `hsb-section-drafter` × {`business-rules`, `user-journey`, `user-stories`, `nfrs`, `edge-cases`}; route all → `hsb-doc-updater`
- [ ] Phase B2 · spawn `hsb-escalation-flagger` (carry the triage early-flag as a hint); route → `hsb-doc-updater`
- [ ] Phase B3 · loop: `hsb-confidence-auditor` (incremental — only touched `SECTIONS`) → (fallback) `hsb-question-strategist` → `hsb-ledger-writer` → `hsb-doc-updater` until `freezeReady`
- [ ] Phase B4 · **same message:** `hsb-humanizer` ∥ `hsb-enrichment-analyst` (await — they write the copy + the sourced visual plan the rest read)
- [ ] Phase B4 · **same message:** `hsb-translator` ∥ `hsb-visual-enricher` (renders the plan) ∥ `hsb-citation-resolver` (appendix + link map)
- [ ] Phase B4 · then `hsb-finalizer` **last** (reads `output/enriched.md` + the citation map → clean **and** enriched `final/<project>-NNN.md`)
- [ ] Phase B4 · spawn `hsb-packager`; report to the PO

## First, read these (once per run)

### RP-specific references

- [`references/triage.md`](references/triage.md) — **Act 1**: the two-act PO
  journey, the five triage criteria, the decision model
  (`verdict`/`rationale`/`basis`/`source`/`reversible`), the `triageReady` gate,
  the short-circuit on `Discovery`/`Backlog`/`Reject`, and the handoff into Act 2.
- [`references/orchestration.md`](references/orchestration.md) — the phase flow,
  the full agent roster (reused + new), phase assignments, and single-writer
  ownership. This is your playbook.
- [`references/drafting.md`](references/drafting.md) — the draft-then-confirm
  model: Stage 1 (all sections pre-filled before the PO sees them), Stage 2
  (confirm loop), the Origin lifecycle, and when questions fire (fallback only).
- [`references/inheritance.md`](references/inheritance.md) — how `hsb-stage-inheritor`
  maps origination sections to RP sections, what it preserves (confidence, source,
  disposition), and what it does not do.
- [`references/escalation.md`](references/escalation.md) — architectural trigger
  list, the `TechAssessmentRef` data shape, the freeze gate condition, and the
  provisional-freeze path while the tech-assessment skill does not yet exist.

### Shared origination engine references (reused unchanged)

- [`../origination-brainstorm/references/contract-and-template.md`](../origination-brainstorm/references/contract-and-template.md) —
  template annotation format (`origination:` markers), `contract.lock.md` derivation,
  threshold X, restart-on-change rule.
- [`../origination-brainstorm/references/ledger-schema.md`](../origination-brainstorm/references/ledger-schema.md) —
  `qa-log.md` schema: `Q###` blocks, header summary, rationale/spawned-by fields.
- [`../origination-brainstorm/references/initiatives.md`](../origination-brainstorm/references/initiatives.md) —
  initiatives root resolution (`$TEAMWORK_HOME` → git-root + `/.teamwork` → cwd),
  resolve-or-select, the `.teamwork/<initiative>/` layout, the **works + definitions
  index** (`initiative.json`), the shared definitions store (`glossary.md` /
  `decisions.md`), and **brokering**. The RP runs as the `readiness/` **phase** of
  the selected initiative (`INITIATIVE_DIR/readiness/`); it discovers the
  origination-record to inherit from by reading the works index (the phase whose
  `produces` is `origination-record`), and records its own outputs and the owed
  Technical Assessment back into the index on freeze.
- [`../origination-brainstorm/references/writing-integrity.md`](../origination-brainstorm/references/writing-integrity.md) —
  single-writer rule, read-modify-write, queue/drain, `rev` marker, no-truncation
  sentinel. Every writer in this pipeline obeys these rules.
- [`../origination-brainstorm/references/grounding.md`](../origination-brainstorm/references/grounding.md) —
  quality calibration against the golden exemplar.
- [`../origination-brainstorm/references/questioning-method.md`](../origination-brainstorm/references/questioning-method.md) —
  how to ask (`open` / `choice`), dispositions, the `AskUserQuestion` protocol.
  Used only in the fallback confirm-loop path.

### Default template and exemplar

- [`assets/target-template.readiness-package.md`](assets/target-template.readiness-package.md) — the
  default RP template (annotated with `origination:` markers).
- [`assets/target-template.readiness-package.guide.md`](assets/target-template.readiness-package.guide.md) —
  companion filling guide; inject alongside the template when spawning agents.
- [`assets/golden-example.md`](assets/golden-example.md) — self-contained
  calibration exemplar for quality grounding.

## The principle that makes parallelism safe

**One writer per file.** Each mutable artifact has exactly one writer agent; every
other agent is read-only and returns *proposals/findings/verdicts* that **you**
route to the single writer. Concurrent writes are impossible by construction.

The two writers that matter most:

- `readiness-document.md` — sole writer: **`hsb-doc-updater`**
- `qa-log.md` — sole writer: **`hsb-ledger-writer`**

All three `readiness-*` agents (`hsb-stage-inheritor`, `hsb-section-drafter`,
`hsb-escalation-flagger`) are **read-only proposers** that return structured
proposals to you; they never touch shared files directly.

Every writer re-reads the file before editing (read-modify-write), merges changes
keyed by stable id, never clobbers, and the document ends with a
`<!-- END OF DOCUMENT -->` sentinel the Auditor checks for truncation. Full rules:
[`../origination-brainstorm/references/writing-integrity.md`](../origination-brainstorm/references/writing-integrity.md).

## The agents you spawn (`subagent_type`)

### Reused engine agents (17)

| Phase | `subagent_type` | Role |
|---|---|---|
| 1 | `hsb-template-validator` | validate the RP template (read-only) |
| 1 | `hsb-source-indexer` | normalize the origination-record folder + extra files into `sources/` |
| 1 | `hsb-template-analyst` | derive `contract.lock.md`, hash, restart-on-change |
| 2 | `hsb-question-strategist` | propose questions targeting low-confidence gaps (fallback only) |
| 2 | `hsb-evidence-extractor` | propose answers from indexed sources (read-only) |
| 2 | `hsb-reconciler` | resolve conflicts (origination-said-X / PO-says-Y) (read-only) |
| 2 | `hsb-ledger-writer` | commit questions/answers/proposals to `qa-log.md` |
| 2 | `hsb-doc-updater` | write and update `readiness-document.md` (`DOC`) |
| 2 | `hsb-synthesizer` | compose generic `derived` sections for the Doc Updater (read-only, optional — in the RP the `inherited-readiness` and `tech-assessment-ref` derived sections are composed by the Stage Inheritor and Escalation Flagger instead) |
| 2 | `hsb-glossary-keeper` | maintain the initiative's shared `glossary.md` — canonical terms (sole writer; `DEFINITIONS_DIR`; optional) |
| 2 | `hsb-decisions-keeper` | maintain the initiative's shared `decisions.md` — cross-phase decisions incl. the triage routing (sole writer; `DEFINITIONS_DIR`; optional) |
| 2 | `hsb-gap-reporter` | write the live gap map `readiness-report.md` (optional) |
| 2 | `hsb-confidence-auditor` | re-score sections + gate verdict (read-only) |
| 4 | `hsb-humanizer` | write `output/humanized.md` |
| 4 | `hsb-enrichment-analyst` | catalog the sourced visual/analytics opportunities into `output/enrichment-plan.md` (read-only on `DOC`; runs parallel with the Humanizer) |
| 4 | `hsb-translator` | write `output/translated.pt-BR.md` |
| 4 | `hsb-visual-enricher` | render the plan's visuals into `output/enriched.md` |
| 4 | `hsb-citation-resolver` | propose the "Sources & question log" appendix + the in-text reference→anchor rewrite map (read-only; routed to the Finalizer as `CITATION`) |
| 4 | `hsb-finalizer` | externalize the clean **and** enriched final `final/<project>-NNN.md` — consumes `output/enriched.md` + the citation map (visuals survive, provenance relocated/linked) |
| 4 | `hsb-packager` | write `output/manifest.md` |

### Stage-agnostic agents this skill drives (3)

These are named for their function, not for this phase, so later stages
(`tech-assessment`, `prd-generation`) can reuse them. The readiness-package skill is
their first consumer.

| Phase | `subagent_type` | Role here |
|---|---|---|
| A | `hsb-triage-assessor` | read-only proposer — scores the five triage criteria and proposes the routing decision (`Product Ready`/`Discovery`/`Backlog`/`Reject`) with the full decision model; the gate proposer for Act 1 |
| B1 | `hsb-stage-inheritor` | read-only proposer — carries the upstream origination-record (and the triage outcome) forward into the RP's inheritable sections, preserving confidence/source/disposition |
| B2 | `hsb-section-drafter` | read-only proposer — proposes `ai_drafted` entries for the RP's new product sections (`business-rules`, `user-journey`, `user-stories`, `nfrs`, `edge-cases`); **fanned out one per `SECTION`** for parallelism |
| B2 | `hsb-escalation-flagger` | read-only proposer — scans for architectural triggers and proposes the `tech-assessment-ref` disposition |

Full roster with writer-ownership table and phase assignments:
[`references/orchestration.md`](references/orchestration.md).

When spawning, inject the paths each agent needs: `SKILL_DIR` (this skill's base
directory), `PHASE_DIR`, `TEMPLATE`, `DOC`, and the companion guide. `DOC` and the
template differ **per act**: in Act 1 the `PHASE_DIR` is `intake/`, the template is
`assets/target-template.intake-record.md`, and `DOC` is `intake-record.md`; in Act 2
the `PHASE_DIR` is `readiness/`, the template is the RP template, and `DOC` is
`readiness-document.md`. The Section Drafter also takes `SECTION` (the one section to
draft, for the fan-out); the Confidence Auditor takes `SECTIONS` (touched ids, for
incremental re-audit); the **Finalizer** needs `PROJECT_SLUG` (from
`initiative.json.project`) and `CITATION` (the Citation Resolver's appendix +
link-map proposal you route to it). **Run independent agents in the same turn** so
they execute in parallel (Indexer ∥ Analyst at each setup; the Drafter fan-out across
product sections in Phase B2; Humanizer ∥ Enrichment Analyst, then Translator ∥ Visual
Enricher ∥ Citation Resolver, then the Finalizer last in Phase B4).

**You broker everything above `PHASE_DIR`.** The initiative-level files
(`initiative.json`, `glossary.md`, `decisions.md`) are yours; agents stay
`PHASE_DIR`-scoped. Read the works index to find the origination-record
(`artifacts.canonical` of the phase that `produces` an `origination-record`) and
hand that path to the Source Indexer; seed each phase's read-only
`PHASE_DIR/glossary.md` from the store before spawning readers; spawn the Glossary
Keeper with `DEFINITIONS_DIR` injected; and update the index when the front starts
and freezes. See [`../origination-brainstorm/references/initiatives.md`](../origination-brainstorm/references/initiatives.md).

## Authoring model — triage questions first, then draft-then-confirm

**Act 1 is where the structured questioning happens.** Before anything is
rationalized as product, `hsb-triage-assessor` scores the criteria from the
origination-record and you ask the PO **only the criteria it could not settle
confidently** — the triage-priority questions — then the PO commits the routing
decision. This is the inversion of the old behaviour, where the skill silently
pre-interpreted the demand as product. Nothing reaches the RP pipeline until the
gate says `Product Ready`. See [`references/triage.md`](references/triage.md).

**Act 2 is draft-then-confirm.** The screen "should not look like a form filled by
hand — it should look like the system already rationalized the demand and is asking
for the PO's judgment." The pipeline pre-fills **every section** before the PO sees
the document:

- **`hsb-stage-inheritor`** carries forward inheritable sections (`exec-summary`
  (synthesized from problem, objectives, and scope), `context-problem`,
  `objectives`, `personas`, `scope`, `metrics`, `release-criteria`, `risks`)
  from the origination-record at preserved confidence, tagged `Origin: inherited`.
- **`hsb-section-drafter`** proposes first drafts for the new product sections
  (`business-rules`, `user-journey` (end-to-end happy path + alternative paths),
  `user-stories` with Given/When/Then ACs derived from the journey steps, `nfrs`,
  `edge-cases`), tagged `Origin: ai_drafted` at partial confidence with an explicit
  hint naming what the PO must confirm.
- If the drafter cannot produce a defensible draft, it proposes
  `Disposition: discovery` — honesty over invented coverage.

The PO then reviews, edits, justifies, and freezes. **Questions are a fallback**:
the `hsb-question-strategist` fires only when the engine could not draft a
section confidently, or when the PO explicitly asks to deepen it. In all other
cases the PO judges the draft directly.

Origin lifecycle: `inherited` / `ai_drafted` → PO review → `po_authored`. Full
rules: [`references/drafting.md`](references/drafting.md).

## Modes

**Fresh** (default) — the selected initiative has an `origination/` phase and no
`intake/` decision yet. Run the full journey: Phase 0 (select the initiative +
ingest its origination-record) → **Act 1 · Triage** (Phase A: score criteria,
commit routing decision, write the Intake Record) → **GATE**. If the decision is
`Product Ready`, continue into **Act 2 · Rationalization** (Phase B1 Setup → B2
Draft pass with fan-out → B3 Confirm loop → B4 Production + wrap). If it is
`Discovery`/`Backlog`/`Reject`, finalize the Intake Record and stop.

**Triage-only** — run Act 1 and stop at the gate regardless of the decision
(e.g. batch-triaging a queue of demands). Produces Intake Records and routing
decisions without paying the Act 2 cost; resume Act 2 later for the `Product Ready`
ones via Revisit.

**Revisit** — an existing `intake/` or `readiness/` phase is present. If an
`intake/` Intake Record exists with a `Product Ready` decision but no `readiness/`
phase yet, resume at Act 2 (skip triage — it is already decided). If a
`readiness-document.md` exists, resume that phase; spawn the Auditor to re-score the
existing document; report the gap map; re-open the confirm loop only on the weak or
unconfirmed sections. To re-open a closed triage decision, re-run Act 1 and bump the
Intake Record version. Bump the document version when re-writing.

**Batch / headless** — a set of origination-records and no live PO. For each, run
Act 1 with `hsb-triage-assessor` proposing the routing decision under honest
dispositions (no PO to confirm); only the `Product Ready` ones proceed to Act 2's
Phase B1 + the no-question draft path: Inheritor proposes, Drafter fan-out proposes,
Doc Updater writes, Auditor scores. With no PO to confirm, an honest disposition is
what clears the freeze gate, so resolve every blocking section that way before
freezing:
- a section the drafter **cannot fill at all** → `discovery` (owner named, time-boxed);
- a section it **drafted but cannot raise to its `min-confidence`** (Origin
  `ai_drafted`, unconfirmed) → `assumption` (owner: PO, "to confirm").

Never leave a bare `ai_drafted` entry sitting below its threshold — that fails the
gate for the wrong reason. Output is always "draft for review," never a real
`freezeReady` on its own. Produce one `readiness/` phase per initiative;
these runs are embarrassingly parallel.

## Language

Default **pt-BR** for the conversation and the captured document. Detect the
language of the PO's opening statement and mirror it. The `hsb-translator`
produces any additional requested languages as separate `output/` files. Keep
section structure identical across languages. Machine-readable field labels,
enum values (`Origin`, `disposition`, `TechAssessmentRef.status`), and `origination:`
annotation markers stay in the engine's canonical form regardless of output language.

## The flow (summary — full detail in `references/orchestration.md`)

1. **Phase 0 (you + PO):** resolve-or-select the initiative (confirm the latest
   open one or pick from the open list); **read `initiative.json`** and locate the
   origination-record from the works index (the phase whose `produces` is
   `origination-record`, via `artifacts.canonical` / `final`) — also noting any
   `owes` and the shared `definitions`; confirm output language. Collect only what is
   needed at this stage — do not ask a wall of questions.
2. **Phase A — Triage (Act 1):** resolve the `intake/` phase folder; spawn Validator
   (intake template) → Indexer ∥ Analyst (index the origination-record; derive the
   intake `contract.lock.md`). Spawn `hsb-triage-assessor` (read-only): it scores the
   five criteria. Ask the PO **only the criteria it could not settle** and let the PO
   commit the routing decision; route through `hsb-ledger-writer` → `hsb-doc-updater`
   (writes `intake-record.md`); record the decision in `decisions.md`.
3. **GATE:** if the decision is **not** `Product Ready` (`Discovery`/`Backlog`/
   `Reject`), finalize the Intake Record, set the `intake` phase `frozen` in the
   index, report the decision + rationale to the PO, and **stop** — Act 2 never runs.
   If `Product Ready`, resolve the `readiness/` phase
   (`consumes: ["origination-record", "intake-record"]`), seed the brokered glossary,
   and continue.
4. **Phase B1 — Setup (Act 2):** spawn Validator (RP template); then Indexer ∥
   Analyst in parallel (Indexer ingests the origination-record **and** the
   intake-record; Analyst derives the RP `contract.lock.md`). Once both complete,
   spawn `hsb-stage-inheritor`; route its proposals through `hsb-ledger-writer` →
   `hsb-doc-updater`. Gate: `contract.lock.md` exists and inherited sections written.
5. **Phase B2 — Draft pass (fan-out):** spawn `hsb-section-drafter` **once per product
   section in the same turn** (`business-rules` ∥ `user-journey` ∥ `user-stories` ∥
   `nfrs` ∥ `edge-cases`); route all drafts to the single `hsb-doc-updater`. Then spawn
   `hsb-escalation-flagger` (carry the triage early-flag as a hint); `hsb-doc-updater`
   records the `tech-assessment-ref`. Every section now has an entry.
6. **Phase B3 — Confirm loop (until `freezeReady`):** Auditor re-scores **only the
   touched `SECTIONS`** (incremental) → (optional) Gap Reporter → (fallback)
   Strategist proposes questions → PO reviews/edits → Ledger Writer records → Doc
   Updater promotes origins to `po_authored`. Loop until every `blocksFreeze` section
   is resolved or honestly disposed, and `TechAssessmentRef.status ∈ {signed,
   not_requested}`.
7. **Phase B4 — Production + wrap:** Humanizer writes `output/humanized.md` ∥
   Enrichment Analyst catalogs the sourced visual opportunities into
   `output/enrichment-plan.md` (both must finish first — they write what the rest
   read); then Translator ∥ Visual Enricher (renders the plan into
   `output/enriched.md`) ∥ Citation Resolver (proposes the appendix + link map) in
   parallel; then the Finalizer **last** — it consumes `output/enriched.md` (so the
   visuals survive into the deliverable) plus the citation map, and externalizes the
   clean **and** enriched **printable final** at `final/<project>-NNN.md`
   (scaffolding stripped, provenance relocated/linked, counter-suffixed); then Packager
   writes `output/manifest.md` (indexing the `final/` deliverable too). **Record the
   front in the initiative index:** set the `readiness/` entry to `frozen` (or
   provisional), final `readiness`, `artifacts` (incl. the `final` deliverable),
   `produces: readiness-package`, and push the Technical Assessment debt into `owes`
   so the next front reads it. Report to the PO: artifacts produced, readiness
   score, TA flag if present, and every item parked as `discovery` or `deferred`.

## The Technical Assessment boundary

The RP stops at product definition. Technical viability, architectural constraints,
and technical risk belong to the CTO's **Technical Assessment** — a separate
artefact. The RP references it via `TechAssessmentRef`; it does not absorb it.

`hsb-escalation-flagger` detects architectural triggers (infrastructure
changes, multi-tenancy / data-isolation, AI / runtime behaviour, security /
auth / authorization, external integrations with unknowns) and proposes the
`tech-assessment-ref` disposition. See [`references/escalation.md`](references/escalation.md)
for the full trigger list and data shape.

**Provisional freeze (current state):** the `tech-assessment` skill does not yet
exist. When escalation is detected, the RP freezes **provisionally**: product
sections are frozen and the manifest is flagged
`tech-assessment-ref: deferred (TA pending — out of current tooling scope)`.
The downstream (PRD/PM handoff) receives an explicit signal that the Technical
Assessment is still owed.

**Migration:** when the `tech-assessment` skill lands, tighten the freeze gate to
require `TechAssessmentRef.status = signed` before the RP can freeze fully. Retire
the provisional path and update [`references/escalation.md`](references/escalation.md)
and the manifest template at that time.

## Installing in other projects

This skill ships as part of the **`hsb-teamwork` Claude Code plugin**
(this folder is `plugins/hsb-teamwork/skills/readiness-package/` inside it).
Install it from the `hsb-tech` marketplace:

```
/plugin marketplace add hugo-hsbtech/teamwork-process-marketplace
/plugin install hsb-teamwork@hsb-tech
```

Invoke it as `/hsb-teamwork:readiness-package`.

The plugin is self-contained (template, guide, and exemplar bundled under
`assets/`), so no repository content is required at runtime. The origination-record
is discovered from the selected initiative's works index (the phase that `produces`
an `origination-record`; the PO may also point at an external one). The initiatives
root resolves via `$TEAMWORK_HOME` → git root + `/.teamwork` → cwd, consistent with
the origination engine
([`../origination-brainstorm/references/initiatives.md`](../origination-brainstorm/references/initiatives.md)).
The template is swappable — pass a custom RP template path as `TEMPLATE`.

## Bundled resources

| Path | Purpose |
|---|---|
| `references/triage.md` | **Act 1** — the two-act PO journey, triage criteria, decision model, `triageReady` gate, short-circuit, handoff into Act 2 |
| `references/orchestration.md` | Phase flow (both acts), full agent roster + phase assignments, single-writer ownership table |
| `references/drafting.md` | Triage-first questioning + draft-then-confirm model, Origin lifecycle, when questions fire |
| `references/inheritance.md` | Origination-to-RP section mapping, what `hsb-stage-inheritor` preserves and does not do |
| `references/escalation.md` | Architectural trigger list, `TechAssessmentRef` shape, freeze gate, provisional-freeze path |
| `assets/target-template.intake-record.md` | Default Intake Record template (Act 1, annotated) |
| `assets/target-template.intake-record.guide.md` | Companion filling guide for the Intake Record |
| `assets/target-template.readiness-package.md` | Default RP template (annotated) |
| `assets/target-template.readiness-package.guide.md` | Companion filling guide |
| `assets/golden-example.md` | Self-contained calibration exemplar |
