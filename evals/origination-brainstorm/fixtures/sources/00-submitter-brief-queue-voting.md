# Submitter Document — Queue Voting

> **This is the Submitter document** — the first artifact of the journey (`00`) and the deliverable of the Submitter persona. It **makes tangible** the model from [`personas/01-submitter.md`](../personas/01-submitter.md): the reasoning (compliance requirements, ToDo generation, score formula) lives in the persona; this document **instantiates** it per demand, in the **Submitter's language** — problem, value, pain, opportunity. Each answer carries how solid it is and where it came from: the confidence layer travels *with* the capture.
>
> **Journey:** `00 Submitter Document` → [`01 Origination Record (PO — triage)`](./01-origination-record-queue-voting.md) → [`02 Readiness Package (PO)`](./02-readiness-package-queue-voting.md) → `03 Technical Assessment — not requested` → [`04 PRD (PO+CTO → PM)`](./04-prd-queue-voting.md). See [`README.md`](./README.md).
>
> **Nothing precedes this document as an artifact.** What comes before is **raw signal** — a quarterly review call with the customer — which **is not an artifact**. That signal enters *here* as evidence/source (disposition `inferred`, with `source`); it is the **capture** that turns it into this first formal document.
>
> **Handoff:** freezes when `gateReady = true` (every blocking requirement resolved by an honest disposition) and is delivered to the **PO**, who formalizes and triages it in the [`01 Origination Record`](./01-origination-record-queue-voting.md).

## The two lenses (every demand is read through both at the same time)

> See [`personas/01-submitter.md` §2](../personas/01-submitter.md). The ToDos live where the lenses intersect: "given what *this* demand means, what does the contract still need?"

| Lens | What it is | Where it shows up in this document |
|---|---|---|
| **Contract** (deterministic) | The fixed compliance requirements every demand must satisfy to move forward | **Readiness Summary** + the numbered requirements (score + open items) |
| **Semantic** (contextual) | What *this* demand means: the facilitator's lack of control over the estimation flow — the real pain is the ungoverned ceremony, not the absence of a "button" | **Problem Statement**, **Impact**, **Value Indicators** and their tensions |

## Metadata

| Field | Value |
|---|---|
| **Demand** | Queue Voting |
| **Recorded by** | Ana Costa (Customer Success) |
| **Capture date** | 2026-03-12 |
| **Status** | Ready for handoff (`gateReady`) |
| **Linked Origination Record** | INT-2026-001 |

## Revision History

| Version | Date | Event | Summary |
|---|---|---|---|
| v1 | 2026-03-12 | Capture started | Ana Costa recorded the demand from a quarterly review call with Banco Meridional. All blocking requirements resolved. Handoff to PO the same day. |

---

## Readiness Summary

> Snapshot of the capture. The score is derived from the requirements below; `low_confidence` counts as partial. The demand is only delivered to the PO when all blocking requirements are resolved (`gateReady = Yes`).

| Field | Value |
|---|---|
| **Readiness Score** | 87 % |
| **Gate released (gateReady)** | Yes |
| **Pending blocking requirements** | — (all 4 blocking requirements resolved) |
| **Dispositions** | 5 answered · 1 inferred · 3 assumptions · 0 discovery · 0 deferred |

### Confidence legend (applies to each answered section)

| Attribute | Values |
|---|---|
| **Confidence** | 0–100 |
| **Source** | Submitter direct · Attached document (p.X) · Inferred · Assumption · Other stakeholder |
| **Status** | Empty · Low confidence · Resolved |
| **Disposition** | Answered · Inferred · Assumption (to validate) · Discovery (to investigate) · Delegated (owner: __) |
| **Hint** | Why confidence is low / what would raise it |

> **"I don't know" does not block.** A requirement reaches readiness through any honest disposition — including "nobody knows yet, and this is the plan" (Discovery) or "we're assuming X" (Assumption). See [`personas/01-submitter.md` §6](../personas/01-submitter.md).

---

## Origin  ·  *(Requirement 2 — Originator and context)*

