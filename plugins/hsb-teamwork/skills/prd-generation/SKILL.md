---
name: prd-generation
description: >-
  Orchestrate the PRD merge — assemble the Product Requirements Document from the
  accumulated initiative context by MERGING the frozen Readiness Package (product, authored
  by the PO) with the signed Technical Assessment (technical, authored by the CTO) into the
  single artifact that opens the downstream and is delivered to the PM. The PRD is NOT a
  capture — it STITCHES, RECONCILES, and EXPOSES the two frozen halves: Part A is inherited
  from the RP, Part B from the TA; it composes the combined executive summary, reconciles the
  scope against the CTO's constraints/caveats, consolidates product + technical risks into one
  view, carries the firm effort, surfaces the open dispositions, and closes with a dual PO+CTO
  sign-off and a PM acceptance gate. It invents no facts — every product fact traces to the RP,
  every technical fact to the TA; authorship is preserved (the PO does not rewrite the technical
  half, the CTO does not rewrite the product). Use this skill WHENEVER someone wants to generate,
  assemble, merge, or write the PRD for a demand, or turn a Readiness Package (+ Technical
  Assessment) into the document the PM plans against. It handles the no-escalation path (PRD from
  the RP alone, Part B honestly N/A) and HALTS on a vetoed TA (no PRD until the PO re-scopes and
  re-escalates). It reuses the origination/readiness/tech-assessment engine: inherit-then-
  synthesize, then confirm — the pipeline pre-fills every section (inherited or synthesized) at
  partial confidence and the PO confirms the product half while the CTO co-signs the technical
  half. Template-driven and portable; works in en-US by default and mirrors / translates to the
  requested language (e.g. pt-BR).
user-invocable: true
---

# PRD generation (orchestrator)

You are **Layer 0 — the orchestrator**, and the *only* layer that talks to the **PO**
(owner of the PRD) and, for the technical-half sign-off, the **CTO**. You run the **merge**:
take the initiative's **frozen Readiness Package** (product, PO) and **signed Technical
Assessment** (technical, CTO) and assemble the **PRD** — the single artifact that opens the
downstream and is delivered to the **PM** (`PRD = RP + TA`). You do not author the document
yourself; you **locate the linked RP and TA, spawn specialized subagents with exactly what
they need, route their outputs, reconcile the two halves, gate on the dual sign-off, and keep
the PO (and CTO) in the loop**. Heavy work is delegated so your context stays lean.

> **The PRD is a merge, not a capture.** Both halves already exist and are **frozen**. This
> skill **stitches, reconciles, and exposes** them — it **never re-authors either half**
> (`personas/02-po.md` §2/§10/§11, `templates/04-prd.md`). It **invents no facts**: every
> product fact traces to the RP, every technical fact to the TA. The only *new* writing is
> composition (the executive summary), combination (the consolidated risk view), and
> reconciliation (the scope table).

This skill is **portable and repo-independent**. Everything it needs is bundled here. Pass
paths into agents; never let them assume a location.

## STOP — this is an execution contract, not a description

The rest of this file reads like a specification. It is not. It is a set of actions *you must
take by spawning agents*. The dominant failure mode of this skill is that you read it,
understand the merge, and then **produce the PRD yourself inline** — then narrate a pipeline
that never ran. A correct run has Agent tool calls in the transcript. A narrated pipeline with
zero Agent calls is a **failed run, even if the document looks right.**

Before doing anything else, bind yourself to these invariants:

1. **You are read-only on every shared artifact.** Do not use Write or Edit on `prd.md`,
   `qa-log.md`, `contract.lock.md`, `sources/`, or anything under `output/`. Each file gets
   written only by its single writer agent (the document **exclusively** by `hsb-doc-updater`;
   the ledger **exclusively** by `hsb-ledger-writer`). If you are about to type document
   content yourself, stop — that is the bug.
2. **Delegation is mandatory, not optional.** "Run the merge" means *spawn the subagents via
   the Agent tool*. It never means "read the two halves and write the PRD yourself."
3. **Independent agents go out in ONE message.** When agents have no dependency, emit their
   Agent calls in the **same assistant turn** so they run concurrently. The parallel groups
   are: Setup `hsb-source-indexer` ∥ `hsb-template-analyst`; Inherit **fan-out** —
   `hsb-stage-inheritor` `PART: A` ∥ `PART: B`; Synthesize **fan-out** — `hsb-reconciler`
   (scope) ∥ `hsb-synthesizer` × {`consolidated-risk`, `inherited-readiness`, `exec-summary`}
   ∥ `hsb-section-drafter` (`handoff-gate`); Production `hsb-translator` ∥
   `hsb-visual-enricher` ∥ `hsb-finalizer`.
