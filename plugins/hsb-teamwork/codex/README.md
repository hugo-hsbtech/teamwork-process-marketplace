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
| `agents/hsb-intake-*.toml` | 15 Codex subagents (one per role) for intake-brainstorm, mirroring the Claude agents |
| `agents/hsb-readiness-drafter.toml` | RP subagent: proposes first-draft content for new RP sections (Origin=ai_drafted); role spec at `../agents/readiness-drafter.md` |
| `agents/hsb-readiness-inheritor.toml` | RP subagent: carries intake-record sections into the RP (Origin=inherited); role spec at `../agents/readiness-inheritor.md` |
| `agents/hsb-readiness-escalation-flagger.toml` | RP subagent: decides CTO TA and records tech-assessment-ref; role spec at `../agents/readiness-escalation-flagger.md` |

> **Naming:** Codex has a **flat** namespace for prompts and subagents, so they are
> vendor-prefixed `hsb-intake-*` / `hsb-readiness-*` to avoid collisions. Claude
> namespaces components under the plugin instead, so its skill/agents stay unprefixed
> (`intake-*`, `readiness-*`). Each Codex subagent reads its shared role spec from the
> unprefixed `agents/<role>.md` and the shared `skills/<skill>/references/`.

## Setup

```bash
# Slash commands:
cp codex/prompts/hsb-teamwork-intake-brainstorm.md   ~/.codex/prompts/
cp codex/prompts/hsb-teamwork-readiness-package.md   ~/.codex/prompts/

# Subagents (project-scoped or global):
cp codex/agents/hsb-intake-*.toml      .codex/agents/   # or ~/.codex/agents/
cp codex/agents/hsb-readiness-*.toml   .codex/agents/   # or ~/.codex/agents/

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
