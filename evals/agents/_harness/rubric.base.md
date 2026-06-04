# Base grading rubric — per-agent evals (shared)

Two layers, mirroring the skill-level evals. **Structural** is automated and gates
the run (`grade.py`, deterministic, config-driven per `agent.json`). **Qualitative**
is LLM-graded against the golden return (judgment, 1-5). Each agent's `rubric.md`
*extends* this file with role-specific dimensions; the dimensions below apply to
every agent and encode the per-component evaluation practices the harness targets.

## Where this fits the market taxonomy

Agent evals are commonly split into three altitudes (Confident AI, IBM "Evaluating
LLM-based Agents", 2025):

| Altitude | What it scores | Who owns it here |
|---|---|---|
| **End-to-end** | does the whole pipeline solve the task | the skill-level evals (`evals/origination-brainstorm`, `evals/readiness-package`) |
| **Trajectory** | tool-use correctness, boundary/contract adherence | `readonly_boundary` / writer-boundary checks in `grade.py` |
| **Component** | does *this one agent* do its single job well | **this harness** — structural `grade.py` + the rubric below |

This harness is the **component-level** layer the skill-level suites can't see: it
isolates one agent, feeds it a fixture, and grades its return on its own contract.

## Layer 1 — structural (automated, pass/fail)

Declared per case in `agent.json` and run by `grade.py`. A run must pass **all**
structural assertions to be eligible for qualitative scoring. The assertion types:
`output_parses`, `required_fields`, `enum_field`, `must_answer`, `no_fabrication`,
`grounded_source`, `readonly_boundary` (documented at the top of `grade.py`).

## Layer 2 — qualitative (LLM-graded, 1-5 each)

Grade the agent's produced return against this rubric and the golden return (when
present). Prompt the judge: *"Score 1-5 and justify, **citing the agent's return
text and the fixture sources**."* Best-practice guardrails for the judge:

- **Reference-based when a golden exists** — comparing to a known-good return is more
  reliable than scoring in the abstract.
- **Chain-of-thought, then score** — make the judge state its reasoning before the
  number; it improves calibration and makes disagreements debuggable.
- **Counter position/verbosity bias** — when comparing two returns, score both orders
  and average; never reward length over substance.
- **Calibrate against the golden's bar** and track judge-vs-human agreement over
  iterations; treat a dimension as trustworthy only once agreement is high.

| Dimension | 5 = excellent | 1 = poor |
|---|---|---|
| **Faithfulness / grounding** | every claim traces to a real span in the provided fixtures; no detail beyond what the sources support | invents facts, numbers, or citations the sources don't contain |
| **Honest dispositions** | unsupported items are routed to `discovery`/`assumption`/`deferred` (or omitted), never dressed up as a confident answer | fakes an answer, or leaves a real gap silent |
| **Contract adherence** | return matches the agent's declared output shape; respects its read-only/single-writer boundary | malformed return, or wrote outside its lane |
| **Confidence honesty** | confidence tracks evidence strength; a figure read from a file scores higher than a recalled one, and the hint says why | flat high confidence regardless of evidence; empty/again-useless hints |
| **Task focus** | does exactly its one job at the right altitude; doesn't bleed into another agent's role | drifts into another agent's responsibility, or under/over-reaches |
| **Fidelity to golden** (when one exists) | same decisions + comparable confidence texture as the golden | diverges from the golden without justification |

## Scorecard

Per iteration, the runner compiles structural pass/fail + pass-rate per case; the
LLM grader appends the 1-5 qualitative scores. Target bar: **100% structural pass;
qualitative mean ≥ 4.0**, with **faithfulness == 5 on every adversarial case** (an
agent that fabricates on an unsupported question fails the suite regardless of its
other scores).
