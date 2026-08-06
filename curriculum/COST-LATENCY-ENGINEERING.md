# Cost & Latency Engineering for AI Systems

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT · RTMA**

---

## 1) Why this pack exists

Beautiful demos die in production on **p95 latency** and **invoice shock**. Engineers who measure both ship.

---

## 2) Latency budget (voice-aware)

Example interactive budget (tune to product):

| Stage | p50 target | p95 target |
|-------|------------|------------|
| STT partial | 200 ms | 400 ms |
| LLM first token | 300 ms | 700 ms |
| Tools | 100 ms | 500 ms |
| TTS first audio | 200 ms | 400 ms |
| Transport | 50 ms | 150 ms |

See lab: `phase1-golden-slice/lab/08_voice_latency_budget.py`.

---

## 3) Cost model (simple and honest)

```text
cost ≈ input_tokens * cin + output_tokens * cout
      + tool_calls * ctool
      + embedding_calls * cemb
      + infra / hour
```

Track **cost per successful task**, not cost per curiosity.

---

## 4) Levers

| Lever | Latency | Cost | Quality risk |
|-------|---------|------|--------------|
| Smaller / local model | ↓ | ↓ | maybe ↓ |
| Cache prompts / RAG | ↓ | ↓ | stale risk |
| Speculative decoding | ↓ | varies | — |
| Shorter outputs | ↓ | ↓ | incomplete |
| Parallel tools | ↓ | ↑ concurrency | races |
| Batch offline | n/a | ↓ | not interactive |

---

## 5) SLOs that matter

- Task success rate  
- p50/p95 latency  
- $/successful task  
- Human escalation rate  
- Safety incident rate  

If you optimize only tokens, you will sacrifice truth.

---

## 6) RTMA artifact

Always store: model id, token counts, stage timings, cache hit, tool errors.

---

## 7) Drill

Take one agent path and produce a spreadsheet of stage timings. Cut one stage by 20% without dropping eval score.

**Educational only · MIT**
