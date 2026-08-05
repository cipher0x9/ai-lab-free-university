# RAG Systems Deep Dive
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** RAG-401 · **Level:** Advanced systems  
> **Outcome:** Design, ablate, and productionize retrieval-augmented generation with measurable faithfulness and hit rate.

---

## 0. Why RAG Exists

LLMs have **parametric memory** (weights) that is static, blurry, and expensive to update. RAG adds **non-parametric memory** (documents) retrieved at query time.

```text
Query → Retrieve (top-k evidence) → (Rerank) → Augment prompt → Generate → Cite → Verify
```

| Goal | RAG contribution |
|------|------------------|
| Freshness | update index, not full retrain |
| Grounding | force answers from evidence |
| Privacy | keep data in your store |
| Cost | smaller generator + docs |
| Audit | citations / doc versions |

**RAG is not magic:** bad chunking, weak embeddings, or no eval → fluent hallucinations with fake citations.

---

## 1. Architecture Map

```text
                    ┌──────────────┐
  Documents ──────► │ Ingestion    │  parse → clean → chunk → embed → index
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
  Query ──────────► │ Query pipe   │  rewrite → expand → embed → search
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Hybrid + RR  │  BM25 ∪ vector → rerank → diversify
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Generator    │  grounded prompt + citations
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Verify/Eval  │  faithfulness, IDs, refusal
                    └──────────────┘
```

---

## 2. Chunking Strategies

### 2.1 Goals of a chunk

1. **Self-contained** enough to answer local questions  
2. **Small enough** for precise retrieval  
3. **Linked** to parent metadata (title, URL, section, version)

### 2.2 Strategy comparison

| Strategy | How | Pros | Cons |
|----------|-----|------|------|
| Fixed tokens (512/1024) | sliding window | simple | splits mid-thought |
| Overlap windows | 10–20% overlap | boundary safety | duplication |
| Sentence pack | pack to budget | cleaner | long sentences |
| Recursive structure | md/html headers | semantic | needs structure |
| Semantic chunking | embed + breakpoints | topical | cost + variance |
| Parent-child | small retrieve, large gen | best of both | complexity |
| Proposition / atomic | one fact per chunk | high precision | oversplit |

### 2.3 Practical defaults (start here)

```text
docs: 400–800 tokens, 10–15% overlap, split on markdown headers first
code: function/class level, keep imports in metadata or parent
tables: keep table intact or row-groups with header repeated
PDFs: layout-aware parse; don’t naively split mid-column
```

```python
def chunk_by_headers(md: str, max_tokens: int = 600, overlap: int = 80):
    """Conceptual: split on AT headers then pack to max_tokens with overlap."""
    sections = split_markdown_sections(md)
    chunks = []
    for sec in sections:
        for piece in pack_tokens(sec.text, max_tokens, overlap):
            chunks.append({
                "text": piece,
                "title": sec.title,
                "path": sec.path,
                "anchors": sec.anchors,
            })
    return chunks
```

### 2.4 Chunk metadata schema

```json
{
  "chunk_id": "doc12::h2.3::c4",
  "doc_id": "doc12",
  "version": "2026-03-01",
  "source": "handbook/policies.md",
  "title": "Refund Policy",
  "section": "Exceptions",
  "token_count": 512,
  "hash": "sha256:...",
  "acl": ["public"],
  "lang": "en"
}
```

**Never retrieve without ACL filters in multi-tenant systems.**

---

## 3. Embeddings

### 3.1 Properties that matter

| Property | Why |
|----------|-----|
| Dimensionality | index size + recall tradeoff |
| MTEB / domain score | general vs your domain gap |
| Instruction-aware | query vs passage prefixes |
| Multilingual | language coverage |
| Max sequence | long chunk support |
| License / local | offline deploy |

### 3.2 Query vs document asymmetry

Many models want:

```text
query:  "Represent this question for retrieving supporting docs: {q}"
passage: "{passage}"
```

Mismatch prefixes → silent recall loss.

### 3.3 Matryoshka / dimension truncation

Some embeddings allow using first D dims for cheaper ANN; validate recall@k after truncation.

### 3.4 When embeddings fail

- Near-identical boilerplate across docs  
- Numbers/IDs (order IDs, error codes) — use keyword/hybrid  
- Code identifiers — hybrid or code-specific models  
- Negation / subtle legal differences  

---

## 4. Vector Databases & Indexes

### 4.1 ANN families

| Index | Idea | Notes |
|-------|------|-------|
| Flat / brute | exact | gold for small |
| HNSW | graph | strong recall/latency |
| IVF-PQ | cluster + quant | huge corpora |
| DiskANN | disk-resident | cost scale |

### 4.2 Ops concerns

- **Upserts & deletes** — tombstones, rebuild cadence  
- **Filtering** — pre/post filter; pre-filter can wreck recall  
- **Sharding** — by tenant or collection  
- **Replication** — read HA  
- **Backups** — snapshot + doc store source of truth  

### 4.3 Dual store pattern

```text
Object store / git  = source of truth (raw docs)
Chunk store         = text + metadata
Vector index        = embeddings + ids
BM25 index          = lexical
```

