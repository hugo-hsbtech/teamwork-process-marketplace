# PRD — Tenant Role-Based Access Control (PokerPlan)
<!-- rev: 1 · updated: 2026-04-22 -->

> The PRD is the **merge** of the Readiness Package (product, PO) with the Technical
> Assessment (technical, CTO). It is the only artifact that opens the downstream — delivered
> to the PM. Each half keeps clear authorship; the PRD stitches, reconciles, and exposes the
> two frozen halves without rewriting either. `PRD = RP (PO) + Technical Assessment (CTO)`.

## Metadata
<!-- origination: id=meta; blocks=false; min-confidence=0; kind=meta -->

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
<!-- origination: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Version | Date | Author | Status | Summary |
|---|---|---|---|---|
| v1 | 2026-04-22 | Lucas Mendes (PO) + Priya Nair (CTO) | In PM Review | Initial merge of RP-2026-002 v2 (frozen) + TA-2026-002 v1 (`Feasible with caveats`). Scope reconciled: SSO/SCIM provisioning deferred per CTO constraint. |

---

## Sign-off
<!-- origination: id=sign-off; blocks=true; min-confidence=85; kind=capture -->
> Rubric: the merge only closes with dual sign-off — PO (RP frozen) + CTO (signed verdict, or
> honest N/A when not escalated). The feasibility verdict is inherited from the TA, never
> re-decided here.

| Role | Name | Verdict | Date |
|---|---|---|---|
| **PO** (product) | Lucas Mendes | RP Frozen (`freezeReady`) — v2 | 2026-04-22 |
| **CTO** (technical) | Priya Nair | Feasible with caveats | 2026-04-21 |

`Confidence:` 92 · `Origin:` cto_authored · `Source:` RP-2026-002 freeze + TA-2026-002 sign-off · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Combined Executive Summary
<!-- origination: id=exec-summary; blocks=true; min-confidence=75; kind=derived; inputs=a-objectives,a-scope,b-feasibility,effort-cost,success-metrics -->
> Rubric: 2–4 paragraphs composing the problem, what will be built, the feasibility, and the
> business outcome — synthesized from the inherited sections, adding no new facts.

PokerPlan currently grants every member of a workspace the same capabilities: anyone can create
sessions, edit the backlog, and change workspace settings. Three enterprise customers (Banco
Meridional, Northwind Labs, Vela Health — together R$ 192,000 ARR) have made role separation a
condition of their next renewal: their security teams will not certify a tool where any
participant can alter workspace configuration.

This PRD defines tenant role-based access control (RBAC): three built-in roles (Owner,
Facilitator, Member) with a fixed permission matrix, enforced server-side on every mutating
operation, plus a workspace settings screen for Owners to assign roles. It returns
configuration control to designated administrators and unblocks the three renewals.

The demand is brownfield and confined to the existing workspace/membership service and the API
authorization layer — no new infrastructure. The CTO assessed it feasible with caveats:
enforcement must be centralized in the existing API-gateway middleware to avoid permission
drift, and automated SSO/SCIM role provisioning was deferred as a separate demand. The
reconciled scope reflects that deferral.

Expected outcome: retention of R$ 192,000 ARR across three renewals (next deadline ~75 days)
and removal of the enterprise security blocker. Firm effort: 21 days.

`Confidence:` 86 · `Origin:` po_authored · `Source:` RP-2026-002 §1 + TA-2026-002 §verdict · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Part A — Product Definition (from the Readiness Package · PO)

> Summary of the key RP sections — inherited, never rewritten. Full source: RP-2026-002 v2.

### A.1 Objectives and Expected Outcome
<!-- origination: id=a-objectives; blocks=true; min-confidence=75; kind=capture -->
> Rubric: the measurable outcomes the demand targets, carried from the RP.

1. Let workspace Owners assign one of three roles (Owner, Facilitator, Member) to every member.
2. Enforce a fixed permission matrix server-side so only authorized roles can perform
   configuration, session-management, and backlog-editing actions.
