# School 02 — Local lab

**Job:** Run models privately on Mac Mini / laptop / Linux — catalog, hygiene, honesty.

## Beginner model
Local lab = classroom brain. Cloud = optional trunk to a bigger carrier.

## Mechanism
| Layer | Common choice |
|-------|----------------|
| Runner | Ollama (friendly) |
| API | localhost **11434** |
| Alt | llama.cpp / MLX |
| Storage | weights on disk — never git |

### Install path (optional)
1. Install Ollama  
2. `ollama pull llama3.2:3b`  
3. `curl http://127.0.0.1:11434/api/tags`  
4. Re-run Lab 01 — backend should become `ollama`

### Mock is valid practice
Flight simulator. Disclose it. Do not claim production from mock-only.

## Lab GREEN
- [ ] Know default host/port  
- [ ] Lab 01 with mock or ollama — say which  
- [ ] One reason local>cloud and cloud>local  
- [ ] Confirm no weight files in free pack  

## RTMA
**Run** pull/hello · **Trace** probe_ollama · **Metric** alive + latency · **Artifact** JSON.

## Interview 30 / 90
**30s:** Local models for privacy/practice; measure latency; weights stay out of git.  
**90s:** Ollama path on 11434; mock fallback so learning never blocks; catalog policy for daily vs heavy models.

## Local → frontier decision lab

Run the same 10 tasks against deterministic mock, one local model, and—only when
you choose to configure it—one cloud adapter. Keep the prompt and grader fixed.

| Capture | Why |
|---|---|
| task pass rate | capability on your work |
| warm/cold p50 and p95 | experience and capacity |
| tokens or local runtime | comparable workload |
| cost per passed task | useful economics |
| data boundary | privacy decision |

Route locally when it meets the bar; burst to frontier capability only for the
measured gap. Keep local fallback and never commit weights or populated env files.

## 2026 local-runtime practice

- Pin model artifact, quantization, tokenizer, context setting, and runtime version in Trace.
- Measure warm-up separately from steady-state tokens/second and end-to-end p95.
- Watch memory pressure, thermal behavior, power, and concurrent-request degradation.
- Test structured output and tool-call reliability; chat quality alone is insufficient.
- Keep private fixtures local and document every later cloud boundary explicitly.
- Promote a local route only when task pass rate meets the same golden threshold as cloud.