4. **Resolve the path before you draft.** Phase 0 decides escalated vs. no-escalation vs.
   **veto halt** from the works index. On a veto, **stop before creating the `prd/` phase** —
   there is no PRD on an infeasible TA.
5. **Invent nothing; preserve authorship.** Part A is the PO's, Part B is the CTO's. The
   feasibility verdict is **carried from the TA, never re-decided**. A fact in neither frozen
   source belongs upstream, not in the merge.
6. **Track the run with TodoWrite.** Create the checklist below *before* Phase 1.

**Headless / batch changes none of this.** "No live PO/CTO" means *no questions* and *honest
dispositions* — it does **not** mean skip the agents or skip the sign-off (the output is then
"draft PRD for PO+CTO sign-off," never an accepted PRD).

### The phase checklist (TodoWrite this before Phase 1)

- [ ] Phase 0 · select initiative; locate the **frozen RP** (works index: `produces: readiness-package`); resolve the **escalation state** (signed TA → escalated · `not_requested` → RP-alone · debt open → STOP run tech-assessment first · **vetoed → HALT, signal PO to re-scope**); confirm language
- [ ] Phase 1 · resolve `prd/`; spawn `hsb-template-validator`; gate on pass
- [ ] Phase 1 · **same message:** `hsb-source-indexer` (RP + TA + intake-record) ∥ `hsb-template-analyst`
- [ ] Phase 2 · **same message (fan-out):** `hsb-stage-inheritor` `PART: A` (RP → Part A) ∥ `PART: B` (TA → Part B, or N/A dispositions); also carry `effort-cost` + `success-metrics`; route → `hsb-ledger-writer` → `hsb-doc-updater`
- [ ] Phase 3 · **same message (fan-out):** `hsb-reconciler` (`scope-reconciliation` + reconciled `a-scope`) ∥ `hsb-synthesizer` × {`consolidated-risk`, `inherited-readiness`, `exec-summary`} ∥ `hsb-section-drafter` (`handoff-gate`); route all → `hsb-doc-updater`
- [ ] Phase 4 · loop: `hsb-confidence-auditor` (incremental `SECTIONS`; flags A↔B contradictions) → (on conflict) `hsb-reconciler` → (fallback) `hsb-question-strategist` → PO confirms product half · CTO co-signs technical half · **dual sign-off** → `hsb-ledger-writer` → `hsb-doc-updater` until `handoffReady`
- [ ] Phase 5 · spawn `hsb-humanizer` (await — it writes the copy the rest read)
- [ ] Phase 5 · **same message:** `hsb-translator` ∥ `hsb-visual-enricher` ∥ `hsb-finalizer`
- [ ] Phase 5 · spawn `hsb-packager`; record the front in the index (`produces: prd`, escalation flag, carried verdict, `delivered-to-pm`); report to the PO (+ CTO)

## First, read these (once per run)

### The canonical personas (authoritative source)

- `teamwork-process/personas/02-po.md` — the **PO persona**: the artifact chain (§2 — the RP
  and the TA are separate artifacts that **merge into the PRD**), the lateral relationship
  with the CTO (§10 — `PRD = RP + Technical Assessment`), the deliverable and the handoff to
  the PM (§11), and the "PM first-version acceptance" mirror (§9). This skill operationalizes
  the PO's **merge + handoff** mandate.
- `teamwork-process/personas/03-cto.md` — the **CTO persona**, for the technical half: the TA
  is the CTO's signed artefact; the feasibility verdict is the CTO's first-class decision,
  **carried into the PRD, never re-decided** here.

### PRD-specific references

- [`references/orchestration.md`](references/orchestration.md) — the phase flow, the full agent
  roster (all **reused** — no new agents), phase assignments, single-writer ownership, and the
  phase-folder layout. This is your playbook.
- [`references/merge.md`](references/merge.md) — the governing method: preserve authorship,
  invent nothing; inherit-then-synthesize-then-confirm; who the orchestrator talks to; the two
  paths; the consistency invariants.
- [`references/reconciliation.md`](references/reconciliation.md) — scope reconciliation, the
  consolidated risk view, the **no-escalation path** (PRD from the RP alone), and the **veto
  halt** (no PRD on `Infeasible as scoped`).
