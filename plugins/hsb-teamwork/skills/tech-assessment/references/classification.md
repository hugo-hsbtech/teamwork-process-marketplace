# Classification — the decision that governs the document

The TA has **two paths, one template** (`templates/03-technical-assessment.md`) — the
**terrain fork** (`personas/03-cto.md` §3.1: greenfield *creates* the terrain, brownfield
*discovers* it). Because *feasibility cannot be assessed on unknown terrain* (`03-cto.md`
§3, the CTO's golden rule), the **first thing the CTO classifies is whether the terrain
already exists.** The `tech-classification` section decides which path is in force, so it
is filled **first** — before any path section is drafted. `hsb-tech-classifier` is the
**governing proposer**: the rest of the run keys off its output.

## The classification is born at triage, confirmed here

The demand nature is **not** invented by the CTO. It was born at triage (Act 1 of the
PO journey — see the readiness-package's `references/triage.md`) and carried into the
Intake Record and the RP metadata. `hsb-tech-classifier`:

1. **Inherits** the nature (Greenfield / Brownfield / Hybrid) and the KB reference
   (`tech-landscape-[system].md` · Partial · To create · N/A) from the **Intake Record**.
2. **Confirms them under the technical lens** — the CTO can override a triage
   classification that the code reality contradicts (e.g. triage said "new feature" but
   it actually modifies an existing module → Brownfield). An override carries a rationale.
3. If it genuinely cannot tell, it marks the nature as a **CTO-priority question**
   rather than guessing.

## Nature → path to fill

| Nature | Path in force (blocking) | Other path | What the TA does |
|---|---|---|---|
| **Greenfield** (new software/module) | `tech-foundation` | `current-state` → N/A | **Defines** the foundation: stack (with criteria), target architecture (C4), structure/conventions. These ADRs **seed** a new `tech-landscape`. |
| **Brownfield** (changes existing software) | `current-state` | `tech-foundation` → N/A | **Discovers** the existing system: patterns/conventions to respect, integration points, debt/regression risk. References (or creates) the `tech-landscape`. |
| **Hybrid** (new module inside existing) | **both** `tech-foundation` and `current-state` | — | Both: define the new module's foundation **and** document the existing terrain it plugs into. |

**The non-applicable path is not a gap.** When a path does not apply, its entry is
filled with `Disposition: decided` and content `"N/A — <nature> (see Technical
classification)"`. This is an **honest disposition** that clears the freeze gate — exactly
like a `discovery` disposition does in the other skills. The orchestrator and the
Confidence Auditor treat a `decided` N/A path entry as resolved, not missing.

## Knowledge Base resolution

The TA cannot judge feasibility on unknown terrain. The classifier resolves the KB — the
terrain's `kbStatus` dial (`personas/03-cto.md` §5.2: `complete` / `partial` / `stub` /
`absent`), surfaced here as `Exists` / `Partial` / `Does not exist`:

| KB state | What it means | What the TA does |
|---|---|---|
| **Exists** | An up-to-date `tech-landscape-[system].md` exists | **Reference it**; record in `current-state` only what is specific to this demand |
| **Partial** | A `tech-landscape` exists but has gaps for this demand | Reference it + name the gaps; fill the gaps in `current-state`; `hsb-landscape-keeper` updates the KB |
| **Does not exist** (brownfield/hybrid) | No KB for the system being changed | **Documenting the current system is a prerequisite** — register a documentation **Discovery spike** in `discovery-path`, and have `hsb-landscape-keeper` create the `tech-landscape`. Feasibility cannot be signed until the terrain is known. |
| **N/A (greenfield)** | No prior terrain to discover | The TA **is the origin** of the KB — the foundational ADRs seed a new `tech-landscape` (Phase 4/5). |

## Why it matters

Without the classification the CTO guesses. With it:

- **Greenfield** → the TA *creates* the terrain (the foundation, then the KB).
- **Brownfield** → the TA *discovers* the terrain (the current state, against the KB).

The classification also tells the orchestrator **which sections to fan out to the
Section Drafter** in Phase 3 (only the in-force path), and tells
`hsb-landscape-keeper` whether to **seed** (greenfield) or **update/reference**
(brownfield) the persistent `tech-landscape`. See [`landscape.md`](landscape.md).

## What the classifier does not do

- It does not draft the path sections — that is `hsb-section-drafter`'s job.
- It does not write shared files — it returns a proposal to the orchestrator, which
  routes it through `hsb-ledger-writer` → `hsb-doc-updater`.
- It does not re-run triage — it confirms (or overrides with rationale) a
  classification that already exists upstream.

## On an override (write the correction to the index, not the frozen RP)

An override does **not** rewrite the frozen RP or Intake Record — they stay canonical
for what they decided at triage. Instead the classifier emits a `nature-override`
signal and the orchestrator records the correction where cross-front truth lives: it
updates this front's `initiative.json` (`nature`, `kbStatus`) and pushes a
`nature-corrected` note to the `readiness/` front. The **index**, not the frozen
document, is what later fronts read, so the corrected nature is the one that travels.
The TA's `tech-classification` (and the PRD's `b-nature-landscape`, which inherits from
the TA) are authoritative over the superseded RP metadata.
