# hsb-teamwork — Codex adapter

The same pipeline as the Claude plugin, adapted to Codex. It reuses the identical
method files under `../skills/` — **no duplicated logic**. Only the harness differs.
This adapter covers **two skills**: `intake-brainstorm` and `readiness-package`.

## What's here

| File | Purpose |
|---|---|
| `AGENTS.md` | the orchestrator entry — Codex reads it from repo root → cwd, or install it as a prompt; covers both skills |
| `prompts/hsb-teamwork-intake-brainstorm.md` | custom prompt → `/hsb-teamwork-intake-brainstorm` slash command |
| `prompts/hsb-teamwork-readiness-package.md` | custom prompt → `/hsb-teamwork-readiness-package` slash command |
| `agents/hsb-*.toml` | 16 engine subagents (one per role) shared by both skills, mirroring the Claude agents |
| `agents/hsb-stage-inheritor.toml` | proposes carry-forward entries from an upstream stage (Origin=inherited); role spec at `../agents/hsb-stage-inheritor.md` |
| `agents/hsb-section-drafter.toml` | proposes first-draft content for the sections a stage introduces (Origin=ai_drafted); role spec at `../agents/hsb-section-drafter.md` |
| `agents/hsb-escalation-flagger.toml` | decides whether the demand owes a downstream specialist assessment (CTO TA today); role spec at `../agents/hsb-escalation-flagger.md` |

> **Naming:** every agent is named for the specialty it performs, not the phase it
> runs in, so one roster serves intake-brainstorm, readiness-package, and the planned
> stages. The names are identical on Claude and Codex: `hsb-<role>`. Codex needs the
> `hsb-` vendor prefix because its namespace is **flat**; Claude adopts the same
> prefix so the two rosters line up one-to-one. Each Codex subagent reads its shared
> role spec from `../agents/hsb-<role>.md` and the shared `skills/<skill>/references/`.

## Setup

```bash
# Slash commands:
cp codex/prompts/hsb-teamwork-intake-brainstorm.md   ~/.codex/prompts/
cp codex/prompts/hsb-teamwork-readiness-package.md   ~/.codex/prompts/

# Subagents (project-scoped or global):
cp codex/agents/hsb-*.toml   .codex/agents/   # or ~/.codex/agents/

# Orchestrator entry: keep codex/AGENTS.md reachable, or drop it in as AGENTS.md.
```

Keep the package's `skills/intake-brainstorm/{references,assets}` and
`skills/readiness-package/{references,assets}` reachable from where you run Codex —
the agents read the method (contracts, rubrics, writing-integrity rules, exemplars)
from there. The Codex subagent `.toml` files are thin wrappers: each points at its
full role spec in `../agents/<role>.md` and the shared references.

## The one real difference from Claude

Claude Code fans the specialist agents out in parallel. **Codex runs them
sequentially** (single-agent, one subagent session at a time). That makes the
single-writer guarantee trivial, but the no-truncation and read-modify-write rules
in `../skills/intake-brainstorm/references/writing-integrity.md` matter just as
much — a single agent rewriting a long document is the main truncation risk.