3. Remove the enterprise security blocker conditioning the Banco Meridional, Northwind Labs, and
   Vela Health renewals (R$ 192,000 ARR).
4. Produce an auditable record of who changed workspace configuration and when.

`Confidence:` 90 · `Origin:` po_authored · `Source:` RP-2026-002 §3 · `Status:` confirmed · `Disposition:` — · `Hint:` —

### A.2 Scope (final)
<!-- origination: id=a-scope; blocks=true; min-confidence=80; kind=capture -->
> Rubric: the final included / excluded / deferred boundaries — the reconciled (final) scope.

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
- Automated SSO/SCIM role provisioning — deferred per the CTO's hard constraint (requires an
  identity-provider integration outside this scope); tracked as INT-2026-007.

`Confidence:` 90 · `Origin:` po_authored · `Source:` RP-2026-002 §5 (reconciled — see Scope Reconciliation) · `Status:` confirmed · `Disposition:` — · `Hint:` —

### A.3 Personas / Jobs-to-be-done
<!-- origination: id=a-personas; blocks=true; min-confidence=70; kind=capture -->
> Rubric: who is impacted and the job each hires the product to do, inherited from the RP.

| Persona | Job | Impact |
|---|---|---|
| Workspace Owner (enterprise admin) | Control who can change workspace configuration, to satisfy the security team | Primary user: gains the settings screen + exclusive configuration rights |
| Facilitator (Scrum Master) | Run sessions and manage the backlog without altering workspace settings | Keeps session/backlog rights; loses settings access |
| Member (participant) | Join sessions and vote without accidentally changing shared configuration | Loses configuration/backlog-edit rights; voting unaffected |

`Confidence:` 88 · `Origin:` inherited · `Source:` RP-2026-002 §4 · `Status:` confirmed · `Disposition:` — · `Hint:` —

### A.4 User Journey (end-to-end)
<!-- origination: id=a-journey; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the end-to-end happy path the User Stories derive from, inherited from the RP.

| # | User action | Expected outcome | Touchpoint |
|---|---|---|---|
| 1 | Owner opens Workspace Settings → Members | Member list with current roles is shown | Settings screen |
| 2 | Owner changes a member's role to Facilitator | Role updated; the change is written to the audit log | Settings screen |
| 3 | The re-roled member attempts to edit workspace settings | Action blocked server-side with a clear "insufficient permissions" message | API + UI |
| 4 | Owner reviews the audit log | Chronological list of configuration/role changes (who, what, when) | Settings → Audit |

`Confidence:` 85 · `Origin:` inherited · `Source:` RP-2026-002 §6.5 · `Status:` confirmed · `Disposition:` — · `Hint:` —

### A.5 Business Rules and Flows
<!-- origination: id=a-business-rules; blocks=true; min-confidence=70; kind=capture -->
> Rubric: rules, validations, and state transitions — summary or pointed RP reference.

Full rules in RP-2026-002 v2 §6. Summary for the PM:

- Exactly three roles; the permission matrix is fixed (no custom roles in this scope).
- Only Owners can assign/change roles or edit workspace settings.
- A workspace must always have at least one Owner (last-Owner protection): the system rejects
  removing or demoting the final Owner.
- Permission decisions are evaluated server-side on every mutating request; the UI hides
  unauthorized actions but the server is the source of truth.
- Every configuration and role-assignment change is recorded in the audit log.

`Confidence:` 85 · `Origin:` inherited · `Source:` RP-2026-002 §6 · `Status:` confirmed · `Disposition:` — · `Hint:` —

### A.6 User Stories + Acceptance Criteria
<!-- origination: id=a-user-stories; blocks=true; min-confidence=80; kind=capture -->
> Rubric: stories + their primary Given/When/Then criteria (what QA/UAT validates).

