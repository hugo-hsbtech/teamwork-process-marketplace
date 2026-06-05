# Escalation — architectural triggers and the freeze gate

The RP stops at product definition. Technical viability, constraints,
architecture decisions, and technical risk belong to a **separate artefact** —
the CTO's Technical Assessment. The RP references the Assessment via
`TechAssessmentRef`; it does not absorb it. The fusion happens in the PRD
(`PRD = RP + Technical Assessment`).

`hsb-escalation-flagger` decides one thing: does this demand owe a
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
When `hsb-escalation-flagger` detects a trigger, it proposes:

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

**Migration note — the `tech-assessment` skill has landed.** The
[`tech-assessment`](../../tech-assessment/SKILL.md) skill now exists. The handoff is:

1. The RP freezes (provisionally) with `TechAssessmentRef.status = requested` /
   `disposition = deferred` and pushes the owed Technical Assessment into the
   initiative index `owes` (`{ "ref": "TechAssessmentRef", "to": "tech-assessment",
   "status": "deferred" }`).
2. `/hsb-teamwork:tech-assessment` runs as the `assessment/` phase, **consumes** that
   frozen RP (+ the Intake Record), produces the signed Technical Assessment, and
   **discharges the debt** in the index — setting the `owes` entry to `status: signed`
   (verdict `viável` / `viável-com-ressalvas`) or `status: vetoed`
   (`inviável-como-escopado`), with a link to the TA.
3. On a **veto**, the TA signals the PO to revise the RP scope and re-escalate
   (Revisit mode bumps the RP and, in turn, the TA version).

So `TechAssessmentRef.status` now moves `deferred → signed | vetoed` once the TA front
runs. The **tightened gate** — requiring `TechAssessmentRef.status = signed` before the
RP can be considered *fully* (not provisionally) frozen — is satisfied by reading the
discharged `owes` entry from the index after the `assessment/` phase completes.

The provisional-`deferred` path remains the documented behaviour **only** for the window
between RP freeze and the TA front running (or when the `tech-assessment` skill is not
installed). It is called out here, in the skill's README, and in every manifest the
packager writes for a provisionally-frozen RP — and is resolved as soon as the TA front
discharges the debt.
