# evals — repo-level (dev/CI only)

Evaluation harness for the `hsb-teamwork` skills. **Not shipped in the plugin** —
this is a development concern (test a skill before releasing it), so it lives at
the repo root, like Claude's `skill-creator` keeps evals beside the skill.

```
evals/
├── eval-viewer/        # shared tooling, vendored from skill-creator (Apache-2.0):
│   ├── generate_review.py  #   local web UI to review runs + grades
│   ├── viewer.html         #   the UI template (with-skill-vs-baseline benchmark tab)
│   ├── make_benchmark.py   #   aggregate per-run grading.json -> benchmark.json
│   ├── LICENSE.txt
│   └── README.md
├── origination-brainstorm/
│   ├── evals.json      # test cases (prompt + files + golden + expected_output)
│   ├── rubric.md       # grading: Layer 1 structural (auto) + Layer 2 qualitative (LLM)
│   ├── assertions.py   # the deterministic structural grader (--grading-json for the viewer)
│   ├── run.sh          # runner: self-test + (with claude CLI) live cases -> scorecard + viewer layout
│   ├── view.sh         # launch the eval-viewer on an iteration's runs
│   ├── golden/         # expected outputs (also grader fixtures)
│   ├── fixtures/       # seeds (e.g. an under-filled doc for the revisit case)
│   └── runs/           # per-iteration outputs + scorecard + viewer layout (gitignored)
└── readiness-package/
    ├── evals.json      # test cases: origination-record -> RP (fresh) + revisit underfilled RP
    ├── rubric.md       # grading: Layer 1 structural (auto) + Layer 2 qualitative (LLM)
    ├── assertions.py   # deterministic structural grader (--grading-json for the viewer)
    ├── fanout.py       # fan-out detector: did the skill actually orchestrate subagents?
    ├── run.sh          # runner: self-test + (with claude CLI) live cases -> scorecard + viewer layout
    ├── view.sh         # launch the eval-viewer on an iteration's runs
    ├── golden/         # seat-management.readiness-document.md (reference output)
    ├── fixtures/       # origination-record input + underfilled RP seed for revisit case
    └── runs/           # per-iteration outputs + scorecard (gitignored)
```

`readiness-package/` grades the `origination-record → RP` pipeline: structural checks
via `assertions.py` (sentinel, annotations, blocking sections, Origin tags,
tech-assessment-ref resolution), a fan-out check via `fanout.py` (the orchestrator
actually spawned its subagents, in parallel), and qualitative scoring via `rubric.md`.

## How it works (mirrors skill-creator's loop)

1. **Cases** in `evals.json`: fresh one-liner, file-grounded, revisit, batch.
2. **Run** each case headlessly **with the skill** and a **baseline** (no skill),
   saving each to `runs/iteration-N/eval-K/{with_skill,baseline}/`.
3. **Grade**:
   - *Layer 1 (automated, gating):* `assertions.py` checks the contract on the
     produced `target-document.md` — sentinel/no-truncation, every blocking
     section resolved-or-disposed, confidence lines, triage flagged draft.
   - *Layer 2 (qualitative):* an LLM grades against `rubric.md` and the golden
     (problem-not-solution, honest confidence, dispositions, defensible triage).
4. **Scorecard** per iteration: structural pass + readiness %, with-skill vs
   baseline delta, and the 1-5 qualitative scores.

## Run it

```bash
cd evals/origination-brainstorm
./run.sh            # self-tests the grader; runs live cases if the `claude` CLI is present
```

The grader alone (no CLI needed):

```bash
python3 assertions.py golden/queue-voting.target-document.md
```

## Review runs in the eval-viewer

Both skills feed the **shared** `eval-viewer/`. Each `run.sh` writes its runs in
the layout the viewer reads (`runs/iteration-N/.../outputs/` + `eval_metadata.json`
+ `grading.json`, plus a workspace `benchmark.json` built by
`eval-viewer/make_benchmark.py`). Launch the UI from either skill dir:

```bash
cd evals/origination-brainstorm   # or: cd evals/readiness-package
./view.sh 1                       # serve at http://localhost:3117 (opens a browser)
./view.sh 1 --static review.html  # headless/remote: write a standalone HTML file
```

It has an **Outputs** tab (each case's prompt, produced document, and pass/fail
grades) and a **Benchmark** tab (with-skill vs. baseline pass rates). Even with no
`claude` CLI, `run.sh` lays out a golden self-test run so the viewer is
demonstrable. See `eval-viewer/README.md` for the data contract and provenance.

## Add a case

Append to `evals.json` (id, name, prompt with `{OUT}` placeholder, files, optional
golden/seed, expected_output). Add a golden under `golden/` when you want fidelity
scoring. Keep prompts non-interactive (gaps become honest dispositions) so cases
run headlessly.
