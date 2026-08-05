# Agent Architecture
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** AGENT-401 · **Level:** Advanced systems  
> **Outcome:** Build bounded agent loops with tools, memory, reflection, multi-agent patterns, guardrails, and cost/latency budgets.

---

## 0. Definition

An **agent** is a loop that **observes state, selects actions (including tools), and updates state** toward a goal under constraints — not “an LLM that chats longer.”

```text
while not done and turns < MAX and cost < BUDGET:
    observe(state)
    plan or policy(state) → action
    if action is tool: result = exec(tool, args)  # scoped
    if action is respond: maybe final
    reflect / verify
    write memory
```

| LLM chat | Agent system |
|----------|--------------|
| one-shot or multi-turn talk | multi-step with side effects |
| no external world | tools + env |
| success = fluent text | success = verified world state |

---

## 1. The Agent Loop (canonical)

### 1.1 Observe → Orient → Decide → Act → Verify

```text
┌─────────────┐
│ Goal + Spec │
└──────┬──────┘
       ▼
┌─────────────┐   messages, files, tool results, memory
│  OBSERVE    │◄──────────────────────────────┐
└──────┬──────┘                               │
       ▼                                      │
┌─────────────┐                               │
│  PLAN/POLICY│  (LLM or hybrid planner)      │
└──────┬──────┘                               │
       ▼                                      │
┌─────────────┐     ┌──────────────┐          │
│  ACT        │────►│ Tool Runtime │──results─┤
└──────┬──────┘     └──────────────┘          │
       ▼                                      │
┌─────────────┐                               │
│  VERIFY     │  tests, schemas, humans       │
└──────┬──────┘                               │
       ▼                                      │
   done? ──no─────────────────────────────────┘
     yes → emit artifact + trace
```

### 1.2 Hard stops (non-negotiable)

| Stop | Why |
|------|-----|
| `max_turns` | infinite loops |
| `max_tool_calls` | thrashing |
| `max_wall_time` | hung tools |
| `max_tokens / $` | cost bombs |
| `forbidden_actions` | safety |
| `verify_fail_budget` | retry storms |

```python
@dataclass
class Budgets:
    max_turns: int = 8
    max_tool_calls: int = 12
    max_wall_s: float = 60.0
    max_usd: float = 0.25
```

---

## 2. Planning Styles

| Style | Description | Best for |
|-------|-------------|----------|
| ReAct | interleave thought + act | general tools |
| Plan-then-execute | outline first | multi-step workflows |
| Hierarchical | manager → workers | large tasks |
| State machine | fixed graph nodes | regulated flows |
| LLM + classical planner | LLM fills PDDL-like | robotics/ops |
| Tree search (ToT) | explore branches | hard puzzles |
| Reflexion | fail → critique → retry | coding agents |

### 2.1 When graphs beat free-form agents

- Compliance / finance / healthcare paths  
- Deterministic approvals  
- Same DAG every time with LLM only at nodes  

**Hybrid:** graph skeleton + agent nodes with local budgets.

```text
ingest → classify → (if refund) agent_refund else FAQ
                 → human_review if confidence < τ
                 → write_ticket
```

---

## 3. Tool Calling

### 3.1 Tool design principles

1. **Narrow** — one job, clear args  
2. **Typed** — JSON schema, enums  
3. **Idempotent** when possible  
4. **Authz outside the model** — IAM on runtime  
5. **Observable** — structured logs  
6. **Timeouts + retries** with backoff  
7. **Side-effect levels** — read / write / irreversible  

```json
{
  "name": "create_ticket",
  "side_effect": "write",
  "requires_approval": true,
  "timeout_s": 10,
  "parameters": {
    "type": "object",
    "required": ["title", "body", "priority"],
    "properties": {
      "title": {"type": "string", "maxLength": 120},
      "body": {"type": "string", "maxLength": 8000},
      "priority": {"type": "integer", "minimum": 1, "maximum": 5}
    }
  }
}
```

### 3.2 Tool runtime security

```text
Model proposes {name, args}
  → schema validate
  → policy engine (role, risk)
  → (optional) human approve
  → execute in sandbox / least privilege
  → return result as DATA (not instructions)
```

Never: raw shell with user text concatenated.  
Prefer: allowlisted commands, containers, fs jails, network egress policies.

### 3.3 Parallel tool calls

Independent reads can run concurrently; writes need ordering and locks.

---

## 4. Memory Architecture

### 4.1 Layers

| Layer | Lifetime | Examples | Risks |
|-------|----------|----------|-------|
| Working | turn | messages in context | overflow |
| Scratchpad | task | plans, todos | leakage to user |
| Episodic | session | prior tool results | stale |
| Semantic | long | user prefs, facts | wrong memory |
| Procedural | long | skills, prompts | version drift |
| Artifact store | durable | files, PRs, reports | ACL |

