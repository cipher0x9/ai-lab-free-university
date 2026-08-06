# MCP & Tool Protocols (2026)

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT · RTMA proof**  
**Audience:** builders wiring agents to real tools without losing the plot

---

## 1) Why tools are the product

A model that only chats is a demo. A model that **calls typed tools** under policy is a system.

| Idea | Meaning |
|------|---------|
| Tool | Named capability with schema + side-effect class |
| Protocol | How host and model exchange tool offers/results |
| MCP | Model Context Protocol — standardized tool/context servers |
| Host | Runtime that approves, logs, and bounds calls |
| Policy | What may run without a human |

---

## 2) MCP mental model

```text
Host (agent runtime)
  ├─ Model (local or frontier)
  ├─ MCP server: filesystem (read-only lab)
  ├─ MCP server: browser (optional)
  └─ MCP server: your API (typed)
```

Each server exposes **tools** with JSON schemas. The host decides exposure. The model proposes calls. The host executes and returns **results + traces**.

---

## 3) RTMA for every tool call

| Letter | Tool-call proof |
|:--:|--|
| **R** | Did the call execute (or refuse) under policy? |
| **T** | Args, order, retries, which server |
| **M** | Latency, error rate, token cost of the step |
| **A** | Durable log JSON + redacted result snapshot |

If you cannot replay the tool story, you cannot debug the agent.

---

## 4) Side-effect classes (assign every tool)

| Class | Examples | Default policy |
|-------|----------|----------------|
| **Read** | search, get_issue | Auto OK in lab |
| **Write-local** | write file in sandbox | Path allowlist |
| **Write-remote** | post comment, email | Human approval |
| **Money/irreversible** | purchase, delete prod | Dual control |
| **Network egress** | arbitrary URL fetch | Domain allowlist |

Never ship "generic shell" to production agents without a cage.

---

## 5) Schema design that reduces hallucination

Good tool schema:

- Clear name (`get_weather` not `do_stuff`)
- Required fields only when needed
- Enums for closed sets
- Descriptions that state **units and limits**
- Error returns that are structured, not prose soup

```json
{
  "name": "get_weather",
  "description": "Current weather for a city. Temp in C.",
  "parameters": {
    "type": "object",
    "required": ["city"],
    "properties": {
      "city": {"type": "string", "minLength": 1, "maxLength": 80}
    }
  }
}
```

---

## 6) Host responsibilities (non-negotiable)

1. Validate args against schema **before** execute  
2. Enforce timeouts and max concurrency  
3. Cap tool loops (see agent architecture pack)  
4. Redact secrets in traces  
5. Emit RTMA artifacts  
6. Fail closed on unknown tools  

---

## 7) Failure modes

| Failure | Symptom | Fix habit |
|---------|---------|-----------|
| Schema drift | Model invents fields | Version tools |
| Over-broad tools | Data exfil risk | Split + allowlist |
| Silent tool error | Model fabricates | Return typed errors |
| Infinite tool thrash | Cost spike | Hard turn cap |
| Prompt injection via tool result | Hijack | Sanitize + trust labels |

---

## 8) Local lab path (zero-key first)

1. Define 2–3 pure functions as tools (`add`, `lookup_fixture`)  
2. Run `phase1-golden-slice` style loop  
3. Log each call as JSON artifact  
4. Only then attach network tools  

See repo labs: `phase1-golden-slice/lab/02_tool_call.py`, `07_agent_loop.py`.

---

## 9) Interop map (2026)

| Style | Notes |
|-------|-------|
| OpenAI-style tools | function calling JSON |
| Anthropic tools | similar schema discipline |
| MCP servers | reusable across hosts |
| LangGraph / custom | still need host policy |

Do not marry identity to one vendor. Marry identity to **contracts + evals**.

---

## 10) Security checklist

- [ ] No raw secrets in tool args or logs  
- [ ] Path allowlists for filesystem tools  
- [ ] Human gate for remote writes  
- [ ] Injection tests on tool-returned text  
- [ ] Rate limits  

---

## 11) Teach-back

Explain MCP in one minute to a UC engineer:

> "MCP is like a standard trunk interface for tools. The model proposes; the session border (host) enforces policy; RTMA is the CDR."

Spaced: 1h → 24h → 7d → 30d → 90d.

**Educational only · MIT · no warranty**
