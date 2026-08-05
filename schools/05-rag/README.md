# School 05 — RAG

**Job:** Chunking, embeddings, citations. Fail closed without evidence.

## Beginner model
RAG = open the right binder, then answer — with page numbers (citations).

## Mechanism
1. Chunk with versions recorded  
2. Embed + index  
3. Retrieve top-k  
4. Generate **only** from evidence  
5. Cite paths/ids  
6. Measure retrieval separately from generation  

## Domain braid
Voice engineers: use **UC Lab Free University** as first corpus.  
Others: public standards, scrubbed notes, open textbooks.

## Lab GREEN (Phase 3 shape)
- [ ] Index a small markdown folder  
- [ ] 20 citation-required questions  
- [ ] Empty retrieval → “not in corpus”  

## Failure modes
Wrong neighbors · stale index · citation theater · overstuffed context.

## RTMA
**Run** query · **Trace** retrieved chunk ids · **Metric** hit rate · **Artifact** answer+citations.

## Interview 30 / 90
**30s:** Retrieve first, answer with citations, fail closed if empty.  
**90s:** Pin embedder/chunker versions. Separate retrieval metrics. Domain corpora beat random scrapes for trust.

## Production ladder and ablation

```text
keyword → chunks+embeddings → hybrid retrieval → reranking
  → ACL/freshness filters → citation eval → monitored index
```

Run `lab/06_rag_ablation.py`, then vary chunk size, overlap, retriever, top-k, and
reranker one at a time. Measure retrieval hit rate/recall@k before answer quality.
Every chunk carries source id, location, version, policy, and timestamp. Every
citation resolves. Empty or unauthorized evidence returns an honest no-answer.

**Falsifier:** a polished answer with the wrong retrieved source is RED.

## 2026 production-RAG practice

- Version parser, chunker, embedder, index, reranker, corpus, and access policy together.
- Compare lexical, dense, hybrid, and reranked retrieval on the same query set.
- Track recall@k or hit rate before judging faithfulness, citation accuracy, and answer utility.
- Exercise deleted, stale, conflicting, multilingual, and unauthorized evidence paths.
- Observe ingestion lag, partial-index failures, cache staleness, and reindex rollback time.
- Release only when every citation resolves and empty evidence produces a calibrated no-answer.