### 4.2 Write policies

- Write only **extracted facts**, not full transcripts  
- Tag confidence + source  
- TTL for prefs that expire  
- User-visible memory editor (GDPR-friendly)

```python
memory.write({
  "type": "preference",
  "key": "timezone",
  "value": "America/Los_Angeles",
  "source": "user_said",
  "confidence": 0.9,
  "ttl_days": 365
})
```

### 4.3 Retrieval into context

Summarize old turns; retrieve top semantic memories; always mark:

```text
<memory source="profile" confidence="0.9">timezone=PT</memory>
```

---

## 5. Reflection & Self-Correction

```text
act → observe error → critique → patch plan → retry (≤ R)
```

| Technique | Use |
|-----------|-----|
| Self-critique prompt | soft errors |
| Unit tests / linters | code agents |
| Schema validators | structured I/O |
| Execution feedback | REPL tools |
| Rubric judge | quality |

**Anti-pattern:** unlimited reflection without external signal → confident loops.

---

## 6. Multi-Agent Patterns

### 6.1 Patterns

| Pattern | Topology | Notes |
|---------|----------|-------|
| Supervisor | 1 manager routes | simple control |
| Peer debate | N agents argue | cost↑, sometimes quality↑ |
| Pipeline | A→B→C specialists | clear contracts |
| Blackboard | shared state store | needs locks |
| Swarm | many short agents | hard to debug |
| Society of mind | roles (critic, maker) | assign metrics |

### 6.2 Contracts between agents

```yaml
from: researcher
to: writer
message_schema:
  required: [sources, bullet_facts]
  sources:
    type: array
    items: {doc_id: string, quote: string}
```

### 6.3 Coordination failure modes

- Infinite handoffs  
- Contradictory goals  
- Shared memory races  
- Cost multiplication (N models × tools)  

**Mitigation:** single orchestrator owns budgets; workers are pure functions when possible.

---

## 7. Guardrails

### 7.1 Stack

```text
Input filters → Agent policy → Tool IAM → Output filters → Audit log
```

| Layer | Examples |
|-------|----------|
| Input | PII detect, jailbreak heuristics, size limits |
| Policy | allowed tools by role, rate limits |
| Tool | scoped tokens, path allowlists |
| Output | secret scan, toxicity, brand |
| Human | high-risk approval queue |

### 7.2 Risk tiers

| Tier | Examples | Gate |
|------|----------|------|
| 0 read | search, calc | auto |
| 1 write reversible | draft email | auto + log |
| 2 external | send email, PR | confirm |
| 3 irreversible | delete, pay | dual control |

---

## 8. Human-in-the-Loop (HITL)

```text
agent proposes action_card
  → UI shows args + risk + diffs
  → human: approve | edit | reject
  → continue with decision in trace
```

**Action card fields:** goal, rationale, tool, args, reversible?, blast radius, evidence.

Design for **async HITL** (queue) not only blocking chat.

---

## 9. Verification (agents that prove)

Agents should end with **checks**, not vibes.

| Domain | Verify how |
|--------|------------|
| Code | tests, types, lint |
| Data | schema, row counts |
| Ops | health checks, dry-run |
| Writing | rubric + citations |
| Math | symbolic / numeric re-eval |

```python
def verify_code_change(repo_path: str) -> tuple[bool, str]:
    r = run(["pytest", "-q"], cwd=repo_path, timeout=120)
    return r.returncode == 0, r.stdout + r.stderr
```

---

## 10. Cost & Latency Budgets

### 10.1 Accounting

```text
cost = sum( model_tokens * price + tool_fees + human_time_alloc )
latency = sum( model_ttft/tpot + tool_time + queue )
```

### 10.2 Control knobs

| Knob | Effect |
|------|--------|
| Smaller model for plan | cheap routing |
| Cache tool results | fewer calls |
| Cap k retrieval | less context |
| Early exit on verify | stop loops |
| Speculative parallel reads | latency↓ cost↑ maybe |
| Distill policies to code | replace LLM steps |

### 10.3 SLO example

```yaml
task: resolve_support_tier2
slo:
  success_rate: 0.85
  p95_latency_s: 45
  max_cost_usd: 0.40
  human_escalation_rate: 0.15
```

---

## 11. State, Traces, Replay

### 11.1 Trace schema (minimum)

