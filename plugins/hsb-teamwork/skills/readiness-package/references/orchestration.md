# Orchestration — RP phases, agents, and what is reused

This skill is a **multi-agent pipeline** that extends the origination engine. The
conversation you (the orchestrator) run is Layer 0 — the only layer that talks
to the PO. Everything else is a specialized subagent you spawn with a focused
prompt and tear down. This file is the authoritative spec for *who runs when,
who may write what, and what runs in parallel* in the readiness-package flow.

## What this reuses (no duplication)

The following engine-level method documents apply **unchanged** to this skill.
Do not copy their rules here; cite and apply them:

| Reference | What it governs |
|---|---|
| [`../../origination-brainstorm/references/contract-and-template.md`](../../origination-brainstorm/references/contract-and-template.md) | Template annotation format (`origination:` markers), `contract.lock.md` derivation, template-hash restart policy |
| [`../../origination-brainstorm/references/ledger-schema.md`](../../origination-brainstorm/references/ledger-schema.md) | `qa-log.md` schema — `Q###` blocks, header summary, rationale/spawned-by fields |
| [`../../origination-brainstorm/references/sessions.md`](../../origination-brainstorm/references/sessions.md) | Session root resolution (`$ORIGINATION_HOME` → git-root → cwd), resolve-or-resume, slug derivation |
| [`../../origination-brainstorm/references/writing-integrity.md`](../../origination-brainstorm/references/writing-integrity.md) | Single-writer rule, read-modify-write, queue/drain, `rev` marker, no-truncation sentinel |
| [`../../origination-brainstorm/references/grounding.md`](../../origination-brainstorm/references/grounding.md) | Quality calibration against the golden exemplar |
| [`../../origination-brainstorm/references/questioning-method.md`](../../origination-brainstorm/references/questioning-method.md) | Question rendering (`open` / `choice`), disposition routes, the `AskUserQuestion` protocol |

**Carry-forwards that apply unchanged:**
- **Single-writer rule** — every mutable file has exactly one writer agent; all
  others return read-only proposals to the orchestrator.
- **Read-modify-write** — every writer re-reads the file before editing and
  merges changes keyed by stable id; it never clobbers.
- **Session resolve-or-resume** — the `-readiness` session folder is resolved
  per [`../../origination-brainstorm/references/sessions.md`](../../origination-brainstorm/references/sessions.md);
  re-running resumes the same folder, nothing duplicates.
- **Ledger schema** — `qa-log.md` uses the same `Q###` block structure; the
  ledger-writer is the sole editor.
- **Annotation marker** — the RP template uses the same `<!-- origination: id=...; blocks=...; ... -->`
  grammar. The `origination:` prefix is the engine's contract grammar and stays
  unchanged even in RP templates.

## The agents you spawn (subagent_type)

### Reused engine agents

These are phase-agnostic specialists (`hsb-*`), shared with origination-brainstorm and
any future stage. They specialize through the RP template and guide, not through
code changes.

| Agent | Writer? | When spawned |
|---|---|---|
| `hsb-template-validator` | read-only | Phase 1 start — audits the RP template |
| `hsb-source-indexer` | **writer** (`sources/`, `sources-index.md`) | Phase 1, parallel after validator passes |
| `hsb-template-analyst` | **writer** (`contract.lock.md`) | Phase 1, parallel after validator passes |
| `hsb-question-strategist` | read-only | Confirm loop — targets low-confidence/unconfirmed blocking sections (fallback only) |
| `hsb-evidence-extractor` | read-only | Confirm loop — satisfies open questions from indexed sources |
| `hsb-reconciler` | read-only | Confirm loop — on conflicts (e.g. origination said X, PO now says Y) |
| `hsb-ledger-writer` | **writer** (`qa-log.md`) | Confirm loop — records questions, answers, proposed entries |
| `hsb-doc-updater` | **writer** (`readiness-document.md`) | Draft pass + confirm loop — the sole writer of the RP document |
| `hsb-glossary-keeper` | **writer** (`glossary.md`) | Optional, when domain terms accumulate |
| `hsb-gap-reporter` | **writer** (`readiness-report.md`) | Optional, gap map for the PO |
| `hsb-confidence-auditor` | read-only | Confirm loop — re-scores sections, flags conflicts |
| `hsb-synthesizer` | read-only | Optional — composes generic `derived` sections; in the RP the `inherited-readiness` and `tech-assessment-ref` derived sections are composed by the Stage Inheritor and Escalation Flagger instead |
| `hsb-humanizer` | **writer** (`output/humanized.md`) | Phase 4 — must finish before translator/enricher |
| `hsb-translator` | **writer** (`output/translated.pt-BR.md`) | Phase 4, parallel with visual-enricher |
| `hsb-visual-enricher` | **writer** (`output/enriched.md`) | Phase 4, parallel with translator |
| `hsb-packager` | **writer** (`output/manifest.md`) | Phase 4 (wrap) |