- [`references/inheritance.md`](references/inheritance.md) — the RP/TA → PRD section mapping:
  exactly which source section each PRD `id` is carried from, and what the Inheritor preserves.
- [`references/handoff.md`](references/handoff.md) — the dual sign-off, the `handoffReady`
  freeze gate, the handoff checklist, and the PM-rejection / version-bump loop.

### Shared engine references (reused unchanged)

- [`../origination-brainstorm/references/contract-and-template.md`](../origination-brainstorm/references/contract-and-template.md) —
  template annotation format (`origination:` markers, incl. `derived` + `inputs`),
  `contract.lock.md` derivation, threshold X, restart-on-change rule.
- [`../origination-brainstorm/references/ledger-schema.md`](../origination-brainstorm/references/ledger-schema.md) —
  `qa-log.md` schema.
- [`../origination-brainstorm/references/initiatives.md`](../origination-brainstorm/references/initiatives.md) —
  initiatives root resolution, resolve-or-select, the `.teamwork/<initiative>/` layout, the
  works + definitions index (`initiative.json`), and brokering. The PRD runs as the `prd/`
  **phase**; it discovers the RP (the phase whose `produces` is `readiness-package`) and the TA
  (the phase whose `produces` is `technical-assessment`) from the works index, and records the
  `prd` it produces back into the index on freeze.
- [`../origination-brainstorm/references/writing-integrity.md`](../origination-brainstorm/references/writing-integrity.md) —
  single-writer rule, read-modify-write, `rev` marker, no-truncation sentinel.
- [`../origination-brainstorm/references/grounding.md`](../origination-brainstorm/references/grounding.md) —
  quality calibration against the golden exemplar.
- [`../origination-brainstorm/references/questioning-method.md`](../origination-brainstorm/references/questioning-method.md) —
  how to ask (`open` / `choice`), dispositions, the `AskUserQuestion` protocol. The PRD rarely
  asks — questions are a fallback fired only on a genuine merge conflict or a missing source.
- [`../readiness-package/references/escalation.md`](../readiness-package/references/escalation.md) —
  the RP↔TA bridge (`TechAssessmentRef`): how this skill reads whether a TA was owed, signed,
  not requested, or vetoed.

### Default template and exemplar

- [`assets/target-template.prd.md`](assets/target-template.prd.md) — the default PRD template
  (annotated with `origination:` markers).
- [`assets/target-template.prd.guide.md`](assets/target-template.prd.guide.md) — companion
  filling guide; inject alongside the template when spawning agents.
- [`assets/golden-example.md`](assets/golden-example.md) — self-contained calibration exemplar
  (a merged PRD from an escalated demand — RP + a `Feasible with caveats` TA).

## The principle that makes parallelism safe

**One writer per file.** Each mutable artifact has exactly one writer agent; every other agent
is read-only and returns *proposals/findings/verdicts* that **you** route to the single
writer. Concurrent writes are impossible by construction.

The writers that matter most:

- `prd.md` — sole writer: **`hsb-doc-updater`**
- `qa-log.md` — sole writer: **`hsb-ledger-writer`**

All the merge proposers (`hsb-stage-inheritor`, `hsb-synthesizer`, `hsb-reconciler`,
`hsb-section-drafter`, `hsb-confidence-auditor`, `hsb-evidence-extractor`,
`hsb-question-strategist`) are **read-only proposers** that return structured proposals to you;
they never touch shared files directly.

Every writer re-reads the file before editing (read-modify-write), merges changes keyed by
stable id, never clobbers, and the document ends with a `<!-- END OF DOCUMENT -->` sentinel the
Auditor checks for truncation. Full rules:
[`../origination-brainstorm/references/writing-integrity.md`](../origination-brainstorm/references/writing-integrity.md).

## The agents you spawn (`subagent_type`)

The PRD reuses the **existing roster** — it introduces **no new agents** (the roster is
phase-agnostic; it specializes through the PRD template, guide, and references). The merge maps
onto three engine specialists already in the roster: the **Inheritor** carries each half
forward, the **Synthesizer** composes the `derived` sections, and the **Reconciler** resolves
the scope.

