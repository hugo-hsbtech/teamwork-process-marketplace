# Orchestration — RP phases, agents, and what is reused

This skill is a **multi-agent pipeline** that extends the origination engine. The
conversation you (the orchestrator) run is Layer 0 — the only layer that talks
to the PO. Everything else is a specialized subagent you spawn with a focused
prompt and tear down. This file is the **narrative** view of *who runs when,
who may write what, and what runs in parallel* in the readiness-package flow. The
**machine** view — validated ordering + the single-writer/single-decider invariants —
is declared per act in [`../pipeline.intake.yaml`](../pipeline.intake.yaml) (Act 1) and
[`../pipeline.readiness.yaml`](../pipeline.readiness.yaml) (Act 2), checked by
`tools/pipeline_graph.py` (see
[`../../tech-assessment/references/scheduling.md`](../../tech-assessment/references/scheduling.md)).
When the prose and the graph disagree, the graph wins.

## What this reuses (no duplication)

The following engine-level method documents apply **unchanged** to this skill.
Do not copy their rules here; cite and apply them:

| Reference | What it governs |
|---|---|
| [`../../origination-brainstorm/references/contract-and-template.md`](../../origination-brainstorm/references/contract-and-template.md) | Template annotation format (`origination:` markers), `contract.lock.md` derivation, template-hash restart policy |
| [`../../origination-brainstorm/references/ledger-schema.md`](../../origination-brainstorm/references/ledger-schema.md) | `qa-log.md` schema — `Q###` blocks, header summary, rationale/spawned-by fields |
| [`../../origination-brainstorm/references/initiatives.md`](../../origination-brainstorm/references/initiatives.md) | Initiatives root resolution (`$TEAMWORK_HOME` → git-root + `/.teamwork` → cwd), resolve-or-select, `.teamwork/<initiative>/` + phase-folder layout |
| [`../../origination-brainstorm/references/writing-integrity.md`](../../origination-brainstorm/references/writing-integrity.md) | Single-writer rule, read-modify-write, queue/drain, `rev` marker, no-truncation sentinel |
| [`../../origination-brainstorm/references/localization.md`](../../origination-brainstorm/references/localization.md) | No-language-leak invariant: leak taxonomy, token map, verbatim allowlist, derived-telemetry line break |
| [`../../origination-brainstorm/references/grounding.md`](../../origination-brainstorm/references/grounding.md) | Quality calibration against the golden exemplar |
| [`../../origination-brainstorm/references/questioning-method.md`](../../origination-brainstorm/references/questioning-method.md) | Question rendering (`open` / `choice`), disposition routes, the `AskUserQuestion` protocol |

**Carry-forwards that apply unchanged:**
- **Single-writer rule** — every mutable file has exactly one writer agent; all
  others return read-only proposals to the orchestrator.
- **Read-modify-write** — every writer re-reads the file before editing and
  merges changes keyed by stable id; it never clobbers.
- **Initiative resolve-or-select** — the `readiness/` phase folder is resolved
  under the selected initiative
  per [`../../origination-brainstorm/references/initiatives.md`](../../origination-brainstorm/references/initiatives.md);
  re-running resumes the same phase folder, nothing duplicates.
- **Ledger schema** — `qa-log.md` uses the same `Q###` block structure; the
  ledger-writer is the sole editor.
- **Annotation marker** — the RP template uses the same `<!-- origination: id=...; blocks=...; ... -->`
  grammar. The `origination:` prefix is the engine's contract grammar and stays
  unchanged even in RP templates.

## The agents you spawn (subagent_type)

### Reused engine agents

These are phase-agnostic specialists (`hsb-*`), shared with origination-brainstorm
and any future stage. They specialize through the RP template and guide, not through
code changes.

