#!/usr/bin/env python3
"""hsb-teamwork cost-capture hook.

Fired on `Stop` and `SubagentStop`. Reads the session transcript, attributes
token usage (per phase, per model, best-effort per agent) to the active
initiative via the session binding, prices it with assets/pricing.json, and
appends consumption blocks to <INITIATIVE_DIR>/analytics/cost-ledger.jsonl.

Design rules (see skills/initiative-analytics/references/cost-telemetry.md):
- Idempotent: a per-session watermark of processed transcript uuids prevents
  double counting across re-fires within a session.
- Append-only: never rewrites the ledger; only appends new blocks.
- Crash-safe: every step is wrapped; the hook ALWAYS exits 0 so a telemetry
  failure can never break the user's run. It captures nothing it cannot
  attribute (no session binding -> silent exit).
"""

import json
import os
import sys


def _eprint(*a):
    # Diagnostics go to stderr only; never affect the run.
    try:
        print(*a, file=sys.stderr)
    except Exception:
        pass


def resolve_teamwork_root(cwd):
    """$TEAMWORK_HOME | <git-root>/.teamwork | <cwd>/.teamwork — same rule the
    skills use."""
    home = os.environ.get("TEAMWORK_HOME")
    if home:
        return home
    # Walk up from cwd looking for a .git directory (git top-level).
    d = os.path.abspath(cwd or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return os.path.join(d, ".teamwork")
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.path.join(os.path.abspath(cwd or os.getcwd()), ".teamwork")


def load_pricing():
    """pricing.json lives next to the analytics skill, alongside the plugin."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(
            here, "..", "skills", "initiative-analytics", "assets", "pricing.json"
        ),
        # CLAUDE_PLUGIN_ROOT is the plugin root when set.
        os.path.join(
            os.environ.get("CLAUDE_PLUGIN_ROOT", here),
            "skills",
            "initiative-analytics",
            "assets",
            "pricing.json",
        ),
    ]
    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            continue
    return None


def rate_for(pricing, model):
    if not pricing:
        return None
    models = pricing.get("models", {})
    if model in models:
        return models[model]
    if pricing.get("_prefixFallback"):
        # Longest matching id-prefix wins (e.g. dated snapshots).
        best = None
        for mid, rate in models.items():
            if model and (model.startswith(mid) or mid.startswith(model)):
                if best is None or len(mid) > len(best[0]):
                    best = (mid, rate)
        if best:
            return best[1]
    return pricing.get("_default")


def usd_for(usage, rate):
    if not rate:
        return None
    M = 1_000_000.0
    return round(
        usage["in"] / M * rate.get("input", 0)
        + usage["out"] / M * rate.get("output", 0)
        + usage["cacheCreate"] / M * rate.get("cacheWrite5m", 0)
        + usage["cacheRead"] / M * rate.get("cacheRead", 0),
        6,
    )


def read_watermark(path):
    seen = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                u = line.strip()
                if u:
                    seen.add(u)
    except Exception:
        pass
    return seen


def main():
    # 1. Read the hook payload.
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    session_id = payload.get("session_id") or payload.get("sessionId")
    transcript_path = payload.get("transcript_path") or payload.get("transcriptPath")
    cwd = payload.get("cwd") or os.getcwd()
    if not session_id or not transcript_path or not os.path.isfile(transcript_path):
        return 0

    # 2. Resolve the active initiative via the session binding.
    root = resolve_teamwork_root(cwd)
    binding_path = os.path.join(root, ".sessions", "%s.json" % session_id)
    try:
        with open(binding_path, "r", encoding="utf-8") as f:
            binding = json.load(f)
    except Exception:
        return 0  # not an hsb-teamwork run — nothing to attribute
    initiative = binding.get("initiative")
    phase = binding.get("phase") or "unknown"
    if not initiative:
        return 0
    init_dir = os.path.join(root, initiative)
    analytics_dir = os.path.join(init_dir, "analytics")
    try:
        os.makedirs(analytics_dir, exist_ok=True)
    except Exception:
        return 0

    ledger_path = os.path.join(analytics_dir, "cost-ledger.jsonl")
    watermark_path = os.path.join(
        analytics_dir, ".cost-watermark-%s" % session_id
    )
    seen = read_watermark(watermark_path)
    pricing = load_pricing()

    new_rows = []
    new_uuids = []

    # 3. Stream the transcript JSONL.
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                uuid = entry.get("uuid") or ""
                if uuid and uuid in seen:
                    continue
                msg = entry.get("message") or {}
                ts = entry.get("timestamp") or ""
                is_side = bool(entry.get("isSidechain"))
                etype = entry.get("type") or msg.get("role")

                # Record token usage on assistant messages.
                if etype == "assistant" and isinstance(msg, dict):
                    usage = msg.get("usage") or {}
                    if usage:
                        u = {
                            "in": int(usage.get("input_tokens", 0) or 0),
                            "out": int(usage.get("output_tokens", 0) or 0),
                            "cacheCreate": int(
                                usage.get("cache_creation_input_tokens", 0) or 0
                            ),
                            "cacheRead": int(
                                usage.get("cache_read_input_tokens", 0) or 0
                            ),
                        }
                        if u["in"] or u["out"] or u["cacheCreate"] or u["cacheRead"]:
                            model = msg.get("model") or "unknown"
                            row = {
                                "kind": "usage",
                                "ts": ts,
                                "phase": phase,
                                "agent": "subagent" if is_side else "orchestrator",
                                "role": "subagent" if is_side else "orchestrator",
                                "model": model,
                                "in": u["in"],
                                "out": u["out"],
                                "cacheCreate": u["cacheCreate"],
                                "cacheRead": u["cacheRead"],
                                "usd": usd_for(u, rate_for(pricing, model)),
                                "durationMs": entry.get("durationMs"),
                                "uuid": uuid,
                            }
                            new_rows.append(row)
                    # Count Task spawns (for exact agent-invocation metrics).
                    content = msg.get("content")
                    if isinstance(content, list):
                        for block in content:
                            if (
                                isinstance(block, dict)
                                and block.get("type") == "tool_use"
                                and block.get("name") == "Task"
                            ):
                                sub = (block.get("input") or {}).get(
                                    "subagent_type"
                                ) or "unknown"
                                new_rows.append(
                                    {
                                        "kind": "spawn",
                                        "ts": ts,
                                        "phase": phase,
                                        "subagent_type": sub,
                                        "uuid": (block.get("id") or uuid),
                                    }
                                )
                if uuid:
                    new_uuids.append(uuid)
    except Exception as e:
        _eprint("teamwork-cost-capture: transcript read failed:", e)
        return 0

    # 4. Append new rows + advance the watermark (best-effort, never fatal).
    if new_rows:
        try:
            with open(ledger_path, "a", encoding="utf-8") as f:
                for row in new_rows:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
        except Exception as e:
            _eprint("teamwork-cost-capture: ledger append failed:", e)
            return 0
    if new_uuids:
        try:
            with open(watermark_path, "a", encoding="utf-8") as f:
                for u in new_uuids:
                    f.write(u + "\n")
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except Exception:
        # Absolute backstop — never break the run.
        sys.exit(0)
