# Submitter Document — Room Access Control

> **This is the Submitter Document** — the first artifact of the journey (`00`) and the deliverable of the Submitter persona. It **makes tangible** the model from [`personas/01-submitter.md`](../personas/01-submitter.md): the reasoning (compliance requirements, ToDo generation, score formula) lives in the persona; this document **instantiates** it per demand, in the **Submitter's language** — problem, value, pain, opportunity. Each answer carries how solid it is and where it came from: the confidence layer travels *with* the capture.
>
> **Journey:** `00 Submitter Document` → [`01 Intake Record (PO — triage)`](./01-intake-record-access-control.md) → [`02 Readiness Package (PO)`](./02-readiness-package-access-control.md) → [`03 Technical Assessment (CTO)`](./03-technical-assessment-access-control.md) → [`04 PRD (PO+CTO → PM)`](./04-prd-access-control.md). See [`README.md`](./README.md).
>
> **Nothing precedes this document as an artifact.** What comes before is **raw signal** — a pre-close call with the customer, an email thread with Sales, a meeting note — which **is not an artifact**. That signal enters *here* as evidence/source (disposition `inferred`, with `source`); it is the **capture** that transforms it into this first formal document.
>
> **Handoff:** it freezes when `gateReady = true` (every blocking requirement resolved by an honest disposition) and is handed off to the **PO**, who formalizes and triages it in the [`01 Intake Record`](./01-intake-record-access-control.md).

## The two lenses (every demand is read through both at the same time)

> See [`personas/01-submitter.md` §2](../personas/01-submitter.md). The ToDos live where the lenses intersect: "given what *this* demand means, what does the contract still need?"

| Lens | What it is | Where it appears in this document |
|---|---|---|
| **Contract** (deterministic) | The fixed compliance requirements that every demand must satisfy to advance | **Readiness Summary** + the numbered requirements (score + open items) |
| **Semantic** (contextual) | What *this* demand means: the real pain (open access exposes identities in mixed ceremonies), its value thesis (R$ 42k deal blocked), its unknowns (Azure AD, LGPD, Jira) | **Problem Statement**, **Impact**, **Value Indicators** and their tensions |

## Metadata

| Field | Value |
|---|---|
| **Demand** | Room Access Control |
| **Logged by** | Rafael Souza (Sales) |
| **Capture date** | 2026-03-15 |
| **Status** | Ready for handoff (`gateReady`) |
| **Linked Intake Record** | INT-2026-002 (assigned by the PO at triage) |

## Revision History

| Version | Date | Event | Summary |
|---|---|---|---|
| v1 | 2026-03-15 | Capture started and completed | Sales (Rafael Souza) captured the demand immediately after a pre-close call with Construtora Ágil. All blocking requirements resolved by honest disposition; 3 integration unknowns logged as Discovery. |

---

## Readiness Summary

> Snapshot of the capture. The score is derived from the requirements below; `low_confidence` counts as partial. The demand is only handed off to the PO when all blocking requirements are resolved (`gateReady = Yes`).

| Field | Value |
|---|---|
| **Readiness Score** | 84 % |
| **Gate released (gateReady)** | Yes |
| **Open blocking requirements** | — (all resolved by honest disposition) |
| **Dispositions** | 5 answered · 1 inferred · 4 assumptions · 3 discovery · 0 delegated |

> **How to read the score:** the blocking requirements (1, 2, 3, 4) are all resolved. The score sits below 100% because urgency (req. 5) and constraints (req. 7) have fields with `low_confidence` and the 3 integration unknowns enter as `discovery` — an honest disposition that counts partially in the calculation. This does not block the gate; it only signals what the PO needs to watch.

### Confidence legend (applies to each answered section)

| Attribute | Values |
|---|---|
| **Confidence** | 0–100 |
| **Source** | Submitter direct · Attached document (p.X) · Inferred · Assumption · Other stakeholder |
| **Status** | Empty · Low confidence · Resolved |
| **Disposition** | Answered · Inferred · Assumption (to validate) · Discovery (to investigate) · Delegated (owner: __) |
| **Hint** | Why confidence is low / what would raise it |

> **"I don't know" doesn't block.** A requirement reaches readiness by any honest disposition — including "nobody knows yet, and this is the plan" (Discovery) or "we're assuming X" (Assumption). See [`personas/01-submitter.md` §6](../personas/01-submitter.md).

---

