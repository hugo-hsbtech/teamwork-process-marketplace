# eval-viewer

A zero-dependency (Python stdlib only) local web app for reviewing eval runs:
each test case's prompt + produced files inline, a per-run **Grades** panel, a
**Benchmark** tab (with-skill vs. baseline pass rates), and a feedback textbox
per run that saves to `feedback.json` for the next iteration to show as context.

## Provenance

Vendored from Anthropic's `skill-creator` skill
(<https://github.com/anthropics/skills/tree/main/skills/skill-creator/eval-viewer>),
Apache-2.0 (see `LICENSE.txt`). `generate_review.py` and `viewer.html` are
**unmodified** so we can re-sync upstream; our project-specific glue lives in
`../intake-brainstorm/` (run.sh, make_benchmark.py, view.sh, assertions.py
`--grading-json`), which produces the layout the viewer reads.

## Data contract (what our harness emits)

The viewer treats any directory containing an `outputs/` subdir as a *run*:

```
runs/iteration-N/
├── benchmark.json                 # optional, Benchmark tab (--benchmark)
├── feedback.json                  # written by the viewer on save
├── golden-selftest/
│   ├── eval_metadata.json         # {eval_id, prompt}
│   ├── grading.json               # {summary, expectations:[{text,passed,evidence}]}
│   └── outputs/target-document.md
└── eval-<id>/
    ├── with_skill/  { eval_metadata.json, grading.json, outputs/ }
    └── baseline/    { eval_metadata.json, grading.json, outputs/ }
```

- `eval_metadata.json` — `{"eval_id": <int|str>, "prompt": "..."}`.
- `grading.json` — `{"summary": {pass_rate, passed, failed, total},
  "expectations": [{"text", "passed", "evidence"}]}` (from `assertions.py --grading-json`).
- `benchmark.json` — `{metadata, run_summary:{with_skill, baseline, delta}, runs, notes}`
  (from `make_benchmark.py`).

## Usage

From `../intake-brainstorm/`:

```bash
./view.sh 1                       # serve at http://localhost:3117, opens a browser
./view.sh 1 --static review.html  # headless/remote: write a standalone HTML file
```

Or directly:

```bash
python3 generate_review.py <workspace> --skill-name NAME \
  [--benchmark <workspace>/benchmark.json] [--static out.html]
```

`--static` is the right mode in headless/CI/remote containers (no browser, no
long-lived server): it embeds everything into one self-contained HTML file.
