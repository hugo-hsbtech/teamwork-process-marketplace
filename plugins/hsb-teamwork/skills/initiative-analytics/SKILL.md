---
name: initiative-analytics
description: >-
  Measure the end-to-end ROI of an initiative — what it cost to take a demand from
  raw signal to a PRD, and the value it carries. Reads the cost telemetry captured
  automatically by the cost-capture hook (tokens, models used, USD, time — per
  phase and per agent) together with the structured artifacts the upstream skills
  produced (initiative.json, qa-logs, frozen documents, dispositions, triage
  decision, feasibility verdict) and renders a per-initiative ROI report:
  investment (tokens/models/USD/time), process & throughput, quality & outcome,
  and ROI composites that pair time × cost × results (cost-to-readiness, gate
  savings, throughput-per-dollar/hour/token, and a value-anchored ROI whose value
  side is EXTRACTED FROM THE DOCUMENTS). Use this skill WHENEVER someone wants to
  know the ROI, cost, token/model consumption, time spent, or efficiency of an
  initiative or its phases — "how much did this initiative cost", "what's the ROI",
  "tokens/models/time per process", "analytics per initiative". It invents no
  numbers: cost is measured from the transcript, value is extracted from the
  documents and labeled estimate, and anything not captured renders as
  "not captured" rather than guessed. Portable and template-driven; mirrors the
  initiative's language (e.g. pt-BR).
user-invocable: true
---

# Initiative Analytics (orchestrator)

You are **Layer 0 — the orchestrator**, and the *only* layer that talks to the
human. This skill is **read-then-report**: it adds nothing to the demand, it
**measures** an initiative the four upstream skills already produced. You resolve
the initiative, spawn read-only collectors that propose findings, compose the ROI
composites, and route everything to one writer that emits the report. Heavy work
is delegated so your context stays lean.

This skill is **portable and repo-independent**. Everything it needs is bundled
here. Pass paths into agents; never let them assume a location.

## First, read these (once per run)

- [`references/orchestration.md`](references/orchestration.md) — the pipeline, the
  roster, the single-writer rule, what runs in parallel. Your playbook.
- [`references/metrics-catalog.md`](references/metrics-catalog.md) — the
  authoritative catalog of every metric, in five families (investment, time,
  process, quality, ROI composites). **The heart of this skill.**
- [`references/cost-telemetry.md`](references/cost-telemetry.md) — how tokens /
  models / time are captured (the hook + transcript), the session binding, the
  cost-ledger schema, and pricing.
- [`references/roi-model.md`](references/roi-model.md) — how ROI is computed and
  how the value score is **extracted from the documents** (no human-entered
  dollars).
- [`../origination-brainstorm/references/initiatives.md`](../origination-brainstorm/references/initiatives.md)
  — the initiative model, `.teamwork/` layout, the session binding, and
  resolve-or-select.
- [`../origination-brainstorm/references/writing-integrity.md`](../origination-brainstorm/references/writing-integrity.md)
  — the no-truncation + read-modify-write rules the Reporter obeys.

## The principle that still holds

**One writer per file.** The report files (`analytics/roi-report.md`,
`analytics/roi.json`) have exactly one writer — the **ROI Reporter**. The cost
ledger is written **only by the hook**, never by an agent. Everything else is
read-only and returns proposals you route to the writer.

## Where the numbers come from (do not fabricate)

- **Cost / tokens / models / time** are **measured** by the cost-capture hook from
  the session transcript and stored in `analytics/cost-ledger.jsonl`. You read
  that ledger; you never estimate tokens yourself.
- **Value** is **extracted from the frozen documents** (reach, impact, objectives,
  metrics) as a 0–100 score, labeled **estimate**. There is no "type a dollar
  figure" prompt.
- **Anything not captured** (no ledger, a phase that never froze) renders as
  **"not captured"** with the reason — never a guessed value.

## The flow (summary — full detail in `orchestration.md`)

