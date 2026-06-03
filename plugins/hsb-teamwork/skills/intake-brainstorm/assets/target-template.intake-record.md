<!--
TARGET TEMPLATE · Intake Record (default)
This file is the contract. Each fillable section carries an annotation:
  <!- - intake: id=...; blocks=...; min-confidence=...; kind=... - ->
and a self-sufficient rubric. The Template Analyst derives contract.lock.md from
these. To use a different document type, copy this file, re-annotate, and pass it
as TEMPLATE. See references/contract-and-template.md.
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.
-->

# Intake Record — [Demand name]
<!-- rev: 0 · updated: AAAA-MM-DD -->

> The formal intake artifact. It consolidates the captured demand, records the
> readiness it arrived with, and carries a **triage draft** (routing decision)
> that is always flagged for human sign-off. This document is self-contained.

## Metadata
<!-- intake: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Field | Value |
|---|---|
| **Record ID** | INT-AAAA-NNN |
| **Version** | v1 |
| **Originator (Submitter)** | [Name] ([Sales / CS / CEO / Marketing]) |
| **Triaged by (owner)** | — (AI draft; pending owner assignment) |
| **Date registered** | AAAA-MM-DD |
| **Date triaged** | — (pending human confirmation) |
| **Status** | New / In triage / Triaged |
| **Output language** | [e.g. en-US] |

## Revision history
<!-- intake: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Version | Date | Event | Summary |
|---|---|---|---|
| v1 | AAAA-MM-DD | Intake drafted | [brief] |

---

## Readiness received
<!-- intake: id=readiness; blocks=false; min-confidence=0; kind=derived; inputs=problem,reach,impact,originator,urgency -->

> A snapshot computed from the captured sections — not re-captured here.

| Field | Value |
|---|---|
| **Readiness score** | __ % |
| **Blocking requirements** | All resolved by honest disposition (gate) — Yes / No |
| **Open dispositions** | __ assumptions to validate · __ discovery · __ deferred |

---

## Consolidated demand

> One-screen read of the demand, each dimension carrying its inherited confidence.

### Problem (the pain, not the solution)
<!-- intake: id=problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: describe the existing pain with observable symptoms — what hurts, for
> whom, how it shows up today. If it names a solution ("build X"), it is NOT
> satisfied: reframe to the pain underneath.

[fill]

`Confidence:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### Originator & context
<!-- intake: id=originator; blocks=true; min-confidence=70; kind=capture -->
> Rubric: who raised it and in what situation (e.g. "COO, Q2 planning"), and the
> channel it came through.

[fill]

`Confidence:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### Who is impacted (reach)
<!-- intake: id=reach; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the personas / segments / teams who feel the pain, each with *how* they
> are affected.

[fill]

`Confidence:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### Business impact
<!-- intake: id=impact; blocks=true; min-confidence=70; kind=capture -->
> Rubric: value across the applicable dimensions (revenue, retention, operational,
> competitive, compliance) — quantified when possible. Estimates are fine if
> marked low-confidence with a hint on what would firm them up.

[fill]

`Confidence:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### Urgency — why now
<!-- intake: id=urgency; blocks=false; min-confidence=70; kind=capture -->
> Rubric: why now and the cost of waiting — a window, a deadline, a compounding
> cost.

[fill]

`Confidence:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

### Declared priority
<!-- intake: id=priority; blocks=false; min-confidence=0; kind=capture -->
> Rubric: the Submitter's priority call **and** the reason behind it (why this
> level, not just the label).

**Level:** Critical / High / Medium / Low — **Reason:** [why]

---

## Triage — routing decision
<!-- intake: id=triage; blocks=false; min-confidence=0; kind=derived; inputs=problem,reach,impact,urgency,assumptions -->

> ⚠️ **TRIAGE DRAFT — AI-generated from the capture, pending owner confirmation.**
> The verdicts and routing below are a *proposal* grounded in captured evidence,
> not a final call. A human owner must review, adjust, and sign off. Until then
> `Status` = *In triage* and this section's disposition is `low_confidence`.
> See the template's companion guide for how to draft this responsibly.

### Criteria assessed

| # | Criterion | Verdict | Rationale | Basis / source |
|---|---|---|---|---|
| 1 | A real problem (not an isolated symptom)? | Yes / No | | |
| 2 | Recurring / has volume? | Yes / No | | |
| 3 | Fits the product vision? | Yes / No | | |
| 4 | Technical & business impact? | High / Med / Low | | |
| 5 | Do urgency & impact justify *now*? | Yes / No | | |

### Decision

| Field | Value |
|---|---|
| **Decision** | Product Ready / Discovery / Backlog / Reject |
| **Rationale** | [defensible — traces to evidence] |
| **Reversible?** | Yes / No |
| **Originator notified** | Pending — (human action; date TBD) |

---

## Architectural escalation
<!-- intake: id=cto_escalation; blocks=false; min-confidence=0; kind=derived; inputs=impact,constraints,assumptions -->
> Rubric: whether the demand needs CTO/architectural review before scope can
> freeze (new infra, payments, multi-tenancy, security, AI/runtime, integrations
> with unknowns), with a one-line reason. A flagged draft signal pending owner
> confirmation — not a final call.

**Needed:** Yes / No — [brief rationale; draft signal pending owner confirmation]

---

## Assumptions
<!-- intake: id=assumptions; blocks=false; min-confidence=0; kind=capture -->

> Conditions assumed true at capture. Each carries a proposed verdict (draft) and
> who validates it. If one proves false, the demand is re-triaged.

| Assumption | Verdict (draft) | Validate with |
|---|---|---|
| [assumption] | Accepted / Rejected / To validate | [who] |

---

## Constraints
<!-- intake: id=constraints; blocks=false; min-confidence=70; kind=capture -->

> Conditions that limit the solution space, to respect regardless of what is built.

| Constraint | Type | Note |
|---|---|---|
| [constraint] | Time / Budget / Legal / Technical / Scope / External | [note] |

`Confidence:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Discovery brief
<!-- intake: id=discovery; blocks=false; min-confidence=0; kind=derived; inputs=triage; condition=triage.decision==Discovery -->

> Fill ONLY if the triage decision is **Discovery**; otherwise remove this section.

| # | Unknown | Who can answer | Method |
|---|---|---|---|
| 1 | [unknown] | [owner] | [spike / call / review] |

**Time-box:** [N days] (AAAA-MM-DD → AAAA-MM-DD)

---

## Handoff
<!-- intake: id=handoff; blocks=false; min-confidence=0; kind=derived; inputs=triage -->

- **If Product Ready:** proceed to rationalization (Readiness Package).
- **If Discovery:** open the Discovery brief above; re-triage when it closes.
- **If Backlog / Reject:** close the pass with a recorded rationale; notify originator.

<!-- END OF DOCUMENT -->
