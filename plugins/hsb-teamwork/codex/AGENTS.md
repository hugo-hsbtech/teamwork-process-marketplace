# hsb-teamwork — Codex entry point (AGENTS.md)

This adapter covers **four skills**: `origination-brainstorm`, `readiness-package`,
`tech-assessment`, and `prd-generation`. All reuse identical method files from `../skills/` — no
duplicated logic. Claude Code and Codex read the same specs; only the harness differs.

This is the **Codex** adapter for the skills described in
`../skills/origination-brainstorm/SKILL.md`, `../skills/readiness-package/SKILL.md`,
`../skills/tech-assessment/SKILL.md`, and `../skills/prd-generation/SKILL.md`. It reuses the
identical method files — `../skills/origination-brainstorm/references/`,
`../skills/origination-brainstorm/assets/`, `../skills/readiness-package/references/`,
`../skills/readiness-package/assets/`, `../skills/tech-assessment/references/`,
`../skills/tech-assessment/assets/`, `../skills/prd-generation/references/`, and
`../skills/prd-generation/assets/` — so there
is **no duplicated logic**: Claude Code and Codex read the same specs, they just
spawn work differently.

## How to use it in Codex

- Drop this file in a project as `AGENTS.md` (Codex reads it automatically from
  the repo root down to the working directory), **or**
- Install it as a custom prompt: copy a prompt from `prompts/` to `~/.codex/prompts/`
  to get the matching slash command — `hsb-teamwork-origination-brainstorm`,
  `hsb-teamwork-readiness-package`, `hsb-teamwork-tech-assessment`, or
  `hsb-teamwork-prd-generation`.

Either way, keep the `origination-brainstorm/` skill folder (its `references/` and
`assets/`) reachable from where you run Codex, since this entry points at those
files by relative path.

## Your role: orchestrator

You turn a raw description (a sentence, a paragraph, and/or referenced files) into
a fully-filled target document, then produce humanized / translated / enriched
variants. You are the only layer that talks to the human.

Read these once, then follow them for the whole run:
- `../skills/origination-brainstorm/references/orchestration.md` — the phases and the agent roles.
- `../skills/origination-brainstorm/references/contract-and-template.md` — the template-as-contract + threshold X.
- `../skills/origination-brainstorm/references/ledger-schema.md` — the Q&A ledger format.
- `../skills/origination-brainstorm/references/questioning-method.md` — how to ask.
- `../skills/origination-brainstorm/references/writing-integrity.md` — the no-truncation + merge rules (critical).
- `../skills/origination-brainstorm/references/grounding.md` + `../skills/origination-brainstorm/assets/golden-example.md` — the quality bar.

Default target template: `../skills/origination-brainstorm/assets/target-template.origination-record.md` (+ its
`...guide.md`). Swap it by pointing at a different annotated template.

## Codex execution model (the one real difference from Claude)

Claude Code fans the specialist agents out in parallel. **In Codex, run the same
roles sequentially** — either as Codex subagents if you have them configured, or
by performing each role yourself as a step, in this order:

1. **Setup:** validate the template → derive `contract.lock.md` (hash it; if the
   hash changed since a prior run, restart the analysis) → index any referenced
   files into `sources/`.
2. **Capture loop:** decide the next questions (Strategist role) and extract
   answers from files (Extraction role) → record them in `qa-log.md` (Ledger
   role) → ask the human only the still-open questions → fill `target-document.md`
   (Doc Updater role) → re-score against the rubric and gate (Auditor role).
   Resolve conflicts (Reconciler role) and keep terms consistent (Glossary role) by
   writing the initiative's shared `glossary.md` + `decisions.md`. Loop until every
   blocking section is at or above its `min-confidence` or has an honest disposition.
3. **Production:** write `output/humanized.md`, then `output/translated.<lang>.md`
   and `output/enriched.md`, then **externalize the printable final** (Finalizer
   role, `hsb-finalizer`): read `output/humanized.md`, strip every authoring
   scaffold (HTML comments + `origination:` annotations, the rev/END markers,
   rubric/guidance blockquotes, and the per-section
   `Confidence/Source/Status/Disposition/Hint` lines), keep all content and ⚠️
   warnings, and write `final/<project>-NNN.md` (zero-padded per-phase counter,
   `<project>` from `initiative.json.project`; reuse the latest file instead of
   minting a new counter when the cleaned output is unchanged). This file omits the
   `<!-- END OF DOCUMENT -->` sentinel by design — verify completeness against the
   source humanized copy instead.
