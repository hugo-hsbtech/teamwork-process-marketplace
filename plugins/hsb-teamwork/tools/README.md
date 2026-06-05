# tools — pipeline graph

Declarative dependency graphs for the hsb-teamwork agent pipelines, and the validator
that turns them into machine-checked invariants.

## Why

The agents in a skill form a dependency graph: each reads some logical datums and
decides others, single writers own files, and a few proposers draft *provisionally*
before the decision they depend on exists. Encoding that as **data** (a `pipeline.yaml`
per skill) instead of only prose lets a tool enforce the invariants that otherwise
depend on the orchestrator getting the prose right:

- one physical writer per file,
- one logical decider per datum (the override guard),
- no dangling reads,
- acyclic hard edges,
- every provisional output has a reconciliation rule (the draft-before-the-decision guard).

See `skills/tech-assessment/references/scheduling.md` for the full model.

## Use

```bash
# validate one graph, print the computed parallel schedule
python3 tools/pipeline_graph.py skills/tech-assessment/pipeline.yaml

# also emit a Mermaid diagram (solid = hard reads, dashed = provisional)
python3 tools/pipeline_graph.py skills/tech-assessment/pipeline.yaml --mermaid

# CI gate: validate every skills/*/pipeline.yaml, non-zero on any failure
tools/check_pipelines.sh
```

Requires Python 3 and PyYAML.

## Status

All five skills are modeled:

| Skill | Graph(s) |
|---|---|
| origination-brainstorm | `pipeline.yaml` |
| readiness-package | `pipeline.intake.yaml` (Act 1) + `pipeline.readiness.yaml` (Act 2) |
| tech-assessment | `pipeline.yaml` (carries the provisional-before-the-verdict case) |
| prd-generation | `pipeline.yaml` |
| initiative-analytics | `pipeline.yaml` |

`check_pipelines.sh` globs `skills/*/pipeline*.yaml`, so new graphs are picked up
automatically. The shared model doc is
`skills/tech-assessment/references/scheduling.md`.
