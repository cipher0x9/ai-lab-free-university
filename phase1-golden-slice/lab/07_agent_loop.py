#!/usr/bin/env python3
"""Lab 07 — observe → act → correct → verify, with a hard stop.

The loop is deterministic and local. A deliberately invalid first action shows
that correction is a state transition, not a motivational word. The iteration
budget and approval boundary are data, so they can be tested.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from lab_tools import run_tool  # noqa: E402
from rtma import RTMA, print_rtma_banner  # noqa: E402

MAX_ITERATIONS = 4


def run_bounded_loop() -> tuple[bool, list[dict]]:
    trace: list[dict] = []
    state = "observe"
    expression = "2 plus 2"  # intentionally invalid for the first attempt
    for iteration in range(1, MAX_ITERATIONS + 1):
        trace.append({"iteration": iteration, "state": state, "observation": f"Need exact result for {expression!r}"})
        if state in {"observe", "correct"}:
            state = "act"
        result = run_tool("calc", {"expression": expression})
        trace.append({"iteration": iteration, "state": state, "tool": "calc", "result": result})
        if not result.get("ok"):
            state = "correct"
            expression = "2+2"
            continue
        state = "verify"
        verified = result.get("result") == 4.0
        trace.append({"iteration": iteration, "state": state, "assertion": "result == 4", "verified": verified})
        return verified, trace
    return False, trace


def main() -> int:
    print_rtma_banner("Lab 07 · Bounded agent loop")
    rtma = RTMA("07_agent_loop")
    ok, trace = run_bounded_loop()
    for event in trace:
        rtma.add_trace("agent_transition", **event)
    iterations = max((e["iteration"] for e in trace), default=0)
    corrections = sum(e.get("state") == "correct" for e in trace)
    rtma.set_metric("iteration_budget", MAX_ITERATIONS)
    rtma.set_metric("iterations_used", iterations)
    rtma.set_metric("corrections", corrections)
    rtma.set_metric("verified", ok)
    rtma.note("External writes, messages, purchases, and destructive tools remain unavailable in this lab.")
    payload = rtma.finish("ok" if ok and iterations <= MAX_ITERATIONS else "fail")
    print(f"Verified: {ok} · iterations: {iterations}/{MAX_ITERATIONS} · corrections: {corrections}")
    print(f"Artifact: {payload['artifact'][-1]}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
