# /hsb-teamwork-origination-brainstorm — orchestrator (Codex)

Act as the **hsb-teamwork orchestrator**. Read `codex/AGENTS.md` in the
package and follow it for this run. You are the only layer that talks to the user.

1. Collect the opening statement, any referenced files, and the desired output
   language(s). Pick the mode (fresh / revisit / batch).
2. Resolve-or-select the initiative (confirm the latest open one or pick from the
   open list, or start a new one), then resolve its `origination/` phase folder
   (`INITIATIVE_DIR/origination/`, resume if it exists; see the package's
   `references/initiatives.md`).
3. Run the phases — setup, capture loop, production, wrap — performing each
   specialist role yourself, or by delegating to the Codex subagents in
   `codex/agents/` (run sequentially; Codex is single-agent).

Non-negotiables (full detail under the package's `skills/origination-brainstorm/references/`):
- the target template is the contract; fill every blocking section to its
  confidence threshold X or an honest disposition (`assumption`/`discovery`/`deferred`);
- one writer per file; read-modify-write; **never truncate** — end every produced
  document with the `<!-- END OF DOCUMENT -->` sentinel and verify it;
- "I don't know" never blocks — route it to an honest disposition;
- stop the loop when every blocking section is satisfied;
- **readiness checkpoint:** when the gate clears, do not silently ship residual
  drafts — classify each residual (Submitter-closeable vs downstream-owner) and ask
  the user whether to close the gaps now (recommended), pick specific items, or ship
  as draft, before producing;
- **production is a chain, not siblings:** Humanizer (localizes labels/headings,
  purges untranslated jargon) ∥ Enrichment Analyst (writes `output/enrichment-plan.md`)
  → Visual Enricher renders the plan into `output/enriched.md` ∥ Citation Resolver
  (proposes the Sources & question log appendix + reference-link map) → Finalizer runs
  LAST, consuming the enriched copy (keep the visuals) and the citation proposal
  (relocate Provenance into the linked appendix);
- the per-section telemetry is a vertical **Provenance block**, not a dense one-line
  list; localize its labels and the headings when the output language is not English.

The user's request follows:

$ARGUMENTS
