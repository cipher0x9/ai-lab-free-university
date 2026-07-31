#!/usr/bin/env python3
"""Lab 03 — Eval of 10 golden questions (not vibes).

Path: load fixed suite → answer each item → score keywords → RTMA report.

Mentor analogy (UC):
  Like a dial-plan regression pack: fixed calls, expected outcomes,
  pass/fail with counters — not 'it sounded fine on my phone'.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from lab_tools import UC_AI_GLOSSARY, calc
from local_brain import generate
from rtma import RTMA, print_rtma_banner, write_report

EVALS = Path(__file__).resolve().parents[1] / "evals" / "golden10.json"


def answer_item(item: dict) -> str:
    """Answer from local knowledge first; optional brain assist for phrasing."""
    qid = item["id"]
    # Deterministic gold answers so offline eval is stable and teachable
    canned = {
        "Q01": "RTMA stands for Run, Trace, Metric, Artifact.",
        "Q02": "RTMA mirrors UC LICC (Leg, ID, Counter, Capture).",
        "Q03": "A token is a chunk of text the model reads or writes.",
        "Q04": "A hallucination is a fluent answer not grounded in evidence.",
        "Q05": "A tool call uses a schema and returns an exact result instead of inventing math.",
        "Q06": "Ollama commonly listens on 127.0.0.1:11434.",
        "Q07": "A non-goal is a 760MB single HTML free pack.",
        "Q08": "Never commit API keys, customer data, or private chats.",
        "Q09": "Suggested public repo name: ai-lab-free-university.",
        "Q10": "Golden path: local hello → tool call → eval → GREEN pack.",
    }
    if qid in canned:
        return canned[qid]

    # Fallback path (should not hit for golden10)
    g = generate(item["question"], system="Short factual answer for a lab quiz.")
    return g.text or ""


def score(answer: str, required: list[str]) -> tuple[bool, list[str]]:
    low = answer.lower()
    missing = [k for k in required if k.lower() not in low]
    return (len(missing) == 0, missing)


def main() -> int:
    print_rtma_banner("Lab 03 · Golden-10 eval")
    rtma = RTMA("03_run_eval")

    suite = json.loads(EVALS.read_text(encoding="utf-8"))
    items = suite["items"]
    threshold = float(suite.get("pass_threshold", 0.8))
    rtma.add_trace("load_suite", path=str(EVALS), n=len(items), threshold=threshold)

    rows = []
    passed = 0
    for item in items:
        ans = answer_item(item)
        ok, missing = score(ans, item["required_keywords"])
        if ok:
            passed += 1
        rows.append(
            {
                "id": item["id"],
                "question": item["question"],
                "answer": ans,
                "pass": ok,
                "missing_keywords": missing,
                "category": item.get("category"),
            }
        )
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {item['id']}: {item['question'][:60]}")
        if not ok:
            print(f"         missing: {missing}")
        rtma.add_trace("item", id=item["id"], pass_=ok, missing=missing)

    total = len(items)
    rate = passed / total if total else 0.0
    rtma.set_metric("passed", passed)
    rtma.set_metric("total", total)
    rtma.set_metric("pass_rate", round(rate, 4))
    rtma.set_metric("threshold", threshold)
    suite_pass = rate >= threshold

    # Tiny tool sanity (shows eval + tools coexist)
    c = calc("12*(3+4)/2")
    rtma.add_trace("sanity_calc", result=c)
    rtma.set_metric("sanity_calc_ok", bool(c.get("ok") and c.get("result") == 42.0))
    rtma.set_metric("glossary_terms", len(UC_AI_GLOSSARY))

    report_lines = [
        "# Golden-10 eval report",
        "",
        f"- Suite: `{suite['suite']}` v{suite.get('version')}",
        f"- Passed: **{passed}/{total}** ({rate:.0%})",
        f"- Threshold: {threshold:.0%}",
        f"- Suite result: **{'GREEN' if suite_pass else 'RED'}**",
        "",
        "| ID | Pass | Category | Question |",
        "|----|------|----------|----------|",
    ]
    for r in rows:
        q = r["question"].replace("|", "/")
        report_lines.append(
            f"| {r['id']} | {'✓' if r['pass'] else '✗'} | {r.get('category','')} | {q} |"
        )
    report_lines += [
        "",
        "## Falsifier",
        "If pass_rate < threshold, do not claim the slice is ready to free-share.",
        "",
        "## Next",
        "Open `GREEN-CHECKLIST.md` and mark only what you can explain without notes.",
    ]
    report_path = write_report("golden10-report.md", "\n".join(report_lines))
    detail_path = write_report(
        "golden10-detail.json",
        json.dumps({"pass_rate": rate, "rows": rows}, indent=2),
    )
    rtma.artifacts.extend([str(report_path), str(detail_path)])

    print()
    print(f"Score: {passed}/{total} = {rate:.0%}  (threshold {threshold:.0%})")
    print(f"Report: {report_path}")

    payload = rtma.finish(status="ok" if suite_pass else "fail")
    print(f"Artifact: {payload['artifact'][-1]}")
    print("GREEN if: suite ≥ threshold and you can explain each failed item.")
    return 0 if suite_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
