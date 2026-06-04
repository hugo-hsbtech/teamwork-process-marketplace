# Escalation — architectural triggers and the freeze gate

The RP stops at product definition. Technical viability, constraints,
architecture decisions, and technical risk belong to a **separate artefact** —
the CTO's Technical Assessment. The RP references the Assessment via
`TechAssessmentRef`; it does not absorb it. The fusion happens in the PRD
(`PRD = RP + Technical Assessment`).

`readiness-escalation-flagger` decides one thing: does this demand owe a
Technical Assessment? It runs once in the draft pass, after scope and
business-rules sections are drafted.

## Architectural trigger list

Escalation is required when the demand touches any of the following
(`personas/02-po.md:299`):

- **Infrastructure or platform changes** — new services, migrations, changes to
  deployment topology, scaling infrastructure.
- **Multi-tenancy or data isolation** — demands that affect tenant boundaries,
  data partitioning, or isolation guarantees.
- **AI / runtime / model behaviour** — demands that incorporate ML models,
  AI-driven decisions, or depend on non-deterministic runtime behaviour.
- **Security, authentication, or authorization** — new auth flows, permission
  models, cryptographic requirements, or compliance constraints.
- **Integrations with external systems that carry unknowns** — third-party APIs,
  external data sources, or inter-system contracts not yet specified.

If none of these are present, escalation is `not_requested`.

## The TechAssessmentRef data shape

`TechAssessmentRef` is a **bridge to the CTO's artefact**, not a section of
the RP. It carries (`personas/02-po.md:152–156`):

| Field | Values | Meaning |
|---|---|---|
| `status` | `not_requested` · `requested` · `in_progress` · `signed` · `vetoed` | Lifecycle state of the Technical Assessment |
| `verdict` | `viável` · `viável-com-ressalvas` · `inviável-como-escopado` | CTO's feasibility ruling (populated when status = `signed`) |
| `link` | reference path or ID | Pointer to the Technical Assessment artefact (CTO's document, not RP content) |

The RP **references** this; it does not absorb the CTO's content. The CTO
never edits the RP. If the CTO vetoes feasibility, the PO revises the RP scope
and re-freezes; the CTO does not redefine the product.

## The freeze gate condition

`freezeReady = true` requires (`personas/02-po.md:161–163`):

1. Every `blocksFreeze` section is resolved: `po_authored` / `decided` /
   confirmed-`inherited`, **or** honestly disposed as `discovery`.
2. `TechAssessmentRef.status ∈ {signed, not_requested}`.
   - If escalation was requested and the Assessment has not returned
     (`status = requested` or `in_progress`), the RP **does not freeze** —
     it waits for the CTO's verdict.
   - If escalation was not required (`status = not_requested`), the gate
     clears on product completeness alone.

## Documented divergence — provisional freeze (temporary)

**Current state:** the `tech-assessment` skill does not yet exist.
When `readiness-escalation-flagger` detects a trigger, it proposes:

```
TechAssessmentRef.status   = requested
TechAssessmentRef.disposition = deferred
Hint: "TA needed; tech-assessment skill not yet available"
```

The RP then freezes **provisionally**: the product sections are frozen and the
package is marked **provisionally frozen**, with the manifest noting
`tech-assessment-ref: deferred (TA pending — out of current tooling scope)`.

The `packager` outputs this flag explicitly in `output/manifest.md` so the
downstream (PRD/PM handoff) knows the Technical Assessment is still owed.

**Migration note:** when the `tech-assessment` skill lands, tighten the gate to
require `TechAssessmentRef.status = signed` before freezing. The `deferred`
path will be retired; the skill will block at the freeze gate and hand off to
the TA skill to produce the Assessment. Update this file and the manifest
template at that time.

This divergence is deliberate and temporary. It is called out here, in the
skill's README, and in every manifest that the packager writes for a
provisionally-frozen RP.
