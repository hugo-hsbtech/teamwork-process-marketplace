# Design Spec — Async Human-in-the-Loop Bridge (Claude + Codex)

**Date:** 2026-06-05
**Plugin:** `hsb-teamwork`
**Status:** Proposed design, pending implementation plan
**Author:** Hugo Seabra

---

## 1. Purpose

Let an **external platform** (separate database, separate UI) mirror every
interaction a `hsb-teamwork` session produces, **render the same questions** the
skill would ask, let a user **answer them on that platform**, and feed those
answers **back into the session** so the pipeline continues — all while the skill
keeps running unchanged.

The bridge must work **identically for Claude Code and Codex**. The two harnesses
already "read the same specs; only the harness differs"
(`plugins/hsb-teamwork/codex/AGENTS.md`). This design keeps that promise: the
human-loop and the recovery mechanic live **below** the harness, and the only
per-harness code is a one-line invocation adapter.

This is a **guidance/design artifact**. It defines contracts, data shapes, and the
control flow. It does **not** ship executable code; the runtime (language/stack)
binds to the platform backend and is left parameterized (see §11).

---

## 2. The core insight that makes this possible

The durable state of the work is **not** in the session — it is in
`.teamwork/<initiative>/`. The `qa-log.md` ledger is already a **durable workflow
state machine**: every `Q###` carries a `status` (`answered` / `parked` /
`superseded` / …). `initiative.json` is the manifest of phases and readiness.

Therefore:

> **The session is disposable. The initiative folder is the durable workflow.**
> A session re-hydrates from the files, advances to the next blocking point, and
> dies. Resuming a blocked flow is **re-hydration from files**, never resurrection
> of a dead tool call.

This is what makes the design harness-agnostic and robust to ephemeral containers.

---

## 3. Locked decisions (from stakeholder review)

1. **Topology A** — Claude Code / Codex owns the session lifecycle; the platform
   plugs in via an MCP server and a post-run sync. (Migration to Topology B —
   platform-owned sessions via the Agent SDK — reuses the same data model and the
   same MCP, so the investment is preserved.)
2. **Bidirectional loop** — the user both *sees* the questions and *answers* them
   on the platform; answers return to the agent.
3. **Source of truth = `.teamwork/` files.** The platform database is a
   **projection**, never the origin. A user's answer is durable on the platform,
   but becomes "truth" only after the agent writes it into `qa-log.md`, which then
   re-projects to the database.
4. **Compatibility with both Claude and Codex is mandatory.**

---

## 4. Design principles that guarantee compatibility

| Principle | Consequence |
|---|---|
| SoT = files | Sessions are disposable; recovery is re-hydration |
| One human-loop interface = one MCP server | Replaces `AskUserQuestion` (Claude) **and** enumerated prose (Codex) with one tool both harnesses call |
| Inbound answers = MCP **pull**, not platform-written files | Works even though the platform has **no filesystem access** to the ephemeral container — the MCP makes an **outbound** call |
| Capture = **post-run sync** in the runner | Independent of Claude-only hooks (Codex has no hook system) |
| Native `--resume` is an **optimization**, not a requirement | A cold start pointed at the initiative folder also works — covers Codex's weaker resume |

Net effect: the Claude/Codex difference collapses to **one line** in the runner.

---

## 5. Architecture

```
        EXTERNAL PLATFORM (orchestrates in Topology A)
        ┌──────────────────────────────────────────────────┐
        │  Interaction screen  ──  Database (projection)    │
        │        ▲   │                      ▲                │
        │        │   ▼                      │               │
        │   ┌──────────────┐        ┌───────────────┐        │
        │   │ API          │        │ Session Runner │       │
        │   │ /questions   │        │  (+ adapter)   │       │
        │   │ /answers     │        └───────┬────────┘       │
        └───┴──────┬───────┴────────────────┼───────────────┘
                   │ HTTP                    │ spawn headless
                   │                         ▼
        ┌──────────┴───────┐    ┌────────────────────────────┐
        │ MCP server       │◀───│  claude --resume … -p  ▲    │
        │ "teamwork-bridge"│    │       OR                    │
        │  • ask_user      │    │  codex exec …          │    │
        │  • get_pending_  │    │  (same MCP on both)    │    │
        │    answers       │    │   skill orchestrator ──┼────┤
        └──────────────────┘    └───────────┬────────────────┘
                   ▲                         │ read / write
                   │ post-run sync           ▼
                   └──────────────  .teamwork/ (SOURCE OF TRUTH)
```

---

## 6. Components

### 6.1 MCP server `teamwork-bridge` (single codebase, both harnesses)

Both Claude Code and Codex load MCP servers over stdio. The **same** server binary
is configured in each. It exposes two **non-blocking** tools.