| Agent | Writer? | When spawned |
|---|---|---|
| `hsb-template-validator` | read-only | Setup of each act — audits that act's template (intake in A, RP in B1) |
| `hsb-source-indexer` | **writer** (`sources/`, `sources-index.md`) | Setup of each act, parallel after validator passes |
| `hsb-template-analyst` | **writer** (`contract.lock.md`) | Setup of each act, parallel after validator passes |
| `hsb-triage-assessor` | read-only | Phase A — see the stage-agnostic table below |
| `hsb-question-strategist` | read-only | Triage questions (Phase A) and the B3 confirm loop — targets low-confidence/unconfirmed blocking sections (fallback in B3) |
| `hsb-evidence-extractor` | read-only | Confirm loop (B3) — satisfies open questions from indexed sources |
| `hsb-reconciler` | read-only | Confirm loop (B3) — on conflicts (e.g. origination said X, PO now says Y) |
| `hsb-ledger-writer` | **writer** (`qa-log.md`, per phase) | Both acts — records questions, answers, proposed entries (intake then RP) |
| `hsb-doc-updater` | **writer** (`$DOC` per phase) | Both acts — sole writer of `intake-record.md` (Act 1) and `readiness-document.md` (Act 2), selected via injected `DOC` |
| `hsb-glossary-keeper` | **writer** (initiative `glossary.md`) | Optional, when domain terms accumulate; spawned with `DEFINITIONS_DIR` |
| `hsb-decisions-keeper` | **writer** (initiative `decisions.md`) | Optional, when cross-phase decisions accumulate (incl. the triage routing decision); spawned with `DEFINITIONS_DIR` |
| `hsb-gap-reporter` | **writer** (`readiness-report.md`) | Optional, gap map for the PO |
| `hsb-confidence-auditor` | read-only | Confirm loop (B3) — re-scores sections (incremental via `SECTIONS`), flags conflicts |
| `hsb-integrity-checker` | read-only | Confirm loop (B3) — mechanically verifies the document is complete/untruncated (sentinel, no elision) |
| `hsb-language-auditor` | read-only | Phase B4 — verifies the humanized copy for language leaks; leaks route back to the Humanizer |
| `hsb-synthesizer` | read-only | Optional — composes generic `derived` sections; in the RP the `inherited-readiness` and `tech-assessment-ref` derived sections are composed by the Stage Inheritor and Escalation Flagger instead |
| `hsb-humanizer` | **writer** (`output/humanized.md`) | Phase B4 — must finish before translator/enricher |
| `hsb-enrichment-analyst` | **writer** (`output/enrichment-plan.md`) | Phase B4 — runs in parallel with the Humanizer; catalogs the sourced visual opportunities the Enricher then renders |
| `hsb-translator` | **writer** (`output/translated.pt-BR.md`) | Phase B4, parallel with visual-enricher |
| `hsb-visual-enricher` | **writer** (`output/enriched.md`) | Phase B4 — renders the Analyst's plan; parallel with translator |
| `hsb-finalizer` | **writer** (`final/<project>-NNN.md`) | Phase B4, parallel with translator/enricher — externalizes the clean, printable final |
| `hsb-packager` | **writer** (`output/manifest.md`) | Phase B4 (wrap) |

### Stage-agnostic agents this skill drives

Named for their function, not for this phase, so later stages can reuse them; the
readiness-package skill is their first consumer.

| Agent | Writer? | When spawned |
|---|---|---|
| `hsb-triage-assessor` | read-only proposer | **Phase A (triage)** — scores the five triage criteria and proposes the routing decision; the gate proposer for Act 1 |
| `hsb-demand-classifier` | read-only proposer | **Phase A (triage)** — proposes the demand-nature / KB classification (born at triage; steers the TA path); runs alongside the Triage Assessor |
| `hsb-stage-inheritor` | read-only proposer | Phase B1, after source-indexer completes — pre-fills inheritable sections from the origination-record (+ the triage outcome) |
| `hsb-section-drafter` | read-only proposer | Phase B2 (draft pass) — proposes `ai_drafted` sections; **fanned out one per `SECTION`** for parallelism |
| `hsb-escalation-flagger` | read-only proposer | Phase B2, once scope and business-rules are drafted |

**`hsb-doc-updater` and `hsb-ledger-writer` are the only writers of
`readiness-document.md` and `qa-log.md` respectively.** All four stage-agnostic
agents above are read-only proposers; they return structured proposals
to the orchestrator, who routes them through the single writers.

## Phase 0 — Select the initiative (you + the PO)

1. **Resolve-or-select the initiative** per
   [`../../origination-brainstorm/references/initiatives.md`](../../origination-brainstorm/references/initiatives.md):
   confirm the latest open initiative or pick one from the open list (closed ones
   omitted). Readiness runs as a **phase of that same initiative**, not a separate
   folder.
