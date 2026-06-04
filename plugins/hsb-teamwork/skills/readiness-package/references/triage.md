# Triage — Act 1 of the PO journey (routing gate before rationalization)

The PO journey is **two acts** (`teamwork-process/personas/02-po.md` §3, §6.1):

| Act | Nature | The question | Output |
|---|---|---|---|
| **1 · Triage** | fast · disposable | "Does this demand merit our effort — and by which path?" | one of 4 routing decisions + justification (the **Intake Record**, `INT-AAAA-NNN`) |
| **2 · Rationalization** | deep · accumulative | "Given it advances, what is the product form of this pain?" | the frozen **Readiness Package** (`RP-AAAA-NNN`) |

The line that separates the two acts is the state **`Product Ready`**. Only it
opens Act 2; the other three decisions close the PO's engagement *here* by a
lateral door. This skill runs **both acts as one journey** but keeps them as
**distinct artefacts and phases** — the Intake Record (`intake/` phase) and the
Readiness Package (`readiness/` phase) — so the separation the documentation
mandates is preserved without a second skill hop.

The historical failure this fixes: the skill used to assume the input was already
`Product Ready` and dove straight into drafting the RP, **pre-interpreting as
product** things that should have been triaged first. Triage is now an explicit,
cheap, gated first phase.

## What triage reuses (no new engine)

Triage runs on the **same engine** as rationalization — the same setup agents,
the same single-writer rule, the same confidence-driven question loop, just
pointed at a different template:

- `hsb-template-validator` / `hsb-source-indexer` / `hsb-template-analyst` —
  validate the intake template, index the origination-record, derive
  `intake/contract.lock.md`.
- `hsb-doc-updater` — sole writer of `intake/intake-record.md` (DOC parametrized).
- `hsb-ledger-writer` — sole writer of `intake/qa-log.md`.
- `hsb-glossary-keeper` — records the routing decision in the initiative's
  shared `decisions.md` (cross-phase fact).
- **`hsb-triage-assessor`** (new) — read-only proposer that scores the criteria,
  proposes the routing decision, and classifies the **demand nature**
  (greenfield / brownfield / hybrid) + Knowledge Base existence.

## The demand nature is born here

Triage also classifies the **demand nature** — Greenfield (new software) /
Brownfield (changes existing software) / Híbrido — and whether a Knowledge Base
(`tech-landscape-[system].md`) exists. The assessor seeds it from the
origination-record's nature-signal ("Touches: new capability / existing software /
not sure") and the PO firms it. This is a **blocking** `demand-nature` section in the
intake contract, not an afterthought: greenfield routes the downstream Technical
Assessment to *define* the foundation (stack, ADRs, structure), brownfield routes it
to *discover* the existing state (patterns, integrations, debt). When the nature is
brownfield/hybrid and no Knowledge Base exists, the first technical task is to create
it — routed as a documentation Discovery. The classification (and KB reference)
travels forward into the RP metadata.

## The six criteria and the routing decision

The assessor scores **five evaluated criteria** (each with the full decision
model below) and proposes **one routing decision** (the sixth element):

| # | Criterion | Verdict scale |
|---|---|---|
| 1 | A real problem (not an isolated symptom)? | Yes / No |
| 2 | Recurring / has volume? | Yes / No |
| 3 | Fits the product vision? | Yes / No |
| 4 | Technical & business impact? | High / Med / Low |
| 5 | Do urgency & impact justify acting *now*? | Yes / No |
| 6 | **Routing decision** | `Product Ready` / `Discovery` / `Backlog` / `Reject` |

## The decision model (first-class, not annotation)

Every triage criterion and the routing decision carry the PO's defensibility
layer (`personas/02-po.md` §4-5) — these are **structured fields**, recorded in
`intake/qa-log.md` and the Intake Record, never optional prose:

| Field | Meaning |
|---|---|
| `verdict` | the choice itself (e.g. `Product Ready`, or "Yes" on criterion 1) |
| `rationale` | **why** — the text that makes the decision defensible; never optional |
| `basis` | the evidence it rests on (origination-record entry, Submitter disposition, portfolio data) |
| `source` | trace-to-source for the evidence (inherited from the Submitter honesty layer) |
| `reversible` | does the decision close a door (`Reject`) or open a recoverable route (`Discovery`/`Backlog`)? |

## Questioning model — triage questions FIRST

Triage is where the structured questioning happens *before* anything is
rationalized as product. The confidence-driven rule from the engine applies:

1. The `hsb-triage-assessor` scores each criterion from the origination-record.
   Where it can answer confidently (≥ the criterion's `min-confidence`), it
   proposes the verdict with `basis`/`source`.
2. The orchestrator asks the PO **only the criteria the assessor could not settle
   confidently** — the triage-priority questions — using the engine's
   `open`/`choice` protocol (`questioning-method.md`). The final routing decision
   is always the PO's.
3. The `hsb-doc-updater` writes the confirmed verdicts into the Intake Record.

This is the inversion of the old behaviour: the PO defines what proceeds as
product **at the gate**, not by reviewing an already-drafted RP.

## The triage gate

```
triageScore = % of the five criteria evaluated (verdict + rationale present)
triageReady = (triageScore == 100)          # all criteria informed
```

`triageReady` does **not** force a particular decision — it forces the decision
to be *informed*. Once `triageReady`, the PO commits one routing decision:

| Decision | reversible | Effect |
|---|---|---|
| `Product Ready` | — | **opens Act 2** → proceed to rationalization (the RP) in the same run |
| `Discovery` | yes | open the Discovery brief, time-box it; **stop** here, re-triage when it closes |
| `Backlog` | yes | good demand, not now; **stop** here, recorded for later |
| `Reject` | no | out of strategy / low value; **stop** here, closed with rationale |

## Short-circuit — the efficiency win

Only `Product Ready` continues into the expensive rationalization pipeline
(inheritance + section drafting + confirm loop). `Discovery` / `Backlog` /
`Reject`:

1. finalize the Intake Record (status `Triado`, decision recorded with the full
   decision model);
2. record the decision in the initiative's `decisions.md` (cross-phase fact);
3. set the `intake` phase to `frozen` in `initiative.json`
   (`produces: intake-record`); do **not** create a `readiness/` phase;
4. report the decision and rationale to the PO and stop.

Because ~3 of 4 outcomes stop here, most demands never pay the cost of the full
RP pipeline — this is the primary lever against the ~40-minute runs.

## Handoff into Act 2

When the decision is `Product Ready`, the `readiness/` phase consumes **both**
the origination-record **and** the intake-record:

- `initiative.json`: `readiness.consumes = ["origination-record", "intake-record"]`.
- The readiness `hsb-source-indexer` indexes the intake-record alongside the
  origination-record, so the Stage Inheritor and Section Drafter see the triage
  decision, the validated assumptions, the recognized constraints, and the
  **demand nature + Knowledge Base** classification — and the RP's "Prontidão
  herdada" section and metadata reflect them.
- A CTO escalation flagged during triage (the intake template's "Escalada
  arquitetural" field) is carried forward as a hint to `hsb-escalation-flagger`,
  which still owns the authoritative `tech-assessment-ref` disposition in Act 2.
