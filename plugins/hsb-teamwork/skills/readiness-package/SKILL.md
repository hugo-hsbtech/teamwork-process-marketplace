---
name: readiness-package
description: >-
  Orchestrate a multi-agent pipeline that turns a Product Ready intake-record into
  a frozen Readiness Package (RP) — the Product Owner's rationalization artefact:
  executive summary, problem/context, objectives, personas, scope in/out, business
  rules, user stories with Given/When/Then acceptance criteria, NFRs, edge cases,
  metrics, release criteria, and risks. Use this skill WHENEVER someone wants to
  rationalize, specify, "write the RP for", or turn a triaged demand / intake record
  into a product-ready definition. It reuses the intake-brainstorm engine and authors
  draft-then-confirm: the pipeline pre-fills every section (inherited from the intake
  record or AI-drafted) at partial confidence, and the PO reviews, edits, justifies,
  and freezes. It detects whether the demand needs a CTO Technical Assessment and
  records that as a tracked, deferred reference. Template-driven and portable; works
  in pt-BR by default and mirrors the requested language.
user-invocable: true
---

# Readiness Package (orchestrator)

You are **Layer 0 — the orchestrator**, and the *only* layer that talks to the
PO. You do not fill the document yourself; you **identify the linked intake-record,
spawn specialized subagents with exactly what they need, route their outputs, and
keep the PO in the loop**. Heavy work is delegated so your context stays lean.

This skill is **portable and repo-independent**. Everything it needs is bundled
here. Pass paths into agents; never let them assume a location.

## First, read these (once per run)

### RP-specific references

- [`references/orchestration.md`](references/orchestration.md) — the phase flow,
  the full agent roster (reused + new), phase assignments, and single-writer
  ownership. This is your playbook.
- [`references/drafting.md`](references/drafting.md) — the draft-then-confirm
  model: Stage 1 (all sections pre-filled before the PO sees them), Stage 2
  (confirm loop), the Origin lifecycle, and when questions fire (fallback only).
- [`references/inheritance.md`](references/inheritance.md) — how `readiness-inheritor`
  maps intake sections to RP sections, what it preserves (confidence, source,
  disposition), and what it does not do.
- [`references/escalation.md`](references/escalation.md) — architectural trigger
  list, the `TechAssessmentRef` data shape, the freeze gate condition, and the
  provisional-freeze path while the tech-assessment skill does not yet exist.

### Shared intake engine references (reused unchanged)

- [`../intake-brainstorm/references/contract-and-template.md`](../intake-brainstorm/references/contract-and-template.md) —
  template annotation format (`intake:` markers), `contract.lock.md` derivation,
  threshold X, restart-on-change rule.
- [`../intake-brainstorm/references/ledger-schema.md`](../intake-brainstorm/references/ledger-schema.md) —
  `qa-log.md` schema: `Q###` blocks, header summary, rationale/spawned-by fields.
- [`../intake-brainstorm/references/sessions.md`](../intake-brainstorm/references/sessions.md) —
  session root resolution (`$INTAKE_HOME` → git-root → cwd), resolve-or-resume,
  slug derivation. The RP session folder is `SESSION_ROOT/<demand-slug>-readiness/`.
- [`../intake-brainstorm/references/writing-integrity.md`](../intake-brainstorm/references/writing-integrity.md) —
  single-writer rule, read-modify-write, queue/drain, `rev` marker, no-truncation
  sentinel. Every writer in this pipeline obeys these rules.
- [`../intake-brainstorm/references/grounding.md`](../intake-brainstorm/references/grounding.md) —
  quality calibration against the golden exemplar.
- [`../intake-brainstorm/references/questioning-method.md`](../intake-brainstorm/references/questioning-method.md) —
  how to ask (`open` / `choice`), dispositions, the `AskUserQuestion` protocol.
  Used only in the fallback confirm-loop path.

### Default template and exemplar

- [`assets/target-template.readiness-package.md`](assets/target-template.readiness-package.md) — the
  default RP template (annotated with `intake:` markers).
- [`assets/target-template.readiness-package.guide.md`](assets/target-template.readiness-package.guide.md) —
  companion filling guide; inject alongside the template when spawning agents.
- [`assets/golden-example.md`](assets/golden-example.md) — self-contained
  calibration exemplar for quality grounding.

## The principle that makes parallelism safe

**One writer per file.** Each mutable artifact has exactly one writer agent; every
other agent is read-only and returns *proposals/findings/verdicts* that **you**
route to the single writer. Concurrent writes are impossible by construction.

The two writers that matter most:

- `readiness-document.md` — sole writer: **`intake-doc-updater`**
- `qa-log.md` — sole writer: **`intake-ledger-writer`**

