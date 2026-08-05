# 🌈 Next-Level AI Engineering Field Guide

**CYPHER0X9 · AI Lab Free University**  
**Spine:** learn while building, prove as you go.  
**Evidence:** RTMA — Run · Trace · Metric · Artifact.

This is the bridge from the 425-lesson campus to a 90-day engineering practice.
It is vendor-neutral, offline-readable, and designed to produce a portfolio of
reproducible evidence rather than a folder of screenshots.

---

## 1. The system you are actually building

```text
question
  ↓
input policy → context assembly → model/router → tool or retrieval request
                                               ↓
approval gate ← proposed side effect ← bounded agent loop
      ↓                                        ↓
 tool runtime → typed result → correction → verification → answer
      ↓                                        ↓
  audit trace → quality + latency + cost + safety metrics → RTMA artifact
```

The model is one component. The product is the contract, context, tools,
permissions, retrieval, evaluation, observability, and human escape hatch around it.

### Derive one request end to end

| Stage | Input | Output | Failure to force | Evidence |
|---|---|---|---|---|
| Policy | user goal | allowed/denied scope | forbidden side effect | decision id |
| Context | approved sources | bounded prompt | injected document | source list |
| Model | typed contract | answer or tool call | malformed arguments | response id |
| Tool | validated arguments | typed result | timeout / bad input | call id + error |
| Retrieval | query + index | ranked chunks | empty / stale index | chunk ids |
| Verify | candidate result | pass/fail/correct | false citation | assertion trace |
| Release | verified output | human-approved action | missing approval | approval id |

---

## 2. The migration runway

Do not jump from a notebook demo to an autonomous production agent. Move one
failure boundary at a time.

```text
deterministic fixture
  → local mock
  → local open-weight model
  → one cloud provider behind an adapter
  → second-provider canary
  → tools with read-only permissions
  → retrieval with citations and empty-result behavior
  → bounded agent loop
  → golden + adversarial eval gates
  → human-approved release
```

At each arrow, freeze the previous known-good version and compare the same task set.

| Gate | Quality | Latency | Cost | Safety | Rollback |
|---|---|---|---|---|---|
| Local → cloud | task pass rate | p50/p95 | cost per passed task | data boundary | local fallback |
| Single → routed | route accuracy | route overhead | blended cost | provider policy | pin one route |
| Answer → tools | exactness | tool round trips | calls per success | allowlist | disable tools |
| Search → RAG | grounded pass rate | retrieval p95 | index/query cost | source ACL | keyword fallback |
| Workflow → agent | completion rate | turns/time | cost per completion | approval escapes | max-turn stop |

### Provider adapter contract

Keep provider details at the edge. Normalize only what the application needs:

```json
{
  "request": {"messages": [], "tools": [], "timeout_ms": 30000},
  "response": {
    "text": "",
    "tool_calls": [],
    "usage": {"input_tokens": 0, "output_tokens": 0},
    "trace": {"provider": "", "model": "", "request_id": ""}
  }
}
```

Never erase provider-specific errors. Preserve them under a namespaced trace field.

---

## 3. Local models versus frontier APIs

There is no universal winner; route by evidence.

| Decision | Local/open-weight | Frontier API | Measure before choosing |
|---|---|---|---|
| Privacy | data can remain local | data crosses a service boundary | policy + retention terms |
| Capability | varies sharply by model/quant | usually strongest broad capability | task pass rate |
| Availability | works offline; hardware-bound | network/quota/provider-bound | error rate + recovery time |
| Latency | predictable after warm-up | variable network + queue | warm/cold p50/p95 |
| Cost | hardware/electricity/ops | tokens, tools, storage, egress | cost per passed task |
| Control | weights/runtime choices | managed surface and safeguards | required controls |
| Maintenance | you own upgrades | provider owns infrastructure | operator hours/month |

Use a small local model for privacy, deterministic drills, classification, or
fallback when it passes the suite. Use a frontier service for hard reasoning,
multimodal work, or tool orchestration only when the measured gain pays for the
extra boundary. A router is useful only if its own errors are evaluated.

---

## 4. Prompt systems: from sentence to release artifact

### Evolution ladder

1. **Instruction** — one task, no durable contract.  
2. **Template** — named variables and explicit uncertainty.  
3. **Structured contract** — schema, refusal path, tool policy.  
4. **Context policy** — trusted instructions separated from untrusted data.  
5. **Versioned prompt** — immutable id and change note.  
6. **Eval-gated system** — golden/adversarial suite before promotion.

### Prompt card

