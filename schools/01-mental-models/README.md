# School 01 — Mental models

**Job:** Tokens, context, probability, failure modes — without math fear.

## Beginner model
| Familiar system idea | AI cousin |
|----------------------|-----------|
| Bandwidth budget | Token / context budget |
| “Up” light but no media | Fluent wrong answer (hallucination) |
| Incident grammar | RTMA |
| Regression pack | Eval suite |

## Mechanism
1. **Tokens** — text chunks models read/write  
2. **Context window** — budget per request  
3. **Next-token prediction** — fluency ≠ truth  
4. **Temperature** — lower for scored work  
5. **Failure catalog** — hallucination, overflow, injection, silent drop  

## Lab GREEN
- [ ] Explain token + context with a budget analogy  
- [ ] Define hallucination in one sentence  
- [ ] Lab 01: name backend mock vs ollama  
- [ ] Golden Q01–Q04 without notes  

## RTMA
**Run** `lab/01_local_hello.py` · **Trace** generate event · **Metric** latency_ms · **Artifact** JSON.

## Interview 30 / 90
**30s:** Models predict tokens; fluency isn’t truth; I use RTMA and evals.  
**90s:** Context is a budget. Low temperature for scored work. Tools and citations fight hallucinations. Artifacts make incidents reviewable.

## Stack map and debugging test

Trace one answer through seven layers: data → representation/tokens → model →
context → tools/retrieval → product policy → human decision. For each layer,
name the object, property, relation, event, and evidence. This prevents “the model
is wrong” from hiding a bad source, truncated context, tool error, or UI claim.

Debugging rule: a reason without an observable consequence is only a hypothesis.
Force one context-overflow or unsupported-claim fixture and capture where the chain breaks.

## 2026 mental-model practice

- Separate capability, reliability, calibration, and product policy; one score cannot represent all four.
- Compare probability-shaped fluency with evidence-grounded correctness on the same fixture.
- Trace context assembly so missing, stale, injected, and truncated evidence become distinct failures.
- Measure structured-output validity separately from semantic task success.
- Treat tool and retrieval results as data with provenance, not automatically trusted truth.
- Update the model only after the trace identifies which layer actually failed.
