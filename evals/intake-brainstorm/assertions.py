#!/usr/bin/env python3
"""Deterministic structural grader for an intake-brainstorm target document.

Validates a produced target-document.md against the contract encoded in its own
section annotations (<!-- intake: id=...; blocks=...; min-confidence=...; kind=... -->).
No LLM required. Pairs with rubric.md (the qualitative LLM-graded layer).

Usage:  python3 assertions.py <path/to/target-document.md>
Exits 0 if all hard checks pass, 1 otherwise. Prints a JSON report.
"""
import re, sys, json

SENTINEL = "<!-- END OF DOCUMENT -->"
ANNOT = re.compile(r"<!--\s*intake:\s*(.*?)\s*-->")
HONEST = {"assumption", "discovery", "deferred"}
TRUNC = ["(unchanged)", "[continues]", "remaining sections omitted",
         "[fill]", "[placeholder]", "[Demand name]"]

def parse_annotation(s):
    d = {}
    for part in s.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip()
    return d

HEADING = re.compile(r"^#{2,6}\s+(.*)")

def split_sections(text):
    """Return list of (heading, annotation_dict|None, body) per heading (## .. ######)."""
    lines = text.splitlines()
    secs, cur = [], None
    for ln in lines:
        m = HEADING.match(ln)
        if m:
            if cur: secs.append(cur)
            cur = [m.group(1).strip(), None, []]
        elif cur is not None:
            m = ANNOT.search(ln)
            if m and cur[1] is None:
                cur[1] = parse_annotation(m.group(1))
            cur[2].append(ln)
    if cur: secs.append(cur)
    return [(h, a, "\n".join(b)) for h, a, b in secs]

def conf_line(body):
    c = re.search(r"`?Confidence:`?\s*([0-9]{1,3}|__)", body)
    disp = re.search(r"`?Disposition:`?\s*([A-Za-z_]+|__)", body)
    conf = c.group(1) if c else None
    return (None if conf in (None, "__") else int(conf)), (disp.group(1).lower() if disp else None)

def grade(path):
    text = open(path, encoding="utf-8").read()
    checks = []
    def add(name, ok, detail=""): checks.append({"check": name, "ok": bool(ok), "detail": detail})

    # 1. No truncation: sentinel is the final non-empty line.
    last = [l for l in text.splitlines() if l.strip()]
    add("sentinel_present", bool(last) and last[-1].strip() == SENTINEL,
        "last line: " + (last[-1].strip() if last else "<empty>"))
    # 2. No truncation/placeholder markers.
    found = [m for m in TRUNC if m in text]
    add("no_truncation_markers", not found, "found: " + ", ".join(found) if found else "clean")

    secs = split_sections(text)
    annotated = [(h, a, b) for h, a, b in secs if a and a.get("id")]
    add("has_annotations", len(annotated) >= 5, f"{len(annotated)} annotated sections")

    # 3. Every blocking capture section is resolved or honestly disposed.
    blocking = [(h, a, b) for h, a, b in annotated
                if a.get("blocks") == "true" and a.get("kind") == "capture"]
    sat = 0
    for h, a, b in blocking:
        thr = int(a.get("min-confidence", "70"))
        conf, disp = conf_line(b)
        ok = (disp in HONEST) or (conf is not None and conf >= thr)
        if ok: sat += 1
        add(f"blocking[{a['id']}]_satisfied", ok,
            f"conf={conf} thr={thr} disp={disp}")
    readiness = round(100 * sat / len(blocking)) if blocking else 0

    # 4. Capture/derived sections carry a confidence line.
    cap = [(h, a, b) for h, a, b in annotated if a.get("kind") in ("capture", "derived")]
    missing = [a["id"] for h, a, b in cap
               if a.get("kind") == "capture" and int(a.get("min-confidence", "0")) > 0
               and "Confidence:" not in b]
    add("confidence_lines_present", not missing,
        "missing on: " + ", ".join(missing) if missing else "all present")

    # 5. Triage (derived) is flagged as a draft pending human sign-off.
    tri = [b for h, a, b in annotated if a.get("id") == "triage"]
    if tri:
        t = tri[0].lower()
        add("triage_flagged_draft",
            ("draft" in t) and ("pending" in t or "confirm" in t),
            "banner found" if "draft" in t else "no DRAFT banner")

    hard = [c for c in checks if not c["check"].startswith("blocking[")] + \
           [c for c in checks if c["check"].startswith("blocking[")]
    ok_all = all(c["ok"] for c in checks)
    return {"file": path, "pass": ok_all, "readiness_pct": readiness,
            "blocking_satisfied": f"{sat}/{len(blocking)}", "checks": checks}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: assertions.py <target-document.md>"); sys.exit(2)
    rep = grade(sys.argv[1])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    sys.exit(0 if rep["pass"] else 1)