Rebuild embeddings anytime from chunk store; never treat vectors as sole source of truth.

---

## 5. Hybrid Search

Lexical (BM25) + dense (ANN) catches complementary failures.

```text
candidates = union(
  bm25(q, k=50),
  vector(q, k=50)
)
merged = rrf(candidates) or weighted_score
top = rerank(merged, k=10)
```

### 5.1 Reciprocal Rank Fusion (RRF)

\[
\mathrm{score}(d) = \sum_{r \in rankers} \frac{1}{60 + \mathrm{rank}_r(d)}
\]

Simple, strong baseline without score calibration.

### 5.2 When pure vector is enough

- Semantic paraphrases only, clean corpus, good domain embedder  
Still keep BM25 for IDs and rare tokens.

---

## 6. Reranking

Cross-encoders / late-interaction models score (query, passage) pairs more accurately than bi-encoders.

```text
Retrieve 50 cheaply → Rerank top 50 → Keep 5–10 for LLM
```

| Stage | Cost | Quality |
|-------|------|---------|
| ANN | low | medium |
| Rerank | medium | high |
| LLM | high | generation |

**Latency budget example:** 30ms embed + 40ms ANN + 80ms rerank + 800ms LLM.

---

## 7. Query Understanding & Expansion

| Technique | Purpose |
|-----------|---------|
| HyDE | generate hypothetical answer, embed it |
| Multi-query | paraphrase N queries, fuse results |
| Step-back | abstract question then retrieve |
| Entity extract | force keyword filters |
| Route | choose collection / tool vs RAG |

```python
# multi-query fusion conceptual
queries = [q] + llm_paraphrase(q, n=3)
pools = [retrieve(qi, k=20) for qi in queries]
fused = rrf(pools)[:50]
final = rerank(q, fused)[:8]
```

Danger: expansion can retrieve **off-topic** fluency; always measure.

---

## 8. Prompting for Grounded Generation

```text
Answer ONLY using the evidence blocks.
If evidence is insufficient, say you don't know and list missing info.
Cite chunk_ids inline like [doc12::c4].
Do not use outside knowledge for facts.

Question: {q}

Evidence:
[1] (chunk_id=...) {text}
[2] (chunk_id=...) {text}
```

### 8.1 Citation rules

- Every factual sentence → ≥1 citation  
- Citations must map to provided IDs only  
- Post-check: regex extract IDs ⊆ retrieved set  

### 8.2 Context packing

Order: **most relevant first** or **interleave diversity**. Watch middle-context degradation on long packs. Prefer fewer high-quality chunks over 30 mediocre ones.

---

## 9. Citation Verification & Faithfulness

### 9.1 Automatic checks

```python
def citation_closed_world(answer: str, allowed_ids: set[str]) -> bool:
    cited = set(re.findall(r"\[([a-zA-Z0-9_.:-]+)\]", answer))
    return cited.issubset(allowed_ids) and len(cited) > 0
```

### 9.2 Faithfulness methods

| Method | Idea |
|--------|------|
| NLI entailment | claim entailed by evidence? |
| LLM-as-judge | “supported / partial / none” |
| Quote overlap | extractive support |
| Human audit | gold standard |

### 9.3 Hallucination types in RAG

1. **Fabricated citation**  
2. **Unsupported claim** with real citation nearby  
3. **Stale doc** correct-at-time wrong-now  
4. **Wrong ACL leak** (security bug)  
5. **Merged entities** across chunks  

---

## 10. Evaluation Methodology

### 10.1 Core metrics

| Metric | Definition | Layer |
|--------|------------|-------|
| Recall@k / Hit rate | gold doc in top-k | retrieval |
| MRR / nDCG | ranking quality | retrieval |
| Context precision | relevant fraction in context | pack |
| Context recall | needed evidence present | pack |
| Faithfulness | answer supported | generation |
| Answer relevancy | addresses question | generation |
| Citation precision | cited IDs actually used correctly | gen |
| End-task success | user job done | product |
| Latency p50/p95 | UX | ops |
| $/query | unit economics | ops |

### 10.2 Golden set design

```jsonl
{"id":"q17","question":"...","gold_doc_ids":["doc9"],"gold_answers":["..."],"difficulty":"hard","tags":["policy"]}
```

Rules:

- ≥100 questions for serious systems; 30 for prototype  
- Include **unanswerable** (should refuse)  
- Include ID/code queries (hybrid stress)  
- Decontaminate from training if you fine-tune  

### 10.3 Ablation methodology (required science)

Change **one** factor:

| Ablation | Example arms |
|----------|--------------|
| Chunk size | 256 / 512 / 1024 |
| Overlap | 0 / 64 / 128 |
| Embedder | A vs B |
| Hybrid | vector / bm25 / both |
| Reranker | off / on |
| k | 3 / 5 / 10 |
| Query rewrite | off / multi / HyDE |
| Generator | SLM vs large |

```text
REPORT TEMPLATE
baseline: hit@5=0.62 faithfulness=0.71 p95=1.8s
+rerank:  hit@5=0.74 faithfulness=0.78 p95=1.95s  Δ worth it? YES
+hyde:    hit@5=0.75 faithfulness=0.76 p95=2.4s   Δ not worth cost
```

