<!--
TARGET TEMPLATE · Initiative ROI Report (default)
This is a RENDERED report, not a capture contract — the ROI Reporter fills it from
the composed metric set (Cost Collector + Metrics Analyst + the orchestrator's ROI
composites). There is no confidence gate and no blocking sections; instead each
section names exactly what to render and from which source family.

Provenance tags: [ledger] = measured by the cost-capture hook; [artifact] = read
from initiative.json / qa-log / frozen documents. Every value-derived number
(value score, value-anchored ROI) is labeled `estimate`. Anything missing renders
as "not captured (<reason>)" — never a fabricated number.

Render in the initiative's language (initiative.json.language). End with the
<!-- END OF DOCUMENT --> sentinel. See references/metrics-catalog.md and roi-model.md.
To customize, copy this file and pass it as TEMPLATE.
-->

# Initiative ROI — [project] · [initiative name]
<!-- rev: 0 · updated: YYYY-MM-DD -->

> End-to-end analytics for this initiative: what it **cost** to take the demand
> from raw signal toward a PRD (tokens, models, USD, time — measured) and the
> **value** it carries (extracted from the documents, estimate-grade). Cost is
> measured; value is an estimate; anything not captured says so.

## 1 · Header
<!-- id=header; source=[ledger]+[artifact] -->

| Field | Value |
|---|---|
| **Initiative** | `<name>` · project `<project>` |
| **Status** | open \| closed |
| **Language** | `<lang>` |
| **Phases reached** | origination → readiness → assessment → prd → delivered-to-pm |
| **Lead time** | `<first started → last finishedAt>` (`<calendar duration>`) [artifact] |
| **Total cost** | **US$ `<sum>`** [ledger] |
| **Total tokens** | `<sum>` (in `<n>` · out `<n>` · cache-read `<n>`) [ledger] |
| **Model mix** | `<model: %tokens / %USD>` … [ledger] |
| **Final readiness** | `<furthest phase readiness>` / 100 [artifact] |

## 2 · Per-phase breakdown
<!-- id=phases; source=[ledger]+[artifact]; one row per phase -->

| Phase | Wall-clock | Tokens | US$ | Spawns | Rounds | Readiness | Outcome | Dispositions (real / assm / disc / def) |
|---|---|---|---|---|---|---|---|---|
| origination | `<h:mm>` | `<n>` | `<$>` | `<n>` | `<n>` | `<NN>` | — | `<%/%/%/%>` |
| readiness | … | … | … | … | … | … | triage: `<Product Ready/…>` | … |
| assessment | … | … | … | … | … | … | verdict: `<feasible/…/vetoed>` | … |
| prd | … | … | … | … | … | … | `<delivered-to-pm / halted>` | … |

> Mark any phase that never froze, or any phase with no ledger rows, as
> **not captured (<reason>)** in the affected cells.

## 3 · Cost drivers
<!-- id=drivers; source=[ledger] -->

- **Top agents by US$:** `<role — $ — % of total>` … (per-agent split is
  best-effort; orchestrator vs subagent is exact).
- **Top models by US$:** `<model — $ — % of total>` …
- **Cache discipline:** cache-hit ratio `<NN%>`; **cache savings** US$ `<sum>`
  (vs paying cache-reads at the input rate).
- **Automation leverage:** active compute `<h:mm>` ÷ wall-clock `<h:mm>` = `<ratio>`
  (the rest was human/async latency).

## 4 · ROI panel
<!-- id=roi; source=[ledger]+[artifact]; value side = estimate -->

| Composite | Value | Source |
|---|---|---|
| **Cost-to-readiness** | US$ `<x>` / readiness pt | [ledger]+[artifact] |
| **Throughput — per dollar** | `<readiness/$>` | [ledger]+[artifact] |
| **Throughput — per hour** | `<readiness/h>` | [ledger]+[artifact] |
| **Throughput — per Mtok** | `<readiness/Mtok>` | [ledger]+[artifact] |
| **Value-anchored ROI** | `<%>` · **estimate** | value [artifact] ÷ cost [ledger] |
| **Gate savings** | US$ `<x>` *(only if a gate stopped the chain)* | [ledger]+[artifact] |

### Value breakdown (extracted from the documents · estimate)
<!-- id=value; source=[artifact]; cite each dimension -->

| Dimension | Weight | Score | Justification → citation |
|---|---|---|---|
| Reach | 25 | `<0–100>` | `<…>` → `<doc:line>` |
| Impact / pain severity | 30 | `<0–100>` | `<…>` → `<doc:line>` |
| Strategic objectives | 20 | `<0–100>` | `<…>` → `<doc:line>` |
| Measurability | 15 | `<0–100>` | `<…>` → `<doc:line>` |
| Confidence-of-value | 10 | `<0–100>` | `<discount for assumption/deferred>` |
| **Value score** | — | **`<weighted 0–100>`** | estimate-grade |

> **Gate savings story** (when present): triage routed to `<Reject/Backlog/Discovery>`
> (or the TA was `vetoed`) before the expensive phases, spending US$ `<actual>` and
> **avoiding ≈ US$ `<baseline − actual>`** vs a comparable full origination→prd run
> (`baseline = <median of completed siblings | configured default>`). The gate paid
> for itself.

## 5 · Open items
<!-- id=open; source=[artifact] -->

- **Outstanding debts (`owes`):** `<ref → to → status>` … (or — none).
- **Parked dispositions (carried risk):** every `assumption` / `discovery` /
  `deferred` still open, by phase and section.
- **Not captured:** the metric families that could not be computed, with the
  reason (e.g. "no cost ledger — hook not installed for these runs").

<!-- END OF DOCUMENT -->
