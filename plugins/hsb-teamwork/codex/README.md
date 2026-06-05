# hsb-teamwork — Codex adapter

The same pipeline as the Claude plugin, adapted to Codex. It reuses the identical
method files under `../skills/` — **no duplicated logic**. Only the harness differs.
This adapter covers **four skills**: `origination-brainstorm`, `readiness-package`,
`tech-assessment`, and `prd-generation`.

## What's here

| File | Purpose |
|---|---|
| `AGENTS.md` | the orchestrator entry — Codex reads it from repo root → cwd, or install it as a prompt; covers all four skills |
| `prompts/hsb-teamwork-origination-brainstorm.md` | custom prompt → `/hsb-teamwork-origination-brainstorm` slash command |
| `prompts/hsb-teamwork-readiness-package.md` | custom prompt → `/hsb-teamwork-readiness-package` slash command |
| `prompts/hsb-teamwork-tech-assessment.md` | custom prompt → `/hsb-teamwork-tech-assessment` slash command |
| `prompts/hsb-teamwork-prd-generation.md` | custom prompt → `/hsb-teamwork-prd-generation` slash command |
| `agents/hsb-*.toml` | engine subagents (one per role) shared by every skill, mirroring the Claude agents |
| `agents/hsb-stage-inheritor.toml` | proposes carry-forward entries from an upstream stage (Origin=inherited); role spec at `../agents/hsb-stage-inheritor.md` |
| `agents/hsb-section-drafter.toml` | proposes first-draft content for the sections a stage introduces (Origin=ai_drafted); role spec at `../agents/hsb-section-drafter.md` |
| `agents/hsb-escalation-flagger.toml` | decides whether the demand owes a downstream specialist assessment (CTO TA today); role spec at `../agents/hsb-escalation-flagger.md` |
| `agents/hsb-enrichment-analyst.toml` | catalogs sourced visual/analytics opportunities into `output/enrichment-plan.md` (the insumo the Visual Enricher renders); role spec at `../agents/hsb-enrichment-analyst.md` |
| `agents/hsb-citation-resolver.toml` | proposes the navigable "Sources & question log" appendix + reference-link map for the Finalizer; role spec at `../agents/hsb-citation-resolver.md` |

> **Naming:** every agent is named for the specialty it performs, not the phase it
> runs in, so one roster serves origination-brainstorm, readiness-package, and the planned
> stages. The names are identical on Claude and Codex: `hsb-<role>`. Codex needs the
> `hsb-` vendor prefix because its namespace is **flat**; Claude adopts the same
> prefix so the two rosters line up one-to-one. Each Codex subagent reads its shared
> role spec from `../agents/hsb-<role>.md` and the shared `skills/<skill>/references/`.

## Setup

```bash
# Slash commands:
cp codex/prompts/hsb-teamwork-origination-brainstorm.md   ~/.codex/prompts/
cp codex/prompts/hsb-teamwork-readiness-package.md   ~/.codex/prompts/
cp codex/prompts/hsb-teamwork-tech-assessment.md   ~/.codex/prompts/
cp codex/prompts/hsb-teamwork-prd-generation.md   ~/.codex/prompts/

# Subagents (project-scoped or global):
cp codex/agents/hsb-*.toml   .codex/agents/   # or ~/.codex/agents/

# Orchestrator entry: keep codex/AGENTS.md reachable, or drop it in as AGENTS.md.
```

Keep the package's `skills/<skill>/{references,assets}` (for the skill you run) and the
shared `skills/origination-brainstorm/{references,assets}` reachable from where you run Codex —
the agents read the method (contracts, rubrics, writing-integrity rules, exemplars)
from there. The Codex subagent `.toml` files are thin wrappers: each points at its
full role spec in `../agents/<role>.md` and the shared references.

## The one real difference from Claude

Claude Code fans the specialist agents out in parallel. **Codex runs them
sequentially** (single-agent, one subagent session at a time). That makes the
single-writer guarantee trivial, but the no-truncation and read-modify-write rules
in `../skills/origination-brainstorm/references/writing-integrity.md` matter just as
much — a single agent rewriting a long document is the main truncation risk.
