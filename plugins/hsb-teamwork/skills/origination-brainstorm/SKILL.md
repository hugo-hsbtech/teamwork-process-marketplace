---
name: origination-brainstorm
description: >-
  Orchestrate a multi-agent pipeline that turns a raw Submitter description (a
  sentence, a paragraph, and/or referenced files) into a fully-filled target
  document, by running a confidence-driven brainstorming loop and then producing
  humanized, translated, and visually-enriched variants. Use this skill WHENEVER
  someone wants to capture, originate, triage, formalize, or "write up" a new demand
  / request / feature idea / pain / opportunity into a structured document - even
  if they don't say "origination" by name. Also use it to REVISIT an existing filled
  document (re-score sections, find gaps, re-open questions) or to BATCH-process a
  pile of raw signals into draft documents without a live interview. The target
  document is defined by a bundled, swappable template; the skill is portable and
  user-scoped (no dependency on any particular repository). Works in en-US by
  default and mirrors / translates to the requested language (e.g. pt-BR).
user-invocable: true
---

# Origination Brainstorm (orchestrator)

You are **Layer 0 — the orchestrator**, and the *only* layer that talks to the
human. You do not fill the document yourself; you **collect information, spawn
specialized subagents with exactly what they need, route their outputs, and keep
the human in the loop**. Heavy work is delegated so your context stays lean.

This skill is **portable and repo-independent**. Everything it needs is bundled
here. Pass paths into agents; never let them assume a location.

## First, read these (once per run)

- [`references/orchestration.md`](references/orchestration.md) — the phase flow,
  the agent roster, the single-writer guarantee, and what runs in parallel. This
  is your playbook.
- [`references/contract-and-template.md`](references/contract-and-template.md) —
  how the target template becomes the contract, the confidence threshold X, and
  the restart-on-change rule.
- [`references/ledger-schema.md`](references/ledger-schema.md) — the Q&A ledger
  format.
- [`references/questioning-method.md`](references/questioning-method.md) — how to
  ask (you run the human-facing questions).
- [`references/grounding.md`](references/grounding.md) — the quality bar.
- [`references/writing-integrity.md`](references/writing-integrity.md) — the
  no-truncation + serialize/queue/merge/conflict rules every writer obeys.
- [`references/localization.md`](references/localization.md) — the single source of
  truth for "no language leaks": leak taxonomy, token map, verbatim allowlist, and the
  derived-telemetry line break, enforced by the Language Auditor.
- [`references/initiatives.md`](references/initiatives.md) — what an initiative is,
  where its state lives, the `.teamwork/` layout with per-front phase folders, and
  the resolve-or-select rule so re-runs reuse work instead of duplicating it.

## The principle that makes parallelism safe

**One writer per file.** Each mutable artifact has exactly one writer agent; every
other agent is read-only and returns *proposals/findings/verdicts* that **you**
route to the single writer. Concurrent writes are impossible by construction. The
ownership table is in `orchestration.md`.

## Execution invariants (read before Phase 1)

This file reads like a description; it is an **execution contract**. The dominant
failure modes are (a) reading the pipeline and then filling the document yourself
inline — a correct run has Agent calls in the transcript — and (b) spawning agents
one at a time and awaiting each, which is what makes a run drag. Bind yourself to:

1. **Delegation is mandatory.** "Run the pipeline" means *spawn the subagents*. Never
   read the template and fill it in yourself.
2. **Independent agents go out in ONE message.** When two agents have no dependency,
   emit both Agent calls in the **same assistant turn** so they run concurrently. The
   parallel pairs are: Phase 1 `hsb-source-indexer` ∥ `hsb-template-analyst`;
   Phase 2 `hsb-question-strategist` ∥ `hsb-evidence-extractor`, and
   `hsb-gap-reporter` ∥ `hsb-glossary-keeper` when both are due;
   Phase 3 `hsb-humanizer` ∥ `hsb-enrichment-analyst`, then `hsb-visual-enricher` ∥
   `hsb-citation-resolver` ∥ `hsb-translator`. The `hsb-finalizer` runs **last**,
   alone: it consumes the enriched copy and the Citation Resolver's appendix, so it
   is a chain, not a sibling of the variants.
3. **Audit incrementally.** After the first full audit, spawn the
   `hsb-confidence-auditor` with `SECTIONS` = the ids touched since the last pass, so
   it re-scores only those and carries the rest forward. Re-grading a settled
   document every iteration is the main avoidable cost in a long run.
4. **Track the run with TodoWrite.** Create the checklist below *before* Phase 1; this
   is the mechanism that stops a multi-agent run from collapsing into serial,
   one-at-a-time spawns.

### The phase checklist (TodoWrite this before Phase 1)

