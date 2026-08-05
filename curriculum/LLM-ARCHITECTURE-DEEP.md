# LLM Architecture Deep Dive
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** LLM-ARCH-401 · **Level:** Advanced · **Prereq:** linear algebra, probability, Python  
> **Outcome:** You can read a transformer paper, reason about serving cost, choose quantization, and design a training → SFT → preference stack.

---

## 0. Mental Model (one page)

```text
Tokens → Embeddings (+ Position) → N × Transformer Block → LM Head → Logits → Softmax → Next token
                    ↑
         (optional: MoE routers, KV cache, speculative draft)
```

A modern decoder-only LLM is a stack of **self-attention + feed-forward** blocks that map a sequence of tokens to a distribution over the next token. Everything else (chat, tools, agents, RAG) sits on this generator.

| Component | Job | Failure if wrong |
|-----------|-----|------------------|
| Tokenizer | text ↔ ids | OOV explosion, bad multilingual |
| Embedding | id → vector | underfit rare tokens |
| Attention | mix context | long-range collapse |
| FFN / MoE | nonlinear transform | capacity waste |
| LM head | vector → vocab logits | calibration drift |
| Sampler | logits → token | repetition / blandness |

---

## 1. Transformers from First Principles

### 1.1 Scaled Dot-Product Attention

Given queries \(Q\), keys \(K\), values \(V\) of dim \(d_k\):

\[
\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right) V
\]

**Why \(\sqrt{d_k}\)?** Dot products grow with dimension; without scaling, softmax saturates → vanishing gradients.

```python
import math
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(q, k, v, mask=None):
    # q,k,v: [B, H, T, D]
    d_k = q.size(-1)
    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, v), weights
```

### 1.2 Multi-Head Attention (MHA)

Split \(d_{model}\) into \(h\) heads so each head learns a different subspace (syntax vs entity vs long-range).

```text
Q,K,V = X W_q, X W_k, X W_v
heads_i = Attention(Q_i, K_i, V_i)
out = Concat(heads) W_o
```

**GQA / MQA (serving win):** share K/V across query heads → smaller KV cache, same quality band for many models (Llama-3 style GQA).

| Pattern | Q heads | KV heads | KV cache size |
|---------|---------|----------|---------------|
| MHA | H | H | full |
| GQA | H | H/g | 1/g |
| MQA | H | 1 | ~1/H |

### 1.3 Causal Mask (decoder-only)

Token \(t\) may attend only to \(\le t\). Training uses a lower-triangular mask; inference uses KV cache (past keys/values stored).

### 1.4 Residual Stream + LayerNorm / RMSNorm

```text
x = x + Attention(Norm(x))
x = x + FFN(Norm(x))
```

Pre-norm (Norm before sublayer) is standard for deep stacks — more stable than post-norm. RMSNorm drops mean-centering for speed with little quality loss.

### 1.5 Feed-Forward Network (SwiGLU)

Classic: \(\mathrm{GELU}(xW_1)W_2\). Modern: **SwiGLU** (SiLU gate × linear) — used in Llama/Mistral family.

\[
\mathrm{FFN}(x) = (SiLU(xW_g) \odot xW_u) W_d
\]

Typical expansion: \(4\times d_{model}\) (or \(8/3\times\) for SwiGLU to keep param count).

---

## 2. Positional Encoding

Attention is **permutation-equivariant** without position. Options:

| Method | How | Pros | Cons |
|--------|-----|------|------|
| Absolute sin/cos (Vaswani) | fixed PE added to emb | simple | weak extrapolation |
| Learned absolute | embedding table by index | flexible | fixed max len |
| Relative (Shaw/T5) | bias by distance | better local | more complex |
| **RoPE** | rotate Q/K by angle ∝ position | excellent extrapolation band | long-context need scaling |
| ALiBi | linear attention bias | long free | less standard now |
| YaRN / NTK-aware | RoPE rescale for long ctx | train short, run long | tune carefully |

### 2.1 RoPE (Rotary Position Embedding) sketch

For 2D pair of dims, rotate by \(\theta_i = 10000^{-2i/d}\):

