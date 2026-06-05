# Companion guide — PRD template

How each section is filled, by `id`. The PRD is **not a capture** — it is a **merge**.
Two frozen upstream artifacts already exist: the **Readiness Package** (product, authored
by the PO) and the **Technical Assessment** (technical, authored by the CTO). This skill
**stitches, reconciles, and exposes** them to the PM — it never re-authors either half.

The PRD is assembled **inherit-then-synthesize, then confirm** (see references/merge.md and
references/reconciliation.md): the `stage-inheritor` carries the RP forward into Part A and
the TA forward into Part B; the `synthesizer` composes the `derived` sections (executive
summary, consolidated risk, inherited readiness) and the `reconciler` produces the scope
reconciliation; then the **PO** confirms the product half and the **CTO** co-signs the
technical half. No section starts empty.

Origins: `inherited` (carried from the linked RP / TA — keep its source and confidence),
`synthesized` (composed by the engine from the inherited halves — partial confidence until
confirmed), `po_authored` (the PO confirmed a product-half entry — full confidence),
`cto_authored` (the CTO confirmed a technical-half entry — full confidence), `decided` (an
honest disposition, e.g. the whole of Part B when there was no escalation). The promotion
path is `inherited` / `synthesized` → **PO/CTO review** → `po_authored` / `cto_authored`.

> **The PRD invents no facts.** Every product fact traces to the RP; every technical fact
> traces to the TA. The only *new* writing is composition (the executive summary), merging
> (the consolidated risk view), and reconciliation (the scope table) — and even those only
> combine what the two frozen halves already established. If you find yourself adding a fact
> that is in neither source, that is a bug: it belongs upstream, not in the merge.

---

## The governing field — read this first

- **`meta` → Escalated?** governs Part B. Read the initiative's works index:
  - **Escalated (a signed TA exists)** → Part B is filled `Origin: inherited` from the TA;
    the feasibility verdict, nature/landscape, architectural impact, NFR feasibility,
    alternatives, hard constraints, and ADRs all carry forward.
  - **Not escalated (the RP froze with `tech-assessment-ref: not_requested`)** → every Part B
    section is `Disposition: decided` with content "N/A — no architectural escalation" (an
    honest disposition that clears the gate). The PRD is `RP alone`; the CTO sign-off row is
    an honest N/A.
  - **Vetoed TA (`Infeasible as scoped`)** → **there is no PRD.** The orchestrator stops
    before drafting and signals the PO to revise the RP scope and re-escalate. A veto is not
    a section to fill — it is a halt. See references/reconciliation.md § The veto halt.

---

## The gate — dual sign-off

- **`sign-off`** (blocks, min-conf 85) — the merge **only closes with dual sign-off**, the
  PRD's freeze gate (`handoffReady`). The **PO** signs the product half (the RP is frozen —
  `freezeReady`); the **CTO** signs the technical half (carrying the TA's feasibility
  verdict), or the CTO field is an **honest N/A** when there was no escalation. The
  feasibility verdict is **inherited from the TA, never re-decided here**. High threshold by
  design — this is the gate that opens the downstream.

---

## The synthesized opening

- **`exec-summary`** (blocks, min-conf 75; derived from `a-objectives`, `a-scope`,
  `b-feasibility`, `effort-cost`, `success-metrics`) — 2–4 paragraphs composed by
  `hsb-synthesizer`: the problem, what will be built, the technical feasibility, the expected
  business outcome. It is the one-page view for CEO/CFO/PM. It **adds no new facts** — it
  composes the inherited ones. Write it after Part A, Part B, and effort exist (so it
  summarizes settled content), and confirm it last.

---

## Part A — the product half (inherited from the RP, confirmed by the PO)

Every A-section is `Origin: inherited`, carried forward from the frozen RP by
`hsb-stage-inheritor` at its preserved confidence, then confirmed `po_authored`. **Summarize,
do not rewrite** — the full source is the linked RP; Part A is what the PM needs to plan.

- **`a-objectives`** (blocks, 75) — the measurable outcomes (outcomes, not outputs).
- **`a-scope`** (blocks, 80) — final included / excluded / deferred. If `scope-reconciliation`
  changed anything, A.2 reflects the **reconciled (final)** scope, not the pre-TA scope.
- **`a-personas`** (blocks, 70) — who is impacted and the job each hires the product to do.
- **`a-journey`** (blocks, 70) — the end-to-end happy path the User Stories derive from.
- **`a-business-rules`** (blocks, 70) — rules, validations, state transitions (summary or
  pointed RP reference) — enough to size the work without surprises.
- **`a-user-stories`** (blocks, 80) — stories with their primary Given/When/Then criteria
  (what QA/UAT validates — they must be testable). Full criteria stay in the RP.
- **`a-nfrs`** (blocks, 75) — the product NFRs (RP §8), each with verification. When escalated,
  each pairs 1:1 with a `b-nfr-feasibility` row — keep them consistent.
- **`a-edge-cases`** (blocks, 70) — edge cases and failure modes (RP §9) with expected behavior.

