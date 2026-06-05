# Feasibility — the CTO's first-class decision and the freeze gate

The CTO's first-class model is **feasibility** (`personas/02-po.md:363` — "confidence
for the Submitter, decision for the PO, **feasibility for the CTO**"). The
`feasibility-verdict` section is the headline of the TA: the defensible ruling on
whether the RP's scope can be built, and under what conditions.

`hsb-feasibility-assessor` is the **gate proposer** (analogous to the
`hsb-triage-assessor` for the PO's routing decision). It reads the drafted
architectural impact, NFR feasibility, integrations, risks, and hard constraints and
proposes one verdict — never a rubber stamp. The CTO commits the final verdict.

## The verdict scale

| Verdict | Meaning | Effect |
|---|---|---|
| `viável` | The scope is buildable as specified | TA proceeds to sign-off; PRD can merge RP + TA |
| `viável-com-ressalvas` | Buildable **if** stated conditions hold (e.g. a specific mechanism, a pre-condition, a hard constraint) | TA signs with the caveats recorded; the PO must honour the hard constraints in scope |
| `inviável-como-escopado` | Not buildable as scoped — the **veto** | TA freezes as a signed veto; the PO revises the RP scope and re-escalates |

## The decision model (first-class, not annotation)

The verdict carries the CTO's defensibility layer — structured, never optional prose:

| Field | Meaning |
|---|---|
| `verdict` | the ruling itself (`viável` / `viável-com-ressalvas` / `inviável-como-escopado`) |
| `rationale` | **why** — the defensible reasoning; never optional |
| `caveats` | for `viável-com-ressalvas`: exactly what must be true for the verdict to hold (each typically also a `hard-constraint`) |
| `basis` | the evidence it rests on (which NFR-feasibility row, architectural-impact area, risk) |
| `source` | trace-to-source for that evidence |

High threshold by design (`min-confidence 85`): this is the central CTO judgment, so
it resolves only at high confidence and is always `cto_authored` — the assessor
proposes; the **CTO commits**.

## The veto path (`inviável-como-escopado`)

The veto is a **first-class, valid outcome**, not a failure of the run
(`interactions/05-po-to-cto.md`, `interactions/06-cto-to-po.md`):

1. The verdict carries the veto + a defensible rationale (which constraint or NFR makes
   the scope unbuildable).
2. The TA **still freezes** — the CTO's decision is complete and signed (`Status: Vetado`).
3. The orchestrator pushes a **scope-revision signal** back to the `readiness/` phase
   (a note in `initiative.json` / `decisions.md`) so the PO revises the RP scope and
   **re-escalates**. The CTO **does not redefine the product** — they veto and state
   why; the PO owns the scope change.
4. On re-escalation, this skill runs again (Revisit mode) against the revised RP and
   bumps the TA version.

A veto is not a discovery gap — it is a signed conclusion. Do not park it as
`discovery`.

## The Discovery exit (a technical unknown blocks the assessment)

Distinct from the veto: if a technical unknown prevents the assessment from **closing
at all** (you cannot reach *any* defensible verdict yet), fill `discovery-path`:

- The CTO defines the **spike / investigation**; the PO determines the **time-box**.
- The demand returns to Discovery; the TA does not sign until the spike resolves.
- The KB-does-not-exist case (brownfield/hybrid, see [`classification.md`](classification.md))
  is the most common Discovery exit — documenting the current system is the spike.

The difference: **veto** = "I assessed it; it's infeasible as scoped." **Discovery** =
"I cannot assess it yet; here's what to investigate first."

## The freeze gate

`signReady = true` requires:

1. The `feasibility-verdict` is committed — `cto_authored` at its `min-confidence`
   (85). A verdict is mandatory; the TA never freezes without one.
2. Every other `blocksFreeze` section is either resolved (`cto_authored` /
   confirmed-`inherited`) **or** honestly disposed:
   - the non-applicable path → `Disposition: decided` ("N/A — <nature>");
   - "nenhuma" sections (integrations / hard-constraints / build-vs-buy when none
     apply) → `Disposition: decided`;
   - an unclosable unknown → `discovery` (owner + time-box).
3. **Verdict-conditioned closure:**
   - `viável` → all in-force technical sections resolved.
   - `viável-com-ressalvas` → the caveats are recorded as `hard-constraints`.
   - `inviável-como-escopado` → the veto rationale is recorded; downstream sections that
     depend on a buildable scope (e.g. `effort-cost`, `adrs`) may be `Disposition: decided`
     ("N/A — escopo vetado, ver Veredito") rather than fully drafted.

When `signReady`, the TA freezes (`Status: Assinado` or `Status: Vetado`) and the
orchestrator discharges the RP's `TechAssessmentRef` debt in the initiative index
(`status: signed` / `vetoed`, with the verdict and link). This is the migration the
readiness-package's `references/escalation.md` anticipated: with the tech-assessment
skill present, the RP's freeze gate tightens to require a **signed** TA instead of the
temporary `deferred` path.

## Headless / batch

No live CTO means **no questions** and **honest dispositions** — not skipping the
verdict. The `hsb-feasibility-assessor` proposes the verdict under honest dispositions;
any section it cannot draft to threshold is disposed `assumption` (owner: CTO, "to
confirm") or `discovery`. The output is always "draft for CTO sign-off," never a real
`signReady` on its own — a feasibility verdict is the CTO's to commit.
