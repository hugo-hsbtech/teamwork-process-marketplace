# Golden example — PRD (escalated merge, `Feasible with caveats`)

> Calibration exemplar for the `prd-generation` skill. It shows a **complete, merged PRD**
> for an **escalated** demand: the product half is carried from a frozen Readiness Package
> (PO), the technical half from a signed Technical Assessment (CTO) whose verdict was
> `Feasible with caveats`, and the merge reconciles a scope item the CTO's constraint
> narrowed. It is self-contained — no external document is needed to judge the quality bar.
> The authoring scaffold (annotations, rubrics, the per-section confidence lines) is stripped,
> as the Finalizer would strip it; what remains is the clean PRD a PM would receive.
>
> The bar: each half keeps its author (Part A traces to the RP, Part B to the TA); the scope
> is reconciled, not just stapled; product and technical risks sit in one table; the effort is
> firm (from the TA); the dual sign-off is present; and nothing is invented — every fact
> traces to a frozen source.

---

# PRD — Tenant Role-Based Access Control (PokerPlan)

## Metadata

| Field | Value |
|---|---|
| **PRD ID** | PRD-2026-002 |
| **Version** | v1 |
| **Linked RP** | RP-2026-002 v2 |
| **Linked Technical Assessment** | TA-2026-002 v1 |
| **Linked Intake** | INT-2026-002 |
| **Escalated?** | Yes (TA merged) |
| **Demand nature** | Brownfield |
| **Authors** | Lucas Mendes (PO) + Priya Nair (CTO) |
| **Status** | In PM Review |
| **Output language** | en-US |
| **Delivered to PM on** | 2026-04-22 |

## Revision History

| Version | Date | Author | Status | Summary |
|---|---|---|---|---|
| v1 | 2026-04-22 | Lucas Mendes (PO) + Priya Nair (CTO) | In PM Review | Initial merge of RP-2026-002 v2 (frozen) + TA-2026-002 v1 (`Feasible with caveats`). Scope reconciled: SSO/SCIM provisioning deferred per CTO constraint. Delivered to PM. |

---

## Sign-off

> The merge closes with dual sign-off. The feasibility verdict is carried from the TA.

| Role | Name | Verdict | Date |
|---|---|---|---|
| **PO** (product) | Lucas Mendes | RP Frozen (`freezeReady`) — v2 | 2026-04-22 |
| **CTO** (technical) | Priya Nair | Feasible with caveats | 2026-04-21 |

---

## Combined Executive Summary

PokerPlan currently grants every member of a workspace the same capabilities: anyone can
create sessions, edit the backlog, and change workspace settings. Three enterprise customers
(Banco Meridional, Northwind Labs, and Vela Health — together R$ 192,000 ARR) have made
role separation a condition of their next renewal: their security teams will not certify a
tool where any participant can alter workspace configuration.

This PRD defines **tenant role-based access control (RBAC)**: three built-in roles (Owner,
Facilitator, Member) with a fixed permission matrix, enforced server-side on every mutating
operation, plus a workspace settings screen for Owners to assign roles. It returns
configuration control to designated administrators and unblocks the three renewals.

Technically the demand is **brownfield** and confined to the existing workspace/membership
service and the API authorization layer — no new infrastructure. The CTO assessed it
**feasible with caveats**: the caveat is that enforcement must be centralized in the existing
API gateway middleware (not scattered per-endpoint) to avoid permission drift, and one scoped
item — automated SSO/SCIM role provisioning — was **deferred** as a separate demand because it
requires an identity-provider integration outside this scope. The reconciled scope reflects
that deferral.

Expected outcome: retention of R$ 192,000 ARR across three renewals (next deadline ~75 days)
and removal of the enterprise security blocker. Firm effort: 21 days.

---

## Part A — Product Definition (from the Readiness Package · PO)

> Synthesis of the RP's key sections. Full source: RP-2026-002 v2. This is what the PM needs
> to plan.

### A.1 Objectives and Expected Outcome

1. Let workspace Owners assign one of three roles (Owner, Facilitator, Member) to every member.
2. Enforce a fixed permission matrix server-side so that only authorized roles can perform
   configuration, session-management, and backlog-editing actions.
3. Remove the enterprise security blocker conditioning the Banco Meridional, Northwind Labs,
   and Vela Health renewals (R$ 192,000 ARR).
4. Produce an auditable record of who changed workspace configuration and when.

### A.2 Scope (final)

