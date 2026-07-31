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