```json
{
  "run_id": "uuid",
  "goal": "...",
  "turns": [
    {
      "i": 1,
      "messages_digest": "...",
      "model": "slm-8b@q4",
      "action": {"type": "tool", "name": "search", "args": {}},
      "observation": {"ok": true, "preview": "..."},
      "tokens_in": 1200,
      "tokens_out": 80,
      "latency_ms": 900
    }
  ],
  "result": {"status": "success", "artifact": "path"},
  "metrics": {"turns": 4, "cost_usd": 0.07}
}
```

**Replay:** deterministic seeds + recorded tool stubs for offline debug.

---

## 12. Reference Single-Agent Implementation

```python
def run_agent(goal, tools, llm, budgets, verify):
    state = {"goal": goal, "messages": [], "artifacts": []}
    tool_calls = 0
    t0 = time.time()
    for turn in range(budgets.max_turns):
        if time.time() - t0 > budgets.max_wall_s:
            return fail(state, "wall_time")
        decision = llm.next_action(state, tools)
        if decision.type == "final":
            ok, info = verify(decision.payload, state)
            if ok:
                return success(state, decision.payload)
            state["messages"].append({"role": "system", "content": f"Verify failed: {info}"})
            continue
        if decision.type == "tool":
            tool_calls += 1
            if tool_calls > budgets.max_tool_calls:
                return fail(state, "tool_budget")
            obs = tools.exec(decision.name, decision.args)
            state["messages"].append({"role": "tool", "content": obs})
            continue
        return fail(state, "unknown_action")
    return fail(state, "max_turns")
```

---

## 13. Multi-Agent Example: Research → Critique → Write

```text
Researcher (tools: search, open) → facts.json
Critic (no web) → gaps.json
Writer (facts only) → report.md
Verifier (citations closed-world) → pass/fail
```

Budgets owned by orchestrator; workers cannot raise their own spend.

---

## 14. Failure Modes Catalog

| Failure | Symptom | Fix |
|---------|---------|-----|
| Looping search | same query | detect duplicates |
| Tool hallucination | fake names | hard schema registry |
| Goal drift | off-task | restate goal each turn |
| Context bloat | slow/poor | summarize + retrieve |
| Premature final | incomplete | verify checklist |
| Over-ask human | friction | better auto tier0 |
| Under-ask human | incidents | risk tiers |
| Prompt injection via tool | policy break | data fences + IAM |

---

## 15. RTMA Labs

### Lab A1 — Bounded ReAct

- **Run:** calculator + search tools, max_turns=6  
- **Trace:** full turn log  
- **Metric:** success on 20 tasks; avg turns; $  
- **Artifact:** `a1_react_metrics.json`

### Lab A2 — Verify gate

- **Run:** code agent must pass pytest  
- **Metric:** false-success rate without tests vs with  
- **Artifact:** `a2_verify.md`

### Lab A3 — Memory write hygiene

- **Run:** extract prefs vs dump transcript  
- **Metric:** retrieval precision of later session  
- **Artifact:** `a3_memory.jsonl`

### Lab A4 — HITL mock

- **Run:** tier-2 actions require approval stub  
- **Metric:** blocked vs allowed correctness  
- **Artifact:** `a4_hitl_trace.json`

### Lab A5 — Multi-agent cost

- **Run:** 1 agent vs 3-agent pipeline same tasks  
- **Metric:** quality delta vs cost delta  
- **Artifact:** `a5_multiagent_roi.csv`

---

## 16. Design Interview: Agent Platform

1. Goal language + schemas  
2. Tool registry + IAM  
3. Orchestrator with budgets  
4. Memory stores  
5. Trace/replay  
6. Eval harness (task success)  
7. HITL console  
8. Canary + kill switch  

Scale: queue workers, per-tenant isolation, model router (SLM default, frontier escalate).

---

## 17. Production Checklist

- [ ] Explicit goal + acceptance tests  
- [ ] Hard budgets on turns/tools/time/$  
- [ ] Tool schemas + side-effect tiers  
- [ ] Policy engine outside model  
- [ ] Memory ACL + TTL  
- [ ] Verification before “success”  
- [ ] Full traces (RTMA)  
- [ ] Injection defenses on tool data  
- [ ] Human path for tier ≥2  
- [ ] Eval suite in CI  
- [ ] Kill switch / cancel run  
- [ ] Cost dashboards  

---

## 18. CYPHER0X9 Proof Seal

```text
PACK: AGENT-ARCHITECTURE
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
PROOF: RTMA labs A1–A5
AXIOM: An agent without budgets is a cost incident waiting to happen.
```

**Teach-back:** Define agent vs chat; list five hard stops; design tool IAM; explain verify-before-success; sketch multi-agent contracts.

---

*End of pack · UC AI Free University · The call must complete — and prove it did.*
