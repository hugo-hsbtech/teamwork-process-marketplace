<!--
TARGET TEMPLATE · PRD — Product Requirements Document (default)
This file is the contract. Each fillable section carries an annotation:
  <!- - origination: id=SECTION-ID; blocks=BOOL; min-confidence=N; kind=TYPE - ->
and a self-sufficient rubric. The Template Analyst derives contract.lock.md from
these (the same engine as origination-brainstorm / readiness-package / tech-assessment —
the marker keyword stays `origination:`).
The confidence line adds an Origin field (inherited | synthesized | po_authored |
cto_authored | decided) per personas/02-po.md §2/§10/§11 and templates/04-prd.md.

THE PRD IS A MERGE, NOT A CAPTURE. It stitches two FROZEN upstream artifacts —
the Readiness Package (product, authored by the PO) and the Technical Assessment
(technical, authored by the CTO) — into one document delivered to the PM. Most
sections are `inherited` (carried forward, summarized, never rewritten) or `derived`
(synthesized/reconciled FROM the inherited material). Authorship is preserved: the
PO does not rewrite the technical half; the CTO does not rewrite the product half.
`PRD = RP (PO) + Technical Assessment (CTO)`. See references/merge.md.

TWO PATHS, ONE TEMPLATE. The `meta` escalation field governs Part B:
 - ESCALATED  → the TA was produced (signed); Part B is filled from it (Origin: inherited).
 - NOT ESCALATED → no architectural impact; every Part B section is dispositioned
   `Disposition: decided` with "N/A — no architectural escalation" (an honest
   disposition that clears the gate). See references/reconciliation.md.
A VETOED TA (Infeasible as scoped) is NOT mergeable: there is no PRD until the PO
revises the RP scope and re-escalates. The orchestrator stops before drafting.

To use a different document type, copy this file, re-annotate, and pass it as TEMPLATE.
See references/contract-and-template.md (in origination-brainstorm).
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.
-->

# PRD — [Demand name]
<!-- rev: 0 · updated: YYYY-MM-DD -->

> The PRD (Product Requirements Document) is the **merge** of the **Readiness Package**
> (product, authored by the PO) with the **Technical Assessment** (technical, authored by
> the CTO). It is the **only artifact that opens the downstream** — delivered to the **PM**.
> Each half keeps clear authorship: the PO does not write the technical part, the CTO does
> not rewrite the product. The PRD **stitches, reconciles, and exposes** to the PM what they
> need to plan — without rewriting either source. See `personas/02-po.md` §2/§10/§11 and
> `templates/04-prd.md`.
>
> **When there was no CTO escalation:** the PRD is formed from the RP alone; Part B is
> dispositioned "N/A — no architectural escalation".
>
> `PRD = RP (PO) + Technical Assessment (CTO)`

## Metadata
<!-- origination: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Field | Value |
|---|---|
| **PRD ID** | PRD-YYYY-NNN |
| **Version** | v1 |
| **Linked RP** | RP-YYYY-NNN vX |
| **Linked Technical Assessment** | TA-YYYY-NNN vX / N/A — no escalation |
| **Linked Intake** | INT-YYYY-NNN |
| **Escalated?** | Yes (TA merged) / No (RP alone) |
| **Demand nature** | Greenfield / Brownfield / Hybrid / N/A |
| **Authors** | [Name] (PO) + [Name] (CTO, when escalated) |
| **Status** | Draft / In PM Review / Accepted / Returned |
| **Output language** | [e.g. en-US] |
| **Delivered to PM on** | — |

## Revision History
<!-- origination: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Version | Date | Author | Status | Summary |
|---|---|---|---|---|
| v1 | YYYY-MM-DD | PO (+ CTO) | Draft | Initial RP + TA merge. |

---

## Sign-off
<!-- origination: id=sign-off; blocks=true; min-confidence=85; kind=capture -->
> Rubric: the merge **only closes with dual sign-off**. The PO signs the product half
> (the RP is frozen — `freezeReady`); the CTO signs the technical half (the TA is signed —
> the feasibility verdict carried from the TA), or the CTO field is an **honest N/A** when
> there was no escalation. The PRD cannot freeze (`handoffReady`) without this row resolved.
> The feasibility verdict is **inherited from the TA, never re-decided here**. A vetoed TA
> never reaches this section — there is no PRD on a veto. High threshold: this is the gate.