| ID | Story | Acceptance criterion (Given/When/Then) |
|---|---|---|
| ST-001 | As an Owner, I want to assign roles to members so only authorized people change configuration | Given I am an Owner, when I set a member's role to Facilitator, then their permissions update immediately and the change is recorded in the audit log |
| ST-002 | As a security admin, I want configuration actions blocked for non-Owners | Given a Member or Facilitator, when they call any workspace-settings mutation, then the server rejects it with HTTP 403 and a clear message, regardless of the UI state |
| ST-003 | As an Owner, I want last-Owner protection so a workspace is never left without an administrator | Given I am the only Owner, when I try to demote or remove myself, then the system blocks it and explains why |
| ST-004 | As an auditor, I want a log of configuration changes | Given configuration or role changes occurred, when I open the audit log, then I see each change with actor, action, target, and timestamp |

Full acceptance criteria in RP-2026-002 v2 §7.

`Confidence:` 88 · `Origin:` po_authored · `Source:` RP-2026-002 §7 · `Status:` confirmed · `Disposition:` — · `Hint:` —

### A.7 Non-Functional Requirements (NFRs)
<!-- origination: id=a-nfrs; blocks=true; min-confidence=75; kind=capture -->
> Rubric: the product NFRs (RP §8), each with verification; each pairs 1:1 with a B.4 row.

| Dimension | Requirement | Verification |
|---|---|---|
| Security | Authorization enforced server-side on 100% of mutating endpoints; no client-trust path | Penetration test enumerating mutations per role |
| Performance | Permission check adds ≤ 15 ms p95 to a request | Load test on annotated endpoints before release |
| Auditability | Every configuration/role change recorded immutably with actor + timestamp | Audit-log integration test |
| Reliability | Role changes propagate to active sessions within 30 s | Forced role-change test against a live session in QA |
| Compatibility | Existing workspaces migrate with all current members defaulting to a safe role | Migration dry-run on a production snapshot |

`Confidence:` 88 · `Origin:` po_authored · `Source:` RP-2026-002 §8 · `Status:` confirmed · `Disposition:` — · `Hint:` —

### A.8 Edge Cases and Failure Modes
<!-- origination: id=a-edge-cases; blocks=true; min-confidence=70; kind=capture -->
> Rubric: edge cases and failure modes (RP §9), each with expected behavior.

- Existing member with no role at migration: defaults to Member; the original workspace creator
  defaults to Owner.
- Last Owner tries to leave: blocked with explanation (last-Owner protection).
- Role changed mid-session: new permissions apply within 30 s; an in-flight unauthorized action
  is rejected on submit.
- Concurrent role edits by two Owners: last write wins; both writes appear in the audit log.
- Member with a stale client showing a hidden action: server rejects with 403 even if the UI did
  not hide the control.

`Confidence:` 85 · `Origin:` inherited · `Source:` RP-2026-002 §9 · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Part B — Technical Definition (from the Technical Assessment · CTO)

> Summary of TA-2026-002 v1 — inherited, never rewritten. Full source: the linked TA.

### B.1 Feasibility Verdict
<!-- origination: id=b-feasibility; blocks=true; min-confidence=80; kind=capture -->
> Rubric: the CTO's verdict, inherited from the TA — never re-decided in the PRD.

| Field | Value |
|---|---|
| **Verdict** | Feasible with caveats |
| **Caveats** | Enforcement must be centralized in the existing API-gateway authorization middleware (not per-endpoint) to prevent permission drift. SSO/SCIM provisioning is out of scope and deferred (see B.6). |

`Confidence:` 90 · `Origin:` cto_authored · `Source:` TA-2026-002 §feasibility-verdict · `Status:` confirmed · `Disposition:` — · `Hint:` —

### B.2 Nature and Technical Landscape
<!-- origination: id=b-nature-landscape; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the terrain engineering decides on, inherited from the TA.