| Field | Value |
|---|---|
| **Source** | Customer |
| **Customer / Requester** | Banco Meridional |
| **Originator and context** | Scrum Masters / facilitators at Banco Meridional, quarterly review call with CS on 2026-03-12. The pain was raised spontaneously during the contract renewal agenda: "without this it's hard to justify the renewal to the squads that haven't adopted yet." |
| **Reported via** | Quarterly review call (CS → customer) |

`Confidence:` 95 · `Source:` Submitter direct (Ana Costa, present on the call) · `Status:` Resolved · `Disposition:` Answered · `Hint:` —

---

## Type

- [x] Feature
- [ ] Bug
- [ ] Enhancement
- [ ] Compliance
- [ ] Integration
- [ ] Operational

---

## Problem Statement  ·  *(Requirement 1 — blocks gate)*

> What is the existing pain? Describe the problem, not the solution. If the statement contains a proposed solution, it goes back for reformulation.

During sprint planning ceremonies, the Banco Meridional teams use the platform to estimate user stories. The facilitator (Scrum Master) has no way to control which stories will be presented and in what order — all participants see the full backlog simultaneously.

The direct consequence: participants read future items ahead of time, form early opinions, and destabilize the estimation flow. The ceremony loses cadence. To work around this, facilitators send one story at a time via chat — a workaround that adds 15–20 minutes of overhead per session.

There is a second layer to the problem: votes appear in real time as they are submitted. Participants who vote last copy the first votes they see, creating anchoring bias and degrading estimate quality.

`Confidence:` 92 · `Source:` Submitter direct (reported by the Scrum Masters on the call) · `Status:` Resolved · `Disposition:` Answered · `Hint:` —

---

## Who Is Impacted (Reach)  ·  *(Requirement 3 — blocks gate)*

> Personas, segments, or teams that feel this pain. This is the "Reach" of the value indicators.

| Persona / Segment | How they are impacted |
|---|---|
| Scrum Masters / Facilitators at Banco Meridional | Lose control of the ceremony flow. Resort to costly manual workarounds. They are the direct users requesting the change. |
| Developers / Voters at Banco Meridional | Exposed to anchoring bias. Less accurate estimates. Longer ceremonies. |
| 3 pending squads (not active on the platform) | The absence of this feature is the adoption blocker cited explicitly on the call. |
| CS (Ana Costa) | Carries the renewal risk of the largest enterprise contract in the portfolio. |

`Confidence:` 88 · `Source:` Submitter direct + inferred from the account context (12 squads, 4 active, 3 blocked by this gap) · `Status:` Resolved · `Disposition:` Answered · `Hint:` The exact number of unique users per squad was not collected on the call — raising it to 95 would require account usage data.

---

## Business Impact  ·  *(Requirement 4 — blocks gate)*

> Use the applicable dimensions. Revenue, Retention, Operational, Competitive, Compliance, Market are the most common. Don't force irrelevant dimensions. Quantify when possible.

| Dimension | Detail |
|---|---|
| **Revenue** | 3 Banco Meridional squads not onboarded; expansion blocked directly by this UX gap. Estimated expansion ARR: R$ 28,000/year (assumption: same ticket per squad as the 4 active ones). |
| **Retention** | Contract renewal in 90 days. CS flagged it as a churn risk if the gap is not addressed before the renewal conversation. ARR at risk: R$ 84,000 (4 active squads × R$ 21,000). |
| **Operational** | Manual sharing workaround via chat adds 15–20 min per ceremony. Estimated cost in lost team hours not calculated at capture. |
| **Competitive** | Two competing tools already offer sequential control and vote hiding. Cited as a differentiation gap on the renewal call — the customer has a viable alternative in the market. |

`Confidence:` 80 · `Source:` Submitter direct (retention and competitive); inferred from account data (revenue) · `Status:` Resolved · `Disposition:` Answered + Assumption (expansion ARR assumes the same ticket as the active squads) · `Hint:` Confirm ticket per squad with CS / Finance before the RP to firm up the expansion number.

---

## Value Indicators (RICE-lite)

> A mirror to challenge the thinking — **not** an automatic ranking. Score each one (Low / Medium / High). Confidence reuses the column above — don't score it again. Effort stays *soft* (Submitter's guess, firmed up later by the CTO).