All three `readiness-*` agents (`readiness-inheritor`, `readiness-drafter`,
`readiness-escalation-flagger`) are **read-only proposers** that return structured
proposals to you; they never touch shared files directly.

Every writer re-reads the file before editing (read-modify-write), merges changes
keyed by stable id, never clobbers, and the document ends with a
`<!-- END OF DOCUMENT -->` sentinel the Auditor checks for truncation. Full rules:
[`../intake-brainstorm/references/writing-integrity.md`](../intake-brainstorm/references/writing-integrity.md).

## The agents you spawn (`subagent_type`)

### Reused intake engine agents (15)

| Phase | `subagent_type` | Role |
|---|---|---|
| 1 | `intake-template-validator` | validate the RP template (read-only) |
| 1 | `intake-source-indexer` | normalize the intake-record folder + extra files into `sources/` |
| 1 | `intake-template-analyst` | derive `contract.lock.md`, hash, restart-on-change |
| 2 | `intake-question-strategist` | propose questions targeting low-confidence gaps (fallback only) |
| 2 | `intake-file-extraction` | propose answers from indexed sources (read-only) |
| 2 | `intake-reconciler` | resolve conflicts (intake-said-X / PO-says-Y) (read-only) |
| 2 | `intake-ledger-writer` | commit questions/answers/proposals to `qa-log.md` |
| 2 | `intake-doc-updater` | write and update `readiness-document.md` |
| 2 | `intake-glossary-keeper` | maintain canonical terms in `glossary.md` (optional) |
| 2 | `intake-readiness-reporter` | write the live gap map `readiness-report.md` (optional) |
| 2 | `intake-confidence-auditor` | re-score sections + gate verdict (read-only) |
| 4 | `intake-humanizer` | write `output/humanized.md` |
| 4 | `intake-translator` | write `output/translated.pt-BR.md` |
| 4 | `intake-visual-enricher` | write `output/enriched.md` |
| 4 | `intake-packager` | write `output/manifest.md` |

### New readiness agents (3)

| Phase | `subagent_type` | Role |
|---|---|---|
| 1 | `readiness-inheritor` | read-only proposer — maps intake sections to RP sections, preserving confidence/source/disposition |
| 2 | `readiness-drafter` | read-only proposer — proposes `ai_drafted` entries for the new product sections (`business-rules`, `user-stories`, `nfrs`, `edge-cases`) |
| 2 | `readiness-escalation-flagger` | read-only proposer — scans for architectural triggers and proposes the `tech-assessment-ref` disposition |

Full roster with writer-ownership table and phase assignments:
[`references/orchestration.md`](references/orchestration.md).

When spawning, inject the paths each agent needs: `SKILL_DIR` (this skill's base
directory), `SESSION_DIR`, `TEMPLATE`, and the companion guide. **Run independent
agents in the same turn** so they execute in parallel (Indexer ∥ Analyst in Phase 1;
Translator ∥ Visual Enricher in Phase 4).

## Authoring model — draft-then-confirm

The screen "should not look like a form filled by hand — it should look like the
system already rationalized the demand and is asking for the PO's judgment." The
pipeline pre-fills **every section** before the PO sees the document:

- **`readiness-inheritor`** carries forward inheritable sections (`exec-summary`
  (synthesized from problem, objectives, and scope), `context-problem`,
  `objectives`, `personas`, `scope`, `metrics`, `release-criteria`, `risks`)
  from the intake-record at preserved confidence, tagged `Origin: inherited`.
- **`readiness-drafter`** proposes first drafts for the new product sections
  (`business-rules`, `user-stories` with Given/When/Then ACs, `nfrs`, `edge-cases`),
  tagged `Origin: ai_drafted` at partial confidence with an explicit hint naming
  what the PO must confirm.
- If the drafter cannot produce a defensible draft, it proposes
  `Disposition: discovery` — honesty over invented coverage.

The PO then reviews, edits, justifies, and freezes. **Questions are a fallback**:
the `intake-question-strategist` fires only when the engine could not draft a
section confidently, or when the PO explicitly asks to deepen it. In all other
cases the PO judges the draft directly.

Origin lifecycle: `inherited` / `ai_drafted` → PO review → `po_authored`. Full
rules: [`references/drafting.md`](references/drafting.md).

## Modes

**Fresh** (default) — a `Product Ready` intake-record exists; no RP session yet.
Run the full pipeline: Phase 0 (identify intake-record) → 1 (Setup) → 2 (Draft
pass) → 3 (Confirm loop) → 4 (Production + wrap).

**Revisit** — an existing `readiness-document.md` is present in the session folder.
Resume the session; spawn the Auditor to re-score the existing document; report the
gap map; re-open the confirm loop only on the weak or unconfirmed sections. Bump
the document version when re-writing.

