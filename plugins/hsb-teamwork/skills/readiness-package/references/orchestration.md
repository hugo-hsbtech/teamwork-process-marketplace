# Orchestration — RP phases, agents, and what is reused

This skill is a **multi-agent pipeline** that extends the intake engine. The
conversation you (the orchestrator) run is Layer 0 — the only layer that talks
to the PO. Everything else is a specialized subagent you spawn with a focused
prompt and tear down. This file is the authoritative spec for *who runs when,
who may write what, and what runs in parallel* in the readiness-package flow.

## What this reuses (no duplication)

The following engine-level method documents apply **unchanged** to this skill.
Do not copy their rules here; cite and apply them:

| Reference | What it governs |
|---|---|
| [`../../intake-brainstorm/references/contract-and-template.md`](../../intake-brainstorm/references/contract-and-template.md) | Template annotation format (`intake:` markers), `contract.lock.md` derivation, template-hash restart policy |
| [`../../intake-brainstorm/references/ledger-schema.md`](../../intake-brainstorm/references/ledger-schema.md) | `qa-log.md` schema — `Q###` blocks, header summary, rationale/spawned-by fields |
| [`../../intake-brainstorm/references/sessions.md`](../../intake-brainstorm/references/sessions.md) | Session root resolution (`$INTAKE_HOME` → git-root → cwd), resolve-or-resume, slug derivation |
| [`../../intake-brainstorm/references/writing-integrity.md`](../../intake-brainstorm/references/writing-integrity.md) | Single-writer rule, read-modify-write, queue/drain, `rev` marker, no-truncation sentinel |
| [`../../intake-brainstorm/references/grounding.md`](../../intake-brainstorm/references/grounding.md) | Quality calibration against the golden exemplar |
| [`../../intake-brainstorm/references/questioning-method.md`](../../intake-brainstorm/references/questioning-method.md) | Question rendering (`open` / `choice`), disposition routes, the `AskUserQuestion` protocol |

**Carry-forwards that apply unchanged:**
- **Single-writer rule** — every mutable file has exactly one writer agent; all
  others return read-only proposals to the orchestrator.
- **Read-modify-write** — every writer re-reads the file before editing and
  merges changes keyed by stable id; it never clobbers.
- **Session resolve-or-resume** — the `-readiness` session folder is resolved
  per [`../../intake-brainstorm/references/sessions.md`](../../intake-brainstorm/references/sessions.md);
  re-running resumes the same folder, nothing duplicates.
- **Ledger schema** — `qa-log.md` uses the same `Q###` block structure; the
  ledger-writer is the sole editor.
- **Annotation marker** — the RP template uses the same `<!-- intake: id=...; blocks=...; ... -->`
  grammar. The `intake:` prefix is the engine's contract grammar and stays
  unchanged even in RP templates.

## The agents you spawn (subagent_type)

### Reused engine agents

These carry their legacy `intake-` prefix names. They specialize through the RP
template and guide, not through code changes.

| Agent | Writer? | When spawned |
|---|---|---|
| `intake-template-validator` | read-only | Phase 1 start — audits the RP template |
| `intake-source-indexer` | **writer** (`sources/`, `sources-index.md`) | Phase 1, parallel after validator passes |
| `intake-template-analyst` | **writer** (`contract.lock.md`) | Phase 1, parallel after validator passes |
| `intake-question-strategist` | read-only | Confirm loop — targets low-confidence/unconfirmed blocking sections (fallback only) |
| `intake-file-extraction` | read-only | Confirm loop — satisfies open questions from indexed sources |
| `intake-reconciler` | read-only | Confirm loop — on conflicts (e.g. intake said X, PO now says Y) |
| `intake-ledger-writer` | **writer** (`qa-log.md`) | Confirm loop — records questions, answers, proposed entries |
| `intake-doc-updater` | **writer** (`readiness-document.md`) | Draft pass + confirm loop — the sole writer of the RP document |
| `intake-glossary-keeper` | **writer** (`glossary.md`) | Optional, when domain terms accumulate |
| `intake-readiness-reporter` | **writer** (`readiness-report.md`) | Optional, gap map for the PO |
| `intake-confidence-auditor` | read-only | Confirm loop — re-scores sections, flags conflicts |
| `intake-humanizer` | **writer** (`output/humanized.md`) | Phase 4 — must finish before translator/enricher |
| `intake-translator` | **writer** (`output/translated.pt-BR.md`) | Phase 4, parallel with visual-enricher |
| `intake-visual-enricher` | **writer** (`output/enriched.md`) | Phase 4, parallel with translator |
| `intake-packager` | **writer** (`output/manifest.md`) | Phase 4 (wrap) |

