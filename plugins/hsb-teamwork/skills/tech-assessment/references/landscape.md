# Tech Landscape — the persistent knowledge base the TA seeds or references

The `tech-landscape-<system>.md` is the **technical knowledge base per system** (not
per demand): product/stack/structure/integrations/debt. It is the "prior knowledge
base" that gives an engineer — or an AI agent with no implicit knowledge of the
source — the terrain for implementation decisions. It is the CTO's **terrain contract**
(`personas/03-cto.md` §5.2): persistent, per-system, the only CTO contract that is not
per-demand — *feasibility rests on terrain* (§3), and the execution layer has no implicit
knowledge of the code. Style: *steering docs* (Kiro) / `document-project` (BMAD). See
`templates/tech-landscape.md` and `templates/README.md`.

The TA's relationship to it depends on the **demand nature** (see
[`classification.md`](classification.md)):

- **Greenfield** → the TA is the **origin** of the KB. The foundational ADRs and stack
  choices in `tech-foundation` **seed** a new `tech-landscape-<system>.md`.
- **Brownfield** → the TA is a **consumer** of the KB. The `current-state` path
  **references** the existing `tech-landscape`, and records back into it anything new
  this demand discovered (updates, not a rewrite).
- **Hybrid** → both: seed the new module's section, update the existing system's.

`hsb-landscape-keeper` is the **sole writer** of `tech-landscape-<system>.md` (a
persistent, initiative/repo-level file — distinct from the per-phase
`technical-assessment.md`). It is the only TA proposer that holds a pen on a shared
file, and it never touches `technical-assessment.md` or `qa-log.md`.

## When it runs

| Nature / KB state | When | What it does |
|---|---|---|
| Greenfield (KB N/A) | Phase 5 (or Phase 4 once ADRs are confirmed) | **Creates** `tech-landscape-<system>.md`, seeding it from the confirmed foundational ADRs, stack selection, and structure conventions. |
| Brownfield, KB `Exists` | Phase 4 | **References** it (no write needed) unless the demand revealed something new; then a small **update**. |
| Brownfield/Hybrid, KB `Does not exist` | Phase 4 (the Discovery spike) | **Creates** the KB by documenting the current system — this is the prerequisite that unblocks the feasibility verdict (feasibility cannot be signed on unknown terrain). |
| Brownfield/Hybrid, KB `Partial` | Phase 4 | **Updates** it — fills the gaps `tech-classification` named. |

## Inputs (injected)

`PHASE_DIR`, `SKILL_DIR`, `LANDSCAPE_PATH` (the `tech-landscape-<system>.md` to seed or
update — resolved by the orchestrator at the initiative/repo level), `NATURE`
(Greenfield / Brownfield / Hybrid), and the confirmed TA sections it draws from
(`tech-foundation` / `current-state`, `adrs`, `architectural-impact`).

## What it writes

A `tech-landscape-<system>.md` that follows the `templates/tech-landscape.md` shape:
product context, stack, structure/conventions, integration points, and known debt. On
**create** (greenfield), it is seeded from the TA's foundation. On **update**
(brownfield), it merges in only what is new — read-modify-write, keyed by section,
never clobbering existing KB content (obey
[`../../origination-brainstorm/references/writing-integrity.md`](../../origination-brainstorm/references/writing-integrity.md):
no truncation; end with the sentinel; re-read before editing).

## Why it is separate from the TA document

The TA is a **per-demand** artefact (frozen, versioned, merged into one PRD). The
`tech-landscape` is **persistent and cross-cutting** — it outlives the demand and is
read by every future TA, Tech Backlog, and engineer. Keeping the Landscape Keeper as
the single writer of the KB (and read-only-proposing everything else into the TA via
the doc-updater) preserves the single-writer guarantee across both files.
