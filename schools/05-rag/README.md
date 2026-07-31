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
