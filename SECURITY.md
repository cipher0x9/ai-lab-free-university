# Security

## Reporting

If you find a security issue in this learning pack, open a private security advisory on GitHub (when the public repo exists) or contact the maintainer via the GitHub profile [@CYPHER0X9](https://github.com/CYPHER0X9).

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
