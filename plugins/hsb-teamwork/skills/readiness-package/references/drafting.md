# Drafting — the draft-then-confirm model

The RP authoring model is **draft-then-confirm**, not section-by-section
interviewing. The screen "should not look like a form filled by hand … it
should look like the system already rationalized the demand and is asking for
the PO's judgment" (`personas/02-po.md:324`). The racionalização "renders as
a materialized product vision: RP sections pre-filled by AI, each with
confidence and origin, each statement traceable — and the PO's job is to
review, edit, justify, and freeze" (`:327`).

This file documents the two stages, the `Origin` lifecycle, when questions
fire, and how read-only proposals flow to the single writer.

## The two stages

### Stage 1 — Draft pass

No section starts empty. Before the PO sees the document, the engine pre-fills
every section:

- **`hsb-stage-inheritor`** proposes carry-forward entries for inheritable
  sections (`exec-summary`, `context-problem`, `objectives`, `personas`,
  `scope`, `metrics`, `release-criteria`, `risks`; plus the non-blocking
  `effort-estimate` and `roadmap` when the origination-record informs them). Each
  entry is tagged `Origin: inherited` with the origination-record's preserved
  confidence.
- **`hsb-section-drafter`** proposes first-draft entries for the new product
  sections (`business-rules`, `user-stories`, `nfrs`, `edge-cases`). Each
  entry is tagged `Origin: ai_drafted` at partial confidence with an explicit
  hint naming what the PO must confirm.
- If the drafter cannot produce a defensible draft for a section (sources too
  thin), it proposes `Disposition: discovery` instead of inventing content —
  honesty over coverage.

The `hsb-doc-updater` writes all proposals into `readiness-document.md`
through the single-writer path (see [`orchestration.md`](orchestration.md)
§ Phase 2).

### Stage 2 — Confirm loop

The PO receives a fully-drafted document. The work is **reviewing, editing,
and confirming** — not filling blanks. For each section the PO either:

- **Accepts** the draft as-is → `hsb-ledger-writer` records confirmation;
  `hsb-doc-updater` promotes `Origin: ai_drafted` → `po_authored`.
- **Edits** the draft → PO's version recorded, origin promotes to `po_authored`
  / `decided`.
- **Accepts an inherited entry** as sufficient for the RP → origin stays
  `inherited` at confirmed confidence.
- **Marks as discovery** → counts as *resolved-as-unknown, time-boxed*
  (`:242-247`); does not block freeze.

The loop repeats until `freezeReady` (see [`orchestration.md`](orchestration.md)
§ Phase 3 gate check).

## The Origin lifecycle

Every RPEntry carries an `origin` field that tracks how it was produced and
whether it has been validated by the PO (`personas/02-po.md:149`):

| `origin` | Meaning | Confidence state |
|---|---|---|
| `inherited` | Carried from the origination-record with its graded source | Partial, traceable — may rise on PO confirmation |
| `ai_drafted` | Engine pre-filled; awaiting PO review | Partial until confirmed |
| `po_authored` | PO decided directly or explicitly confirmed a draft | Full confidence |
| `reused_from_KB` | Reused from a prior RP/ADR *(deferred — out of scope)* | Full, if confirmed |

The promotion path is: `inherited` / `ai_drafted` → **PO review** → `po_authored`.
The `hsb-doc-updater` performs the promotion when `hsb-ledger-writer`
records a confirmed answer. Confidence rises at promotion time to reflect the
PO's judgment; it is never inflated before that.

## Why questions are a fallback, not the primary mode

The question-first machinery (`hsb-question-strategist` → human →
`hsb-ledger-writer`) is the engine's default loop for the origination skill,
where the Submitter fills a blank document. For the RP, that model is inverted:
the system pre-rationalizes; the PO judges.

**Questions fire only when:**
1. The engine could not draft a section confidently (below the section's
   `min-confidence` threshold after the draft pass) — the gap the drafter
   could not close.
2. The PO explicitly asks to deepen a section (a follow-up investigation the
   PO initiates, not the engine).

In all other cases, the PO judges the draft directly. The `hsb-confidence-auditor`
identifies the low-confidence gaps and the `hsb-question-strategist` targets
only those. This keeps the interaction as a judgment surface, not an interview.

## How proposals flow to the single writer

Both `hsb-stage-inheritor` and `hsb-section-drafter` are **read-only proposers**:
they return structured proposal lists to the orchestrator and write nothing.

The orchestrator routes:
1. Proposals → **`hsb-ledger-writer`** (records in `qa-log.md`).
2. Ledger entries → **`hsb-doc-updater`** (writes to `readiness-document.md`).

This preserves the single-writer guarantee from the origination engine
([`../../origination-brainstorm/references/writing-integrity.md`](../../origination-brainstorm/references/writing-integrity.md)):
`readiness-document.md` has exactly one writer (`hsb-doc-updater`), and
`qa-log.md` has exactly one writer (`hsb-ledger-writer`). The drafters never
hold the pen on shared files.
