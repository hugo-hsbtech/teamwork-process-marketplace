# readiness-package

> **Part of the `hsb-teamwork` toolkit.** `readiness-package` is the second skill,
> invoked as `/hsb-teamwork:readiness-package`. It runs the Product Owner's full
> two-act journey on a demand and produces the PO's artefacts. Sibling steps
> planned in the same plugin: `tech-assessment`, `prd-generation` — each a skill
> under `/hsb-teamwork:<skill>`, reusing this skill's engine.

A portable, PO-facing Claude skill that runs the **Product Owner's two acts**
(`teamwork-process/personas/02-po.md` §3) on an origination-record:

1. **Act 1 — Triage.** Score the demand against the triage criteria and commit a
   routing decision — `Product Ready` / `Discovery` / `Backlog` / `Reject` —
   recorded as an **Intake Record** (`INT-AAAA-NNN`). Only `Product Ready` opens
   Act 2; the other three short-circuit (recorded, then stop). This gate is what
   keeps the skill from pre-interpreting a demand as product before it is triaged —
   and it is the main efficiency win, since most demands never pay the RP cost.
2. **Act 2 — Rationalization.** Turn the `Product Ready` demand into a fully-frozen
   **Readiness Package (RP)** (`RP-AAAA-NNN`): the Product Owner's rationalization
   artefact.

The RP contains: executive summary, problem/context, objectives, personas,
scope in/out, business rules, user stories with Given/When/Then acceptance
criteria, NFRs, edge cases, metrics, release criteria, and risks.

> This README is the orientation. The authoritative spec lives in
> [`SKILL.md`](SKILL.md) (the orchestrator) and [`references/`](references/).

## The big idea

**Triage first, rationalize only what passes.** Act 1 asks the structured
triage questions and commits a routing decision; only a `Product Ready` demand
enters Act 2's expensive pipeline. In Act 2 the pipeline **pre-fills every section
before the PO sees the document** — the screen looks like the system already
rationalized the demand and is asking for the PO's judgment, not like a blank
form. The PO's job is to **review, edit, justify, and freeze**.

Principles underpinning correctness, speed, and parallelism:

1. **Triage gate (Act 1).** `hsb-triage-assessor` scores the criteria from the
   origination-record; the orchestrator asks the PO only the criteria it could not
   settle, and the PO commits the routing decision. `Discovery`/`Backlog`/`Reject`
   short-circuit — no RP drafting runs.
2. **Draft-then-confirm (Act 2).** `hsb-stage-inheritor` carries inheritable sections
   forward from the origination-record at preserved confidence; `hsb-section-drafter`
   proposes first drafts for the new product sections — **fanned out one per section
   in parallel** so the draft pass is fast. Every section has an entry —
   `inherited`, `ai_drafted`, or an honest `discovery` — before the PO opens the
   document. Questions there are a fallback, not the primary mode.
3. **One writer per file.** `intake-record.md` (Act 1) and `readiness-document.md`
   (Act 2) are written exclusively by `hsb-doc-updater`; `qa-log.md` exclusively by
   `hsb-ledger-writer`. The stage-agnostic proposers this skill drives
   (`hsb-triage-assessor`, `hsb-stage-inheritor`, `hsb-section-drafter`,
   `hsb-escalation-flagger`) are read-only; the orchestrator routes their proposals
   through the single writers, which is what makes the fan-out safe.
4. **Enriched, readable output (Phase B4).** The frozen RP is not the last word — the
   production phase turns it into deliverables that meet the same reading-quality and
   didactic bar as the origination-record. `hsb-humanizer` produces the clean copy;
   `hsb-enrichment-analyst` catalogs every visual the data **already supports** into
   a sourced, citation-carrying `enrichment-plan.md`; `hsb-visual-enricher` renders
   that plan (Mermaid-native charts, scope/persona/business-rule/metrics visuals) so
   the package reads at a glance and never invents a number. Deciding *what* to
   visualize separately from *how* to render it is what keeps the enrichment
   auditable — without the Analyst, the enricher runs blind and the RP ships
   un-enriched.

## How to invoke

```
/hsb-teamwork:readiness-package
```

When you invoke it, it resolves the **initiative** to run in (confirm the latest
open one or pick from the open list), then reads the initiative's **works +
definitions index** (`initiative.json`) to discover the origination-record to
triage — the phase whose `produces` is `origination-record` — plus any debts prior
fronts left open and the shared definitions. Act 1 runs as the `intake/` **phase**
(producing the Intake Record); only if triage decides `Product Ready` does Act 2 run
as the `readiness/` **phase**, recording its outputs and the owed Technical Assessment
back into the index on freeze. The output language defaults to pt-BR unless you
specify otherwise.

## Input

A **candidate origination-record** — the `target-document.md` (or its
`output/humanized.md` / `final/<project>-NNN.md`) in the initiative's `origination/`
phase, produced by `/hsb-teamwork:origination-brainstorm`. The skill triages it in
Act 1; it does **not** assume it is already `Product Ready` — that is the routing
decision the PO commits at the gate.

The PO provides:
- The initiative to run in (its `origination/` phase is the origination-record; an
  external origination-record path may be given instead).