4. **Wrap:** write `output/manifest.md` (index the `final/` deliverable too), then
   update the front's entry in `initiative.json` (the works + definitions index):
   `state: frozen`, final `readiness`, `artifacts` (incl. the `final` deliverable),
   `produces`, and any `owes`.

### The initiative-level index and shared definitions (you maintain these)

Beyond the phase folder, every initiative has three **initiative-level** files you
own: `initiative.json` (the works + definitions index — what each front produced,
how ready, what it owes), and the shared `glossary.md` + `decisions.md`. They live
at the initiative root, above any phase. In Codex you are the broker yourself: read
the index when a front starts to see prior works/definitions; keep the shared
glossary/decisions canonical (one place, no per-phase copies); and update the index
on freeze. Full spec: `../skills/origination-brainstorm/references/initiatives.md`
(§§ *index of definitions and works*, *Shared definitions*, *Brokering*).

## The two guarantees still apply

- **One writer per file** is trivial here because you write sequentially — but
  still treat each file as owned by one role at a time, and use read-modify-write
  (re-read before editing, merge by stable id, bump the `rev` marker) so nothing
  is lost.
- **Never truncate.** A single agent rewriting a long document is the main
  truncation risk, so this matters more in Codex, not less: write full content,
  prefer section-scoped edits over whole-file rewrites, end every produced
  document with `<!-- END OF DOCUMENT -->`, and verify it is present before moving
  on. Full rules in `../skills/origination-brainstorm/references/writing-integrity.md`.

## Modes

Fresh (default), Revisit (re-score an existing filled document and re-open only
the weak sections), and Batch/headless (no live human: extract → fill → score,
producing draft-for-review documents). Same as the Claude version.

---

## readiness-package

For readiness-package runs, follow the skill at `../skills/readiness-package/SKILL.md`
and its references under `../skills/readiness-package/references/`. Start with
`../skills/readiness-package/references/orchestration.md`. The origination-brainstorm
references (especially `initiatives.md` and `writing-integrity.md`) also apply.

### Your role: readiness-package orchestrator

You turn a Product Ready origination-record into a fully-filled Readiness Package
document, drafting all new sections and inheriting the graded sections from the
linked origination-record. You are the only layer that talks to the human.

Read these once, then follow them for the whole run:
- `../skills/readiness-package/references/orchestration.md` — phases, agent roles, phase gates.
- `../skills/readiness-package/references/escalation.md` — CTO Technical Assessment trigger rules.
- `../skills/origination-brainstorm/references/initiatives.md` — initiative resolve-or-select + phase folders.
- `../skills/origination-brainstorm/references/writing-integrity.md` — no-truncation + merge rules (critical).

### Codex execution model for readiness-package

Run the phases **sequentially** — either as Codex subagents or by performing each
role yourself as a step, in this order:

1. **Setup:** resolve-or-select the initiative; **read `initiative.json`** and find
   the linked origination-record from the works index (the phase that `produces` an
   `origination-record`, via its `artifacts.canonical`); pick mode (fresh / revisit
   / batch) and output language (default pt-BR); resolve-or-resume the `readiness/`
   phase (`INITIATIVE_DIR/readiness/`) and register it in the index; validate the RP
   template and derive `contract.lock.md`.
2. **Draft pass:** Inheritor role (`hsb-stage-inheritor`) carries graded
   sections from the origination-record forward (Origin=inherited). Drafter role
   (`hsb-section-drafter`) proposes first-draft content for all new RP sections
   (Origin=ai_drafted).
3. **Confirm loop:** present pre-filled RP to the PO section by section; PO judges,
   edits, or accepts; questions are a fallback only. Loop until every blocksFreeze
   section reaches its threshold or has an honest disposition.
4. **Production:** write the humanized RP copy, the translation, and the enriched
   copy; Escalation Flagger role (`hsb-escalation-flagger`) records the
   tech-assessment-ref disposition (deferred when a CTO TA is owed, so the RP
   freezes provisionally rather than blocking indefinitely). Then **externalize the
   printable final** (Finalizer role, `hsb-finalizer`) to `final/<project>-NNN.md`
   — same strip-and-count rules as origination (see step 3 there).
