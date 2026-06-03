# hsb-teamwork — Codex adapter

The same pipeline as the Claude plugin, adapted to Codex. It reuses the identical
method files under `../skills/intake-brainstorm/references/` and `../assets/` —
**no duplicated logic**. Only the harness differs.

## What's here

| File | Purpose |
|---|---|
| `AGENTS.md` | the orchestrator entry — Codex reads it from repo root → cwd, or install it as a prompt |
| `prompts/hsb-teamwork-intake-brainstorm.md` | a custom prompt → `/hsb-teamwork-intake-brainstorm` slash command |
| `agents/hsb-intake-*.toml` | 15 Codex subagents (one per role), mirroring the Claude agents |

> **Naming:** Codex has a **flat** namespace for prompts and subagents, so they are
> vendor-prefixed `hsb-intake-*` to avoid collisions. Claude namespaces components
> under the plugin instead, so its skill/agents stay unprefixed (`intake-*`). Each
> Codex subagent reads its shared role spec from the unprefixed `agents/intake-<role>.md`.

## Setup

```bash
# Slash command:
cp codex/prompts/hsb-teamwork-intake-brainstorm.md  ~/.codex/prompts/hsb-teamwork-intake-brainstorm.md

# Subagents (project-scoped or global):
cp codex/agents/hsb-intake-*.toml  .codex/agents/        # or ~/.codex/agents/

# Orchestrator entry: keep codex/AGENTS.md reachable, or drop it in as AGENTS.md.
```

Keep the package's `skills/intake-brainstorm/{references,assets}` reachable from
where you run Codex — the agents read the method (the contract, the rubrics, the
writing-integrity rules, the golden exemplar) from there. The Codex subagent
`.toml` files are thin wrappers: each points at its full role spec in
`../agents/intake-<role>.md` and the shared references.

## The one real difference from Claude

Claude Code fans the specialist agents out in parallel. **Codex runs them
sequentially** (single-agent, one subagent session at a time). That makes the
single-writer guarantee trivial, but the no-truncation and read-modify-write rules
in `../skills/intake-brainstorm/references/writing-integrity.md` matter just as
much — a single agent rewriting a long document is the main truncation risk.
