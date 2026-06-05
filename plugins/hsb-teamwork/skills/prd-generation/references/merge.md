# Merge — how two frozen halves become one PRD

This is the governing method of the skill. The PRD is **not authored** — it is
**merged**. Two upstream artifacts already exist and are **frozen**:

- the **Readiness Package (RP)** — the product half, authored **alone** by the PO;
- the **Technical Assessment (TA)** — the technical half, authored **alone** by the CTO
  (present only when the demand was escalated).

`PRD = RP (PO) + Technical Assessment (CTO)`. The PRD **stitches, reconciles, and
exposes** these to the PM — and it is the PRD, not the RP, that opens the downstream
(`personas/02-po.md` §2/§10/§11, `templates/04-prd.md`).

## The one rule: preserve authorship, invent nothing

The structural correction this whole chain rests on (`personas/02-po.md` §2): the RP and
the TA are **separate artifacts with different authors** that **merge into the PRD**.
Mixing product authorship and technical authorship in one document is what produces "the
PO as meeting note-taker" and "the CTO who rewrites the product." The PRD keeps them
separate **even inside the merged document**:

- **Part A** is the PO's product definition, carried forward from the RP.
- **Part B** is the CTO's technical definition, carried forward from the TA.
- The PO confirms Part A (`po_authored`); the CTO co-signs Part B (`cto_authored`).
  Neither rewrites the other's half.

> **The PRD invents no facts.** Every product fact traces to the RP; every technical fact
> traces to the TA. If you are about to write a fact that is in neither frozen source,
> stop — it belongs upstream (re-open the RP or the TA), not in the merge. The merge's
> only *new* writing is **composition** (the executive summary), **combination** (the
> consolidated risk view), and **reconciliation** (the scope table) — and each of those
> only recombines what the two halves already established.

## Inherit-then-synthesize, then confirm

Three kinds of section, three engine roles:

| Kind | Sections | Engine role | Origin |
|---|---|---|---|
| **Inherited** (carried forward, summarized) | all of Part A; all of Part B; `effort-cost`; `success-metrics` | `hsb-stage-inheritor` (`PART: A` from the RP, `PART: B` from the TA) | `inherited` |
| **Derived** (composed from the inherited halves) | `exec-summary`, `consolidated-risk`, `inherited-readiness` | `hsb-synthesizer` (one per `SECTION`) | `synthesized` |
| **Reconciled / drafted** | `scope-reconciliation` (Reconciler), `handoff-gate` (Section Drafter) | `hsb-reconciler` / `hsb-section-drafter` | `synthesized` |

Then the humans confirm: the **PO** promotes the product half to `po_authored`; the
**CTO** co-signs the technical half to `cto_authored`. The `meta` / `revisions` /
`sign-off` rows are filled from the works index and the confirmations.

### Why "summaries, not copies"

Part A and Part B are **what the PM needs to plan**, not a re-paste of the full upstream
documents. The Inheritor summarizes each source section to the PRD's altitude and **links
back** to the full RP/TA for the complete detail (full acceptance criteria, the service
blueprint, the full risk register, the ADR bodies). A PRD that copy-pastes the entire RP
and TA is a merge failure in the other direction: it buries the PM instead of equipping
them.

## Who the orchestrator talks to

The **PO owns the PRD** and drives the merge — they confirm the product half and the
synthesized/reconciled sections. The **CTO co-signs the technical half**: the merge only
closes with **dual sign-off** (`sign-off`), and the feasibility verdict in that row is
**carried from the TA, never re-decided**. On the **no-escalation path** there is no CTO
in the loop — the CTO sign-off field is an honest N/A and the whole conversation is with
the PO.

> In **headless / batch** mode there is no live PO or CTO: the inherited and synthesized
> entries clear the gate by their honest dispositions, but the **sign-off is never
> auto-committed** — the output is always "draft PRD for PO+CTO sign-off," never an
> accepted PRD.

## The two paths

The `meta → Escalated?` field (resolved in Phase 0 from the works index) governs Part B:

- **Escalated** — a **signed** TA exists. Part B is inherited from it; the feasibility
  verdict, nature/landscape, architectural impact, NFR feasibility, alternatives, hard
  constraints, and ADRs all carry forward. `effort-cost` is the TA's **firm** number.
- **Not escalated** — the RP froze with `tech-assessment-ref: not_requested`. Part B is
  the honest-N/A path (every B-section `Disposition: decided`, "N/A — no architectural
  escalation"); `effort-cost` carries the RP's **preliminary** number (the Tech Lead
  firms it in breakdown). See [`reconciliation.md`](reconciliation.md).
- **Vetoed** — the TA returned `Infeasible as scoped`. **There is no PRD.** The
  orchestrator halts in Phase 0 and signals the PO to revise the RP scope and
  re-escalate. See [`reconciliation.md`](reconciliation.md) § The veto halt.

## Keeping the halves consistent

The merge's value is that the two halves are made to **agree**. Two consistency
invariants the Confidence Auditor enforces:

1. **A.7 ↔ B.4 — every product NFR has a feasibility answer.** Each NFR the RP declared
   (A.7) must have a matching row in B.4 (or the whole of Part B is the N/A path). A
   declared NFR with no feasibility answer is a gap, not a detail.
2. **A.2 ↔ scope-reconciliation — the scope is the reconciled scope.** If the TA's
   constraints or caveats changed what the RP scoped, `scope-reconciliation` records it
   **and** `a-scope` reflects the final, reconciled boundaries — not the pre-TA scope.

A flagged inconsistency routes to the Reconciler, never silently to a guess.

## The boundary — what the PRD is and is not

The PRD **is** the merge: stitched halves, reconciled scope, consolidated risks, firm
effort, dual sign-off, and a checkable handoff gate. The PRD **is not** a place to
redefine the product (that is the RP) or to re-judge feasibility (that is the TA). It does
not start downstream technical breakdown (that is the Tech Lead's job, after the PM
plans). It is the single document the PM accepts — and the only artifact that opens the
downstream.
