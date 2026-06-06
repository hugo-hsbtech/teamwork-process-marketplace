# Localization — the single source of truth for "no language leaks"

The pipeline's templates ship in **English**. When a run's output language differs
(e.g. pt-BR), the produced document must read as if it were authored in that language
end to end. "No language leak" is a **cross-cutting invariant**: it is owned by this
one file, enforced by one detector (the **Language Auditor**), and applied by one
writer per artifact (the **Doc Updater** for `$DOC`, the **Humanizer** for
`humanized.md`, the **Translator** for `translated.<lang>.md`). Those agents reference
this file rather than each restating the rules, so a gap is fixed in one place.

This file is **template-agnostic**: it applies to every document the pipeline emits
(origination record, intake/readiness, technical assessment, PRD, analytics).

## What counts as a leak (the taxonomy)

When the output language is not English, ALL of the following are leaks:

1. **Untranslated jargon.** Stray English terms in prose that have a natural
   target-language form: "org-wide" → "em toda a organização", "headcount" → "número
   de pessoas", "business case" → "caso de negócio", "pass-through" → "repasse",
   "snapshot" → "retrato/instantâneo", "time-box" → "prazo fechado".
2. **Unlocalized scaffolding labels.** Any section **heading** or **Provenance
   label** still in English (Provenance/Confidence/Source/Status/Disposition/Hint vs.
   Proveniência/Confiança/Fonte/Situação/Disposição/Observação).
3. **Untranslated scaffolding PROSE.** This is the most common miss. The fixed prose
   copied verbatim from the template — the **intro blockquotes / callouts** on each
   section (including the ⚠️ triage-draft banner) and the **Handoff destination
   bullets** ("If Product Ready: …") — must be rewritten in the output language, not
   pasted in English. A heading-and-label check does **not** cover these; they are
   whole sentences, not labels.
4. **Untranslated status/disposition TOKENS.** Enum tokens in the telemetry are prose,
   not stable identifiers — translate them (see the map below). A `low_confidence
   (DRAFT)` or `Disposition: answered` sitting in a pt-BR document is a leak.
5. **Inline/appendix token mismatch.** The inline confidence lines and the appendix
   telemetry table must use the **same** localized tokens — never English in one and
   the target language in the other.
6. **Terminology drift.** Synonym-cycling a concept instead of using the glossary's
   one canonical term.
7. **Em / en dashes.** Any `—` or `–` in the humanized/finalized copy (replace with a
   period, comma, colon, parentheses, or restructure).

## Token map (pt-BR)

| Field | English token | pt-BR |
|---|---|---|
| status | `open` | aberta |
| status | `answered` | respondida |
| status | `parked` | em espera |
| status | `superseded` | superada |
| status | `resolved` | resolvida |
| status | `low_confidence` | baixa confiança |
| disposition | `answered` | respondida |
| disposition | `inferred` | inferida |
| disposition | `assumption` | premissa |
| disposition | `discovery` | descoberta |
| disposition | `deferred` | adiada |
| origin | `ai_drafted` | rascunho IA |
| flag | `DRAFT` | RASCUNHO |

For other target languages, translate the tokens analogously and keep one consistent
choice per term across the whole document (record it in `glossary.md`).

## What stays verbatim (the allowlist)

Only these are NOT translated:
- **Q### ids, numbers, dates** — stable identifiers.
- **Proper nouns** and glossary-canonical terms with no natural translation (e.g.
  "greenfield"); gloss them on first use. Mark these as **allowed**, not leaks.
- **Routing-stage names** that name a downstream artifact: **Product Ready /
  Discovery / Backlog / Reject**. These are process-stage identifiers shared across
  skills.

## Derived-section telemetry — line break (formatting)

The derived sections (triage draft, escalation, readiness snapshot, handoff,
executive summary) carry their telemetry as a **short header line of its own** —
`Confidence · Disposition` (localized) — followed by the rationale as a **separate
paragraph below it** (blank line between). Never mash the `Confidence · Disposition`
label and its multi-sentence rationale into one dense run-on paragraph. (The capture
sections use the vertical Provenance block for the same reason: the telemetry should
never crowd or be crowded by prose.)

## Ownership (who does what)

- **Doc Updater** — first writer of `$DOC`: localizes headings, labels, scaffolding
  prose, capture content, and tokens as it fills, per this file.
- **Humanizer** — sole writer of `humanized.md`, last line of defense: applies the
  Language Auditor's findings and fixes any leak it still sees, per this file.
- **Language Auditor** — read-only detector: audits `humanized.md` against this
  taxonomy and returns a `language = clean | leaks-found` verdict with locations. It
  writes nothing; leaks route back to the Humanizer.
- **Translator** — writer of `translated.<lang>.md`: a faithful translation that
  obeys the same token map, allowlist, and line-break rule.
