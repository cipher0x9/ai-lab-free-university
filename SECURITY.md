# Security

## Reporting

If you find a security issue in this learning pack, open a private security advisory on GitHub or contact the maintainer via the GitHub profile:

**[@cipher0x9](https://github.com/cipher0x9)** · display name **CYPHER0X9**

## Safe use of this repo

- Educational AI lab curriculum, labs, and prompts — **not** a hosted model service.
- Do **not** paste production credentials, customer data, private captures, or PII into issues, PRs, or forks.
- Phase-1 labs are designed to run **without** cloud keys.
- Treat automation prompts as **read-only by default**; require human approval for side effects (email, post, spend, delete).
- Lab safely. Pin official vendor documentation before production.

## Maintainer / contributor hygiene

- Enable 2FA on GitHub
- Prefer SSH keys or fine-scoped PATs
- Never commit `.env`, tokens, or private keys
- Rotate any credential that appears in a screenshot or log

## Model weights

Do not commit model blobs (`.gguf`, large bin files). Document pull commands instead.

## Links (canonical)

| | |
|--|--|
| Profile | https://github.com/cipher0x9 |
| This repo | https://github.com/cipher0x9/ai-lab-free-university |
| Sibling UC | https://github.com/cipher0x9/uc-lab-free-university |
| Hub | https://linktr.ee/cyphermonkey |

## Agent and RAG threat boundary

| Boundary | Abuse case | Required control | Proof |
|---|---|---|---|
| Untrusted content → prompt | injection overrides policy | separate data/instructions | adversarial fixture |
| Model → tool | malformed or excessive call | schema + allowlist + budgets | denied-call trace |
| Tool → outside world | message/delete/spend | named human approval | approval id |
| Query → corpus | unauthorized retrieval | ACL before ranking | forbidden-source test |
| Chunk → answer | citation theater | resolvable source ids | citation precision |
| Agent → loop | runaway turns/cost | max turns/time/spend | stop event |
| Update → release | silent regression | versioned eval gate | before/after scorecard |

Controlled sabotage and agentic-misalignment research should be treated as a
reason to test permissions and oversight, not as proof of a real-world autonomous
attack. Run red-team scenarios only in owned, isolated labs. Never give a learning
agent live credentials merely to make the demo feel realistic.

Production-readiness fixtures: `phase1-golden-slice/evals/production_readiness.json`.
