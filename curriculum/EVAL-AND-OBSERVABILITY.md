# Eval and Observability
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** EVAL-401 · **Level:** Advanced production  
> **Outcome:** Build offline/online eval, LLM-as-judge with calibration, tracing, monitoring, canary/rollback — prove quality like reliability engineers.

---

## 0. Law of LLM Quality

> **If you cannot measure it offline, you cannot safely ship it online.**  
> **If you cannot trace it, you cannot fix it.**

```text
RTMA = Run · Trace · Metric · Artifact
Every meaningful experiment produces all four.
```

---

## 1. Eval Taxonomy

| Layer | Question | Examples |
|-------|----------|----------|
| Unit | component correct? | JSON schema, retrieval hit@k |
| Contract | interfaces hold? | tool schema, citation IDs |
| Task | user job done? | ticket resolved, code passes tests |
| Product | business KPI? | CSAT, conversion, time-to-resolve |
| Safety | policy held? | injection ASR, PII leak |
| Ops | reliable? | latency, error rate, cost |

Ship gates should bind **task + safety + ops**, not only vibes.

---

## 2. Golden Sets

### 2.1 Design

```jsonl
{"id":"g001","input":"...","expected":{"type":"regex","pattern":"..."},"tags":["billing","easy"],"split":"train_dev"}
{"id":"g002","input":"...","expected":{"type":"rubric","min_score":4},"tags":["hard"],"split":"holdout"}
```

### 2.2 Properties of a good golden set

| Property | Practice |
|----------|----------|
| Representative | mirrors production mix |
| Hard enough | includes edge cases |
| Labeled carefully | dual review on hard items |
| Versioned | `suite@semver` + changelog |
| Decontaminated | not in train/SFT if possible |
| Sized | 50 prototype / 200 serious / 1k+ mature |
| Sliced | language, length, intent, risk |

### 2.3 Expected checkers

```python
CHECKERS = {
  "exact": lambda out, exp: out.strip() == exp["value"],
  "contains": lambda out, exp: exp["value"] in out,
  "regex": lambda out, exp: bool(re.search(exp["pattern"], out)),
  "json_schema": lambda out, exp: validate_json(out, exp["schema"]),
  "numeric_tol": lambda out, exp: abs(float(out)-exp["value"]) <= exp["tol"],
  "test_cmd": lambda out, exp: run_tests(exp["cmd"]) == 0,
}
```

---

## 3. LLM-as-Judge

### 3.1 When useful

- Open-ended answers without unique gold string  
- Rubrics: helpfulness, tone, structure  
- Pairwise preference A vs B  

### 3.2 When dangerous

- Factual correctness without evidence  
- Same model family judging itself  
- Uncalibrated absolute scores  

### 3.3 Judge prompt skeleton

```text
You are a strict grader. Score 1-5 on:
- Correctness (use evidence only)
- Completeness
- Safety

Return JSON: {scores, pass, rationale}
Pass iff correctness>=4 and safety>=5.

[Task]
[Evidence if any]
[Candidate answer]
```

### 3.4 Bias controls

| Bias | Mitigation |
|------|------------|
| Position | randomize A/B order |
| Verbosity | instruct prefer concise correct |
| Self-preference | cross-family judge |
| Scale drift | anchor examples |
| Hallucinated rationale | require quote evidence |

### 3.5 Calibration with humans

```text
Sample 100 items → human labels → judge labels
Report agreement (Cohen's κ / accuracy)
Only promote judge if κ ≥ threshold (e.g. 0.6+)
Re-calibrate when product changes
```

---

## 4. Semantic Similarity Metrics

| Metric | Use | Caveat |
|--------|-----|--------|
| BLEU / ROUGE | overlap summaries | poor semantics |
| BERTScore | embedding similarity | can miss facts |
| Cosine on embeddings | paraphrase detect | not faithfulness |
| Exact + normalize | IDs, code | brittle to format |

**Never use cosine alone as faithfulness.** Pair with NLI or citation checks for RAG.

---

## 5. Adversarial Evals & Red Teams

### 5.1 Categories

1. Prompt injection (direct/indirect)  
2. Jailbreaks / policy bypass  
3. Data exfil (prompt, tools, memory)  
4. Abuse (scams, malware help) — refuse properly  
5. Privacy (PII reconstruction)  
6. Availability (cost bombs, loops)  
7. Integrity (poisoned RAG docs)  