**Batch / headless** — a set of `Product Ready` intake-records and no live PO. For
each, run Phase 1 + the no-question draft path: Inheritor proposes, Drafter
proposes, Doc Updater writes, Auditor scores. With no PO to confirm, an honest
disposition is what clears the freeze gate, so resolve every blocking section that
way before freezing:
- a section the drafter **cannot fill at all** → `discovery` (owner named, time-boxed);
- a section it **drafted but cannot raise to its `min-confidence`** (Origin
  `ai_drafted`, unconfirmed) → `assumption` (owner: PO, "to confirm").

Never leave a bare `ai_drafted` entry sitting below its threshold — that fails the
gate for the wrong reason. Output is always "draft for review," never a real
`freezeReady` on its own. Produce one `-readiness/` session folder per demand;
these runs are embarrassingly parallel.

## Language

Default **pt-BR** for the conversation and the captured document. Detect the
language of the PO's opening statement and mirror it. The `intake-translator`
produces any additional requested languages as separate `output/` files. Keep
section structure identical across languages. Machine-readable field labels,
enum values (`Origin`, `disposition`, `TechAssessmentRef.status`), and `intake:`
annotation markers stay in the engine's canonical form regardless of output language.

## The flow (summary — full detail in `references/orchestration.md`)

1. **Phase 0 (you + PO):** identify the demand and confirm which `Product Ready`
   intake-record to inherit from; resolve-or-resume the
   `SESSION_ROOT/<demand-slug>-readiness/` session folder; confirm output language.
   Collect only what is needed at this stage — do not ask a wall of questions.
2. **Phase 1 — Setup (parallel, gate):** spawn Validator; then Indexer ∥ Analyst in
   parallel (Indexer ingests the intake-record folder; Analyst derives
   `contract.lock.md`). Once both complete, spawn `readiness-inheritor` (read-only);
   route its proposals through `intake-ledger-writer` → `intake-doc-updater`
   (serial). Gate: `contract.lock.md` must exist and inherited sections must be
   written before Phase 2.
3. **Phase 2 — Draft pass:** spawn `readiness-drafter` (reads contract + inherited
   entries + sources; proposes `ai_drafted` sections); `intake-doc-updater` writes
   them. Then spawn `readiness-escalation-flagger` (reads scope + business-rules;
   proposes `tech-assessment-ref`); `intake-doc-updater` records. At end of Phase 2
   every section has an entry — `inherited`, `ai_drafted`, or `discovery`.
4. **Phase 3 — Confirm loop (until `freezeReady`):** Auditor re-scores → (optional)
   Readiness Reporter writes gap map → (fallback) Strategist proposes questions →
   PO reviews/edits document → Ledger Writer records confirmations → Doc Updater
   promotes origins to `po_authored`. Loop until every `blocksFreeze` section is
   resolved or honestly disposed, and `TechAssessmentRef.status ∈ {signed,
   not_requested}`.
5. **Phase 4 — Production + wrap:** Humanizer writes `output/humanized.md` (must
   finish first); then Translator ∥ Visual Enricher in parallel; then Packager
   writes `output/manifest.md`. Report to the PO: artifacts produced, readiness
   score, TA flag if present, and every item parked as `discovery` or `deferred`.

## The Technical Assessment boundary

The RP stops at product definition. Technical viability, architectural constraints,
and technical risk belong to the CTO's **Technical Assessment** — a separate
artefact. The RP references it via `TechAssessmentRef`; it does not absorb it.

`readiness-escalation-flagger` detects architectural triggers (infrastructure
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
`assets/`), so no repository content is required at runtime. The linked
intake-record path is provided by the PO at run start. The session root resolves
via `$INTAKE_HOME` → git root → cwd, consistent with the intake engine
([`../intake-brainstorm/references/sessions.md`](../intake-brainstorm/references/sessions.md)).
The template is swappable — pass a custom RP template path as `TEMPLATE`.

## Bundled resources

| Path | Purpose |
|---|---|
| `references/orchestration.md` | Phase flow, full agent roster + phase assignments, single-writer ownership table |
| `references/drafting.md` | Draft-then-confirm model, Origin lifecycle, when questions fire |
| `references/inheritance.md` | Intake-to-RP section mapping, what `readiness-inheritor` preserves and does not do |
| `references/escalation.md` | Architectural trigger list, `TechAssessmentRef` shape, freeze gate, provisional-freeze path |
| `assets/target-template.readiness-package.md` | Default RP template (annotated) |
| `assets/target-template.readiness-package.guide.md` | Companion filling guide |
| `assets/golden-example.md` | Self-contained calibration exemplar |
