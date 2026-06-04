# evals — repo-level (dev/CI only)

Evaluation harness for the `hsb-teamwork` skills. **Not shipped in the plugin** —
this is a development concern (test a skill before releasing it), so it lives at
the repo root, like Claude's `skill-creator` keeps evals beside the skill.

```
evals/
├── eval-viewer/        # vendored from skill-creator (Apache-2.0): local web UI to
│   │                   #   review runs, grades, and a with-skill-vs-baseline benchmark
│   ├── generate_review.py
│   ├── viewer.html
│   ├── LICENSE.txt
│   └── README.md
└── intake-brainstorm/
    ├── evals.json      # test cases (prompt + files + golden + expected_output)
    ├── rubric.md       # grading: Layer 1 structural (auto) + Layer 2 qualitative (LLM)
    ├── assertions.py   # the deterministic structural grader (no LLM needed)
    ├── make_benchmark.py  # aggregate grading.json files -> benchmark.json (viewer)
    ├── run.sh          # runner: self-test + (with claude CLI) live cases -> scorecard
    ├── view.sh         # launch the eval-viewer on an iteration's runs
    ├── golden/         # expected outputs (also grader fixtures)
    ├── fixtures/       # seeds (e.g. an under-filled doc for the revisit case)
    └── runs/           # per-iteration outputs + scorecard + viewer layout (gitignored)
```

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
cd evals/intake-brainstorm
./run.sh            # self-tests the grader; runs live cases if the `claude` CLI is present
```

The grader alone (no CLI needed):

```bash
python3 assertions.py golden/queue-voting.target-document.md
```

## Review runs in the eval-viewer

`run.sh` also writes each run in the layout the **eval-viewer** reads
(`runs/iteration-N/.../outputs/` + `eval_metadata.json` + `grading.json`, plus a
workspace `benchmark.json`). Launch the UI:

```bash
cd evals/intake-brainstorm
./view.sh 1                       # serve at http://localhost:3117 (opens a browser)
./view.sh 1 --static review.html  # headless/remote: write a standalone HTML file
```

It has an **Outputs** tab (each case's prompt, produced document, and pass/fail
grades) and a **Benchmark** tab (with-skill vs. baseline pass rates). Even with no
`claude` CLI, `run.sh` lays out a golden self-test run so the viewer is
demonstrable. See `../eval-viewer/README.md` for the data contract and provenance.

## Add a case

Append to `evals.json` (id, name, prompt with `{OUT}` placeholder, files, optional
golden/seed, expected_output). Add a golden under `golden/` when you want fidelity
scoring. Keep prompts non-interactive (gaps become honest dispositions) so cases
run headlessly.
