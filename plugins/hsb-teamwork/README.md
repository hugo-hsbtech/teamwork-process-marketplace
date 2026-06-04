# hsb-teamwork

> ↑ Part of the **`hsb-tech`** marketplace. For the project overview, the
> architecture of the pipeline, and the eval suite, see the
> [repository README](../../README.md).

A demand-to-delivery toolkit for **Claude Code** and **Codex**. Skills so far:

- **`intake-brainstorm`** — turns a rough demand description (and any files you
  point at) into a fully-filled, confidence-graded document, then produces
  humanized, translated, and visually-enriched variants.
- **`readiness-package`** — takes a Product Ready intake-record and produces a
  frozen Readiness Package (RP) via a draft-then-confirm flow, with automatic
  CTO-escalation detection.

This page is the **install-and-use guide**; pick your tool below.

- Marketplace: **`hsb-tech`** · Plugin: **`hsb-teamwork`**
- Author: Hugo Seabra · Dedicated repo: `hugo-hsbtech/teamwork-process-marketplace`

**`hsb-teamwork` is a multi-step toolkit.** Today it ships two skills,
`intake-brainstorm` and `readiness-package`. Planned siblings in the same plugin:
`tech-assessment`, `prd-generation` — each invoked as `/hsb-teamwork:<skill>`
(Claude) or `/hsb-teamwork-<skill>` (Codex). They share this plugin's agents and
reference files, so the pipeline mechanics carry across every step.

---

## A. Claude Code

### Install

The plugin is published from its **own repository** — a dedicated repo is the
clean way to host a marketplace (its root holds `.claude-plugin/marketplace.json`).

```
/plugin marketplace add hugo-hsbtech/teamwork-process-marketplace
/plugin install hsb-teamwork@hsb-tech
```

> While it is still developed inside the monorepo, you can instead
> `/plugin marketplace add hugo-hsbtech/teamwork-process` (same marketplace.json),
> then install the same way.

- `marketplace add` takes the **git repo** that holds `.claude-plugin/marketplace.json`.
- `install` takes `<plugin>@<marketplace>` = `hsb-teamwork@hsb-tech`.
- When prompted, choose a **scope**: *user* (all your projects), *project*
  (committed for your team), or *local* (just you, this repo).

### Use

Invoke the skill (plugin skills are namespaced `<plugin>:<skill>`):

```
/hsb-teamwork:intake-brainstorm
```

Then describe your demand in one line, optionally naming files to read. The
orchestrator asks only the gaps, fills the document, and produces the variants.
You can also just describe a demand in normal chat — the skill is set to trigger
on intake/capture/triage requests.

```
/hsb-teamwork:readiness-package
```

Point at a Product Ready intake-record. The skill drafts the Readiness Package,
presents it for your confirmation, and freezes the final RP. CTO-escalation
triggers are flagged automatically.

### Update / remove

```
/plugin marketplace update hsb-tech     # pull the latest
/plugin uninstall hsb-teamwork@hsb-tech
```

---

## B. Codex

Codex has no marketplace; you place three kinds of file. Codex uses a **flat
namespace**, so the Codex artifacts are vendor-prefixed `hsb-intake-*`.

### Install

From a clone of the repo (so the method files under
`plugins/hsb-teamwork/skills/intake-brainstorm/` are reachable):

```bash
cd plugins/hsb-teamwork

# 1. Slash command  ->  /hsb-teamwork-intake-brainstorm
cp codex/prompts/hsb-teamwork-intake-brainstorm.md  ~/.codex/prompts/

# 2. The 15 subagents (project-scoped, or ~/.codex/agents for global)
mkdir -p .codex/agents && cp codex/agents/hsb-intake-*.toml  .codex/agents/

# 3. Orchestrator instructions: either drop codex/AGENTS.md in as AGENTS.md
#    at your project root, or rely on the slash command above.
```

Keep the package's `skills/intake-brainstorm/{references,assets}` reachable from
where you run Codex — the agents read the method (contract, rubrics,
writing-integrity rules, golden exemplar) from there.

### Use

```
/hsb-teamwork-intake-brainstorm
```

Then describe the demand. Codex runs the roles **sequentially** (single-agent);
the no-truncation and read-modify-write rules still apply.

---

## What you get (both tools)

A session folder is created at `SESSION_ROOT/<demand-slug>/`, where `SESSION_ROOT`
is `$INTAKE_HOME` or your project's git root + `/intake`. It holds the contract,
the Q&A ledger, the filled document, the glossary, a readiness report, and an
`output/` folder with the humanized, translated, and enriched variants plus a
manifest.

**Re-running is safe.** The same demand resolves to the same session and
**resumes** — answers are merged, never duplicated, and nothing is re-asked.

## Customize the target document

The document is defined by an annotated template. The default is an intake record
(`skills/intake-brainstorm/assets/target-template.intake-record.md`). To target a
different document type, copy that file, re-annotate its sections (`id`, `blocks`,
`min-confidence`, `kind` + a rubric per section), and pass it as the template.

## Notes

- **Naming:** Claude namespaces components under the plugin, so its skill/agents
  stay unprefixed (`intake-*`). Codex is flat, so its prompt and subagents are
  `hsb-intake-*`.
- **"I don't know" never blocks** — it becomes an honest disposition (assumption /
  discovery / deferred).
- See [`skills/intake-brainstorm/README.md`](skills/intake-brainstorm/README.md)
  for the architecture and diagrams, and [`codex/README.md`](codex/README.md) for
  Codex details.
