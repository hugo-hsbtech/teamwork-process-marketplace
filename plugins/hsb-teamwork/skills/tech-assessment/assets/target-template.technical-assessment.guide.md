# Companion guide — Technical Assessment template

How each section is filled, by `id`. The TA is authored **classify-first, then
draft-then-confirm** (see references/classification.md and references/feasibility.md):
the `tech-classifier` confirms the demand nature and resolves the Knowledge Base,
which **governs which path is required**; then the engine pre-fills every applicable
section at partial confidence with an explicit `Origin`, and the **CTO** reviews,
edits, justifies, and signs. No applicable section starts empty.

The TA is the **CTO's** artefact. It **responds** to the RP and is written **alone**;
it **never edits the RP** (`personas/02-po.md` §2/§10). It may **veto** feasibility —
then the PO revises the RP scope and re-escalates.

Origins: `inherited` (carried from the linked RP / Intake Record, keep its source),
`ai_drafted` (engine first-draft, partial confidence until the CTO confirms),
`cto_authored` (the CTO decided or explicitly confirmed a draft — full confidence),
`reused_from_KB` (an ADR/decision reused from the `tech-landscape` — full once the
CTO confirms). The promotion path is `inherited` / `ai_drafted` → **CTO review** →
`cto_authored`.

> These map onto the CTO persona's dispositions (`personas/03-cto.md` §6:
> `assessed` / `ai_drafted` / `reused_from_KB` / `discovery`) — `cto_authored` is the
> engine's name for `assessed` (the CTO judged directly). `discovery` is the honest
> "I can't assess yet" disposition: a technical unknown blocks the verdict, so it is
> time-boxed as a spike (→ `discovery-path`) rather than bluffed — exactly the
> Submitter's `discovery` philosophy applied to the terrain.

---

## The governing section — fill this first

- **`tech-classification`** (blocks, min-conf 80) — **the decision that governs the
  rest of the document.** `hsb-tech-classifier` inherits the demand nature
  (Greenfield / Brownfield / Hybrid) and the KB reference from the **Intake Record**,
  confirms them under the technical lens, and sets the **path to fill**:
  - **Greenfield** → the `tech-foundation` path is required; `current-state` is N/A.
  - **Brownfield** → the `current-state` path is required; `tech-foundation` is N/A.
  - **Hybrid** → **both** paths are required.
  Resolve the KB: `Exists` (reference the `tech-landscape-[system].md`), `Partial`
  (reference + name the gaps), or `Does not exist` (route documenting the current system as
  a **Discovery spike** in `discovery-path`, and have `hsb-landscape-keeper` create/seed
  the `tech-landscape`). Feasibility cannot be judged on unknown terrain. If the CTO
  cannot settle the nature, it becomes a CTO-priority question — do not guess.

---

## The CTO's first-class decision

