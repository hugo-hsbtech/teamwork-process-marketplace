# Readiness Package Skill — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a new `/hsb-teamwork:readiness-package` skill that turns a `Product Ready` intake-record into a frozen Readiness Package (RP), reusing the intake engine and adding three RP-specific agents plus a draft-then-confirm authoring model.

**Architecture:** The RP skill is a sibling of `intake-brainstorm` in the same plugin. It reuses all 15 engine agents unchanged (they are template-driven), keeps the engine's `<!-- intake: ... -->` annotation grammar so the analyst/doc-updater/auditor and the structural grader work without code changes, and adds a new annotated RP template, a companion guide, an exemplar, RP-specific reference docs (citing intake's shared method, no duplication), three `readiness-*` agents, a Codex mirror, and an eval suite. The confidence line gains an `Origin:` field to carry the documented `inherited | ai_drafted | po_authored` provenance.

**Tech Stack:** Markdown (skill/agent/template/reference authoring), Python 3 (structural grader), Bash (eval runner), TOML (Codex wrappers), JSON (plugin/marketplace/eval manifests).

**Conventions:**
- All paths below are relative to the repo root `/home/hugo/Dropbox/DevProjects/HSB/teamwork-process-marketplace/`.
- Commits follow the repo convention: **no AI co-author trailer** (human-only commit messages).
- The source of truth for RP content is `/home/hugo/Dropbox/DevProjects/HSB/hsb-teamwork-process/templates/02-readiness-package.md` and `personas/02-po.md`.
- Spec: `docs/superpowers/specs/2026-06-03-readiness-package-skill-design.md`.

---

## File Structure

