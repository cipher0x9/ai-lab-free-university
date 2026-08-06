# Structured Outputs & Contracts

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT · RTMA**

---

## 1) Prose is not an API

If another system must consume the answer, require a **schema**.

---

## 2) Contract stack

1. JSON Schema / typed model  
2. Validator in host (never trust model alone)  
3. Repair loop (bounded)  
4. Hard fail + metric  

---

## 3) Patterns

| Pattern | When |
|---------|------|
| JSON mode / constrained decode | High reliability need |
| Tool call as output | Actions |
| Markdown + parse | Weak; add validator |

---

## 4) RTMA

Log raw model text, parse success bool, repair count, final object hash.

---

## 5) UC analogy

Structured output is like **ISDN IE / SIP headers**: machines need fields, not poetry.

**Educational only · MIT**