---

## 11. Production RAG Patterns

### 11.1 Indexing pipeline

```text
webhook/git push → parse → PII scan → chunk → embed → upsert
                 → quality metrics (empty chunks, lang, size)
                 → canary query suite
```

### 11.2 Online path SLO example

| Stage | Budget |
|-------|--------|
| rewrite | 100ms |
| retrieve | 50ms |
| rerank | 80ms |
| generate | 1.2s |
| verify | 30ms |
| **total p95** | **~1.5–2.0s** |

### 11.3 Caching

- Query embedding cache  
- Exact query result cache (TTL)  
- Prefix KV for system+tool schemas  
- Doc version pin for answer reproducibility  

### 11.4 Multi-tenant safety

- Filter by `tenant_id` **before** returning chunks  
- Separate collections if needed  
- Never put another tenant’s text in prompt  

### 11.5 Failure modes & fallbacks

| Failure | Fallback |
|---------|----------|
| empty retrieval | clarify / web tool / human |
| low score | refuse or ask narrowing Q |
| generator contradiction | regenerate with stricter prompt |
| index lag | show doc as_of version |

---

## 12. Advanced Topics

### 12.1 GraphRAG / knowledge graphs

Extract entities/relations; retrieve subgraphs for multi-hop. Higher build cost; wins on relationship questions.

### 12.2 Agentic RAG

Agent decides: search → open → compare → answer, with budgets.

```text
while turns < N and not verified:
  plan → tool(retrieve/open) → reflect → maybe answer
```

### 12.3 Long-context vs RAG

| Approach | Strength | Weakness |
|----------|----------|----------|
| Stuff long ctx | simple | cost, mid-loss, stale whole-dump |
| RAG | scalable, fresh | retrieval errors |
| Hybrid | best docs + long window | complexity |

**2026 rule:** long context complements RAG; it does not replace indexing for large private corpora.

### 12.4 Multimodal RAG

Images/tables as chunks; CLIP-style or VLM embeddings; OCR text dual-index.

---

## 13. RTMA Labs

### Lab R1 — Chunk ablation

- **Run:** same corpus, 3 chunk sizes, fixed embedder  
- **Trace:** chunk stats histogram  
- **Metric:** hit@5, faithfulness, tokens/query  
- **Artifact:** `r1_chunk_ablation.csv`

### Lab R2 — Hybrid vs pure

- **Run:** vector / BM25 / RRF on golden set  
- **Metric:** hit@5 by query tag (semantic vs id)  
- **Artifact:** `r2_hybrid.md`

### Lab R3 — Rerank ROI

- **Run:** top50 → rerank top8 vs top8 raw  
- **Metric:** Δ faithfulness vs Δ latency  
- **Artifact:** `r3_rerank_roi.json`

### Lab R4 — Citation closed-world

- **Run:** post-validator on 100 answers  
- **Metric:** illegal citation rate  
- **Artifact:** `r4_cite_report.md`

### Lab R5 — Unanswerable detection

- **Run:** 30 questions with no support  
- **Metric:** correct refusal rate  
- **Artifact:** `r5_refuse.json`

---

## 14. Minimal Reference Implementation Sketch

```python
class RagPipeline:
    def __init__(self, embedder, vdb, bm25, reranker, llm):
        self.embedder = embedder
        self.vdb = vdb
        self.bm25 = bm25
        self.reranker = reranker
        self.llm = llm

    def answer(self, q: str, k=8, tenant=None):
        qv = self.embedder.encode_query(q)
        dense = self.vdb.search(qv, k=40, filters={"tenant": tenant})
        sparse = self.bm25.search(q, k=40, filters={"tenant": tenant})
        fused = rrf([dense, sparse])[:50]
        top = self.reranker.rank(q, fused)[:k]
        prompt = build_grounded_prompt(q, top)
        raw = self.llm.generate(prompt, temperature=0)
        if not citation_closed_world(raw, {c.id for c in top}):
            raw = self.llm.generate(prompt + "\nFix citations.", temperature=0)
        return {"answer": raw, "chunks": top}
```

---

## 15. Production Checklist

- [ ] Source of truth + versioning  
- [ ] Chunk strategy documented  
- [ ] Hybrid retrieval on  
- [ ] Metadata ACL filters  
- [ ] Rerank within latency budget  
- [ ] Grounded prompt + refuse path  
- [ ] Citation validation  
- [ ] Golden set + CI ablation  
- [ ] Index freshness SLO  
- [ ] Cost per successful answer  
- [ ] Red-team: injection in docs  
- [ ] Observability: retrieve scores, empty rate  

---

## 16. CYPHER0X9 Proof Seal

```text
PACK: RAG-SYSTEMS-DEEP
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
PROOF: RTMA labs R1–R5 · ablation-first culture
MODE: Offline-first dense systems curriculum
```

**Teach-back:** Draw the pipeline; explain why hybrid helps IDs; define faithfulness vs hit rate; design a one-factor ablation.

---

*End of pack · UC AI Free University · Retrieval is a product, not a feature.*