### 5.2 Metrics

\[
\mathrm{ASR} = \frac{\#\text{ successful attacks}}{\#\text{ attempts}}
\]

Track ASR by category; gate releases on max ASR.

### 5.3 Continuous red team

```text
weekly: expand attack suite from prod incidents
ci: run fast subset on every prompt change
release: full suite + human spot checks
```

---

## 6. Hallucination Detection

### 6.1 Types

| Type | Signal |
|------|--------|
| Factual error | contradicts KB/world |
| Fabricated cite | bad IDs |
| Overconfidence | wrong + high certainty |
| Entity error | wrong person/date |
| Code hallucination | APIs that don't exist |

### 6.2 Detectors (ensemble)

- Retrieval faithfulness NLI  
- Closed-world citation check  
- Tool re-query verification  
- Self-consistency vote  
- External knowledge tool  
- Human review for high risk  

```python
def grounded_or_abstain(answer, evidence, nli):
    claims = split_claims(answer)
    for c in claims:
        if nli.entails(evidence, c) != "entail":
            return "ABSTAIN_OR_FIX"
    return "OK"
```

---

## 7. Offline Eval Harness (reference)

```python
def run_suite(suite, system, judge=None):
    rows = []
    for case in suite:
        t0 = time.time()
        out, trace = system.run(case["input"])  # returns RTMA trace
        latency = time.time() - t0
        hard = score_hard(out, case.get("expected"))
        soft = judge.score(case, out) if judge else None
        rows.append({
            "id": case["id"],
            "hard_pass": hard,
            "soft": soft,
            "latency": latency,
            "trace_path": trace.path,
            "tags": case.get("tags", []),
        })
    return summarize(rows)
```

### 7.1 Summaries that matter

- Overall pass rate  
- Pass by tag/slice  
- p50/p95 latency  
- Cost per case  
- Regression vs baseline suite version  
- Flaky rate across seeds  

---

## 8. Tracing with OpenTelemetry Concepts

Even offline-first, learn the model:

```text
Trace (request/run)
 └─ Span: retrieve
 └─ Span: rerank
 └─ Span: llm.generate  (attrs: model, tokens, temp)
 └─ Span: tool.search   (attrs: args hash, ok)
 └─ Span: verify
```

### 8.1 Attributes to log (AI-specific)

| Attr | Why |
|------|-----|
| `gen_ai.system` | provider |
| `gen_ai.request.model` | model id |
| `gen_ai.usage.input_tokens` | cost |
| `gen_ai.usage.output_tokens` | cost |
| `prompt_id` / `prompt_version` | regression |
| `session_id` / `user_tier` | slice |
| `tool.name` | reliability |
| `rag.top_scores` | retrieval health |
| `safety.flags` | policy |

### 8.2 Privacy in traces

- Redact secrets, tokens, raw PII  
- Hash user ids  
- Sample bodies; keep metadata always  
- Retention policies  

---

## 9. Online Monitoring

### 9.1 Golden signals for LLM apps

| Signal | Alert idea |
|--------|------------|
| Request rate | spike/drop |
| Error rate | 5xx, tool fail |
| Latency TTFT/TPOT | p95 SLO |
| Token cost | budget burn |
| Thumbs down / CSAT | quality |
| Refusal rate | policy or over-refuse |
| Empty retrieval rate | index health |
| Schema invalid rate | prompt/model break |
| Jailbreak hits | security |
| Drift score | embed distribution |

### 9.2 Feedback loops

```text
user feedback → label queue → golden set growth → re-eval → prompt/model change
```

### 9.3 Shadow & canary

```text
baseline 95% traffic
canary 5% new prompt/model
compare: task proxy metrics + safety + latency + cost
promote if non-inferior on gates; else rollback
```

---

## 10. Canary / Rollback Playbook

### 10.1 Immutable artifacts

```text
artifact = {
  model_id,
  prompt_bundle_hash,
  tool_registry_hash,
  index_version,
  eval_report_id
}
```

### 10.2 Steps

1. Pre-prod offline suite green  
2. Canary 1–5%  
3. Watch burn-in window (N minutes / N requests)  
4. Auto-rollback triggers: error↑, latency↑, safety flags↑, cost↑  
5. Postmortem with traces  

```yaml
rollback_if:
  error_rate_5m: "> 2x baseline"
  p95_latency: "> slo"
  safety_flag_rate: "> 0.1%"
  cost_per_req: "> 1.5x baseline"
```

---

## 11. Human Calibration Programs

| Activity | Cadence |
|----------|---------|
| Dual-label hard set | weekly |
| Judge agreement audit | per release |
| Side-by-side preference | biweekly |
| Incident labeling | continuous |
| Rubric revision | when product shifts |

**Inter-annotator agreement** is part of the metric system, not optional bureaucracy.

---

## 12. Experiment Tracking

Minimum fields:

```text
run_id, timestamp, git_sha, prompt_version, model, params,
suite_version, metrics{}, artifact_paths[], notes, author
```

Compare runs with **paired** tests on same suite IDs.

---

## 13. RTMA Deep Dive (campus standard)

### 13.1 Run

Executable command or job that anyone can re-invoke.

```bash
python evals/run_suite.py --suite golden_v3.jsonl --system canary --out artifacts/run_042/
```

### 13.2 Trace

Step-level log: inputs digests, tool I/O previews, model messages metadata, timings.

### 13.3 Metric

Numeric, comparable, sliced. Prefer **task success** over “sounds good.”

### 13.4 Artifact

Durable files: reports, plots data, failing cases, model cards.

```text
artifacts/run_042/
  summary.json
  failures.jsonl
  traces/
  COMPARE.md  # vs baseline
```

### 13.5 Definition of done for a change

- [ ] RTMA folder exists  
- [ ] Metrics vs baseline recorded  
- [ ] Failures triaged (not ignored)  
- [ ] Safety suite run  
- [ ] Owner sign-off  

---

## 14. Lab Suite

### Lab E1 — Golden harness

- **Run:** 30-case suite with ≥3 checker types  
- **Trace:** per-case traces  
- **Metric:** pass rate + p95 latency  
- **Artifact:** `e1_summary.json`

### Lab E2 — Judge calibration

- **Run:** 50 items human vs judge  
- **Metric:** κ / accuracy  
- **Artifact:** `e2_calibration.md`

### Lab E3 — Adversarial ASR

- **Run:** 40 injection prompts  
- **Metric:** ASR overall + by type  
- **Artifact:** `e3_redteam.json`

### Lab E4 — Trace tree

- **Run:** instrument RAG path with spans  
- **Metric:** % requests with full span set  
- **Artifact:** `e4_trace_example.json`

### Lab E5 — Canary simulation

- **Run:** two prompt versions offline “canary” bootstrap CI  
- **Metric:** detect 5% quality drop  
- **Artifact:** `e5_canary.md`

---

## 15. Dashboards (ASCII wireframe)

```text
┌──────── LLM Service Health ────────┐
│ QPS  err%  p95  $ / 1k req         │
│ schema_valid%  thumbs_down%        │
│ retrieve_empty%  safety_flags      │
├──────── Quality Canary ────────────┤
│ baseline vs canary task_success    │
│ slices: intent × locale            │
├──────── Top Failures ──────────────┤
│ links to traces + golden IDs       │
└────────────────────────────────────┘
```

---

## 16. Interview Answers (compressed)

**Q: How do you eval a chatbot?**  
A: Golden task success + safety ASR + latency/cost; LLM-judge calibrated to humans; online feedback; canary.

**Q: Faithfulness vs relevancy?**  
A: Faithfulness = supported by evidence; relevancy = addresses question; both needed for RAG.

**Q: Why traces?**  
A: Multi-step systems fail in tools/retrieval; metrics without traces are un-actionable.

---

## 17. Production Checklist

- [ ] Versioned golden suites  
- [ ] Hard checkers + soft judges  
- [ ] Human calibration plan  
- [ ] Safety/adversarial suite  
- [ ] RTMA on every release candidate  
- [ ] OTel-style traces with redaction  
- [ ] Online monitors + alerts  
- [ ] Canary + automatic rollback  
- [ ] Immutable artifact registry  
- [ ] Ownership & on-call runbooks  

---

## 18. CYPHER0X9 Proof Seal

```text
PACK: EVAL-AND-OBSERVABILITY
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
STANDARD: RTMA on every meaningful change
MODE: Offline-first · production-grade measurement
```

**Teach-back:** Build a golden item schema; calibrate a judge; define three rollback triggers; emit a full RTMA folder for a prompt change.

---

*End of pack · UC AI Free University · Measure twice, ship once.*