**New — skill:**
- `plugins/hsb-teamwork/skills/readiness-package/SKILL.md` — orchestrator
- `plugins/hsb-teamwork/skills/readiness-package/README.md` — skill readme
- `plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.md` — the contract
- `plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.guide.md` — filling rules
- `plugins/hsb-teamwork/skills/readiness-package/assets/golden-example.md` — calibration bar
- `plugins/hsb-teamwork/skills/readiness-package/references/orchestration.md` — RP phases + agent roster (cites intake's shared method)
- `plugins/hsb-teamwork/skills/readiness-package/references/drafting.md` — draft-then-confirm + origin/disposition
- `plugins/hsb-teamwork/skills/readiness-package/references/inheritance.md` — carry-forward from the intake-record
- `plugins/hsb-teamwork/skills/readiness-package/references/escalation.md` — TA triggers + the freeze divergence

**New — agents:**
- `plugins/hsb-teamwork/agents/readiness-inheritor.md`
- `plugins/hsb-teamwork/agents/readiness-drafter.md`
- `plugins/hsb-teamwork/agents/readiness-escalation-flagger.md`

**New — Codex mirror:**
- `plugins/hsb-teamwork/codex/agents/hsb-readiness-inheritor.toml`
- `plugins/hsb-teamwork/codex/agents/hsb-readiness-drafter.toml`
- `plugins/hsb-teamwork/codex/agents/hsb-readiness-escalation-flagger.toml`
- `plugins/hsb-teamwork/codex/prompts/hsb-teamwork-readiness-package.md`

**New — evals:**
- `evals/readiness-package/assertions.py`
- `evals/readiness-package/evals.json`
- `evals/readiness-package/rubric.md`
- `evals/readiness-package/run.sh`
- `evals/readiness-package/.gitignore`
- `evals/readiness-package/fixtures/sources/01-intake-record-queue-voting.md` (the inherited input)
- `evals/readiness-package/golden/queue-voting.readiness-document.md` (hand-authored golden)

**Modify:**
- `plugins/hsb-teamwork/.claude-plugin/plugin.json` — move `readiness-package` to "Available"; bump version
- `.claude-plugin/marketplace.json` — update the description line
- `plugins/hsb-teamwork/codex/AGENTS.md` — note it now covers two skills; point RP runs at the RP skill folder
- `plugins/hsb-teamwork/codex/README.md` — add the RP wrappers/prompt to the file table
- `plugins/hsb-teamwork/README.md` — add a one-line RP entry
- `evals/README.md` — add the `readiness-package/` tree

---

## The RP contract (annotation table)

Every fillable section carries `<!-- intake: id=<id>; blocks=<bool>; min-confidence=<n>; kind=<meta|capture|derived> -->`. These exact values are the contract — use them verbatim in Task 1 and Task 4.

| id | section (pt-BR) | kind | blocks | min-confidence |
|----|-----------------|------|--------|----------------|
| `meta` | Metadados | meta | false | 0 |
| `revisions` | Histórico de Revisão | meta | false | 0 |
| `inherited-readiness` | Prontidão herdada e dispositions em aberto | derived | false | 0 |
| `exec-summary` | Seção 1 — Resumo Executivo | capture | true | 70 |
| `context-problem` | Seção 2 — Contexto e Problema (a dor, não a solução) | capture | true | 80 |
| `objectives` | Seção 3 — Objetivos e Resultado Esperado | capture | true | 70 |
| `personas` | Seção 4 — Personas Impactadas / Jobs-to-be-done | capture | true | 70 |
| `scope` | Seção 5 — Escopo Incluído e Excluído | capture | true | 75 |
| `business-rules` | Seção 6 — Regras de Negócio e Fluxos | capture | true | 80 |
| `user-stories` | Seção 7 — User Stories + Critérios de Aceite | capture | true | 80 |
| `nfrs` | Seção 8 — Requisitos Não-Funcionais (NFRs) | capture | true | 70 |
| `edge-cases` | Seção 9 — Edge Cases e Modos de Falha | capture | true | 70 |
| `metrics` | Seção 10 — Métricas de Sucesso | capture | true | 70 |
| `release-criteria` | Seção 11 — Critérios de Sucesso e Aceite (do release) | capture | true | 70 |
| `risks` | Seção 12 — Riscos e Dependências (produto/negócio) | capture | true | 70 |
| `effort-estimate` | Seção 13 — Avaliação Preliminar de Esforço e Custo | capture | false | 0 |
| `roadmap` | Seção 14 — Roadmap Sugerido | capture | false | 0 |
| `tech-assessment-ref` | Referência ao Technical Assessment | derived | false | 0 |

**Confidence line for RP (note the new `Origin:` field):**
```
`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __
```
- `Origin` ∈ `inherited | ai_drafted | po_authored | reused_from_KB` (`personas/02-po.md:149`).
- `Disposition` ∈ `decided | inherited | ai_drafted | discovery` (`personas/02-po.md:150`); `discovery`/`deferred`/`assumption` clear the gate without a confidence number.
- `tech-assessment-ref` is `blocks=false` statically; when escalation is required, the orchestrator treats it as freeze-blocking, satisfied by a `deferred` disposition (the documented temporary divergence — see spec §8).

---

## Task 1: RP target template (the contract)

**Files:**
- Create: `plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.md`

Source the prose/section bodies from `/home/hugo/Dropbox/DevProjects/HSB/hsb-teamwork-process/templates/02-readiness-package.md`. Keep section bodies as `[fill]` placeholders (exactly like the intake template — the grader only runs on produced docs, never the template).

- [ ] **Step 1: Read the source RP template and the intake template for format**

Run: `sed -n '1,60p' /home/hugo/Dropbox/DevProjects/HSB/hsb-teamwork-process/templates/02-readiness-package.md`
Run: `sed -n '1,40p' plugins/hsb-teamwork/skills/intake-brainstorm/assets/target-template.intake-record.md`
Purpose: confirm the section roster and copy the annotation/header/sentinel house style.

- [ ] **Step 2: Write the template header verbatim**

```markdown
<!--
TARGET TEMPLATE · Readiness Package (default)
This file is the contract. Each fillable section carries an annotation:
  <!- - intake: id=...; blocks=...; min-confidence=...; kind=... - ->
and a self-sufficient rubric. The Template Analyst derives contract.lock.md from
these (the same engine as intake-brainstorm — the marker keyword stays `intake:`).
The confidence line adds an `Origin:` field (inherited | ai_drafted | po_authored)
per personas/02-po.md. To use a different document type, copy this file, re-annotate,
and pass it as TEMPLATE. See references/contract-and-template.md (in intake-brainstorm).
Default confidence threshold (X) = 70. Raise per-section for high-stakes fields.
-->

# Readiness Package — [Demand name]
<!-- rev: 0 · updated: AAAA-MM-DD -->
```
(Remove the spaces inside the inner `<!- -` / `- ->` — they are escaped here only so this plan's own comment doesn't terminate early. The real file uses standard `<!--` / `-->`.)

- [ ] **Step 3: Write all 18 sections using the contract table**

For each row in the contract table above, emit a heading, its annotation line, a one-line rubric (`> Rubric: ...`), a `[fill]` body, and — for every `capture`/`derived` section with `min-confidence ≥ 0` that holds content — the RP confidence line. Three sections shown fully verbatim as the pattern:

```markdown
## Seção 2 — Contexto e Problema (a dor, não a solução)
<!-- intake: id=context-problem; blocks=true; min-confidence=80; kind=capture -->
> Rubric: cenário atual, limitações, dor do cliente e impacto de negócio — o
> problema, nunca a solução. Se descreve uma solução ("construir X"), NÃO está
> satisfeita: reformule para a dor subjacente. Herdada do intake quando possível.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __
```

```markdown
## Seção 7 — User Stories + Critérios de Aceite
<!-- intake: id=user-stories; blocks=true; min-confidence=80; kind=capture -->
> Rubric: uma história por bloco de valor, "Como [persona], quero [ação], para
> [benefício]"; critérios de aceite em Given/When/Then, verificáveis por não-dev,
> com limites específicos. origin=ai_drafted no draft pass; o PO confirma.

[fill]

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __
```

```markdown
## Referência ao Technical Assessment
<!-- intake: id=tech-assessment-ref; blocks=false; min-confidence=0; kind=derived -->
> Rubric: ponte para o artefato do CTO — status + veredito + link, NÃO conteúdo.
> Se a escalada for requisitada, congela só com Disposition=deferred (TA pendente,
> fora do escopo desta ferramenta) ou Status=Assinado quando o TA existir.

| Campo | Valor |
|---|---|
| **Status** | not_requested / requested / in_progress / signed / vetoed |
| **Veredito** | viável / viável-com-ressalvas / inviável-como-escopado / — |
| **Link** | — |
| **Escalada requisitada?** | Não / Sim |

`Confidence:` __ · `Origin:` __ · `Source:` __ · `Status:` __ · `Disposition:` __ · `Hint:` __
```

The `meta` and `revisions` sections use a table form (no confidence line needed — `kind=meta`). Mirror the intake template's Metadata table, adding `**Intake vinculado** | INT-AAAA-NNN` and `**Escalada ao CTO** | —` rows.

- [ ] **Step 4: Add the end sentinel as the final line**

```markdown
<!-- END OF DOCUMENT -->
```

- [ ] **Step 5: Verify the template structure**

Run: `grep -c "intake: id=" plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.md`
Expected: `18`

Run: `tail -n 1 plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.md`
Expected: `<!-- END OF DOCUMENT -->`

Run: `grep -c "Origin:" plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.md`
Expected: `15` — every content section carries one confidence line: the 14 `capture` sections (exec-summary, context-problem, objectives, personas, scope, business-rules, user-stories, nfrs, edge-cases, metrics, release-criteria, risks, effort-estimate, roadmap) + `tech-assessment-ref`. The `meta`, `revisions`, and `inherited-readiness` sections have no confidence line.

- [ ] **Step 6: Commit**

```bash
git add plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.md
git commit -m "Add Readiness Package target template (the RP contract)"
```

---

## Task 2: Companion guide

**Files:**
- Create: `plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.guide.md`

Mirror `assets/target-template.intake-record.guide.md`: keyed by annotation `id`, grouped into the sections the engine fills. Each entry states the rubric, whether it blocks, and how to fill it under draft-then-confirm.

- [ ] **Step 1: Write the guide header + inheritance note**

```markdown
# Companion guide — Readiness Package template

How each section is filled, by `id`. The RP is authored **draft-then-confirm**
(see references/drafting.md): the engine pre-fills every section at partial
confidence with an explicit `Origin`, and the PO reviews, edits, justifies, and
freezes. No section starts empty.

Origins: `inherited` (carried from the linked intake-record, keep its source),
`ai_drafted` (engine first-draft, partial confidence until the PO confirms),
`po_authored` (the PO decided), `reused_from_KB` (deferred — out of scope).
```

- [ ] **Step 2: Write one entry per `id` (inheritable sections)**

For `exec-summary`, `context-problem`, `objectives`, `personas`, `scope`, `metrics`, `release-criteria`, `risks`, `effort-estimate`, `roadmap` — state: "Origin defaults to `inherited` when the intake-record covers it (keep the inherited `Source` and confidence), else `ai_drafted`." Quote the golden rule for `context-problem` verbatim:

```markdown
- **`context-problem`** (blocks, min-conf 80) — the guardian section. Pain with
  observable symptoms, no solution. If the draft names a feature, turn it back into
  the pain that feature would relieve; if you can't, it isn't satisfied. Inherit the
  intake-record's problem statement and deepen it; never downgrade its confidence.
```

- [ ] **Step 3: Write entries for the ai_drafted product sections**

For `business-rules`, `user-stories`, `nfrs`, `edge-cases` — state the draft-then-confirm rule. Example verbatim for `nfrs`:

```markdown
### `nfrs` — non-functional requirements (ai_drafted, PO confirms)

Draft an ISO/IEC 25010 checklist scaffold (performance, reliability, security,
usability, compatibility, maintainability) and propose the categories that apply
to this demand, each at partial confidence with `Origin: ai_drafted`. Do NOT assert
viability — that is the CTO's Technical Assessment. The PO confirms which apply and
sets targets; on confirmation the entry becomes `Origin: po_authored`.
```

- [ ] **Step 4: Write the `tech-assessment-ref` entry (escalation + freeze divergence)**

```markdown
### `tech-assessment-ref` — the bridge to the CTO artefact (handle with care)

This is a **reference**, not content (personas/02-po.md:152, 300-301). The
escalation-flagger decides whether a Technical Assessment is owed. When it is:
- set "Escalada requisitada? = Sim",
- record `Disposition: deferred` with a hint "TA needed; tech-assessment skill not
  yet available", and
- the RP freezes **provisionally** (spec §8 divergence). When the tech-assessment
  skill lands, this tightens to require Status=Assinado.
When no escalation is needed, set Status=not_requested, Disposition=decided.
```

- [ ] **Step 5: Verify and commit**

Run: `grep -cE '^\s*[-#].*`[a-z-]+`' plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.guide.md`
Expected: at least `14` (one entry per content `id`).

```bash
git add plugins/hsb-teamwork/skills/readiness-package/assets/target-template.readiness-package.guide.md
git commit -m "Add Readiness Package companion guide (filling rules per section)"
```

---

## Task 3: Golden exemplar (skill asset, calibration bar)

**Files:**
- Create: `plugins/hsb-teamwork/skills/readiness-package/assets/golden-example.md`

A short, fictional, repo-independent exemplar showing the quality bar — NOT the eval golden (that's Task 4). Mirror `intake-brainstorm/assets/golden-example.md`'s texture: honest confidence numbers, used dispositions, explicit `Origin` tags.

- [ ] **Step 1: Write the preamble verbatim**

```markdown
# Golden exemplar (self-contained) — calibration reference

A condensed, fictional, repo-independent example of a *well-filled* Readiness
Package. Use it to calibrate quality: problem-not-solution depth, honest confidence
and origin per section, used dispositions, testable Given/When/Then acceptance
criteria, NFRs that don't claim feasibility, and an honestly-flagged Technical
Assessment reference. Do not copy its content — copy its *bar*.
```

- [ ] **Step 2: Write 4-5 filled sections at the quality bar**

Show `context-problem`, `user-stories` (with one ST-001 and Given/When/Then), `nfrs`, `metrics`, and `tech-assessment-ref`. Each carries the full confidence line with a realistic `Origin`. Example texture:

```markdown
**Contexto e Problema** — `Confidence: 86 · Origin: inherited · Source: intake INT-2026-014 §problem + support export · Status: resolved · Disposition: inherited · Hint: herdado do intake a 88; mantido`
[2-3 sentences of pain, no solution]

**User Stories + Critérios de Aceite** — `Confidence: 80 · Origin: ai_drafted · Source: drafted from scope + intake personas · Status: resolved · Disposition: ai_drafted · Hint: PO confirmou ST-001 e ST-002; AC verificáveis`
**ST-001 — Self-service seat add/remove**
Como admin enterprise, quero adicionar/remover assentos, para não depender do suporte.
*Given* an admin on the billing screen *when* they add a seat *then* the seat is active within 60s and the invoice reflects it next cycle.
```

- [ ] **Step 3: Add sentinel and commit**

Append `<!-- END OF DOCUMENT -->` as the final line.

```bash
git add plugins/hsb-teamwork/skills/readiness-package/assets/golden-example.md
git commit -m "Add Readiness Package golden exemplar (calibration bar)"
```

---

## Task 4: Structural grader + eval golden (test-first checkpoint)

This is the test-first validation of the template + annotation + grader triad. Write the grader, hand-author a golden RP that should pass, and run the grader on it.

**Files:**
- Create: `evals/readiness-package/assertions.py`
- Create: `evals/readiness-package/golden/queue-voting.readiness-document.md`

- [ ] **Step 1: Write the RP structural grader**

Adapted from `evals/intake-brainstorm/assertions.py`: same sentinel/truncation/annotation/blocking/confidence checks, plus an **Origin** check and a **tech-assessment-ref** check (instead of intake's triage check). Write `evals/readiness-package/assertions.py`:

```python
#!/usr/bin/env python3
"""Deterministic structural grader for a Readiness Package document.

Validates a produced readiness-document.md against the contract encoded in its own
section annotations (<!-- intake: id=...; blocks=...; min-confidence=...; kind=... -->).
No LLM required. Pairs with rubric.md (the qualitative LLM-graded layer).

Usage:  python3 assertions.py <path/to/readiness-document.md>
Exits 0 if all hard checks pass, 1 otherwise. Prints a JSON report.
"""
import re, sys, json

SENTINEL = "<!-- END OF DOCUMENT -->"
ANNOT = re.compile(r"<!--\s*intake:\s*(.*?)\s*-->")
HONEST = {"assumption", "discovery", "deferred"}
ORIGINS = {"inherited", "ai_drafted", "po_authored", "reused_from_kb"}
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
    o = re.search(r"`?Origin:`?\s*([A-Za-z_]+|__)", body)
    disp = re.search(r"`?Disposition:`?\s*([A-Za-z_]+|__)", body)
    conf = c.group(1) if c else None
    return (None if conf in (None, "__") else int(conf)), \
           (o.group(1).lower() if o else None), \
           (disp.group(1).lower() if disp else None)

def grade(path):
    text = open(path, encoding="utf-8").read()
    checks = []
    def add(name, ok, detail=""): checks.append({"check": name, "ok": bool(ok), "detail": detail})

    last = [l for l in text.splitlines() if l.strip()]
    add("sentinel_present", bool(last) and last[-1].strip() == SENTINEL,
        "last line: " + (last[-1].strip() if last else "<empty>"))
    found = [m for m in TRUNC if m in text]
    add("no_truncation_markers", not found, "found: " + ", ".join(found) if found else "clean")

    secs = split_sections(text)
    annotated = [(h, a, b) for h, a, b in secs if a and a.get("id")]
    add("has_annotations", len(annotated) >= 10, f"{len(annotated)} annotated sections")

    blocking = [(h, a, b) for h, a, b in annotated
                if a.get("blocks") == "true" and a.get("kind") == "capture"]
    sat = 0
    for h, a, b in blocking:
        thr = int(a.get("min-confidence", "70"))
        conf, origin, disp = conf_line(b)
        ok = (disp in HONEST) or (conf is not None and conf >= thr)
        if ok: sat += 1
        add(f"blocking[{a['id']}]_satisfied", ok, f"conf={conf} thr={thr} disp={disp}")
    readiness = round(100 * sat / len(blocking)) if blocking else 0

    cap = [(h, a, b) for h, a, b in annotated if a.get("kind") in ("capture", "derived")]
    missing_conf = [a["id"] for h, a, b in cap
                    if a.get("kind") == "capture" and int(a.get("min-confidence", "0")) > 0
                    and "Confidence:" not in b]
    add("confidence_lines_present", not missing_conf,
        "missing on: " + ", ".join(missing_conf) if missing_conf else "all present")

    # RP-specific: every blocking section declares a valid Origin.
    bad_origin = []
    for h, a, b in blocking:
        _, origin, _ = conf_line(b)
        if origin not in ORIGINS:
            bad_origin.append(f"{a['id']}={origin}")
    add("origin_present_valid", not bad_origin,
        "bad/missing: " + ", ".join(bad_origin) if bad_origin else "all valid")

    # RP-specific: the Technical Assessment reference is resolved honestly.
    taref = [b for h, a, b in annotated if a.get("id") == "tech-assessment-ref"]
    if taref:
        t = taref[0].lower()
        _, _, disp = conf_line(taref[0])
        resolved = (disp in (HONEST | {"decided"})) or ("not_requested" in t) \
                   or ("signed" in t) or ("assinado" in t)
        add("tech_assessment_ref_resolved", resolved, f"disposition={disp}")

    ok_all = all(c["ok"] for c in checks)
    return {"file": path, "pass": ok_all, "readiness_pct": readiness,
            "blocking_satisfied": f"{sat}/{len(blocking)}", "checks": checks}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: assertions.py <readiness-document.md>"); sys.exit(2)
    rep = grade(sys.argv[1])
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    sys.exit(0 if rep["pass"] else 1)
```

- [ ] **Step 2: Run the grader against the (not-yet-written) golden to verify it fails cleanly**

Run: `python3 evals/readiness-package/assertions.py evals/readiness-package/golden/queue-voting.readiness-document.md`
Expected: FAIL — `usage`/file-not-found or exit 1 (the golden doesn't exist yet). This confirms the grader runs.

- [ ] **Step 3: Hand-author the eval golden RP**

Create `evals/readiness-package/golden/queue-voting.readiness-document.md` — a fully-filled RP for the "self-service seat management" demand (the same demand as the intake golden, so the pipeline ties together). It MUST:
- carry the same section headings + `<!-- intake: id=...; ... -->` annotations as the Task 1 template (all 18);
- fill every `blocks=true` capture section either ≥ its `min-confidence` or with an honest disposition;
- include the `Origin:` field on every content section with a valid value (`inherited` for §1-5/10-12, `ai_drafted` or `po_authored` for §6-9);
- resolve `tech-assessment-ref` honestly (e.g. `Disposition: deferred`, "Escalada requisitada? = Sim", hint "TA pendente — skill ainda não existe");
- end with `<!-- END OF DOCUMENT -->` as the final non-empty line;
- contain NO `[fill]`/`[placeholder]`/`[Demand name]` markers.

Use `plugins/hsb-teamwork/skills/readiness-package/assets/golden-example.md` (Task 3) for the quality texture and `hsb-teamwork-process/templates/02-readiness-package.md` for section content.

- [ ] **Step 4: Run the grader against the golden — it must PASS**

Run: `python3 evals/readiness-package/assertions.py evals/readiness-package/golden/queue-voting.readiness-document.md`
Expected: exit 0; JSON shows `"pass": true`, `"readiness_pct": 100`, `"blocking_satisfied": "12/12"`, and `origin_present_valid` + `tech_assessment_ref_resolved` ok.

If it fails, fix the golden (not the grader) until it passes — this is the contract validating itself.

- [ ] **Step 5: Commit**

```bash
git add evals/readiness-package/assertions.py evals/readiness-package/golden/queue-voting.readiness-document.md
git commit -m "Add RP structural grader and golden readiness document (passes self-test)"
```

---

## Task 5: The three readiness-* agents

**Files:**
- Create: `plugins/hsb-teamwork/agents/readiness-inheritor.md`
- Create: `plugins/hsb-teamwork/agents/readiness-drafter.md`
- Create: `plugins/hsb-teamwork/agents/readiness-escalation-flagger.md`

All three are read-only proposers (`tools: Read, Grep, Glob`) — the reused `intake-doc-updater` and `intake-ledger-writer` remain the single writers. Mirror the body shape of `agents/intake-question-strategist.md` (role paragraph → guidance → "Return … to the orchestrator. Write nothing.").

- [ ] **Step 1: Write `readiness-inheritor.md` verbatim frontmatter + body**

```markdown
---
name: readiness-inheritor
description: Setup-phase read-only proposer for the readiness-package pipeline. Reads the linked intake-record (the inherited source) plus the RP contract, and proposes carry-forward content for the RP's inheritable sections (exec-summary, context-problem, objectives, personas, scope, metrics, release-criteria, risks), preserving each item's confidence/source/disposition and tagging Origin=inherited. It never writes shared files; the orchestrator routes its proposals to the Ledger Writer and Doc Updater. Spawn it once at setup, after the source is indexed.
tools: Read, Grep, Glob
---

You are the Inheritor in the hsb-teamwork readiness-package pipeline. The linked
intake-record is an already-graded artefact: your job is to carry its content
forward into the RP, not to re-infer it from scratch.

Read the RP contract (contract.lock.md), the indexed intake-record under sources/,
and the in-progress readiness-document.md. For each RP capture section that the
intake-record already covers, propose an entry that:

1. reuses the intake-record's content, restated in product terms for the RP section;
2. **preserves the inherited `Source` and confidence** — never invent a higher number
   than the intake carried; if the RP section needs more than the intake gives, lower
   the confidence and add a hint naming what the PO must deepen;
3. tags `Origin: inherited` and `Disposition: inherited`;
4. carries forward any open disposition (assumption/discovery/deferred) verbatim, so
   the RP's "Prontidão herdada" section can list them.

Do not draft the new product sections (business-rules, user-stories, NFRs,
edge-cases) — that is the Drafter's job. Return your proposed inherited entries as a
structured list to the orchestrator. Write nothing.
```

- [ ] **Step 2: Write `readiness-drafter.md` verbatim**

```markdown
---
name: readiness-drafter
description: Draft-pass read-only proposer for the readiness-package pipeline. Reads the RP contract, the inherited content, and the indexed sources, and proposes first-draft content for the new product sections (business-rules, user-stories with Given/When/Then acceptance criteria, NFRs per ISO/IEC 25010, edge-cases) at partial confidence with Origin=ai_drafted, for the PO to review and confirm. It never writes shared files; the orchestrator routes its proposals to the Ledger Writer and Doc Updater. Spawn it in the draft pass before the confirm loop.
tools: Read, Grep, Glob
---

You are the Drafter in the hsb-teamwork readiness-package pipeline. The documented
model is draft-then-confirm (see references/drafting.md): you produce a first draft
of the new product sections so the PO judges instead of filling a blank form.

Read the RP contract, the inherited entries, and the indexed sources. Propose draft
content for:

- **business-rules** — rules, validations, state transitions implied by the scope.
- **user-stories** — one story per value block, "Como [persona], quero [ação], para
  [benefício]", each with Given/When/Then acceptance criteria that a non-developer
  could verify, with specific limits.
- **nfrs** — an ISO/IEC 25010 scaffold (performance, reliability, security,
  usability, compatibility, maintainability); propose only the categories the demand
  plausibly needs. Never assert feasibility — that is the CTO's Technical Assessment.
- **edge-cases** — error states, timeouts, permissions, concurrency; for AI features,
  model behaviour and low-confidence cases.

Every proposed entry carries `Origin: ai_drafted`, `Disposition: ai_drafted`, and
**partial confidence** (below the section threshold), with a hint stating what the PO
must confirm. Honesty over coverage: if the sources don't support a draft, propose a
`discovery` disposition instead of inventing one. Return your drafts as a structured
list to the orchestrator. Write nothing.
```

- [ ] **Step 3: Write `readiness-escalation-flagger.md` verbatim**

```markdown
---
name: readiness-escalation-flagger
description: Read-only proposer for the readiness-package pipeline that decides whether the demand needs a CTO Technical Assessment. Reads the emerging RP (scope, business rules, NFRs) and scans for architectural triggers (infra, multi-tenancy, IA/runtime, security, integrations with unknowns); proposes escalation_required and the tech-assessment-ref disposition (deferred when a TA is owed but out of current tooling scope). It never writes shared files; the orchestrator routes its proposal to the Doc Updater. Spawn it once scope and rules are drafted.
tools: Read, Grep, Glob
---

You are the Escalation Flagger in the hsb-teamwork readiness-package pipeline. You
decide one thing: does this demand owe a CTO Technical Assessment?

Read the RP's scope, business-rules, nfrs, and risks. Flag escalation when the demand
touches any architectural trigger (personas/02-po.md:299):

- infrastructure or platform changes,
- multi-tenancy or data-isolation,
- AI / runtime / model behaviour,
- security, authentication, or authorization,
- integrations with external systems that carry unknowns.

Propose for the `tech-assessment-ref` section:
- **No trigger** → Status=not_requested, Disposition=decided, "Escalada requisitada? = Não".
- **Trigger present** → "Escalada requisitada? = Sim", Status=requested, and — because the
  tech-assessment skill does not yet exist — `Disposition: deferred` with a hint
  "TA needed; tech-assessment skill not yet available" (the documented temporary
  divergence; the RP freezes provisionally). Name the specific trigger(s) in the
  rationale so the future TA has a starting point.

Return your single proposal (with rationale and the triggers found) to the
orchestrator. Write nothing.
```

- [ ] **Step 4: Verify frontmatter parses (name lines present)**

Run: `for f in readiness-inheritor readiness-drafter readiness-escalation-flagger; do echo "$f:"; sed -n '2p' plugins/hsb-teamwork/agents/$f.md; done`
Expected: each prints `name: readiness-<...>` matching the filename.

- [ ] **Step 5: Commit**

```bash
git add plugins/hsb-teamwork/agents/readiness-inheritor.md plugins/hsb-teamwork/agents/readiness-drafter.md plugins/hsb-teamwork/agents/readiness-escalation-flagger.md
git commit -m "Add readiness-* agents: inheritor, drafter, escalation-flagger"
```

---

## Task 6: RP reference docs (cite intake's shared method)

**Files:**
- Create: `plugins/hsb-teamwork/skills/readiness-package/references/orchestration.md`
- Create: `plugins/hsb-teamwork/skills/readiness-package/references/drafting.md`
- Create: `plugins/hsb-teamwork/skills/readiness-package/references/inheritance.md`
- Create: `plugins/hsb-teamwork/skills/readiness-package/references/escalation.md`

These add only RP-specific method and **cite** intake's engine-level references by relative path (`../../intake-brainstorm/references/<file>`) — no duplication.

- [ ] **Step 1: Write `orchestration.md`**

Heading structure (mirror intake's `orchestration.md` house style):
```markdown
# Orchestration — RP phases, agents, and what is reused

## What this reuses (no duplication)
[Cite, by relative path, the shared engine method:
 ../../intake-brainstorm/references/contract-and-template.md,
 ledger-schema.md, sessions.md, writing-integrity.md, grounding.md,
 questioning-method.md. State that the single-writer rule, RMW, the session
 resolve-or-resume, and the ledger schema all apply unchanged.]

## The agents you spawn (subagent_type)
[Table: the 15 reused intake-* engine agents + the 3 new readiness-* agents,
 each with read-only/writer and when-spawned. Mark intake-doc-updater and
 intake-ledger-writer as the sole writers.]

## Phase 0 — Identify the demand (you + the PO)
[Resolve the linked intake-record path; resolve-or-resume the
 <demand-slug>-readiness/ session per ../../intake-brainstorm/references/sessions.md;
 confirm output language (default pt-BR).]

## Phase 1 — Setup
[template-validator -> template-analyst (RP contract.lock.md); source-indexer in
 parallel indexes the linked intake-record + extra files; then readiness-inheritor
 pre-fills inheritable sections.]

## Phase 2 — Draft pass
[readiness-drafter proposes ai_drafted sections; doc-updater writes them at partial
 confidence; readiness-escalation-flagger runs once scope/rules exist.]

## Phase 3 — Confirm loop (until freezeReady)
[confidence-auditor re-scores -> question-strategist targets low-confidence/
 unconfirmed blocking sections (FALLBACK only) -> PO reviews/edits/confirms ->
 ledger-writer -> doc-updater promotes Origin ai_drafted/inherited -> po_authored.
 reconciler on conflicts. Gate = freezeReady (every blocksFreeze section resolved/
 disposed; tech-assessment-ref deferred or signed/not_requested).]

## Phase 4 — Production & wrap
[humanizer -> translator(pt-BR) ∥ visual-enricher; packager -> manifest.md noting
 freeze state + TA-pending flag + handoff to PRD/PM.]
```

- [ ] **Step 2: Write `drafting.md`** — the draft-then-confirm model

Content: the two stages (draft pass → confirm loop), the `Origin` lifecycle (`inherited`/`ai_drafted` at partial confidence → `po_authored`/`decided` on confirmation), why questions are a fallback not the primary mode (cite `personas/02-po.md:324, 327`), and how the drafter's proposals flow through the single writer (doc-updater). State explicitly: questions fire only when the engine cannot draft a section confidently or the PO asks to deepen it.

- [ ] **Step 3: Write `inheritance.md`** — carry-forward from the intake-record

Content: the intake-record is indexed as a source but treated specially; the inheritor preserves the intake's `Source` and confidence (never inflates), maps intake sections → RP sections (problem→context-problem, reach/personas→personas, scope→scope, metrics→metrics), and carries open dispositions forward into "Prontidão herdada". Cite `personas/02-po.md:245` (`inherited` = partial confidence, traceable).

- [ ] **Step 4: Write `escalation.md`** — triggers + the freeze divergence

Content: the architectural trigger list (`personas/02-po.md:299`), the `tech-assessment-ref` data shape (`:152-156`), the freeze gate condition (`:161-163`), and the documented temporary divergence (spec §8): when escalation is required but the tech-assessment skill doesn't exist, the RP freezes **provisionally** with `tech-assessment-ref` disposition `deferred`; migration note: tighten to `signed` when the TA skill lands.

- [ ] **Step 5: Verify the cross-references resolve**

Run: `grep -rl "intake-brainstorm/references" plugins/hsb-teamwork/skills/readiness-package/references/`
Expected: at least `orchestration.md` listed.

Run: `ls plugins/hsb-teamwork/skills/intake-brainstorm/references/contract-and-template.md`
Expected: file exists (the cited target is real).

- [ ] **Step 6: Commit**

```bash
git add plugins/hsb-teamwork/skills/readiness-package/references/
git commit -m "Add RP reference docs (orchestration, drafting, inheritance, escalation)"
```

---

## Task 7: SKILL.md + README.md

**Files:**
- Create: `plugins/hsb-teamwork/skills/readiness-package/SKILL.md`
- Create: `plugins/hsb-teamwork/skills/readiness-package/README.md`

- [ ] **Step 1: Write SKILL.md frontmatter verbatim**

```markdown
---
name: readiness-package
description: >-
  Orchestrate a multi-agent pipeline that turns a Product Ready intake-record into
  a frozen Readiness Package (RP) — the Product Owner's rationalization artefact:
  executive summary, problem/context, objectives, personas, scope in/out, business
  rules, user stories with Given/When/Then acceptance criteria, NFRs, edge cases,
  metrics, release criteria, and risks. Use this skill WHENEVER someone wants to
  rationalize, specify, "write the RP for", or turn a triaged demand / intake record
  into a product-ready definition. It reuses the intake-brainstorm engine and authors
  draft-then-confirm: the pipeline pre-fills every section (inherited from the intake
  record or AI-drafted) at partial confidence, and the PO reviews, edits, justifies,
  and freezes. It detects whether the demand needs a CTO Technical Assessment and
  records that as a tracked, deferred reference. Template-driven and portable; works
  in pt-BR by default and mirrors the requested language.
user-invocable: true
---
```

- [ ] **Step 2: Write the SKILL.md body**

Mirror `intake-brainstorm/SKILL.md`'s sections, RP-adapted:
```markdown
# Readiness Package (orchestrator)

## First, read these (once per run)
[List the RP references (references/orchestration.md, drafting.md, inheritance.md,
 escalation.md) AND the cited intake shared method by relative path. Name the default
 template assets/target-template.readiness-package.md + its .guide.md + golden-example.md.]

## The principle that makes parallelism safe
[Single-writer rule, RMW, sentinel — cite ../intake-brainstorm/references/writing-integrity.md.]

## The agents you spawn (subagent_type)
[The 15 reused intake-* agents + readiness-inheritor, readiness-drafter,
 readiness-escalation-flagger. Note: doc-updater and ledger-writer are the only writers.]

## Authoring model — draft-then-confirm
[Draft pass then confirm loop; Origin lifecycle; questions are a fallback. See drafting.md.]

## Modes
[Fresh (intake-record -> RP), Revisit (re-score an existing RP), Batch/headless.]

## Language
[Default pt-BR; mirror requested language.]

## The flow (summary — full detail in references/orchestration.md)
[Phases 0-4 one-liners.]

## The Technical Assessment boundary
[TA is out of scope; escalation is detected and recorded as a deferred reference;
 the RP freezes provisionally. See escalation.md + spec §8.]

## Installing in other projects
[Same portability note as intake: paths passed in, session resolved via $INTAKE_HOME
 -> git root -> cwd; the linked intake-record path is provided at run start.]

## Bundled resources
[Table of assets/ + references/.]
```

- [ ] **Step 3: Write README.md**

A short readme mirroring `intake-brainstorm/README.md`: what the skill does, how to invoke (`/hsb-teamwork:readiness-package`), the inputs (a Product Ready intake-record), the outputs (`readiness-document.md` + humanized/translated/enriched/manifest in `<demand-slug>-readiness/`), and the TA boundary.

- [ ] **Step 4: Verify**

Run: `sed -n '1,2p' plugins/hsb-teamwork/skills/readiness-package/SKILL.md`
Expected: `---` then `name: readiness-package`.

Run: `grep -c "readiness-inheritor\|readiness-drafter\|readiness-escalation-flagger" plugins/hsb-teamwork/skills/readiness-package/SKILL.md`
Expected: `≥ 3` (all three agents referenced).

- [ ] **Step 5: Commit**

```bash
git add plugins/hsb-teamwork/skills/readiness-package/SKILL.md plugins/hsb-teamwork/skills/readiness-package/README.md
git commit -m "Add readiness-package SKILL.md orchestrator and README"
```

---

## Task 8: Codex mirror

**Files:**
- Create: `plugins/hsb-teamwork/codex/agents/hsb-readiness-inheritor.toml`
- Create: `plugins/hsb-teamwork/codex/agents/hsb-readiness-drafter.toml`
- Create: `plugins/hsb-teamwork/codex/agents/hsb-readiness-escalation-flagger.toml`
- Create: `plugins/hsb-teamwork/codex/prompts/hsb-teamwork-readiness-package.md`
- Modify: `plugins/hsb-teamwork/codex/AGENTS.md`
- Modify: `plugins/hsb-teamwork/codex/README.md`

- [ ] **Step 1: Write the three `.toml` wrappers (thin, point at shared `.md`)**

`hsb-readiness-drafter.toml` (the others follow the same shape, swapping name/description/role-path):
```toml
name = "hsb-readiness-drafter"
description = "Propose first-draft content for the new RP product sections (business rules, user stories + acceptance criteria, NFRs, edge cases) at partial confidence with Origin=ai_drafted, for the PO to confirm."
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
You are the Drafter in the hsb-teamwork readiness-package pipeline (Codex adapter).

Propose first-draft content for the new RP product sections (business rules, user stories with Given/When/Then acceptance criteria, NFRs per ISO/IEC 25010, edge cases) at partial confidence with Origin=ai_drafted, for the PO to confirm.

Read your full role specification at `agents/readiness-drafter.md` and the shared method under `skills/readiness-package/references/` and `skills/intake-brainstorm/references/` (start with skills/readiness-package/references/orchestration.md) in the package, and follow them exactly. Obey writing-integrity.md: never truncate, use read-modify-write, key edits by stable id, and end every produced document with the `<!-- END OF DOCUMENT -->` sentinel, verified. The orchestrator provides SESSION_DIR and any paths you need. Return your result to the orchestrator.
"""
```
For `hsb-readiness-inheritor.toml`: description "Carry the linked intake-record's graded sections forward into the RP, preserving confidence/source and tagging Origin=inherited."; role path `agents/readiness-inheritor.md`.
For `hsb-readiness-escalation-flagger.toml`: description "Decide whether the demand owes a CTO Technical Assessment and record the tech-assessment-ref disposition (deferred when out of scope)."; role path `agents/readiness-escalation-flagger.md`.

- [ ] **Step 2: Write the Codex prompt `hsb-teamwork-readiness-package.md`**

Mirror `codex/prompts/hsb-teamwork-intake-brainstorm.md`, pointing at the RP skill:
```markdown
# /hsb-teamwork-readiness-package — orchestrator (Codex)

Act as the **hsb-teamwork readiness-package orchestrator**. Read `codex/AGENTS.md`
in the package (the readiness-package section) and follow it for this run. You are
the only layer that talks to the user.

1. Identify the demand and the linked Product Ready intake-record. Pick the mode
   (fresh / revisit / batch) and the output language (default pt-BR).
2. Resolve-or-resume the `<demand-slug>-readiness/` session (see the package's
   `skills/intake-brainstorm/references/sessions.md`).
3. Run the phases — setup, draft pass, confirm loop, production, wrap — performing
   each specialist role yourself, or by delegating to the Codex subagents in
   `codex/agents/` (run sequentially; Codex is single-agent).

Non-negotiables (full detail under `skills/readiness-package/references/` and the
cited `skills/intake-brainstorm/references/`):
- the RP template is the contract; fill every blocksFreeze section to its threshold
  or an honest disposition; tag each entry's Origin (inherited/ai_drafted/po_authored);
- draft-then-confirm: pre-fill, then the PO judges — questions are a fallback;
- one writer per file; read-modify-write; never truncate — end with the
  `<!-- END OF DOCUMENT -->` sentinel and verify it;
- detect CTO escalation; when a TA is owed, record tech-assessment-ref as deferred
  (the RP freezes provisionally) — do not block indefinitely.

The user's request follows:

$ARGUMENTS
```

- [ ] **Step 3: Update `codex/AGENTS.md`**

Add a top note that the adapter now covers two skills, and a "## readiness-package" section pointing RP runs at `../skills/readiness-package/SKILL.md` + its references, restating the sequential execution order for the RP phases (setup → draft pass → confirm loop → production → wrap). Keep the existing intake-brainstorm content intact.

- [ ] **Step 4: Update `codex/README.md`**

Add the three `hsb-readiness-*.toml` wrappers and the `hsb-teamwork-readiness-package` prompt to the file table; note they read their role specs from `../agents/readiness-*.md` and the shared `skills/readiness-package/references/`.

- [ ] **Step 5: Verify TOML name keys**

Run: `grep -h '^name = ' plugins/hsb-teamwork/codex/agents/hsb-readiness-*.toml`
Expected: three lines — `hsb-readiness-inheritor`, `hsb-readiness-drafter`, `hsb-readiness-escalation-flagger`.

- [ ] **Step 6: Commit**

```bash
git add plugins/hsb-teamwork/codex/
git commit -m "Add Codex mirror for readiness-package (wrappers, prompt, AGENTS/README updates)"
```

---

## Task 9: Manifest + README updates

**Files:**
- Modify: `plugins/hsb-teamwork/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `plugins/hsb-teamwork/README.md`

- [ ] **Step 1: Update `plugin.json`**

Bump `"version"` to `"0.2.0"`. Replace the `"description"` value's Available/Planned clause with:
```
Available: intake-brainstorm (raw demand -> a fully-filled, confidence-graded document via a multi-agent pipeline, plus humanized/translated/enriched variants); readiness-package (a Product Ready intake-record -> a frozen Readiness Package via draft-then-confirm, with CTO-escalation detection). Planned: tech-assessment, prd-generation.
```
Add `"readiness"` and `"product-owner"` to `"keywords"`.

- [ ] **Step 2: Update `marketplace.json`**

Bump the plugin entry `"version"` to `"0.2.0"`. Update its `"description"` line to:
```
HSB Teamwork — a demand-to-delivery toolkit for Claude Code and Codex. Skills: intake-brainstorm, readiness-package (available); tech-assessment, prd-generation (planned).
```

- [ ] **Step 3: Update the plugin README**

Add a one-line entry for `/hsb-teamwork:readiness-package` next to the intake-brainstorm entry, describing input (Product Ready intake-record) → output (frozen RP).

- [ ] **Step 4: Verify JSON validity**

Run: `python3 -c "import json; json.load(open('plugins/hsb-teamwork/.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('valid')"`
Expected: `valid`

- [ ] **Step 5: Commit**

```bash
git add plugins/hsb-teamwork/.claude-plugin/plugin.json .claude-plugin/marketplace.json plugins/hsb-teamwork/README.md
git commit -m "Register readiness-package skill in plugin and marketplace manifests"
```

---

## Task 10: Eval suite (manifest, rubric, runner, fixtures)

**Files:**
- Create: `evals/readiness-package/evals.json`
- Create: `evals/readiness-package/rubric.md`
- Create: `evals/readiness-package/run.sh`
- Create: `evals/readiness-package/.gitignore`
- Create: `evals/readiness-package/fixtures/sources/01-intake-record-queue-voting.md`
- Modify: `evals/README.md`

- [ ] **Step 1: Create the inherited-input fixture**

Copy the intake golden (the queue-voting demand's filled intake record) as the RP's inherited input, so the pipeline ties together:

Run: `mkdir -p evals/readiness-package/fixtures/sources && cp evals/intake-brainstorm/golden/queue-voting.target-document.md evals/readiness-package/fixtures/sources/01-intake-record-queue-voting.md`
Expected: file created.

- [ ] **Step 2: Write `evals.json`**

```json
{
  "skill": "hsb-teamwork:readiness-package",
  "notes": "Repo-level evals (dev/CI only; not shipped in the plugin). Each case runs the skill headlessly (no live PO: gaps become honest dispositions, ai_drafted sections stay partial) and is graded by assertions.py (structural) + rubric.md (qualitative, vs the golden).",
  "evals": [
    {
      "id": 0,
      "name": "intake-to-rp-queue-voting",
      "prompt": "Run the hsb-teamwork readiness-package skill in non-interactive mode. Linked intake-record (Product Ready): evals/readiness-package/fixtures/sources/01-intake-record-queue-voting.md. Inherit the capture sections from it (Origin=inherited, preserve source/confidence); draft the new product sections (business-rules, user-stories with Given/When/Then, NFRs, edge-cases) at partial confidence with Origin=ai_drafted; detect CTO escalation and record tech-assessment-ref honestly. For any genuine gap, use an honest disposition rather than asking. Write the filled RP to {OUT}/readiness-document.md (keep the section annotations and the END OF DOCUMENT sentinel). Do not ask questions.",
      "files": ["evals/readiness-package/fixtures/sources/01-intake-record-queue-voting.md"],
      "golden": "golden/queue-voting.readiness-document.md",
      "expected_output": "A filled RP: all blocking sections resolved at/above threshold or honestly disposed, every content section tagged with a valid Origin, tech-assessment-ref resolved (deferred when escalation is required), sentinel present."
    },
    {
      "id": 1,
      "name": "revisit-underfilled-rp",
      "prompt": "Run the hsb-teamwork readiness-package skill in REVISIT mode on the existing RP at {OUT}/seed.md (copied in by the runner). Re-score each section, fill or honestly dispose the weak/empty ones non-interactively, promote confirmed ai_drafted entries toward po_authored where the seed shows confirmation, bump the revision, and write the result to {OUT}/readiness-document.md.",
      "files": [],
      "seed": "fixtures/underfilled-rp-seed.md",
      "golden": null,
      "expected_output": "Previously empty blocking sections become resolved or honestly disposed; Origin tags present; revision bumped; sentinel present."
    }
  ]
}
```

- [ ] **Step 3: Create the revisit seed fixture**

Create `evals/readiness-package/fixtures/underfilled-rp-seed.md` — a partial RP with the correct annotations but several blocking sections left as `[fill]` or empty confidence lines, mirroring `evals/intake-brainstorm/fixtures/underfilled-seed.md`. (Add `fixtures/underfilled-rp-seed.md` to the files committed in this task.)

- [ ] **Step 4: Write `rubric.md`**

Adapt `evals/intake-brainstorm/rubric.md`. Layer 1 (automated) lists the RP grader checks: `sentinel_present`, `no_truncation_markers`, `has_annotations`, `blocking[<id>]_satisfied`, `confidence_lines_present`, `origin_present_valid`, `tech_assessment_ref_resolved`. Layer 2 (qualitative, 1-5) dimensions: problem-not-solution; confidence + Origin honesty (inherited preserves intake's number, ai_drafted stays partial until confirmed); dispositions used well; testable Given/When/Then acceptance criteria; NFRs that don't claim feasibility; escalation called correctly; fidelity to golden.

- [ ] **Step 5: Write `run.sh`**

Adapt `evals/intake-brainstorm/run.sh` with these exact changes: header says `readiness-package`; the self-test grades `golden/queue-voting.readiness-document.md`; the `grade()` target and the produced-file check use `readiness-document.md` (not `target-document.md`); keep the `</dev/null` stdin-drain fix and the baseline-vs-with_skill loop. Make it executable.

Run: `chmod +x evals/readiness-package/run.sh`

- [ ] **Step 6: Write `.gitignore`**

```
runs/
```

- [ ] **Step 7: Update `evals/README.md`**

Add a `readiness-package/` subtree alongside `intake-brainstorm/` in the directory diagram, and a one-line note that it grades `intake-record -> RP` (structural via `assertions.py`, qualitative via `rubric.md`).

- [ ] **Step 8: Run the grader self-test through run.sh**

Run: `cd evals/readiness-package && ./run.sh && cd ../..`
Expected: the scorecard's self-test row shows the golden as `PASS readiness=100% blocking=12/12`; live cases are skipped if the `claude` CLI is absent (that's fine here).

- [ ] **Step 9: Commit**

```bash
git add evals/readiness-package/ evals/README.md
git commit -m "Add readiness-package eval suite (manifest, rubric, runner, fixtures)"
```

---

## Task 11: End-to-end live verification (optional, requires claude CLI) + final check

**Files:** none (verification only)

- [ ] **Step 1: Confirm the plugin loads the new skill**

Run: `claude --help >/dev/null 2>&1 && echo "cli present" || echo "no cli — skip live run"`
If no CLI: skip to Step 4.

- [ ] **Step 2: Run the live eval case 0 with the skill**

Run: `cd evals/readiness-package && ./run.sh && cd ../..`
Expected: scorecard now has an `intake-to-rp-queue-voting | with_skill` row. Inspect `evals/readiness-package/runs/iteration-1/eval-0/with_skill/readiness-document.md`.

- [ ] **Step 3: Grade the live output structurally**

Run: `python3 evals/readiness-package/assertions.py evals/readiness-package/runs/iteration-1/eval-0/with_skill/readiness-document.md`
Expected: `"pass": true`. If false, read the failing checks and fix the SKILL.md/agent prompts (not the grader), then re-run.

- [ ] **Step 4: Final repo-wide sanity checks**

Run: `python3 evals/readiness-package/assertions.py evals/readiness-package/golden/queue-voting.readiness-document.md | python3 -c "import json,sys; print('golden pass:', json.load(sys.stdin)['pass'])"`
Expected: `golden pass: True`

Run: `python3 -c "import json; json.load(open('plugins/hsb-teamwork/.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('manifests valid')"`
Expected: `manifests valid`

Run: `ls plugins/hsb-teamwork/skills/readiness-package/SKILL.md plugins/hsb-teamwork/agents/readiness-*.md plugins/hsb-teamwork/codex/agents/hsb-readiness-*.toml`
Expected: all listed (skill, 3 agents, 3 codex wrappers).

- [ ] **Step 5: Final commit (if Step 3 required prompt fixes)**

```bash
git add -A
git commit -m "Tune readiness-package prompts to pass live structural eval"
```

---

## Notes for the implementer

- **Do not modify the engine agents** (`agents/intake-*.md`) or `evals/intake-brainstorm/`. The RP skill reuses them as-is; if something seems to need a change there, it's a signal the RP template/guide should carry the difference instead.
- **The annotation marker stays `intake:`** in the RP template — it's the engine's contract grammar, not the document type. Changing it would break `template-analyst`, `doc-updater`, and the grader.
- **`readiness-document.md`** is the RP's filled target document (the analog of intake's `target-document.md`); keep that filename consistent across the SKILL.md, evals, and grader.
- **Freeze divergence is intentional** (spec §8): a provisionally-frozen RP with a deferred TA is the correct output until the tech-assessment skill exists. The grader's `tech_assessment_ref_resolved` accepts `deferred`.
```
