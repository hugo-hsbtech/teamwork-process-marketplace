# eval-viewer

Shared review tooling for every `hsb-teamwork` eval set (`../origination-brainstorm/`,
`../readiness-package/`, …). A zero-dependency (Python stdlib only) local web app
for reviewing eval runs: each test case's prompt + produced files inline, a per-run
**Grades** panel, a **Benchmark** tab (with-skill vs. baseline pass rates), and a
feedback textbox per run that saves to `feedback.json` for the next iteration.

## Provenance

`generate_review.py` and `viewer.html` are vendored from Anthropic's `skill-creator`
skill (<https://github.com/anthropics/skills/tree/main/skills/skill-creator/eval-viewer>),
Apache-2.0 (see `LICENSE.txt`), and kept **unmodified** so we can re-sync upstream.
The project glue is `make_benchmark.py` (here, shared) plus each skill's `run.sh`,
`view.sh`, and `assertions.py --grading-json`, which produce the layout below.

## Data contract (what our harness emits)

The viewer treats any directory containing an `outputs/` subdir as a *run*:

```
runs/iteration-N/
├── benchmark.json                 # optional, Benchmark tab (--benchmark)
├── feedback.json                  # written by the viewer on save
├── golden-selftest/
│   ├── eval_metadata.json         # {eval_id, prompt}
│   ├── grading.json               # {summary, expectations:[{text,passed,evidence}]}
│   └── outputs/<doc>.md           # target-document.md or readiness-document.md
└── eval-<id>/
    ├── with_skill/  { eval_metadata.json, grading.json, outputs/ }
    └── baseline/    { eval_metadata.json, grading.json, outputs/ }
```

Run-dir extras the viewer ignores (only `outputs/` is shown): `seed.md`,
`agent.log`, and — for `readiness-package` — `trace.jsonl` / `fanout.json`.

- `eval_metadata.json` — `{"eval_id": <int>, "prompt": "..."}` (keep ids integer;
  the golden self-test uses `-1`).
- `grading.json` — `{"summary": {pass_rate, passed, failed, total},
  "expectations": [{"text", "passed", "evidence"}]}` (from `assertions.py --grading-json`).
- `benchmark.json` — `{metadata, run_summary:{with_skill, baseline, delta}, runs, notes}`
  (from `make_benchmark.py`, which scans `eval-*/{with_skill,baseline}/grading.json`).

## Usage

From any skill's eval dir (`../origination-brainstorm/`, `../readiness-package/`):

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