| Field | Value |
|---|---|
| **Nature** | Brownfield |
| **Knowledge base** | `tech-landscape-pokerplan.md` (existing; updated this cycle with the authorization-middleware section) |
| **Current state (brownfield)** | Workspace/membership service (Postgres `memberships`, no role column); API gateway middleware checks authentication only, not authorization; WebSocket session layer reads membership at join. |
| **Foundation (greenfield)** | N/A — brownfield |

`Confidence:` 85 · `Origin:` inherited · `Source:` TA-2026-002 §current-state · `Status:` confirmed · `Disposition:` — · `Hint:` —

### B.3 Architectural Impact and Integrations
<!-- origination: id=b-arch-impact; blocks=true; min-confidence=75; kind=capture -->
> Rubric: systems/areas touched + required integrations under the feasibility lens.

| Area / System | Impact | Note |
|---|---|---|
| Membership service | Add a `role` column + role-assignment API; backfill on migration | Default Member; creator → Owner |
| API gateway middleware | Extend the existing auth middleware to evaluate the permission matrix per route (centralized) | The caveat: one enforcement point |
| WebSocket session layer | Re-read role on role-change events to apply within 30 s | New `role_changed` event |
| Audit subsystem | Append-only audit records for config/role changes | Reuses the existing audit table |
| Integrations | None — no external identity provider in this scope | SSO/SCIM deferred (B.6) |

`Confidence:` 85 · `Origin:` inherited · `Source:` TA-2026-002 §architectural-impact · `Status:` confirmed · `Disposition:` — · `Hint:` —

### B.4 NFR Feasibility
<!-- origination: id=b-nfr-feasibility; blocks=true; min-confidence=75; kind=capture -->
> Rubric: the CTO's response to each RP NFR (A.7) — feasible? and how — inherited from the TA.

| NFR (from A.7) | Feasible? | Approach | Caveat |
|---|---|---|---|
| Server-side enforcement on 100% of mutations | Yes | Centralized middleware evaluates a route→permission map; deny-by-default | Route map must be complete — covered by the pentest |
| ≤ 15 ms p95 permission check | Yes | In-memory permission matrix + role cached on the session | Cache invalidation on role change adds the 30 s propagation |
| Immutable audit record | Yes | Append-only audit table already exists | — |
| 30 s role propagation to sessions | With caveats | `role_changed` event + cache TTL | Worst case bounded by the 30 s TTL |
| Safe migration of existing workspaces | Yes | Backfill: creator → Owner, others → Member; dry-run first | Run on ended sessions only |

`Confidence:` 85 · `Origin:` inherited · `Source:` TA-2026-002 §nfr-feasibility · `Status:` confirmed · `Disposition:` — · `Hint:` —

### B.5 Key Alternatives Considered
<!-- origination: id=b-alternatives; blocks=false; min-confidence=0; kind=capture -->
> Rubric: discarded options + why not — so the downstream does not re-litigate.

| Alternative | Why it was NOT chosen |
|---|---|
| Per-endpoint authorization checks | Permission drift — every new endpoint risks an unguarded mutation; rejected for centralized middleware |
| Custom / fully-granular roles now | Out of scope and over-built for the three renewals; the fixed matrix satisfies the requirement |
| Client-side enforcement only | Fails the security NFR — the server must be the source of truth |

`Confidence:` 80 · `Origin:` inherited · `Source:` TA-2026-002 §alternatives · `Status:` confirmed · `Disposition:` — · `Hint:` —

### B.6 Hard Constraints
<!-- origination: id=b-hard-constraints; blocks=true; min-confidence=75; kind=capture -->
> Rubric: non-negotiable conditions + their effect on scope — these feed Scope Reconciliation.

| Constraint | Effect on scope |
|---|---|
| Enforcement centralized in the API-gateway middleware | All authorization routes through one point; no per-endpoint ad-hoc checks |
| No identity-provider integration in this scope | Automated SSO/SCIM role provisioning is removed from scope and deferred to INT-2026-007 |
| Migration runs on ended sessions only | The backfill is scheduled outside active sessions |

