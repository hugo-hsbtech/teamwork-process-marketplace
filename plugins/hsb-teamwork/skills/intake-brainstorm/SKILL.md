---
name: intake-brainstorm
description: >-
  Orchestrate a multi-agent pipeline that turns a raw Submitter description (a
  sentence, a paragraph, and/or referenced files) into a fully-filled target
  document, by running a confidence-driven brainstorming loop and then producing
  humanized, translated, and visually-enriched variants. Use this skill WHENEVER
  someone wants to capture, intake, triage, formalize, or "write up" a new demand
  / request / feature idea / pain / opportunity into a structured document - even
  if they don't say "intake" by name. Also use it to REVISIT an existing filled
  document (re-score sections, find gaps, re-open questions) or to BATCH-process a
  pile of raw signals into draft documents without a live interview. The target
  document is defined by a bundled, swappable template; the skill is portable and
  user-scoped (no dependency on any particular repository). Works in en-US by
  default and mirrors / translates to the requested language (e.g. pt-BR).
user-invocable: true
---

# Intake Brainstorm (orchestrator)

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
- [`references/sessions.md`](references/sessions.md) — where session state lives,
  and the resolve-or-resume rule so re-runs reuse work instead of duplicating it.

## The principle that makes parallelism safe

**One writer per file.** Each mutable artifact has exactly one writer agent; every
other agent is read-only and returns *proposals/findings/verdicts* that **you**
route to the single writer. Concurrent writes are impossible by construction. The
ownership table is in `orchestration.md`.

## The agents you spawn (`subagent_type`)

| Phase | `subagent_type` | Role |
|---|---|---|
| 1 | `intake-template-validator` | validate the template (read-only); run before the Analyst |
| 1 | `intake-source-indexer` | normalize referenced files into `sources/` |
| 1 | `intake-template-analyst` | derive `contract.lock.md`, hash, restart-on-change |
| 2 | `intake-question-strategist` | propose the next questions (read-only) |
| 2 | `intake-file-extraction` | propose answers from files (read-only) |
| 2 | `intake-reconciler` | resolve conflicting evidence (read-only) |
| 2 | `intake-ledger-writer` | commit questions/answers to `qa-log.md` |
| 2 | `intake-doc-updater` | fill `target-document.md` |
| 2 | `intake-glossary-keeper` | maintain canonical terms in `glossary.md` |
| 2 | `intake-readiness-reporter` | write the live gap map `readiness-report.md` |
| 2 | `intake-confidence-auditor` | re-score + gate verdict (read-only) |
| 3 | `intake-humanizer` | write `output/humanized.md` |
| 3 | `intake-translator` | write `output/translated.<lang>.md` |
| 3 | `intake-visual-enricher` | write `output/enriched.md` |
| 4 | `intake-packager` | write `output/manifest.md` |

When spawning, inject the paths each agent needs: `SKILL_DIR` (this skill's base
directory, which you are told at launch), `SESSION_DIR`, `TEMPLATE`, and the
template's companion guide if one exists. **Run independent agents in the same
turn** so they execute in parallel (Indexer ∥ Analyst; Strategist ∥ Extraction;
Translator ∥ Enricher).

## Modes

**Fresh** (default) — opening statement, maybe files, no document yet. Run the
full pipeline.

**Revisit** — the input points at an existing filled document. Have the Analyst
build the contract, then the Auditor re-score the existing document, report the
gap map to the human, and re-open questions only on the weak sections. Bump the
version when you re-write.

**Batch / headless** — a set of raw signals (a folder of briefs/tickets) and no
live human. For each, run Phase 1 + the *no-question* path: File Extraction
proposes, Ledger Writer commits, Doc Updater fills, Auditor scores. Truly-unknown
blocking fields land as honest `assumption`/`discovery` dispositions rather than
real answers, so batch output is always "draft for review," never `gateReady` on
its own. Produce one session folder per signal; these runs are embarrassingly
parallel.

## Language

Detect the language of the opening statement and mirror it for the conversation
and the captured document. Default en-US when ambiguous. The Translator produces
any additional requested languages as separate `output/` files. Keep section
*structure* identical across languages.

## The flow (summary — full detail in `orchestration.md`)

1. **Phase 0 (you + human):** collect statement, file refs, output language(s),
   optional custom `TEMPLATE`; pick the mode; then **resolve-or-resume** the
   session — anchor `SESSION_ROOT` at the project (git) root, not the cwd, and if
   `SESSION_ROOT/<demand-slug>/` already exists, **resume it** instead of creating
   a duplicate. See [`references/sessions.md`](references/sessions.md).
2. **Phase 1 (parallel, gate):** spawn Indexer ∥ Analyst. Contract must exist before
   looping; a changed template hash restarts analysis.
3. **Phase 2 (loop):** Strategist ∥ Extraction propose → Ledger Writer commits →
   you ask the human the still-open questions → Ledger Writer records answers
   (answers may spawn follow-ups) → Doc Updater fills → Auditor scores. Loop until
   every blocking section is ≥ its `min-confidence` or honestly disposed.
4. **Phase 3 (isolated, parallel variants):** Humanizer writes the canonical clean
   copy; then Translator ∥ Enricher each read it and write their own file.
5. **Phase 4:** Packager writes the manifest. You report: artifacts produced,
   readiness score, and every item parked as assumption/discovery/deferred.

## Installing in other projects

This skill ships as the **`hsb-teamwork` Claude Code plugin** (this folder
is `plugins/hsb-teamwork/skills/intake-brainstorm/` inside it). Install it
from the `hsb-tech` marketplace — no copying, versioned, namespaced:

```
/plugin marketplace add hugo-hsbtech/teamwork-process-marketplace
/plugin install hsb-teamwork@hsb-tech
```

Invoke it as `/hsb-teamwork:intake-brainstorm`.

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
| `references/sessions.md` | session location, resolve-or-resume, cross-run idempotency |
| `assets/target-template.intake-record.md` | default target template (annotated) |
| `assets/target-template.intake-record.guide.md` | companion filling guide (incl. triage drafting) |
| `assets/golden-example.md` | self-contained calibration exemplar |