\[
\begin{bmatrix} q'_{2i} \\ q'_{2i+1} \end{bmatrix}
=
\begin{bmatrix} \cos m\theta_i & -\sin m\theta_i \\ \sin m\theta_i & \cos m\theta_i \end{bmatrix}
\begin{bmatrix} q_{2i} \\ q_{2i+1} \end{bmatrix}
\]

Relative position falls out of \(Q_m^\top K_n \propto (m-n)\).

### 2.2 Long-context engineering

- **Sliding window** attention (local + sparse global)
- **Ring / block sparse** patterns
- **Chunked prefill** + streaming decode
- **YaRN** base-frequency scaling when extending from 8k → 128k
- Dual-chunk / hierarchical memory for agent contexts

**Rule of thumb:** advertised context ≠ reliable context. Measure needle-in-haystack *and* multi-needle *and* mid-doc QA degradation curves.

---

## 3. Mixture of Experts (MoE)

Sparse activation: route each token to \(k\) of \(E\) experts (usually \(k=1\) or \(2\)).

```text
g = Softmax(Router(x))           # [E]
top-k experts process token
y = sum_i g_i * Expert_i(x)
```

| Term | Meaning |
|------|---------|
| Expert | FFN specialist |
| Router | linear → logits over experts |
| Load balancing loss | prevent expert collapse |
| Capacity factor | max tokens/expert/batch |
| Shared expert | always-on FFN (DeepSeek-style) |

**Train gotchas:** expert imbalance, routing noise, all-to-all communication cost on multi-GPU.

**Serve gotchas:** expert parallelism vs replication; cold experts; higher VRAM than dense of same active FLOPs.

---

## 4. KV Cache & Inference Math

### 4.1 Prefill vs decode

- **Prefill:** process prompt in parallel (compute-bound).
- **Decode:** one token at a time; read growing KV (memory-bandwidth bound).

### 4.2 Cache size formula

\[
\mathrm{bytes} \approx 2 \times L \times H_{kv} \times D_{head} \times T \times b_{dtype}
\]

(2 for K and V; \(L\) layers; \(T\) sequence length).

Example (order-of-magnitude): 32 layers, 8 KV heads, 128 dim, fp16, 8k tokens → tens of MB per request; multi-user batches dominate GPU HBM.

### 4.3 Optimizations

| Technique | Idea | Tradeoff |
|-----------|------|----------|
| GQA/MQA | fewer KV heads | slight quality |
| Quantized KV (int8/fp8) | compress cache | rare accuracy hit |
| PagedAttention | non-contiguous pages | fragmentation free |
| Prefix caching | share system prompt KV | multi-tenant careful |
| Speculative decoding | draft small + verify large | needs draft model |
| Continuous batching | pack sequences | scheduler complexity |

```python
# Pseudocode: decode step with cache
def decode_step(model, token_id, past_kv):
    logits, new_kv = model.forward_one(token_id, past_kv)
    next_id = sample(logits[:, -1, :], temperature=0.7, top_p=0.9)
    return next_id, new_kv
```

---

## 5. Training Pipeline: Pre-train → SFT → Preference

```text
[Web + code + books + synthetic]
        │
        ▼
   PRETRAIN (next-token CE)
        │  → base model
        ▼
   SFT (instruction/chat pairs)
        │  → chat model
        ▼
   Preference (RLHF / DPO / ORPO / KTO)
        │  → aligned model
        ▼
   Domain adapters (LoRA) / tools / RAG
```

### 5.1 Pre-training

- **Objective:** causal LM cross-entropy
- **Data mix:** quality filtering, dedup (MinHash), domain balance, decontamination vs eval sets
- **Scaling laws (Kaplan / Chinchilla):** for fixed compute, optimal params vs tokens; **Chinchilla** says more tokens than old Kaplan recipes
- **Stability:** warmup, cosine/WSD schedules, grad clip, mixed precision (bf16), ZeRO / FSDP

### 5.2 Supervised Fine-Tuning (SFT)

- Format: system / user / assistant turns with special tokens
- **Diversity > volume** after a point; multi-task packing
- Mask loss on prompts if desired (train only on assistant tokens)

### 5.3 RLHF classic

1. Collect preferred vs rejected responses  
2. Train **reward model** \(r_\theta(x,y)\)  
3. Optimize policy with PPO against reward + KL penalty to SFT ref  

