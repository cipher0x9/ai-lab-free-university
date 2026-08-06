# Embeddings & Retrieval Math

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT**

---

## 1) Embedding as a map

An embedding model maps text → vector so **nearby meanings** have **nearby vectors** (ideally). Reality: biases, domain shift, multilingual gaps.

---

## 2) Similarity

| Metric | Notes |
|--------|-------|
| Cosine | Common default |
| Dot product | Often with normalized vectors |
| L2 | Depends on space |

Always know whether vectors are normalized.

---

## 3) Index structures (intuition)

- Brute force: correct, slow  
- HNSW: graph ANN, practical default  
- IVF / PQ: compress for scale  

Trade recall vs latency. Measure both.

---

## 4) Hybrid retrieval

Lexical (BM25) + dense + fusion (RRF) often beats either alone on enterprise docs.

Lab: `06_rag_ablation.py` — keep the misses as gold.

---

## 5) Chunking is product design

- Too small: no context  
- Too large: diluted similarity  
- Parent-child: retrieve child, return parent  

Version chunker with corpus version in RTMA.

---

## 6) Eval

- Recall@k  
- nDCG  
- Answer faithfulness  
- Latency  

**Educational only · MIT**
