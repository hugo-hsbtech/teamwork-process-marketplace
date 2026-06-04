---
template: target-template.intake-record.md
template_hash: 7d95916c27cef9200f18c5c754b84941efa1ec5267be61604833a3aa224194d9
template_version: v1
default_min_confidence: 70
generated: 2026-06-03
---

# Contract

Derived from `target-template.intake-record.md`. The template is the source of
truth; this snapshot binds the ledger's questions/answers to its sections. Fresh
session — no prior lock, no restart delta.

## Fillable & meta sections

| id | section | kind | blocks | min-confidence | rubric (one line) |
|----|---------|------|--------|----------------|-------------------|
| meta | Metadata | meta | false | 0 | record IDs, originator, dates, status, output language |
| revisions | Revision history | meta | false | 0 | versioned log of intake events |
| readiness | Readiness received | derived | false | 0 | computed readiness snapshot from captured sections |
| problem | Problem (the pain, not the solution) | capture | true | 80 | existing pain w/ observable symptoms — what hurts, for whom, today; no solution |
| originator | Originator & context | capture | true | 70 | who raised it, in what situation, via which channel |
| reach | Who is impacted (reach) | capture | true | 70 | personas/segments/teams who feel the pain + how each is affected |
| impact | Business impact | capture | true | 70 | value across applicable dimensions, quantified when possible; low-conf estimates ok w/ hint |
| urgency | Urgency — why now | capture | false | 70 | why now + cost of waiting (window, deadline, compounding cost) |
| priority | Declared priority | capture | false | 0 | Submitter's priority level **and** the reason behind it |
| triage | Triage — routing decision | derived | false | 0 | DRAFT routing proposal from evidence; always pending owner sign-off |
| cto_escalation | Architectural escalation | derived | false | 0 | whether CTO/architectural review needed before scope freeze, w/ one-line reason |
| assumptions | Assumptions | capture | false | 0 | conditions assumed true at capture, each w/ draft verdict + validator |
| constraints | Constraints | capture | false | 70 | conditions limiting the solution space, to respect regardless of build |
| discovery | Discovery brief | derived | false | 0 | unknowns + owners + method; only when triage decision is Discovery |
| handoff | Handoff | derived | false | 0 | next-step routing keyed off the triage decision |

## Derived sections — inputs & conditions

| id | inputs | condition |
|----|--------|-----------|
| readiness | problem, reach, impact, originator, urgency | — |
| triage | problem, reach, impact, urgency, assumptions | — |
| cto_escalation | impact, constraints, assumptions | — |
| discovery | triage | triage.decision==Discovery |
| handoff | triage | — |

## Gate

Blocking sections (`blocks=true`) — the gate cannot clear until each is resolved
to its `min-confidence` or honestly disposed:

- `problem` (min-confidence 80)
- `originator` (min-confidence 70)
- `reach` (min-confidence 70)
- `impact` (min-confidence 70)

## Notes

- Fresh session: no prior `contract.lock.md` existed; no restart delta.
- Default threshold `X` = 70; `problem` is raised to 80 (high-stakes).
- `capture` sections carrying the confidence line and graded for readiness:
  problem, originator, reach, impact, urgency, constraints. `priority` and
  `assumptions` are `min-confidence=0` capture sections (not graded).
- Derived sections (readiness, triage, cto_escalation, discovery, handoff) are
  recomputed from inputs, not graded by a confidence line.

<!-- END OF DOCUMENT -->