1. **Resolve-or-select** the initiative to analyze. Unlike the upstream skills,
   include **closed** initiatives in the list (you often want the ROI of a
   finished one). Read its `initiative.json` for phases, artifacts, readiness,
   owes, triage decision, and feasibility verdict. This skill is
   **initiative-scoped** (reads across all phases); it writes only under
   `INITIATIVE_DIR/analytics/`.
2. **Phase 1 — Collect (parallel, same turn):** spawn `hsb-cost-collector`
   (ledger → investment §A/§B) ∥ `hsb-metrics-analyst` (qa-logs + documents +
   `initiative.json` → process/outcome §C/§D + the document-derived value score
   §E). Both read-only.
3. **Phase 2 — Compose ROI (you):** pair investment against results to compute the
   §E composites per `roi-model.md` — cost-to-readiness, throughput per
   dollar/hour/token, value-anchored ROI (estimate), **gate savings** when a gate
   stopped the chain early, automation leverage, cache discipline. For gate
   savings, read sibling initiatives' `roi.json` (or the configured baseline) for
   the comparable full-run cost.
4. **Phase 3 — Report (single writer):** spawn `hsb-roi-reporter` to render
   `analytics/roi-report.md` (from the bundled template) and `analytics/roi.json`.
   Then report the headline to the human: total USD, tokens, model mix, lead time,
   final readiness, the ROI panel, gate savings if any, and outstanding
   debts/parked dispositions.

## The agents you spawn (`subagent_type`)

| Phase | `subagent_type` | Role |
|---|---|---|
| 1 | `hsb-cost-collector` | aggregate `cost-ledger.jsonl` (+ `PRICING`) → investment & time metrics (read-only) |
| 1 | `hsb-metrics-analyst` | process/outcome metrics + document-derived value score (read-only) |
| 3 | `hsb-roi-reporter` | write `analytics/roi-report.md` + `analytics/roi.json` (sole writer) |

When spawning, inject: `SKILL_DIR` (told to you at launch), `INITIATIVE_DIR`,
`PRICING` (= `SKILL_DIR/assets/pricing.json`), and `REPORT_DIR`
(= `INITIATIVE_DIR/analytics/`). **Run the two collectors in the same turn** so
they execute in parallel.

## Execution invariants

1. **Delegation is mandatory.** "Run the analytics" means *spawn the collectors
   and the reporter*. Do not parse the ledger and write the report inline.
2. **The two collectors go out in ONE message** (independent → parallel).
3. **Never write tokens you didn't measure.** Read the ledger; if it is absent,
   render the cost families as "not captured".
4. **Track the run with TodoWrite** before Phase 1.

### The phase checklist (TodoWrite this before Phase 1)

- [ ] Resolve-or-select the initiative (closed allowed); read `initiative.json`
- [ ] Phase 1 · **same message:** `hsb-cost-collector` ∥ `hsb-metrics-analyst`
- [ ] Phase 2 · compose the ROI composites (gate savings via sibling baselines)
- [ ] Phase 3 · spawn `hsb-roi-reporter`; report the headline to the human

## Language

Mirror the initiative's language (from `initiative.json.language`; default the
human's). Keep the report structure identical across languages.

## Installing in other projects

This skill ships in the **`hsb-teamwork` plugin**. Install from the `hsb-tech`
marketplace and invoke as `/hsb-teamwork:initiative-analytics`. The cost-capture
hook ships with the plugin (`hooks/hooks.json`) and registers automatically; the
four upstream skills write the session binding the hook needs. A Codex adapter
lives at the plugin's `codex/`.

## Bundled resources

| Path | Purpose |
|---|---|
| `references/orchestration.md` | pipeline, roster, single-writer rule |
| `references/metrics-catalog.md` | the full metric catalog (five families) |
| `references/cost-telemetry.md` | hook + transcript + ledger schema + pricing |
| `references/roi-model.md` | ROI computation + document-derived value score |
| `assets/pricing.json` | model → USD rates (updatable) |
| `assets/target-template.roi-report.md` | the report template (annotated) |
| `assets/target-template.roi-report.guide.md` | companion filling guide |
| `assets/golden-example.md` | calibration exemplar |
