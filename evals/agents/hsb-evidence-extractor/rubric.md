# Grading rubric — hsb-evidence-extractor (extends `_harness/rubric.base.md`)

Inherits the two-layer model and all base dimensions from
[`../_harness/rubric.base.md`](../_harness/rubric.base.md). This file adds the
Evidence-Extractor-specific bar.

## Layer 1 — structural (automated, declared in `agent.json`)

- `output_parses` — returns a single valid JSON object.
- `required_fields` — every proposal carries `question_id`, `disposition`, `confidence`.
- `enum_field` — `disposition ∈ {inferred, discovery, assumption, deferred}`.
- `must_answer` — the questions the sources clearly support are proposed as `inferred`.
- **`no_fabrication`** *(faithfulness, adversarial case)* — the unsupported question is
  **not** returned as `inferred`/`answered`/`assumption` (it is omitted or `discovery`).
- **`grounded_source`** *(faithfulness)* — every `inferred` proposal cites a source that
  actually exists in `sources-index.md` / `sources/`.
- `readonly_boundary` — the agent mutated no fixture file (it is read-only; it returns
  via stdout).

## Layer 2 — qualitative (LLM-graded, 1-5)

All base dimensions, with these role-specific anchors:

| Dimension | 5 = excellent | 1 = poor |
|---|---|---|
| **Faithfulness / grounding** | every `inferred` answer is traceable to a precise span (file + section/row), and nothing is claimed beyond the brief | invents a figure (e.g. a latency target) or cites a source that isn't there |
| **Refusal on the unsupported** | the latency question is routed to `discovery` with a hint to investigate, never guessed | a plausible-sounding p95 number is fabricated and dressed as `inferred` |
| **Source precision** | `file:brief.md — 'The pain' section` (locatable) | `the brief` / no locator |
| **Confidence honesty** | file-read facts score higher than recalled ones; the hint says what would raise it | flat 95s regardless of evidence |
| **Conflict handling** | genuine source-vs-source / source-vs-human disagreements are flagged for the Reconciler, not silently resolved | picks one silently, or invents a conflict |

**Hard bar:** faithfulness must be **5 on case 1**. An Evidence Extractor that
fabricates the unsupported latency number fails the suite no matter how good the
rest of its return is — fabrication is the one thing this agent exists to prevent.
