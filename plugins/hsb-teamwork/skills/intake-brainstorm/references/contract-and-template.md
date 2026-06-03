# Contract & template — the target template *is* the contract

The skill fills a **target template**. The template is the source of truth: its
sections, the explanation under each, and a little machine-readable metadata
*are* the contract the whole pipeline runs against. Swap the template and you swap
the contract — no code changes. This is what makes the skill portable across
projects and document types.

## Template annotation format

Each fillable section carries a one-line HTML-comment annotation directly under
its heading. It is invisible in rendered Markdown and survives editing:

```markdown
## Problem statement
<!-- intake: id=problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: describe the existing pain with observable symptoms, without
> prescribing a solution. A confident answer names what hurts, for whom, and how
> it shows up today.

[fill here]

`Confidence:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __
```

Annotation fields:

| Field | Meaning |
|---|---|
| `id` | stable key for the section (used by the ledger to bind questions/answers) |
| `blocks` | `true` = the gate cannot clear until this section is resolved or honestly disposed |
| `min-confidence` | the **X%** threshold a *direct* answer must meet to count as resolved (default 70; raise for high-stakes sections) |
| `kind` | `capture` (filled from Submitter answers) · `derived` (computed from other sections, e.g. a triage draft) · `meta` (IDs, dates) |
| `inputs` | (derived only) the section ids this one is computed from |
| `condition` | (optional) include the section only when the condition holds; may reference a derived field as `<section-id>.<field>` (e.g. `triage.decision==Discovery`) |

The **explanation/rubric** under the heading is mandatory and must be
self-sufficient: it is what tells every agent (Strategist, Doc Updater, Auditor)
what "good enough at this confidence" looks like *without any external document*.

## Deriving `contract.lock.md` (Template Analyst's job)

The Analyst parses the template into a contract snapshot:

```markdown
---
template: target-template.intake-record.md
template_hash: <sha256 of the template file>
template_version: v1
default_min_confidence: 70
generated: 2026-06-03
---

# Contract

| id | section | kind | blocks | min-confidence | rubric (one line) |
|----|---------|------|--------|----------------|-------------------|
| problem | Problem statement | capture | true | 80 | pain w/ symptoms, no solution |
| reach   | Who is impacted    | capture | true | 70 | personas/segments + how affected |
| ...     | ...                | ...     | ...  | ...            | ... |
```

If a section lacks an annotation or a usable rubric, the Analyst **flags it** — a
template that can't drive confident filling is a template bug, and the audit
checklist below catches it.

## Template audit checklist (run when bundling or swapping a template)

A template is "ready to drive the pipeline" only if **every** fillable section:

- [ ] has an annotation with `id`, `blocks`, `min-confidence`, `kind`;
- [ ] has a rubric that states what a confident answer contains (not just a label);
- [ ] carries the confidence line (`Confidence/Source/Status/Disposition/Hint`)
      on every `capture` section whose `min-confidence` > 0 (the ones graded for
      readiness). `min-confidence=0` capture sections (e.g. a simple priority or a
      list) and `derived` sections do **not** require it — a `derived` section
      signals confidence through its own mechanism (e.g. the triage DRAFT banner
      with `low_confidence`);
- [ ] for `derived` sections, names the `inputs` it is computed from (and, if
      conditional, a `condition` that references an existing id/field);
- [ ] has `blocks=true` set on exactly the sections that must not be guessed.

If any box is unchecked, enrich the template until it passes. The guarantee we are
buying: **a template that passes the audit can always be filled to the point where
every blocking section reaches its `min-confidence` or an honest disposition.**

## The confidence threshold X

`min-confidence` is per-section (default `default_min_confidence`, 70). A *direct*
answer below the section's threshold is `low_confidence` and does **not** clear a
blocking gate on its own — it must either improve or take an honest disposition
(`assumption`/`discovery`/`deferred`). The Auditor enforces this; see
`questioning-method.md` for the disposition routes.

## Restart on template change

The Analyst compares the template's current hash to the `template_hash` in any
existing `contract.lock.md`:

- **Same hash** → reuse the contract; continue where the ledger left off.
- **Different hash** → **restart the analysis**: re-derive the contract, mark every
  ledger entry whose `targets-section` no longer exists (or whose rubric/threshold
  changed) as `superseded`, and let the Strategist re-open questions for new or
  changed sections. Answers bound to *unchanged* sections survive but are
  re-validated by the Auditor against the new rubric.

The diff policy is intentionally simple (full re-analysis). A finer incremental
policy can replace it later without touching the rest of the pipeline.
