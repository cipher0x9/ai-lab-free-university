# MLOps and Production
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** MLOPS-401 · **Level:** Advanced engineering  
> **Outcome:** Design ML/LLM pipelines, registries, CI/CD, serving, A/B tests, drift monitors, and cost control for production systems.

---

## 0. MLOps = Software + Data + Models + Proof

```text
Code CI  +  Data CI  +  Model CI  +  Eval Gates  +  Serve  +  Observe  +  Rollback
```

LLM apps inherit classical MLOps and add: **prompt versions, traces, tool IAM, token economics**.

---

## 1. Pipeline Architecture

### 1.1 Classical ML pipeline

```text
ingest → validate → features → train → eval → register → deploy → monitor
```

### 1.2 LLM application pipeline

```text
doc ingest → chunk/embed/index
prompt/model change → offline eval → canary → serve
feedback → dataset growth → (optional) FT → register
```

### 1.3 Orchestration patterns

| Tool class | Role |
|------------|------|
| Workflow orchestrator | DAGs, retries, schedules |
| Feature compute | batch + streaming |
| Notebook → job | parameterized runs |
| Event triggers | git push, new data, drift alert |

Design pipelines **idempotent** and **restartable**.

---

## 2. Data & Feature Stores

### 2.1 Why feature stores

- Train/serve skew prevention  
- Reuse features across models  
- Point-in-time correctness  

### 2.2 Entities & keys

```text
entity: user_id
features: last_7d_spend, country, plan_tier
as_of: timestamp for training rows
```

### 2.3 LLM analogue

| ML feature store | LLM system |
|------------------|------------|
| feature vector | memory facts / profile |
| batch features | index builds |
| online store | low-latency RAG / prefs |
| skew | prompt template mismatch |

---

## 3. Model Registry

### 3.1 What to register

```json
{
  "name": "support-router",
  "version": "2.4.1",
  "artifact_uri": "models/support-router/2.4.1/",
  "framework": "gguf|lora|api",
  "metrics": {"task_success": 0.91},
  "eval_report": "evals/2.4.1.json",
  "lineage": {"data": "ds_17", "code": "git:abc123", "prompt": "p@3.2.0"},
  "stage": "Staging|Production|Archived"
}
```

### 3.2 Stages & promotion

```text
None → Staging (offline green) → Production (canary green) → Archived
```

**Only registry artifacts** are deployable — no “it works on my laptop” weights.

---

## 4. CI/CD for ML & LLM

### 4.1 CI checks

| Check | ML | LLM |
|-------|----|-----|
| Unit tests | transforms | parsers, tools |
| Data validation | schema, nulls | chunk stats |
| Training dry-run | 1-batch | 1-step LoRA optional |
| Eval suite | holdout metrics | golden + safety |
| Policy | license | license + jailbreak |
| IaC | serve config | prompt bundle hash |

### 4.2 CD strategies

- Blue/green  
- Canary %  
- Shadow traffic  
- Rolling with auto-rollback  

```yaml
# conceptual gate
promote_to_prod:
  require:
    - offline_task_success >= baseline - 0.01
    - safety_asr <= 0.02
    - p95_latency_ms <= SLO
    - human_approval: true  # for high risk
```

### 4.3 Prompt as code

```text
/prompts
  support_triage/
    system.md
    tools.json
    VERSION
/evals
  support_triage_v3.jsonl
```

PR must include eval delta commentary.

---

## 5. Serving Infrastructure

### 5.1 Patterns

| Pattern | Use |
|---------|-----|
| Batch scoring | nightly risk |
| Online REST/gRPC | interactive |
| Streaming tokens | chat UX |
| Async workers | long agents |
| Edge / on-device | privacy, offline |

### 5.2 LLM serve components

```text
API gateway → auth/rate limit → router (model/adapter)
  → prefill/decode workers → cache (prefix/KV)
  → tool workers → guardrails → response
```

### 5.3 Autoscaling signals

- Queue depth  
- GPU util / KV memory  
- TTFT SLO violations  
- Token throughput  

Scale on **lagging and leading** indicators; GPU scale-up is slow — keep headroom.

### 5.4 Multi-model routing

```text
if task=="classify" and len<500: slm_local
elif needs_deep_reason: frontier_api
else: mid_model
```

Log route decisions for cost analysis.

---

## 6. A/B Tests & Experimentation

### 6.1 Design

- Randomize on user_id hash  
- Fixed assignment for session consistency  
- Primary metric pre-registered  
- Guardrail metrics (safety, latency)  

### 6.2 LLM-specific metrics

| Primary | Guardrails |
|---------|------------|
| task success proxy | toxicity/safety flags |
| CSAT / thumbs | cost per session |
| time-to-resolution | tool error rate |
| conversion | p95 latency |

### 6.3 CUPED / variance reduction (concept)

Use pre-period covariates to reduce variance when traffic limited.

### 6.4 Stop rules

- Minimum sample  
- Sequential testing caution (peeking)  
- Kill switch on safety  

---

## 7. Drift Monitoring

### 7.1 Types