### Stage-agnostic agents this skill drives

Named for their function, not for this phase, so later stages can reuse them; the
readiness-package skill is their first consumer.

| Agent | Writer? | When spawned |
|---|---|---|
| `hsb-stage-inheritor` | read-only proposer | Phase 1, after source-indexer completes — pre-fills inheritable sections from the upstream origination-record |
| `hsb-section-drafter` | read-only proposer | Phase 2 (draft pass) — proposes `ai_drafted` sections |
| `hsb-escalation-flagger` | read-only proposer | Phase 2, once scope and business-rules are drafted |

**`hsb-doc-updater` and `hsb-ledger-writer` are the only writers of
`readiness-document.md` and `qa-log.md` respectively.** All three stage-agnostic
agents above are read-only proposers; they return structured proposals
to the orchestrator, who routes them through the single writers.

## Phase 0 — Identify the demand (you + the PO)

1. **Resolve the linked origination-record path.** Confirm which `Product Ready`
   demand's origination session folder to inherit from (`SESSION_ROOT/<demand-slug>/`).
2. **Resolve-or-resume the `-readiness` session** per
   [`../../origination-brainstorm/references/sessions.md`](../../origination-brainstorm/references/sessions.md):
   session folder is `SESSION_ROOT/<demand-slug>-readiness/`. If it already
   exists, resume it; if ambiguous, list candidates and ask.
3. **Confirm output language.** Default is `pt-BR` (mirrors the origination default).
   Record in session context; the translator will target this language in Phase 4.

Do not ask a wall of questions at this stage — just collect the origination-record
path and confirm language.

## Phase 1 — Setup

1. **`hsb-template-validator`** audits the RP template. Proceed only once it
   passes; fix the template if it fails the audit checklist
   ([`../../origination-brainstorm/references/contract-and-template.md`](../../origination-brainstorm/references/contract-and-template.md) § audit checklist).
2. Then spawn **in the same turn** (independent → parallel):
   - **`hsb-source-indexer`** indexes the linked origination-record folder (its
     `output/humanized.md` or `target-document.md` as the primary source) plus
     any extra files the PO provides. Writes `sources/` and `sources-index.md`.
   - **`hsb-template-analyst`** derives `contract.lock.md` from the RP
     template (hash-locked). If a prior `contract.lock.md` exists with a
     different hash, it restarts analysis and supersedes stale ledger entries.
3. Once both complete: spawn **`hsb-stage-inheritor`** (read-only). It reads the
   indexed origination-record and proposes carry-forward entries for all inheritable
   RP sections (`exec-summary`, `context-problem`, `objectives`, `personas`,
   `scope`, `metrics`, `release-criteria`, `risks`), each tagged
   `Origin: inherited` at the origination's preserved confidence (plus the
   non-blocking `effort-estimate` and `roadmap` when the origination-record informs
   them). Route proposals to `hsb-ledger-writer` then `hsb-doc-updater`
   (serial).

Gate: `contract.lock.md` must exist and inherited sections must be written
before moving to Phase 2.

## Phase 2 — Draft pass