| Indicator | Score | Rationale (in their language) | Confidence |
|---|---|---|---|
| **Impact** ("how much does it move the business?") | High | R$ 84k ARR renewal at risk + R$ 28k expansion blocked. Competitive gap with alternatives in the market. | 80 |
| **Reach** ("how many feel this?") | Medium | 4 active squads (direct users of the pain) + 3 blocked squads. Within one account, but it is the largest enterprise customer in the portfolio. | 75 |
| **Urgency** ("why now? cost of waiting?") | High | Renewal in 90 days creates a non-negotiable window. Each month without delivery is another month of workaround and of risk of losing the renewal conversation. | 90 |
| **Effort** *(soft — deferred to the CTO)* | Medium | CS's initial guess: looks like UI + session state, no new infrastructure. CTO must confirm. | low_confidence |

> **Tensions recorded:**
> - **Medium Reach + High Impact:** apparent tension — reach is limited to one account. Resolution: the financial impact is disproportionate to the reach because it is the largest enterprise customer. The R$ 84k renewal plus the R$ 28k expansion justify the high impact score even with concentrated reach.
> - **High Urgency + soft Effort:** the 90-day deadline applies pressure, but effort is not firmed up. Honest resolution: if the CTO identifies an architectural blocker, the deadline becomes the scope-cutting constraint, not a reason to postpone.

---

## Urgency  ·  *(Requirement 5)*

**Deadline / window:** Banco Meridional contract renewal in 90 days from 2026-03-12 (expiration ~2026-06-10). The feature must be in production before the renewal conversation.

**Cost of waiting:** If delivery does not happen before the renewal, the customer has a concrete argument to not renew or to reduce the contract — and has alternatives in the market. CS has already flagged that the topic was explicitly placed on the renewal call agenda.

`Confidence:` 90 · `Source:` Submitter direct (Ana Costa) · `Status:` Resolved · `Disposition:` Answered · `Hint:` —

---

## Evidence and Documents  ·  *(Requirement 6)*

> Attachments or prior conversations that ground the demand. Source for AI pre-filling.

| Document / Conversation | Type | Relevance |
|---|---|---|
| Quarterly review call with Banco Meridional — 2026-03-12 | Call (CS notes) | Primary source: pain raised by the Scrum Masters, mention of the renewal risk and the competitive gap. |
| Banco Meridional support ticket history | Internal records | CS mentions that 3 other enterprise customers reported a similar pain informally. The tickets were not formalized. |

`Confidence:` 70 · `Source:` Submitter direct (call notes) + inferred (informal tickets) · `Status:` Resolved · `Disposition:` Answered + Inferred · `Hint:` Formalizing the tickets from the 3 other customers would raise confidence and strengthen the business case beyond Banco Meridional.

---

## Stakeholders  ·  *(Requirement 8)*

| Stakeholder | Role | Interest | Influence |
|---|---|---|---|
| Ana Costa | Customer Success — recorder of the demand, owner of the relationship | Retention of the Banco Meridional renewal; avoid R$ 84k ARR churn | High |
| Scrum Masters at Banco Meridional | End users (facilitators) — direct originators of the pain | Control of the ceremony flow and vote integrity | High — users who adopt or don't adopt |
| Developers at Banco Meridional | End users (voters) | Less distraction, more focused estimates, shorter ceremonies | Medium |
| Lucas Mendes | PO | Alignment of the product with the pain and quality of the delivery | High — decides whether it moves forward and in what form |
| CEO | Executive sponsor | Revenue retention and health of the enterprise relationship | Medium — informed of the risk, not involved in the detail |

`Confidence:` 85 · `Source:` Submitter direct · `Status:` Resolved · `Disposition:` Answered · `Hint:` PM not yet defined (to be defined by the PO during triage).

---

## Assumptions

Conditions assumed true at capture. If an assumption proves false, the demand must be re-triaged. Assumptions are a **valid disposition** for requirements without a direct answer.