```text
Goal: observable outcome
Inputs: trusted fields and untrusted fields
Constraints: safety, scope, time, token budget
Tools: purpose, schema, return shape, errors, approval class
Output: schema + uncertainty + citations
Stop: max turns, timeout, no-evidence rule
Success: exact evaluator and threshold
```

Change one variable per experiment. A shorter prompt is not better unless the
same suite still passes with lower cost or latency.

---

## 5. RAG: naive to production

```text
documents → parse → normalize → chunk+metadata → embed/index
                                                     ↓
question → query rewrite → lexical+dense retrieve → rerank → context budget
                                                     ↓
answer contract ← grounded generation ← cited chunks ← ACL/freshness filter
     ↓
faithfulness + answer relevance + retrieval hit rate + empty-result behavior
```

### Ablation matrix

| Experiment | Hold constant | Change | Primary metric | Common trap |
|---|---|---|---|---|
| Chunk size | corpus/query/model | 200 vs 500 vs 900 tokens | recall@k | overlap hides duplication |
| Overlap | size/embedder | 0 vs 10% vs 20% | answer coverage | index inflation |
| Retriever | corpus/chunks | lexical vs dense vs hybrid | hit rate | judging answer only |
| Top-k | everything else | 3 vs 5 vs 10 | recall and latency | context stuffing |
| Reranker | candidate set | none vs reranker | nDCG / task pass | reranker cost ignored |
| Freshness | query set | old vs refreshed index | stale-answer rate | silent partial update |

### Production invariants

- Every chunk has source id, location, version, access policy, and timestamp.
- Retrieval is scored separately from generation.
- Empty or unauthorized retrieval fails closed.
- Citations resolve to the exact indexed source.
- A corpus/index version travels with every answer trace.
- Reindexing has a canary, rollback, and stale-index alarm.

Run `python3 phase1-golden-slice/lab/06_rag_ablation.py` for the zero-key mechanism.

---

## 6. Agent loop: observe, act, correct, verify

```text
OBSERVE → choose next bounded action
   ↓
VALIDATE → schema + permission + budget
   ↓
ACT → execute one tool call
   ↓
CORRECT ← tool/schema/assertion failure
   ↓
VERIFY → evidence satisfies completion contract?
   ├─ no → loop if budget remains
   └─ yes → emit result + RTMA
```

### State data worth preserving

```json
{
  "goal": "",
  "state": "observe",
  "iteration": 0,
  "max_iterations": 4,
  "tool_allowlist": [],
  "approval_id": null,
  "trace": [],
  "completion_assertions": [],
  "stop_reason": null
}
```

The correction step may change the plan or arguments; it may not invent a tool
result. Verification checks the real artifact. A critic can reject work but cannot
grant itself more permission. Run `lab/07_agent_loop.py` to see the loop fail once,
correct, and stop within budget.

### Framework selection

| Shape | Best first move | Why | Exit signal |
|---|---|---|---|
| One or two tools | plain typed loop | maximum visibility | state logic repeats |
| Long-running state graph | graph/workflow framework | checkpoints + explicit edges | framework dominates logic |
| Provider-native tools | provider agent SDK | fast integration | portability becomes required |
| Multi-agent roles | only after single loop is measured | isolates real roles | coordination cost exceeds gain |
| Typed Python application | schema-first agent framework | validation near boundaries | custom runtime needs exceed it |

Compare frameworks on checkpointing, tool schemas, human interrupts,
observability, replay, portability, testability, and operational burden—not stars.

---

## 7. Eval harness: taste becomes engineering

### Three-layer harness

1. **Deterministic checks** — schema, exact values, citations, permissions, stop budget.  
2. **Model judge** — rubric-scored meaning where exact matching is insufficient.  
3. **Human gate** — calibrated review for ambiguity, risk, and release ownership.

```text
versioned task fixture
  → candidate system
  → raw output + trace
  → deterministic graders
  → blinded model judge (optional)
  → sampled human labels
  → disagreement analysis
  → release / block / investigate
```

| Metric | What it answers | Do not confuse with |
|---|---|---|
| task success | completed required outcome? | eloquence |
| precision/recall/F1 | classification quality? | retrieval recall@k |
| retrieval hit rate | correct evidence found? | grounded answer |
| citation precision | citations support claims? | citation presence |
| judge-human agreement | judge calibrated? | judge confidence |
| tool success rate | calls executed correctly? | end-to-end success |
| escape rate | unsafe action bypassed gate? | refusal rate |
| cost per passed task | useful economics? | cost per request |
| p95 latency | tail experience? | average latency |

