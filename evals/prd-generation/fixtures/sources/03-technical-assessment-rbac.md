# Technical Assessment — Tenant Role-Based Access Control (PokerPlan)

> Signed TA (technical half, authored by the CTO). Responds to RP-2026-002; never edits it.
> This is the eval fixture the prd-generation skill inherits Part B from.

## Metadata

| Field | Value |
|---|---|
| **Assessment ID** | TA-2026-002 |
| **Version** | v1 |
| **Linked RP** | RP-2026-002 v2 |
| **Owner** | Priya Nair (CTO) |
| **Status** | Signed off |
| **Feasibility verdict** | Feasible with caveats |
| **Output language** | en-US |

## Feasibility Verdict

**Feasible with caveats.** Rationale: the demand is confined to the existing
workspace/membership service and the API authorization layer; the patterns exist. Two caveats:
(1) enforcement must be centralized in the existing API-gateway authorization middleware (not
implemented per-endpoint) to prevent permission drift; (2) automated SSO/SCIM role provisioning
is out of scope — it requires an identity-provider integration not present today and must be a
separate demand. Terrain: `tech-landscape-pokerplan.md` (updated this cycle).

## Technical Classification and Knowledge Base

Brownfield. KB exists (`tech-landscape-pokerplan.md`), updated this cycle with the
authorization-middleware section.

## Current State

Workspace/membership service backed by Postgres (`memberships` table, no role column today).
API requests pass through a gateway middleware that currently checks authentication only, not
authorization. The WebSocket session layer reads membership at join time.

## Affected Systems / Architectural Impact

- **Membership service** — add a `role` column + a role-assignment API; backfill on migration
  (default Member; creator → Owner).
- **API gateway middleware** — extend the existing auth middleware to evaluate the permission
  matrix per route, centralized (deny-by-default).
- **WebSocket session layer** — re-read role on a new `role_changed` event to apply within 30 s.
- **Audit subsystem** — append-only audit records for config/role changes (reuses the existing
  audit table).

## Integrations

None — no external identity provider in this scope. (SSO/SCIM deferred.)

## NFR Feasibility (responding to RP §8)

- Server-side enforcement on 100% of mutations → **Yes**, centralized middleware with a
  route→permission map, deny-by-default. Caveat: the route map must be complete (covered by the
  pentest).
- ≤ 15 ms p95 permission check → **Yes**, in-memory matrix + role cached on the session.
- Immutable audit record → **Yes**, the append-only audit table already exists.
- 30 s role propagation → **With caveats**, `role_changed` event + cache TTL bounded at 30 s.
- Safe migration → **Yes**, backfill creator→Owner / others→Member, dry-run first, ended sessions
  only.

## Key Alternatives Considered

- Per-endpoint authorization checks — rejected (permission drift; an unguarded endpoint is a hole).
- Custom/granular roles now — rejected (out of scope; the fixed matrix satisfies the requirement).
- Client-side enforcement only — rejected (fails the security NFR).

## Hard Constraints

- Enforcement centralized in the API-gateway middleware (no per-endpoint ad-hoc checks).
- No identity-provider integration in this scope → **SSO/SCIM role provisioning is removed from
  scope** and must be a separate demand.
- Migration runs on ended sessions only.

## Technical Risks

- An unguarded mutation slips past the middleware (Technical/Security; Medium/High) — deny-by-default
  route map + pentest.
- Migration mis-assigns roles on existing workspaces (Technical; Low/High) — dry-run on a
  production snapshot first.
- Role-change propagation lag (Technical; Low/Low) — 30 s TTL documented.

## ADRs

- **ADR-014** — Centralize authorization in the gateway middleware with a deny-by-default
  route→permission map. ✓
- **ADR-015** — Model roles as a fixed enum on `memberships.role` (no custom-role table). ✓
- **ADR-016** — Propagate role changes via a `role_changed` event + 30 s cache TTL. ✓

## Effort and Cost (firm)

- Backend — middleware authorization + role API: 8 days (Senior).
- Backend — migration + audit integration: 3 days (Mid-senior).
- Frontend — settings/members + audit screen: 5 days (Mid).
- QA — security (pentest) + load + migration dry-run: 5 days (QA/Security).
- **Total: 21 days.** No new infrastructure or external services (SSO/SCIM deferred); negligible
  audit-storage increase.