1. The existing WebSocket infrastructure supports new event types without requiring a new broker or messaging layer. — `to validate with:` CTO / Tech Lead during rationalization
2. Session state persistence can be extended with new fields (queue order, reveal state) without a full schema migration. — `to validate with:` CTO / Tech Lead during rationalization
3. The Banco Meridional Scrum Masters have the autonomy to adopt new features without approval from their organization's IT. — `to validate with:` Ana Costa (CS) + direct contact with the customer
4. Co-facilitation is not needed in this release — a single-facilitator model is sufficient for Banco Meridional now. — `to validate with:` Ana Costa (CS) on the next call with the customer
5. The ticket per squad of the 3 pending squads is equivalent to that of the 4 active ones (basis for the estimated expansion ARR). — `to validate with:` Finance / CS before the RP

---

## Constraints  ·  *(Requirement 7)*

Conditions that limit the solution space, to be respected regardless of what is built.

| Constraint | Type | Detail |
|---|---|---|
| Renewal deadline | Time | Renewal in ~90 days. The feature must be in production before the Banco Meridional renewal conversation. |
| No mobile redesign | Scope | The existing mobile layout applies. No investment in mobile UI in this release. |
| Single-facilitator model | Scope | Co-facilitation is explicitly out of scope in this release. The architecture must not make it impossible in the future, but does not need to implement it now. |
| Zero-downtime deploy | Technical | The feature must be deployable without interrupting active sessions. |
| No new external services | Budget | Built on existing infrastructure. No new third-party service may be contracted. |

`Confidence:` 88 · `Source:` Submitter direct (deadline + scope) + inferred (zero-downtime deploy, platform standard) · `Status:` Resolved · `Disposition:` Answered + Assumption (zero-downtime deploy inferred as the operational standard) · `Hint:` —

---

## Preliminary Risks

Risks identified at capture — before the technical assessment. The full record belongs to the Readiness Package.

| Risk | Category | Initial Assessment |
|---|---|---|
| WebSocket event-ordering inconsistencies under load | Technical | Unknown — requires load testing during QA |
| Vote-hiding bypass via client-side inspection | Security | Likely mitigable — the server must enforce the hiding, not the client |
| Session state loss on facilitator reconnection | Technical | Requires resilience design — grace period or session snapshot |
| Anchoring bias not fully eliminated (participants can still speak verbally) | Product | Accepted — the platform controls only digital visibility |
| Renewal deadline missed if rationalization reveals blockers | Schedule | Low probability based on the initial assessment; the demand appears circumscribed to UI and session state |

---

## High-Level Scope Boundary

**In:** Facilitator queue management (add, order, reveal one by one), vote hiding until explicit reveal, facilitator-controlled vote reveal, session state persistence, basic controls (skip, return, end).

**Out:** Per-item timers, automatic vote reveal, co-facilitation / multi-facilitator control, mobile redesign, reports and analytics, Jira/Linear integration.

**Deferred:** Automatic-reveal preference toggle, queue template reuse across sessions, ceremony analytics dashboard.

---

## Priority

**Level:** High

**Reason:** Banco Meridional contract renewal in 90 days. CS flagged it as a potential churn risk if not resolved before the renewal conversation.

---

## Success Criteria

High-level indicators that define "done and valuable." Detailed measurable targets belong to the Readiness Package; these are the capture-level signals. **They serve as a projected baseline** for post-handoff tracking (see [`metrics.md`](../metrics.md)).

| Criterion | Type | Indicator | Projected value |
|---|---|---|---|
| Banco Meridional contract renewed | Business | Renewal signed before the expiration date | R$ 84,000 ARR retained |
| 3 pending squads onboarded | Business | Squad activation count in the account dashboard within 60 days of release | +R$ 28,000 expansion ARR |
| Ceremony duration reduced | Operational | Average session time for ceremonies with 10+ items drops ≥ 20% vs. baseline | ≥ 20% reduction |
| Facilitator workaround eliminated | Operational | Zero CS tickets reporting manual story sharing post-release | 0 tickets |
| Zero vote-anchoring complaints | Quality | Zero CS tickets citing premature vote visibility | 0 tickets |
| Feature adopted without training | UX | Facilitators enable the queue and reveal without support intervention | 0 onboarding calls |