Problems: reward hacking, expensive PPO, RM brittleness.

### 5.4 DPO (Direct Preference Optimization)

Skip explicit RM; closed-form preference loss against reference policy:

\[
\mathcal{L}_{DPO} = -\log \sigma\left(\beta \log\frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log\frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\right)
\]

**When DPO wins:** offline prefs, simpler stack.  
**When RLHF still used:** online sampling, complex multi-objective rewards.

### 5.5 Scaling laws practical checklist

- [ ] Plot loss vs compute (log-log) for ablations  
- [ ] Hold out true decontaminated eval  
- [ ] Track data repeats (epoch >1 often hurts)  
- [ ] Measure downstream not only perplexity  

---

## 6. Quantization (GPTQ / AWQ / GGUF)

Goal: lower bits per weight → fit bigger model / faster matmuls.

| Method | Bits | How | Best for |
|--------|------|-----|----------|
| PTQ naive | 8 | round | easy baseline |
| **GPTQ** | 3–4 | Hessian-aware weight quant | offline high quality |
| **AWQ** | 4 | protect salient channels | activation-aware |
| SmoothQuant | 8 | migrate act outliers to weights | int8 serve |
| bitsandbytes QLoRA | 4 | NF4 + double quant | train adapters |
| **GGUF** (llama.cpp) | 2–8 | k-quants, CPU/Metal | local/edge |
| FP8 train/serve | 8 | H100+ native | modern stacks |

```bash
# Conceptual GGUF convert + quant (llama.cpp family)
# python convert_hf_to_gguf.py ./model --outfile model-f16.gguf
# ./quantize model-f16.gguf model-Q4_K_M.gguf Q4_K_M
```

**Eval after quant always:** MMLU subset, your golden set, perplexity on domain corpus, tool-call JSON validity rate.

**KV quant vs weight quant:** independent knobs; combine carefully.

---

## 7. Serving Architecture

```text
Client → API Gateway → Router
                         ├─ Rate limit / auth
                         ├─ Prompt template + tools
                         └─ Scheduler
                              ├─ Prefill workers
                              ├─ Decode continuous batch
                              └─ Prefix / LoRA multiplex
```

### 7.1 Key metrics

| Metric | Definition | Target thinking |
|--------|------------|-----------------|
| TTFT | time to first token | UX feel |
| TPOT / ITL | inter-token latency | stream smoothness |
| tokens/s | throughput | cost |
| concurrency | simultaneous seqs | capacity |
| $ / 1M tokens | fully loaded | unit economics |

### 7.2 Sampling knobs

```python
# Common decode controls
{
  "temperature": 0.0,   # greedy for tools/JSON
  "top_p": 0.9,
  "top_k": 40,
  "min_p": 0.05,
  "repetition_penalty": 1.05,
  "max_tokens": 1024,
  "stop": ["</tool_call>"],
  "seed": 42            # reproducibility for eval
}
```

**Structured outputs:** constrained decoding / grammar (JSON schema, regex) beats “please return JSON” alone.

### 7.3 Failure modes in production

1. **Context overflow** — silent truncate kills RAG citations  
2. **KV OOM** — long multi-turn without eviction  
3. **Stop-token leakage** — chat templates mismatch train format  
4. **Tokenizer mismatch** — client vs server BPE versions  
5. **Temperature >0 + tools** — invalid JSON; use constrained decode  
6. **Multi-tenant prefix cache poisoning** — isolate tenants  

---

## 8. Chat Templates & Special Tokens

Never invent a template that wasn’t used in SFT. Mismatch = capability collapse.

```text
Example (conceptual ChatML-style):
<|im_start|>system
You are a precise engineering assistant.
<|im_end|>
<|im_start|>user
Explain GQA in one paragraph.
<|im_end|>
<|im_start|>assistant
```

Checklist:

- [ ] BOS/EOS consistent  
- [ ] Tool call format matches training  
- [ ] System prompt position stable  
- [ ] Multi-turn history not double-wrapped  

---

## 9. Architecture Families (map, not hype)

