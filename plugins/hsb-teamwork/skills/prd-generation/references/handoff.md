# Handoff — the dual sign-off, the freeze gate, and the PM acceptance loop

The PRD is the artifact that **opens the downstream**. It closes only with **dual
sign-off**, freezes at `handoffReady`, and is then handed to the **PM** — who has
explicit authority to **reject** it. This file governs that gate and that loop.

## The dual sign-off — `sign-off`

The merge closes with two signatures, one per author, each on their own half:

| Role | Signs | Verdict in the row |
|---|---|---|
| **PO** (product) | the product half — the RP is frozen (`freezeReady`) | "RP Frozen (`freezeReady`)" |
| **CTO** (technical) | the technical half — the TA is signed | the TA's verdict: `Feasible` / `Feasible with caveats` — **carried, not re-decided** |

On the **no-escalation path**, the CTO row is an **honest N/A**: "N/A — no architectural
escalation; technical premises validated as reasonable; the Tech Lead confirms in
breakdown." Only the PO signs. This is not a missing signature — it is the recorded
absence of an escalation (see [`reconciliation.md`](reconciliation.md)).

> The feasibility verdict in `sign-off` and `b-feasibility` is **inherited from the TA**.
> The PRD never re-decides feasibility — and an `Infeasible as scoped` verdict never
> reaches this section, because a veto halts the merge upstream (the veto halt). If you are
> about to type a verdict the TA did not give, that is the bug.

## The freeze gate — `handoffReady`

`handoffReady = true` when **all** of:

1. **`sign-off` is committed** — PO: RP frozen; CTO: signed verdict **or** honest N/A. The
   `sign-off` section is at its threshold (min-conf 85).
2. **Every other `blocksFreeze` section is resolved or honestly disposed** — each is
   `po_authored` / `cto_authored` / confirmed-`inherited` at its threshold, **or** carries
   an honest disposition (`decided` N/A for the Part B no-escalation path; an inherited
   `assumption` / `discovery` that surfaces in `inherited-readiness`).
3. **Scope is reconciled** — `scope-reconciliation` is recorded and `a-scope` reflects the
   reconciled (final) scope (the `A.2 ↔ scope-reconciliation` invariant).
4. **The consistency invariants hold** — every `a-nfrs` NFR has a `b-nfr-feasibility`
   answer (or Part B is the N/A path); no Auditor-flagged contradiction between the halves
   is open.
5. **The handoff checklist is fully checkable** — every box in `handoff-gate` can be ticked
   from the merged document (not aspirationally).

The Confidence Auditor returns the gate verdict; the orchestrator does not freeze on a
narrated checklist — a box is checkable only if the corresponding section actually
resolves it.

## The handoff checklist — `handoff-gate`

The delivery checklist the PM accepts against. Each box maps to a section that must
already resolve it:

| Checklist box | Resolved by |
|---|---|
| RP frozen (`freezeReady`) and referenced | `meta` (Linked RP) + `sign-off` (PO row) |
| Technical Assessment signed off (or N/A justified) | `sign-off` (CTO row) + `b-feasibility` |
| Scope reconciliation recorded | `scope-reconciliation` |
| Risks and dependencies consolidated | `consolidated-risk` |
| External dependencies explicit | `consolidated-risk` (external dependencies line) |
| Open dispositions visible | `inherited-readiness` |

The section closes with the **priority and business context** — why this demand, now —
so the PM plans against the right urgency (it is the scope-cutting constraint when there
is a deadline, not a deferral one).

## The PM acceptance loop (Revisit mode)

The PM receives the frozen PRD and does one of two things:

- **Accepts** — `meta → Status: Accepted`; the PRD opens the downstream (PM execution
  planning). The orchestrator records `delivered-to-pm` / `downstream-ready` in the
  initiative index.
- **Rejects** — the PM returns the PRD with **specific** gaps (not a generic "needs more
  detail"): e.g. "ST-004 has no acceptance criterion," "the consolidated risk view omits
  the third-party SLA dependency," "effort is preliminary but the demand is escalated —
  needs the firm TA number." This is **Revisit mode**:
  1. the rejection + reason is recorded in `revisions` (a new row) and the version bumps;
  2. the orchestrator re-spawns the Auditor on the named sections only;
  3. the **PO** addresses product gaps; the **CTO** addresses technical gaps (re-open only
     the affected half — the rest stays frozen);
  4. the corrected PRD is re-frozen and re-delivered.

> The PM does not redefine scope or re-author either half — they **gate** the merge's
> completeness. A rejection names what is missing or contradictory **for planning**; the
> fix addresses only those gaps. The PO's "PM first-version acceptance" metric
> (`personas/02-po.md` §9) is the mirror on how well the merge was assembled — a high
> rejection rate means the PRD is leaving gaps the PM has to bounce.

## What the gate is not

- It is **not** a place to keep capturing — both halves are frozen; if the gate cannot
  clear because a source section is genuinely missing, the fix is upstream (re-open the
  RP/TA), not a guess in the PRD.
- It is **not** a re-judgment of feasibility — the CTO's verdict is carried as-is.
- A **vetoed** TA never reaches this gate — the merge halts before drafting (the veto
  halt).
