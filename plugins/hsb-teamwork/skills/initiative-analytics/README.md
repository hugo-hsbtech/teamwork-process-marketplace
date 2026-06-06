# `initiative-analytics` — the ROI of an initiative

> Measure what an initiative **cost** end-to-end and the **value** it carries.
> Invoke as `/hsb-teamwork:initiative-analytics` (Claude) or
> `hsb-teamwork-initiative-analytics` (Codex).

The four upstream skills (`origination-brainstorm` → `readiness-package` →
`tech-assessment` → `prd-generation`) *produce* a demand. This skill **measures**
the initiative they produced: how much it cost (tokens, models, USD, time — per
phase and per agent), how the work flowed (questions, rounds, rework), what came
out (readiness, dispositions, triage decision, feasibility verdict), and the
**ROI** that pairs *time × cost × results*.

## How the numbers are captured

- **Cost is measured, not estimated.** A cost-capture **hook**
  (`plugins/hsb-teamwork/hooks/`) fires on `Stop` / `SubagentStop`, reads the
  session transcript's real `usage` (input/output/cache tokens + model), prices it
  via `assets/pricing.json`, and appends consumption blocks to
  `<initiative>/analytics/cost-ledger.jsonl`. The four upstream skills write a tiny
  **session binding** so the hook knows which initiative/phase a session is in.
- **Value is extracted from the documents.** No human types a dollar figure: the
  Metrics Analyst scores declared value (reach, impact, objectives, measurability,
  confidence-of-value) from the frozen documents, as a 0–100 **estimate**.
- **Anything not captured says so.** Missing ledger or an unfrozen phase renders as
  "not captured" with the reason — never a fabricated number.

## The metric catalog

Five families, fully detailed in
[`references/metrics-catalog.md`](references/metrics-catalog.md):

1. **Investment** — tokens & USD by phase/agent/model, cache savings, model mix.
2. **Time** — wall-clock, active compute, human-latency gap, lead time.
3. **Process** — questions, capture-loop rounds, rework, throughput efficiency.
4. **Quality** — readiness, disposition mix, debts, triage decision, verdict.
5. **ROI composites** — cost-to-readiness, **gate savings**, throughput per
   dollar/hour/token, value-anchored ROI (estimate), automation leverage.

## The pipeline

Read-then-report (no capture loop). Resolve-or-select the initiative (closed ones
included), then:

1. **Collect (parallel):** `hsb-cost-collector` (ledger → investment) ∥
   `hsb-metrics-analyst` (documents → process/outcome) ∥ `hsb-value-scorer`
   (documents → value score 0–100).
2. **Compose (you):** the ROI composites, including gate savings vs sibling
   baselines.
3. **Report:** `hsb-roi-reporter` (sole writer) → `analytics/roi-report.md` +
   `analytics/roi.json`.

> Deep dive: [`references/orchestration.md`](references/orchestration.md) ·
> telemetry: [`references/cost-telemetry.md`](references/cost-telemetry.md) ·
> ROI model: [`references/roi-model.md`](references/roi-model.md) · spec:
> [`SKILL.md`](SKILL.md).

## Bundled resources

| Path | Purpose |
|---|---|
| `references/orchestration.md` | pipeline, roster, single-writer rule |
| `references/metrics-catalog.md` | the full metric catalog (five families) |
| `references/cost-telemetry.md` | hook + transcript + ledger schema + pricing |
| `references/roi-model.md` | ROI computation + document-derived value score |
| `assets/pricing.json` | model → USD rates (updatable) |
| `assets/target-template.roi-report.md` (+ `.guide.md`) | the report template |
| `assets/golden-example.md` | calibration exemplar |

The cost-capture hook ships at the plugin root
(`../../hooks/teamwork-cost-capture.py`, registered in `../../hooks/hooks.json`).
