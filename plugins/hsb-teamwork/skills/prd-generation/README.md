# prd-generation

> **Part of the `hsb-teamwork` toolkit.** `prd-generation` is the fourth skill, invoked as
> `/hsb-teamwork:prd-generation`. It runs the **PRD merge** — assembling the **Product
> Requirements Document** from the frozen **Readiness Package** (product, PO) and the signed
> **Technical Assessment** (technical, CTO) into the single artifact that opens the downstream
> and is delivered to the **PM**. Sibling steps: `origination-brainstorm`, `readiness-package`,
> `tech-assessment` (upstream) — each a skill under `/hsb-teamwork:<skill>`, reusing the same
> engine.

A portable, PO-facing Claude skill that produces the **PRD** (`PRD-AAAA-NNN`) by **merging**
the two frozen upstream halves — the PO persona's *merge + handoff* mandate
(`teamwork-process/personas/02-po.md` §2/§10/§11, `templates/04-prd.md`).

The PRD is a **merge, not a capture**: both halves already exist and are frozen. The skill
**stitches, reconciles, and exposes** them to the PM — it **never re-authors either half** and
**invents no facts**. `PRD = RP (PO) + Technical Assessment (CTO)`.

> This README is the orientation. The authoritative spec lives in [`SKILL.md`](SKILL.md) (the
> orchestrator) and [`references/`](references/).

## The big idea

**Inherit both halves, synthesize the bridge, reconcile the scope — then dual sign-off.** The
PRD's value is not new content; it is a *single, coherent, reconciled* planning view in which
each half keeps its author. The pipeline:

1. **Resolve the path.** Phase 0 reads the works index to learn whether the demand was
   **escalated** (a signed TA → merge both halves), **not escalated** (RP alone → Part B is an
   honest N/A), the TA is **owed but unwritten** (stop — run `tech-assessment` first), or
   **vetoed** (`Infeasible as scoped` → **halt**: no PRD until the PO re-scopes and
   re-escalates).
2. **Inherit.** `hsb-stage-inheritor` carries the RP forward into **Part A** and the TA into
   **Part B** — **fanned out one per part in parallel** — summarized to the PM's altitude,
   linking back to the full sources, tagged `Origin: inherited` at preserved confidence.
3. **Synthesize & reconcile.** `hsb-synthesizer` composes the `derived` sections (the combined
   executive summary, the consolidated risk view, the inherited-readiness view);
   `hsb-reconciler` produces the scope reconciliation and the reconciled final scope — all
   **fanned out in parallel**, tagged `Origin: synthesized`.
4. **Confirm — dual sign-off.** The **PO** confirms the product half; the **CTO** co-signs the
   technical half and the feasibility verdict carried from the TA. The merge freezes at
   `handoffReady` and is delivered to the **PM**, who may accept or reject with specific gaps.
5. **One writer per file.** `prd.md` is written exclusively by `hsb-doc-updater`; `qa-log.md`
   by `hsb-ledger-writer`. Every merge proposer (Inheritor, Synthesizer, Reconciler, Section
   Drafter, Auditor) is read-only; the orchestrator routes proposals through the single
   writers, which makes the fan-out safe.

**No new agents.** The roster is phase-agnostic: the merge maps onto engine specialists that
already exist — the **Inheritor** (carries each half), the **Synthesizer** (composes the
`derived` sections), and the **Reconciler** (resolves the scope).

## How to invoke

```
/hsb-teamwork:prd-generation
```