**`ask_user(question) → { status, answer? }`**
- Registers the question on the platform (`POST /questions`, upsert by `q_id`),
  marks it `aguardando`.
- Returns **immediately**. If the platform already holds an answer for that
  `q_id`, returns `{ status: "answered", answer }`; otherwise `{ status: "pending" }`.
- **Never blocks the session.** "Pending" is a clean signal the orchestrator uses
  to pause.

**`get_pending_answers(initiative_id) → Answer[]`**
- `GET /answers?initiative=<id>&status=respondida`.
- Returns answers the user has given that the agent has **not yet applied**.
- Called at the **start of every run** (fresh, resumed, or cold).

> **Why pull-over-MCP, not a platform-written inbox file:** in Topology A the
> platform has **no filesystem access** to the ephemeral container. The MCP server
> runs *next to* the harness and makes an **outbound** HTTPS call to the platform
> API. Nothing is written into the container from outside.

### 6.2 Async human-loop protocol (one reference doc, read by both)

A single reference file — proposed location
`plugins/hsb-teamwork/skills/<skill>/references/async-human-loop.md`, pointed to by
both `SKILL.md` (Claude) and `AGENTS.md` (Codex). It instructs the orchestrator to
run this loop on **every** invocation:

```
ON EVERY RUN (fresh | resume | cold start):
  1. get_pending_answers(initiative)
       → for each returned answer:
           guard: apply ONLY if qa-log Q### status == aguardando   (idempotent)
           apply via the Ledger Writer (status → answered/parked)
  2. recompute readiness / gate
  3. decide the next open gaps (Question Strategist)
  4. for each gap:  ask_user(Q###)
       → if it returns an answer, apply it immediately
       → if it returns "pending", leave Q### as aguardando
  5. if all open questions are "pending":
       persist state, then END THE TURN CLEANLY (pause — do not block)
```

This replaces `AskUserQuestion` (Claude) and enumerated prose (Codex) with one
call. Because both harnesses keep "the orchestrator is the only layer that talks to
the human," the loop runs **identically** on each.

### 6.3 Session Runner + adapter (the only per-harness code)

In the platform's orchestration layer:

```
runSession(initiative_id, harness):
  prompt = "Process the initiative at .teamwork/<id>/ per async-human-loop.md"
  cmd = (harness == "claude")
      ? ["claude", "--resume", session_id, "-p", prompt, "--mcp-config", cfg]
      : ["codex", "exec", prompt]          # MCP declared in ~/.codex/config.toml
  spawn(cmd); wait for exit (the session either pauses or completes)
```

Triggered in two cases: (a) initial start; (b) the platform receives an answer and
enqueues a resume. A **per-initiative lock** guarantees at most one active runner
(no race).

### 6.4 Capture — post-run sync (harness-agnostic backbone)

**Codex has no hook system**, so capture cannot depend on hooks. The backbone is:

- **Post-run sync in the Runner:** after the headless process exits, read the
  changed files in `.teamwork/<id>/` (`qa-log.md`, `initiative.json`, the document)
  and upsert them into the platform DB, keyed by `q_id` and section `id`+`rev`.

- **Optional Claude `PostToolUse` hook:** a *Claude-only enhancement* for
  near-real-time projection during long turns. Not the backbone.

### 6.5 Database schema (projection of `qa-log` + `initiative.json`)

```
initiative(id, project, language, status, harness, created_at)
phase(initiative_id, name, state, readiness, template_hash, produces, owes_json)
question(q_id, phase_id, targets_section, mode, question, options_json,
         rationale, hint, status, asked_at, spawned_by)
answer(q_id, text, disposition, confidence, source,
       answered_by, answered_at, applied_bool)
doc_section(id, phase_id, rev, content, confidence, status, updated_at)
```

The platform UI **reads** from `question`/`answer`/`doc_section`. The user's answer
writes the `answer` row (`status=respondida`); it becomes truth only after the
agent applies it and the post-run sync flips `applied_bool` from the re-read
`qa-log.md`.

---

## 7. Data contracts

**Question (platform ← `ask_user`), mirrors the `qa-log` ledger schema**
```json
{
  "q_id": "Q012",
  "initiative_id": "20260603-1833-pokerplan-a8432a",
  "phase": "origination",
  "targets_section": "reach",
  "mode": "choice",                  // "open" | "choice"
  "question": "…",
  "options": ["…", "…"],             // only when mode == "choice"
  "escape_hatches": ["assumption", "discovery", "deferred"],
  "rationale": "…",
  "hint": "…",
  "asked_at": "2026-06-05T12:00:00-03:00"
}
```

