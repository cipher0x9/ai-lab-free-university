# Curated prompts

Small, high-signal drills for Phase 1.

| File | Use |
|------|-----|
| `PHASE1-DRILLS.md` | Daily mentor drills |

## Full seed library (already exists — do not rebuild)

In the UC free share pack (sibling folder):

`UC-LAB-FREE-SHARE/prompts/02-ai-ml-future-lab/`

- `PROMPTS-EXPANDED-LIBRARY.md` — 1000 seeds  
- `PROMPTS-MAC-MINI-LAB.md`  
- `PROMPTS-AGENTS-AND-TOOLS.md`  
- `PROMPTS-EVAL-AND-SAFETY.md`  
- `NEW-SESSION-VISION-HANDOFF.md`  

**Rule:** never delete that tree; AI Lab Free University may copy seeds later into releases.

## Prompt-system contract

Each new prompt should declare: goal, trusted inputs, untrusted inputs,
constraints, tool schemas, approval class, output schema, uncertainty behavior,
stop budget, evaluator, and rollback id. Version the contract beside the eval
result. Change one variable, rerun the same suite, and retain failed candidates as
learning evidence when safe.

Evolution: instruction → template → structured contract → context policy →
versioned suite → release gate.
