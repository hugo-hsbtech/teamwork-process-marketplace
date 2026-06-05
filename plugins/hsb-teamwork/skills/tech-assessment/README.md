# tech-assessment

> **Part of the `hsb-teamwork` toolkit.** `tech-assessment` is the third skill,
> invoked as `/hsb-teamwork:tech-assessment`. It runs the **CTO's journey** on an
> escalated, frozen Readiness Package and produces the **Technical Assessment (TA)** —
> the technical half that merges with the RP into the PRD. Sibling steps:
> `origination-brainstorm`, `readiness-package` (upstream) and `prd-generation`
> (planned) — each a skill under `/hsb-teamwork:<skill>`, reusing the same engine.

A portable, CTO-facing Claude skill that produces the **Technical Assessment**
(`TA-AAAA-NNN`) for a demand the PO escalated to the CTO — the CTO persona's
*technical-strategy* mandate, the **feasibility authority** and **terrain-setter**
(`teamwork-process/personas/03-cto.md`, `templates/03-technical-assessment.md`,
`personas/02-po.md` §2/§10, `interactions/05-po-to-cto.md`).

The TA is the **CTO's** artefact. It **responds** to the Readiness Package and is
authored **alone** — it **never edits the RP**. It may **veto** feasibility, in which
case the PO revises the RP scope and re-escalates. The TA contains: the feasibility
verdict (carrying the **terrain** it rests on), architectural impact, integrations
feasibility, NFR feasibility (mapped to RP §8), testability/observability, hard
constraints, technical risks, suggested ADRs (the CTO approves), and the firm
effort/cost.

> **Scope — the technical-strategy mandate.** The CTO persona has a **dual mandate**
> (`03-cto.md` §2): *technical strategy* (the TA — a per-demand artefact that **freezes**)
> and *people leadership* (capacity map, 90-day reviews, hiring signal — a living state
> that **never freezes**). This skill operationalizes the **technical-strategy** mandate:
> the Technical Assessment. The people-leadership cockpit is out of scope here.

> This README is the orientation. The authoritative spec lives in [`SKILL.md`](SKILL.md)
> (the orchestrator) and [`references/`](references/).

## The big idea

**Classify first, then draft-then-confirm — feasibility is the headline.** The CTO's
first-class model is *feasibility* (`personas/03-cto.md` §3), and *feasibility cannot be
assessed on unknown terrain* — so every verdict carries the **terrain** (the
`tech-landscape` KB) it rests on. The pipeline:

1. **Classification gate.** `hsb-tech-classifier` confirms the demand nature under the
   technical lens — **Greenfield** (the TA *defines* the foundation: stack, ADRs,
   structure) / **Brownfield** (the TA *discovers* the current system: patterns,
   integrations, debt) / **Híbrido** (both) — and resolves the Knowledge Base
   (`tech-landscape`). This **governs which path is in force**; the other path is an
   honest `N/A`.
2. **Draft-then-confirm.** `hsb-stage-inheritor` carries the RP/Intake material forward
   (NFRs → NFR feasibility, integrations, PO questions, demand nature);
   `hsb-section-drafter` drafts the in-force technical sections — **fanned out one per
   section in parallel**; `hsb-adr-proposer` arrives with suggested ADRs;
   `hsb-effort-estimator` proposes the firm cost; `hsb-feasibility-assessor` proposes
   the verdict. The CTO reviews, edits, approves, and **signs (or vetoes)**.
3. **One writer per file.** `technical-assessment.md` is written exclusively by
   `hsb-doc-updater`; `qa-log.md` by `hsb-ledger-writer`; the persistent
   `tech-landscape-<system>.md` by `hsb-landscape-keeper`. Every CTO proposer is
   read-only; the orchestrator routes proposals through the single writers, which makes
   the fan-out safe.

## How to invoke

```
/hsb-teamwork:tech-assessment
```

It resolves the **initiative** to run in, then reads the **works + definitions index**
(`initiative.json`) to discover the **Readiness Package** to respond to — the phase
whose `produces` is `readiness-package` — plus the **Intake Record** (for the demand
nature + KB) and the **`TechAssessmentRef` debt** the RP pushed into `owes`. The TA runs
as the `assessment/` **phase**, recording its outputs and **discharging the owed
Technical Assessment** back into the index on sign-off. Output language defaults to
pt-BR.

## Input

A **frozen, escalated Readiness Package** — produced by
`/hsb-teamwork:readiness-package`, with `tech-assessment-ref` = requested/deferred (an
architectural trigger was detected). If the RP froze with `Status: not_requested`,
there is **no TA** — the PRD forms from the RP alone
(`templates/03-technical-assessment.md` § "When there is NO TA").

