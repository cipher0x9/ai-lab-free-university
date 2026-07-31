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
