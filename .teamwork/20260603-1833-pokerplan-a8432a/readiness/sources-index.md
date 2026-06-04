# Sources Index — PokerPlan Readiness Package
<!-- rev: 1 · updated: 2026-06-03 -->

> Written by the Source Indexer. This file is the authoritative inventory of
> every source brought under `PHASE_DIR/sources/` for this RP phase.
> Inheritors (File Extraction, Strategist, Doc Updater) read this index to know
> what exists and where each piece of information lives.
>
> **Inheritance note:** This RP inherits from intake record INT-2026-001
> (PokerPlan). The intake was triaged **Discovery** (not Product Ready). The PO
> has chosen to proceed to the Readiness Package anyway. Open dispositions —
> 8 assumptions, 1 commercial/market discovery flag, urgency uncaptured — are
> preserved faithfully below. They must NOT be laundered or resolved silently;
> each requires explicit handling during RP elaboration.

---

## Source Table

| ID | File (under `sources/`) | Type | Likely contents | Language | Role | Status |
|---|---|---|---|---|---|---|
| SRC-001 | `intake-target-document.md` | Markdown — Intake Record | PRIMARY: canonical filled intake artefact, INT-2026-001 Rev 2. Contains consolidated demand (problem, originator, reach, impact, urgency, priority), triage decision (Discovery draft), readiness score (63 %), assumptions (a)–(h), constraints/business rules RN-001–RN-010, discovery brief (5 items), architectural escalation, and handoff notes. | pt-BR | **Primary** | Indexed |
| SRC-002 | `pokerplan-spec.md` | Markdown — Raw Spec | SECONDARY: Submitter's original specification. Contains product vision, participant roles (Host, Participant, Observer), estimation scales (Fibonacci, T-Shirt), traditional flow (8 stages), business rules RN-001–RN-010, conceptual data model (Room, Participant, Task, Round, Vote), digital flow, statistics post-reveal, and MVP feature breakdown (V1 / V1.1 / V2). | pt-BR | Secondary | Indexed |
| SRC-003 | `intake-humanized.md` | Markdown — Humanized Variant | Humanized/plain-language re-render of the intake record (same structure and data as SRC-001 but with softened header annotations). Useful as readable reference; SRC-001 is canonical. | pt-BR | Secondary | Indexed |
| SRC-004 | `readiness-report.md` | Markdown — Readiness Report | Reference dashboard computed from the intake: readiness score headline (63 %, gate CLEARED), section map with per-field confidence and thresholds, narrative on how each blocking field was answered, deliberately parked items (arithmetic inconsistency in efficiency model, urgency absent, TAM unsized, SaaS monetisation unvalidated), and discovery-as-readiness rationale. | pt-BR | Reference | Indexed |
| SRC-005 | `glossary.md` | Markdown — Canonical Glossary | Normative terminology for PokerPlan: 30 + canonical terms with definitions, prohibited synonyms, and usage notes (Planning Poker, Host, Participante, Rodada, Revelação, Auto Reveal, Consenso, Escala, Fibonacci, T-Shirt, Rastreabilidade, Sala, Tarefa, MVP, SaaS, Squad, Sprint, Scrum, aderência problema-mercado, etc.). | pt-BR | Reference | Indexed |
| SRC-006 | `qa-log.md` | Markdown — Q&A Ledger | Full interview ledger (Q001–Q011). Records every question asked, Submitter answers, per-question confidence, disposition and source. Audit trail showing how each section was answered, which entries were superseded (Q002 superseded by Q008/Q010; Q003 superseded in substance by Q009), and where open items remain. | pt-BR | Reference | Indexed |

---

## Section Map — Primary Source (SRC-001)

Locates each RP-relevant topic within `intake-target-document.md`.