### New readiness-* agents

| Agent | Writer? | When spawned |
|---|---|---|
| `readiness-inheritor` | read-only proposer | Phase 1, after source-indexer completes — pre-fills inheritable sections |
| `readiness-drafter` | read-only proposer | Phase 2 (draft pass) — proposes `ai_drafted` sections |
| `readiness-escalation-flagger` | read-only proposer | Phase 2, once scope and business-rules are drafted |

**`intake-doc-updater` and `intake-ledger-writer` are the only writers of
`readiness-document.md` and `qa-log.md` respectively.** All three new
`readiness-*` agents are read-only proposers; they return structured proposals
to the orchestrator, who routes them through the single writers.

## Phase 0 — Identify the demand (you + the PO)

1. **Resolve the linked intake-record path.** Confirm which `Product Ready`
   demand's intake session folder to inherit from (`SESSION_ROOT/<demand-slug>/`).
2. **Resolve-or-resume the `-readiness` session** per
   [`../../intake-brainstorm/references/sessions.md`](../../intake-brainstorm/references/sessions.md):
   session folder is `SESSION_ROOT/<demand-slug>-readiness/`. If it already
   exists, resume it; if ambiguous, list candidates and ask.
3. **Confirm output language.** Default is `pt-BR` (mirrors the intake default).
   Record in session context; the translator will target this language in Phase 4.

Do not ask a wall of questions at this stage — just collect the intake-record
path and confirm language.

## Phase 1 — Setup

1. **`intake-template-validator`** audits the RP template. Proceed only once it
   passes; fix the template if it fails the audit checklist
   ([`../../intake-brainstorm/references/contract-and-template.md`](../../intake-brainstorm/references/contract-and-template.md) § audit checklist).
2. Then spawn **in the same turn** (independent → parallel):
   - **`intake-source-indexer`** indexes the linked intake-record folder (its
     `output/humanized.md` or `target-document.md` as the primary source) plus
     any extra files the PO provides. Writes `sources/` and `sources-index.md`.
   - **`intake-template-analyst`** derives `contract.lock.md` from the RP
     template (hash-locked). If a prior `contract.lock.md` exists with a
     different hash, it restarts analysis and supersedes stale ledger entries.
3. Once both complete: spawn **`readiness-inheritor`** (read-only). It reads the
   indexed intake-record and proposes carry-forward entries for all inheritable
   RP sections (`exec-summary`, `context-problem`, `objectives`, `personas`,
   `scope`, `metrics`, `release-criteria`, `risks`), each tagged
   `Origin: inherited` at the intake's preserved confidence (plus the
   non-blocking `effort-estimate` and `roadmap` when the intake-record informs
   them). Route proposals to `intake-ledger-writer` then `intake-doc-updater`
   (serial).

Gate: `contract.lock.md` must exist and inherited sections must be written
before moving to Phase 2.

## Phase 2 — Draft pass

1. Spawn **`readiness-drafter`** (read-only). It reads the contract, the
   inherited entries, and the indexed sources, and proposes first drafts for the
   new product sections: `business-rules`, `user-stories` (Given/When/Then ACs),
   `nfrs` (ISO/IEC 25010 scaffold), and `edge-cases`. All proposals carry
   `Origin: ai_drafted` at partial confidence with a hint naming what the PO
   must confirm.