- **`feasibility-verdict`** (blocks, min-conf 85) — the **CTO's first-class model is
  feasibility** (`personas/03-cto.md` §3 — *feasibility is first class*).
  `hsb-feasibility-assessor` proposes one verdict — `Feasible` / `Feasible with caveats` /
  `Infeasible as scoped` — carrying the full feasibility model: `verdict` + `rationale`
  + **`terrain`** + `confidence` + `source` + `generates`. A defensible rationale (never a
  rubber stamp), the **terrain** it rests on (the `tech-landscape` KB, or an honest
  "undocumented → Discovery" — *"feasibility cannot be assessed on unknown terrain"*,
  the CTO's golden rule, `03-cto.md` §3), and, when "with caveats", what must be true for
  it to hold. The **`generates`** field names what the verdict creates downstream —
  `hard_constraint` / `adr` / `discovery_spike` / `kb_update` — so the judgment links to
  the sections it drives. High threshold by design: this is the central CTO judgment, so
  it resolves only at high confidence and is always `cto_authored` (the CTO commits it).
  - **`Infeasible as scoped` is the veto path:** the verdict carries the veto +
    rationale; the TA still freezes (the CTO's decision is complete and signed), and the
    orchestrator signals the PO to revise the RP scope and re-escalate. The CTO does not
    redefine the product. See references/feasibility.md § The veto path.

> **Terrain is traced everywhere, not only here.** Beyond the verdict's explicit Terrain
> row, every entry's `Source` carries *trace-to-source* (`03-cto.md` §3 — e.g. "RP
> question #2", "tech-landscape §5", "reused ADR-102"), and `tech-classification` resolves
> the KB. Terrain is the structural twin of confidence: a verdict on undocumented terrain
> is a guess, not a verdict.

---

## Trace-to-source

- **`po-questions`** (blocks, min-conf 70) — the specific technical unknowns the PO
  escalated, each with the CTO's answer. Inherited from the RP's escalation / the
  `tech-assessment-ref` hint. Keeps the assessment anchored to what was asked. If no
  specific questions were escalated, state that explicitly with `Disposition: decided`.

---

## The two paths (only the path the classification requires is in force)

- **`current-state`** (BROWNFIELD path; blocks when nature ∈ {Brownfield, Hybrid}) —
  **document the system before changing it.** Existing patterns/conventions to respect,
  integration points touched (with coupling nature + risk), and technical debt /
  regression risk (with current test coverage). The equivalent of BMAD's
  *document-project*. When an up-to-date `tech-landscape` exists, **reference it** and
  record only what is specific to this demand. **If greenfield:** dispose
  `Disposition: decided`, content "N/A — greenfield (see Technical classification)".

- **`tech-foundation`** (GREENFIELD path; blocks when nature ∈ {Greenfield, Hybrid}) —
  **decide the foundation with criteria, not by reflex.** Stack selection (each layer:
  choice + decision criterion + discarded alternative), target architecture (C4-style
  context/container, only the levels that add value), and structure / repo conventions.
  These foundational choices **seed** a new `tech-landscape` via `hsb-landscape-keeper`.
  **If brownfield:** dispose `Disposition: decided`, content "N/A — brownfield (see
  Technical classification)".

> The non-applicable path's `Disposition: decided` N/A entry is an **honest disposition**
> that clears the freeze gate — it is not a gap. See references/classification.md.

---

## Technical sections (ai_drafted, CTO confirms)

For all sections in this group the engine drafts at partial confidence with
`Origin: ai_drafted`; the CTO reviews, edits, justifies, and confirms; on confirmation
each entry becomes `Origin: cto_authored`.

- **`affected-systems`** (blocks, min-conf 70) — every service/module touched and the
  nature of the impact (new / modified / consumed only). Inherit the systems the RP
  scope named.

- **`architectural-impact`** (blocks, min-conf 75) — **exclusive CTO territory** (migrated
  from old RP §8). For each area touched (data model, events, frontend, security,
  multi-tenancy, performance, observability) the impact and the architectural note
  (pattern to follow/avoid). Fill only the relevant areas.

- **`integrations`** (blocks, min-conf 70) — the RP's required integrations under the
  **technical feasibility** lens (migrated from old RP §7): type, protocol, and
  feasibility / known third-party risks per system. "None" with `Disposition: decided`
  if the demand has no integrations.

- **`build-vs-buy`** (non-blocking, min-conf 0) — for each non-trivial capability:
  Build / Buy / Reuse, with rationale and the effect on cost/timeline. Skip with
  `Disposition: decided` ("no relevant make-or-buy decision") if there is none.

- **`alternatives`** (blocks, min-conf 70) — **the rationale, not just the conclusion**
  (design-doc standard). One row per significant alternative: pros, cons, and **why it
  was NOT chosen** — so the downstream does not re-litigate it.

- **`nfr-feasibility`** (blocks, min-conf 75) — **closes the product ↔ technical loop.**
  One row per NFR the RP declared in §8: feasible? (Yes / With caveats / No), how it
  will be achieved, and the risk/caveat. An infeasible NFR is a veto or re-scoping
  signal, not a detail — surface it and reflect it in `feasibility-verdict`.

- **`testability-observability`** (blocks, min-conf 70) — how to **prove** it works
  (test strategy, test data/environment covering the RP §9 edge cases) and how to **see**
  it in production (telemetry/technical metrics, logs/alerts). Without this the RP
  acceptance criteria cannot be verified.

- **`hard-constraints`** (blocks, min-conf 75) — non-negotiable conditions that limit the
  solution space, with type, detail, and effect on scope. The PO does not soften these;
  if they disagree they escalate explicitly. "None" with `Disposition: decided` if
  there are none.

- **`tech-risks`** (blocks, min-conf 75) — **technical** risks only (product/business
  risks stay in the RP §12), each with category, probability, impact, and mitigation.

- **`adrs`** (blocks, min-conf 75) — architectural decisions at the CTO level. The
  engine (`hsb-adr-proposer`) **arrives with suggested ADRs** (reused from the
  `tech-landscape` KB where possible — `Origin: reused_from_KB`); the CTO approves /
  adjusts. Fine-grained / implementation ADRs belong to the Tech Lead's Tech Backlog.
  Each ADR needs the CTO sign-off mark.

- **`effort-cost`** (blocks, min-conf 70) — the CTO's **firm** estimates (replace the
  PO's preliminary RP §13 number): development effort by area + seniority, infrastructure
  impact, third-party cost, recurring operational cost, and a TCO assessment.
  `hsb-effort-estimator` proposes; the CTO firms it.

---

## Conditional section

- **`discovery-path`** (non-blocking, min-conf 0) — fill **only** if a technical unknown
  blocks the assessment from closing (incl. "the KB does not exist" from
  `tech-classification`). The CTO defines the spike/investigation; the PO determines the
  time-box; the demand returns to Discovery. If nothing blocks, "—" with
  `Disposition: decided`.

---

## Meta sections

- **`meta`** (non-blocking) — stable IDs (TA-AAAA-NNN, linked RP-AAAA-NNN vX,
  INT-AAAA-NNN), the responsible CTO, status (Requested / In progress / Signed off /
  Vetoed), the feasibility verdict mirror, sign-off date, and output language. Filled by
  the engine from context; the CTO confirms IDs and sign-off date.
- **`revisions`** (non-blocking) — version, date, author, status, and change summary per
  revision. Initialised v1 / In progress; updated each confirmed edit cycle.

---

## The bar

A good TA reads like a CTO's signed feasibility judgment *that an engineer who has never
seen the code could act on*: the demand nature is confirmed and governs the document; the
applicable path is filled and the other is honestly N/A; every NFR the RP declared has a
feasibility answer; alternatives record *why not*; ADRs carry the CTO's sign-off; the
effort/cost is firm; and the feasibility verdict is defensible — a clear `Feasible` /
`Feasible with caveats`, or an honest `Infeasible as scoped` veto with rationale. The TA
contains **no product authorship** — it responds to the RP and never edits it. It is the
technical half that merges with the RP into the PRD.
