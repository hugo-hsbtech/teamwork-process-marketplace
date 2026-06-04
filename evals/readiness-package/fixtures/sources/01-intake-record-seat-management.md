# Intake Record — Enterprise Seat Management Self-Service
<!-- rev: 1 · updated: 2026-06-03 -->

> The formal intake artifact. Input for the readiness-package eval: a Product Ready
> intake record for INT-2026-014, seat management self-service for enterprise admins.
> Fictional, self-contained; consistent with the golden RP (RP-2026-014).

## Metadata
<!-- intake: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Field | Value |
|---|---|
| **Record ID** | INT-2026-014 |
| **Version** | v1 |
| **Originator (Submitter)** | Carla Mendes (Customer Success) |
| **Triaged by (owner)** | Ana Ribeiro (PO) |
| **Date registered** | 2026-03-18 |
| **Date triaged** | 2026-03-21 |
| **Status** | Triaged |
| **Output language** | pt-BR |

## Revision history
<!-- intake: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Version | Date | Event | Summary |
|---|---|---|---|
| v1 | 2026-03-18 | Intake drafted | Filled from CS brief + support export; triage drafted. |
| v1.1 | 2026-03-21 | Triage confirmed | PO Ana Ribeiro confirmed Product Ready; CTO escalation flagged. |

---

## Readiness received
<!-- intake: id=readiness; blocks=false; min-confidence=0; kind=derived; inputs=problem,reach,impact,originator,urgency -->

| Field | Value |
|---|---|
| **Readiness score** | 82 % |
| **Blocking requirements** | All resolved by honest disposition (gate) — Yes |
| **Open dispositions** | 2 assumptions to validate · 1 discovery · 1 deferred |

---

## Consolidated demand

> One-screen read of the demand, each dimension carrying its inherited confidence.

### Problem (the pain, not the solution)
<!-- intake: id=problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: describe the existing pain with observable symptoms — what hurts, for
> whom, how it shows up today. If it names a solution ("build X"), it is NOT
> satisfied: reframe to the pain underneath.

Enterprise admins have no direct access to seat management in the product. Every addition or removal of a license requires opening a support ticket — there is no self-service path. The CS team handles each request manually in the backend and confirms by email, creating a structural 1–3 business-day lead time. In Q1 2026, 240 tickets (18% of total enterprise volume) were of this type. Admins in high-churn accounts report 5–10 such tickets per month; in onboarding waves the lead time reaches 3 days and blocks new team members from day-1 access. Three enterprise accounts flagged this dependency as a renewal concern in Q4 2025 interviews.

`Confidence:` 88 · `Source:` Submitter direct (CS brief) + support export Q1 2026 + CS interview notes Q4 2025 · `Status:` resolved · `Disposition:` answered · `Hint:` breakdown of 240 tickets by account not available yet; CS can extract in ~1 week — would raise to ~93

### Originator & context
<!-- intake: id=originator; blocks=true; min-confidence=70; kind=capture -->
> Rubric: who raised it and in what situation (e.g. "COO, Q2 planning"), and the
> channel it came through.

Raised by Carla Mendes (Customer Success) on the Q1 2026 product-review call, citing friction reported by the enterprise admin cohort and three at-risk renewal accounts. Logged via the CS feedback channel. Escalated to PO for triage after the support export confirmed the ticket volume.

`Confidence:` 95 · `Source:` Submitter direct · `Status:` resolved · `Disposition:` answered · `Hint:` —

### Who is impacted (reach)
<!-- intake: id=reach; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the personas / segments / teams who feel the pain, each with *how* they
> are affected.

**Enterprise Admins** (role `billing_admin`): cannot add or remove seats without intermediary; every headcount change (hire, departure, restructure) requires a support request. Estimated 80–120 active enterprise admins across the platform.

**CS Analysts**: field ~240 repetitive, low-complexity seat-management tickets per quarter, blocking capacity for higher-value support work.

**New team members**: day-1 access delayed by 1–3 days when admin cannot provision immediately.

**Finance contacts** (read-only): no visibility into current seat count or billing impact without requesting extracts from CS.

`Confidence:` 82 · `Source:` Submitter direct + support export Q1 2026 + CS interview notes Q4 2025 · `Status:` resolved · `Disposition:` answered · `Hint:` admin headcount (80–120) is an estimate from account records; exact count per account not pulled

### Business impact
<!-- intake: id=impact; blocks=true; min-confidence=70; kind=capture -->
> Rubric: value across the applicable dimensions (revenue, retention, operational,
> competitive, compliance) — quantified when possible. Estimates are fine if
> marked low-confidence with a hint on what would firm them up.

**Operational cost:** 240 tickets/quarter at an estimated R$ 120–180 per ticket (analyst time + overhead) = R$ 29k–43k/quarter in avoidable CS cost.

**Retention risk:** 3 enterprise accounts (combined ARR not disclosed in this record) explicitly flagged the seat-management friction in Q4 2025 renewal conversations. Loss of even one would represent significant ARR impact.

**Revenue blockers:** Admins who cannot add seats quickly have reported delaying headcount requests — potential expansion revenue sitting idle.

**Competitive signal:** At least two competitors already offer self-service seat management; the gap is visible in procurement evaluations.