2. **Read `initiative.json` and discover the origination-record from the works
   index.** Find the phase whose `produces` is `origination-record` and read its
   `artifacts.canonical` (the humanized copy) — that path is the linked
   origination-record; do not assume `origination/`. Also note `phases.*.owes`
   (debts you may be picking up) and the shared `definitions`. The record must be
   `Product Ready`; if no phase produces an `origination-record`, say so and stop —
   there is nothing to inherit. (A PO may override with an external path.)
3. **Confirm output language.** Default is `pt-BR` (mirrors the origination default).
   Record it; the translator will target this language in Phase B4.

Do not ask a wall of questions at this stage — just select the initiative, confirm
the origination-record, and confirm language. The phase to resolve depends on the
act: Act 1 resolves `intake/`, Act 2 resolves `readiness/`.

## Phase A — Triage (Act 1)

This is the routing gate the documentation calls the PO's first act
(`teamwork-process/personas/02-po.md` §3, §6.1). Full spec: [`triage.md`](triage.md).
It runs on the same engine as Act 2, pointed at the **Intake Record** template.

1. **Resolve-or-resume the `intake/` phase** at `INITIATIVE_DIR/intake/`. Register it
   in `initiative.json.phases` (`started`, `state: active`,
   `consumes: ["origination-record"]`, `produces: "intake-record"`). Seed the brokered
   `PHASE_DIR/glossary.md`. Inject `TEMPLATE = assets/target-template.intake-record.md`,
   `DOC = intake-record.md`.
2. **`hsb-template-validator`** audits the intake template; proceed once it passes.
3. Spawn **in the same turn** (independent → parallel):
   - **`hsb-source-indexer`** indexes the origination-record (the `artifacts.canonical`
     / `final` path from the works index) into `intake/sources/`.
   - **`hsb-template-analyst`** derives `intake/contract.lock.md` from the intake template.
4. Spawn **in the same turn** (read-only, parallel): **`hsb-triage-assessor`** — scores
   the five criteria and proposes the routing decision
   (`verdict`/`rationale`/`basis`/`source`/`reversible`); and **`hsb-demand-classifier`** —
   proposes the demand-nature / KB classification (born at triage, steers the TA path).
   Each flags anything it cannot settle.
5. **Ask the PO only the unsettled criteria** (triage-priority questions, engine
   `open`/`choice` protocol); the PO commits the final routing decision. Route confirmed
   verdicts through **`hsb-ledger-writer`** → **`hsb-doc-updater`** (writes
   `intake-record.md`). Spawn **`hsb-decisions-keeper`** (with `DEFINITIONS_DIR`) to record
   the routing decision in the initiative's `decisions.md` (a cross-phase fact).

### Gate — the routing decision

`triageReady` = all five criteria evaluated. Then the PO's decision routes:

- **`Discovery` / `Backlog` / `Reject`** → finalize the Intake Record (status `Triado`),
  set the `intake` phase `frozen` in `initiative.json`, report the decision + rationale to
  the PO, and **STOP**. Act 2 does not run. (This short-circuit is the primary efficiency
  lever — most demands never pay the rationalization cost.)
- **`Product Ready`** → **resolve-or-resume the `readiness/` phase** at
  `INITIATIVE_DIR/readiness/`, register it
  (`consumes: ["origination-record", "intake-record"]`), seed its brokered glossary, and
  continue to Phase B1.

## Phase B1 — Setup (Act 2)

1. **`hsb-template-validator`** audits the RP template. Proceed only once it
   passes; fix the template if it fails the audit checklist
   ([`../../origination-brainstorm/references/contract-and-template.md`](../../origination-brainstorm/references/contract-and-template.md) § audit checklist).
2. Then spawn **in the same turn** (independent → parallel):
   - **`hsb-source-indexer`** indexes the origination-record (the
     `artifacts.canonical` / `final` path you read from the works index) as the
     primary source **and the intake-record** (`intake/intake-record.md`) so the
     triage decision, validated assumptions, and recognized constraints are visible —
     plus any extra files the PO provides. It writes `readiness/sources/` and
     `sources-index.md`, staying within `PHASE_DIR`.
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
before moving to Phase B2.

