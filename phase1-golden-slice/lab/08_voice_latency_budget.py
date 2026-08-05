#!/usr/bin/env python3
"""Lab 08 — STT → LLM/tools → TTS latency budget from local fixtures."""

from __future__ import annotations

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rtma import RTMA, print_rtma_banner, write_report  # noqa: E402

SAMPLES_MS = {
    "capture_endpoint": [95, 110, 120, 130, 145],
    "stt": [170, 185, 210, 240, 280],
    "llm_and_tools": [310, 350, 410, 470, 560],
    "tts_first_audio": [125, 140, 160, 190, 230],
    "transport_buffer": [35, 40, 45, 55, 70],
}
STAGE_BUDGET_MS = {"capture_endpoint": 160, "stt": 300, "llm_and_tools": 600, "tts_first_audio": 250, "transport_buffer": 80}
TURN_BUDGET_MS = 1400


def percentile95(values: list[int]) -> float:
    return statistics.quantiles(values, n=20, method="inclusive")[18]


def main() -> int:
    print_rtma_banner("Lab 08 · Voice latency budget")
    rtma = RTMA("08_voice_latency_budget")
    rows = []
    for stage, values in SAMPLES_MS.items():
        p50 = statistics.median(values)
        p95 = percentile95(values)
        budget = STAGE_BUDGET_MS[stage]
        rows.append((stage, p50, p95, budget, p95 <= budget))
        rtma.add_trace("stage_samples", stage=stage, samples_ms=values)
        rtma.set_metric(f"{stage}_p50_ms", p50)
        rtma.set_metric(f"{stage}_p95_ms", p95)
    turn_p95 = sum(row[2] for row in rows)
    green = all(row[4] for row in rows) and turn_p95 <= TURN_BUDGET_MS
    rtma.set_metric("turn_p95_budget_sum_ms", round(turn_p95, 2))
    rtma.set_metric("turn_budget_ms", TURN_BUDGET_MS)
    rtma.set_metric("green", green)

    report = ["# Voice latency budget", "", "| Stage | p50 ms | p95 ms | Budget ms | Gate |", "|---|---:|---:|---:|---|"]
    for stage, p50, p95, budget, ok in rows:
        report.append(f"| {stage} | {p50:.0f} | {p95:.0f} | {budget} | {'GREEN' if ok else 'RED'} |")
    report.extend(
        [
            "",
            f"Budgeted-turn p95 sum: **{turn_p95:.0f} ms / {TURN_BUDGET_MS} ms**.",
            "Fault isolation: capture, speech recognition, model/tools, synthesis, and transport are separate legs.",
            "Falsifier: one fast demo does not prove the p95 budget; replace fixtures with measured timestamps before a production claim.",
        ]
    )
    path = write_report("voice-latency-budget.md", "\n".join(report))
    rtma.artifacts.append(str(path))
    payload = rtma.finish("ok" if green else "fail")
    print(f"Budgeted p95 sum: {turn_p95:.0f}/{TURN_BUDGET_MS} ms · GREEN={green}")
    print(f"Artifact: {payload['artifact'][-1]}")
    return 0 if green else 1


if __name__ == "__main__":
    raise SystemExit(main())
