# Companion guide — Readiness Package template

How each section is filled, by `id`. The RP is authored **draft-then-confirm**
(see references/drafting.md): the engine pre-fills every section at partial
confidence with an explicit `Origin`, and the PO reviews, edits, justifies, and
freezes. No section starts empty.

Origins: `inherited` (carried from the linked origination-record, keep its source),
`ai_drafted` (engine first-draft, partial confidence until the PO confirms),
`po_authored` (the PO decided), `reused_from_KB` (deferred — out of scope).

---

## Inheritable sections (origin defaults to `inherited` when the origination-record covers it)

For all sections in this group: origin defaults to `inherited` when the
origination-record covers the material (keep the inherited Source and confidence as-is,
never downgrade); else `ai_drafted`. The PO confirms or edits; on confirmation the
entry becomes `Origin: po_authored`.

- **`exec-summary`** (blocks, min-conf 70) — 2–4 short paragraphs: what is the
  problem, what will be built, and what is the expected business outcome. Must be
  readable by any stakeholder without additional context. Inherit and expand from
  the origination-record's problem/impact fields when possible. A draft that merely
  re-states the feature request without anchoring to the business outcome is not
  satisfied.

- **`context-problem`** (blocks, min-conf 80) — the guardian section. Pain with
  observable symptoms, no solution. If the draft names a feature, turn it back into
  the pain that feature would relieve; if you can't, it isn't satisfied. Inherit the
  origination-record's problem statement and deepen it; never downgrade its confidence.

- **`objectives`** (blocks, min-conf 70) — numbered, observable objectives this
  delivery must achieve after release. Each objective must be verifiable: if it
  cannot be measured or observed, it is not satisfied. Minimum two objectives.
  Inherit from origination-record impact/urgency when available.

- **`personas`** (blocks, min-conf 70) — for each persona: the job-to-be-done (what
  they are trying to accomplish) and how they are affected by this delivery. Without
  a defined persona, scope and acceptance criteria have no anchor. Inherit from the
  origination-record's `reach` field when available; expand with job-to-be-done framing.

- **`scope`** (blocks, min-conf 75) — protects the downstream from scope creep. Must
  list explicitly what is OUT, not only what is in. Deferred items feed the Roadmap
  (Section 14). Without "Excluído" filled, the section is NOT satisfied. Draft all
  three subsections (Incluído / Excluído / Adiado) even at partial confidence.

- **`metrics`** (blocks, min-conf 70) — projected values: the baseline that
  metrics.md will confront with post-rollout actuals. Include leading and lagging
  indicators and at least one guardrail (the metric that must not worsen). Each
  target carries its projection confidence. Inherit from origination-record impact
  quantifications; mark low-confidence projections with a firming hint.

- **`release-criteria`** (blocks, min-conf 70) — high-level indicators that define
  "done and valuable" for this release — distinct from the continuous metrics in
  Section 10. Must cover at least the Business, Quality, and UX dimensions. Generic
  criteria ("works well") are NOT satisfied: require a measurable target value.

- **`risks`** (blocks, min-conf 70) — product, business, adoption, external, and
  compliance risks. Technical risks migrate to the Technical Assessment. Each risk
  carries probability, impact, and mitigation. Product/business dependencies listed
  separately. Inherit known risks from the origination-record's constraints/assumptions.

- **`effort-estimate`** (non-blocking, min-conf 0) — internal use only: the PO's
  rough guess to support sequencing. The firm number comes from the CTO in the
  Technical Assessment. Not a contractual commitment, not for clients. Confidence
  expected to be low (`ai_drafted` or `po_authored` without firm data); always mark
  it as preliminary with a firming hint pointing to the CTO Assessment.

- **`roadmap`** (non-blocking, min-conf 0) — suggested sequencing of value beyond
  this release. Deferred items from Section 5 feed future phases. MVP = this
  release; Phase 2 and Phase 3 are future backlog. Not a delivery commitment. Draft
  all three phase subsections; the PO confirms phasing and priority.

---

## Product sections (ai_drafted, PO confirms)

For all sections in this group: the engine drafts at partial confidence with
`Origin: ai_drafted`; the PO reviews, edits, justifies, and confirms. On
confirmation each entry becomes `Origin: po_authored`.

- **`business-rules`** (blocks, min-conf 80) — rules, validations, and state
  transitions that govern the functionality. Each rule must be verifiable and
  atomic. State-transition flows must cover error paths, not just the happy path.
  Draft by inferring rules from the origination-record's scope signals and problem
  statement; flag any rule that requires PO confirmation explicitly. A draft with
  only the happy path is not satisfied.