- Optionally: additional files to index (specs, research, prior ADRs).
- Optionally: a custom RP template (if not using the default).

## Outputs

All artifacts land in the initiative's `readiness/` phase, `INITIATIVE_DIR/readiness/`:

```
<INITIATIVE_DIR>/readiness/
├── contract.lock.md            # derived RP contract + template hash
├── sources-index.md            # index of ingested inputs (incl. origination-record)
├── sources/                    # normalized input files
├── qa-log.md                   # Q&A ledger (questions + rationale + PO answers)
├── readiness-document.md       # the RP being filled and frozen
├── glossary.md                 # brokered read-only copy of the initiative's shared glossary
├── readiness-report.md         # live gap map (optional)
├── output/
│   ├── humanized.md            # canonical clean copy
│   ├── translated.pt-BR.md     # translated variant (or the confirmed output language)
│   ├── enrichment-plan.md      # sourced catalog of visual opportunities (insumo for the enricher)
│   ├── enriched.md             # visually enriched — the plan rendered (scope table, persona map, etc.)
│   └── manifest.md             # index of all artifacts + freeze state + TA flag
└── final/                      # the clean, printable final deliverable(s)
    └── <project>-NNN.md        # externalized, scaffolding-stripped, counter-suffixed
```

The shared `glossary.md` and `decisions.md`, and the `initiative.json` works +
definitions index, live one level up at the **initiative root** (`INITIATIVE_DIR/`),
not inside `readiness/` — they are shared across every front. See
[`../origination-brainstorm/references/initiatives.md`](../origination-brainstorm/references/initiatives.md).

## The Technical Assessment boundary

The RP stops at product definition. Technical viability and architectural
constraints belong to the CTO's **Technical Assessment** — a separate artefact.

`hsb-escalation-flagger` detects architectural triggers (infrastructure
changes, multi-tenancy, AI/runtime behaviour, security/auth, external integrations
with unknowns) and proposes the compound shape `TechAssessmentRef.status =
requested` AND `disposition = deferred` — the `deferred` disposition is what the
manifest propagates downstream and what makes the freeze provisional.

**Current state — provisional freeze:** the `tech-assessment` skill does not yet
exist. When a Technical Assessment is owed, the RP freezes **provisionally**: the
product sections are frozen and `output/manifest.md` is flagged
`tech-assessment-ref: deferred (TA pending — out of current tooling scope)`, so
the downstream PRD/PM handoff knows the Assessment is still owed.

When the `tech-assessment` skill lands, the freeze gate will be tightened to
require a signed TA. Until then, the provisional-freeze path is the intended
behavior and is documented in
[`references/escalation.md`](references/escalation.md).

## Modes

- **Fresh** (default) — origination-record exists, no triage decision yet. Full
  journey: Act 1 triage → gate → (if `Product Ready`) Act 2 rationalization.
- **Triage-only** — run Act 1 and stop at the gate regardless of decision (e.g.
  batch-triaging a queue). Produces Intake Records without paying the Act 2 cost.
- **Revisit** — existing `intake/` or `readiness/` phase. Resume at Act 2 if triage
  already decided `Product Ready`; re-score an existing RP and re-open questions only
  on weak sections; or re-run Act 1 to re-open a triage decision.
- **Batch / headless** — a set of origination-records, no live PO. Triage under honest
  dispositions; only `Product Ready` ones run the no-question draft path; output is
  always "draft for review," never frozen on its own.

## Using it elsewhere

In **this repo** it already works — symlinked into `.claude/` from the plugin.

To reuse it in **other projects**, install it as a Claude Code plugin:

```
/plugin marketplace add hugo-hsbtech/teamwork-process-marketplace
/plugin install hsb-teamwork@hsb-tech
```

Then invoke it as `/hsb-teamwork:readiness-package`.

## Layout (within the plugin)

```
plugins/hsb-teamwork/
├── skills/readiness-package/
│   ├── SKILL.md                                    # orchestrator spec
│   ├── README.md                                   # this file
│   ├── references/
│   │   ├── triage.md                               # Act 1 — criteria, decision model, gate, short-circuit
│   │   ├── orchestration.md                        # phases (both acts), roster, single-writer rule
│   │   ├── drafting.md                             # triage-first questioning + draft-then-confirm
│   │   ├── inheritance.md                          # origination-to-RP section mapping
│   │   └── escalation.md                           # TA triggers, freeze gate, provisional path
│   └── assets/
│       ├── target-template.intake-record.md        # default Intake Record template (Act 1, annotated)
│       ├── target-template.intake-record.guide.md  # companion guide for the Intake Record
│       ├── target-template.readiness-package.md    # default RP template (annotated)
│       ├── target-template.readiness-package.guide.md  # companion filling guide
│       └── golden-example.md                       # calibration exemplar
└── agents/hsb-*.md                                 # shared engine agents (incl. hsb-triage-assessor)
```

The stage-agnostic agents this skill drives (`hsb-triage-assessor`,
`hsb-stage-inheritor`, `hsb-section-drafter`, `hsb-escalation-flagger`) are defined in
`agents/hsb-*.md` alongside the rest of the shared roster.