**Answer (`get_pending_answers` → agent)**
```json
{
  "q_id": "Q012",
  "text": "…",
  "disposition": "assumption",       // assumption|discovery|deferred|inferred|null
  "confidence": 70,                  // optional; agent may re-score
  "source": "user:direct",
  "answered_by": "user@example.com",
  "answered_at": "2026-06-05T15:30:00-03:00"
}
```

> The platform UI **must** render the `escape_hatches` plus a free-text path. The
> `questioning-method.md` rubric requires every `choice` question to offer the
> honest dispositions and an open answer; without them the pipeline "stalls on
> I-don't-know," which the whole system is designed to avoid.

---

## 8. End-to-end flow (identical on both harnesses)

1. Platform → Runner starts a headless session for initiative `X`.
2. Orchestrator: `get_pending_answers(X)` → empty → reads files → finds a gap →
   `ask_user(Q012)` → `pending` → writes `qa-log` `Q012: aguardando` → **pauses**
   (ends the turn).
3. Runner exits → **post-run sync** projects `qa-log` → `Q012` appears on the
   user's screen.
4. User answers on the platform → `answer` row `respondida` → platform enqueues a
   resume.
5. Runner resumes → `get_pending_answers(X)` → returns `Q012` → orchestrator
   applies it to `qa-log` (Ledger Writer) → recomputes readiness → next gap or
   completes.
6. Loop until the readiness gate clears / the phase is `frozen`.

---

## 9. Question state machine (the reconciliation between the two worlds)

```
aguardando ──(user answers on platform)──▶ respondida
respondida ──(agent applies via get_pending_answers)──▶ applied (answered|parked in qa-log)
applied ──(new evidence)──▶ superseded     (entry preserved as audit trail, per the ledger)
```

The platform owns `aguardando` / `respondida`; `qa-log.md` owns `applied` /
`answered`. `get_pending_answers` + the status guard is the idempotent bridge.

---

## 10. Idempotency & safety

- **`ask_user`** upserts by `q_id` — asking twice is a no-op.
- **Apply guard** — the orchestrator applies a pulled answer only if the `qa-log`
  status is still `aguardando`; an already-`applied`/`superseded` question is
  skipped. Resumes can fire twice safely.
- **Post-run sync** upserts by `q_id` and section `id`+`rev`; out-of-order events
  with a lower `rev` are discarded.
- **No destructive writes** — `superseded` answers are preserved as an audit
  trail, mirroring `writing-integrity.md`.
- **Concurrency** — one running session per initiative (lock) → no double runner.
- **Reconciliation job** — if a sync event is lost, a periodic job re-reads
  `.teamwork/` and re-projects; safe because the file is the source of truth.

---

## 11. Open decision — runtime binding

The MCP server and the Session Runner are runtime-agnostic by contract. They bind
to the platform backend stack (e.g., Node/TypeScript, Python, …). Recommendation:
match the platform's existing backend to minimize operational surface. If the team
later migrates to **Topology B**, the Claude Agent SDK (TS or Python) hosts the
runner and intercepts the human-loop via its tool/permission callback — reusing
this same MCP and schema.

**To finalize:** confirm the platform backend stack so the implementation plan can
pin concrete libraries (MCP SDK, HTTP client, process spawner).

---

## 12. Compatibility matrix — how each Claude/Codex difference is neutralized

| Incompatibility risk | Neutralized by |
|---|---|
| Codex lacks `AskUserQuestion` | MCP `ask_user` is the single transport |
| Codex lacks a hook system | Capture = post-run sync (file-based) |
| Codex resume is less mature | Recovery = MCP pull + re-hydration; cold start works without resume |
| Platform has no container FS access | MCP makes an outbound call; nothing written from outside |
| Parallel (Claude) vs sequential (Codex) execution | Already handled in-repo — same method files, different fan-out |

The residual Claude/Codex difference is **one line** in the Runner adapter (§6.3).

---

## 13. Rollout

1. **Capture-only (read-only):** post-run sync → DB → interaction screen. Zero risk,
   immediate value.
2. **MCP human-loop:** introduce `ask_user` / `get_pending_answers` behind a flag,
   keeping native `AskUserQuestion` / prose as fallback. Closes the bidirectional
   loop.
3. **Wire `async-human-loop.md`** into one skill (e.g. `origination-brainstorm`)
   first; generalize to the other three once validated.
4. **(Later) Topology B:** move session ownership into the platform via the Agent
   SDK; data model and MCP are unchanged.

---

## 14. Out of scope (this spec)

- The platform UI implementation and its authentication.
- The concrete MCP server / Runner code (runtime pending — §11).
- Topology B (Agent-SDK-owned sessions) — separate spec when needed.
- Multi-user conflict policy when two people answer the same `Q###` (default:
  last-write-wins on the platform, reconciled by the agent at apply time).