- **`user-journey`** (blocks, min-conf 70) — the end-to-end user journey, the
  missing piece between "what" and "the stories". Draft the main happy-path journey
  (3+ steps: trigger/action → expected result → touchpoint → precondition), plus
  alternative/exit paths (which tie to edge-cases), and an **optional** service
  blueprint only when there is relevant backstage/ops/human-in-the-loop. PO
  territory — product flow, not detailed UX. Compression: a small improvement is a
  3–5 step happy path with no blueprint. **User stories (next) derive from these
  steps** — each happy-path step generates or validates a story. Without at least
  the main journey's happy path, the section is NOT satisfied. Draft from scope,
  personas, and business-rules; `Origin: ai_drafted` at partial confidence.

- **`user-stories`** (blocks, min-conf 80) — **epics and the user stories grouped
  under them**. Each **epic** is a coherent **deliverable** of value (`EPIC-NNN` +
  title + objective/value): the block the team ships and the stakeholder recognises
  as a result. Under each epic come its stories, in the format "Como [persona],
  quero [ação], para [benefício]"; acceptance criteria in Given/When/Then, verifiable
  by a non-developer, with specific limits (not "should work well"). This is the
  behaviour contract that QA validates. **Derive the stories from the journey steps
  (`user-journey`)** — one story per happy-path step (and the alternative paths) —
  from scope and personas, and **group stories that deliver the same value outcome
  into one epic**; mark each as `Origin: ai_drafted` at partial confidence. The PO
  confirms the epics and the story set, adjusts scope, and verifies that each
  acceptance criterion is testable by someone without code access. **Deliverable-
  evidence rule: every story belongs to exactly one epic and no story is orphaned —
  if a story fits no epic, an epic is missing.** At least one epic with one story
  required; no upper limit, but prefer atomic stories over omnibus ones.

### `nfrs` — non-functional requirements (ai_drafted, PO confirms)

Draft an ISO/IEC 25010 checklist scaffold (performance, reliability, security,
usability, compatibility, maintainability) and propose the categories that apply
to this demand, each at partial confidence with `Origin: ai_drafted`. Do NOT assert
viability — that is the CTO's Technical Assessment. The PO confirms which apply and
sets targets; on confirmation the entry becomes `Origin: po_authored`.

- **`edge-cases`** (blocks, min-conf 70) — error states, timeouts, permissions,
  concurrency. For AI features: model behaviour under low confidence and failure
  modes. First class — not a footnote. Each item describes the expected system
  behaviour (not merely what can go wrong). Draft from scope and business rules;
  flag gaps for PO confirmation. A section with only happy-path edge cases is not
  satisfied.

---

## Derived and bridge sections

### `tech-assessment-ref` — the bridge to the CTO artefact (handle with care)

This is a **reference**, not content (personas/02-po.md:152, 300-301). The
escalation-flagger decides whether a Technical Assessment is owed. When it is:
- set "Escalada requisitada? = Sim",
- record `Disposition: deferred` with a hint "TA needed; tech-assessment skill not
  yet available", and
- the RP freezes **provisionally** (spec §8 divergence). When the tech-assessment
  skill lands, this tightens to require Status=Assinado.
When no escalation is needed, set Status=not_requested, Disposition=decided.

### `meta` — identifiers, status, and linked origination

Holds the stable IDs (RP-AAAA-NNN, linked INT-AAAA-NNN), the responsible PO,
escalation flag, freeze status, and output language. Also carries the **demand
nature** (Greenfield / Brownfield / Híbrido) and the **Knowledge Base** reference
(`tech-landscape-[system].md` · Parcial · A criar · N/A) **inherited from the Intake
Record** — the Stage Inheritor copies these forward; do not re-derive them. Filled by
the engine from context at creation; the PO confirms IDs and freeze date. Non-blocking.

### `revisions` — version history

Tracks version, date, author, status, and change summary for each revision.
Initialised with v1/Rascunho at creation; updated on each confirmed edit cycle.
Non-blocking.

### `inherited-readiness` — open dispositions carried from the origination-record

A summary table listing the origination readiness score, assumptions still to validate,
open discovery unknowns, and delegated requirements with owners — surfacing what
came in soft so it is visible at the start of execution, not buried in sections.
Filled by the engine from the linked origination-record's readiness/handoff data;
the PO reviews and confirms nothing was missed. If a carried assumption is later
falsified during execution, the demand must be re-evaluated (the origination re-triage
trigger applies downstream). Non-blocking.

---

## The bar

A good RP reads like a product demand *understood and owned*: the problem is pain
not solution, every inheritable section traces back to the origination-record with its
confidence preserved, ai_drafted product sections are explicit first-drafts the PO
can confirm or contest (never silent assertions), dispositions are honest
(`discovery` is acceptable; blank is not), and the `tech-assessment-ref` is either
closed (not_requested) or honestly deferred. The RP does not contain CTO-authored
content; viability lives in the Technical Assessment, which the RP only references.