| Family trait | Implication |
|--------------|-------------|
| Dense decoder | simple serve, full FLOPs |
| MoE sparse | high capacity / active FLOP |
| Small SLM 1–8B | edge, high QPS tools |
| Mid 70B-class | quality/cost balance |
| Frontier closed API | best raw reasoning, less control |
| Vision-language | image tokens + projector |
| Reasoner / long CoT | train for think tokens; latency ↑ |

---

## 10. Lab Exercises (RTMA-ready)

### Lab A — Attention unit

- **Run:** implement SDP attention + causal mask; compare to `torch.nn.functional.scaled_dot_product_attention`  
- **Trace:** log shapes of Q,K,V, scores, weights  
- **Metric:** max abs error < 1e-5 vs reference  
- **Artifact:** `artifacts/lab_a_attention_shapes.json`

### Lab B — KV cache memory model

- **Run:** spreadsheet or script: bytes vs (layers, heads, dim, seq, dtype)  
- **Trace:** inputs + formula used  
- **Metric:** predicted vs measured VRAM (if GPU available)  
- **Artifact:** `kv_budget.csv`

### Lab C — Quant quality gate

- **Run:** same prompts on fp16 vs Q4 on a small open model  
- **Trace:** outputs + tokenizer version  
- **Metric:** exact-match on 20 fact Qs; JSON validity rate  
- **Artifact:** `quant_eval_report.md`

### Lab D — Context reliability curve

- **Run:** needle at 10%, 50%, 90% depth for 4k/8k/16k  
- **Metric:** retrieval accuracy vs depth  
- **Artifact:** plot data table (offline)

---

## 11. Design Interview Sketch: “Serve a 70B chat API”

1. **Model choice:** GQA, known chat template, license OK  
2. **Quant:** AWQ/GPTQ 4-bit for cost; FP8 if hardware  
3. **Infra:** continuous batching + paged KV + prefix cache  
4. **API:** streaming SSE, structured tools, idempotency keys  
5. **Observability:** TTFT/TPOT histograms, token accounting, toxic rate  
6. **Safety:** input/output filters, rate limits, audit logs  
7. **Eval gate:** golden set + canary before promote  

Capacity estimate:

```text
tokens_per_day = concurrent_users * tokens_per_session * sessions
GPUs ≈ (active_params_FLOPs * tokens) / (GPU_FLOPs * util)
Also bound by HBM for KV, not only FLOPs.
```

---

## 12. Glossary

| Term | Definition |
|------|------------|
| Autoregressive | next token conditioned on past |
| Prefill | prompt processing phase |
| Decode | token generation phase |
| Perplexity | exp(avg NLL); lower better |
| KL penalty | keep policy near ref in RLHF |
| Speculative decoding | draft-verify speedup |
| Tensor parallel | split layers across GPUs |
| Pipeline parallel | split depth across GPUs |
| ZeRO | shard optimizer/state |

---

## 13. Master Checklist Before “Production Model”

- [ ] Architecture card: layers, heads, GQA, ctx, tokenizer  
- [ ] Training stages documented (data hashes)  
- [ ] Chat template golden tests  
- [ ] Quant recipe + quality delta  
- [ ] Serving SLO: TTFT p95, error budget  
- [ ] Eval suite: general + domain + safety  
- [ ] Rollback: previous model artifact immutable  
- [ ] Cost: $ / 1k successful task completions (not just tokens)

---

## 14. Further Self-Study Order (offline)

1. Attention is All You Need (core)  
2. GPT-2/3 technical reports (scaling intuition)  
3. Llama / Mistral model cards (modern stack)  
4. RoPE + YaRN notes (context)  
5. FlashAttention paper (IO-aware)  
6. DPO paper (preference without RM)  
7. vLLM / PagedAttention (serve)  
8. GPTQ / AWQ / GGUF docs (compress)

---

## 15. CYPHER0X9 Proof Seal

```text
PACK: LLM-ARCHITECTURE-DEEP
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
PROOF STYLE: RTMA (Run · Trace · Metric · Artifact)
MODE: Offline-first · dense technical · no CDN required
```

**Teach-back (pass if you can explain without notes):**  
Why decode is memory-bound; why RoPE helps relative position; why DPO can replace PPO; why GQA shrinks KV; why quant must be eval-gated.

---

*End of pack · UC AI Free University · Curriculum lattice seed · Grow by teaching.*