It resolves the **initiative** to run in, then reads the **works + definitions index**
(`initiative.json`) to discover the **Readiness Package** (the phase whose `produces` is
`readiness-package`) and, when escalated, the **Technical Assessment** (the phase whose
`produces` is `technical-assessment`). The PRD runs as the `prd/` **phase**, recording the
`prd` it produces and a `delivered-to-pm` signal on freeze. Output language defaults to
**en-US** (mirroring the PO's opening statement when another language is detected).

## Input

A **frozen Readiness Package** — produced by `/hsb-teamwork:readiness-package`. When the RP
escalated (`tech-assessment-ref` = requested/deferred), a **signed Technical Assessment** —
produced by `/hsb-teamwork:tech-assessment` — must also exist; the PRD merges both. When the
RP froze with `tech-assessment-ref: not_requested`, the PRD forms from the **RP alone** and
Part B is an honest N/A.

The PO provides:
- The initiative to run in (its `readiness/` and, when escalated, `assessment/` phases are the
  sources; external RP/TA paths may be given instead).
- Optionally: a custom PRD template (if not using the default).

## Outputs

All artifacts land in the initiative's `prd/` phase:

```
<INITIATIVE_DIR>/
└── prd/
    ├── contract.lock.md            # derived PRD contract + template hash
    ├── sources-index.md            # index of ingested inputs (RP + TA + intake-record)
    ├── sources/                    # normalized input files
    ├── qa-log.md                   # Q&A ledger (sparse — the PRD rarely asks)
    ├── prd.md                      # the PRD being merged and signed
    ├── glossary.md                 # brokered read-only copy of the initiative glossary
    ├── prd-report.md               # live gap map (optional)
    ├── output/
    │   ├── humanized.md            # canonical clean copy
    │   ├── translated.<lang>.md     # translated variant (or the confirmed language)
    │   ├── enriched.md             # visually enriched (risk table, scope-reconciliation diff, effort)
    │   └── manifest.md             # index of artifacts + sign-off status + handoff note
    └── final/
        └── <project>-NNN.md        # externalized, scaffolding-stripped final — what the PM receives
```

The shared `glossary.md`, `decisions.md`, and the `initiative.json` index live at the
**initiative root**, shared across every front.

## The two paths and the veto halt

- **Escalated** — a signed TA exists. Part B is inherited from it; `effort-cost` is the TA's
  firm number; the dual sign-off carries the CTO's verdict. *(This is the golden-example case —
  a `Feasible with caveats` merge.)*
- **Not escalated** — the RP froze `not_requested`. Part B is the honest-N/A path; only the PO
  signs; `effort-cost` carries the RP's preliminary number.
- **Vetoed** — the TA returned `Infeasible as scoped`. **There is no PRD.** The skill halts in
  Phase 0 and signals the PO to revise the RP scope and re-escalate. See
  [`references/reconciliation.md`](references/reconciliation.md) § The veto halt.

## The handoff to the PM

The merge closes with **dual sign-off** and freezes at `handoffReady`. The PM has explicit
authority to **reject** the PRD and return it with **specific** gaps (not "needs more detail");
the rejection enters the Revision History and the PO (or CTO) addresses only the gaps and bumps
the version (Revisit mode). The PO's "PM first-version acceptance" metric
(`personas/02-po.md` §9) is the mirror on how well the merge was assembled. See
[`references/handoff.md`](references/handoff.md).

## Modes

- **Fresh** (default) — frozen RP (+ signed TA when escalated), no PRD yet. Full merge.
- **Revisit** — re-run after a PM rejection (address named gaps, bump the version), or after an
  upstream half changed (re-frozen RP / re-signed TA), or resume an unfrozen PRD.
- **Batch / headless** — frozen RPs (+ TAs), no live PO/CTO. Inherit + synthesize + reconcile
  under honest dispositions; output is always "draft PRD for PO+CTO sign-off."

## Using it elsewhere

In **this repo** it works once symlinked into `.claude/` from the plugin. To reuse it in
**other projects**, install it as a Claude Code plugin:

```
/plugin marketplace add hugo-hsbtech/teamwork-process-marketplace
/plugin install hsb-teamwork@hsb-tech
```

Then invoke it as `/hsb-teamwork:prd-generation`.

## Layout (within the plugin)

```
plugins/hsb-teamwork/
├── skills/prd-generation/
│   ├── SKILL.md                          # orchestrator spec
│   ├── README.md                         # this file
│   ├── references/
│   │   ├── orchestration.md              # phases, roster (all reused), single-writer rule, layout
│   │   ├── merge.md                      # the governing method — preserve authorship, invent nothing
│   │   ├── reconciliation.md             # scope reconciliation, consolidated risk, no-escalation path, veto halt
│   │   ├── inheritance.md                # RP/TA → PRD section mapping
│   │   └── handoff.md                    # dual sign-off, handoffReady gate, PM acceptance/rejection loop
│   └── assets/
│       ├── target-template.prd.md        # default PRD template (annotated)
│       ├── target-template.prd.guide.md  # companion filling guide
│       └── golden-example.md             # calibration exemplar (escalated merge, Feasible with caveats)
└── agents/hsb-*.md                       # shared engine agents — reused unchanged (no new agents)
```

The merge reuses the shared roster — chiefly `hsb-stage-inheritor` (carries each half),
`hsb-synthesizer` (composes the `derived` sections), and `hsb-reconciler` (resolves the scope)
— plus `hsb-section-drafter`, `hsb-confidence-auditor`, and the production agents. It adds **no
new agents**.