2. **`intake-doc-updater`** writes the `ai_drafted` proposals into
   `readiness-document.md` at partial confidence (serial, single-writer).
3. Spawn **`readiness-escalation-flagger`** (read-only) once scope and
   business-rules sections exist. It scans for architectural triggers and
   proposes the `tech-assessment-ref` disposition (see [`escalation.md`](escalation.md)).
   Route its proposal to `intake-doc-updater`.

At the end of Phase 2 every section has an entry — either `inherited`,
`ai_drafted`, or `discovery` (when the drafter cannot confidently propose) — so
the PO never faces a blank form.

## Phase 3 — Confirm loop (until freezeReady)

Repeats until the freeze gate clears:

1. **`intake-confidence-auditor`** (read-only) re-scores every section against
   its rubric, flags conflicts, returns the gap verdict.
   - On a flagged conflict (e.g. intake said X, PO now says Y): spawn
     **`intake-reconciler`** (read-only) to recommend resolution; route to
     `intake-ledger-writer`.
   - Optional: spawn **`intake-readiness-reporter`** to write a live gap map.
2. **`intake-question-strategist`** (read-only, **fallback only**) targets the
   lowest-confidence / unconfirmed blocking sections. Questions fire only when
   the engine could not draft a section confidently or the PO asks to deepen
   it (see [`drafting.md`](drafting.md) § When questions fire).
3. PO reviews the pre-filled document, edits sections, confirms entries. Each
   confirmed entry is recorded by **`intake-ledger-writer`** (serial).
4. **`intake-doc-updater`** promotes confirmed entries: `Origin: ai_drafted` /
   `inherited` → `po_authored`, raising confidence to reflect PO judgment.
5. **Gate check:** `freezeReady = true` when every `blocksFreeze` section is
   either resolved (`po_authored` / `decided` / confirmed-`inherited`) or
   honestly disposed (`discovery`), **and** `TechAssessmentRef.status ∈
   {signed, not_requested}`. See [`escalation.md`](escalation.md) §
   Documented divergence for the temporary `deferred` path when a TA is owed
   but the tech-assessment skill does not yet exist.

Optional: spawn **`intake-glossary-keeper`** when domain terms accumulate (after
first confirm rounds and again before production).

## Phase 4 — Production & wrap

Once `freezeReady`:

1. **`intake-humanizer`** writes `output/humanized.md` — the canonical clean
   copy all production agents read. Must finish first.
2. Then spawn **in the same turn** (parallel, distinct files):
   - **`intake-translator`** → `output/translated.pt-BR.md` (or the confirmed
     output language).
   - **`intake-visual-enricher`** → `output/enriched.md` (scope in/out table,
     persona/JTBD map, business-rule flow, metrics table with guardrails).
3. **`intake-packager`** writes `output/manifest.md` noting: freeze state,
   the TA-pending flag (if `tech-assessment-ref` disposition is `deferred`),
   open `discovery` dispositions, template hash/version, and the handoff note
   to PRD/PM.
4. Report to the PO: what was produced, the readiness score, the TA flag if
   present, and every item still parked as `discovery` or `deferred`.

## The session folder layout

```
SESSION_ROOT/<demand-slug>-readiness/
├── contract.lock.md            # intake-template-analyst
├── sources-index.md            # intake-source-indexer
├── sources/                    # intake-source-indexer (incl. inherited intake-record)
├── qa-log.md                   # intake-ledger-writer
├── readiness-document.md       # intake-doc-updater
├── glossary.md                 # intake-glossary-keeper (optional)
├── readiness-report.md         # intake-readiness-reporter (optional)
└── output/
    ├── humanized.md            # intake-humanizer
    ├── translated.pt-BR.md     # intake-translator
    ├── enriched.md             # intake-visual-enricher
    └── manifest.md             # intake-packager
```
