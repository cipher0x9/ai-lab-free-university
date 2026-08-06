# Agent Evals Advanced

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT · RTMA**

---

## 1) Unit tests are not enough

Agents fail by **trajectory**: wrong tool, right answer by cheat, infinite loop, unsafe action.

---

## 2) Eval layers

| Layer | Measures |
|-------|----------|
| Tool choice | Correct tool selected |
| Args | Schema-valid + semantically right |
| Trajectory | Order / necessity |
| Final answer | Task success |
| Safety | Refusals / injections |
| Cost/latency | Budgets |

---

## 3) Golden fixtures

Start with 10, grow to 25–100 domain cases. Keep hard negatives.

Repo fixtures: `phase1-golden-slice/evals/`.

---

## 4) Judge models

LLM-as-judge needs:

- Rubric  
- Blindness to brand  
- Spot-check by humans  
- Known bias log  

---

## 5) Gate for release

```text
eval GREEN + safety GREEN + budget GREEN + human OK → release
```

Anything less is a demo, not a deploy.

**Educational only · MIT**
