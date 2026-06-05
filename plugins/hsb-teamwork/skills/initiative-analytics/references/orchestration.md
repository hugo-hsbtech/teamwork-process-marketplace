# Orchestration — the analytics pipeline, roster, and single-writer rule

`initiative-analytics` is a **read-then-report** pipeline, not a capture loop. It
adds nothing to the demand; it **measures** an initiative that the four upstream
skills already produced. You (the orchestrator, Layer 0) resolve the initiative,
spawn read-only collectors that propose findings, and route them to one writer
that emits the report. Same engine, same single-writer discipline as the rest of
the toolkit.

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

## Phase 0.5 — Pricing freshness gate (you, before pricing)

Before any cost is computed, check the price lifecycle (`cost-telemetry.md` §
*Pricing freshness*). Read `PRICING` (`pricing.json`): compute
`age = now − capturedAt` and compare to `ttlHours` (default 48; the human may
override per run).

- **Fresh** (`age ≤ ttlHours`) → use `PRICING` as-is.
- **Stale** (`age > ttlHours`) → **fetch a fresh table first**: invoke the
  bundled **`claude-api`** skill (canonical Current-Models pricing), else
  **WebFetch** `https://platform.claude.com/docs/en/pricing.md`. Rewrite
  `pricing.json`'s `models` with the fresh rates and set `capturedAt` to now (keep
  `ttlHours`). Then proceed.
- **Refresh unavailable** (offline / no source) → do **not** block: proceed with
  the stale table and tell the Reporter to **flag staleness** (show `capturedAt`
  and age) so the USD is used knowingly.

Because the ledger stores **raw tokens**, re-pricing here makes the report reflect
*current* rates regardless of when capture happened — that is the whole point of
the TTL.

## Phase 1 — Collect (parallel, read-only)

Spawn **in the same turn** (independent → parallel):

- **Cost Collector** (`hsb-cost-collector`) — reads `analytics/cost-ledger.jsonl`
  (+ the freshness-checked `PRICING` from Phase 0.5) and returns the §A/§B
  investment aggregates: tokens & USD by phase / agent / model, cache savings,
  durations, spawn counts. **It prices the raw tokens with `PRICING` as the
  authoritative USD** (the row `usd` is only an at-capture snapshot). If the ledger
  is absent, it returns a `notCaptured` verdict with the reason.
- **Metrics Analyst** (`hsb-metrics-analyst`) — reads each phase's `qa-log.md`,
  `contract.lock.md`, the frozen documents, and `initiative.json`, and returns the
  §C/§D process & outcome metrics **and** the §E value score (from the documents,
  per `roi-model.md`).

Both are read-only proposers. They write nothing.

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
| 1 | `hsb-metrics-analyst` | process/outcome metrics + document-derived value score (read-only) |
| 3 | `hsb-roi-reporter` | write `roi-report.md` + `roi.json` (sole writer) |

Run the two collectors **in one turn** (parallel). The Reporter runs after, once
you have composed the ROI set. Add any future capability as its own agent under
the same single-writer rule.

## Modes

- **Single initiative** (default) — analyze one initiative end-to-end.
- **Re-run** — safe and idempotent: re-reading the ledger and re-rendering the
  report merges into the existing `analytics/` files (the hook's watermark keeps
  the ledger itself free of duplicates).

<!-- END OF DOCUMENT -->
