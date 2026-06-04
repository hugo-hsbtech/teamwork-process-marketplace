---
name: readiness-package
description: >-
  Orchestrate a multi-agent pipeline that turns a Product Ready origination-record into
  a frozen Readiness Package (RP) — the Product Owner's rationalization artefact:
  executive summary, problem/context, objectives, personas, scope in/out, business
  rules, user stories with Given/When/Then acceptance criteria, NFRs, edge cases,
  metrics, release criteria, and risks. Use this skill WHENEVER someone wants to
  rationalize, specify, "write the RP for", or turn a triaged demand / origination record
  into a product-ready definition. It reuses the origination-brainstorm engine and authors
  draft-then-confirm: the pipeline pre-fills every section (inherited from the origination
  record or AI-drafted) at partial confidence, and the PO reviews, edits, justifies,
  and freezes. It detects whether the demand needs a CTO Technical Assessment and
  records that as a tracked, deferred reference. Template-driven and portable; works
  in pt-BR by default and mirrors the requested language.
user-invocable: true
---

# Readiness Package (orchestrator)

You are **Layer 0 — the orchestrator**, and the *only* layer that talks to the
PO. You do not fill the document yourself; you **identify the linked origination-record,
spawn specialized subagents with exactly what they need, route their outputs, and
keep the PO in the loop**. Heavy work is delegated so your context stays lean.

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
   pairs are: Phase 1 `hsb-source-indexer` ∥ `hsb-template-analyst`;
   Phase 4 `hsb-translator` ∥ `hsb-visual-enricher` ∥ `hsb-finalizer`.
4. **Track the run with TodoWrite.** Create the checklist below *before* Phase 1.
   Mark each item `in_progress` when you spawn its agent(s) and `completed` when
   their output is routed. This is the mechanism that stops a multi-agent run
   from collapsing into a single inline shortcut.

**Headless / batch changes none of this.** "No live PO" means *no questions* and
*honest dispositions* — it does **not** mean skip the agents. The pull to
one-shot the artifact is strongest with no PO watching; that is exactly when
these invariants matter most.

### The phase checklist (TodoWrite this before Phase 1)

- [ ] Phase 1 · spawn `hsb-template-validator`; gate on pass
- [ ] Phase 1 · **same message:** `hsb-source-indexer` ∥ `hsb-template-analyst`
- [ ] Phase 1 · spawn `hsb-stage-inheritor`; route proposals → `hsb-ledger-writer` → `hsb-doc-updater`
- [ ] Phase 2 · spawn `hsb-section-drafter`; route → `hsb-doc-updater`
- [ ] Phase 2 · spawn `hsb-escalation-flagger`; route → `hsb-doc-updater`
- [ ] Phase 3 · loop: `hsb-confidence-auditor` → (fallback) `hsb-question-strategist` → `hsb-ledger-writer` → `hsb-doc-updater` until `freezeReady`
- [ ] Phase 4 · spawn `hsb-humanizer` (await — it writes the copy the rest read)
- [ ] Phase 4 · **same message:** `hsb-translator` ∥ `hsb-visual-enricher` ∥ `hsb-finalizer`
- [ ] Phase 4 · spawn `hsb-packager`; report to the PO

## First, read these (once per run)

### RP-specific references

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
| 2 | `hsb-glossary-keeper` | maintain the initiative's shared `glossary.md` + `decisions.md` (sole writer; spawned with `DEFINITIONS_DIR`; optional) |
| 2 | `hsb-gap-reporter` | write the live gap map `readiness-report.md` (optional) |
| 2 | `hsb-confidence-auditor` | re-score sections + gate verdict (read-only) |
| 4 | `hsb-humanizer` | write `output/humanized.md` |
| 4 | `hsb-translator` | write `output/translated.pt-BR.md` |
| 4 | `hsb-visual-enricher` | write `output/enriched.md` |
| 4 | `hsb-finalizer` | externalize the clean, printable final `final/<project>-NNN.md` |
| 4 | `hsb-packager` | write `output/manifest.md` |

### Stage-agnostic agents this skill drives (3)

These are named for their function, not for this phase, so later stages
(`tech-assessment`, `prd-generation`) can reuse them. The readiness-package skill is
their first consumer.

| Phase | `subagent_type` | Role here |
|---|---|---|
| 1 | `hsb-stage-inheritor` | read-only proposer — carries the upstream origination-record forward into the RP's inheritable sections, preserving confidence/source/disposition |
| 2 | `hsb-section-drafter` | read-only proposer — proposes `ai_drafted` entries for the RP's new product sections (`business-rules`, `user-stories`, `nfrs`, `edge-cases`) |
| 2 | `hsb-escalation-flagger` | read-only proposer — scans for architectural triggers and proposes the `tech-assessment-ref` disposition |

Full roster with writer-ownership table and phase assignments:
[`references/orchestration.md`](references/orchestration.md).

When spawning, inject the paths each agent needs: `SKILL_DIR` (this skill's base
directory), `PHASE_DIR`, `TEMPLATE`, `DOC` (the target document's filename —
`readiness-document.md` for this skill), and the companion guide. The **Finalizer**
also needs `PROJECT_SLUG` (from `initiative.json.project`) to name the externalized
deliverable. **Run independent agents in the same turn** so they execute in parallel
(Indexer ∥ Analyst in Phase 1; Translator ∥ Visual Enricher ∥ Finalizer in Phase 4).