| Drift | Detect |
|-------|--------|
| Input data | PSI, KS, embed centroid shift |
| Label | delayed ground truth |
| Prediction | output distribution |
| Embedding | RAG query space shift |
| Concept | same input, new best action |
| Prompt injection mix | attack rate |

### 7.2 Actions

```text
alert → triage dashboard → shadow retrain/eval → fix data/prompt/model → canary
```

### 7.3 RAG drift

- Document freshness lag  
- Empty retrieve rate ↑  
- Score distribution shift  
- New jargon not in embedder  

---

## 8. Cost Control

### 8.1 Unit economics

\[
\text{cost/successful task} = \frac{\text{model + tools + infra + human}}{\#\text{ successes}}
\]

Optimizing tokens alone can increase failures → worse true cost.

### 8.2 Levers

| Lever | Effect |
|-------|--------|
| Smaller models | $↓ quality? |
| Caching | $↓ |
| RAG precision | fewer tokens |
| Constrained decode | fewer retries |
| Early rules/ deterministic | skip LLM |
| Batch non-urgent | GPU util ↑ |
| Quantization | $↓ |
| Budget caps per tenant | protect margin |

### 8.3 FinOps dashboards

- $ per feature  
- $ per customer tier  
- Waste: retries, loops, overlong max_tokens  

---

## 9. Reliability & SLOs

### 9.1 Example SLO set

```yaml
availability: 99.9%
p95_ttft_ms: 800
p95_e2e_ms: 3000
tool_error_rate: < 1%
task_success_7d: > 0.88
safety_incident: 0 sev-1
```

### 9.2 Error budgets

If burn rate high → freeze features, fix reliability.

### 9.3 Chaos for LLM systems

- Tool timeouts  
- Empty index  
- Model 429s  
- Partial multi-agent failures  

Verify fallbacks: degrade gracefully, don’t silent-hallucinate.

---

## 10. Security Ops

- Secrets in vault, not prompts  
- Tenant isolation tests in CI  
- SBOM for containers  
- Model/provenance supply chain  
- Audit logs for tool side effects  
- Red-team on release  

---

## 11. Tooling Map (category-level, offline curriculum)

| Category | Responsibility |
|----------|----------------|
| Tracking | experiments, params |
| Registry | models/prompts |
| Orchestration | pipelines |
| Serve | batch/online/LLM |
| Feature | train-serve features |
| Observability | metrics/traces/logs |
| Eval | golden harnesses |
| Data quality | validators |
| Infra as code | reproducible envs |

Prefer **few integrated tools** over a zoo.

---

## 12. Reference Production Blueprint (support copilot)

```text
Git mono-repo:
  app/           API + UI
  prompts/       versioned
  evals/         golden + safety
  pipelines/     index build
  infra/         k8s/terraform
  runbooks/      incidents

Flow:
  PR → CI (unit+eval) → staging deploy → canary 5% → prod
  nightly: reindex docs + drift report
  weekly: human label review → suite growth
```

---

## 13. RTMA Labs

### Lab O1 — Registry stub

- **Run:** save model/prompt artifact with hash + metrics  
- **Trace:** lineage json  
- **Metric:** promote only if eval pass  
- **Artifact:** `o1_registry/`

### Lab O2 — CI eval gate

- **Run:** script fails if pass_rate < baseline  
- **Metric:** gate correctness on intentional regression  
- **Artifact:** `o2_ci_log.txt`

### Lab O3 — Canary simulator

- **Run:** two systems, traffic split offline bootstrap  
- **Metric:** detect quality drop  
- **Artifact:** `o3_canary.md`

### Lab O4 — Drift report

- **Run:** PSI on feature or embedding dims week1 vs week2  
- **Metric:** alert threshold demo  
- **Artifact:** `o4_drift.json`

### Lab O5 — Cost unit

- **Run:** compute $/success for baseline vs cached  
- **Metric:** delta  
- **Artifact:** `o5_finops.csv`

---

## 14. Runbooks (minimum set)

1. Model 5xx / timeouts  
2. Cost spike  
3. Safety flag surge  
4. Index stale / empty retrieve  
5. Bad canary rollback  
6. Data poison suspicion  

Each: symptoms → dashboards → mitigate → verify → postmortem.

---

## 15. Production Checklist

- [ ] Pipelines idempotent  
- [ ] Feature/train-serve parity tests  
- [ ] Registry stages enforced  
- [ ] CI eval + safety gates  
- [ ] Canary + rollback automated  
- [ ] SLOs + error budget  
- [ ] Drift monitors  
- [ ] Cost dashboards  
- [ ] Secrets/IAM reviewed  
- [ ] Runbooks drilled  
- [ ] RTMA on releases  

---

## 16. CYPHER0X9 Proof Seal

```text
PACK: MLOPS-AND-PRODUCTION
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
PROOF: RTMA labs O1–O5
AXIOM: Deploy only registry artifacts that passed eval gates.
```

**Teach-back:** Draw LLM CD flow; define registry record; list guardrail metrics for A/B; compute cost/success; write one rollback trigger.

---

*End of pack · UC AI Free University · Production is the real exam.*