## Origin  ·  *(Requirement 2 — Originator and context)*

| Field | Value |
|---|---|
| **Source** | Customer |
| **Customer / Requester** | Construtora Ágil (mid-market, onboarding process underway) |
| **Originator and context** | Rafael Souza (Sales), pre-close call on 2026-03-15. Construtora Ágil's IT Lead (Fernanda Ramos) and Scrum Masters joined the call. |
| **Reported via** | Pre-close video call — notes logged by Rafael immediately after the call |

`Confidence:` 95 · `Source:` Submitter direct · `Status:` Resolved · `Disposition:` Answered · `Hint:` —

---

## Type

- [x] Feature
- [ ] Bug
- [ ] Enhancement
- [x] Compliance
- [x] Integration
- [ ] Operational

---

## Problem Statement  ·  *(Requirement 1 — blocks gate)*

> What is the existing pain? Describe the problem, not the solution.

Construtora Ágil runs agile planning ceremonies with mixed teams: internal developers, external contractors, and product managers. The platform's current model is completely open — anyone with the room link gets in, sees the names of all participants, and can vote. This creates three concrete pains:

1. **No entry control:** external contractors with the link can join without facilitator approval, violating the company's internal data governance policy.
2. **No anonymity among voters:** in sessions with contractors, cross-visibility of identities is prohibited by internal policy. Today there is no way to hide who is in the room.
3. **No role distinction:** product managers and executives who want to follow the ceremony without influencing the estimates have no observation mode — they either join as voters or stay out.

The result is that Construtora Ágil **cannot onboard** without these gaps being addressed. The deal is conditioned on the feature.

`Confidence:` 92 · `Source:` Submitter direct · `Status:` Resolved · `Disposition:` Answered · `Hint:` —

---

## Who Is Impacted (Reach)  ·  *(Requirement 3 — blocks gate)*

> Personas, segments, or teams that feel this pain.

| Persona / Segment | How it is impacted |
|---|---|
| **Construtora Ágil's Scrum Masters** | Need granular control over who enters and what they see; today they manage access outside the platform (manual workaround). |
| **Construtora Ágil's external contractors** | Take part in sessions but should not see peers' identities; today they see everything. |
| **Product Managers / Executives** | Want to observe the ceremonies without voting; today they either join as voters (influencing the process) or don't join at all. |
| **Construtora Ágil's IT Lead (Fernanda Ramos)** | Responsible for LGPD compliance and Azure AD integration; needs technical guarantees before go-live. |
| **Enterprise deals in pipeline (2 identified)** | 2 other prospects with the same requirement flagged by Sales in Q1. |

`Confidence:` 88 · `Source:` Submitter direct + inferred from the call · `Status:` Resolved · `Disposition:` Answered · `Hint:` The 2 pipeline deals are Sales signals, with no written confirmation from the customer — confidence slightly below the main deal.

---

## Business Impact  ·  *(Requirement 4 — blocks gate)*

> Applicable dimensions quantified when possible.

| Dimension | Detail |
|---|---|
| **Revenue** | Construtora Ágil deal: R$ 42,000/year (ARR). Conditioned on this feature — without it, the contract doesn't close. Sales made an informal delivery commitment of 60 days (to validate with the PM before confirming to the customer). |
| **Market** | 2 other enterprise deals in pipeline with the same requirement flagged by Sales in Q1. Potential of R$ 84,000+ in additional ARR if the feature is generic enough. |
| **Retention** | Not applicable — customer not yet onboarded. Becomes relevant after onboarding. |
| **Operational** | Scrum Masters use manual workarounds today (controlling who receives the link, notifying outside the platform). Real operational impact for the facilitator. |
| **Compliance** | Construtora Ágil operates under internal data governance policies. LGPD requirement: participant identity data must reside in Brazil. Non-negotiable for this customer. |

`Confidence:` 90 · `Source:` Submitter direct (main deal) + inferred (pipeline) · `Status:` Resolved · `Disposition:` Answered · `Hint:` The value of the 2 pipeline deals is not quantified — assumption that they follow a profile similar to Construtora Ágil. The Sales 60-day commitment has no capacity validation; the PO should investigate before confirming.

---

## Value Indicators (RICE-lite)