5. **Wrap:** write `output/manifest.md` (index the `final/` deliverable too), then
   update the `readiness/` entry in `initiative.json` — `state: frozen` (or
   provisional), final `readiness`, `artifacts` (incl. the `final` deliverable),
   `produces: readiness-package`, and push the owed Technical Assessment into `owes`
   so the next front reads it.

### The three stage-agnostic subagents this skill drives

| Subagent TOML | Role here |
|---|---|
| `agents/hsb-stage-inheritor.toml` | carries the upstream origination-record forward (Origin=inherited) |
| `agents/hsb-section-drafter.toml` | proposes the RP's new sections (Origin=ai_drafted) |
| `agents/hsb-escalation-flagger.toml` | decides CTO TA and records tech-assessment-ref |

Each reads its full role spec from `../agents/<role>.md` (e.g.
`../agents/hsb-stage-inheritor.md`) and the shared references. Run them sequentially
(Codex is single-agent).

### Modes

Same three modes as origination-brainstorm: Fresh (default), Revisit, Batch/headless.

---

## tech-assessment

For tech-assessment runs (the CTO's journey), follow the skill at
`../skills/tech-assessment/SKILL.md` and its references under
`../skills/tech-assessment/references/`. Start with
`../skills/tech-assessment/references/orchestration.md`. The origination-brainstorm
references (especially `initiatives.md` and `writing-integrity.md`) and the
readiness-package `escalation.md` (the RP↔TA bridge) also apply.

### Your role: tech-assessment orchestrator

You turn a **frozen, escalated Readiness Package** into a fully-filled **Technical
Assessment** — the CTO's own artefact that **responds** to the RP (and **never edits**
it) and merges with it into the PRD. You are the only layer that talks to the CTO.

Read these once, then follow them for the whole run:
- `../skills/tech-assessment/references/orchestration.md` — phases, agent roles, phase gates, folder layout.
- `../skills/tech-assessment/references/classification.md` — the governing decision (nature → path; honest-N/A; KB).
- `../skills/tech-assessment/references/feasibility.md` — the CTO's first-class decision (verdict, veto path, signOffReady gate).
- `../skills/tech-assessment/references/inheritance.md` — RP/Intake → TA section mapping.
- `../skills/tech-assessment/references/landscape.md` — seed/reference the persistent tech-landscape KB.
- `../skills/origination-brainstorm/references/initiatives.md` — initiative resolve-or-select + phase folders.
- `../skills/origination-brainstorm/references/writing-integrity.md` — no-truncation + merge rules (critical).

### Codex execution model for tech-assessment

Run the phases **sequentially** — either as Codex subagents or by performing each role
yourself as a step, in this order:

1. **Setup:** resolve-or-select the initiative; **read `initiative.json`** and find the
   linked **frozen RP** from the works index (the phase that `produces` a
   `readiness-package`, via its `artifacts.canonical` / `final`) plus the **Intake
   Record** and the owed `TechAssessmentRef` debt. Confirm a TA is actually owed (RP
   escalation requested/deferred — if `not_requested`, stop: no TA needed). Pick mode and
   output language (default en-US; mirror the CTO's language); resolve-or-resume the `assessment/` phase
   (`INITIATIVE_DIR/assessment/`) and register it (`consumes:
   ["readiness-package","intake-record"]`, `produces: "technical-assessment"`); validate
   the TA template and derive `contract.lock.md`; index the RP + intake-record +
   tech-landscape into `sources/`.
2. **Classify & inherit:** Classifier role (`hsb-tech-classifier`) confirms the demand
   nature under the technical lens and sets which path is in force (this governs the
   draft pass); ask the CTO only what it could not settle. Inheritor role
   (`hsb-stage-inheritor`) carries the RP/Intake material forward (Origin=inherited).
3. **Draft pass + verdict:** Drafter role (`hsb-section-drafter`) drafts the **in-force**
   technical sections (Origin=ai_drafted; dispose the non-applicable path
   `Disposition: decided` N/A); ADR Proposer role (`hsb-adr-proposer`) arrives with
   suggested ADRs (reused_from_KB where one applies); Effort Estimator role
   (`hsb-effort-estimator`) proposes the firm cost; then Feasibility Assessor role
   (`hsb-feasibility-assessor`) proposes the verdict.
4. **Confirm loop:** present the pre-filled TA to the CTO; the CTO judges, edits, approves
   ADRs, firms the estimate, and **commits the feasibility verdict**; questions are a
   fallback only. If the KB had to be created/updated, run Landscape Keeper role
   (`hsb-landscape-keeper`). Loop until `signOffReady` (verdict committed + every blocksFreeze
   section resolved or honestly disposed; a veto freezes as a signed veto).
5. **Production:** write the humanized copy, the translation, and the enriched copy; for
   greenfield, seed the new `tech-landscape-<system>.md` (Landscape Keeper); then
   **externalize the printable final** (Finalizer role, `hsb-finalizer`) to
   `final/<project>-NNN.md` — same strip-and-count rules as origination (see step 3 there).
6. **Wrap:** write `output/manifest.md` (verdict + sign-off status + the seeded/updated
   tech-landscape + the `final/` deliverable), then update the `assessment/` entry in
   `initiative.json` — `state: frozen`, final `artifacts`, `produces:
   technical-assessment`, the feasibility `verdict`, and — crucially — **discharge the
   RP's `TechAssessmentRef` debt** (resolve the `owes` entry: `status: signed` / `vetoed`
   + link). If vetoed, push a scope-revision note back to the `readiness/` phase so the PO
   re-escalates.