- [ ] Phase 1 · spawn `hsb-template-validator`; gate on pass
- [ ] Phase 1 · **same message:** `hsb-source-indexer` ∥ `hsb-template-analyst`
- [ ] Phase 2 · loop: **same message** `hsb-question-strategist` ∥ `hsb-evidence-extractor` → `hsb-ledger-writer` → ask human → `hsb-ledger-writer` → `hsb-doc-updater` (+ `hsb-synthesizer` for derived) → `hsb-confidence-auditor` (incremental `SECTIONS`) until the gate clears
- [ ] Phase 2.5 · refresh `hsb-gap-reporter`; classify residuals; **ask the human** (close gaps now / pick items / ship as draft) before producing
- [ ] Phase 3 · **same message:** `hsb-humanizer` ∥ `hsb-enrichment-analyst` (await — they write what the rest read)
- [ ] Phase 3 · **same message:** `hsb-visual-enricher` (reads plan) ∥ `hsb-citation-resolver` ∥ `hsb-translator`
- [ ] Phase 3 · then `hsb-finalizer` (reads `enriched.md` + Citation Resolver appendix/links; last in the chain)
- [ ] Phase 4 · spawn `hsb-packager`; record the front in `initiative.json`; report to the human

## The agents you spawn (`subagent_type`)

| Phase | `subagent_type` | Role |
|---|---|---|
| 1 | `hsb-template-validator` | validate the template (read-only); run before the Analyst |
| 1 | `hsb-source-indexer` | normalize referenced files into `sources/` |
| 1 | `hsb-template-analyst` | derive `contract.lock.md`, hash, restart-on-change |
| 2 | `hsb-question-strategist` | propose the next questions (read-only) |
| 2 | `hsb-evidence-extractor` | propose answers from files (read-only) |
| 2 | `hsb-reconciler` | resolve conflicting evidence (read-only) |
| 2 | `hsb-ledger-writer` | commit questions/answers to `qa-log.md` |
| 2 | `hsb-doc-updater` | fill `target-document.md` (`DOC`) |
| 2 | `hsb-synthesizer` | compose `derived` sections (exec summary, triage draft) for the Doc Updater (read-only) |
| 2 | `hsb-glossary-keeper` | maintain the initiative's shared `glossary.md` — canonical terms (sole writer) |
| 2 | `hsb-decisions-keeper` | maintain the initiative's shared `decisions.md` — cross-phase decisions (sole writer) |
| 2 | `hsb-gap-reporter` | write the live gap map `readiness-report.md` |
| 2 | `hsb-confidence-auditor` | re-score + gate verdict (read-only) |
| 3 | `hsb-humanizer` | write `output/humanized.md` (localizes labels/headings, purges untranslated jargon) |
| 3 | `hsb-enrichment-analyst` | catalog visual/analytics opportunities into `output/enrichment-plan.md` (read-only proposer) |
| 3 | `hsb-translator` | write `output/translated.<lang>.md` |
| 3 | `hsb-visual-enricher` | render the plan's visuals into `output/enriched.md` |
| 3 | `hsb-citation-resolver` | propose the "Sources & question log" appendix + reference-link map (read-only) |
| 3 | `hsb-finalizer` | externalize the clean, **enriched**, link-traceable final `final/<project>-NNN.md` |
| 4 | `hsb-packager` | write `output/manifest.md` |

