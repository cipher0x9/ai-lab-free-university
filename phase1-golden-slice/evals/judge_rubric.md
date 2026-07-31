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
