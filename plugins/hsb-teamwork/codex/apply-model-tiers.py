#!/usr/bin/env python3
"""Stamp Codex agent model tiers from the single source of truth.

Reads codex/model-tiers.toml and writes the `model` and `model_reasoning_effort`
lines into each codex/agents/<agent>.toml. Codex has no model aliases and agents
cannot reference a config profile, so the literal ids must live in each toml — this
keeps them all in sync with one declaration. Idempotent; run after editing the map.

    python3 codex/apply-model-tiers.py [--check]

--check exits non-zero if any toml is out of sync (for CI), changing nothing.
"""
from __future__ import annotations
import re, sys, tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAP = ROOT / "model-tiers.toml"
AGENTS_DIR = ROOT / "agents"


def stamp(text: str, model: str, effort: str) -> str:
    text, n_m = re.subn(r'(?m)^model\s*=.*$', f'model = "{model}"', text, count=1)
    text, n_e = re.subn(
        r'(?m)^model_reasoning_effort\s*=.*$',
        f'model_reasoning_effort = "{effort}"', text, count=1)
    if n_m == 0:
        raise SystemExit("missing `model` line")
    if n_e == 0:
        raise SystemExit("missing `model_reasoning_effort` line")
    return text


def main() -> int:
    check = "--check" in sys.argv[1:]
    cfg = tomllib.loads(MAP.read_text())
    tiers, agents = cfg["tiers"], cfg["agents"]

    drift, applied = [], 0
    for name, tier in agents.items():
        toml = AGENTS_DIR / f"{name}.toml"
        if not toml.exists():
            print(f"skip   {name}: no toml yet")
            continue
        t = tiers[tier]
        current = toml.read_text()
        updated = stamp(current, t["model"], t["reasoning_effort"])
        if updated != current:
            drift.append(name)
            if not check:
                toml.write_text(updated)
        applied += 1
        print(f'{name:24} -> {tier:6} ({t["model"]}, {t["reasoning_effort"]})')

    if check and drift:
        print(f"\nOUT OF SYNC: {', '.join(drift)} — run apply-model-tiers.py")
        return 1
    print(f"\n{'checked' if check else 'stamped'} {applied} agent(s); "
          f"{len(drift)} {'drifted' if check else 'changed'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
