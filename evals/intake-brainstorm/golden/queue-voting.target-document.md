# Intake Record — Queue Voting
<!-- rev: 1 · updated: 2026-06-03 -->

> The formal intake artifact. Golden reference output for the file-grounded eval
> case (source: a planning-poker queue-voting demand). Fictional, self-contained.

## Metadata
<!-- intake: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Field | Value |
|---|---|
| **Record ID** | INT-2026-001 |
| **Version** | v1 |
| **Originator (Submitter)** | Ana Costa (Customer Success) |
| **Triaged by (owner)** | — (AI draft; pending owner assignment) |
| **Date registered** | 2026-06-03 |
| **Date triaged** | — (pending human confirmation) |
| **Status** | In triage |
| **Output language** | en-US |

## Revision history
<!-- intake: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Version | Date | Event | Summary |
|---|---|---|---|
| v1 | 2026-06-03 | Intake drafted | Filled from the Submitter brief; triage drafted, pending PO sign-off. |

---

## Readiness received
<!-- intake: id=readiness; blocks=false; min-confidence=0; kind=derived; inputs=problem,reach,impact,originator,urgency -->

| Field | Value |
|---|---|
| **Readiness score** | 87 % |
| **Blocking requirements** | All resolved by honest disposition (gate) — Yes |
| **Open dispositions** | 5 assumptions to validate · 0 discovery · 0 deferred |

---

## Consolidated demand

### Problem (the pain, not the solution)
<!-- intake: id=problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: describe the existing pain with observable symptoms, without prescribing a solution.

During sprint-planning estimation, the facilitator cannot control which stories are shown or in what order, and votes appear in real time. Participants read ahead and copy early votes (anchoring bias), the ceremony loses cadence, and facilitators fall back to a manual workaround (sharing one story at a time in chat) that adds 15-20 minutes per session.

`Confidence:` 92 · `Source:` Submitter direct (Scrum Masters on the QBR call) · `Status:` resolved · `Disposition:` answered · `Hint:` —

### Originator & context
<!-- intake: id=originator; blocks=true; min-confidence=70; kind=capture -->
> Rubric: who raised it and in what situation, plus the channel.

Raised by Ana Costa (Customer Success) on the Banco Meridional quarterly review call, where the facilitators named it as a renewal blocker for the squads not yet on the platform.

`Confidence:` 95 · `Source:` Submitter direct · `Status:` resolved · `Disposition:` answered · `Hint:` —

### Who is impacted (reach)
<!-- intake: id=reach; blocks=true; min-confidence=70; kind=capture -->
> Rubric: personas / segments / teams + how each is affected.

Scrum Masters/facilitators (lose flow control), developers/voters (anchoring, longer ceremonies), 3 squads blocked from adopting, and CS (carries renewal risk on the largest enterprise account).

`Confidence:` 88 · `Source:` Submitter direct + account data · `Status:` resolved · `Disposition:` answered · `Hint:` exact users per squad not pulled; would raise to ~95.

### Business impact
<!-- intake: id=impact; blocks=true; min-confidence=70; kind=capture -->
> Rubric: value across applicable dimensions, quantified when possible.

Retention: R$ 84k ARR at renewal risk (4 active squads). Revenue: +R$ 28k expansion blocked (3 squads). Competitive: two rivals already ship sequential control + hidden votes.

`Confidence:` 80 · `Source:` Submitter direct + inferred from account data · `Status:` resolved · `Disposition:` answered · `Hint:` expansion ARR assumes equal ticket per squad; confirm with Finance.

### Urgency — why now
<!-- intake: id=urgency; blocks=false; min-confidence=70; kind=capture -->
> Rubric: why now and the cost of waiting.

Contract renewal in ~90 days; the feature must be live before the renewal conversation, which already has the gap on the agenda.

`Confidence:` 90 · `Source:` Submitter direct · `Status:` resolved · `Disposition:` answered · `Hint:` —

### Declared priority
<!-- intake: id=priority; blocks=false; min-confidence=0; kind=capture -->

**Level:** High — **Reason:** renewal window + competitive gap on the largest enterprise account.

---

## Triage — routing decision
<!-- intake: id=triage; blocks=false; min-confidence=0; kind=derived; inputs=problem,reach,impact,urgency,assumptions -->

> ⚠️ **TRIAGE DRAFT — AI-generated from the capture, pending owner confirmation.**
> The verdicts and routing below are a proposal grounded in captured evidence, not
> a final call. A human owner must review, adjust, and sign off. Until then
> `Status` = *In triage* and this section's disposition is `low_confidence`.

### Criteria assessed

| # | Criterion | Verdict | Rationale | Basis / source |
|---|---|---|---|---|
| 1 | A real problem (not an isolated symptom)? | Yes | Reported directly by facilitators; concrete 15-20 min workaround + anchoring. | Problem capture |
| 2 | Recurring / has volume? | Yes | Every ceremony; 4 active + 3 blocked squads; 3 other accounts informally. | Reach + evidence |
| 3 | Fits the product vision? | Yes | Estimation ceremony is core; parity with competitors. | PO read |
| 4 | Technical & business impact? | High (business) / Low (technical) | R$ 112k ARR combined; UI + session state on existing infra. | Impact capture |
| 5 | Do urgency & impact justify now? | Yes | Firm 90-day renewal window. | Urgency capture |

### Decision

| Field | Value |
|---|---|
| **Decision** | Product Ready |
| **Rationale** | Blocking sections answered directly at solid confidence; only open items are routine technical-feasibility assumptions, validated in rationalization. |
| **Reversible?** | Yes |
| **Originator notified** | Pending — (human action; date TBD) |

---

## Architectural escalation
<!-- intake: id=cto_escalation; blocks=false; min-confidence=0; kind=derived; inputs=impact,constraints,assumptions -->

**Needed:** No — extension of existing UI and session state on current infrastructure; no architectural change. Draft signal, pending owner confirmation.

---

## Assumptions
<!-- intake: id=assumptions; blocks=false; min-confidence=0; kind=capture -->

| Assumption | Verdict (draft) | Validate with |
|---|---|---|
| WebSocket layer supports new event types without a new broker | Accepted | Tech Lead (breakdown) |
| Session state extends without a full schema migration | Accepted | Tech Lead (breakdown) |
| Expansion ARR ticket ≈ active squads | To validate | Finance / CS |

---

## Constraints
<!-- intake: id=constraints; blocks=false; min-confidence=70; kind=capture -->

| Constraint | Type | Note |
|---|---|---|
| Renewal window (~90 days) | Time | Feature live before the renewal conversation. |
| No new external services | Budget | Build on existing infrastructure. |

`Confidence:` 88 · `Source:` Submitter direct · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Handoff
<!-- intake: id=handoff; blocks=false; min-confidence=0; kind=derived -->

- **If Product Ready:** proceed to rationalization (readiness-package).
- Originator (Ana Costa) to be notified of the triage result — human action pending.

<!-- END OF DOCUMENT -->
