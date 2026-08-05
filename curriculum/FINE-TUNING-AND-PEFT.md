# Fine-Tuning and PEFT
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** FT-401 · **Level:** Advanced applied  
> **Outcome:** Choose full FT vs LoRA/QLoRA, prepare data, run SFT/DPO, eval before/after, and know when **not** to fine-tune.

---

## 0. Decision Tree (start here)

```text
Is the failure style/format/domain language?
  ├─ Can prompt + tools + RAG fix it? → DO THAT FIRST
  ├─ Need stable behavior at high volume / offline? → consider FT
  └─ Need new factual knowledge that changes weekly? → RAG, not FT

Is compute limited?
  ├─ Yes → LoRA / QLoRA
  └─ No, and large data → full FT or continued pretrain carefully

Is preference/alignment the issue?
  └─ SFT then DPO/ORPO (or RLHF if online reward)
```

**Fine-tuning is a product decision**, not a resume decoration.

---

## 1. Full Fine-Tune vs PEFT

| Approach | What's trained | VRAM | Risk | Best for |
|----------|----------------|------|------|----------|
| Full FT | all weights | high | forgetting, cost | big data, new domain |
| LoRA | low-rank adapters | medium | small capacity | most product FT |
| QLoRA | LoRA on 4-bit base | low | quant noise | consumer GPUs |
| Prefix / prompt tuning | soft prompts | low | limited | light style |
| Adapters (Houlsby) | bottleneck modules | med | older stack | research parity |
| DoRA / rsLoRA | LoRA variants | med | newer | quality chase |

### 1.1 LoRA math

For weight \(W\), train \(\Delta W = BA\) with rank \(r \ll \min(d_{in},d_{out})\):

\[
W' = W + \frac{\alpha}{r} BA
\]

Typical: inject into attention `q,v` (sometimes `k,o` and MLP).

| Hyperparam | Practical range |
|------------|-----------------|
| rank \(r\) | 8–64 |
| alpha | ~1–2× r |
| dropout | 0.05–0.1 |
| target modules | q_proj,v_proj (+more) |

```python
# Conceptual PEFT config
lora_config = {
  "r": 16,
  "lora_alpha": 32,
  "lora_dropout": 0.05,
  "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
  "bias": "none",
  "task_type": "CAUSAL_LM",
}
```

### 1.2 QLoRA essentials

- Base weights in **NF4** (or similar 4-bit)  
- Double quantization optional  
- Compute in bf16/fp16 for LoRA mats  
- Paged optimizers when CPU offload needed  

---

## 2. Data Preparation

### 2.1 Instruction / chat format

```jsonl
{"messages":[
  {"role":"system","content":"You are a concise SQL tutor."},
  {"role":"user","content":"Write a query to ..."},
  {"role":"assistant","content":"SELECT ..."}
]}
```

Rules:

- Match **inference chat template** exactly  
- Mask loss on non-assistant tokens when appropriate  
- Deduplicate; remove eval contamination  
- Balance tasks; avoid 90% one intent  

### 2.2 Quality > quantity curve

| Stage | Data notes |
|-------|------------|
| 100–1k | prototype style lock |
| 1k–10k | solid SFT if clean |
| 10k–100k+ | multi-task; watch noise |
| Synthetic | verify; model collapse risk |

### 2.3 Synthetic data pipeline

```text
seed tasks → generate → filter (unit tests, rubrics, executors) → human sample audit → train
```

Never train on unfiltered model outputs for correctness-critical domains.

### 2.4 Preference pairs (DPO)

```jsonl
{"prompt":"...","chosen":"...","rejected":"..."}
```

Sources: human rank, better-vs-worse models, unit-test pass vs fail, shorter correct vs verbose wrong.

---

## 3. Supervised Fine-Tuning (SFT)

### 3.1 Objectives

- Teach format, tools, tone  
- Specialize domain language  
- Improve instruction following  

### 3.2 Hyperparameter starter (LoRA SFT)

```text
lr: 1e-4 to 2e-4 (LoRA) ; 5e-6 to 2e-5 (full)
epochs: 1–3 (more → overfit)
batch: as large as VRAM; grad accum to effective 16–128
warmup: 3–5%
scheduler: cosine
max_seq_len: match product
pack: sequence packing for efficiency (careful with cross-doc attention)
```

### 3.3 Catastrophic forgetting

Symptoms: general capability drop, safety regressions.

Mitigations:

- Mix general instruction data (replay)  
- Lower LR / fewer epochs  
- Smaller rank  
- Evaluate general + domain suites  

---

## 4. Preference Optimization

### 4.1 DPO recap

Train policy to upweight chosen vs rejected relative to reference (usually SFT model).

### 4.2 Variants map

| Method | Idea |
|--------|------|
| DPO | offline prefs, simple |
| IPO | alternate objective |
| KTO | binary desirable signals |
| ORPO | odds ratio, sometimes no ref |
| RLHF-PPO | online sampling + RM |

### 4.3 DPO practical tips

- Start from strong SFT  
- β too high → stuck near ref; too low → drift/hack  
- Length bias: rejected may be longer; normalize awareness  
- Safety prefs mandatory in mix  

---

## 5. Eval Before / After (mandatory gate)

### 5.1 Suites to run every FT

| Suite | Purpose |
|-------|---------|
| Domain golden | why you FT'd |
| General smoke | forgetting check |
| Safety / injection | regression |
| Tool JSON validity | format |
| RAG faithfulness | if applicable |
| Latency/cost | same hardware |