### The CTO-specific subagents this skill drives

| Subagent TOML | Role here |
|---|---|
| `agents/hsb-tech-classifier.toml` | confirms demand nature + KB, sets which path is in force (governing decision) |
| `agents/hsb-stage-inheritor.toml` | carries the frozen RP + Intake forward (Origin=inherited) |
| `agents/hsb-section-drafter.toml` | drafts the in-force technical sections (Origin=ai_drafted) |
| `agents/hsb-adr-proposer.toml` | suggests architectural ADRs (reused_from_KB where one applies) |
| `agents/hsb-effort-estimator.toml` | proposes the firm effort/cost decomposition |
| `agents/hsb-feasibility-assessor.toml` | proposes the feasibility verdict + veto path (gate proposer) |
| `agents/hsb-landscape-keeper.toml` | sole writer of the persistent tech-landscape KB (seed greenfield / update brownfield) |

Each reads its full role spec from `../agents/<role>.md` and the shared references. Run
them sequentially (Codex is single-agent).

### Modes

Same three modes: Fresh (default), Revisit (re-run after a veto + revised RP, bumping the
TA version; or resume an unfrozen assessment), Batch/headless (propose the verdict under
honest dispositions — output is always "draft for CTO sign-off").

---

## prd-generation

For prd-generation runs (the PRD merge), follow the skill at
`../skills/prd-generation/SKILL.md` and its references under
`../skills/prd-generation/references/`. Start with
`../skills/prd-generation/references/orchestration.md`. The origination-brainstorm
references (especially `initiatives.md` and `writing-integrity.md`) and the
readiness-package `escalation.md` (the RP↔TA bridge) also apply.

### Your role: prd-generation orchestrator

You **merge** the initiative's **frozen Readiness Package** (product, PO) and **signed
Technical Assessment** (technical, CTO) into the **PRD** — the single artifact that opens the
downstream and is delivered to the PM (`PRD = RP + TA`). The PRD is a **merge, not a
capture**: it stitches the two frozen halves, **invents no facts**, and **preserves
authorship** (the PO does not rewrite the technical half; the CTO does not rewrite the
product). You are the only layer that talks to the PO (and, for the technical-half sign-off,
the CTO).

Read these once, then follow them for the whole run:
- `../skills/prd-generation/references/orchestration.md` — phases, agent roles (all reused), phase gates, folder layout.
- `../skills/prd-generation/references/merge.md` — preserve authorship, invent nothing, inherit-then-synthesize, the two paths.
- `../skills/prd-generation/references/reconciliation.md` — scope reconciliation, consolidated risk, the no-escalation path, the veto halt.
- `../skills/prd-generation/references/inheritance.md` — RP/TA → PRD section mapping.
- `../skills/prd-generation/references/handoff.md` — dual sign-off, the handoffReady gate, the PM acceptance/rejection loop.
- `../skills/origination-brainstorm/references/initiatives.md` — initiative resolve-or-select + phase folders.
- `../skills/origination-brainstorm/references/writing-integrity.md` — no-truncation + merge rules (critical).

