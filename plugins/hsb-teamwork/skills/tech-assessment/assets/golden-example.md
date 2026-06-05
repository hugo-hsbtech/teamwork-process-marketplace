# Golden example — Technical Assessment (calibration exemplar)

A self-contained, **already-filled** Technical Assessment used to calibrate quality
(the bar the `hsb-confidence-auditor` scores against, per
`../origination-brainstorm/references/grounding.md`). It is **brownfield** (modifies an
existing multi-tenant SaaS), with a security/multi-tenancy trigger — so the
`current-state` path is in force and `tech-foundation` is honestly N/A. It ends in a
`Feasible with caveats` verdict. Read it for *shape and depth*, not domain reuse.

> Demand: **"Turn-based voting queues with per-tenant isolation"** — the RP (RP-2026-014)
> asks for time-windowed voting queues, scoped per tenant, with a guardrail that vote
> propagation latency must not exceed 500 ms. Escalated to the CTO for multi-tenancy /
> data-isolation impact.

---

## Metadata

| Field | Value |
|---|---|
| **Assessment ID** | TA-2026-009 |
| **Version** | v1 |
| **Linked RP** | RP-2026-014 v2 |
| **Linked Intake** | INT-2026-031 |
| **Owner** | C. Nunes (CTO) |
| **Status** | Signed off |
| **Feasibility verdict** | Feasible with caveats |
| **Sign-off date** | 2026-05-28 |
| **Output language** | en-US |

---

## Feasibility Verdict

| Field | Value |
|---|---|
| **Verdict** | Feasible with caveats |
| **Rationale** | Per-tenant isolation is already guaranteed by the `tenant_id` column + RLS in Postgres; this demand reuses that contract. The only threat is the 500 ms guardrail under concurrent vote fan-out, feasible only with the event-based propagation path (not polling) described in NFR Feasibility. |
| **Terrain** | `tech-landscape-voting-platform.md` (updated 2026-04) — documented and complete terrain |
| **Caveats (if applicable)** | Remains feasible **if** (1) propagation migrates to the existing event channel and (2) the partial index `idx_votes_open_window` is created before rollout. Without both, the 500 ms guardrail is infeasible. |
| **Generates** | hard_constraint (event-based propagation + pre-rollout index) · adr (ADR-001, ADR-002) |

`Confidence:` 90 · `Origin:` cto_authored · `Source:` CTO analysis + event-channel benchmark · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Technical classification and Knowledge Base

| Field | Value |
|---|---|
| **Nature (confirmed by CTO)** | Brownfield (existing) |
| **Path to fill** | Current state (brownfield) |
| **Knowledge Base (KB)** | Exists → reference |
| **KB reference** | `tech-landscape-voting-platform.md` (updated 2026-04) |

`Confidence:` 92 · `Origin:` inherited · `Source:` Intake INT-2026-031 (nature) + tech-landscape · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## PO Questions Addressed

| # | PO question | CTO answer |
|---|---|---|
| 1 | Can we guarantee a tenant never sees another tenant's queue? | Yes — RLS by `tenant_id` already covers `votes` and `queues`; the new `vote_windows` table inherits the same policy. No new leakage path. |
| 2 | Is the 500 ms propagation guardrail achievable? | With a caveat: only via the event channel (item 1 of the caveats). Polling does not hit the target under concurrency. |

`Confidence:` 88 · `Origin:` cto_authored · `Source:` escalation from RP §8 + §6 · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## BROWNFIELD Path — Current state / Technical landscape

### Existing patterns and conventions to respect

| Aspect | How it is today | Implication for this demand |
|---|---|---|
| **Code structure / organization** | Modules by bounded context in `app/contexts/*`; voting in `contexts/voting` | Add `vote_windows` inside `contexts/voting`, not a new module |
| **Data / persistence patterns** | Postgres, `tenant_id` on every table + RLS; migrations via Ecto | New table inherits `tenant_id` + policy; reversible migration |
| **API / contract patterns** | Versioned REST (`/v3`) + internal events on RabbitMQ | Reuse the `voting.events` topic; no new external contract |
| **Authentication / authorization** | OIDC + role scopes; `tenant_id` in the token | No change — the `voting:write` scope already exists |

