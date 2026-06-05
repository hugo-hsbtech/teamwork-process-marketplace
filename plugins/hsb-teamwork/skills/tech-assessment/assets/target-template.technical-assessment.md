<!--
TARGET TEMPLATE · Technical Assessment (default)
This file is the contract. Each fillable section carries an annotation:
  <!- - origination: SECTION-ID; blocks=BOOL; min-confidence=N; kind=TYPE - ->
and a self-sufficient rubric. The Template Analyst derives contract.lock.md from
these (the same engine as origination-brainstorm / readiness-package — the marker
keyword stays `origination:`).
The confidence line adds an Origin field (inherited | ai_drafted | cto_authored |
reused_from_KB) per personas/03-cto.md §3/§6 and templates/03-technical-assessment.md.
The TA is the CTO's output: it RESPONDS to the RP and is authored ALONE by the CTO —
it never edits the RP. To use a different document type, copy this file, re-annotate,
and pass it as TEMPLATE. See references/contract-and-template.md (in origination-brainstorm).
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.

TWO PATHS, ONE TEMPLATE. The `tech-classification` section governs which path is
required: Greenfield (the TA DEFINES the foundation — fill `tech-foundation`) or
Brownfield/Hybrid (the TA DISCOVERS the current system — fill `current-state`).
Fill the applicable path; the other is dispositioned `Disposition: decided` with
content "N/A — see Technical classification" (an honest disposition that clears the
gate). See references/classification.md.
-->

# Technical Assessment — [Demand name]
<!-- rev: 0 · updated: YYYY-MM-DD -->

> The Technical Assessment (TA) is the **CTO's output** — and goes **beyond
> architecture**: it establishes the **technical terrain** on which engineering decides.
> Because the execution layer (human or AI agent) **has no implicit knowledge of the
> source code**, the TA makes explicit what normally goes unstated: the nature of the
> demand (new vs. existing software), the current state or the foundation to be created,
> the knowledge base, the feasibility of each NFR, the discarded alternatives,
> testability, and observability. It is written **alone** by the CTO, **in parallel** with
> the Readiness Package, and **responds** to it: the CTO **never edits the RP**. The TA
> does not redefine the product — it may **veto** the feasibility of the scope, in which
> case the PO revises the RP scope. The merge of the RP (product) with this TA (technical)
> happens in the PRD. See `personas/03-cto.md`, `personas/02-po.md` §2/§10, and
> `interactions/05-po-to-cto.md` / `interactions/06-cto-to-po.md`.

## Metadata
<!-- origination: id=meta; blocks=false; min-confidence=0; kind=meta -->

| Field | Value |
|---|---|
| **Assessment ID** | TA-YYYY-NNN |
| **Version** | v1 |
| **Linked RP** | RP-YYYY-NNN vX |
| **Linked Intake** | INT-YYYY-NNN |
| **Owner** | [Name] (CTO) |
| **Status** | Requested / In progress / Signed off / Vetoed |
| **Feasibility verdict** | Feasible / Feasible with caveats / Infeasible as scoped |
| **Sign-off date** | — |
| **Output language** | [e.g. en-US] |

## Revision History
<!-- origination: id=revisions; blocks=false; min-confidence=0; kind=meta -->

| Version | Date | Author | Status | Summary |
|---|---|---|---|---|
| v1 | YYYY-MM-DD | [Name] (CTO) | In progress | Initial assessment. |

---