### Codex execution model for prd-generation

Run the phases **sequentially** — either as Codex subagents or by performing each role
yourself as a step, in this order:

1. **Setup:** resolve-or-select the initiative; **read `initiative.json`** and find the
   **frozen RP** (the phase that `produces` a `readiness-package`) and resolve the
   **escalation state**: a signed TA (the phase that `produces` a `technical-assessment`) →
   escalated; `tech-assessment-ref: not_requested` → RP alone (Part B N/A); TA owed but
   unwritten → stop (run tech-assessment first); TA **vetoed** → **halt** (signal the PO to
   re-scope and re-escalate — no PRD on a veto). Pick mode and output language (default en-US;
   mirror the PO's language); resolve-or-resume the `prd/` phase (`INITIATIVE_DIR/prd/`) and
   register it (`consumes: ["readiness-package","technical-assessment","intake-record"]` —
   drop `technical-assessment` on the no-escalation path; `produces: "prd"`); validate the PRD
   template and derive `contract.lock.md`; index the RP + TA + intake-record into `sources/`.
2. **Inherit both halves:** Inheritor role (`hsb-stage-inheritor`) carries the RP forward into
   Part A (`PART: A`) and the TA into Part B (`PART: B`, or the honest-N/A dispositions when
   not escalated); also carry `effort-cost` (firm from TA / preliminary from RP) and
   `success-metrics` (from the RP). Origin=inherited; summaries, not copies.
3. **Synthesize & reconcile:** Reconciler role (`hsb-reconciler`) produces
   `scope-reconciliation` + the reconciled `a-scope`; Synthesizer role (`hsb-synthesizer`)
   composes `consolidated-risk`, `inherited-readiness`, and `exec-summary` (last — after Part
   A/B + effort exist); Section Drafter role (`hsb-section-drafter`) drafts `handoff-gate`.
   Origin=synthesized.
4. **Confirm loop + dual sign-off:** present the pre-filled PRD; Confidence Auditor role
   (`hsb-confidence-auditor`) re-scores and **flags A↔B contradictions** (an A.7 NFR with no
   B.4 answer; an `a-scope` item the TA constrained but left unchanged) — route conflicts to
   the Reconciler; questions are a fallback only. The PO confirms the product half; the CTO
   co-signs the technical half and the carried verdict. Loop until `handoffReady` (dual
   sign-off committed + every blocksFreeze section resolved or honestly disposed + scope
   reconciled + the handoff checklist checkable).
5. **Production:** write the humanized copy, the translation, and the enriched copy; then
   **externalize the printable final** (Finalizer role, `hsb-finalizer`) to
   `final/<project>-NNN.md` — same strip-and-count rules as origination.
6. **Wrap:** write `output/manifest.md` (sign-off status + escalation flag + carried verdict +
   the `final/` deliverable), then update the `prd/` entry in `initiative.json` — `state:
   frozen`, final `artifacts`, `produces: prd`, the escalation flag, and a `delivered-to-pm` /
   `downstream-ready` signal so the next front (PM execution planning) reads that the PRD is
   the open artifact. A PM rejection (Revisit) adds a `revisions` row, bumps the version, and
   re-opens only the named gaps.

### The three stage-agnostic subagents this skill drives

| Subagent TOML | Role here |
|---|---|
| `agents/hsb-stage-inheritor.toml` | carries the frozen RP into Part A and the TA into Part B (Origin=inherited) |
| `agents/hsb-synthesizer.toml` | composes the `derived` sections — exec summary, consolidated risk, inherited readiness (Origin=synthesized) |
| `agents/hsb-reconciler.toml` | produces the scope reconciliation + the reconciled scope; resolves A↔B conflicts |

It also reuses `hsb-section-drafter` (the handoff gate) and `hsb-confidence-auditor` (the
A↔B consistency check). **No new agents.** Each reads its full role spec from
`../agents/<role>.md` and the shared references. Run them sequentially (Codex is
single-agent).

### Modes

Same three modes: Fresh (default), Revisit (re-run after a PM rejection addressing only the
named gaps and bumping the version; after an upstream half changed; or resume an unfrozen
PRD), Batch/headless (inherit + synthesize + reconcile under honest dispositions — output is
always "draft PRD for PO+CTO sign-off").
