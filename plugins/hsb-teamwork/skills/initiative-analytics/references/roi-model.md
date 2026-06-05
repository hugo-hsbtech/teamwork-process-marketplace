# The ROI model — pairing investment against value

ROI = return ÷ investment. The **investment** side is fully objective — dollars,
tokens, and time captured by the hook (`cost-telemetry.md`) plus the durations in
`initiative.json`. The **return/value** side is, in this toolkit, captured
*qualitatively* in the documents. This file defines how the Metrics Analyst turns
that qualitative material into a **value score** and how the ROI composites are
computed — so ROI is a defensible metric, not a vibe.

> **Decision in force:** the value anchor is **extracted from the documents**, not
> asked from a human. There is no "type a dollar figure" prompt. The value score
> is therefore an **estimate-grade, dimensionless score (0–100)**, and every ROI
> composite that uses it is labeled *estimate* in the report. The cost side stays
> exact (USD/tokens/time).

---

## The investment index

A single normalized **investment** figure feeds the composites, alongside the raw
USD. It is built from the ledger:

```
investment_usd      = Σ usd                      (exact, headline)
investment_tokens   = Σ (in + out + cacheCreate + cacheRead)
investment_minutes  = active compute minutes  (Σ durationMs / 60000)
```

For the value-anchored composite, investment is **normalized to 0–100** against a
configurable reference band (default: a small initiative ≈ low score, a full
four-phase initiative ≈ high score), so it is comparable to the value score on the
same scale. The raw USD is always reported next to it — the normalization is for
the ratio, never a replacement for the real dollar figure.

---

## The value score (0–100) — extracted from the documents

The Metrics Analyst reads the frozen, canonical documents and scores **declared
value** across weighted dimensions. It reads, never invents — every point traces
to a line in a document; unstated dimensions score low (and are flagged as
"value not articulated", which is itself a finding).

| Dimension | Weight | Source in the documents |
|---|---|---|
| **Reach** | 25 | origination-record: who/how many it affects (reach/persona breadth) |
| **Impact / pain severity** | 30 | origination-record problem framing; RP problem & objectives |
| **Strategic objectives** | 20 | RP §objectives — how directly it serves a stated goal |
| **Measurability** | 15 | RP §success-metrics / metrics — are outcomes quantified and trackable? |
| **Confidence of value** | 10 | disposition mix on the value-bearing sections (real-answered vs assumption/deferred) — discounts value that rests on unvalidated assumptions |

`value_score = Σ (dimension_score × weight) / 100`, each dimension scored 0–100
against its rubric. The **Confidence-of-value** dimension is what keeps the score
honest: a demand whose impact is all `assumption`/`deferred` is scored down, so
ROI never rewards confident-looking value that the pipeline itself marked as
unvalidated.

The report always shows the **value breakdown by dimension** with the document
citations, so the human can challenge any point. This is the auditable substitute
for a human-entered dollar value.

---

## The ROI composites (computation)

All composites are defined in `metrics-catalog.md` §E. Here is how each is
computed and reported:

- **Cost-to-readiness** = `investment_usd ÷ final_readiness`. Exact. ↓ better.
- **Throughput per dollar / hour / Mtok** = `final_readiness ÷ {usd | hours | Mtok}`. Exact. ↑ better.
- **Value-anchored ROI** = `(value_score − investment_norm) ÷ investment_norm`,
  reported as a percentage and clearly marked **estimate** (value side is the
  document-derived score). Show the value breakdown beside it.
- **Gate savings** = `baseline_full_run_usd − investment_usd`, computed **only**
  when a gate stopped the chain early (triage `Reject`/`Backlog`/`Discovery`
  before Act 2, or a feasibility `veto` before the PRD). `baseline_full_run_usd`
  is, in order of preference: (a) the median USD of comparable *completed*
  initiatives in this `TEAMWORK_ROOT`; (b) a configurable default; (c) omitted
  with a note if neither is available. ↑ better — this is the gate's own ROI.
- **Automation leverage** = `active_compute ÷ wall_clock`. Context metric.
- **Cache discipline** = cache-hit ratio. ↑ better.

---

## Honesty rules

1. **Cost is exact; value is an estimate.** Never blur the two — label every
   value-derived number `estimate` and show its provenance.
2. **No fabricated value.** A dimension with nothing in the documents scores low
   and is flagged, never imagined upward.
3. **Discount unvalidated value.** The Confidence-of-value dimension exists so ROI
   doesn't reward value resting on `assumption`/`deferred` dispositions.
4. **Degrade, don't guess.** Missing ledger → dollar composites render
   readiness-only variants and say so (`cost-telemetry.md` § Graceful
   degradation).
5. **Gate savings only on a real gate.** Never claim avoided cost on an
   initiative that simply hasn't finished yet — only on a recorded early stop.

<!-- END OF DOCUMENT -->