**Included:**
- Three built-in roles with a fixed permission matrix (Owner / Facilitator / Member)
- Workspace settings screen: Owners view members and assign/change roles
- Server-side enforcement on every mutating operation (sessions, backlog, settings, members)
- Audit log of configuration and role-assignment changes (who, what, when)
- Last-Owner protection (a workspace cannot be left without an Owner)

**Excluded:**
- Custom / user-defined roles or granular per-permission editing
- Per-session (as opposed to per-workspace) roles
- Cross-workspace / organization-level administration

**Deferred (separate demand):**
- **Automated SSO/SCIM role provisioning** — deferred per the CTO's hard constraint (requires
  an identity-provider integration outside this scope); tracked as INT-2026-007.

### A.3 Personas / Jobs-to-be-done

| Persona | Job | Impact |
|---|---|---|
| Workspace Owner (enterprise admin) | Control who can change workspace configuration and assign roles, to satisfy the security team | Primary user: gains the settings screen and exclusive configuration rights |
| Facilitator (Scrum Master) | Run sessions and manage the backlog without being able to alter workspace-level settings | Keeps session/backlog rights; loses settings access |
| Member (participant) | Join sessions and vote without accidentally changing shared configuration | Loses configuration/backlog-edit rights; voting unaffected |

### A.4 User Journey (end-to-end)

| # | User action | Expected outcome | Touchpoint |
|---|---|---|---|
| 1 | Owner opens Workspace Settings → Members | Member list with current roles is shown | Settings screen |
| 2 | Owner changes a member's role to Facilitator | Role updated; the change is written to the audit log | Settings screen |
| 3 | The re-roled member attempts to edit workspace settings | Action blocked server-side with a clear "insufficient permissions" message | API + UI |
| 4 | Owner reviews the audit log | Chronological list of configuration/role changes (who, what, when) is shown | Settings → Audit |

### A.5 Business Rules and Flows

Full rules in RP-2026-002 v2 §6. Summary for the PM:

- Exactly three roles; the permission matrix is fixed (no custom roles in this scope).
- Only Owners can assign/change roles or edit workspace settings.
- A workspace must always have at least one Owner (last-Owner protection): the system rejects
  removing or demoting the final Owner.
- Permission decisions are evaluated **server-side** on every mutating request; the UI hides
  unauthorized actions but the server is the source of truth.
- Every configuration and role-assignment change is recorded in the audit log.

State flow: Member invited → role assigned (default Member) → role may be changed by an Owner →
every change audited.

### A.6 User Stories + Acceptance Criteria

| ID | Story | Acceptance criterion (Given/When/Then) |
|---|---|---|
| ST-001 | As an Owner, I want to assign roles to members so that only authorized people change configuration | Given I am an Owner, when I set a member's role to Facilitator, then their permissions update immediately and the change is recorded in the audit log |
| ST-002 | As a security admin, I want configuration actions blocked for non-Owners so that the workspace cannot be altered by participants | Given a Member or Facilitator, when they call any workspace-settings mutation, then the server rejects it with HTTP 403 and a clear message, regardless of the UI state |
| ST-003 | As an Owner, I want last-Owner protection so that a workspace is never left without an administrator | Given I am the only Owner, when I try to demote or remove myself, then the system blocks it and explains why |
| ST-004 | As an auditor, I want a log of configuration changes so that I can review who changed what | Given configuration or role changes occurred, when I open the audit log, then I see each change with actor, action, target, and timestamp |

Full acceptance criteria in RP-2026-002 v2 §7.

### A.7 Non-Functional Requirements (NFRs)

| Dimension | Requirement | Verification |
|---|---|---|
| Security | Authorization enforced server-side on 100% of mutating endpoints; no client-trust path | Penetration test enumerating mutations per role; payload/route inspection |
| Performance | Permission check adds ≤ 15 ms p95 to a request | Load test on annotated endpoints before release |
| Auditability | Every configuration/role change is recorded immutably with actor + timestamp | Audit-log integration test |
| Reliability | Role changes propagate to active sessions within 30 s | Forced role-change test against a live session in QA |
| Compatibility | Existing workspaces migrate with all current members defaulting to a safe role | Migration dry-run on a production snapshot |

### A.8 Edge Cases and Failure Modes

- **Existing member with no role at migration:** defaults to Member; the original workspace
  creator defaults to Owner.
- **Last Owner tries to leave:** blocked with explanation (last-Owner protection).
- **Role changed mid-session:** new permissions apply within 30 s; an in-flight unauthorized
  action is rejected on submit.
- **Concurrent role edits by two Owners:** last write wins; both writes appear in the audit log.
- **Member with a stale client showing a hidden action:** server rejects with 403 even if the
  UI did not hide the control.

