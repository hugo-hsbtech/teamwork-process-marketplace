# Grading rubric — readiness-package

Two layers. **Structural** is automated (`assertions.py`, deterministic, gates the
run). **Qualitative** is LLM-graded against the golden bar (judgment, scored 1-5).

## Layer 1 — structural (automated, pass/fail)

Run by `assertions.py` on each produced `readiness-document.md`:

- `sentinel_present` — ends with `<!-- END OF DOCUMENT -->` (no truncation).
- `no_truncation_markers` — no `...` / `(unchanged)` / leftover `[fill]` placeholders.
- `has_annotations` — section annotations preserved (≥ 10 annotated sections).
- `blocking[<id>]_satisfied` — every `blocks=true` capture section is ≥ its
  `min-confidence` (direct answer) or carries an honest disposition
  (assumption/discovery/deferred). Blocking sections: `exec-summary`,
  `context-problem`, `objectives`, `personas`, `scope`, `business-rules`,
  `user-stories`, `nfrs`, `edge-cases`, `metrics`, `release-criteria`, `risks`.
- `confidence_lines_present` — capture sections with `min-confidence>0` carry the
  `Confidence/Origin/Source/Status/Disposition/Hint` line.
- `origin_present_valid` — every blocking section's confidence line contains an
  `Origin` value drawn from the allowed set (`inherited`, `ai_drafted`,
  `po_authored`, `reused_from_kb`).
- `tech_assessment_ref_resolved` — the `tech-assessment-ref` section has a
  `Disposition` of `deferred` or `decided`, or contains `not_requested` / `signed` /
  `assinado` (i.e. the TA status is explicitly accounted for, not left blank).

A run must pass **all** structural checks to be eligible for qualitative scoring.

### Process checks (from `fanout.py`, on the run trace)

These grade *how* the journey ran, not just the artifact:

- `triage_present` — Act 1 ran the gate proposer (`hsb-triage-assessor`) before any
  RP drafting. A Product Ready run must show triage first; a `Discovery`/`Backlog`/
  `Reject` run short-circuits after it (no `hsb-section-drafter`, no
  `readiness-document.md`).
- `drafter_fanout_in_turn ≥ 2` — the Act 2 draft pass fanned out section drafters in
  parallel (one per product section) rather than one serial drafter. This is the
  process signal for the efficiency fix.
- `fanout_pass` — ≥ 3 CORE agents ran AND at least one turn spawned ≥ 2 agents.

## Layer 2 — qualitative (LLM-graded, 1-5 each)

Grade the produced document against `grounding.md` and the golden (when present).
For an LLM grader, prompt: *"Score 1-5 and justify, citing the text."*

| Dimension | 5 = excellent | 1 = poor |
|---|---|---|
| **Problem = pain, not solution** | Sections 1–2 frame the demand as observable pain + business impact with zero solution language | Names a feature / prescribes implementation instead of the underlying pain |
| **Confidence + Origin honesty** | Inherited sections preserve the origination's confidence number and `Origin=inherited`; ai_drafted sections stay at partial confidence (≤ 85) with a real hint; no flat 90+ on ai_drafted fields | Inherited sections claim lower/higher confidence without justification; ai_drafted sections claim certainty they don't have; hints absent |
| **Dispositions used well** | Genuine gaps routed to `assumption`/`discovery`/`deferred` with an owner or a note on what would resolve them; no fake-filled sections | Gaps left blank, or filled with placeholder content, or disposition missing |
| **Testable Given/When/Then acceptance criteria** | Each user story's ACs are expressed in Given/When/Then with specific, numeric bounds (e.g. ≤ 60 s, HTTP 403), verifiable by a non-developer | Vague ACs ("it works", "no errors"), missing bounds, or no Given/When/Then format |
| **NFRs that don't claim feasibility** | NFR section describes the *quality requirement* (what the PO needs); explicitly defers implementation and viability to the Technical Assessment | NFRs prescribe solutions, claim architectural feasibility, or omit the TA deferral |
| **Escalation called correctly** | CTO escalation detected and `tech-assessment-ref` carries `Disposition=deferred` when a TA is owed; `not_requested` when no escalation is needed; consistent with complexity signals in scope/business-rules/NFRs | Escalation missed on a billing/provisioning feature, or incorrectly triggered on a trivial feature; TA ref left blank or unresolved |
| **Triage gate correctness** (Act 1) | Intake Record commits one routing decision (`Product Ready`/`Discovery`/`Backlog`/`Reject`) with the full decision model (`verdict`/`rationale`/`basis`/`source`/`reversible`); only `Product Ready` proceeds to the RP, the others short-circuit with a recorded rationale; questions asked only on criteria the assessor couldn't settle | Decision missing or unjustified; a non-`Product Ready` demand still ran the full RP pipeline; or the demand was pre-interpreted as product with no triage |
| **Fidelity to the golden** (eval-0 only) | Same structural decisions as the golden (same blocking sections resolved, same escalation call, same scope boundaries); confidence texture comparable | Diverges on a key decision (e.g. skips escalation, drops a blocking section) without justification |

## Scorecard

`run.sh` (or the runner) compiles, per iteration:
- structural pass/fail + readiness % per case,
- with-skill vs baseline delta (does the skill add lift over no-skill?),
- qualitative 1-5 per dimension (filled by the grader).

Target bar: 100% structural pass; qualitative mean ≥ 4.0; with-skill readiness
meaningfully above baseline.