| RP Topic | Section / id | Key location in SRC-001 | Confidence | Disposition |
|---|---|---|---|---|
| **Problem (pain, not solution)** | `## Consolidated demand > ### Problem` · `id=problem` | Lines ~72–91. Symptoms: no secrecy, no history, tool fragmentation, repeated undocumented discussions. Workaround: video calls + chats + spreadsheets + disconnected PP tools. | 84 | answered |
| **Originator & context** | `### Originator & context` · `id=originator` | Lines ~94–110. Collective bottom-up origin: product, engineering and management teams. Formalised as commercial SaaS product bet. No named individual sponsor — consistent with bottom-up origin, not a gap. | 85 | answered |
| **Personas / Reach** | `### Who is impacted (reach)` · `id=reach` | Lines ~113–141. Internal personas table: Developers, POs, Scrum Masters, Tech Leads, Engineering/Product Managers. Commercial segments table: tech companies, software consultancies, software factories, product-led companies, Scrum/agile orgs. TAM not sized — Discovery item. | 78 | answered |
| **Business impact** | `### Business impact` · `id=impact` | Lines ~144–198. Layer A: efficiency model (8 people × ~4 sessions/month = 32 h-h/month per squad; 15–20 min waste reduction — arithmetic inconsistency flagged). Layer B: SaaS commercial opportunity explicitly NOT validated. | 70 | assumption (Layer A) + discovery flag (Layer B) |
| **Urgency / why now** | `### Urgency — why now` · `id=urgency` | Lines ~201–207. No window, deadline, competitor, or cost-of-waiting declared. | 0 | open (non-blocking) |
| **Declared priority** | `### Declared priority` · `id=priority` | Lines ~209–220. No relative portfolio priority declared. Implicit scope priority: V1 > V1.1 > V2. | 40 | inferred |
| **Business rules RN-001–RN-010** | `## Constraints` · `id=constraints` | Lines ~285–303. Full list: RN-001 vote secrecy, RN-002 vote changeable while round open, RN-003 host-only reveal, RN-005 host-only close, RN-006 multi-round per task, RN-007 full history, RN-008 no retroactive vote, RN-009 host-only cancel, RN-010 final estimate separate from individual votes. Also: no-auth MVP V1, preserve physical PP rules. RN-004 (optional auto-reveal) present in SRC-002 but not listed in constraints table — carry forward to RP. | 80 | inferred |
| **Assumptions (a)–(h)** | `## Assumptions` · `id=assumptions` | Lines ~266–280. Eight assumptions: (a) remote sync sessions; (b) no-auth MVP V1; (c) Fibonacci + T-Shirt scales; (d) integrations to V2; (e) target audience already practises PP; (f) SaaS monetisation model; (g) no formal market validation yet; (h) problem widely distributed across agile teams. | 35 (aggregate) | (a)–(e) to validate with Submitter; (f)–(h) to validate via Discovery |
| **Metrics / success criteria** | Not a discrete section in SRC-001 | Embedded in `impact` (efficiency model) and `discovery` brief (criteria). Efficiency proxy: 15–20 min waste reduced per session. Quality proxy: improved estimate predictability. Discovery exit criteria (SRC-001 lines ~326–327): 5 interviews, qualitative pain evidence, corrected impact model, assumptions (f)–(h) revisited. | — | see impact + discovery sections |
| **Risks** | Embedded across `assumptions`, `impact` hint, `triage` | Key risks: (1) arithmetic inconsistency in efficiency model (~10x discrepancy between Submitter's "8–11 h-h/year" and model's ~96–128 h-h/year); (2) no market validation (TAM, willingness-to-pay, revenue projections absent); (3) urgency absent (weakens prioritisation); (4) real-time state for simultaneous participants (assumption a — architecture concern for Tech Lead). | — | parked / discovery |
| **Triage decision** | `## Triage — routing decision` · `id=triage` | Lines ~225–250. Verdict: **Discovery** (AI draft, pending human sign-off). All 4 blocking fields cleared (≥ threshold). Routed to Discovery because commercial market is explicitly unvalidated, not due to capture gaps. | draft | pending owner confirmation |
| **Discovery brief** | `## Discovery brief` · `id=discovery` | Lines ~307–327. 5 items: (1) problem-market fit interviews; (2) willingness-to-pay / monetisation validation; (3) correct efficiency impact model; (4) TAM market sizing; (5) urgency / market-entry window. Time-box: 3 weeks (→ 2026-06-24). Exit criteria explicit. | — | draft |
| **MVP phases V1 / V1.1 / V2** | `### Declared priority` (summary) + SRC-002 `# Funcionalidades do MVP` | SRC-001 lines ~215–219 (scope priority overview); SRC-002 lines ~322–352 (full feature lists). V1: create room, share link, no-auth entry, task list, secret voting, reveal, multi-round, consensus, session history. V1.1: timer, auto-reveal, automatic statistics, CSV export. V2: Jira/Linear integrations, permanent teams, org-level history, metrics dashboard, round comparison, anonymous vote comments. | — | from SRC-002 |
| **Architectural escalation** | `## Architectural escalation` · `id=cto_escalation` | Lines ~255–261. Verdict: Not needed (draft). MVP V1 is UI/state extension with well-defined business rules. No payments, no complex multi-tenancy, no AI/runtime, no external integrations (V2 only). Real-time state for simultaneous participants is a Tech Lead viability question, not an architectural escalation. | draft | pending owner confirmation |
| **Handoff** | `## Handoff` · `id=handoff` | Lines ~331–339. Three paths: (a) proceed with Discovery brief; (b) re-triage to Product Ready after Discovery confirms fit; (c) re-triage to Backlog; (d) Discovery reveals no fit → archive. Immediate action: owner must sign off triage, assign themselves, open Discovery brief. | — | pending owner action |

