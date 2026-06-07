# Inheritance — RP/TA → PRD section mapping

This file is the lookup `hsb-stage-inheritor` uses to carry each frozen half forward.
Each PRD section `id` names exactly which **source** section it is summarized from. The
Inheritor runs **once per `PART`** (`A` from the RP, `B` from the TA), preserves the
source's confidence, tags every entry `Origin: inherited`, and **links back** to the full
source for the complete detail — it summarizes to the PRD's altitude, it does not copy.

> "Preserve confidence" means: if a source section was `low_confidence` or carried an
> `assumption` / `discovery` disposition, that travels into the PRD unchanged. The PRD does
> not launder uncertainty — an assumption inherited from the RP stays an assumption the PM
> must see (it surfaces again in `inherited-readiness`). See `personas/01-submitter.md` §3–§6
> on confidence traveling with the artifact.

## Part A — from the Readiness Package (PART: A)

| PRD `id` | Source (RP) | What the Inheritor carries |
|---|---|---|
| `a-objectives` | RP objectives / expected outcome | the measurable outcomes (outcomes, not outputs) |
| `a-scope` | RP scope (included / excluded / deferred) | the **reconciled** boundaries (see [`reconciliation.md`](reconciliation.md)) |
| `a-personas` | RP personas / jobs-to-be-done | who is impacted + the job each hires the product to do |
| `a-journey` | RP user journey (happy path) | the end-to-end flow the stories derive from; alt paths stay in the RP |
| `a-business-rules` | RP business rules, validations, state transitions | a summary or pointed reference — enough to size the work |
| `a-user-stories` | RP epics + user stories + acceptance criteria | epics (deliverables) with their stories + **primary** Given/When/Then; preserve the RP's epic grouping, every story under exactly one epic; full criteria stay in the RP |
| `a-nfrs` | RP §8 (non-functional requirements) | each NFR + its verification (pairs 1:1 with `b-nfr-feasibility`) |
| `a-edge-cases` | RP §9 (edge cases / failure modes) | each case + expected behavior |
| `success-metrics` | RP metrics with guardrails / success criteria | primary metrics + guardrails, with target / window / confidence |
| `effort-cost` (no-escalation path) | RP §13 preliminary estimate | the preliminary number, **labeled preliminary** |
| `inherited-readiness` (assumptions, in part) | RP open dispositions (assumptions / discovery / deferred) | what survived upstream, with owner |

## Part B — from the Technical Assessment (PART: B; escalated path only)

| PRD `id` | Source (TA) | What the Inheritor carries |
|---|---|---|
| `b-feasibility` | TA `feasibility-verdict` | the verdict + caveats, **carried, never re-decided** |
| `b-nature-landscape` | TA `tech-classification` + `current-state` / `tech-foundation` | the nature + the terrain summary (current state or foundation) + KB link |
| `b-arch-impact` | TA `affected-systems` + `architectural-impact` + `integrations` | systems/areas touched + integrations under the feasibility lens |
| `b-nfr-feasibility` | TA `nfr-feasibility` | one row per `a-nfrs` NFR: feasible? + how + caveat |
| `b-alternatives` | TA `alternatives` | the discarded options + **why not** |
| `b-hard-constraints` | TA `hard-constraints` | non-negotiable conditions + effect on scope (feeds `scope-reconciliation`) |
| `b-adrs` | TA `adrs` | the CTO-signed architectural ADRs (implementation ADRs stay in the Tech Backlog) |
| `effort-cost` (escalated path) | TA `effort-cost` | the **firm** estimate (replaces the RP preliminary) |
| `consolidated-risk` (technical rows) | TA `tech-risks` | the technical risks, tagged `Origin: TA`, merged with the RP risks |

On the **no-escalation path**, `PART: B` returns the honest-N/A dispositions instead of
inherited content: every Part B `id` is `Disposition: decided`, "N/A — no architectural
escalation" (see [`reconciliation.md`](reconciliation.md)).

## What the Inheritor preserves — and what it does not

**Preserves:**

- the **source confidence** and any open disposition (`assumption` / `discovery` /
  `deferred`) — uncertainty travels;
- the **authorship boundary** — Part A entries trace to the RP (the PO's), Part B entries
  to the TA (the CTO's);
- the **trace-to-source** in each entry's `Source` field (e.g. "RP §6.5", "TA
  feasibility-verdict", "RP question #2").

**Does not:**

- **rewrite** either source — it summarizes and links back; the frozen RP/TA stay
  canonical;
- **re-decide** anything — the verdict, the scope, the risks are carried as the frozen
  documents settled them;
- **compose or reconcile** — that is the Synthesizer's and Reconciler's job (the `derived`
  sections), not the Inheritor's;
- **invent** facts absent from the source — a missing source section is a gap the Auditor
  flags, not a blank the Inheritor fills.

## Fan-out

Spawn the Inheritor **once per `PART`, both in the same turn** (independent → parallel):
`PART: A` (from the RP) ∥ `PART: B` (from the TA, or the N/A dispositions). Each returns
its proposals to the orchestrator, who routes them through `hsb-ledger-writer` →
`hsb-doc-updater` (the single writers). The Inheritor never writes a shared file directly.
