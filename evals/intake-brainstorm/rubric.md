# Grading rubric — intake-brainstorm

Two layers. **Structural** is automated (`assertions.py`, deterministic, gates the
run). **Qualitative** is LLM-graded against the golden bar (judgment, scored 1-5).

## Layer 1 — structural (automated, pass/fail)

Run by `assertions.py` on each produced `target-document.md`:

- `sentinel_present` — ends with `<!-- END OF DOCUMENT -->` (no truncation).
- `no_truncation_markers` — no `...` / `(unchanged)` / leftover `[fill]` placeholders.
- `has_annotations` — section annotations preserved.
- `blocking[<id>]_satisfied` — every `blocks=true` capture section is ≥ its
  `min-confidence` (direct answer) or carries an honest disposition
  (assumption/discovery/deferred).
- `confidence_lines_present` — capture sections with `min-confidence>0` carry the
  `Confidence/Source/Status/Disposition/Hint` line.
- `triage_flagged_draft` — the triage section carries the DRAFT-pending-confirmation banner.

A run must pass **all** structural checks to be eligible for qualitative scoring.

## Layer 2 — qualitative (LLM-graded, 1-5 each)

Grade the produced document against `grounding.md` and the golden (when present).
For an LLM grader, prompt: *"Score 1-5 and justify, citing the text."*

| Dimension | 5 = excellent | 1 = poor |
|---|---|---|
| **Problem = pain, not solution** | concrete pain + observable symptoms, zero solution language | names a feature / prescribes implementation |
| **Confidence honesty** | mid-range where evidence is soft, high only where sourced; every soft field has a real hint | flat 95s, or no hints |
| **Dispositions used well** | unknowns routed to assumption/discovery/deferred with owners/time-box | gaps left empty, or fake-answered |
| **Tensions registered** | RICE-lite tensions surfaced and resolved | ignored |
| **Triage defensibility** | each criterion traces to evidence; routing rationale would survive a PO reading cold; clearly a flagged draft | unsupported verdicts, or presented as final |
| **Fidelity to golden** (when one exists) | same decision + comparable confidence texture | diverges on decision without justification |

## Scorecard

`score.py` (or the runner) compiles, per iteration:
- structural pass/fail + readiness % per case,
- with-skill vs baseline delta (does the skill add lift over no-skill?),
- qualitative 1-5 per dimension (filled by the grader).

Target bar: 100% structural pass; qualitative mean ≥ 4.0; with-skill readiness
meaningfully above baseline.