| Role | Name | Verdict | Date |
|---|---|---|---|
| **PO** (product) | [Name] | RP Frozen (`freezeReady`) | YYYY-MM-DD |
| **CTO** (technical) | [Name] / — | Feasible / Feasible with caveats / N/A — no escalation | YYYY-MM-DD |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Combined Executive Summary
<!-- origination: id=exec-summary; blocks=true; min-confidence=75; kind=derived; inputs=a-objectives,a-scope,b-feasibility,effort-cost,success-metrics -->
> Rubric: 2–4 paragraphs — the problem, what will be built, the technical feasibility, and
> the expected business outcome. The one-page view for CEO/CFO/PM. **Synthesized** from the
> inherited sections (it adds no new facts — it composes the ones already merged). A good
> summary lets a reader who reads nothing else still know why this demand, what it delivers,
> whether it is feasible, and the outcome it targets.

[Summary here]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Part A — Product Definition (from the Readiness Package · PO)

> Summary of the key RP sections — **inherited, never rewritten**. The complete source is the
> linked `RP-YYYY-NNN`; here is what the PM needs to plan. Every A-section is `Origin: inherited`
> (carried forward from the frozen RP at its preserved confidence) and confirmed by the PO.

### A.1 Objectives and Expected Outcome
<!-- origination: id=a-objectives; blocks=true; min-confidence=75; kind=capture -->
> Rubric: the measurable outcomes the demand targets, carried from the RP. Each objective is
> an outcome (what changes for the user/business), not an output (what is built).

1. [Objective 1]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### A.2 Scope (final)
<!-- origination: id=a-scope; blocks=true; min-confidence=80; kind=capture -->
> Rubric: the final included / excluded / deferred boundaries from the frozen RP. This is the
> scope the PM plans against — fixed at the PRD; downstream executes, it does not redefine.
> If `scope-reconciliation` changed anything, this reflects the reconciled (final) scope.

**Included:** [items]
**Excluded:** [items]
**Deferred:** [items]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### A.3 Personas / Jobs-to-be-done
<!-- origination: id=a-personas; blocks=true; min-confidence=70; kind=capture -->
> Rubric: who is impacted and the job each is hiring the product to do, inherited from the RP.

| Persona | Job | Impact |
|---|---|---|
| [Persona] | [Job] | [Impact] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### A.4 User Journey (end-to-end)
<!-- origination: id=a-journey; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the happy-path flow the user takes end to end, inherited from the RP — the flow the
> User Stories derive from. Alternative paths and the full service blueprint stay in the RP.

| # | User action | Expected outcome | Touchpoint |
|---|---|---|---|
| 1 | [Action] | [Outcome] | [Where] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### A.5 Business Rules and Flows
<!-- origination: id=a-business-rules; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the rules, validations, and state transitions the system must enforce — summary or
> pointed reference to the RP sections. Enough for the PM to size the work without surprises.

[Summary or reference to the RP sections]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### A.6 Epics + User Stories + Acceptance Criteria
<!-- origination: id=a-user-stories; blocks=true; min-confidence=80; kind=capture -->
> Rubric: the stories **grouped under their epics**, with their primary Given/When/Then
> acceptance criteria, inherited from the RP. Each epic (`EPIC-NNN` + objective/value) is a
> coherent **deliverable** — the unit the PM sequences and the stakeholder recognises; every
> story belongs to exactly one epic. These are what QA/UAT validates — they must be testable.
> Full criteria stay in the RP.

#### EPIC-001 — [Deliverable title] · [objective/value]

| ID | Story | Acceptance criterion (Given/When/Then) |
|---|---|---|
| ST-001 | [As… I want… so that…] | [Given/When/Then] |

#### EPIC-002 — [Deliverable title] · [objective/value]

| ID | Story | Acceptance criterion (Given/When/Then) |
|---|---|---|
| ST-002 | [As… I want… so that…] | [Given/When/Then] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### A.7 Non-Functional Requirements (NFRs)
<!-- origination: id=a-nfrs; blocks=true; min-confidence=75; kind=capture -->
> Rubric: the product NFRs declared in the RP (§8), each with how it is verified. When
> escalated, each pairs with a feasibility answer in B.4 — keep the two consistent.