Full edge cases in RP-2026-002 v2 §9.

---

## Part B — Technical Definition (from the Technical Assessment · CTO)

> Synthesis of TA-2026-002 v1. Full source: the linked TA.

### B.1 Feasibility Verdict

| Field | Value |
|---|---|
| **Verdict** | Feasible with caveats |
| **Caveats** | Enforcement must be centralized in the existing API-gateway authorization middleware (not implemented per-endpoint) to prevent permission drift. SSO/SCIM provisioning is out of scope and deferred (see B.6). |

### B.2 Nature and Technical Landscape

| Field | Value |
|---|---|
| **Nature** | Brownfield |
| **Knowledge base** | `tech-landscape-pokerplan.md` (existing; updated this cycle with the authorization-middleware section) |
| **Current state (brownfield)** | Workspace/membership service (Postgres `memberships` table, no role column); API requests pass through a gateway middleware that today only checks authentication, not authorization; WebSocket session layer reads membership at join. |
| **Foundation (greenfield)** | N/A — brownfield |

### B.3 Architectural Impact and Integrations

| Area / System | Impact | Note |
|---|---|---|
| Membership service | Add a `role` column + role-assignment API; backfill on migration | Default Member; creator → Owner |
| API gateway middleware | Extend the existing auth middleware to evaluate the permission matrix per route (centralized) | The caveat: one enforcement point, not per-endpoint checks |
| WebSocket session layer | Re-read role on role-change events to apply within 30 s | New `role_changed` event |
| Audit subsystem | Append-only audit records for config/role changes | Reuses the existing audit table |
| Integrations | None — no external identity provider in this scope | SSO/SCIM deferred (B.6) |

### B.4 NFR Feasibility

| NFR (from A.7) | Feasible? | Approach | Caveat |
|---|---|---|---|
| Server-side enforcement on 100% of mutations | Yes | Centralized middleware evaluates a route→permission map; deny-by-default | Requires the route map to be complete — covered by the test in A.7 |
| ≤ 15 ms p95 permission check | Yes | In-memory permission matrix + role cached on the session | Cache invalidation on role change adds the 30 s propagation |
| Immutable audit record | Yes | Append-only audit table already exists | — |
| 30 s role propagation to sessions | With caveats | `role_changed` WebSocket event + cache TTL | Worst case bounded by the cache TTL (set to 30 s) |
| Safe migration of existing workspaces | Yes | Backfill: creator → Owner, others → Member; dry-run first | Run on ended sessions only |

### B.5 Key Alternatives Considered

| Alternative | Why it was NOT chosen |
|---|---|
| Per-endpoint authorization checks | Permission drift — every new endpoint risks an unguarded mutation; rejected in favor of centralized middleware (the caveat) |
| Custom / fully-granular roles now | Out of scope and over-built for the three renewals; the fixed three-role matrix satisfies the requirement; granular roles can follow later |
| Client-side enforcement only | Fails the security NFR — the server must be the source of truth |

### B.6 Hard Constraints

| Constraint | Effect on scope |
|---|---|
| Enforcement centralized in the API-gateway middleware | Implementation must route all authorization through one point; no per-endpoint ad-hoc checks |
| No identity-provider integration in this scope | **Automated SSO/SCIM role provisioning is removed from scope** and deferred to INT-2026-007 — roles are assigned manually in the settings screen for now |
| Migration runs on ended sessions only | The backfill is scheduled outside active sessions to avoid mid-session role changes |

### B.7 ADRs (architectural level)

| # | Decision | CTO sign-off |
|---|---|---|
| ADR-014 | Centralize authorization in the gateway middleware with a deny-by-default route→permission map | ✓ |
| ADR-015 | Model roles as a fixed enum on `memberships.role` (no custom-role table in this scope) | ✓ |
| ADR-016 | Propagate role changes to sessions via a `role_changed` event + 30 s cache TTL | ✓ |

---

## Scope Reconciliation

> The CTO's constraint deferred one RP-scoped item. Everything else stands.

| Original item (RP) | Change after Technical Assessment | Reason |
|---|---|---|
| Automated SSO/SCIM role provisioning | **Removed → Deferred** (INT-2026-007) | CTO hard constraint: requires an identity-provider integration outside this scope (B.6) |
| Three built-in roles + fixed matrix | Unchanged | No technical conflict |
| Server-side enforcement | Unchanged (reinforced by ADR-014 — centralized) | Aligns with the security NFR |
| Audit log | Unchanged | Reuses existing audit subsystem |

