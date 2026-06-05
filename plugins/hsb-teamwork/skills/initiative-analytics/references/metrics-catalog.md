# The metric catalog — every signal an initiative exposes

This file is the **authoritative catalog** of what `initiative-analytics` can
measure. Every metric below is derived from data the initiative already
accumulates: the **cost ledger** (`analytics/cost-ledger.jsonl`, written by the
cost-capture hook), the **works+definitions index** (`initiative.json`), the
**Q&A ledgers** (`<phase>/qa-log.md`), and the **frozen documents** of each
phase. Nothing here requires a live human to type a number — the value side of
ROI is *extracted from the documents*, not asked (see `roi-model.md`).

The metrics are grouped into **five families**. The first four are objective and
fully computable; the fifth (ROI) is a family of composites that pairs the others
— *time × cost × results*.

> **Provenance discipline.** Every metric traces to a source. Investment/time
> metrics that depend on the hook are marked `[ledger]`; process/quality metrics
> read from the static artifacts are marked `[artifact]`. When the ledger is
> absent (hook never ran), the `[ledger]` family degrades gracefully to "not
> captured" rather than guessed — say so in the report, never invent tokens.

---

## A · Investment / consumption — *what it cost to produce* `[ledger]`

The cost ledger is a JSONL append log; each line is one consumption block:
`{ ts, phase, agent, role, model, in, out, cacheCreate, cacheRead, usd, durationMs }`
(schema in `cost-telemetry.md`). The Cost Collector aggregates it.

| Metric | Definition | Why it matters |
|---|---|---|
| **Tokens — total** | Σ `in + out + cacheCreate + cacheRead` | the raw consumption envelope |
| **Tokens by type** | input / output / cache-create / cache-read, separately | output is the expensive half; cache-read is near-free |
| **Tokens by phase** | grouped by `phase` | where the spend concentrates (origination vs readiness vs assessment vs prd) |
| **Tokens by agent** | grouped by `agent`/`role` (best-effort, see telemetry note) | which specialist is the cost driver |
| **Model mix** | % of tokens **and** % of USD per `model` | are we burning Opus where Haiku would do? |
| **USD — total** | Σ `usd` | the headline number: end-to-end dollar cost |
| **USD by phase / agent / model** | Σ `usd` grouped | the same drill-downs in money |
| **Cache savings** | (cacheRead tokens × input-rate) − (cacheRead tokens × cacheRead-rate) | dollars the prompt cache saved vs paying full input price |
| **Cache-hit ratio** | cacheRead ÷ (input + cacheRead) | cost discipline of the pipeline |
| **Agent invocations** | count of `Task` spawns per phase, per `subagent_type` | fan-out volume; pairs with tokens for cost-per-spawn |
| **Orchestrator turns** | count of top-level (non-sidechain) assistant turns | how much the Layer-0 conversation itself cost |

---

## B · Time / duration — *how long it took* `[ledger]` + `[artifact]`

Wall-clock comes from `initiative.json` timestamps (`phases.*.started` and the
new `phases.*.finishedAt`, set on freeze). Active-compute and human-latency come
from the ledger's per-message `durationMs` and timestamps.

| Metric | Definition | Why it matters |
|---|---|---|
| **Phase wall-clock** | `finishedAt − started` per phase | calendar time each front consumed |
| **Initiative lead time** | last `finishedAt` − first `started` | end-to-end calendar time, raw signal `[artifact]` |
| **Active compute time** | Σ `durationMs` of model calls in the phase | time the machine actually worked `[ledger]` |
| **Human-latency gap** | phase wall-clock − active compute time | time spent waiting on the human (think + away) — the automation-leverage signal |
| **Time-in-gate** | span from first open question to gate-clear, from qa-log `Asked:` timestamps | how long convergence took `[artifact]` |
| **Active-to-wall ratio** | active compute ÷ wall-clock | leverage: low ratio = mostly human/async time, machine cost is small relative to elapsed |

---

## C · Process / throughput — *how the work flowed* `[artifact]`

From `<phase>/qa-log.md` (the Q&A ledger schema), `contract.lock.md`, and the
filled documents.

| Metric | Definition | Why it matters |
|---|---|---|
| **Questions asked** | count of `Q###` per phase | interrogation volume |
| **Answer outcome mix** | answered vs parked vs superseded vs open | how cleanly the demand resolved |
| **Capture-loop rounds** | distinct audit/loop iterations (inferable from qa-log revs / ledger turn bursts) | convergence difficulty — the main avoidable-cost driver in a long run |
| **Follow-up ratio** | questions with `Spawned-by` ÷ total questions | how much each answer opened new gaps |
| **Rework events** | superseded entries + template-restart + revisits + version bumps + PM rejections + CTO vetoes | wasted/redone work — pure ROI drag |
| **Blocking-section coverage** | resolved-or-disposed blocking sections ÷ total blocking | completion of the contract |
| **Tokens per question** | phase tokens ÷ questions answered `[ledger+artifact]` | interrogation efficiency |
| **USD per answered question** | phase USD ÷ questions answered `[ledger+artifact]` | dollar cost of each unit of understanding |
| **Tokens per blocking section** | phase tokens ÷ blocking sections resolved `[ledger+artifact]` | cost per unit of deliverable |