`Confidence:` 88 · `Origin:` inherited · `Source:` TA-2026-002 §hard-constraints · `Status:` confirmed · `Disposition:` — · `Hint:` —

### B.7 ADRs (architectural level)
<!-- origination: id=b-adrs; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the CTO-signed architectural ADRs, inherited from the TA. Implementation ADRs stay in the Tech Backlog.

| # | Decision | CTO sign-off |
|---|---|---|
| ADR-014 | Centralize authorization in the gateway middleware with a deny-by-default route→permission map | ✓ |
| ADR-015 | Model roles as a fixed enum on `memberships.role` (no custom-role table in this scope) | ✓ |
| ADR-016 | Propagate role changes to sessions via a `role_changed` event + 30 s cache TTL | ✓ |

`Confidence:` 88 · `Origin:` inherited · `Source:` TA-2026-002 §adrs · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Scope Reconciliation
<!-- origination: id=scope-reconciliation; blocks=true; min-confidence=80; kind=derived; inputs=a-scope,b-feasibility,b-hard-constraints -->
> Rubric: reconcile the RP scope against the TA's verdict, caveats, and hard constraints; ensure A.2 reflects the reconciled result.

| Original item (RP) | Change after Technical Assessment | Reason |
|---|---|---|
| Automated SSO/SCIM role provisioning | Removed → Deferred (INT-2026-007) | CTO hard constraint: requires an identity-provider integration outside this scope (B.6) |
| Three built-in roles + fixed matrix | Unchanged | No technical conflict |
| Server-side enforcement | Unchanged (reinforced by ADR-014 — centralized) | Aligns with the security NFR |
| Audit log | Unchanged | Reuses existing audit subsystem |

Reconciled scope is reflected in A.2 (SSO/SCIM moved to Deferred).

`Confidence:` 88 · `Origin:` po_authored · `Source:` RP-2026-002 §5 vs TA-2026-002 §hard-constraints · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Consolidated Risk and Dependency View
<!-- origination: id=consolidated-risk; blocks=true; min-confidence=75; kind=derived; inputs=a-edge-cases,b-arch-impact,b-hard-constraints -->
> Rubric: merge the RP's product/business risks with the TA's technical risks into one tagged table; list external dependencies.

| Risk | Origin | Type | Probability | Impact | Mitigation |
|---|---|---|---|---|---|
| Renewal deadline missed if effort overruns | RP | Timeline | Low | High | PM capacity check at planning; cut the audit-log UI (not enforcement) as the scope lever |
| An unguarded mutation slips past the middleware | TA | Technical/Security | Medium | High | Deny-by-default route map + pentest enumerating mutations per role |
| Migration mis-assigns roles on existing workspaces | TA | Technical | Low | High | Dry-run on a production snapshot before the live backfill |
| Enterprises expect SSO provisioning at launch | RP/TA | External | Medium | Medium | CS communicates the manual-assignment interim + the INT-2026-007 follow-up before renewal |
| Role-change propagation lag frustrates admins | TA | Technical | Low | Low | 30 s bound documented; `role_changed` event covers the common case quickly |
| Residual confusion from removed UI controls | RP | Product | Medium | Low | UI hides unauthorized actions; clear 403 messaging on stale clients |

**Known external dependencies:**
- CS (Ana Costa): communicate the manual-assignment interim + the SSO follow-up to the three
  enterprise accounts before their renewal conversations.
- PM: capacity assessment within the ~75-day renewal window.

`Confidence:` 85 · `Origin:` po_authored · `Source:` RP-2026-002 §12 + TA-2026-002 §tech-risks · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Effort and Cost (firm)
<!-- origination: id=effort-cost; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the firm estimate from the TA (replaces the RP preliminary). Internal use only.

