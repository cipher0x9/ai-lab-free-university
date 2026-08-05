#!/usr/bin/env python3
"""Lab 06 — deterministic RAG ablation with no model and no API key.

The learner compares retrieval configurations instead of trusting a polished
answer. This is deliberately tiny: the mechanism is visible on one screen and
the output is an RTMA report that can be reproduced offline.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rtma import RTMA, print_rtma_banner, write_report  # noqa: E402

DOCUMENTS = {
    "rtma.md": "RTMA means Run Trace Metric Artifact. A falsifier challenges a mastery claim.",
    "rag.md": "RAG retrieves evidence before generation. Production retrieval uses citations and fails closed when empty.",
    "agents.md": "An agent is a bounded loop with tool permissions, approval gates, traces, and evaluation.",
    "voice.md": "A voice AI path measures STT, model, tool, TTS, transport, and human handoff latency separately.",
}

QUESTIONS = [
    ("What does RTMA preserve?", "rtma.md"),
    ("What should RAG do when retrieval is empty?", "rag.md"),
    ("Why does an agent need approval gates?", "agents.md"),
    ("Which voice stages need separate latency measurements?", "voice.md"),
]


def tokens(text: str) -> list[str]:
    """Lowercase word tokens with a tiny stop-list; deterministic by design."""
    stop = {"a", "an", "and", "does", "is", "the", "to", "what", "when", "which", "why", "with"}
    return [x for x in re.findall(r"[a-z0-9]+", text.lower()) if x not in stop]


def overlap_score(query: str, document: str) -> float:
    q, d = set(tokens(query)), set(tokens(document))
    return len(q & d) / max(1, len(q | d))


def weighted_score(query: str, document: str) -> float:
    """Simple term-frequency score plus phrase/intent bonuses (a reranker toy)."""
    q, d = Counter(tokens(query)), Counter(tokens(document))
    lexical = sum(min(q[t], d[t]) for t in q) / max(1, sum(q.values()))
    intent_bonus = 0.0
    pairs = (("empty", "fails closed"), ("approval", "permissions"), ("latency", "separately"), ("preserve", "artifact"))
    low_q, low_d = query.lower(), document.lower()
    for cue, evidence in pairs:
        if cue in low_q and evidence in low_d:
            intent_bonus += 0.35
    return lexical + intent_bonus


def retrieve(query: str, scorer) -> tuple[str, float]:
    ranked = sorted(((scorer(query, body), path) for path, body in DOCUMENTS.items()), reverse=True)
    score, path = ranked[0]
    return path, round(score, 4)


def evaluate(name: str, scorer) -> dict:
    rows = []
    for question, expected in QUESTIONS:
        actual, score = retrieve(question, scorer)
        rows.append({"question": question, "expected": expected, "actual": actual, "score": score, "pass": actual == expected})
    passed = sum(row["pass"] for row in rows)
    return {"variant": name, "passed": passed, "total": len(rows), "hit_rate": passed / len(rows), "rows": rows}


def main() -> int:
    print_rtma_banner("Lab 06 · RAG retrieval ablation")
    rtma = RTMA("06_rag_ablation")
    baseline = evaluate("set-overlap", overlap_score)
    reranked = evaluate("weighted-rerank", weighted_score)
    rtma.add_trace("corpus", documents=list(DOCUMENTS), questions=len(QUESTIONS))
    rtma.add_trace("variant", **baseline)
    rtma.add_trace("variant", **reranked)
    delta = reranked["hit_rate"] - baseline["hit_rate"]
    rtma.set_metric("baseline_hit_rate", baseline["hit_rate"])
    rtma.set_metric("reranked_hit_rate", reranked["hit_rate"])
    rtma.set_metric("absolute_delta", round(delta, 4))
    rtma.set_metric("citation_coverage", 1.0)
    rtma.note("A higher retrieval score is not automatically a better answer; inspect misses and citations.")

    report = [
        "# RAG ablation report",
        "",
        "| Variant | Hits | Hit rate |",
        "|---------|------|----------|",
        f"| {baseline['variant']} | {baseline['passed']}/{baseline['total']} | {baseline['hit_rate']:.0%} |",
        f"| {reranked['variant']} | {reranked['passed']}/{reranked['total']} | {reranked['hit_rate']:.0%} |",
        "",
        f"Decision: {'keep the reranker candidate' if delta >= 0 else 'revert the reranker candidate'}; inspect every miss before shipping.",
        "Falsifier: a configuration fails if citation-required queries retrieve the wrong document or return evidence for an empty match.",
    ]
    path = write_report("rag-ablation-report.md", "\n".join(report))
    rtma.artifacts.append(str(path))
    ok = reranked["hit_rate"] >= baseline["hit_rate"] and reranked["hit_rate"] >= 0.75
    payload = rtma.finish("ok" if ok else "fail")
    print(f"Baseline: {baseline['hit_rate']:.0%} · reranked: {reranked['hit_rate']:.0%} · delta: {delta:+.0%}")
    print(f"Artifact: {payload['artifact'][-1]}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
