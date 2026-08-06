# Local LLM Ops (Ollama, llama.cpp & friends)

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT · RTMA**  
**Privacy-first architecture for learners and labs**

---

## 1) Why local

| Benefit | Reality check |
|---------|----------------|
| Privacy | Still secure the host |
| Cost predictability | Electricity + hardware |
| Offline demos | Model quality tradeoffs |
| Learning | Weights become tangible |

Frontier APIs remain useful. Local is a **first-class peer**, not a toy.

---

## 2) Runtime map

| Runtime | Strength |
|---------|----------|
| Ollama | Ergonomic local serve |
| llama.cpp | Portable GGUF inference |
| MLX (Apple) | Mac-native speed |
| vLLM | Throughput serving (GPU servers) |

Pick by hardware you actually own.

---

## 3) Model selection habits

1. Start tiny for plumbing tests  
2. Climb size only when evals demand  
3. Pin versions (model digest / tag)  
4. Record quant (Q4/Q5/Q8) in RTMA artifacts  

---

## 4) Ops checklist

- [ ] Health endpoint  
- [ ] Timeout defaults  
- [ ] Concurrent request limits  
- [ ] Disk for models  
- [ ] No secrets in prompts written to disk casually  
- [ ] Eval suite on upgrade  

---

## 5) Local → cloud adapter pattern

```text
interface Complete(prompt, tools) → text
   ├─ LocalBackend
   └─ CloudBackend
```

Same evals hit both. Models are replaceable; **contracts are not**.

---

## 6) Lab

Use `phase1-golden-slice` zero-key fixtures first. Attach Ollama only when ready. Keep traces.

**Educational only · MIT**
