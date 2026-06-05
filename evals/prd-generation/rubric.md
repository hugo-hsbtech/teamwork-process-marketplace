# Grading rubric — prd-generation

Two layers. **Structural** is automated (`assertions.py`, deterministic, gates the run).
**Qualitative** is LLM-graded against the golden bar (judgment, scored 1-5).

The PRD is a **merge**: Part A is inherited from the Readiness Package (product, PO), Part B
from the Technical Assessment (technical, CTO), and the derived sections are synthesized from
both halves. The grader's spine is that the merge **preserves authorship, invents no facts, and
reconciles the two halves** — it is not a staple.

## Layer 1 — structural (automated, pass/fail)

Run by `assertions.py` on each produced `prd-document.md`:

- `sentinel_present` — ends with `<!-- END OF DOCUMENT -->` (no truncation).
- `no_truncation_markers` — no `...` / `(unchanged)` / leftover `[fill]` / `[Summary here]`
  placeholders.
- `has_annotations` — section annotations preserved (≥ 20 annotated sections).
- `merge_sections_present` — the sections that make a PRD a *merge* are all present:
  `exec-summary`, `scope-reconciliation`, `consolidated-risk`, `handoff-gate`, `sign-off`.
- `blocking[<id>]_satisfied` — every `blocks=true` section (capture **and** derived) is ≥ its
  `min-confidence` (direct answer) or carries an honest disposition. Blocking sections:
  `sign-off`, `exec-summary`, `a-objectives`, `a-scope`, `a-personas`, `a-journey`,
  `a-business-rules`, `a-user-stories`, `a-nfrs`, `a-edge-cases`, `b-feasibility`,
  `b-nature-landscape`, `b-arch-impact`, `b-nfr-feasibility`, `b-hard-constraints`, `b-adrs`,
  `scope-reconciliation`, `consolidated-risk`, `effort-cost`, `inherited-readiness`,
  `success-metrics`, `handoff-gate`. On the no-escalation path the Part B sections clear via
  `Disposition: decided` ("N/A — no architectural escalation").
- `confidence_lines_present` — capture/derived sections with `min-confidence>0` carry the
  `Confidence/Origin/Source/Status/Disposition/Hint` line.
- `origin_present_valid` — every blocking section's `Origin` is drawn from the allowed set
  (`inherited`, `synthesized`, `po_authored`, `cto_authored`, `decided`).
- `dual_signoff_present` — the `sign-off` section names both a PO row and a CTO row (the CTO row
  may be an honest N/A on the no-escalation path).

A run must pass **all** structural checks to be eligible for qualitative scoring.

### Process checks (from `fanout.py`, on the run trace)

These grade *how* the merge ran, not just the artifact:

- `reconciler_present` — the Reconciler (`hsb-reconciler`) ran. A PRD reconciles the two halves;
  a run that never reconciles is a staple, not a merge.
- `inheritor_fanout_in_turn ≥ 2` — the Inheritor fanned out Part A ∥ Part B in one turn (rather
  than one serial pass), proving the two halves were carried in parallel.
- `synthesizer_fanout_in_turn` — the derived sections fanned out (reported; not gated).
- `fanout_pass` — ≥ 3 CORE agents ran AND at least one turn spawned ≥ 2 agents in parallel.

## Layer 2 — qualitative (LLM-graded, 1-5 each)

Grade the produced document against `grounding.md` and the golden (when present). For an LLM
grader, prompt: *"Score 1-5 and justify, citing the text."*

| Dimension | 5 = excellent | 1 = poor |
|---|---|---|
| **Invents no facts** | Every product fact traces to the RP and every technical fact to the TA; the merge adds only composition (exec summary), combination (risk view), and reconciliation (scope) | New requirements, risks, or constraints appear that are in neither source half |
| **Preserves authorship** | Part A reads as the PO's product definition, Part B as the CTO's technical definition; neither half rewrites the other | The PRD re-judges feasibility, re-defines the product, or blends the two voices into one re-authored document |
| **Verdict carried, not re-decided** | `b-feasibility` and the CTO sign-off carry the TA's exact verdict + caveats; no new verdict is computed | The PRD states a verdict the TA did not give, or "upgrades"/"downgrades" the caveats |
| **Scope is reconciled, not stapled** | `scope-reconciliation` records the delta the TA's constraints/caveats imposed, **and** `a-scope` reflects the reconciled result (the A.2 ↔ reconciliation invariant) | The reconciliation table is empty or generic while a TA constraint clearly changed the scope; or A.2 still lists a deferred item as included |
| **Consistency invariants hold** | Every `a-nfrs` NFR has a matching `b-nfr-feasibility` answer (or Part B is the N/A path); risks from both halves appear once, tagged by origin | A declared NFR has no feasibility answer; risks are duplicated or untagged |
| **Honest dispositions** | The no-escalation path disposes Part B `decided` N/A; surviving assumptions/Discovery/delegated items appear in `inherited-readiness` with owners | Part B is blank or faked on the no-escalation path; open dispositions are dropped instead of surfaced |
| **Handoff is checkable** | Every `handoff-gate` box is verifiable from the document; dual sign-off present (or CTO honestly N/A); priority/business context stated | Checklist boxes ticked that the document does not support; sign-off missing |
| **Fidelity to the golden** (eval-0 only) | Same merge decisions as the golden (same Part A/B carry-forward, same scope deferral, same verdict, same risk consolidation) | Diverges on a key merge decision (drops the SSO/SCIM deferral, re-decides the verdict, loses a blocking section) without justification |

## Scorecard

`run.sh` (or the runner) compiles, per iteration:
- structural pass/fail + readiness % per case,
- with-skill vs baseline delta (does the skill add lift over no-skill?),
- qualitative 1-5 per dimension (filled by the grader).

Target bar: 100% structural pass; qualitative mean ≥ 4.0; with-skill `fanout_pass` true while
the baseline stays inline.
