# Cost telemetry — capturing tokens, models, and time automatically

The investment side of ROI (`metrics-catalog.md` §A/§B) is **captured
automatically** by a Claude Code hook that reads the session transcript and
appends consumption blocks to the initiative's cost ledger. This file is the
spec for the capture mechanism, the session binding that makes it possible, the
ledger schema, and the pricing table. No agent computes tokens by hand — the hook
does it from ground truth (the transcript's `usage` fields).

> **Why a hook and not the orchestrator.** Token counts and the model used live
> in the transcript, not in the orchestrator's own view. A hook fired on `Stop` /
> `SubagentStop` gets the `transcript_path` and can read the real `usage` per
> message, so the numbers are *measured*, not estimated. The plugin stays
> stateless; the captured data lives in the stateful initiative folder.

---

## The session binding — how a hook knows which initiative is active

A hook is handed a `session_id`, a `transcript_path`, and the `cwd` — but **not**
which initiative/phase the run is working in. The skills already resolve that at
the start of every run (resolve-or-select). So each `hsb-teamwork` skill, right
after it resolves the initiative and phase, writes a tiny **session binding**:

```
<TEAMWORK_ROOT>/.sessions/<session_id>.json
  { "initiative": "<INITIATIVE_DIR name>", "phase": "<phase>", "updated": "<ISO ts>" }
```

This is the only new initiative-level write the four existing skills take on (see
`initiatives.md` § *The session binding*). The hook reads it by `session_id` to
attribute consumption to the right `<INITIATIVE_DIR>/<phase>`. If no binding
exists for the session (a run that is not an `hsb-teamwork` run), the hook exits
silently — it captures nothing it cannot attribute.

`TEAMWORK_ROOT` is resolved exactly as the skills resolve it: `$TEAMWORK_HOME`,
else the git top-level + `/.teamwork`, else `cwd/.teamwork`.

---

## The hook — `hooks/teamwork-cost-capture.py`

Registered in the plugin's `hooks/hooks.json` on two events:

- **`SubagentStop`** — fires when a spawned subagent (a `Task`) finishes. Captures
  that subagent's slice of consumption.
- **`Stop`** — fires when the orchestrator's turn ends. Captures the
  orchestrator's slice and reconciles anything not yet recorded.

Both events deliver, on **stdin** as JSON: `session_id`, `transcript_path`,
`cwd`, `hook_event_name` (and, for `SubagentStop`, run metadata). The hook
command is invoked as
`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/teamwork-cost-capture.py` — `CLAUDE_PLUGIN_ROOT`
is injected by Claude Code so the script and `pricing.json` resolve regardless of
where the plugin is installed.

### What it does (idempotent, append-only, crash-safe)

1. Read stdin JSON → `session_id`, `transcript_path`.
2. Resolve `TEAMWORK_ROOT`; read `.sessions/<session_id>.json`. **No binding →
   exit 0** (nothing to attribute).
3. Read the **watermark** `<INITIATIVE_DIR>/analytics/.cost-watermark-<session_id>`
   — the set of transcript message `uuid`s already recorded. (Re-firing within a
   session must never double-count.)
4. Stream the transcript JSONL. For each **assistant** entry not in the watermark:
   - read `message.model` and `message.usage`
     (`input_tokens`, `output_tokens`, `cache_creation_input_tokens`,
     `cache_read_input_tokens`);
   - classify `agent`: `orchestrator` when `isSidechain` is false/absent,
     `subagent` when `isSidechain` is true. Best-effort `role` =
     `subagent_type` resolved from the spawning `Task` tool-use block when
     determinable, else `subagent` (see *Agent attribution* below);
   - compute `usd` from `pricing.json` (model → rates; cache-read priced at the
     cheap rate, cache-create at the write rate);
   - compute `durationMs` from adjacent timestamps when present;
   - append one ledger line; add the `uuid` to the watermark.
5. Also tally **`Task` spawns** per `subagent_type` (from orchestrator tool-use
   blocks) into the same ledger as `kind: "spawn"` rows, so §A "agent
   invocations" is exact even when token attribution is coarse.
6. Write the watermark back. **Every step is wrapped; the hook always exits 0** —
   a telemetry failure must never break the user's run.

### Agent attribution — exact where possible, honest where not

Per-phase and per-model totals are **exact** (every assistant `usage` block is
attributed to the bound phase and its stated model). Per-*agent* attribution is
**best-effort**: the transcript marks subagent work with `isSidechain`, and the
spawning `Task` tool-use block carries `subagent_type`, but the linkage between a
sidechain entry and its originating `Task` is reconstructed heuristically. The
ledger therefore always carries a reliable `orchestrator` vs `subagent` split and
an exact spawn count per `subagent_type`; the finer per-agent token split is
labeled as best-effort in the report. The skill never overstates precision.

---

## The ledger — `<INITIATIVE_DIR>/analytics/cost-ledger.jsonl`

Append-only JSON Lines, one block per recorded unit. Pure JSONL so a human can
read it and any agent can parse it. The Cost Collector reads it; nothing else
writes it except the hook.

```jsonl
{"kind":"usage","ts":"2026-06-03T18:34:11-03:00","phase":"origination","agent":"orchestrator","role":"orchestrator","model":"claude-opus-4-8","in":1840,"out":420,"cacheCreate":0,"cacheRead":15200,"usd":0.02064,"durationMs":9100,"uuid":"…"}
{"kind":"usage","ts":"2026-06-03T18:34:55-03:00","phase":"origination","agent":"subagent","role":"hsb-question-strategist","model":"claude-opus-4-8","in":620,"out":310,"cacheCreate":0,"cacheRead":8400,"usd":0.01207,"durationMs":4200,"uuid":"…"}
{"kind":"spawn","ts":"2026-06-03T18:34:50-03:00","phase":"origination","subagent_type":"hsb-question-strategist","uuid":"…"}
```

| field | meaning |
|---|---|
| `kind` | `usage` (a consumption block) or `spawn` (a `Task` invocation, for counts) |
| `ts` | ISO-8601 timestamp of the message |
| `phase` | the bound phase (`origination` / `readiness` / `assessment` / `prd`) |
| `agent` | `orchestrator` or `subagent` (always reliable) |
| `role` | best-effort `subagent_type` (or `orchestrator`) |
| `model` | the model id from `message.model` (priced via `pricing.json`) |
| `in` / `out` | input / output tokens |
| `cacheCreate` / `cacheRead` | prompt-cache write / read tokens |
| `usd` | computed dollar cost of this block |
| `durationMs` | active compute time for this block, when derivable |
| `uuid` | transcript message id — the idempotency key (also in the watermark) |

The ledger is **per initiative**, accumulating across every phase and every run,
exactly like the rest of the initiative folder. Commit `.teamwork/` (or use
`$TEAMWORK_HOME`) to carry it across machines.

---

## Pricing — `assets/pricing.json`

Model → USD-per-1M-tokens, with the standard prompt-caching multipliers baked in
(`cacheWrite5m` = 1.25× input, `cacheWrite1h` = 2× input, `cacheRead` = 0.1×
input). Unknown models fall back by id-prefix, then to `_default`. The table
carries an `asOf` date; update it when Anthropic prices change. The skill reads
prices **only** from this file — never hard-code a rate in an agent.

---

## Graceful degradation

If the hook never ran (not installed, or older runs predate this feature), the
ledger is absent or partial. The analytics skill detects this and renders the
`[ledger]` families as **"not captured"** with the reason, while still producing
the full `[artifact]` half (process/quality/outcome from qa-log + documents +
`initiative.json`). ROI composites that need dollars degrade to their
token-free / readiness-only variants. The report is always honest about what was
measured versus what was unavailable.

<!-- END OF DOCUMENT -->
