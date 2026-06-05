# Readiness Package — Tenant Role-Based Access Control (PokerPlan)

> Frozen RP (product half, authored by the PO). Escalated to the CTO — a signed Technical
> Assessment (TA-2026-002) accompanies it. This is the eval fixture the prd-generation skill
> inherits Part A from.

## Metadata

| Field | Value |
|---|---|
| **Package ID** | RP-2026-002 |
| **Version** | v2 |
| **Linked Intake** | INT-2026-002 |
| **Owner** | Lucas Mendes (PO) |
| **Escalated to CTO** | Yes — Technical Assessment TA-2026-002 (signed) |
| **Status** | Frozen (`freezeReady`) |
| **Output language** | en-US |

## 1. Executive Summary

PokerPlan grants every workspace member the same capabilities — anyone can create sessions,
edit the backlog, and change workspace settings. Three enterprise customers (Banco Meridional,
Northwind Labs, Vela Health — R$ 192,000 ARR combined) condition their next renewal on role
separation: their security teams will not certify a tool where any participant can alter
configuration.

## 3. Objectives and Expected Outcome

1. Let workspace Owners assign one of three roles (Owner, Facilitator, Member) to every member.
2. Enforce a fixed permission matrix server-side so only authorized roles can perform
   configuration, session-management, and backlog-editing actions.
3. Remove the enterprise security blocker conditioning the three renewals (R$ 192,000 ARR).
4. Produce an auditable record of who changed workspace configuration and when.

## 4. Personas / Jobs-to-be-done

- **Workspace Owner (enterprise admin)** — control who can change workspace configuration, to
  satisfy the security team. Gains the settings screen and exclusive configuration rights.
- **Facilitator (Scrum Master)** — run sessions and manage the backlog without altering
  workspace settings. Keeps session/backlog rights; loses settings access.
- **Member (participant)** — join sessions and vote without accidentally changing shared
  configuration. Loses configuration/backlog-edit rights; voting unaffected.

## 5. Scope

**Included:** three built-in roles with a fixed permission matrix; a workspace settings screen
for Owners to assign roles; server-side enforcement on every mutating operation; an audit log of
configuration and role-assignment changes; last-Owner protection.

**Excluded:** custom/user-defined roles or granular per-permission editing; per-session roles;
cross-workspace/organization-level administration.

**Original (pre-TA) scope also included:** automated SSO/SCIM role provisioning — flagged as a
candidate item for the CTO to assess.

## 6. Business Rules and Flows

- Exactly three roles; the permission matrix is fixed.
- Only Owners can assign/change roles or edit workspace settings.
- A workspace must always have at least one Owner (last-Owner protection).
- Permission decisions are evaluated server-side on every mutating request; the UI hides
  unauthorized actions but the server is the source of truth.
- Every configuration and role-assignment change is recorded in the audit log.

State flow: Member invited → role assigned (default Member) → role may be changed by an Owner →
every change audited.

## 7. User Stories + Acceptance Criteria

- **ST-001** — As an Owner, I want to assign roles to members so only authorized people change
  configuration. *Given I am an Owner, when I set a member's role to Facilitator, then their
  permissions update immediately and the change is recorded in the audit log.*
- **ST-002** — As a security admin, I want configuration actions blocked for non-Owners. *Given a
  Member or Facilitator, when they call any workspace-settings mutation, then the server rejects
  it with HTTP 403 and a clear message, regardless of the UI state.*
- **ST-003** — As an Owner, I want last-Owner protection. *Given I am the only Owner, when I try
  to demote or remove myself, then the system blocks it and explains why.*
- **ST-004** — As an auditor, I want a log of configuration changes. *Given configuration or role
  changes occurred, when I open the audit log, then I see each change with actor, action, target,
  and timestamp.*

## 8. Non-Functional Requirements

- **Security:** authorization enforced server-side on 100% of mutating endpoints; no client-trust
  path. Verify with a penetration test enumerating mutations per role.
- **Performance:** permission check adds ≤ 15 ms p95 to a request. Verify with a load test.
- **Auditability:** every configuration/role change recorded immutably with actor + timestamp.
- **Reliability:** role changes propagate to active sessions within 30 s.
- **Compatibility:** existing workspaces migrate with all current members defaulting to a safe
  role.

## 9. Edge Cases and Failure Modes

- Existing member with no role at migration → defaults to Member; creator → Owner.
- Last Owner tries to leave → blocked with explanation.
- Role changed mid-session → applies within 30 s; in-flight unauthorized action rejected on submit.
- Concurrent role edits by two Owners → last write wins; both appear in the audit log.
- Stale client showing a hidden action → server rejects with 403.

## 12. Risks (product / business)

- Renewal deadline missed if effort overruns (Timeline; Low/High) — PM capacity check; cut the
  audit-log UI before enforcement.
- Enterprises expect SSO provisioning at launch (External; Medium/Medium) — CS communicates the
  manual interim.
- Residual confusion from removed UI controls (Product; Medium/Low) — UI hides unauthorized
  actions; clear 403 messaging.

## 13. Preliminary Estimate

~18–22 days (to be firmed by the CTO's Technical Assessment).

## Metrics (projected)

- **Primary:** enterprise renewals closed (Banco Meridional, Northwind, Vela) — 3 of 3, by each
  renewal date (~75 days), confidence 80.
- **Primary:** workspaces with ≥ 1 non-Owner role assigned (enterprise cohort) — ≥ 90%, 30 days
  post-release, confidence 70.
- **Guardrail:** unauthorized-mutation attempts that succeed — Zero, continuous, confidence 95.
- **Guardrail:** p95 request latency on annotated endpoints — no increase > 15 ms, 30 days,
  confidence 80.

## Inherited Readiness and Open Dispositions

- **Assumptions still to validate:** (1) the three-role matrix satisfies all three enterprise
  security teams — CS to confirm; (2) the audit table meets the customers' immutability bar —
  validate with Vela Health's auditor.
- **Delegated:** SSO/SCIM provisioning — escalated to the CTO for a feasibility call.
