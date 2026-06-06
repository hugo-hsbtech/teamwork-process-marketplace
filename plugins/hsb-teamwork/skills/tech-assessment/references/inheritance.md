# Inheritance — carry-forward from the RP and the Intake Record

The Readiness Package is not just another source file. It is an **already-graded,
frozen artefact**: the PO rationalized the product, scored every section, and froze it.
The TA **responds** to the RP — it does not re-derive the product. `hsb-stage-inheritor`
carries the RP's relevant material forward into the TA's inheritable sections,
preserving the RP's `confidence` / `source` / `disposition`, so the CTO starts from a
traceable baseline rather than a blank form.

`inherited = partial confidence, traceable`. The TA **never edits the RP**
(`personas/02-po.md` §2/§10) — inheritance is read-only carry-forward into the TA's
own document.

## How the RP and Intake are indexed

The orchestrator discovers the **RP** from the works index in `initiative.json` (the
phase whose `produces` is `readiness-package`, via its `artifacts.canonical` / `final`
path) and the **Intake Record** from the `intake/` phase. It hands both to
`hsb-source-indexer`, which records them as **in-place references** in the assessment
phase's `sources-index.md` (the RP as the **primary source**), alongside the
`tech-landscape` if one exists — each read at its canonical path, never copied into
`sources/` (which holds only files the CTO provides). Shared terms come from the
brokered `PHASE_DIR/glossary.md`.

`hsb-stage-inheritor` reads the referenced RP + Intake and the TA contract
(`contract.lock.md`). It does **not** perform fresh inference — it maps RP/Intake
sections to TA sections, preserving the already-graded values.

## The section mapping

| Source section | TA section | Inheritance note |
|---|---|---|
| Intake: **demand nature** + **KB reference** | `tech-classification` (meta carry) | Carried verbatim into the metadata so `hsb-tech-classifier` confirms (not re-derives) it. |
| RP **escalation / specific technical questions** | `po-questions` | The unknowns the PO escalated become the rows the CTO answers. Trace-to-source preserved. |
| RP §7 **required integrations** | `integrations` | Carry the systems/protocols the PO named; the CTO adds the **feasibility** column. |
| RP scope / §6 systems touched | `affected-systems` | Carry the services/modules the scope implies; the CTO confirms the nature of impact. |
| RP §8 **NFRs** | `nfr-feasibility` | **One row per RP NFR** — the PO's quality requirement is the question side; the CTO answers feasibility + how. This is the product↔technical loop. |
| RP §9 **edge cases** | `testability-observability` (test data/env) | Carried as the scenarios the test strategy must reproduce. |
| RP §13 **preliminary effort** | `effort-cost` (context only) | Carried as the PO's preliminary number that the CTO's **firm** estimate replaces — not as the answer. |

Sections with no RP/Intake counterpart (`feasibility-verdict`, `current-state` /
`tech-foundation`, `architectural-impact`, `alternatives`, `hard-constraints`,
`tech-risks`, `adrs`, `discovery-path`) are **CTO-authored** — drafted by
`hsb-section-drafter` / the specialized proposers, or authored directly by the CTO. The
inheritor never invents content for sections the RP did not cover.

## What the inheritor preserves

For every proposed entry:

1. **Content** — restated for the TA section, without adding new substance (no
   feasibility claims — that is the CTO's, drafted/confirmed downstream).
2. **`confidence`** — the RP's graded value, never inflated. If the TA section needs
   more than the RP gives, it **lowers** confidence and adds a hint naming what the CTO
   must deepen.
3. **`source`** — the RP's source attribution (RP section id, PO authorship).
4. **`disposition`** — any open RP disposition carried forward verbatim.

## What the inheritor does not do

- It does not assert feasibility, draft the architectural impact, or propose ADRs —
  those are CTO-authored (Section Drafter, ADR Proposer, Feasibility Assessor, or the
  CTO directly).
- It does not edit the RP (it has no authorship there) — it only carries forward.
- It does not write shared files — it returns proposals to the orchestrator, which
  routes them through `hsb-ledger-writer` → `hsb-doc-updater` per the single-writer
  rule ([`../../origination-brainstorm/references/writing-integrity.md`](../../origination-brainstorm/references/writing-integrity.md)).