---

## Open Dispositions — Carry-Forward Notice

The following open items from the intake MUST be carried forward into the RP
elaboration. They are not gaps to paper over — they are honest epistemic states
that the PO acknowledged when choosing to proceed despite the Discovery triage.

### 8 Assumptions to validate

| ID | Assumption | Validator | Risk if false |
|---|---|---|---|
| (a) | Sessions are remote and synchronous with simultaneous connected participants | Submitter | Changes real-time state architecture |
| (b) | No authentication in MVP V1 — name-only identification is sufficient | Submitter | May require identity management if there is a future identity requirement |
| (c) | Relevant scales are Fibonacci and T-Shirt (customisable); others are secondary | Submitter | Low risk — industry standard |
| (d) | Jira/Linear integrations are V2 — MVP V1 does not depend on them | Submitter (confirm V2 scope) | Low risk — explicitly scoped out |
| (e) | Target audience already practises Planning Poker — no method onboarding needed | Submitter | Impacts positioning and product copy |
| (f) | Monetisation model = SaaS per organisation, plans by users/teams/features | Submitter / Discovery | Unvalidated willingness-to-pay — central commercial risk |
| (g) | No formal market validation exists; sufficient problem-fit assumed | Discovery (interviews/market tests) | High — if fit is weaker than expected, commercial viability collapses |
| (h) | Problem is widely distributed across agile teams (addressable market sufficient for SaaS) | Discovery (market sizing) | Without TAM/SAM data, scalability of the commercial model is unproven |

### 1 Commercial / Market Discovery Flag

The business impact section (SRC-001 `id=impact`, Layer B) is explicitly
flagged as a **discovery item, not a capture gap**. The Submitter declared no
formal market validation, no revenue projections, and no TAM quantification.
The stated objective is to validate whether sufficient problem-market adherence
exists before committing development capacity to a commercial product. This flag
must appear in the RP's scope and risk sections — it is not resolved by the
intake.

### Urgency uncaptured

`id=urgency` in SRC-001 has confidence 0. No window, deadline, competitor, or
cost-of-waiting was declared. This is non-blocking at the intake gate but
weakens relative prioritisation. If the Discovery brief reveals a market-entry
window (item 5 of the brief), urgency can be revisited. The RP should note this
absence explicitly and not invent urgency.

### Arithmetic inconsistency (impact model)

The efficiency model in SRC-001 (`id=impact`, Layer A) contains a flagged
arithmetic inconsistency: the Submitter cited "8–11 h-h/year per squad" as
savings, but the stated model (15–20 min × ~48 sessions/year × 8 people)
produces ~96–128 h-h/year — a ~10x discrepancy. The RP should not use the
Submitter's cited savings figure in materials without first resolving the base
calculation. This is assigned to Discovery item 3.

---

<!-- END OF DOCUMENT -->