> A mirror to challenge the thinking — **not** an automatic ranking. Effort stays *soft* (Submitter's guess; firmed up later by the CTO).

| Indicator | Score | Rationale (in their language) | Confidence |
|---|---|---|---|
| **Impact** ("how much does it move the business?") | High | R$ 42k ARR blocked + 2 deals in pipeline with the same requirement. The feature unlocks an enterprise segment that today cannot onboard. | 88 |
| **Reach** ("how many feel this?") | Medium | Directly affects Construtora Ágil + the 2 pipeline deals. On the current platform, it impacts the enterprise/regulated segment — a minority of total volume but high value per account. | 75 |
| **Urgency** ("why now? cost of waiting?") | High | Every week without the feature delays closing the deal and increases the risk of the customer looking for an alternative. Sales already made an informal 60-day commitment. | 85 |
| **Effort** *(soft — deferred to the CTO)* | High | Sales intuition: involves access control, Azure AD integration, and LGPD compliance. Probably larger than it looks. | low_confidence |

> **Tensions logged:**
> - **High Impact + Medium Reach:** the per-account impact is high (R$ 42k), but immediate reach is restricted to a specific segment. Resolution: the value per account is enough to justify it; the pattern created serves as a basis for the broader enterprise segment.
> - **High Urgency + High Effort (soft):** real risk that the informal 60-day deadline is not viable if the effort is larger than expected. Disposition: technical Discovery before any external date commitment.

---

## Urgency  ·  *(Requirement 5)*

**Deadline / window:** Sales made an informal commitment to the customer of delivery in 60 days starting mid-March. No date is confirmed until the PM runs a capacity assessment. Critical window: if the deal doesn't close in Q2, it enters prospect churn risk.

**Cost of waiting:** Construtora Ágil does not start onboarding without this feature. Each week of delay is a week of lost MRR. In addition, the 2 pipeline deals may look for alternatives if delivery slips too much.

`Confidence:` 80 · `Source:` Submitter direct · `Status:` Low confidence · `Disposition:` Assumption (to validate) · `Hint:` The 60-day deadline is an informal Sales commitment, with no PM capacity validation. Confidence rises once the PM confirms the deadline is feasible.

---

## Evidence and Documents  ·  *(Requirement 6)*

> Attachments or prior conversations that back the demand.

| Document / Conversation | Type | Relevance |
|---|---|---|
| Pre-close call notes (2026-03-15) | Internal Sales notes | Primary source: pain described by Construtora Ágil's Scrum Masters and IT Lead |
| Follow-up email from Fernanda Ramos (IT Lead) | Email thread | Written confirmation of the LGPD requirements and the need for Azure AD integration |
| Q1 pipeline signals (Sales) | Internal CRM | 2 deals with a similar requirement identified by Rafael Souza |

`Confidence:` 78 · `Source:` Submitter direct + document · `Status:` Low confidence · `Disposition:` Answered · `Hint:` Call notes are Sales' perception, not a transcript. Fernanda's email raises confidence on the LGPD/Azure AD requirement. The pipeline signals are CRM entries without detail — the PO should confirm with Sales whether they are analogous requirements or just similar.

---

## Stakeholders  ·  *(Requirement 8)*

| Stakeholder | Role | Interest | Influence |
|---|---|---|---|
| Rafael Souza | Sales — demand reporter | Close the Construtora Ágil contract | High |
| Fernanda Ramos (IT Lead — Construtora Ágil) | Customer's technical authority | Azure AD integration and LGPD compliance confirmed before go-live | High |
| Construtora Ágil's Scrum Masters | Primary end users | Compliant access control for ceremonies with contractors | High |
| Ana Costa | Customer Success — owner of the post-sale relationship | Smooth onboarding and post-close health | Medium |
| Lucas Mendes | PO — owner of the rationalization | Product alignment and scope definition | High |
| Rodrigo Lima | CTO — technical assessment | Architectural integrity, LGPD compliance, Azure AD feasibility | High |
| CEO | Executive sponsor | Revenue from the new contract and compliance posture | Medium |

`Confidence:` 92 · `Source:` Submitter direct · `Status:` Resolved · `Disposition:` Answered · `Hint:` —

---

## Assumptions

Conditions assumed true at capture. If an assumption proves false, the demand must be re-triaged.

1. Construtora Ágil is willing and able to register the platform as an approved application in its Azure AD tenant — `to validate with:` Fernanda Ramos (IT Lead) at the start of Discovery
2. The customer's IT team can complete the Azure AD registration within the delivery window once the technical specs are provided — `to validate with:` Fernanda Ramos at project start
3. The existing authentication layer (OAuth2) can be extended for OIDC group-claim validation without replacement or rewrite — `to validate with:` CTO (technical spike)
4. LGPD compliance can be achieved with per-tenant routing (without a full platform migration) — `to validate with:` CTO (infrastructure review)
5. Jira integration is not required to close the deal — `to validate with:` Construtora Ágil (customer call)
6. Aliases in anonymous mode are sufficient for compliance — no need for additional database-level masking beyond what is displayed — `to validate with:` PO + CTO
7. The scope of access control is per room, not per organization account — `to validate with:` PO at rationalization

---

## Constraints  ·  *(Requirement 7)*

Conditions that limit the solution space, to be respected regardless of what is built.

| Constraint | Type | Detail |
|---|---|---|
| Deal deadline (informal) | Time | Sales made an informal 60-day commitment to the customer. Not confirmed until the PM's capacity assessment. |
| LGPD compliance | Legal / Regulatory | Identity data of Brazilian customers' participants must reside in `sa-east-1`. Non-negotiable for this customer. |
| Azure AD dependency (customer side) | External | Construtora Ágil controls its own Azure AD tenant. Integration cannot be completed without action from their IT. The timeline is partially outside our control. |
| No full enterprise SSO | Scope | Only OIDC group-claim validation for this release — not a full SSO/SAML implementation. |
| Backward compatibility | Technical | Existing open-link rooms must keep working unchanged. Access control is opt-in per room, not a platform-level breaking change. |
| No new external auth providers | Budget | No new identity provider (Okta, Auth0, etc.) may be contracted. Only an extension of the existing auth layer. |

`Confidence:` 85 · `Source:` Submitter direct (business constraints) + inferred (technical) · `Status:` Resolved · `Disposition:` Answered · `Hint:` The technical constraints (backward compatibility, no full SSO) were confirmed on the call by the customer's IT. The deadline constraint has lower confidence because it is an informal commitment.

---

## Preliminary Risks

Risks identified at capture — before the technical assessment. The full register belongs to the Readiness Package.

| Risk | Category | Initial Assessment |
|---|---|---|
| Azure AD registration delayed by the customer's IT | External / Timeline | Medium — dependency outside our control; mitigation: provide spec and checklist to the customer's IT early |
| LGPD posture requires more infrastructure work than expected | Compliance | Medium — CTO must confirm scope before committing |
| Sales' informal deadline commitment conflicts with real capacity | Operational | High — PM must run a capacity assessment before any external communication |
| Jira integration escalated to mandatory during delivery | Scope | Low — to be settled definitively in a customer call |
| Scope-creep pressure (audit logs, SSO, guest access) | Scope | Medium — explicit exclusions must be documented and enforced by the PO |

---

## High-Level Scope Boundary

**In:** Access modes (Open / Invite-only / Approval required), anonymous mode, Voter/Observer role assignment, participant removal, Azure AD OIDC group-claim mapping, per-customer `sa-east-1` data residency routing with an LGPD flag.

**Out:** Full SSO / SAML, audit logs, Jira integration, guest access without account registration, organization-level default settings, password-protected rooms.

**Deferred:** Bulk invite via CSV, automatic observer assignment by organizational role, compliance export for governance — feeds the backlog.

---

## Priority

**Level:** High

**Reason:** Pre-close blocker for the Construtora Ágil deal (R$ 42,000 ARR). Urgency validated by the deal dependency and Sales' informal commitment. Without resolving the integration unknowns, a deadline cannot be confirmed.

---

## Success Criteria

High-level indicators that define "done and valuable." Detailed measurable targets belong to the Readiness Package.

| Criterion | Type | Indicator | Projected value |
|---|---|---|---|
| Construtora Ágil contract closed | Business | Contract signed after the release | R$ 42,000 ARR |
| Zero unauthorized access incidents | Security / Compliance | None reported after go-live | 0 incidents |
| LGPD compliance confirmed by the customer | Legal | Construtora Ágil's IT confirms data residency before go-live | Sign-off from Fernanda Ramos |
| Azure AD mapping working end-to-end | Technical | Employees and contractors receive correct roles automatically | 100% in staging |
| At least 1 additional pipeline deal unblocked | Business | One of the 2 flagged deals advances to closing | Within 90 days of the release |
| Anonymous mode adopted in enterprise sessions | Product | Adoption in ≥ 30% of enterprise sessions | Within 60 days of the release |
