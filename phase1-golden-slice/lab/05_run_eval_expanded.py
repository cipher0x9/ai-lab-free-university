#!/usr/bin/env python3
"""Lab 05 — Optional expanded golden-25 eval (general audience deeper bar)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rtma import RTMA, print_rtma_banner, write_report  # noqa: E402

EVALS = Path(__file__).resolve().parents[1] / "evals" / "golden25_domain.json"

CANNED = {
    "D01": "RTMA is Run Trace Metric Artifact",
    "D02": "It maps to UC LICC",
    "D03": "A token is a chunk of text",
    "D04": "A hallucination is a fluent answer without evidence",
    "D05": "Tool calls use a schema and return exact results",
    "D06": "Ollama default port is 11434",
    "D07": "Non-goal: 760MB single HTML",
    "D08": "Never commit API keys",
    "D09": "Repo name ai-lab-free-university",
    "D10": "Path: hello tool eval green",
    "D11": "Context window is a token budget",
    "D12": "Never auto-send email without approval",
    "D13": "RAG retrieves relevant documents first",
    "D14": "RAG answers need citations",
    "D15": "Lower temperature is more deterministic",
    "D16": "Prompt injection tries to override instructions",
    "D17": "Local models help privacy",
    "D18": "License is MIT",
    "D19": "Backend mock means no real model server",
    "D20": "Threshold is 80 percent",
    "D21": "Budgets include STT and TTS",
    "D22": "Default HTML budget upper is 20 MB",
    "D23": "An agent is a loop with privileges",
    "D24": "Ask what observation would kill the claim",
    "D25": "Sibling is UC Lab Free University",
}


def score(answer: str, required: list[str]) -> tuple[bool, list[str]]:
    low = answer.lower()
    missing = [k for k in required if k.lower() not in low]
    return (not missing, missing)


def main() -> int:
    print_rtma_banner("Lab 05 · Expanded golden-25 eval")
    rtma = RTMA("05_run_eval_expanded")
    suite = json.loads(EVALS.read_text(encoding="utf-8"))
    items = suite["items"]
    threshold = float(suite.get("pass_threshold", 0.8))
    rows = []
    passed = 0
    for item in items:
        ans = CANNED.get(item["id"], "")
        ok, missing = score(ans, item["required_keywords"])
        if ok:
            passed += 1
        rows.append({"id": item["id"], "pass": ok, "missing": missing, "answer": ans})
        print(f"  [{'PASS' if ok else 'FAIL'}] {item['id']}: {item['question'][:56]}")
        rtma.add_trace("item", id=item["id"], pass_=ok, missing=missing)

    total = len(items)
    rate = passed / total if total else 0.0
    rtma.set_metric("passed", passed)
    rtma.set_metric("total", total)
    rtma.set_metric("pass_rate", round(rate, 4))
    rtma.set_metric("threshold", threshold)
    suite_pass = rate >= threshold

    report = [
        "# Golden-25 expanded report",
        "",
        f"- Passed: **{passed}/{total}** ({rate:.0%})",
        f"- Threshold: {threshold:.0%}",
        f"- Result: **{'GREEN' if suite_pass else 'RED'}**",
        "",
    ]
    for r in rows:
        report.append(f"- {r['id']}: {'PASS' if r['pass'] else 'FAIL ' + str(r['missing'])}")
    path = write_report("golden25-report.md", "\n".join(report))
    rtma.artifacts.append(str(path))
    print(f"\nScore: {passed}/{total} = {rate:.0%}")
    print(f"Report: {path}")
    payload = rtma.finish(status="ok" if suite_pass else "fail")
    print(f"Artifact: {payload['artifact'][-1]}")
    return 0 if suite_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
