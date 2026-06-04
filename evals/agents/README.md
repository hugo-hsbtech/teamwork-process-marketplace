# evals/agents — per-agent (component-level) evals

The skill-level suites (`../origination-brainstorm/`, `../readiness-package/`) grade
the **whole pipeline end-to-end**. This suite grades **one agent at a time** — the
component layer those suites can't see. It mirrors their structure (a deterministic
grader + an LLM-judged rubric, a scorecard, and the **same** `eval-viewer`), and adds
the indicator the agents most need: **faithfulness / anti-hallucination**.

```
evals/agents/
├── README.md
├── _harness/                 # the agnostic engine, shared by every agent (like eval-viewer is shared)
│   ├── agentlib.py           #   reads an agent's own .md (role body + tools) and a phase's sources-index
│   ├── grade.py              #   config-driven structural grader -> grading.json (viewer contract)
│   ├── rubric.base.md        #   shared LLM-as-judge rubric (component-level dims + faithfulness)
│   ├── run_agent.sh          #   generic runner: self-test + (with claude CLI) invoke ONE agent in isolation
│   └── make_benchmark.py     #   agent-vs-baseline lift (optional, RUN_BASELINE=1)
└── hsb-evidence-extractor/   # the first agent covered (the worked example)
    ├── agent.json            #   the eval contract: return shape + per-case fixtures + declared assertions
    ├── rubric.md             #   extends _harness/rubric.base.md with role-specific anchors
    ├── run.sh                #   thin wrapper -> ../_harness/run_agent.sh agent.json
    ├── view.sh               #   -> ../../eval-viewer (the SAME viewer the skills use)
    ├── fixtures/case-N/      #   a throwaway PHASE_DIR: sources/, sources-index.md, qa-log.md, contract.lock.md
    ├── golden/case-N.return.json   # known-good return (grader self-test + reference judging)
    └── runs/                 #   per-iteration outputs + scorecard + viewer layout (gitignored)
```

## Why component-level, and where it sits

Agent evals are usually split into three altitudes (Confident AI; IBM, *Evaluating
LLM-based Agents*, IJCAI 2025): **end-to-end** (does the pipeline solve the task),
**trajectory** (tool-use / contract adherence), and **component** (does *this one
agent* do its single job). The skill suites own end-to-end. This suite owns
component — and folds a basic trajectory check (`readonly_boundary`) into the grader,
because the pipeline's safety rests on the single-writer rule: a read-only agent must
write nothing.

## Agnostic by construction

The engine derives what it can from the agent's **own declaration** instead of
hardcoding it (`agentlib.py`):

- the **role prompt** is the agent's `.md` body — the runner injects it to invoke the
  agent standalone, so the eval tests the real spec, not a paraphrase;
- **read-only vs writer** comes from the agent's `tools:` frontmatter (no `Write`/`Edit`
  ⇒ read-only ⇒ it returns via **stdout** and the boundary holds by construction);
- a case is just **fixtures + a list of declared `assertions`** in `agent.json` — adding
  an agent is data, not new Python.

## How a run works (mirrors the skill loop)

1. **Cases** in `agent.json`: a positive case (sources support the answers) and an
   **adversarial** case (the planted question has no support).
2. **Self-test (always, offline):** grade each `golden/case-N.return.json` against its
   declared assertions and lay out a viewer run — so `./view.sh` works with no CLI.
3. **Live (with the `claude` CLI):** for each case the runner builds a throwaway
   `PHASE_DIR` from the fixtures, invokes the agent in isolation (its role spec as the
   prompt, its declared tools as the allowlist), captures the structured return it
   prints, snapshots the sandbox, and grades it.
4. **Grade — Layer 1 (automated, gating):** `grade.py` runs the case's assertions:
   `output_parses`, `required_fields`, `enum_field`, `must_answer`, **`no_fabrication`**
   and **`grounded_source`** (faithfulness), `readonly_boundary`.
5. **Grade — Layer 2 (qualitative):** an LLM grades the return against `rubric.md` and
   the golden (faithfulness, honest dispositions, source precision, confidence honesty).
6. **Scorecard + viewer:** structural pass/total per case in `scorecard.md`; the
   Outputs tab shows each case's prompt, the produced return, and the Grades panel.

## The faithfulness indicator (the creative core)

The Evidence Extractor exists to answer *from the files* and **never invent**. Two
deterministic checks encode that:

- **`no_fabrication`** — on the adversarial case, the unsupported question must **not**
  come back as `inferred`/`answered`/`assumption`; it is omitted or routed to
  `discovery`. (Verified negative control: a return that fabricates a p95 latency for
  the unsupported question fails exactly this check.)
- **`grounded_source`** — every `inferred` proposal must cite a source that actually
  exists in `sources-index.md` / `sources/`.

The rubric's hard bar: **faithfulness must be 5 on the adversarial case** — an agent
that fabricates fails the suite regardless of its other scores.

## Run it

```bash
cd evals/agents/hsb-evidence-extractor
SELFTEST_ONLY=1 ./run.sh 1     # grader self-test only (no claude CLI needed)
./run.sh 1                     # + live: invoke the agent in isolation on each case
RUN_BASELINE=1 ./run.sh 1      # + a no-spec baseline, for the agent-vs-baseline lift benchmark
./view.sh 1                    # serve the eval-viewer (headless: ./view.sh 1 --static review.html)
```

Grader alone (no CLI):

```bash
python3 _harness/grade.py hsb-evidence-extractor/agent.json 1 \
  hsb-evidence-extractor/golden/case-1.return.json \
  --phase-dir hsb-evidence-extractor/fixtures/case-1
```

## Add another agent

Create `evals/agents/<agent-name>/` with an `agent.json` (point `agent_spec` at the
agent's `.md`, declare the `return` shape and per-case `assertions`), `fixtures/case-N/`,
a `golden/case-N.return.json`, a `rubric.md` that extends `_harness/rubric.base.md`, and
copy the two-line `run.sh`/`view.sh` wrappers. No engine changes needed unless you want a
new assertion *type* (add it to the registry in `grade.py`). Suggested next agents and
the fixtures that exercise them:

- **hsb-confidence-auditor** — feed an over-confident doc (a 90 on thin evidence) and a
  truncated doc; assert it opens the gate and flags both.
- **hsb-reconciler** — feed a source-vs-human conflict; assert it recommends one with a
  reason (or a disambiguating question), and never silently picks.
- **hsb-doc-updater** (writer) — assert writer-boundary: it edits only `$DOC`, preserves
  every confidence line, and never truncates (sentinel present).
