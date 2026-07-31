#!/usr/bin/env python3
"""Lab 02 — Tool call with schema + permission discipline.

Path: model (or router) requests a tool → tool runs → result returns → RTMA.

Mentor analogy (UC):
  Like a CTI connector — the app does not invent the agent state;
  it calls an API with a contract and logs the transaction ID.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from lab_tools import TOOL_SPECS, run_tool
from local_brain import generate
from rtma import RTMA, print_rtma_banner


def plan_tool_calls(user_goal: str) -> list[dict]:
    """Prefer structured routing. Try model JSON; fall back to deterministic planner."""
    schema_hint = json.dumps(
        [{"name": s["name"], "description": s["description"]} for s in TOOL_SPECS],
        indent=2,
    )
    prompt = f"""You route tools for a safe lab agent.
Available tools:
{schema_hint}

User goal: {user_goal}

Reply with ONLY a JSON array of tool calls, e.g.
[{{"name":"calc","arguments":{{"expression":"2+2"}}}}]
If no tool needed, return [].
"""
    reply = generate(prompt, system="Output JSON only. No markdown.")
    text = (reply.text or "").strip()
    # extract JSON array if model wrapped it
    match = re.search(r"\[[\s\S]*\]", text)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list) and data:
                return data, reply
        except json.JSONDecodeError:
            pass
    # Deterministic planner (always works offline / mock)
    calls: list[dict] = []
    goal = user_goal.lower()
    if any(x in goal for x in ["+", "-", "*", "/", "calculate", "math", "compute"]):
        # pull first arithmetic-looking snippet
        m = re.search(r"([0-9+\-*/().% ]{3,80})", user_goal)
        expr = (m.group(1) if m else "12*(3+4)/2").strip()
        calls.append({"name": "calc", "arguments": {"expression": expr}})
    if any(x in goal for x in ["rtma", "token", "hallucin", "sip", "ollama", "rag", "licc", "tool call", "glossary"]):
        # pick first known-ish word
        for term in ["RTMA", "token", "hallucination", "SIP", "ollama", "RAG", "LICC", "tool call"]:
            if term.lower() in goal:
                calls.append({"name": "glossary_lookup", "arguments": {"term": term}})
                break
        else:
            calls.append({"name": "glossary_lookup", "arguments": {"term": "RTMA"}})
    if not calls:
        calls = [
            {"name": "calc", "arguments": {"expression": "12*(3+4)/2"}},
            {"name": "glossary_lookup", "arguments": {"term": "RTMA"}},
        ]
    return calls, reply


def main() -> int:
    print_rtma_banner("Lab 02 · Tool call (schema + trace)")
    rtma = RTMA("02_tool_call")

    user_goal = (
        "Calculate 12*(3+4)/2 exactly, and look up the glossary definition of RTMA."
    )
    print(f"Goal: {user_goal}")
    rtma.add_trace("user_goal", text=user_goal)
    rtma.add_trace("tool_specs", count=len(TOOL_SPECS), names=[s["name"] for s in TOOL_SPECS])

    calls, plan_reply = plan_tool_calls(user_goal)
    rtma.add_trace(
        "plan",
        backend=plan_reply.backend,
        model=plan_reply.model,
        latency_ms=plan_reply.latency_ms,
        calls=calls,
    )
    rtma.set_metric("plan_backend", plan_reply.backend)
    rtma.set_metric("tool_call_count", len(calls))

    results = []
    for i, call in enumerate(calls, 1):
        name = call.get("name", "")
        args = call.get("arguments") or {}
        print(f"\n→ Tool [{i}] {name}({json.dumps(args)})")
        rtma.add_trace("tool_request", index=i, name=name, arguments=args)
        result = run_tool(name, args)
        results.append({"name": name, "arguments": args, "result": result})
        rtma.add_trace("tool_result", index=i, name=name, result=result)
        print(f"  Result: {json.dumps(result, ensure_ascii=False)}")

    # Final synthesis (uses tool results; no invention for math)
    synthesis_bits = []
    for r in results:
        if r["name"] == "calc" and r["result"].get("ok"):
            synthesis_bits.append(
                f"Calculator says {r['arguments'].get('expression')} = {r['result'].get('result')}"
            )
        if r["name"] == "glossary_lookup" and r["result"].get("ok"):
            synthesis_bits.append(
                f"Glossary[{r['result'].get('term')}]: {r['result'].get('definition')}"
            )
    final = " | ".join(synthesis_bits) if synthesis_bits else "No successful tool results."
    print()
    print("Synthesis (grounded in tools only):")
    print(final)
    rtma.add_trace("synthesis", text=final)
    rtma.set_metric("successful_tools", sum(1 for r in results if r["result"].get("ok")))

    ok = (
        any(r["name"] == "calc" and r["result"].get("ok") for r in results)
        and any(r["name"] == "glossary_lookup" and r["result"].get("ok") for r in results)
    )
    payload = rtma.finish(status="ok" if ok else "fail")
    print()
    print(f"Artifact: {payload['artifact'][-1]}")
    print("GREEN if: you can explain why tools beat invented numbers, and open the trace.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
