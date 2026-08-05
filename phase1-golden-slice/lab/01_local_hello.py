#!/usr/bin/env python3
"""Lab 01 — Local model hello (Mac Mini ready).

Path: Run a local brain, measure latency, write RTMA artifact.

Mentor analogy (UC):
  This is like dialing your own lab phone and confirming media path.
  If the phone stack is not up, you still document what failed and why.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from local_brain import DEFAULT_HOST, DEFAULT_MODEL, generate, list_models, ollama_alive
from rtma import RTMA, print_rtma_banner


def main() -> int:
    print_rtma_banner("Lab 01 · Local model hello")
    rtma = RTMA("01_local_hello")

    alive = ollama_alive()
    models = list_models() if alive else []
    rtma.add_trace("probe_ollama", host=DEFAULT_HOST, alive=alive, models=models)
    rtma.set_metric("ollama_alive", alive)
    rtma.set_metric("model_count", len(models))
    rtma.set_metric("preferred_model", DEFAULT_MODEL)

    if alive:
        print(f"✓ Ollama reachable at {DEFAULT_HOST}")
        if models:
            print(f"  Models: {', '.join(models[:8])}{'…' if len(models) > 8 else ''}")
        else:
            print("  No models listed yet — pull one later, e.g. `ollama pull llama3.2:3b`")
            rtma.note("Ollama up but empty model list")
    else:
        print(f"○ Ollama not reachable at {DEFAULT_HOST}")
        print("  Using honest MOCK local brain so you still practice RTMA.")
        print("  Install later: https://ollama.com  then `ollama pull llama3.2:3b`")
        rtma.note("mock_brain_used")

    prompt = (
        "In one short paragraph: what is RTMA (Run, Trace, Metric, Artifact) "
        "and how is it like UC LICC (Leg, ID, Counter, Capture)?"
    )
    rtma.add_trace("prompt", text=prompt)

    reply = generate(prompt, system="You are a calm AI lab mentor. Be precise. No hype.")
    rtma.add_trace(
        "generate",
        backend=reply.backend,
        model=reply.model,
        latency_ms=reply.latency_ms,
        error=reply.error,
    )
    rtma.set_metric("backend", reply.backend)
    rtma.set_metric("latency_ms", reply.latency_ms)
    rtma.set_metric("answer_chars", len(reply.text or ""))
    rtma.set_decision(
        baseline="deterministic mock is the always-available classroom baseline",
        changed_variable="use local Ollama when reachable",
        observed_delta={"backend": reply.backend, "latency_ms": reply.latency_ms},
        keep_or_revert="keep the observed backend only for claims its eval suite supports",
        rollback_trigger="empty answer, failed health probe, or unacceptable latency",
    )

    print()
    print(f"Backend : {reply.backend}  ({reply.model})")
    print(f"Latency : {reply.latency_ms} ms")
    print("-" * 64)
    print(reply.text or "(empty answer)")
    print("-" * 64)

    ok = bool(reply.text and len(reply.text.strip()) > 20)
    if not ok:
        rtma.note("empty_or_short_answer")
    payload = rtma.finish(status="ok" if ok else "fail")
    print()
    print(f"Artifact: {payload['artifact'][-1]}")
    print("GREEN if: you can restate RTMA in your own words + open the JSON artifact.")
    print("REVIEW: teach it again at 1h, 24h, 7d, 30d, and 90d.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
