# Phase 1 — Golden vertical slice

**local hello → tool call → 10-Q eval → GREEN pack**

This is the smallest path that still feels like a real AI lab.

## Quick run

From repo root:

```bash
bash scripts/verify_slice.sh
```

Or step by step:

```bash
cd phase1-golden-slice
python3 lab/01_local_hello.py
python3 lab/02_tool_call.py
python3 lab/03_run_eval.py
python3 lab/04_rtma_quiz.py
python3 lab/05_run_eval_expanded.py
```

## Layout

| Path | Role |
|------|------|
| `lab/01_local_hello.py` | Local brain ping + latency + RTMA |
| `lab/02_tool_call.py` | Schema tools + trace chain |
| `lab/03_run_eval.py` | Golden-10 scoring + report |
| `lab/04_rtma_quiz.py` | RTMA cold self-check |
| `lab/05_run_eval_expanded.py` | Golden-25 deeper bar |
| `lab/local_brain.py` | Ollama client + honest mock |
| `lab/rtma.py` | Evidence writer |
| `tools/lab_tools.py` | `calc` + `glossary_lookup` |
| `evals/golden10.json` | Fixed questions (core) |
| `evals/golden25_domain.json` | Expanded general-audience suite |
| `artifacts/` | Per-run RTMA JSON |
| `reports/` | Human-readable eval report |
| `GREEN-CHECKLIST.md` | Mentor completion bar |

## Ollama (optional for Phase 1)

```bash
# install from https://ollama.com then:
ollama pull llama3.2:3b
export OLLAMA_MODEL=llama3.2:3b
python3 lab/01_local_hello.py
```

If Ollama is down, labs **still pass** with a mock brain.  
That is intentional teaching: RTMA does not require cloud keys.

## Pass bar

| Check | Target |
|-------|--------|
| Lab 01 | Non-empty answer + artifact |
| Lab 02 | Both calc + glossary succeed |
| Lab 03 | ≥ 80% of 10 questions |

## RTMA reminder

| | |
|--|--|
| **R**un | command you typed |
| **T**race | events / tool chain |
| **M**etric | ms, pass_rate, counts |
| **A**rtifact | files under `artifacts/` + `reports/` |