---

## Part B — the technical half (inherited from the TA, co-signed by the CTO)

Every B-section is `Origin: inherited` from the **signed TA**, then confirmed `cto_authored`.
**When there was no escalation, every B-section is `Disposition: decided` N/A** — an honest
disposition that clears the gate (the no-TA path; see references/reconciliation.md).

- **`b-feasibility`** (blocks, 80) — the verdict + caveats, **inherited from the TA, never
  re-decided**. `Infeasible as scoped` never reaches a PRD (a veto halts the merge). N/A when
  not escalated.
- **`b-nature-landscape`** (blocks, 70) — the terrain: brownfield current state (+ link to the
  `tech-landscape`) or greenfield foundation (stack + target architecture). N/A when not
  escalated.
- **`b-arch-impact`** (blocks, 75) — systems/areas touched + required integrations under the
  feasibility lens. N/A when not escalated.
- **`b-nfr-feasibility`** (blocks, 75) — one row per `a-nfrs` NFR: feasible? and how. Keeps the
  product↔technical loop closed. N/A when not escalated.
- **`b-alternatives`** (non-blocking, 0) — the discarded options + **why not**, so downstream
  does not re-litigate. "—" / `decided` if none or not escalated.
- **`b-hard-constraints`** (blocks, 75) — non-negotiable conditions + their effect on scope;
  these feed `scope-reconciliation`. "None" / `decided` if none; N/A when not escalated.
- **`b-adrs`** (blocks, 70) — the CTO-signed architectural decisions. Fine-grained /
  implementation ADRs belong to the Tech Lead's Tech Backlog. N/A when not escalated.

---

## The reconciliation work — the PRD's own intellectual content

- **`scope-reconciliation`** (blocks, 80; derived from `a-scope`, `b-feasibility`,
  `b-hard-constraints`) — produced by `hsb-reconciler`. Compare the RP scope against the TA's
  verdict, caveats, and hard constraints. If the CTO imposed something that changed the scope,
  record exactly **what changed and why** — and ensure `a-scope` reflects the reconciled
  result. If nothing changed (or no escalation): "RP scope maintained in full." This is where
  the two halves are made to agree; it is the reason the merge is more than a staple.

- **`consolidated-risk`** (blocks, 75; derived from `a-edge-cases`, `b-arch-impact`,
  `b-hard-constraints`) — `hsb-synthesizer` merges the RP's product/business risks (§12) with
  the TA's technical risks into one table, each row tagged origin (RP / TA) and type, with
  probability, impact, and mitigation, plus explicit external dependencies. No new risks are
  invented — only the two registers combined.

- **`inherited-readiness`** (blocks, 70; derived from `a-scope`, `b-feasibility`) — the
  assumptions still to validate, the Discovery unknowns (resolved/open), and the delegated
  answers (with owner) that survived from upstream. If an assumption proves false in
  execution, the demand is re-triaged (downstream re-triage trigger). Carried forward from the
  RP/TA dispositions.

---

## Carried-forward sections

- **`effort-cost`** (blocks, 70) — the **firm** estimate from the TA (it replaces the RP's
  preliminary number). When **not escalated**, carry the RP's preliminary estimate and label
  it preliminary (the Tech Lead firms it in breakdown). Internal use only.
- **`success-metrics`** (blocks, 75) — primary metrics + guardrails (a guardrail must not
  worsen), inherited from the RP, with target/window/confidence. The projected baseline
  `metrics.md` compares against post-rollout.

---

## The handoff

- **`handoff-gate`** (blocks, 80; derived from `sign-off`, `scope-reconciliation`,
  `consolidated-risk`, `inherited-readiness`) — the delivery checklist the PM accepts or
  rejects against. Every box must be checkable from the merged document. The PM may **reject**
  with **specific** gaps (not "needs more detail"); the rejection enters the Revision History
  and the PO (or CTO) addresses only the gaps and bumps the version (Revisit mode). Close with
  the priority and business context: why this demand, now.

---

## Meta sections

- **`meta`** (non-blocking) — stable IDs (PRD-YYYY-NNN, linked RP-YYYY-NNN vX, TA-YYYY-NNN vX
  or N/A, INT-YYYY-NNN), the escalation flag, the demand nature, the authors (PO + CTO when
  escalated), status (Draft / In PM Review / Accepted / Returned), output language, and the
  delivered-to-PM date. Filled by the engine from the works index; the PO confirms.
- **`revisions`** (non-blocking) — version, date, author, status, change summary per revision.
  Initialised v1 / Draft; a PM rejection adds a row and bumps the version.

---

## The bar

A good PRD reads like a single document a PM can plan against, in which **each half keeps its
author**: the product definition is the PO's RP, summarized faithfully; the technical
definition is the CTO's TA, summarized faithfully; the scope is reconciled so the two agree;
the risks of both halves sit in one table; the effort is firm; and the dual sign-off is
present (or the CTO half is honestly N/A). It **invents nothing** — every fact traces to a
frozen source. It opens the downstream because the PM can accept it without returning it.