### 5.2 Report template

```text
BASE model_id: ...
FT artifact: ...
Data: n=, hash=
Domain pass: 0.72 → 0.88 (+16)
General pass: 0.81 → 0.79 (-2)  # acceptable?
Safety ASR: 0.04 → 0.05
p95 latency: +3%
Decision: SHIP / ITERATE / ABORT
```

### 5.3 Statistical humility

With small goldens, bootstrap confidence intervals; don’t ship on +1 case luck.

---

## 6. When NOT to Fine-Tune

1. **Knowledge freshness** — use RAG  
2. **One-off tasks** — prompt  
3. **Brittle tool APIs** — better schemas + constrained decode  
4. **Unlabeled mess** — clean data first  
5. **Safety-only failures** — policy + filters + DPO mix carefully; don’t “just FT jailbreaks”  
6. **No eval suite** — you cannot detect regressions  
7. **License forbids** — legal stop  
8. **Latency already tight** — adapters may be OK; huge full FT models may not  

**Opportunity cost:** weeks of FT often lose to one week of retrieval + eval.

---

## 7. Serving Adapters

```text
Base model (shared) + LoRA adapters per tenant/task
Router selects adapter_id
Merge adapters offline for single-file deploy if needed
```

| Mode | Pros | Cons |
|------|------|------|
| Dynamic LoRA | multi-skill one GPU | orchestration |
| Merged weights | simple serve | many artifacts |
| Base only | simplest | loses FT gains |

Watch: adapter hot-swap memory fragmentation; version pin adapters with base revision.

---

## 8. Continued Pretraining (domain)

Train causal LM on domain corpus **before** SFT when language distribution is far (legal, medical notes, code dialect).

```text
base → continued PT (domain text) → SFT (instructions) → prefs
```

Risks: compute, forgetting, data licensing, leakage of secrets in corpus (scan!).

---

## 9. Safety & Privacy in FT

- Scrub PII/secrets from train data  
- Dedup against private eval  
- Include refusal examples  
- Red-team after FT  
- Document data provenance in model card  

---

## 10. Tooling Landscape (conceptual)

| Job | Tool class |
|-----|------------|
| Train LoRA | PEFT + HF Trainer / Axolotl / Unsloth-like |
| Data | JSONL cleaners, dedup |
| Eval | custom harness (see EVAL pack) |
| Quant after | GPTQ/AWQ/GGUF |
| Registry | model cards + hashes |

Pick one stack and master it; switching mid-project burns time.

---

## 11. End-to-End Lab Recipe

```text
1. Freeze metrics + golden v1
2. Baseline: base model + best prompt/RAG
3. Collect 2k clean SFT rows
4. LoRA SFT 1 epoch
5. Eval gate
6. Build 1k preference pairs from failures
7. DPO
8. Eval gate + safety
9. Quantize candidate
10. Canary online
```

---

## 12. RTMA Labs

### Lab F1 — LoRA SFT micro

- **Run:** 500-instruction toy domain  
- **Trace:** train logs, loss curves  
- **Metric:** domain exact-match before/after  
- **Artifact:** `f1_sft_report.md`

### Lab F2 — Forgetting check

- **Run:** general 50-case smoke pre/post  
- **Metric:** delta pass  
- **Artifact:** `f2_forget.csv`

### Lab F3 — DPO prefs

- **Run:** 300 pairs; DPO short train  
- **Metric:** win rate pairwise judge (calibrated)  
- **Artifact:** `f3_dpo.json`

### Lab F4 — QLoRA vs LoRA

- **Run:** same data two recipes if hardware allows  
- **Metric:** quality Δ + VRAM  
- **Artifact:** `f4_qlora.md`

### Lab F5 — Abort decision

- **Run:** attempt FT on “fresh facts” task vs RAG  
- **Metric:** accuracy@date  
- **Artifact:** `f5_rag_wins.md` (document why FT aborted)

---

## 13. Failure Modes

| Failure | Cause | Fix |
|---------|-------|-----|
| Template mismatch | train≠serve tokens | unify template tests |
| Overfit memorization | tiny data many epochs | less epoch, more data |
| Safety drop | domain data toxic skew | mix safety data |
| Tool break | format drift | more tool-call examples |
| Silent bad merge | wrong base rev | pin hashes |
| Eval illusion | contaminated gold | re-split |

---

## 14. Model Card Minimum (after FT)

```text
Base model + license
Training data summary + size + filters
Objectives (SFT/DPO)
Hyperparams
Eval tables (domain/general/safety)
Intended use / out-of-scope
Quantization notes
Contact / changelog
```

---

## 15. Production Checklist

- [ ] Prompt/RAG baselines beaten with evidence  
- [ ] Data cleaned, licensed, PII-scanned  
- [ ] Template parity tests  
- [ ] LoRA config recorded  
- [ ] Before/after eval + safety  
- [ ] Artifact hashed in registry  
- [ ] Serve plan (dynamic vs merge)  
- [ ] Rollback to previous artifact  
- [ ] Cost of training + inference noted  

---

## 16. CYPHER0X9 Proof Seal

```text
PACK: FINE-TUNING-AND-PEFT
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
PROOF: RTMA labs F1–F5
AXIOM: Fine-tune last, measure first.
```

**Teach-back:** Explain LoRA; write a when-not-to-FT list; design before/after gates; outline SFT→DPO data.

---

*End of pack · UC AI Free University · Adapters are scalpels, not sledgehammers.*