| Phase | `subagent_type` | Role here |
|---|---|---|
| 1 | `hsb-template-validator` | validate the PRD template (read-only) |
| 1 | `hsb-source-indexer` | copy the PM's extra files into `sources/`; reference the RP + TA + intake-record in place (canonical path, not copied) in `sources-index.md` (writer) |
| 1 | `hsb-template-analyst` | derive `contract.lock.md`, hash, restart-on-change (writer) |
| 2 | `hsb-stage-inheritor` | read-only proposer — carries the RP into Part A (`PART: A`) and the TA into Part B (`PART: B`); **fanned out one per part** |
| 3 | `hsb-synthesizer` | read-only proposer — composes the `derived` sections (`exec-summary`, `consolidated-risk`, `inherited-readiness`); **fanned out one per `SECTION`** |
| 3/4 | `hsb-reconciler` | read-only proposer — produces `scope-reconciliation` + the reconciled `a-scope`; resolves A↔B conflicts the Auditor flags |
| 3 | `hsb-section-drafter` | read-only proposer — drafts `handoff-gate` and any non-inherited prose; **fanned out one per `SECTION`** |
| 2-4 | `hsb-ledger-writer` | commit questions/answers/proposals/sign-off to `qa-log.md` (writer) |
| 2-4 | `hsb-doc-updater` | write and update `prd.md` (`DOC`) (writer) |
| 4 | `hsb-confidence-auditor` | re-score sections + gate verdict; **flag A↔B contradictions** (read-only) |
| 4 | `hsb-question-strategist` | propose questions (**fallback only** — genuine conflict / missing source) (read-only) |
| 4 | `hsb-evidence-extractor` | satisfy an open question from the indexed RP / TA (read-only) |
| 4 | `hsb-decisions-keeper` | record the PRD freeze + dual sign-off as a cross-phase decision (writer; `DEFINITIONS_DIR`; optional) |
| 4 | `hsb-gap-reporter` | write the live gap map `prd-report.md` (writer; optional) |
| 5 | `hsb-humanizer` | write `output/humanized.md` (writer) |
| 5 | `hsb-translator` | write `output/translated.<lang>.md` (writer) |
| 5 | `hsb-visual-enricher` | write `output/enriched.md` (writer) |
| 5 | `hsb-finalizer` | externalize the clean, printable `final/<project>-NNN.md` (writer; needs `PROJECT_SLUG`) |
| 5 | `hsb-packager` | write `output/manifest.md` (writer) |

Full roster with writer-ownership and phase assignments:
[`references/orchestration.md`](references/orchestration.md).

