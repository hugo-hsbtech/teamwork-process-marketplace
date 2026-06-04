# readiness-package

> **Part of the `hsb-teamwork` toolkit.** `readiness-package` is the second skill,
> invoked as `/hsb-teamwork:readiness-package`. It receives the output of
> `origination-brainstorm` and produces the PO's rationalization artefact. Sibling steps
> planned in the same plugin: `tech-assessment`, `prd-generation` — each a skill
> under `/hsb-teamwork:<skill>`, reusing this skill's engine.

A portable, PO-facing Claude skill that turns a **Product Ready origination-record** —
the triaged output of `/hsb-teamwork:origination-brainstorm` — into a fully-frozen
**Readiness Package (RP)**: the Product Owner's rationalization artefact.

The RP contains: executive summary, problem/context, objectives, personas,
scope in/out, business rules, user stories with Given/When/Then acceptance
criteria, NFRs, edge cases, metrics, release criteria, and risks.

> This README is the orientation. The authoritative spec lives in
> [`SKILL.md`](SKILL.md) (the orchestrator) and [`references/`](references/).

## The big idea

The pipeline **pre-fills every section before the PO sees the document** — the
screen looks like the system already rationalized the demand and is asking for
the PO's judgment, not like a blank form. The PO's job is to **review, edit,
justify, and freeze**.

Two principles underpin correctness and parallelism:

1. **Draft-then-confirm.** `hsb-stage-inheritor` carries inheritable sections
   forward from the origination-record at preserved confidence; `hsb-section-drafter`
   proposes first drafts for the new product sections. Every section has an
   entry — `inherited`, `ai_drafted`, or an honest `discovery` — before the PO
   opens the document. Questions are a fallback, not the primary mode.
2. **One writer per file.** `readiness-document.md` is written exclusively by
   `hsb-doc-updater`; `qa-log.md` is written exclusively by
   `hsb-ledger-writer`. The three stage-agnostic proposers this skill drives
   (`hsb-stage-inheritor`, `hsb-section-drafter`, `hsb-escalation-flagger`) are
   read-only; the orchestrator routes their proposals through the single writers.

## How to invoke

```
/hsb-teamwork:readiness-package
```

When you invoke it, it resolves the **initiative** to run in (confirm the latest
open one or pick from the open list). Readiness runs as the `readiness/` **phase**
of that initiative, inheriting from its `origination/` phase (the origination-record).
The skill resolve-or-resumes `INITIATIVE_DIR/readiness/` and defaults the output
language to pt-BR unless you specify otherwise.

## Input

A **Product Ready origination-record** — the `target-document.md` (or its
`output/humanized.md`) in the initiative's `origination/` phase, produced by
`/hsb-teamwork:origination-brainstorm` after the demand has been triaged to
`Product Ready` status.

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
├── glossary.md                 # canonical terms (optional)
├── readiness-report.md         # live gap map (optional)
└── output/
    ├── humanized.md            # canonical clean copy
    ├── translated.pt-BR.md     # translated variant (or the confirmed output language)
    ├── enriched.md             # visually enriched (scope table, persona map, etc.)
    └── manifest.md             # index of all artifacts + freeze state + TA flag
```

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

- **Fresh** (default) — origination-record exists, no RP yet. Full pipeline.
- **Revisit** — existing `readiness-document.md` in the `readiness/` phase folder. Re-score,
  report the gap map, re-open questions only on weak sections.
- **Batch / headless** — a set of origination-records, no live PO. No-question draft
  path; output is always "draft for review," never frozen on its own.

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
│   │   ├── orchestration.md                        # phases, roster, single-writer rule
│   │   ├── drafting.md                             # draft-then-confirm, Origin lifecycle
│   │   ├── inheritance.md                          # origination-to-RP section mapping
│   │   └── escalation.md                           # TA triggers, freeze gate, provisional path
│   └── assets/
│       ├── target-template.readiness-package.md    # default RP template (annotated)
│       ├── target-template.readiness-package.guide.md  # companion filling guide
│       └── golden-example.md                       # calibration exemplar
└── agents/hsb-*.md                                 # 16 shared engine agents
```

The three stage-agnostic agents this skill drives (`hsb-stage-inheritor`,
`hsb-section-drafter`, `hsb-escalation-flagger`) are defined in `agents/hsb-*.md`
alongside the rest of the shared roster.