### Integration points touched

| Integration point | System/module | Coupling nature | Risk of changing |
|---|---|---|---|
| `voting.events` (RabbitMQ) | Notifications service | Event (asynchronous) | Medium — increases message volume |
| `votes` (table) | Reporting | Shared DB (read-replica) | Low |

### Technical debt and regression risk

| Area | Known debt / fragility | Regression risk | Current test coverage |
|---|---|---|---|
| `contexts/voting` | Vote counting recomputes everything on each vote (no incremental aggregation) | Medium | Good (unit + integration) |

`Confidence:` 85 · `Origin:` cto_authored · `Source:` tech-landscape-voting-platform.md · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## GREENFIELD Path — Technical foundation

N/A — brownfield (see Technical classification).

`Confidence:` 100 · `Origin:` cto_authored · `Source:` Technical classification · `Status:` resolved · `Disposition:` decided · `Hint:` path not applicable to this demand

---

## Affected Systems and Components

| System / Component | Nature of impact |
|---|---|
| `contexts/voting` | Modified (new `vote_windows` entity, incremental aggregation) |
| Notifications service | Consumed (new volume on the `voting.events` topic) |
| Reporting pipeline | Consumed only (no breaking schema change) |

`Confidence:` 86 · `Origin:` ai_drafted→cto_authored · `Source:` RP §5 scope · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Architectural Impact

| Area | Impact | Architectural note |
|---|---|---|
| **Data model** | New `vote_windows` table + partial index `idx_votes_open_window` | Follow the `tenant_id` + RLS pattern; partial index only over open windows |
| **Events / messaging** | +1 `vote.window.closed` event on `voting.events` | Reuse the topic; idempotency by `window_id` |
| **Multi-tenancy** | No new leakage path — inherits RLS | Test the policy on the new table explicitly |
| **Performance / Scalability** | Incremental aggregation removes the O(n) recompute per vote | Prerequisite for the 500 ms guardrail |
| **Observability** | Per-tenant propagation latency metric | Histogram `vote_propagation_ms` with `tenant` label |

`Confidence:` 84 · `Origin:` ai_drafted→cto_authored · `Source:` RP §6/§8 + tech-landscape · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Required Integrations

| System | Type | Protocol | Feasibility / Known risks |
|---|---|---|---|
| Notifications service | Internal / Event | AMQP (RabbitMQ) | Feasible — low risk; monitor queue depth under peak |

`Confidence:` 82 · `Origin:` ai_drafted→cto_authored · `Source:` RP §7 + tech-landscape · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Build vs. Buy

| Capability | Decision | Rationale | Effect on cost/timeline |
|---|---|---|---|
| Window scheduling | Reuse | The internal cron (`Oban`) already covers the case | Zero cost, no new provider |

`Confidence:` 80 · `Origin:` ai_drafted→cto_authored · `Source:` tech-landscape · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Alternatives Considered

| Alternative | Pros | Cons | Why it was NOT chosen |
|---|---|---|---|
| Propagation by polling (client fetches every 1s) | Simple; no new events | Latency ≥ 1s; linear DB load | Violates the 500 ms guardrail under concurrency |
| Full recompute per vote (status quo) | Already exists | O(n) per vote; does not scale on large windows | Misses the latency target; replaced by incremental aggregation |

`Confidence:` 83 · `Origin:` cto_authored · `Source:` CTO analysis · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## NFR Feasibility  ·  *(mapped to RP, Section 8)*