## Phase B2 — Draft pass (fan-out)

1. Spawn **`hsb-section-drafter`** **once per product section, all in the same
   turn** (independent → parallel), each injected with a single `SECTION`:
   `business-rules` ∥ `user-journey` (end-to-end happy path + alternative paths) ∥
   `user-stories` (Given/When/Then ACs derived from the journey steps) ∥ `nfrs`
   (ISO/IEC 25010 scaffold) ∥ `edge-cases`. Each is a read-only proposer that reads
   the contract, the inherited entries, and the indexed sources and returns drafts
   for **its one section** at `Origin: ai_drafted`, partial confidence, with a hint.
   Running the drafters concurrently — instead of one drafter doing all five serially
   — is the main lever against slow runs; the single-writer rule keeps it safe.
2. **`hsb-doc-updater`** writes all the `ai_drafted` proposals into
   `readiness-document.md` (serial, single-writer — it drains the fan-out batch in
   one read-modify-write pass keyed by section id).
3. Spawn **`hsb-escalation-flagger`** (read-only) once scope and
   business-rules sections exist. It scans for architectural triggers — carry the
   intake-record's `cto-escalation` early flag as a hint — and proposes the
   `tech-assessment-ref` disposition (see [`escalation.md`](escalation.md)).
   Route its proposal to `hsb-doc-updater`.

At the end of Phase B2 every section has an entry — either `inherited`,
`ai_drafted`, or `discovery` (when the drafter cannot confidently propose) — so
the PO never faces a blank form.

## Phase B3 — Confirm loop (until freezeReady)

Repeats until the freeze gate clears:

1. **`hsb-confidence-auditor`** (read-only) re-scores against the rubric, flags
   conflicts, returns the gap verdict. On the **first** pass it scores every
   section; on later passes inject `SECTIONS` (the ids touched since the last
   audit) so it **re-scores only those**, reusing the prior verdicts you carry
   forward for untouched sections — each loop iteration stays cheap. The auditor's
   verdict is the **single source** of the readiness number (`readiness` + `as-of-rev`):
   `hsb-ledger-writer` persists it in the qa-log header, and `hsb-gap-reporter` /
   `hsb-packager` **quote** it from there — no other agent recomputes the score.
   - In the same turn, spawn **`hsb-integrity-checker`** (read-only, mechanical): it
     verifies the document ends with the sentinel and has no truncation/elision.
     `integrity = fail` is a **hard block** on the gate regardless of the score.
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

Optional: spawn **`hsb-glossary-keeper`** (with `DEFINITIONS_DIR` injected) when
domain terms or cross-phase decisions accumulate (after first confirm rounds and
again before production). It writes the **initiative's** shared `glossary.md` /
`decisions.md`; you then re-seed the brokered `PHASE_DIR/glossary.md`. Terms coined
during readiness become available to later fronts because the store is shared.

## Phase B4 — Production & wrap

Once `freezeReady`:

1. Spawn **in the same turn** (parallel, distinct files):
   - **`hsb-humanizer`** writes `output/humanized.md` — the canonical clean
     copy all production agents read. Then spawn **`hsb-language-auditor`**
     (read-only) to verify it for language leaks (untranslated jargon,
     unlocalized labels, terminology drift, em/en dashes); route any leaks back
     to the Humanizer to fix before the rest read it.
   - **`hsb-enrichment-analyst`** → `output/enrichment-plan.md` — a read-only
     pass over the **settled `readiness-document.md`** (plus the ledger and
     sources) that catalogs every analytical/quantitative visual the data
     **already supports** (scope in/out balance, persona/JTBD map, business-rule
     flow, NFR coverage, metrics with guardrails, confidence-by-section), each
     entry carrying its `Q###`/source citation and an evidence grade. It runs on
     the frozen document, so it is independent of the Humanizer and goes out in
     the same turn. **Separating "what to visualize, from which sourced data"
     from "how to render it" is what makes the enrichment auditable** — this is
     the step whose absence left earlier RPs un-enriched.
   Both must finish before step 2 (the rest read what they write).
