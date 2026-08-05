# Judge rubric — Golden-10

Use this when a human (or future LLM judge) reviews free-form answers.

## Pass rules (Phase 1)

1. **Keyword gate** (automated): all `required_keywords` present (case-insensitive).  
2. **Meaning gate** (human): answer does not contradict `reference_answer`.  
3. **Honesty gate**: if the system used mock brain, the learner can say so.

## Severity

| Level | Meaning | Action |
|-------|---------|--------|
| Blocker | Wrong RTMA/LICC definition | Re-study School 00–01 |
| Major | Tool vs invent confusion | Re-run Lab 02 |
| Minor | Wording awkward but correct | Accept; polish later |

## What not to score

- Fancy model names  
- Long essays  
- Confidence theater  

## Future (Phase 3+)

- Citation required for UC RAG answers  
- Cost + latency budgets per item  
- Red-team injection items in separate suite  

## Calibrated judge extension

For meaning-based tasks after Phase 1:

1. Freeze a held-out set with two human labels per item.
2. Blind candidate identity and order.
3. Give the judge an observable rubric, not “is this good?”
4. Record judge model/version, prompt id, temperature, raw score, and rationale.
5. Measure exact agreement and inspect every high-risk disagreement.
6. Keep deterministic schema, citation, permission, and budget checks authoritative.
7. A named human owns release when impact or ambiguity is material.

Judge output is another trace event. It cannot approve its own side effects or
silently replace the golden reference.
