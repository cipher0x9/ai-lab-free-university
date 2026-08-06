# Context Engineering

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT · RTMA**  
**Thesis:** In 2026, many "prompt problems" are actually **context budget** problems.

---

## 1) What is context engineering?

Designing **what enters the window**, in what order, with what freshness, under what token budget — so the model can do the job without drowning.

| Lever | Question |
|-------|----------|
| Selection | What is relevant? |
| Compression | What can be summarized? |
| Structure | How is it labeled? |
| Freshness | What is stale? |
| Authority | What is source-of-truth? |
| Privacy | What must never leave local? |

---

## 2) Context layers (stack)

```text
1. System / policy (stable)
2. Tool schemas (stable per version)
3. Task brief (per run)
4. Retrieved evidence (RAG)
5. Working memory / scratchpad
6. Conversation turns (ephemeral)
7. Tool results (volatile, large)
```

Budget like QoS: **policy and task first**, then evidence, then chat history.

---

## 3) Failure modes

| Failure | Symptom |
|---------|---------|
| Context stuffing | Model ignores middle |
| Stale RAG | Confident wrong answer |
| Tool result flood | Lost instruction |
| Conflicting authorities | Flip-flop answers |
| PII in window | Compliance risk |

---

## 4) Techniques that work

1. **Hard budgets** per layer (tokens)  
2. **Citations** for retrieved chunks  
3. **Summarize with loss notes** ("dropped fields: X")  
4. **Pinned facts** vs soft chat  
5. **Scratchpad outside final answer**  
6. **Re-retrieve** instead of infinite history  

---

## 5) RTMA template for a context build

```json
{
  "run_id": "...",
  "budget_tokens": 12000,
  "layers": {"policy": 800, "task": 400, "rag": 6000, "history": 2000, "tools": 2800},
  "dropped": ["old_turn_12", "chunk_9_low_score"],
  "metric": {"answer_faithfulness": 0.0, "latency_ms": 0}
}
```

---

## 6) UC bridge

Think of context like a **call admission budget**: if you admit too many low-priority streams, the emergency call (core instruction) gets jitter. QoS for tokens.

---

## 7) Practice drills

1. Same question with 2k vs 20k of noise — measure accuracy  
2. Summarize a 50-turn chat preserving decisions only  
3. Label each RAG chunk as {title, date, trust}  

**Educational only · MIT**