---

## D · Quality / outcome — *what was produced* `[artifact]`

From `initiative.json` (readiness, owes, produces) and the frozen documents
(dispositions, triage decision, feasibility verdict, sign-offs).

| Metric | Definition | Why it matters |
|---|---|---|
| **Readiness per phase** | `phases.*.readiness` (0–100) | the confidence the front froze at |
| **Disposition mix** | % real-answered vs assumption / discovery / deferred | uncertainty load carried forward — honesty, not failure, but a risk weight |
| **Open debts** | count + list of unresolved `phases.*.owes` | handoffs still outstanding (e.g. an owed TA) |
| **Triage decision** | Product Ready / Discovery / Backlog / Reject (from the Intake Record) | the routing gate — and which ones avoided the expensive Act 2 |
| **Feasibility verdict** | feasible / feasible-with-caveats / infeasible / vetoed (from the TA) | the architectural gate |
| **Escalation outcome** | TA owed? signed? vetoed? PM accepted/rejected? | how the gated chain actually resolved |
| **Completion depth** | furthest phase reached (origination → readiness → assessment → prd → delivered-to-pm) | did the demand make it to a PRD, or stop early? |

---

## E · ROI composites — *time × cost × results* `[ledger+artifact]`

ROI is **not one number**. It is a family of ratios pairing the investment side
(A+B, objective dollars/tokens/time) against the results side (C+D, throughput
and outcome). The *value* anchor is **extracted from the documents** — see
`roi-model.md` for exactly how the value score is built. Each composite is
labeled with its direction (↓ better / ↑ better).

| Composite | Formula | Reads | Direction |
|---|---|---|---|
| **Cost-to-readiness** | total USD ÷ final readiness | A, D | ↓ dollars per readiness point |
| **Gate savings** | est. full-pipeline USD − USD actually spent, when a gate (triage Reject/Backlog/Discovery, or a TA veto) stopped the chain early | A, D | ↑ the ROI of the gate itself: money the gate *avoided* |
| **Value-anchored ROI** | (value score − normalized investment) ÷ normalized investment | A, D + value | ↑ return over investment, value extracted from docs (estimate-grade) |
| **Throughput — per dollar** | final readiness ÷ total USD | A, D | ↑ readiness delivered per dollar |
| **Throughput — per hour** | final readiness ÷ active compute hours | B, D | ↑ readiness delivered per machine-hour |
| **Throughput — per Mtok** | final readiness ÷ (total tokens ÷ 1e6) | A, D | ↑ readiness delivered per million tokens |
| **Automation leverage** | active compute time ÷ wall-clock | B | context: how much elapsed time was machine vs human |
| **Cache discipline** | cache-hit ratio (from A) | A | ↑ share of input served cheap from cache |
| **Cost per deliverable** | total USD ÷ printable `final/` deliverables produced | A, D | ↓ dollars per shipped artifact |

### The gate-savings story (the headline ROI of this toolkit)

The whole point of the gated chain is **spending little to avoid spending a
lot**. Quantify it: when triage routes a demand to `Reject`/`Backlog`/`Discovery`
*before* Act 2, or a feasibility `veto` halts the PRD merge, the initiative spent
only the cheap upstream cost and **avoided** the expensive downstream phases.
`Gate savings = (median USD of a full origination→prd run on comparable
initiatives, or a configurable baseline) − (USD actually spent)`. Report it as a
first-class ROI win, not a footnote — it is the clearest dollar evidence that the
gates pay for themselves.

---

## How the families compose into the report

The `roi-report.md` renders these in this order (see the template):

1. **Header** — initiative identity, status, lead time, total USD, total tokens, model mix.
2. **Per-phase table** — for each phase: wall-clock, tokens, USD, agent spawns, loop rounds, final readiness, outcome (triage / verdict), disposition mix.
3. **Cost drivers** — top agents and models by USD/tokens.
4. **ROI panel** — the E composites, with the value anchor and its provenance stated, gate savings called out.
5. **Open items** — outstanding debts and every parked assumption/discovery/deferred (the carried risk).

Every number cites its source family so a human can audit it. When a metric
cannot be computed (no ledger, or a phase never froze), it renders as
**"not captured"** with the reason — never a fabricated value.

<!-- END OF DOCUMENT -->