Reconciled scope is reflected in A.2 (SSO/SCIM moved to Deferred).

---

## Consolidated Risk and Dependency View

| Risk | Origin | Type | Probability | Impact | Mitigation |
|---|---|---|---|---|---|
| Renewal deadline missed if effort overruns | RP | Timeline | Low | High | PM capacity check at planning; deferring the audit-log UI (not enforcement) is the scope-cut lever |
| An unguarded mutation slips past the middleware | TA | Technical/Security | Medium | High | Deny-by-default route map + penetration test enumerating mutations per role (A.7) |
| Migration mis-assigns roles on existing workspaces | TA | Technical | Low | High | Dry-run on a production snapshot before the live backfill |
| Enterprises expect SSO provisioning at launch | RP/TA | External | Medium | Medium | CS communicates the manual-assignment interim + the INT-2026-007 follow-up before renewal |
| Role-change propagation lag frustrates admins | TA | Technical | Low | Low | 30 s bound documented; `role_changed` event covers the common case quickly |
| Residual confusion from removed UI controls | RP | Product | Medium | Low | UI hides unauthorized actions; clear 403 messaging on stale clients |

**Known external dependencies:**
- CS (Ana Costa): communicate the manual-assignment interim + the SSO follow-up to the three
  enterprise accounts before their renewal conversations.
- PM: capacity assessment within the ~75-day renewal window.

---

## Effort and Cost (firm)

> Firm estimate from TA-2026-002 v1. Internal use only.

| Area | Firm estimate | Seniority |
|---|---|---|
| Backend — middleware authorization + role API | 8 days | Senior |
| Backend — migration + audit integration | 3 days | Mid-senior |
| Frontend — settings/members + audit screen | 5 days | Mid |
| QA — security (pentest) + load + migration dry-run | 5 days | QA / Security |
| **Total** | **21 days** | |

**Infra / Third parties / Recurring opex:** None. No new infrastructure or external services
in this scope (SSO/SCIM deferred). Negligible storage increase for audit records.

---

## Inherited Readiness and Open Dispositions

| Field | Value |
|---|---|
| **Assumptions still to validate** | (1) The three-role matrix satisfies all three enterprise security teams — CS to confirm with each before delivery; (2) the existing audit table meets the customers' immutability bar — validate with Vela Health's auditor |
| **Discovery unknowns** | — (none open; the SSO integration is deferred as a scoped follow-up, not an open unknown) |
| **Delegated requirements (with owner)** | SSO/SCIM role provisioning → INT-2026-007 (owner: PO, next cycle) |

> If an assumption proves false during execution (e.g. a customer requires a fourth role), the
> demand is re-triaged — downstream re-triage trigger.

---

## Success Criteria and Metrics (projected)

| Type | Metric | Target (projected) | Window | Confidence |
|---|---|---|---|---|
| **Primary** | Enterprise renewals closed (Banco Meridional, Northwind, Vela) | 3 of 3 renewed | By each renewal date (~75 days) | 80 |
| **Primary** | Workspaces with at least one non-Owner role assigned (enterprise cohort) | ≥ 90% | 30 days post-release | 70 |
| **Guardrail** | Unauthorized-mutation attempts that succeed | Zero | Continuous post-release | 95 |
| **Guardrail** | p95 request latency on annotated endpoints | No increase > 15 ms vs. baseline | 30 days post-release | 80 |

---

## Handoff to PM — Acceptance Gate

> The PM may reject and return this PRD with specific gaps; the rejection enters the Revision
> History and the PO (or CTO) addresses only the gaps and bumps the version.

| Delivery checklist | OK? |
|---|---|
| RP frozen (`freezeReady`) and referenced | ☑ — RP-2026-002 v2 |
| Technical Assessment signed off (or N/A justified) | ☑ — TA-2026-002 v1, `Feasible with caveats` |
| Scope reconciliation recorded | ☑ — SSO/SCIM deferred to INT-2026-007 |
| Risks and dependencies consolidated | ☑ |
| External dependencies explicit | ☑ — CS comms + PM capacity |
| Open dispositions visible | ☑ — two assumptions + one delegated item |

**Priority and business context:** High priority. Three enterprise renewals (R$ 192,000 ARR
combined) are conditioned on role separation; the nearest deadline is ~75 days out. The
deadline is the scope-cutting constraint, not a deferral one — if capacity is tight, cut the
audit-log **UI** (keep audit recording) before cutting enforcement or role assignment.

<!-- END OF DOCUMENT -->