| Dimension | Requirement | Verification |
|---|---|---|
| [Performance / Security / …] | [Requirement] | [How] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### A.8 Edge Cases and Failure Modes
<!-- origination: id=a-edge-cases; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the edge cases and failure modes (RP §9), each with expected behavior. The PM and
> Tech Leads size the unhappy paths from this.

- [Edge case / failure → expected behavior]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Part B — Technical Definition (from the Technical Assessment · CTO)

> Summary of the TA — **inherited, never rewritten**. The complete source is the linked
> `TA-YYYY-NNN`. **When there was no escalation**, every B-section below is dispositioned
> `Disposition: decided` with content "N/A — no architectural escalation" (an honest
> disposition that clears the gate). See references/reconciliation.md.

### B.1 Feasibility Verdict
<!-- origination: id=b-feasibility; blocks=true; min-confidence=80; kind=capture -->
> Rubric: the CTO's verdict, **inherited from the TA — never re-decided in the PRD**. Carries
> the verdict + the caveats that must hold. `Infeasible as scoped` never reaches a PRD (a veto
> sends the RP back for re-scoping). N/A when not escalated.

| Field | Value |
|---|---|
| **Verdict** | Feasible / Feasible with caveats / N/A — no escalation |
| **Caveats** | [—] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### B.2 Nature and Technical Landscape
<!-- origination: id=b-nature-landscape; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the terrain engineering decides on, inherited from the TA. Brownfield → summary of
> the **current state** (patterns, integrations, debt) with link to the `tech-landscape`.
> Greenfield → summary of the **foundation** (chosen stack + target architecture). N/A when
> not escalated.

| Field | Value |
|---|---|
| **Nature** | Greenfield / Brownfield / Hybrid / N/A |
| **Knowledge base** | [reference or "created in this cycle" / N/A] |
| **Current state (brownfield)** | [Systems/patterns/integrations touched — or N/A] |
| **Foundation (greenfield)** | [Stack + target architecture — or N/A] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### B.3 Architectural Impact and Integrations
<!-- origination: id=b-arch-impact; blocks=true; min-confidence=75; kind=capture -->
> Rubric: each system/area touched and the nature of the impact, plus the required
> integrations under the technical-feasibility lens — inherited from the TA. N/A when not
> escalated.

| Area / System | Impact | Note |
|---|---|---|
| [Data model / Integration / …] | [Description] | |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### B.4 NFR Feasibility
<!-- origination: id=b-nfr-feasibility; blocks=true; min-confidence=75; kind=capture -->
> Rubric: the CTO's response to each RP NFR (A.7 / RP §8) — feasible? and how — inherited from
> the TA. Keep one row per A.7 NFR so the product↔technical loop stays closed. N/A when not
> escalated.

| NFR (from A.7) | Feasible? | Approach | Caveat |
|---|---|---|---|
| [Requirement] | Yes / With caveats / No | [How] | [—] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### B.5 Key Alternatives Considered
<!-- origination: id=b-alternatives; blocks=false; min-confidence=0; kind=capture -->
> Rubric: the rationale behind the technical decisions — what was discarded and why — so the
> downstream does not re-litigate it. Only the alternatives the PM needs to know. Inherited
> from the TA; "—" with `Disposition: decided` if none / not escalated.

| Alternative | Why it was NOT chosen |
|---|---|
| [Approach] | [Reason] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### B.6 Hard Constraints
<!-- origination: id=b-hard-constraints; blocks=true; min-confidence=75; kind=capture -->
> Rubric: the non-negotiable conditions that limit the solution space and their effect on
> scope — inherited from the TA. These feed `scope-reconciliation`. "None" with
> `Disposition: decided` if none; N/A when not escalated.

| Constraint | Effect on scope |
|---|---|
| [Constraint] | [What it limits] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### B.7 ADRs (architectural level)
<!-- origination: id=b-adrs; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the architectural decisions the CTO signed off, inherited from the TA. Fine-grained /
> implementation ADRs belong to the Tech Lead's Tech Backlog, not here. N/A when not escalated.

