# Orchestration — the analytics pipeline, roster, and single-writer rule

`initiative-analytics` is a **read-then-report** pipeline, not a capture loop. It
adds nothing to the demand; it **measures** an initiative that the four upstream
skills already produced. You (the orchestrator, Layer 0) resolve the initiative,
spawn read-only collectors that propose findings, and route them to one writer
that emits the report. Same engine, same single-writer discipline as the rest of
the toolkit. The validated ordering and the single-writer/single-decider invariants are
declared in [`../pipeline.yaml`](../pipeline.yaml) and checked by
`tools/pipeline_graph.py` (see
[`../../tech-assessment/references/scheduling.md`](../../tech-assessment/references/scheduling.md)).

## The one rule that still holds

**Every mutable file has exactly one writer agent.** Here the only mutable
artifacts are the report files, owned solely by the **ROI Reporter**. Everyone
else is read-only and returns findings you route to it. The cost ledger is
written **only** by the hook (never by an agent).

| Artifact | Sole writer | Everyone else |
|---|---|---|
| `analytics/cost-ledger.jsonl` | the cost-capture **hook** | read-only |
| `analytics/roi-report.md` | ROI Reporter | read-only |
| `analytics/roi.json` | ROI Reporter | read-only |
| `<initiative>/initiative.json` | Orchestrator (you) | read-only |

## Paths are passed in, never hardcoded

Inject into every agent's spawn prompt:

- `SKILL_DIR` — this skill's base directory (told to you at launch).
- `INITIATIVE_DIR` — the resolved initiative root (this skill reads **across all
  phases**, so unlike the upstream skills it is initiative-scoped, not
  phase-scoped — it is a reporting skill, and you are the broker).
- `PRICING` — `SKILL_DIR/assets/pricing.json`.
- `REPORT_DIR` — `INITIATIVE_DIR/analytics/`.

## Resolve-or-select (run first)

Reuse the standard rule from
[`../../origination-brainstorm/references/initiatives.md`](../../origination-brainstorm/references/initiatives.md):
compute `TEAMWORK_ROOT`, list **all** initiatives (for analytics, include
`closed` ones too — you often want the ROI of a finished initiative), and let the
human pick which initiative to analyze (default: latest, or offer the open list +
"pick a closed one"). Read its `initiative.json` to learn the phases, artifacts,
readiness, owes, and the triage/verdict outcomes. There is **no phase folder to
create** — this skill writes only under `INITIATIVE_DIR/analytics/`.

## Phase 1 — Collect (parallel, read-only)

Spawn **in the same turn** (independent → parallel):

- **Cost Collector** (`hsb-cost-collector`) — reads `analytics/cost-ledger.jsonl`
  (+ `PRICING`) and returns the §A/§B investment aggregates: tokens & USD by
  phase / agent / model, cache savings, durations, spawn counts. If the ledger is
  absent, it returns a `notCaptured` verdict with the reason.
- **Metrics Analyst** (`hsb-metrics-analyst`) — reads each phase's `qa-log.md`,
  `contract.lock.md`, the frozen documents, and `initiative.json`, and returns the
  §C/§D process & outcome metrics.
- **Value Scorer** (`hsb-value-scorer`) — reads `initiative.json` and the frozen
  documents and returns the §E value score (0–100, **from the documents only**, per
  `roi-model.md`), each dimension cited to a document line. Split from the Metrics
  Analyst so the value *judgment* is separate from the metric *counting*.

All three are read-only proposers. They write nothing.

## Phase 2 — Compose ROI (you)

Combine the two proposals: pair investment (Cost Collector) against results
(Metrics Analyst) to compute the §E ROI composites per `roi-model.md`
(cost-to-readiness, throughput ratios, value-anchored ROI, **gate savings** when a
gate stopped the chain, automation leverage, cache discipline). For gate savings,
read sibling initiatives' `analytics/roi.json` (or the configured baseline) to get
the comparable full-run baseline. Hand the assembled metric set to the writer.

## Phase 3 — Report (single writer)

- **ROI Reporter** (`hsb-roi-reporter`) — sole writer. Renders
  `analytics/roi-report.md` from `SKILL_DIR/assets/target-template.roi-report.md`
  (and its guide), and the machine-readable `analytics/roi.json`. It obeys
  `../../origination-brainstorm/references/writing-integrity.md` (read-modify-write,
  no truncation, END sentinel on the `.md`). It labels every value-derived number
  `estimate`, marks `notCaptured` families honestly, and cites each metric's
  source family.

Then **you** present the human the headline: total USD, tokens, model mix, lead
time, final readiness, the ROI panel, gate savings if any, and the outstanding
debts/parked dispositions. Offer the report path.

## The roster (each a standalone agent)

| Phase | `subagent_type` | Role |
|---|---|---|
| 1 | `hsb-cost-collector` | aggregate the cost ledger → investment metrics (read-only) |
| 1 | `hsb-metrics-analyst` | process/outcome metrics (read-only) |
| 1 | `hsb-value-scorer` | document-derived value score 0–100 (read-only) |
| 3 | `hsb-roi-reporter` | write `roi-report.md` + `roi.json` (sole writer) |

Run the three collectors **in one turn** (parallel). The Reporter runs after, once
you have composed the ROI set. Add any future capability as its own agent under
the same single-writer rule.

## Modes

- **Single initiative** (default) — analyze one initiative end-to-end.
- **Re-run** — safe and idempotent: re-reading the ledger and re-rendering the
  report merges into the existing `analytics/` files (the hook's watermark keeps
  the ledger itself free of duplicates).

<!-- END OF DOCUMENT -->