1. Spawn **`hsb-section-drafter`** (read-only). It reads the contract, the
   inherited entries, and the indexed sources, and proposes first drafts for the
   new product sections: `business-rules`, `user-stories` (Given/When/Then ACs),
   `nfrs` (ISO/IEC 25010 scaffold), and `edge-cases`. All proposals carry
   `Origin: ai_drafted` at partial confidence with a hint naming what the PO
   must confirm.
2. **`hsb-doc-updater`** writes the `ai_drafted` proposals into
   `readiness-document.md` at partial confidence (serial, single-writer).
3. Spawn **`hsb-escalation-flagger`** (read-only) once scope and
   business-rules sections exist. It scans for architectural triggers and
   proposes the `tech-assessment-ref` disposition (see [`escalation.md`](escalation.md)).
   Route its proposal to `hsb-doc-updater`.

At the end of Phase 2 every section has an entry — either `inherited`,
`ai_drafted`, or `discovery` (when the drafter cannot confidently propose) — so
the PO never faces a blank form.

## Phase 3 — Confirm loop (until freezeReady)

Repeats until the freeze gate clears:

1. **`hsb-confidence-auditor`** (read-only) re-scores every section against
   its rubric, flags conflicts, returns the gap verdict.
   - On a flagged conflict (e.g. origination said X, PO now says Y): spawn
     **`hsb-reconciler`** (read-only) to recommend resolution; route to
     `hsb-ledger-writer`.
   - Optional: spawn **`hsb-gap-reporter`** to write a live gap map.
2. **`hsb-question-strategist`** (read-only, **fallback only**) targets the
   lowest-confidence / unconfirmed blocking sections. Questions fire only when
   the engine could not draft a section confidently or the PO asks to deepen
   it (see [`drafting.md`](drafting.md) § When questions fire).
3. PO reviews the pre-filled document, edits sections, confirms entries. Each
   confirmed entry is recorded by **`hsb-ledger-writer`** (serial).
4. **`hsb-doc-updater`** promotes confirmed entries: `Origin: ai_drafted` /
   `inherited` → `po_authored`, raising confidence to reflect PO judgment.
5. **Gate check:** `freezeReady = true` when every `blocksFreeze` section is
   either resolved (`po_authored` / `decided` / confirmed-`inherited`) or
   honestly disposed (`discovery`), **and** `TechAssessmentRef.status ∈
   {signed, not_requested}`. See [`escalation.md`](escalation.md) §
   Documented divergence for the temporary `deferred` path when a TA is owed
   but the tech-assessment skill does not yet exist.

Optional: spawn **`hsb-glossary-keeper`** when domain terms accumulate (after
first confirm rounds and again before production).

## Phase 4 — Production & wrap

Once `freezeReady`:

1. **`hsb-humanizer`** writes `output/humanized.md` — the canonical clean
   copy all production agents read. Must finish first.
2. Then spawn **in the same turn** (parallel, distinct files):
   - **`hsb-translator`** → `output/translated.pt-BR.md` (or the confirmed
     output language).
   - **`hsb-visual-enricher`** → `output/enriched.md` (scope in/out table,
     persona/JTBD map, business-rule flow, metrics table with guardrails).
3. **`hsb-packager`** writes `output/manifest.md` noting: freeze state,
   the TA-pending flag (if `tech-assessment-ref` disposition is `deferred`),
   open `discovery` dispositions, template hash/version, and the handoff note
   to PRD/PM.
4. Report to the PO: what was produced, the readiness score, the TA flag if
   present, and every item still parked as `discovery` or `deferred`.

## The session folder layout

```
SESSION_ROOT/<demand-slug>-readiness/
├── contract.lock.md            # hsb-template-analyst
├── sources-index.md            # hsb-source-indexer
├── sources/                    # hsb-source-indexer (incl. inherited origination-record)
├── qa-log.md                   # hsb-ledger-writer
├── readiness-document.md       # hsb-doc-updater
├── glossary.md                 # hsb-glossary-keeper (optional)
├── readiness-report.md         # hsb-gap-reporter (optional)
└── output/
    ├── humanized.md            # hsb-humanizer
    ├── translated.pt-BR.md     # hsb-translator
    ├── enriched.md             # hsb-visual-enricher
    └── manifest.md             # hsb-packager
```