**You broker everything above `PHASE_DIR`.** The initiative-level files
(`initiative.json`, `glossary.md`, `decisions.md`) are yours; agents stay
`PHASE_DIR`-scoped. Read the works index to find the origination-record
(`artifacts.canonical` of the phase that `produces` an `origination-record`) and
hand that path to the Source Indexer; seed each phase's read-only
`PHASE_DIR/glossary.md` from the store before spawning readers; spawn the Glossary
Keeper with `DEFINITIONS_DIR` injected; and update the index when the front starts
and freezes. See [`../origination-brainstorm/references/initiatives.md`](../origination-brainstorm/references/initiatives.md).

## Authoring model — draft-then-confirm

The screen "should not look like a form filled by hand — it should look like the
system already rationalized the demand and is asking for the PO's judgment." The
pipeline pre-fills **every section** before the PO sees the document:

- **`hsb-stage-inheritor`** carries forward inheritable sections (`exec-summary`
  (synthesized from problem, objectives, and scope), `context-problem`,
  `objectives`, `personas`, `scope`, `metrics`, `release-criteria`, `risks`)
  from the origination-record at preserved confidence, tagged `Origin: inherited`.
- **`hsb-section-drafter`** proposes first drafts for the new product sections
  (`business-rules`, `user-stories` with Given/When/Then ACs, `nfrs`, `edge-cases`),
  tagged `Origin: ai_drafted` at partial confidence with an explicit hint naming
  what the PO must confirm.
- If the drafter cannot produce a defensible draft, it proposes
  `Disposition: discovery` — honesty over invented coverage.

The PO then reviews, edits, justifies, and freezes. **Questions are a fallback**:
the `hsb-question-strategist` fires only when the engine could not draft a
section confidently, or when the PO explicitly asks to deepen it. In all other
cases the PO judges the draft directly.

Origin lifecycle: `inherited` / `ai_drafted` → PO review → `po_authored`. Full
rules: [`references/drafting.md`](references/drafting.md).

## Modes

**Fresh** (default) — the selected initiative has a `Product Ready` `origination/`
phase; no `readiness/` phase yet. Run the full pipeline: Phase 0 (select the
initiative + confirm its origination-record) → 1 (Setup) → 2 (Draft pass) → 3
(Confirm loop) → 4 (Production + wrap).

**Revisit** — an existing `readiness-document.md` is present in the initiative's
`readiness/` phase folder. Resume the phase; spawn the Auditor to re-score the
existing document; report the gap map; re-open the confirm loop only on the weak
or unconfirmed sections. Bump the document version when re-writing.

**Batch / headless** — a set of `Product Ready` origination-records and no live PO. For
each, run Phase 1 + the no-question draft path: Inheritor proposes, Drafter
proposes, Doc Updater writes, Auditor scores. With no PO to confirm, an honest
disposition is what clears the freeze gate, so resolve every blocking section that
way before freezing:
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
   `Product Ready` origination-record from the works index (the phase whose
   `produces` is `origination-record`, via `artifacts.canonical`) — also noting any
   `owes` and the shared `definitions`; resolve the `readiness/` phase folder
   (`INITIATIVE_DIR/readiness/`), register it in the index, and seed the brokered
   glossary; confirm output language. Collect only what is needed at this stage — do
   not ask a wall of questions.
2. **Phase 1 — Setup (parallel, gate):** spawn Validator; then Indexer ∥ Analyst in
   parallel (Indexer ingests the origination-record folder; Analyst derives
   `contract.lock.md`). Once both complete, spawn `hsb-stage-inheritor` (read-only);
   route its proposals through `hsb-ledger-writer` → `hsb-doc-updater`
   (serial). Gate: `contract.lock.md` must exist and inherited sections must be
   written before Phase 2.
3. **Phase 2 — Draft pass:** spawn `hsb-section-drafter` (reads contract + inherited
   entries + sources; proposes `ai_drafted` sections); `hsb-doc-updater` writes
   them. Then spawn `hsb-escalation-flagger` (reads scope + business-rules;
   proposes `tech-assessment-ref`); `hsb-doc-updater` records. At end of Phase 2
   every section has an entry — `inherited`, `ai_drafted`, or `discovery`.
4. **Phase 3 — Confirm loop (until `freezeReady`):** Auditor re-scores → (optional)
   Gap Reporter writes gap map → (fallback) Strategist proposes questions →
   PO reviews/edits document → Ledger Writer records confirmations → Doc Updater
   promotes origins to `po_authored`. Loop until every `blocksFreeze` section is
   resolved or honestly disposed, and `TechAssessmentRef.status ∈ {signed,
   not_requested}`.
5. **Phase 4 — Production + wrap:** Humanizer writes `output/humanized.md` (must
   finish first); then Translator ∥ Visual Enricher ∥ Finalizer in parallel — the
   Finalizer externalizes the **printable final deliverable** at
   `final/<project>-NNN.md` (scaffolding stripped, counter-suffixed); then Packager
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
| `references/orchestration.md` | Phase flow, full agent roster + phase assignments, single-writer ownership table |
| `references/drafting.md` | Draft-then-confirm model, Origin lifecycle, when questions fire |
| `references/inheritance.md` | Origination-to-RP section mapping, what `hsb-stage-inheritor` preserves and does not do |
| `references/escalation.md` | Architectural trigger list, `TechAssessmentRef` shape, freeze gate, provisional-freeze path |
| `assets/target-template.readiness-package.md` | Default RP template (annotated) |
| `assets/target-template.readiness-package.guide.md` | Companion filling guide |
| `assets/golden-example.md` | Self-contained calibration exemplar |
