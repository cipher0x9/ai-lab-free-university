# Schools index

Full offline corpus (recommended): `../university/v2-UNIVERSITY.html`  
Source of truth for HTML sections: `../curriculum/corpus.py`

| ID | Path | Depth |
|----|------|-------|
| 00 | [00-orientation](./00-orientation/) | Full |
| 01 | [01-mental-models](./01-mental-models/) | Full |
| 02 | [02-local-lab](./02-local-lab/) | Full |
| 03 | [03-cloud-apis](./03-cloud-apis/) | Full |
| 04 | [04-prompt-systems](./04-prompt-systems/) | Full |
| 05 | [05-rag](./05-rag/) | Full |
| 06 | [06-agents-tools](./06-agents-tools/) | Full + Lab 02 |
| 07 | [07-voice-ai-bridge](./07-voice-ai-bridge/) | Full |
| 08 | [08-evals-safety](./08-evals-safety/) | Full + Labs 03–05 |
| 09 | [09-ship-share](./09-ship-share/) | Full |
| 10 | [10-capstone](./10-capstone/) | Full (build later) |

Also in HTML corpus (not separate md folders): **RTMA handbook · Glossary · Paths · Interview · FAQ**.

Module spine: beginner model → mechanism → lab GREEN → failure → RTMA → interview 30/90.

## Next-level module grammar

Every school now adds: simple hook → vendor-neutral invariant → named exception
→ worked implementation → forced failure → RTMA proof → teach-back.
Keep learning chunks between roughly five and nine connected ideas, then review at
**1h → 24h → 7d → 30d → 90d**.

Cross-school runway: local lab → provider adapter → prompt contract → RAG →
bounded tools/agents → eval gate → optional voice → capstone. The complete
implementation map lives in [`NEXT-LEVEL-ENGINEERING.md`](../NEXT-LEVEL-ENGINEERING.md).

## 2026 practice depth across every school

- Production RAG separates retrieval quality from answer quality and tests empty evidence.
- Eval harnesses combine deterministic checks, calibrated model graders, and human review.
- Agent traces preserve state, tool calls, approvals, corrections, cost, and stop reason.
- Local/frontier choices compare privacy, task pass rate, p95 latency, and cost per verified task.
- MCP-style tools remain typed, scoped, authenticated, observable, and revocable.
- Every release keeps a canary, rollback, and human owner for material side effects.
