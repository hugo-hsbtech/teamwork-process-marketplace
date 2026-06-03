# evals — repo-level (dev/CI only)

Evaluation harness for the `hsb-teamwork` skills. **Not shipped in the plugin** —
this is a development concern (test a skill before releasing it), so it lives at
the repo root, like Claude's `skill-creator` keeps evals beside the skill.

```
evals/
└── intake-brainstorm/
    ├── evals.json      # test cases (prompt + files + golden + expected_output)
    ├── rubric.md       # grading: Layer 1 structural (auto) + Layer 2 qualitative (LLM)
    ├── assertions.py   # the deterministic structural grader (no LLM needed)
    ├── run.sh          # runner: self-test + (with claude CLI) live cases -> scorecard
    ├── golden/         # expected outputs (also grader fixtures)
    ├── fixtures/       # seeds (e.g. an under-filled doc for the revisit case)
    └── runs/           # per-iteration outputs + scorecard (gitignored)
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

## Add a case

Append to `evals.json` (id, name, prompt with `{OUT}` placeholder, files, optional
golden/seed, expected_output). Add a golden under `golden/` when you want fidelity
scoring. Keep prompts non-interactive (gaps become honest dispositions) so cases
run headlessly.
