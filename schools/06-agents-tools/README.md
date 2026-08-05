# School 06 — Agents & tools

**Job:** Tool schema, handoffs, memory, permissions.

## Beginner model
An agent is a **loop with privileges**, not a personality.

## Mechanism (Lab 02 already ships this)
1. Goal in  
2. Plan tool calls (schema)  
3. Permission check  
4. Execute  
5. Synthesize from tool results when facts matter  
6. RTMA artifact out  

## Tools in this pack
- `calc` — exact arithmetic  
- `glossary_lookup` — fixed local definitions  

## Never-without-approval
Email/post · delete outside sandbox · spend money · message customers · force-push main.

## Lab GREEN
- [ ] Lab 02 passes  
- [ ] Explain tool chain from an artifact JSON  
- [ ] Name three side effects that need humans  

## Failure modes
Invented tool results · missing schemas · multi-agent without owner · permission bypass via prompt.

## RTMA
**Run** goal · **Trace** each tool request/result · **Metric** success count/latency · **Artifact** chain JSON.

## Interview 30 / 90
**30s:** Privileged loops; schema tools; default-deny side effects.  
**90s:** Exact facts via tools; shared trace ids; critic agents cannot self-escalate permissions.

## Bounded loop implementation

```text
observe → validate schema/permission/budget → act
  → correct on real error → verify artifact → stop or repeat
```

Persist goal, state, iteration/max, allowlist, approval id, trace, completion
assertions, and stop reason. The corrector may revise arguments; it cannot invent
a result. A critic may reject but cannot grant permission. Compare plain loops,
state-graph frameworks, provider SDKs, and multi-agent patterns on checkpointing,
interrupts, replay, portability, and testability—not popularity.

Run `lab/07_agent_loop.py`; GREEN requires a visible failure, correction, assertion,
and hard stop within budget.

## 2026 agent-observability practice

- Give the run, state transition, model span, retrieval span, and tool span correlated ids.
- Record proposed action, schema result, permission decision, approval, execution, and assertion.
- Separate planner errors, tool errors, environment errors, and verification errors in metrics.
- Test cancellation, checkpoint resume, duplicate delivery, timeout, and exhausted-budget paths.
- Treat MCP/tool metadata as untrusted until host policy authorizes the capability.
- A completion claim is GREEN only when the external artifact exists and can be replayed.