The CTO provides:
- The initiative to run in (its `readiness/` phase is the RP; an external RP path may be
  given instead).
- Optionally: additional files to index (existing `tech-landscape`, prior ADRs, specs).
- Optionally: a custom TA template (if not using the default).

## Outputs

All artifacts land in the initiative's `assessment/` phase, plus the persistent
`tech-landscape` at the initiative root:

```
<INITIATIVE_DIR>/
├── tech-landscape-<system>.md      # persistent KB — seeded (greenfield) / updated (brownfield)
└── assessment/
    ├── contract.lock.md            # derived TA contract + template hash
    ├── sources-index.md            # index of ingested inputs (incl. the RP + intake-record)
    ├── sources/                    # normalized input files
    ├── qa-log.md                   # Q&A ledger
    ├── technical-assessment.md     # the TA being filled and signed
    ├── glossary.md                 # brokered read-only copy of the initiative glossary
    ├── assessment-report.md        # live gap map (optional)
    ├── output/
    │   ├── humanized.md            # canonical clean copy
    │   ├── translated.pt-BR.md     # translated variant (or the confirmed language)
    │   ├── enriched.md             # visually enriched (NFR table, integrations map, ADRs)
    │   └── manifest.md             # index of artifacts + verdict + sign-off status
    └── final/
        └── <project>-NNN.md        # externalized, scaffolding-stripped final
```

The shared `glossary.md`, `decisions.md`, the `tech-landscape`, and the
`initiative.json` index live at the **initiative root**, shared across every front.

## The feasibility verdict and the veto

- **`viável`** — buildable as specified → TA signs; PRD can merge RP + TA.
- **`viável-com-ressalvas`** — buildable **if** stated conditions hold → TA signs with
  the caveats recorded as hard constraints.
- **`inviável-como-escopado`** — the **veto**: the TA freezes as a signed veto and the
  orchestrator signals the PO to revise the RP scope and re-escalate. The CTO does not
  redefine the product. See [`references/feasibility.md`](references/feasibility.md).

## The RP↔TA migration

The readiness-package skill detects architectural escalation and (historically) froze
the RP **provisionally** with `tech-assessment-ref: deferred`, because the
tech-assessment skill did not yet exist
([readiness-package `references/escalation.md`](../readiness-package/references/escalation.md)).
**This skill is what that migration anticipated.** With the TA skill present, the RP's
freeze gate tightens to require a **signed** TA, and this skill **discharges** the RP's
`TechAssessmentRef` debt on sign-off (`status: signed` / `vetoed`, with the verdict and
link).

## Modes

- **Fresh** (default) — escalated RP exists, no assessment yet. Full journey.
- **Revisit** — re-run after a veto + revised RP (bump the TA version), or resume an
  unfrozen assessment (re-score, re-open only weak sections).
- **Batch / headless** — escalated RPs, no live CTO. Classify + draft + propose the
  verdict under honest dispositions; output is always "draft for CTO sign-off" (the
  verdict is the CTO's to commit).

## Using it elsewhere

In **this repo** it works once symlinked into `.claude/` from the plugin. To reuse it in
**other projects**, install it as a Claude Code plugin:

```
/plugin marketplace add hugo-hsbtech/teamwork-process-marketplace
/plugin install hsb-teamwork@hsb-tech
```

Then invoke it as `/hsb-teamwork:tech-assessment`.

## Layout (within the plugin)

```
plugins/hsb-teamwork/
├── skills/tech-assessment/
│   ├── SKILL.md                                       # orchestrator spec
│   ├── README.md                                      # this file
│   ├── references/
│   │   ├── orchestration.md                           # phases, roster, single-writer rule, layout
│   │   ├── classification.md                          # nature → path, honest-N/A, KB resolution
│   │   ├── feasibility.md                             # verdict, veto path, Discovery exit, signOffReady gate
│   │   ├── inheritance.md                             # RP/Intake → TA section mapping
│   │   └── landscape.md                               # seed/reference the persistent tech-landscape
│   └── assets/
│       ├── target-template.technical-assessment.md    # default TA template (annotated)
│       ├── target-template.technical-assessment.guide.md  # companion filling guide
│       └── golden-example.md                          # calibration exemplar
└── agents/hsb-*.md                                    # shared engine agents + the CTO roster
```

The CTO-specific agents this skill drives (`hsb-tech-classifier`,
`hsb-feasibility-assessor`, `hsb-adr-proposer`, `hsb-effort-estimator`,
`hsb-landscape-keeper`) live in `agents/hsb-*.md` alongside the rest of the shared
roster; it also reuses `hsb-stage-inheritor` and `hsb-section-drafter`.