When spawning, inject the paths each agent needs: `SKILL_DIR` (this skill's base
directory, which you are told at launch), `PHASE_DIR`, `TEMPLATE`, `DOC` (the
target document's filename — `target-document.md` for this skill), and the
template's companion guide if one exists. The **Finalizer** also needs
`PROJECT_SLUG` (from `initiative.json.project`) to name the externalized
deliverable. **Run independent agents in the same turn** so they execute in
parallel (Indexer ∥ Analyst; Strategist ∥ Extraction; Humanizer ∥ Enrichment
Analyst; then Enricher ∥ Citation Resolver ∥ Translator). The Finalizer runs last,
alone, consuming the enriched copy + the Citation Resolver's appendix.

**You are the broker for everything above `PHASE_DIR`.** The three initiative-level
files — `initiative.json` (the works + definitions index), `glossary.md`, and
`decisions.md` — are yours; agents stay `PHASE_DIR`-scoped. So: seed each phase's
read-only `PHASE_DIR/glossary.md` from the initiative store before spawning readers;
spawn the **Glossary Keeper** with `DEFINITIONS_DIR` (= `INITIATIVE_DIR`) injected,
since it is the sole writer of the shared store; and update each phase's
`initiative.json` entry when the front starts and when it freezes. Full rules in
[`references/initiatives.md`](references/initiatives.md).

## Modes

**Fresh** (default) — opening statement, maybe files, no document yet. Run the
full pipeline.

**Revisit** — the input points at an existing filled document. Have the Analyst
build the contract, then the Auditor re-score the existing document, report the
gap map to the human, and re-open questions only on the weak sections. Bump the
version when you re-write.

**Batch / headless** — a set of raw signals (a folder of briefs/tickets) and no
live human. For each, run Phase 1 + the *no-question* path: Evidence Extractor
proposes, Ledger Writer commits, Doc Updater fills, Auditor scores. Truly-unknown
blocking fields land as honest `assumption`/`discovery` dispositions rather than
real answers, so batch output is always "draft for review," never `gateReady` on
its own. Produce one initiative per signal (its own `origination/` phase); these
runs are embarrassingly parallel.

## Language

Detect the language of the opening statement and mirror it for the conversation
and the captured document. Default en-US when ambiguous. The Translator produces
any additional requested languages as separate `output/` files. Keep section
*structure* identical across languages.

## The flow (summary — full detail in `orchestration.md`)

1. **Phase 0 (you + human):** collect statement, file refs, output language(s),
   optional custom `TEMPLATE`; pick the mode; then **resolve-or-select** the
   initiative — anchor `TEAMWORK_ROOT` at the project (git) root + `/.teamwork`,
   not the cwd; confirm the latest open initiative or pick from the open list (or
   start a new one); **read `initiative.json`** to become aware of what prior fronts
   defined, produced, and owe; then resolve its origination
   `PHASE_DIR = INITIATIVE_DIR/origination/`, resuming it if it already exists
   instead of creating a duplicate, registering the phase in the index, and seeding
   the brokered `glossary.md`. See [`references/initiatives.md`](references/initiatives.md).
2. **Phase 1 (parallel, gate):** spawn Indexer ∥ Analyst. Contract must exist before
   looping; a changed template hash restarts analysis.
3. **Phase 2 (loop):** Strategist ∥ Extraction propose (same turn) → Ledger Writer
   commits → you ask the human the still-open questions → Ledger Writer records
   answers (answers may spawn follow-ups) → Doc Updater fills → Auditor scores
   (full on the first pass, then only the touched `SECTIONS`). Loop until every
   blocking section is ≥ its `min-confidence` or honestly disposed.
4. **Phase 2.5 (checkpoint, you + human):** the gate clearing is not "the human is
   done." Refresh the Gap Reporter, **classify each residual** as Submitter-closeable
   vs downstream-owner, and **ask the human** what to do — *close the gaps now*
   (recommended; re-enter the loop on Submitter-closeable residuals to maximize
   readiness), *pick specific items*, or *ship as draft for review*. Only then
   produce. Never silently ship residual drafts the human never chose to keep.
5. **Phase 3 (isolated, a chain into the deliverable):** Humanizer ∥ Enrichment
   Analyst run first (the Humanizer writes the canonical clean copy and localizes
   labels/headings + purges untranslated jargon; the Analyst writes
   `output/enrichment-plan.md`, the sourced catalog of visuals). Then Visual Enricher
   (renders the plan into `output/enriched.md`) ∥ Citation Resolver (proposes the
   provenance appendix + reference-link map) ∥ Translator. Finally the **Finalizer**
   externalizes the **printable final deliverable** under `final/<project>-NNN.md`:
   it reads the **enriched** copy (so visuals survive), strips authoring scaffold
   (HTML comments and `origination:` annotations, the rev/END markers, rubric/guidance
   blockquotes, and the `<!-- VISUAL ... -->` comments) **but keeps every Mermaid
   block and summary table**, **relocates** each Provenance block into the appendix
   and applies the reference links, keeps all content and ⚠️ warnings, and
   counter-suffixes the name (idempotency guard skips a new counter when unchanged).
6. **Phase 4:** Packager writes the manifest (indexing the `final/` deliverable
   too); then **you record the front in the initiative index** — set its
   `initiative.json` entry to `state: frozen` with the final `readiness`, the
   `artifacts` paths (incl. the canonical humanized copy and the printable
   `final` deliverable), `produces: origination-record`, and any `owes`. You
   report: artifacts produced, readiness score, and every item parked as
   assumption/discovery/deferred.

## Installing in other projects

This skill ships as the **`hsb-teamwork` Claude Code plugin** (this folder
is `plugins/hsb-teamwork/skills/origination-brainstorm/` inside it). Install it
from the `hsb-tech` marketplace — no copying, versioned, namespaced:

```
/plugin marketplace add hugo-hsbtech/teamwork-process-marketplace
/plugin install hsb-teamwork@hsb-tech
```

Invoke it as `/hsb-teamwork:origination-brainstorm`.

The plugin is self-contained (template, companion guide, and exemplar bundled
under `assets/`), so no repository content is required at runtime. A Codex adapter
lives alongside at the plugin's `codex/` (see its README). See the plugin
[`README.md`](README.md) for the full layout.

## Bundled resources

| Path | Purpose |
|---|---|
| `references/orchestration.md` | phase flow, roster, single-writer rule |
| `references/contract-and-template.md` | template→contract, threshold X, restart |
| `references/ledger-schema.md` | `qa-log.md` format |
| `references/questioning-method.md` | how to ask, dispositions, tensions |
| `references/grounding.md` | quality bar + pointer to the exemplar |
| `references/writing-integrity.md` | no-truncation + queue/merge/conflict rules for writers |
| `references/initiatives.md` | initiative model, `.teamwork/` + phase-folder layout, the works+definitions index (`initiative.json`), shared definitions (`glossary.md`/`decisions.md`), brokering, resolve-or-select, cross-run idempotency |
| `assets/target-template.origination-record.md` | default target template (annotated) |
| `assets/target-template.origination-record.guide.md` | companion filling guide (incl. triage drafting) |
| `assets/golden-example.md` | self-contained calibration exemplar |