| Area | Firm estimate | Seniority |
|---|---|---|
| Backend — middleware authorization + role API | 8 days | Senior |
| Backend — migration + audit integration | 3 days | Mid-senior |
| Frontend — settings/members + audit screen | 5 days | Mid |
| QA — security (pentest) + load + migration dry-run | 5 days | QA / Security |
| **Total** | **21 days** | |

**Infra / Third parties / Recurring opex:** None. No new infrastructure or external services in
this scope (SSO/SCIM deferred). Negligible storage increase for audit records.

`Confidence:` 88 · `Origin:` inherited · `Source:` TA-2026-002 §effort-cost · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Inherited Readiness and Open Dispositions
<!-- origination: id=inherited-readiness; blocks=true; min-confidence=70; kind=derived; inputs=a-scope,b-feasibility -->
> Rubric: assumptions still to validate, Discovery unknowns (resolved/open), and delegated answers (with owner), carried from the RP/TA dispositions.

| Field | Value |
|---|---|
| **Assumptions still to validate** | (1) The three-role matrix satisfies all three enterprise security teams — CS to confirm with each before delivery; (2) the existing audit table meets the customers' immutability bar — validate with Vela Health's auditor |
| **Discovery unknowns** | — (none open; the SSO integration is deferred as a scoped follow-up, not an open unknown) |
| **Delegated requirements (with owner)** | SSO/SCIM role provisioning → INT-2026-007 (owner: PO, next cycle) |

`Confidence:` 82 · `Origin:` po_authored · `Source:` RP-2026-002 §inherited-readiness · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Success Criteria and Metrics (projected)
<!-- origination: id=success-metrics; blocks=true; min-confidence=75; kind=capture -->
> Rubric: primary metrics + guardrails (a guardrail must not worsen), inherited from the RP.

| Type | Metric | Target (projected) | Window | Confidence |
|---|---|---|---|---|
| **Primary** | Enterprise renewals closed (Banco Meridional, Northwind, Vela) | 3 of 3 renewed | By each renewal date (~75 days) | 80 |
| **Primary** | Workspaces with at least one non-Owner role assigned (enterprise cohort) | ≥ 90% | 30 days post-release | 70 |
| **Guardrail** | Unauthorized-mutation attempts that succeed | Zero | Continuous post-release | 95 |
| **Guardrail** | p95 request latency on annotated endpoints | No increase > 15 ms vs. baseline | 30 days post-release | 80 |

`Confidence:` 80 · `Origin:` inherited · `Source:` RP-2026-002 §metrics · `Status:` confirmed · `Disposition:` — · `Hint:` —

---

## Handoff to PM — Acceptance Gate
<!-- origination: id=handoff-gate; blocks=true; min-confidence=80; kind=derived; inputs=sign-off,scope-reconciliation,consolidated-risk,inherited-readiness -->
> Rubric: the delivery checklist the PM accepts against; every box checkable from the merged document; close with priority and business context.

| Delivery checklist | OK? |
|---|---|
| RP frozen (`freezeReady`) and referenced | ☑ — RP-2026-002 v2 |
| Technical Assessment signed off (or N/A justified) | ☑ — TA-2026-002 v1, `Feasible with caveats` |
| Scope reconciliation recorded | ☑ — SSO/SCIM deferred to INT-2026-007 |
| Risks and dependencies consolidated | ☑ |
| External dependencies explicit | ☑ — CS comms + PM capacity |
| Open dispositions visible | ☑ — two assumptions + one delegated item |

**Priority and business context:** High priority. Three enterprise renewals (R$ 192,000 ARR
combined) are conditioned on role separation; the nearest deadline is ~75 days out. The deadline
is the scope-cutting constraint, not a deferral one — if capacity is tight, cut the audit-log UI
(keep audit recording) before cutting enforcement or role assignment.

`Confidence:` 88 · `Origin:` po_authored · `Source:` derived from sign-off + scope-reconciliation + consolidated-risk + inherited-readiness · `Status:` confirmed · `Disposition:` — · `Hint:` —

<!-- END OF DOCUMENT -->