| # | Decision | CTO sign-off |
|---|---|---|
| ADR-001 | [Decision] | ✓ |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Scope Reconciliation
<!-- origination: id=scope-reconciliation; blocks=true; min-confidence=80; kind=derived; inputs=a-scope,b-feasibility,b-hard-constraints -->
> Rubric: **reconcile** the RP scope against the TA's verdict, caveats, and hard constraints.
> If the CTO imposed constraints or caveats that changed what the RP scoped, record exactly
> what changed and why — and ensure A.2 reflects the reconciled (final) scope. If nothing
> changed (or no escalation): "RP scope maintained in full." This is the PRD's reconciliation
> work — it is `derived`, computed from the inherited halves, never invented.

| Original item (RP) | Change after Technical Assessment | Reason |
|---|---|---|
| [Item] | Added / Removed / Re-scoped / Unchanged | [Constraint or caveat] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Consolidated Risk and Dependency View
<!-- origination: id=consolidated-risk; blocks=true; min-confidence=75; kind=derived; inputs=a-edge-cases,b-arch-impact,b-hard-constraints -->
> Rubric: a single table merging the **product/business risks** (from the RP, §12) with the
> **technical risks** (from the TA) — each tagged by origin and type, with probability, impact,
> and mitigation. The PM plans against this consolidated view. List known external
> dependencies explicitly. `derived` — composed from both halves, no new risks invented.

| Risk | Origin | Type | Probability | Impact | Mitigation |
|---|---|---|---|---|---|
| [Risk] | RP / TA | Product / Business / Technical / External / Compliance | High/Medium/Low | High/Medium/Low | [Mitigation] |

**Known external dependencies:** [client action, procurement, third-party integration — or "None"]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Effort and Cost (firm)
<!-- origination: id=effort-cost; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the **firm** estimate from the Technical Assessment (it replaces the RP's
> preliminary number). When **not escalated**, carry the RP's preliminary estimate and label
> it preliminary (the Tech Lead firms it in breakdown). Internal use only — not a contractual
> or client-facing commitment.

| Area | Estimate | Seniority |
|---|---|---|
| [Backend / Frontend / QA] | [X days] | [Seniority] |
| **Total** | **X days** | |

**Infra / Third parties / Recurring opex:** [summary or "None"]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Inherited Readiness and Open Dispositions
<!-- origination: id=inherited-readiness; blocks=true; min-confidence=70; kind=derived; inputs=a-scope,b-feasibility -->
> Rubric: what the PM must see before planning — the assumptions still to validate, the
> Discovery unknowns (resolved or open), and the delegated answers (with owner) that survived
> from upstream. If an assumption proves false during execution, the demand is re-triaged
> (downstream re-triage trigger). `derived` — carried forward from the RP/TA dispositions.

| Field | Value |
|---|---|
| **Assumptions still to validate** | [list or —] |
| **Discovery unknowns** | [resolved / open] |
| **Delegated requirements (with owner)** | [list or —] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Success Criteria and Metrics (projected)
<!-- origination: id=success-metrics; blocks=true; min-confidence=75; kind=capture -->
> Rubric: the projected baseline — primary metrics and guardrails (a guardrail is a metric
> that must NOT worsen) — inherited from the RP, with target, window, and confidence. This is
> what `metrics.md` (projected vs. actual) compares against post-rollout.

| Type | Metric | Target (projected) | Window | Confidence |
|---|---|---|---|---|
| **Primary** | [Metric] | [Target] | [Window] | __ |
| **Guardrail** | [Metric that must not worsen] | [Limit] | | __ |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Handoff to PM — Acceptance Gate
<!-- origination: id=handoff-gate; blocks=true; min-confidence=80; kind=derived; inputs=sign-off,scope-reconciliation,consolidated-risk,inherited-readiness -->
> Rubric: the delivery checklist the PM accepts (or rejects) against. The PM has **explicit
> authority to reject** the PRD and return it with **specific** gaps (not a generic "needs more
> detail"); the rejection and reason enter the Revision History, and the PO (or CTO, depending
> on the gap) addresses only the gaps and increments the version. Every box must be checkable
> from the merged document. `derived` — it asserts the merge is complete; it invents nothing.

| Delivery checklist | OK? |
|---|---|
| RP frozen (`freezeReady`) and referenced | ☐ |
| Technical Assessment signed off (or N/A justified) | ☐ |
| Scope reconciliation recorded | ☐ |
| Risks and dependencies consolidated | ☐ |
| External dependencies explicit | ☐ |
| Open dispositions visible | ☐ |

**Priority and business context:** [why this demand, now]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

<!-- END OF DOCUMENT -->
