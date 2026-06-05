# Reconciliation — scope, risk, the no-escalation path, and the veto halt

The merge is more than a staple: the PRD makes the two frozen halves **agree** and
exposes a single planning view to the PM. This file governs the reconciliation work and
the two non-standard paths (no escalation, veto).

## Scope reconciliation — `scope-reconciliation` (Reconciler)

The RP froze a scope. The TA may have imposed **hard constraints** or attached **caveats**
to its `Feasible with caveats` verdict that change what is actually buildable. Scope
reconciliation is where the PRD records that delta and makes Part A's scope the **final,
reconciled** one.

`hsb-reconciler` compares three inputs:

- `a-scope` — the scope inherited from the RP;
- `b-feasibility` — the verdict + caveats inherited from the TA;
- `b-hard-constraints` — the non-negotiable conditions inherited from the TA.

and produces the reconciliation table. Each row is one of:

| Outcome | When | Effect on `a-scope` |
|---|---|---|
| **Unchanged** | the TA imposed nothing that touches this item | item stays as the RP scoped it |
| **Re-scoped** | a caveat narrowed how the item can be built | item updated to the reconciled form; the reason cites the caveat/constraint |
| **Removed** | a hard constraint makes the item infeasible **as scoped** (but the demand overall is feasible) | item moves to Excluded/Deferred; the reason cites the constraint |
| **Added** | the TA surfaced a required item the RP did not scope (e.g. a migration step a constraint forces) | item added to Included; the reason cites the constraint |

The Reconciler **proposes the reconciled `a-scope`** alongside the table, so the orchestrator
routes both to `hsb-doc-updater` and Part A ends up reflecting the final scope (the
`A.2 ↔ scope-reconciliation` invariant in [`merge.md`](merge.md)).

> **The PO and CTO already agreed.** Reconciliation does **not** re-open a negotiation: the
> RP is frozen and the TA is signed; the caveats and constraints are the CTO's, the scope
> is the PO's, and the agreement between them happened when the TA was signed. The PRD
> **records** that agreement; it does not relitigate it. If reconciliation surfaces a
> genuine new conflict the two frozen documents cannot settle, that is the rare case where
> the confirm loop fires a question (fallback) — or, if the conflict is material, a signal
> to re-open the RP/TA upstream, not to invent a resolution in the PRD.

If nothing changed (or there was no escalation): a single row, "RP scope maintained in
full," `Disposition: decided`.

## Consolidated risk — `consolidated-risk` (Synthesizer)

The PM plans against **one** risk view, not two registers. `hsb-synthesizer` merges:

- the RP's **product / business risks** (RP §12) — tagged `Origin: RP`;
- the TA's **technical risks** — tagged `Origin: TA` (absent on the no-escalation path);

into a single table, each row carrying type (Product / Business / Technical / External /
Compliance), probability, impact, and mitigation. It also lists the **known external
dependencies** explicitly (client action, procurement, third-party integration) so the PM
sees what is outside the team's control. **No new risks are invented** — only the two
registers combined and de-duplicated (a risk both halves named appears once, tagged
`RP/TA`).

## The no-escalation path (PRD from the RP alone)

When the RP froze with `tech-assessment-ref: not_requested`, there was no architectural
impact and **no TA was written**. The PRD is `RP alone`:

- `meta → Escalated?` = **No**; `Linked Technical Assessment` = "N/A — no escalation".
- **Every Part B section** (`b-feasibility`, `b-nature-landscape`, `b-arch-impact`,
  `b-nfr-feasibility`, `b-alternatives`, `b-hard-constraints`, `b-adrs`) is
  `Disposition: decided` with content **"N/A — no architectural escalation"**. This is an
  **honest disposition that clears the freeze gate** — it is not a gap (the same mechanism
  the TA uses for its non-applicable greenfield/brownfield path).
- `sign-off` → the **CTO row is an honest N/A** ("N/A — no architectural escalation;
  technical premises validated as reasonable; Tech Lead confirms in breakdown"); only the
  PO signs.
- `effort-cost` carries the RP's **preliminary** estimate, labeled preliminary (the Tech
  Lead firms it in breakdown).
- `scope-reconciliation` = "RP scope maintained in full" (no TA → nothing to reconcile).
- `consolidated-risk` carries the RP risks; technical premises the PO assessed are noted
  as "to confirm with Tech Lead," and a false premise triggers a downstream re-triage.

The PRD still freezes and opens the downstream — the absence of a TA is **recorded
honestly**, not treated as missing.

## The veto halt (no PRD on an infeasible TA)

If the TA was discharged **`vetoed`** (`Infeasible as scoped`), **there is no PRD to
assemble.** A veto means the CTO judged the scope infeasible as written; the resolution
is upstream, not in the merge:

1. The orchestrator detects the veto in **Phase 0** (the `assessment/` phase's debt
   discharged `vetoed`) and **stops before drafting** — it does not create a `prd/` phase
   with an infeasible verdict.
2. It **signals the PO** to revise the RP scope and **re-escalate** to the CTO (the
   tech-assessment skill re-runs against the revised RP and bumps the TA version).
3. Only once a **non-veto** TA (`Feasible` / `Feasible with caveats`) is signed does the
   PRD become assemblable. Re-running this skill then picks up the revised RP + the new TA.

A veto is a **halt, not a section** — the PRD never carries an `Infeasible as scoped`
verdict, because such a verdict has no downstream to open. See
[`merge.md`](merge.md) § The two paths and the tech-assessment skill's
`references/feasibility.md` § The veto path.

## What reconciliation does not do

- It does **not** rewrite the RP or the TA — those are frozen; reconciliation records the
  delta between them, it does not edit either source.
- It does **not** re-decide feasibility — the verdict is the CTO's, carried as-is.
- It does **not** invent risks, scope, or mitigations absent from both halves — a fact
  that belongs to neither source belongs upstream.
- It does **not** reconcile the **demand nature**: when the CTO overrode the triage
  nature, the TA's `tech-classification` is authoritative and `b-nature-landscape`
  inherits it — the PRD shows the corrected nature, never the superseded RP-metadata
  value (the correction was already recorded to `initiative.json` at TA wrap; see the
  tech-assessment skill's `references/classification.md` § On an override).