| NFR (from RP §8) | Feasible? | How it will be achieved / approach | Risk / caveat |
|---|---|---|---|
| Vote propagation < 500 ms (guardrail) | With caveats | Incremental aggregation + event propagation on `voting.events`; no polling | Infeasible by polling; depends on the partial index |
| Total per-tenant isolation | Yes | RLS by `tenant_id` inherited on the new table | Explicit policy test mandatory |
| 99.9% availability | Yes | No new SPOF; degrades to eventual counting if the broker drops | — |

`Confidence:` 87 · `Origin:` cto_authored · `Source:` RP §8 · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Testability and Observability

| Dimension | Approach |
|---|---|
| **Test strategy** | Unit (window rules), integration (RLS on the new table), e2e (concurrent fan-out measuring latency); regression on counting |
| **Test data / environment** | Multi-tenant seed (2 tenants); concurrency scenario (200 votes/s) covering the "window closes during a vote" edge case (RP §9) |
| **Telemetry / technical metrics** | `vote_propagation_ms` (histogram, `tenant` label); `voting.events` queue depth |
| **Logs / alerts** | Alert if p95 propagation > 400 ms; broker backlog alert |

`Confidence:` 84 · `Origin:` ai_drafted→cto_authored · `Source:` RP §9/§8 · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Hard Constraints

| Constraint | Type | Detail | Effect on scope |
|---|---|---|---|
| Propagation must be event-based, not polling | Technical | Required for the 500 ms guardrail | None on product scope; it is an implementation decision |
| Partial index created before rollout | Platform | `idx_votes_open_window` is a performance precondition | Adds 1 step to the release plan |

`Confidence:` 85 · `Origin:` cto_authored · `Source:` CTO analysis · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Technical Risks and Mitigations

| Risk | Category | Probability | Impact | Mitigation |
|---|---|---|---|---|
| Broker backlog under peak degrades latency | Infra | Medium | High | Consumer autoscaling + queue-depth alert |
| RLS policy not applied to the new table | Security | Low | High | Integration test that fails if the policy is missing |

`Confidence:` 86 · `Origin:` ai_drafted→cto_authored · `Source:` Architectural Impact · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Architecture Decisions (ADRs)

| # | Decision | Rationale | CTO sign-off |
|---|---|---|---|
| ADR-001 | Vote propagation by event (`voting.events`), not polling | The only feasible path for the 500 ms guardrail under concurrency | ✓ |
| ADR-002 | Incremental per-window count aggregation | Removes the O(n) recompute per vote; performance prerequisite | ✓ |
| ADR-003 | Reuse RLS by `tenant_id` on `vote_windows` (reused_from_KB) | Isolation pattern already validated in the tech-landscape | ✓ |

`Confidence:` 88 · `Origin:` reused_from_KB→cto_authored · `Source:` tech-landscape (ADR-003) + AI proposal · `Status:` resolved · `Disposition:` answered · `Hint:` —

---

## Effort and Cost Assessment (firm)

### Development Effort

| Area | Estimate | Seniority |
|---|---|---|
| Backend (table, RLS, aggregation, event) | 6 days | Senior |
| QA (concurrency + RLS) | 2 days | QA |
| **Total** | **8 days** | |

### Infrastructure Impact

No new provisioning — reuses existing Postgres and RabbitMQ.

### Third-Party Cost Impact

None.

### Recurring Operational Cost Impact

Marginal: +message volume on `voting.events` (estimated < 2% of current traffic).

### TCO Assessment

Creates a reusable foundation: incremental aggregation benefits all vote counting, not only this feature.

`Confidence:` 81 · `Origin:` cto_authored · `Source:` CTO decomposition · `Status:` resolved · `Disposition:` answered · `Hint:` refinable by the Tech Lead in the TB

---

## Discovery Path (if a technical unknown blocks completion)

—

`Confidence:` 100 · `Origin:` cto_authored · `Source:` — · `Status:` resolved · `Disposition:` decided · `Hint:` no unknown blocks closing

<!-- END OF DOCUMENT -->