## Feasibility Verdict
<!-- origination: id=feasibility-verdict; blocks=true; min-confidence=85; kind=capture -->
> Rubric: the **CTO's first-class decision** (`personas/03-cto.md` §3 — *feasibility is
> first class*: every judgment carries `verdict` + `rationale` + **`terrain`** +
> `confidence` + `source` + `generates`). Carries rationale — never a rubber stamp — and
> the **terrain** it rests on: *"feasibility cannot be assessed on unknown terrain"*
> (`03-cto.md` §3, the CTO's golden rule). If **Infeasible as scoped**, the CTO returns
> with a veto + rationale; the PO revises the RP scope and re-escalates. The CTO does not
> redefine the product. This section resolves only at high confidence (feasibility is the
> CTO's central judgment).

| Field | Value |
|---|---|
| **Verdict** | Feasible / Feasible with caveats / Infeasible as scoped |
| **Rationale** | [Why — defensible] |
| **Terrain** | `tech-landscape-[system].md` (the KB it rests on) · "undocumented → Discovery" |
| **Caveats (if applicable)** | [What must be true for the verdict to hold] |
| **Generates** | hard_constraint · adr · discovery_spike · kb_update · — |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Technical classification and Knowledge Base
<!-- origination: id=tech-classification; blocks=true; min-confidence=80; kind=capture -->
> Rubric: **the decision that governs the rest of the document.** Inherits the demand
> nature from the Intake and confirms it under the technical lens. Defines which path to
> fill (greenfield vs. brownfield) and anchors the TA in the knowledge base — what exists,
> what is missing, what will be created. If the KB does not exist or is incomplete
> (brownfield), documenting the current system is a **prerequisite**: register it as a
> spike in the *Discovery Path* and produce/update the `tech-landscape`. If greenfield,
> the foundational ADRs **seed** a new `tech-landscape`.

| Field | Value |
|---|---|
| **Nature (confirmed by CTO)** | Greenfield (new) · Brownfield (existing) · Hybrid (new within existing) |
| **Path to fill** | Technical foundation (greenfield) · Current state (brownfield) · Both (hybrid) |
| **Knowledge Base (KB)** | Exists → reference · Partial → reference + gaps · Does not exist → create (Discovery) |
| **KB reference** | `tech-landscape-[system].md` · link · — |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## PO Questions Addressed
<!-- origination: id=po-questions; blocks=true; min-confidence=70; kind=capture -->
> Rubric: *trace-to-source.* The specific technical unknowns the PO escalated — and the
> answer to each. Keeps the assessment anchored to what was asked (inherited from the RP /
> the escalation). Without at least one question addressed (or "no specific question was
> escalated"), the section is NOT satisfied.

| # | PO question | CTO answer |
|---|---|---|
| 1 | [Technical unknown] | [Answer] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## BROWNFIELD Path — Current state / Technical landscape
<!-- origination: id=current-state; blocks=true; min-confidence=75; kind=capture -->
> Rubric: **document the system before changing it** (fill in if the demand modifies
> existing software). In brownfield, the implementation decision depends on what already
> exists — patterns, conventions, integrations, debt. This is the equivalent of BMAD's
> *document-project*. When an up-to-date `tech-landscape` exists, **reference it** and
> record here only what is specific to this demand. **If greenfield:** not applicable —
> `Disposition: decided`, content "N/A — greenfield (see Technical classification)".

### Existing patterns and conventions to respect

| Aspect | How it is today | Implication for this demand |
|---|---|---|
| **Code structure / organization** | [Where things live] | [What to follow] |
| **Data / persistence patterns** | [Model, migrations] | |
| **API / contract patterns** | [REST/events, versioning] | |
| **Authentication / authorization** | [How it is applied] | |

### Integration points touched

| Integration point | System/module | Coupling nature | Risk of changing |
|---|---|---|---|
| [Interface/service] | [Who] | [Synchronous / event / shared DB] | High / Medium / Low |

### Technical debt and regression risk

| Area | Known debt / fragility | Regression risk | Current test coverage |
|---|---|---|---|
| [Module] | [What is fragile] | High / Medium / Low | [Good / partial / none] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## GREENFIELD Path — Technical foundation
<!-- origination: id=tech-foundation; blocks=true; min-confidence=75; kind=capture -->
> Rubric: **decide the foundation — with criteria, not by reflex** (fill in if the demand
> builds new software/module). In greenfield there is no terrain to discover: the TA
> **creates** it. Record the base choices and the *why*, so they sustain ADRs and become
> the starting point of the new `tech-landscape`. **If pure brownfield:** not applicable —
> `Disposition: decided`, content "N/A — brownfield (see Technical classification)".

### Stack selection (with criteria)

| Layer | Choice | Decision criterion | Discarded alternative |
|---|---|---|---|
| **Language / runtime** | [Choice] | [Why — team, ecosystem, performance] | [What and why not] |
| **Framework / app** | | | |
| **Persistence / data** | | | |
| **Infra / deploy** | | | |

### Target architecture

> Context and container diagram (C4 style — only the levels that add value). Text or reference to diagram.

```text
[Context/container diagram — systems, users, containers and how they communicate]
```

### Structure and repository conventions

- **Folder / module organization:** [pattern to adopt]
- **Naming / lint / test conventions:** [pattern to adopt]
- **Branching / CI strategy:** [pattern to adopt]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Affected Systems and Components
<!-- origination: id=affected-systems; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the blast-radius map. Each service/module touched and the nature of the impact.
> Inherits the systems/integrations the RP named in scope.

| System / Component | Nature of impact |
|---|---|
| [Service / module] | [New / modified / consumed only] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Architectural Impact
<!-- origination: id=architectural-impact; blocks=true; min-confidence=75; kind=capture -->
> Rubric: exclusive CTO territory (migrated from the old RP Section 8). For each area
> touched, the impact and the architectural note (pattern to follow/avoid). Fill in only
> the relevant areas — do not force the irrelevant ones.

| Area | Impact | Architectural note |
|---|---|---|
| **Data model** | [Description] | [Pattern to follow/avoid] |
| **Events / messaging** | [Description] | |
| **Frontend** | [Description] | |
| **Security** | [Description] | |
| **Multi-tenancy** | [Description] | |
| **Performance / Scalability** | [Description] | |
| **Observability** | [Description] | |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Required Integrations
<!-- origination: id=integrations; blocks=true; min-confidence=70; kind=capture -->
> Rubric: the RP's integrations, now under the **technical feasibility** lens (migrated
> from the old RP Section 7). For each system: type, protocol, and feasibility / known
> risks. If the demand has no integrations, record "none" with `Disposition: decided`.

| System | Type | Protocol | Feasibility / Known risks |
|---|---|---|---|
| [System 1] | Internal / External / API / Event / Webhook / DB | [REST / OIDC / gRPC / …] | [Feasible / third-party limitations / risk] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Build vs. Buy
<!-- origination: id=build-vs-buy; blocks=false; min-confidence=0; kind=capture -->
> Rubric: for each non-trivial capability — build, buy/integrate a third party, or reuse
> something existing? The decision has a direct effect on cost, timeline, and risk. Skip
> (with `Disposition: decided`, "no relevant make-or-buy decision") if there is none.

| Capability | Decision | Rationale | Effect on cost/timeline |
|---|---|---|---|
| [Capability] | Build / Buy / Reuse | [Why] | [Summary] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Alternatives Considered
<!-- origination: id=alternatives; blocks=true; min-confidence=70; kind=capture -->
> Rubric: **the rationale, not just the conclusion** (design-doc standard, Google/RFC).
> Recording what was evaluated and **why it was discarded** gives the downstream the
> context to decide on implementation — and prevents the same alternative from being
> re-litigated later. One row per significant alternative.

| Alternative | Pros | Cons | Why it was NOT chosen |
|---|---|---|---|
| [Approach A] | [Pros] | [Cons] | [Reason for rejection] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## NFR Feasibility  ·  *(mapped to RP, Section 8)*
<!-- origination: id=nfr-feasibility; blocks=true; min-confidence=75; kind=capture -->
> Rubric: **closes the product ↔ technical loop.** The PO declared quality requirements in
> the RP (Section 8); here the CTO responds, NFR by NFR, whether they are **feasible** and
> **how** — the *quality scenarios* from arc42. An infeasible NFR is a veto or re-scoping
> signal, not a detail. One row per NFR inherited from RP §8.

| NFR (from RP §8) | Feasible? | How it will be achieved / approach | Risk / caveat |
|---|---|---|---|
| [e.g.: propagation < 500ms] | Yes / With caveats / No | [Technical mechanism] | [What threatens it] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Testability and Observability
<!-- origination: id=testability-observability; blocks=true; min-confidence=70; kind=capture -->
> Rubric: how to **prove** it works and how to **see** it in production. Without this, the
> RP acceptance criteria cannot be verified and behavior cannot be monitored.

| Dimension | Approach |
|---|---|
| **Test strategy** | [Unit / integration / e2e — what covers what; regression risk areas] |
| **Test data / environment** | [How to reproduce scenarios, including edge cases from RP §9] |
| **Telemetry / technical metrics** | [What to instrument to observe the feature] |
| **Logs / alerts** | [Failure signals and how they will be detected] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Hard Constraints
<!-- origination: id=hard-constraints; blocks=true; min-confidence=75; kind=capture -->
> Rubric: non-negotiable conditions that limit the solution space. The PO does not soften
> or reinterpret them — if they disagree, they escalate explicitly
> (`interactions/06-cto-to-po.md`). If there are no hard constraints, record "none" with
> `Disposition: decided`.

| Constraint | Type | Detail | Effect on scope |
|---|---|---|---|
| [Constraint 1] | Technical / Platform / Security / Multi-tenancy / External | [Detail] | [What changes in the RP, if anything] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Technical Risks and Mitigations
<!-- origination: id=tech-risks; blocks=true; min-confidence=75; kind=capture -->
> Rubric: **technical** risks live here (migrated from the RP). Product/business risks
> remain in the RP (Section 12). Each risk carries category, probability, impact, and
> mitigation.

| Risk | Category | Probability | Impact | Mitigation |
|---|---|---|---|---|
| [Risk 1] | Technical / Security / Infra / Integration / Data | High / Medium / Low | High / Medium / Low | [Mitigation] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Architecture Decisions (ADRs)
<!-- origination: id=adrs; blocks=true; min-confidence=75; kind=capture -->
> Rubric: architectural direction at the CTO level. The AI may arrive with **suggested
> ADRs** (reused from the knowledge base) — the CTO approves/adjusts (the WOW moment of
> `03-cto.md` §3/§12). Fine-grained breakdown and implementation ADRs belong to the Tech
> Lead's Tech Backlog. Each ADR carries the decision, rationale, and the CTO sign-off.

| # | Decision | Rationale | CTO sign-off |
|---|---|---|---|
| ADR-001 | [Decision] | [Why this approach] | ✓ |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Effort and Cost Assessment (firm)
<!-- origination: id=effort-cost; blocks=true; min-confidence=70; kind=capture -->
> Rubric: internal use only. These are the CTO's **firm** estimates — they replace the
> PO's preliminary estimate (RP Section 13). They will be refined by the Tech Lead in the
> Tech Backlog. Not a contractual commitment or client-facing material.

### Development Effort

| Area | Estimate | Seniority |
|---|---|---|
| [Backend / Frontend / QA] | [X days] | Senior / Mid / Junior / QA |
| **Total** | **X days** | |

### Infrastructure Impact

[New provisioning, cluster changes, additional regions — or "None"]

### Third-Party Cost Impact

[New providers, licenses, paid APIs — or "None"]

### Recurring Operational Cost Impact

[Storage, observability, bandwidth — quantify if possible]

### TCO Assessment

[Is the feature cost-neutral, does it add recurring cost, or does it create a reusable foundation for future phases?]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

---

## Discovery Path (if a technical unknown blocks completion)
<!-- origination: id=discovery-path; blocks=false; min-confidence=0; kind=capture -->
> Rubric: fill in only if a technical unknown prevents the assessment from closing. The
> CTO defines the spike/investigation; the PO determines the time-box. The demand returns
> to Discovery (`interactions/05-po-to-cto.md`). If nothing blocks, record "—" with
> `Disposition: decided`.

| Unknown | Spike / Investigation | Who | Suggested time-box |
|---|---|---|---|
| [Technical unknown] | [What to investigate] | [CTO / team] | [N days] |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __

<!-- END OF DOCUMENT -->