`Confidence:` 78 · `Source:` Support export Q1 2026 + CS interview notes Q4 2025 + PM market scan · `Status:` resolved · `Disposition:` answered · `Hint:` cost-per-ticket is CS estimate; ARR at risk not quantified (Finance to confirm); competitive comparison based on PM research, not customer statement

### Urgency — why now
<!-- intake: id=urgency; blocks=false; min-confidence=70; kind=capture -->
> Rubric: why now and the cost of waiting — a window, a deadline, a compounding
> cost.

Q2 2026 has two renewal cohorts covering accounts that flagged this issue. The demand compounds: as the enterprise base grows, ticket volume scales linearly with headcount churn — the R$ 29k–43k/quarter cost estimate grows proportionally. Each quarter without the feature adds ~240 avoidable tickets and defers expansion revenue tied to fast onboarding.

`Confidence:` 80 · `Source:` Submitter direct + support trend data · `Status:` resolved · `Disposition:` answered · `Hint:` renewal-cohort count confirmed with CS; projected ticket volume growth is linear assumption, not a modeled forecast

### Declared priority
<!-- intake: id=priority; blocks=false; min-confidence=0; kind=capture -->

**Level:** High — **Reason:** compounding operational cost + active renewal risk + competitive gap; the combination clears the bar for immediate roadmap entry.

---

## Triage — routing decision
<!-- intake: id=triage; blocks=false; min-confidence=0; kind=derived; inputs=problem,reach,impact,urgency,assumptions -->

> ⚠️ **TRIAGE DRAFT — AI-generated from the capture, pending owner confirmation.**
> The verdicts and routing below are a *proposal* grounded in captured evidence,
> not a final call. A human owner must review, adjust, and sign off. Until then
> `Status` = *In triage* and this section's disposition is `low_confidence`.

### Criteria assessed

| # | Criterion | Verdict | Rationale | Basis / source |
|---|---|---|---|---|
| 1 | A real problem (not an isolated symptom)? | Yes | 240 tickets/quarter from the entire enterprise cohort; 3 accounts flagged at renewal; admin cohort reports 5–10 tickets/admin/month. | Problem capture + support export |
| 2 | Recurring / has volume? | Yes | 18% of total enterprise ticket volume; steady across Q4 2025 and Q1 2026. | Support export Q1 2026 |
| 3 | Fits the product vision? | Yes | Self-service operations for enterprise admins are core to the product's enterprise positioning. | PO judgment |
| 4 | Technical & business impact? | High (business) / Medium (technical) | R$ 29k–43k/quarter avoidable cost; retention and expansion risk; billing and provisioning coupling require architectural review. | Impact capture + CTO flag |
| 5 | Do urgency & impact justify now? | Yes | Q2 renewal cohort + linear cost compounding. | Urgency capture |

### Decision

| Field | Value |
|---|---|
| **Decision** | Product Ready |
| **Rationale** | All blocking sections answered at solid confidence; open items (breakdown by account, ARR at risk) are refinement data, not blockers. CTO escalation flagged for billing/provisioning architecture. |
| **Reversible?** | Yes |
| **Originator notified** | 2026-03-21 — Carla Mendes notified by Ana Ribeiro (PO). |

---

## Architectural escalation
<!-- intake: id=cto_escalation; blocks=false; min-confidence=0; kind=derived; inputs=impact,constraints,assumptions -->

**Needed:** Yes — seat management touches billing and provisioning; consistency guarantees (no cobrança sem provisionamento e vice-versa), idempotency, and potential sync/async architecture require CTO review before scope freezes. Draft signal, pending owner confirmation.

---

## Assumptions
<!-- intake: id=assumptions; blocks=false; min-confidence=0; kind=capture -->

| Assumption | Verdict (draft) | Validate with |
|---|---|---|
| Billing platform supports prorated seat additions mid-cycle | To validate | CTO / Technical Assessment |
| 240 tickets/quarter is representative of the ongoing baseline (not a Q1 spike) | Accepted | CS (trend data confirmed across Q4 2025 and Q1 2026) |
| Breakdown of tickets by account can be extracted by CS in ~1 week | To validate | CS team |

---

## Constraints
<!-- intake: id=constraints; blocks=false; min-confidence=70; kind=capture -->

| Constraint | Type | Note |
|---|---|---|
| No manual CS intervention for standard seat changes post-rollout | Scope | The feature must fully eliminate the CS dependency for add/remove; escalation path remains for exceptions. |
| LGPD compliance for audit log data (name/email in event records) | Legal | DPO alignment required before rollout. |
| No changes to the billing provider contract in this release | External | Provisioning logic must work within current billing provider capabilities. |

`Confidence:` 85 · `Source:` PO + CS alignment · `Status:` resolved · `Disposition:` answered · `Hint:` LGPD constraint flagged by PO; DPO confirmation pending

---

## Handoff
<!-- intake: id=handoff; blocks=false; min-confidence=0; kind=derived -->

- **Product Ready:** proceed to Readiness Package (RP-2026-014, assignee Ana Ribeiro).
- CTO escalation flagged: Technical Assessment TA-2026-014 to be opened in parallel.
- Discovery item: CS to extract ticket breakdown by account — feeds RP §Métricas.

<!-- END OF DOCUMENT -->
