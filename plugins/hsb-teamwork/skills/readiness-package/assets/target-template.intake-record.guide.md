# Companion guide — Intake Record template (Act 1 · triage)

How each section is filled, by `id`. The Intake Record is the **triage artefact**:
the engine pre-scores the criteria from the origination-record at partial
confidence, the PO confirms the verdicts and commits **one** routing decision.
See [`references/triage.md`](../references/triage.md).

Decision model on triage entries (`personas/02-po.md` §4-5): every criterion and
the routing decision carry **verdict · rationale · basis · source · reversible** —
these are required fields, never optional prose.

---

- **`demand-summary`** (blocks, min-conf 70) — one-screen consolidation of the
  origination-record, validated by the PO (not re-typed). Problem = the pain, not
  the solution. Inherit each dimension's confidence from the capture; never inflate.

- **`triage-criteria`** (blocks, min-conf 70) — the five evaluated criteria. The
  `hsb-triage-assessor` proposes a `verdict` + `rationale` + `basis/source` for
  each from the origination-record. `triageReady` requires all five evaluated
  (verdict + rationale present). Criteria the assessor cannot settle confidently
  become triage-priority questions to the PO — asked **first**, before any product
  rationalization.

- **`triage-decision`** (blocks, min-conf 80) — the single routing decision, always
  `po_authored`. Allowed verdicts: `Product Ready` / `Discovery` / `Backlog` /
  `Reject`. Record `rationale`, `basis/source`, and `reversible` (Discovery/Backlog
  are reversible lateral doors; Reject closes). Only `Product Ready` opens Act 2;
  the other three short-circuit (finalize, record in `decisions.md`, stop).

- **`cto-escalation`** (derived, non-blocking) — early flag of whether Act 2 will
  likely need a Technical Assessment. Authoritative `tech-assessment-ref` is decided
  in the RP by `hsb-escalation-flagger`; this is only a hint carried forward.

- **`validated-assumptions`** (non-blocking) — Submitter assumptions the PO reviewed
  (Accepted / Rejected / To validate). Survivors travel forward to the RP explicitly.

- **`constraints`** (non-blocking) — constraints the downstream must respect from day
  one (time / budget / legal / technical / scope / external), inherited and validated.

- **`discovery`** (derived, conditional) — fill **only** when the decision is
  `Discovery`: the unknowns, who answers them, the method, and the time-box. Re-triage
  when it closes. Remove the section for any other decision.

- **`handoff`** (derived) — routes by decision: `Product Ready` → start the RP;
  `Discovery` → open the brief, re-triage on close; `Backlog`/`Reject` → close the
  PO pass, notify the Submitter with the rationale.