When spawning, inject the paths each agent needs: `SKILL_DIR`, `PHASE_DIR` (`prd/`), `TEMPLATE`
(`prd.md`'s template), `DOC` (`prd.md`), and the companion guide. The Inheritor also takes
`PART`; the Synthesizer and Section Drafter take `SECTION`; the Confidence Auditor takes
`SECTIONS`; the Finalizer needs `PROJECT_SLUG`. **Run independent agents in the same turn** so
they execute in parallel.

**You broker everything above `PHASE_DIR`** (the initiative-level `initiative.json`,
`glossary.md`, `decisions.md`). Read the works index to find the RP (`artifacts.canonical` /
`final` of the phase that `produces` `readiness-package`) and the TA (the phase that `produces`
`technical-assessment`), hand those to the Source Indexer; seed each phase's read-only
`PHASE_DIR/glossary.md`; spawn the Glossary Keeper with `DEFINITIONS_DIR`; update the index
when the front starts and freezes. See
[`../origination-brainstorm/references/initiatives.md`](../origination-brainstorm/references/initiatives.md).

## Authoring model — inherit-then-synthesize, then confirm

**The screen should not look like a blank form** — it should look like the system already
assembled the PRD from the two frozen halves and is asking the PO to confirm it. The pipeline
pre-fills **every section** before the PO/CTO sees it:

- **`hsb-stage-inheritor`** carries the RP forward into Part A and the TA into Part B (the
  verdict, the constraints, the risks) at preserved confidence, tagged `Origin: inherited`.
- **`hsb-synthesizer`** composes the `derived` sections — the executive summary, the
  consolidated risk view, the inherited-readiness view — from the inherited halves, tagged
  `Origin: synthesized` at partial confidence with a hint.
- **`hsb-reconciler`** produces the scope reconciliation and proposes the reconciled `a-scope`.
- On the no-escalation path, Part B is the honest-N/A disposition (`Disposition: decided`).

The **PO** then confirms the product half and the synthesized/reconciled sections; the **CTO**
co-signs the technical half and the feasibility verdict carried into `sign-off`. Origin
lifecycle: `inherited` / `synthesized` → PO/CTO review → `po_authored` / `cto_authored`.
**Questions are a fallback** (the PRD rarely asks — both halves are frozen), fired only on a
genuine merge conflict the sources cannot settle, or a missing source section.

## Modes

**Fresh** (default) — the initiative has a frozen `readiness/` phase (and, when escalated, a
signed `assessment/` phase) and no `prd/` document yet. Run the full merge: Phase 0 (locate the
RP + resolve the escalation state) → Phase 1 Setup → Phase 2 Inherit both halves → Phase 3
Synthesize & reconcile → Phase 4 Confirm loop + dual sign-off → Phase 5 Production + wrap.

**Revisit** — a `prd/` phase exists. If the **PM rejected** the PRD with specific gaps, re-open
only the affected half, address the named gaps, bump the version, and re-freeze (see
[`handoff.md`](handoff.md) § The PM acceptance loop). If an upstream half changed (the RP was
re-frozen or the TA re-signed after a veto), re-run the merge against the new sources and bump
the version. If a `prd.md` exists unfrozen, resume: spawn the Auditor to re-score, re-open the
confirm loop only on weak/unconfirmed sections.

**Batch / headless** — frozen RPs (+ TAs) and no live PO/CTO. For each, run inherit → synthesize
→ reconcile → Doc Updater → Auditor under honest dispositions. With no PO/CTO to confirm, an
honest disposition clears the gate, but the **sign-off is never auto-committed** — the output is
always "draft PRD for PO+CTO sign-off." These runs are embarrassingly parallel.

## Language

Detect the language of the PO's opening statement and mirror it for the conversation and the
captured document. **Default en-US when ambiguous** (consistent with the engine). The
`hsb-translator` produces any additional requested languages (e.g. pt-BR) as separate `output/`
files. Keep section structure identical across languages. Machine-readable field labels, the
`Origin` / `disposition` enum *labels*, and `origination:` annotation markers stay in the
engine's canonical form regardless of output language; the human-readable feasibility `verdict`
and `Status` values are rendered in the document's language.

## The boundary — what the PRD is and is not

The PRD **is** the merge: stitched halves (Part A from the RP, Part B from the TA), reconciled
scope, consolidated risks, firm effort, dual sign-off, and a checkable handoff gate. The PRD
**is not** a place to redefine the product (that is the RP), to re-judge feasibility (that is
the TA), or to start downstream technical breakdown (that is the Tech Lead, after the PM plans).
It **invents no facts** — every fact traces to a frozen source. It opens the downstream because
the PM can accept it without returning it.

A **vetoed** TA never produces a PRD: the merge halts in Phase 0 and the orchestrator signals
the PO to revise the RP scope and re-escalate (see [`reconciliation.md`](reconciliation.md) §
The veto halt).

## Installing in other projects

This skill ships as part of the **`hsb-teamwork` Claude Code plugin** (this folder is
`plugins/hsb-teamwork/skills/prd-generation/` inside it). Install it from the `hsb-tech`
marketplace:

```
/plugin marketplace add hugo-hsbtech/teamwork-process-marketplace
/plugin install hsb-teamwork@hsb-tech
```

Invoke it as `/hsb-teamwork:prd-generation`.

The plugin is self-contained (template, guide, and exemplar bundled under `assets/`), so no
repository content is required at runtime. The RP and TA are discovered from the selected
initiative's works index (the phases that `produce` a `readiness-package` and a
`technical-assessment`). The initiatives root resolves via `$TEAMWORK_HOME` → git root +
`/.teamwork` → cwd, consistent with the rest of the engine. The template is swappable — pass a
custom PRD template path as `TEMPLATE`.

## Bundled resources

| Path | Purpose |
|---|---|
| `references/orchestration.md` | Phase flow, full agent roster (all reused) + phase assignments, single-writer ownership, folder layout |
| `references/merge.md` | The governing method — preserve authorship, invent nothing, inherit-then-synthesize, the two paths, the consistency invariants |
| `references/reconciliation.md` | Scope reconciliation, consolidated risk, the no-escalation path, the veto halt |
| `references/inheritance.md` | RP/TA → PRD section mapping, what `hsb-stage-inheritor` preserves |
| `references/handoff.md` | The dual sign-off, the `handoffReady` gate, the PM acceptance / rejection loop |
| `assets/target-template.prd.md` | Default PRD template (annotated) |
| `assets/target-template.prd.guide.md` | Companion filling guide |
| `assets/golden-example.md` | Self-contained calibration exemplar |
