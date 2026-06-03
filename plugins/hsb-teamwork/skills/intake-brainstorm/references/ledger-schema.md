# The Q&A ledger — `qa-log.md` schema (pure Markdown)

`qa-log.md` is the **single source of truth for the interview**: every question,
*why it was asked*, its answer, and how confident/where-sourced that answer is.
Only the **Ledger Writer** edits it. It is pure Markdown so a human can read and
audit it directly, and structured enough that any agent can parse it.

## File shape

```markdown
# Q&A Ledger — <demand name>

> Session: <SESSION_DIR> · Template: <template_version> · Rev: N · Updated: AAAA-MM-DD
> Readiness: <NN>% · Gate: <Open|Cleared> · Open blocking: <list or —>

## Q001 · targets: problem · status: answered
- **Rationale:** Why this question exists — which gap/section it closes and what a
  good answer unlocks downstream. (If it was triggered by another answer, say so.)
- **Spawned-by:** — | A004
- **Asked:** AAAA-MM-DD
- **Mode:** open | choice
- **Question:** <the question, in the human's language, business terms>
- **Choice:** <selected option label> | Other: <verbatim> | — (for `open`/prose)
- **Answer:** <verbatim-ish answer, or — if still open>
- **Disposition:** answered | inferred | assumption | discovery | deferred | —
- **Confidence:** 0–100 | —
- **Source:** Submitter direct | file:<path> p.X | inferred | other stakeholder | —
- **Hint:** why confidence is low / what would raise it | —
- **Follow-ups:** — | Q006, Q007

## Q002 · targets: reach · status: open
...
```

## Question lifecycle (the `status` field)

| status | meaning |
|---|---|
| `open` | asked (or proposed), no satisfactory answer yet |
| `answered` | has an answer with an honest disposition; if a direct answer, confidence ≥ the section's `min-confidence` |
| `parked` | answered via `assumption`/`discovery`/`deferred` — honest, clears the gate, still flagged to validate |
| `superseded` | retired because the template changed or a later answer made it obsolete (keep it for the audit trail; never delete) |

## Rules for the Ledger Writer

1. **Never delete.** Supersede instead — the ledger is an audit trail of how the
   demand was understood over time.
2. **Every question carries a rationale.** A question with no "why" is not allowed;
   the rationale is what lets a human (and the Auditor) judge whether it was worth
   asking and whether its answer really closes the gap.
3. **Answers can spawn questions.** When an answer reveals a new gap, the Strategist
   proposes a follow-up; record it as a new `Q###` with `spawned-by: A<n>` and link
   it from the parent's `Follow-ups`.
4. **One source of provenance per answer.** If File Extraction and a human both
   answer, record the higher-confidence one and note the other in `Hint`; flag the
   conflict for the Auditor to reconcile.
5. **Keep the header summary fresh** (readiness %, gate state, open blocking) on
   every edit — it is the at-a-glance state for the orchestrator and the human.
6. **Record the selection for `choice` questions.** Store the picked option label
   (or `Other: <verbatim>`) in `Choice`, and set `Disposition` from it: an appended
   escape-hatch option maps to `assumption` / `discovery` / `deferred`; a substantive
   option or `Other` maps to `answered` / `inferred`. For `open`/prose questions
   leave `Choice: —` and record the answer as before.

## How other agents use it (read-only)

- **Question Strategist** reads it to avoid re-asking and to see which gaps remain.
- **File Extraction** reads open questions and proposes answers it can source.
- **Doc Updater** reads `answered`/`parked` entries to fill the target document.
- **Confidence Auditor** cross-checks the ledger's confidences against the filled
  document and against the contract's thresholds.

None of them write here. They return proposals to the orchestrator, who routes
them to the Ledger Writer.