LLM-as-judge is a measurement instrument, not an oracle. Calibrate it on held-out
human labels, blind candidate order, record judge version, and inspect disagreements.

---

## 8. Voice AI bridge

```text
audio capture → endpointing/VAD → STT partial/final → dialog state
  → LLM → tool(s) → response contract → TTS first audio → transport
  → barge-in / repeat / human handoff
```

Write one latency budget per leg. Measure p50 and p95, plus accuracy and handoff
success. Never use one total-turn average to hide a slow recognizer, tool, or
synthesizer. Text-agent GREEN comes before voice polish.

| Leg | Metric | Failure injection | Fallback |
|---|---|---|---|
| Capture/VAD | endpoint delay | noise/silence | reprompt |
| STT | word/domain error | jargon/accent | confirm critical field |
| LLM/tools | p95 + task success | timeout/tool error | bounded retry/human |
| TTS | time to first audio | long text | chunk/stream |
| Transport | jitter/loss | packet impairment | buffer/reconnect |
| Handoff | transfer success | unavailable human | honest queue message |

Run `lab/08_voice_latency_budget.py` with local fixtures, then replace fixture
timestamps with measurements from your own consented lab.

---

## 9. Safety watchdog: test the capability before it surprises you

Frontier safety research uses controlled sabotage and agentic-misalignment
evaluations to ask whether a model can insert subtle bugs, manipulate oversight,
hide capability, or choose harmful actions in a simulated environment. These are
stress tests—not proof that a deployed model independently conducted a real-world
cyberattack. The engineering lesson is still urgent: powerful tools plus long
horizons create a larger failure surface.

### Watchdog design

- Sandbox network, filesystem, and credentials.
- Default-deny every side effect; allowlist exact tools and targets.
- Separate proposer from executor; executor validates policy.
- Cap turns, wall time, spend, output bytes, and retries.
- Require approval for messages, publishing, purchases, deletion, and privilege change.
- Log tool request, policy decision, tool result, and caller linkage.
- Plant canary secrets and tripwires; alert on access attempts.
- Red-team prompt injection, confused-deputy paths, rollback tampering, and monitor evasion.
- Convert each incident or near miss into a permanent eval fixture.

Official starting points are recorded in `research-notes/SOURCES-2026.md`.

---

## 10. The 90-day builder path

| Days | Build | Proof to keep |
|---:|---|---|
| 1–7 | local hello + RTMA | 5 artifacts, one teach-back |
| 8–14 | typed tools + bounded loop | error/correction trace |
| 15–21 | prompt contract versions | eval diff + rollback |
| 22–30 | tiny RAG | ablation report + resolvable citations |
| 31–45 | provider adapter | local/cloud comparison scorecard |
| 46–60 | golden + adversarial evals | calibrated rubric + misses |
| 61–75 | optional voice bridge | stage p50/p95 + handoff drill |
| 76–84 | capstone hardening | threat list + canary + runbook |
| 85–90 | stranger test + portfolio | cold-start proof + demo narrative |

### Review rhythm

For each new idea, review at **1 hour → 24 hours → 7 days → 30 days →
90 days**. Keep each learning chunk to roughly five to nine connected units. At
every review, teach the idea simply, reconstruct the mechanism without notes, and
open the artifact.

### Feynman card

1. Explain it to a smart 12-year-old.  
2. Draw the data path.  
3. Name the hidden assumption.  
4. Force one failure.  
5. Show the metric and artifact.  
6. Teach the corrected model.

---

## 11. Portfolio capstone acceptance

Build a small domain coach with citations and an optional voice front end.

- [ ] Stranger follows the cold-start guide without your help.
- [ ] At least 25 versioned golden tasks run.
- [ ] Retrieval and generation are scored separately.
- [ ] Empty evidence produces an honest no-answer.
- [ ] Tool calls are typed, allowlisted, bounded, and replayable.
- [ ] Every side effect requires a human approval artifact.
- [ ] Quality, p95 latency, cost per passed task, and safety escapes are reported.
- [ ] Prompt/model/index changes run the suite before release.
- [ ] Rollback is written and rehearsed.
- [ ] The portfolio shows one failure, one correction, and one decision—not only success.

### Final RTMA

**Run:** exact cold-start command and task suite.  
**Trace:** input → retrieval/tools → policy → answer → approval.  
**Metric:** task pass rate, retrieval hit rate, citation precision, p95, cost, escapes.  
**Artifact:** versioned code, scorecard, runbook, demo, and a one-page architecture note.

> Build calmly. Break it safely. Prove the fix. Share freely.
