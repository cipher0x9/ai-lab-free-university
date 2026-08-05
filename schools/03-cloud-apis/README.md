# School 03 — Cloud APIs

**Job:** Keys vault, rate limits, structured output, cost control.  
**Audience:** everyone who will eventually leave pure-local practice.

## Beginner model
Cloud = rented super-brain with a meter and a data boundary.  
Treat API keys like production trunk credentials.

## Mechanism
1. Secrets only in env / vault — ship `.env.example` empty  
2. Prefer **structured outputs** + validators  
3. Track tokens and **$/week**  
4. Backoff on 429; circuit-break on burn  
5. Written burst policy (what may leave the machine)

## Lab GREEN
- [ ] Explain why Phase 1 needs zero keys  
- [ ] Draft a monthly budget + kill-switch  
- [ ] List three fields you would log (no secrets) in an RTMA cloud artifact  
- [ ] Read `.env.example`

## Failure modes
| Failure | Detection |
|---------|-----------|
| Key in git | secret scan |
| Bill shock | budget alert |
| Silent model swap | pin model ids + evals |
| PII to public model | policy + redaction |

## RTMA
**Run** API call · **Trace** request id · **Metric** tokens+cost · **Artifact** receipt JSON (redacted).

## Interview 30 / 90
**30s:** Cloud keys are production credentials; I pin models, validate structure, and track cost.  
**90s:** Local-first practice; cloud under policy. Structured outputs validated. Budgets have kill-switches. This free pack starts key-free so anyone can enroll.

## Status
Full teaching module. Concrete multi-provider labs land after Phase 1 GREEN.

## Adapter-first migration

Normalize application fields—text, tool calls, usage, provider/model/request id—but
preserve provider-specific errors in Trace. Put timeout, retry, rate-limit, and
budget policy outside the prompt. A migration is GREEN only when the same golden
set passes and the quality/latency/cost/safety delta is recorded.

Provider practice lanes: Vertex AI, OpenAI, Anthropic, and xAI. These names are
implementation examples, not the architecture. Model ids, features, prices, data
terms, and quotas are release-sensitive; verify official docs at build time.

Rollback: pin the previous adapter/model configuration and prove the switch-back path.

## 2026 cloud-runtime practice

- Capture provider, model snapshot, request id, region, timeout, retry count, tokens, and cost.
- Use exponential backoff only for retryable failures and keep the whole request under one deadline.
- Add idempotency or deduplication before retrying any side-effecting operation.
- Route canaries through the candidate model while the known-good route remains available.
- Evaluate data retention, residency, and logging controls before sending sensitive content.
- Report blended cost per verified task; a cheap failed call is not an efficiency win.
