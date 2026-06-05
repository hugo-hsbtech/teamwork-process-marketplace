# Companion guide — filling the Initiative ROI Report

This guide tells the **ROI Reporter** how to fill each section of
`target-template.roi-report.md` from the composed metric set. The report is
*rendered*, not captured — there is no confidence loop. The bar is: every number
is sourced, value is labeled estimate, nothing is fabricated.

## Global rules

- **Language:** render in `initiative.json.language` (default the human's).
- **Provenance:** tag each metric `[ledger]` (measured by the hook) or
  `[artifact]` (from documents / `initiative.json`). Keep the tags in the report.
- **Estimate labeling:** the value score and the value-anchored ROI are
  **estimate** — say so every time they appear.
- **Not captured:** if the ledger is absent, render §1 cost / §2 token-USD cells /
  §3 / and the dollar ROI rows as **"not captured (<reason>)"**, and still fill the
  `[artifact]` half (readiness, dispositions, outcomes, value). Never guess a token
  or dollar figure.
- **No truncation:** end the file with `<!-- END OF DOCUMENT -->`; on re-run,
  read-modify-write into the existing file.

## Per section

**§1 Header.** Identity and the headline totals. Lead time = last
`finishedAt` − first `started` from `initiative.json`. Model mix = the Cost
Collector's %tokens / %USD per model. Final readiness = the furthest phase's
`readiness`.

**§2 Per-phase breakdown.** One row per phase that exists in `initiative.json`.
Wall-clock from `started → finishedAt`. Tokens/US$/spawns from the Cost Collector,
keyed by `phase`. Rounds and disposition mix from the Metrics Analyst. Outcome =
the phase's gate result (triage decision for readiness; feasibility verdict for
assessment; delivered/halted for prd). A phase with no `finishedAt` or no ledger
rows → "not captured" in the affected cells.

**§3 Cost drivers.** Top agents/models by USD (note the per-agent split is
best-effort; orchestrator-vs-subagent is exact). Cache discipline and savings, and
automation leverage, straight from the Cost Collector.

**§4 ROI panel.** The composites the orchestrator computed (`roi-model.md`).
Cost-to-readiness and throughput ratios are exact. Value-anchored ROI is estimate.
**Gate savings** appears **only** when a gate stopped the chain early (triage
Reject/Backlog/Discovery before Act 2, or a vetoed TA) — otherwise omit the row and
the story. Always render the **value breakdown** table with the Metrics Analyst's
per-dimension scores and document citations — this is the auditable substitute for
a human dollar figure.

**§5 Open items.** Outstanding `owes`, every parked disposition (the carried risk),
and an explicit list of any not-captured metric families with the reason.

## roi.json

Write the same content machine-readable: `{ initiative, project, status, leadTime,
totals:{usd,tokens:{...},modelMix}, phases:[...], drivers, roi:{...,
valueBreakdown:[...], gateSavings}, open:{owes, parked, notCaptured} }`. Keep it in
sync with the markdown — sibling runs read `roi.json` for the gate-savings
baseline.