2. Then spawn **in the same turn** (parallel, distinct files):
   - **`hsb-translator`** → `output/translated.pt-BR.md` (or the confirmed
     output language).
   - **`hsb-visual-enricher`** → `output/enriched.md` — reads `humanized.md`
     **and `output/enrichment-plan.md`** and **renders the planned visuals**
     (Mermaid-native: `xychart-beta`/`pie`/`radar`/`flowchart`; tables/callouts
     as Markdown), honoring each entry's draft flag and never inventing a number
     the plan did not source. (No plan → legacy fallback, additive visuals only.)
   - **`hsb-finalizer`** → `final/<project>-NNN.md` — the clean, **printable
     final deliverable**. It reads the canonical `output/humanized.md`, strips
     every authoring scaffold (HTML comments + `origination:` annotations, the
     rev/END markers, rubric/guidance blockquotes, and the per-section
     `Confidence/Source/Status/Disposition/Hint` lines), keeps all content and ⚠️
     warnings, and externalizes it under `final/` named `<PROJECT_SLUG>-<NNN>.md`
     (zero-padded per-phase counter; idempotency guard skips a new counter when
     unchanged). Inject `PROJECT_SLUG` (from `initiative.json.project`).
3. **`hsb-packager`** writes `output/manifest.md` noting: freeze state,
   the TA-pending flag (if `tech-assessment-ref` disposition is `deferred`),
   open `discovery` dispositions, template hash/version, the handoff note
   to PRD/PM, and an index entry for the Finalizer's `final/` deliverable.
4. **Record the front in the initiative index.** Update this phase's
   `initiative.json` entry: `state: frozen` (or note a provisional freeze), final
   `readiness`, the `artifacts` paths (incl. `canonical: readiness/output/humanized.md`
   and `final: readiness/final/<project>-NNN.md`),
   `produces: readiness-package`, and — crucially — push the Technical Assessment
   debt into `owes` (e.g. `{ "ref": "TechAssessmentRef", "to": "tech-assessment",
   "status": "deferred" }`). This turns a debt raised inside the RP document into a
   fact the next front reads from the index.
5. Report to the PO: what was produced, the readiness score, the TA flag if
   present, and every item still parked as `discovery` or `deferred`.

## The phase folder layout

The PO's two acts live in two phase folders — `intake/` (Act 1) and `readiness/`
(Act 2) — beside the `origination/` phase they inherit from. The `readiness/` front
exists only when triage decided `Product Ready`:

```
INITIATIVE_DIR/                  # shared by every front
├── initiative.json             # orchestrator — works + definitions index
├── glossary.md                 # Glossary Keeper — shared canonical terms
├── decisions.md                # Glossary Keeper — shared cross-phase decisions (incl. the triage routing decision)
├── origination/                # the upstream front (the origination-record)
├── intake/                     # PHASE_DIR for Act 1 — triage
│   ├── contract.lock.md        # hsb-template-analyst (intake template)
│   ├── sources/                # hsb-source-indexer (the origination-record)
│   ├── qa-log.md               # hsb-ledger-writer
│   └── intake-record.md        # hsb-doc-updater (the routing decision — INT-AAAA-NNN)
└── readiness/                  # PHASE_DIR for Act 2 — rationalization (only if Product Ready)
    ├── contract.lock.md        # hsb-template-analyst
    ├── sources-index.md        # hsb-source-indexer
    ├── sources/                # hsb-source-indexer (incl. inherited origination-record + intake-record)
    ├── qa-log.md               # hsb-ledger-writer
    ├── readiness-document.md   # hsb-doc-updater
    ├── glossary.md             # brokered read-only copy of the initiative glossary
    ├── readiness-report.md     # hsb-gap-reporter (optional)
    ├── output/
    │   ├── humanized.md        # hsb-humanizer
    │   ├── translated.pt-BR.md # hsb-translator
    │   ├── enrichment-plan.md  # hsb-enrichment-analyst — sourced visual catalog (insumo for the Enricher)
    │   ├── enriched.md         # hsb-visual-enricher — renders the plan
    │   └── manifest.md         # hsb-packager
    └── final/                  # hsb-finalizer — clean, printable final deliverable(s)
        └── <project>-NNN.md    # externalized, scaffolding-stripped, counter-suffixed
```
