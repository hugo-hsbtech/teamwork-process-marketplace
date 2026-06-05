# Readiness Package — Session Timer Display (PokerPlan)

> Frozen RP (product half, PO). **Not escalated** to the CTO — `tech-assessment-ref:
> not_requested` (no architectural impact; UI + session-state only). This is the eval fixture
> for the no-escalation PRD path: the PRD forms from the RP alone and Part B is honestly N/A.

## Metadata

| Field | Value |
|---|---|
| **Package ID** | RP-2026-005 |
| **Version** | v1 |
| **Linked Intake** | INT-2026-005 |
| **Owner** | Lucas Mendes (PO) |
| **Escalated to CTO** | No — `tech-assessment-ref: not_requested` (no architectural impact) |
| **Status** | Frozen (`freezeReady`) |
| **Output language** | en-US |

## 1. Executive Summary

Facilitators have no visible sense of how long a planning ceremony or an individual item is
taking. They eyeball the clock and lose track, so sessions drift. Several teams have asked for a
simple elapsed-time display. The demand is confined to the existing session UI and the session
state already tracked — no new infrastructure.

## 3. Objectives and Expected Outcome

1. Show the facilitator a running elapsed timer for the overall session.
2. Show a per-item elapsed timer that resets when a new item is revealed.
3. Let the facilitator hide/show the timers without affecting participants.

## 4. Personas / Jobs-to-be-done

- **Facilitator** — keep the ceremony on pace by seeing elapsed time at a glance.
- **Participant** — (no change) unaffected; timers are a facilitator aid.

## 5. Scope

**Included:** overall session elapsed timer; per-item elapsed timer (resets on reveal);
facilitator toggle to show/hide. **Excluded:** countdown/auto-advance; per-item time limits;
historical time analytics; participant-visible timers.

## 6. Business Rules and Flows

- Timers are derived from the existing session `started_at` and item `revealed_at` timestamps —
  no new persisted state.
- The toggle is facilitator-local UI state; it is not broadcast to participants.
- On reconnection, timers re-derive from the persisted timestamps (no drift introduced).

## 7. User Stories + Acceptance Criteria

- **ST-001** — As a facilitator, I want an overall session timer. *Given a session is active, when
  I look at the facilitator panel, then I see elapsed time updating each second from session
  start.*
- **ST-002** — As a facilitator, I want a per-item timer. *Given I reveal a new item, when it
  becomes active, then the per-item timer resets to 0 and counts up.*
- **ST-003** — As a facilitator, I want to hide the timers. *Given timers are shown, when I toggle
  them off, then they hide for me only; participants are unaffected.*

## 8. Non-Functional Requirements

- **Performance:** timer updates must not cause layout thrash; ≤ 1 re-render per second.
- **Reliability:** timers re-derive correctly after a reconnection (no accumulated drift).
- **Usability:** timer is legible at a glance; toggle is discoverable.

## 9. Edge Cases and Failure Modes

- Reconnection mid-session → timers re-derive from persisted timestamps.
- Clock skew between client and server → timers anchor to server timestamps, not client clock.
- Session paused (facilitator absent) → overall timer keeps running; this is intended (it reflects
  wall-clock ceremony time).

## 12. Risks (product / business)

- Low business risk; nice-to-have with broad demand. Main risk: scope creep into countdown/limits
  (Product; Medium/Low) — explicitly excluded.

## 13. Preliminary Estimate

~4–5 days (UI + derived state; the Tech Lead firms it in breakdown).

## Metrics (projected)

- **Primary:** facilitators who enable timers at least once (active cohort) — ≥ 60%, 30 days
  post-release, confidence 65.
- **Guardrail:** session-panel render performance — no regression, continuous, confidence 80.

## Inherited Readiness and Open Dispositions

- **Assumptions still to validate:** the existing `revealed_at` timestamp is populated for all
  item types — confirm in breakdown.
- No Discovery unknowns; no delegated requirements.

## Technical premise note

Confined to UI and derived session state; technical premises (timestamps already persisted) were
assessed as reasonable at triage. No architectural escalation — `tech-assessment-ref:
not_requested`. The Tech Lead confirms premises in breakdown; if one proves false, the demand is
re-triaged.
