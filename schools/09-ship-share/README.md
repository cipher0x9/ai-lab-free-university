# School 09 — Ship & share (safely)

Learn how to **share learning work** without leaking secrets or confusing friends.

## Goals

- Publish only educational material
- Prefer small, browser-friendly packs
- Never commit API keys, customer data, or private chats
- Use a human gate before any public post

## Practice

1. List what is safe to share vs what must stay private  
2. Write a one-page “how to open this pack” for a non-git friend  
3. Check a zip opens offline in Chrome or Safari  
4. Name one falsifier: what would make this share unsafe?

## Related in this repo

- [SECURITY.md](../../SECURITY.md)  
- [HOW-TO-GET.md](../../HOW-TO-GET.md)  
- [SIBLINGS.md](../../SIBLINGS.md)  
- Sibling UC Lab: https://github.com/cipher0x9/uc-lab-free-university  

## RTMA check

| | |
|--|--|
| **Run** | Did you open the shared HTML yourself offline? |
| **Trace** | Download path a stranger will actually use |
| **Metric** | Zip size + time-to-first-page |
| **Artifact** | Short HOW-TO note next to the zip |

Be kind. Share freely for learning. Lab safely.

## Release ladder

```text
local GREEN → rebuilt offline HTML → structural/link checks
  → Chrome/Safari/Edge/Firefox smoke → clean-room stranger test
  → human approval → publish → download/read-back → rollback ready
```

Report SHIPPED only after the artifact exists at the target; report VERIFIED only
after a fresh consumer path opens it and matches expected bytes/content. A render,
notification, or draft is not shipment. Include release tag, hash, file size,
browser matrix, falsifier, and prior-version rollback link.

## 2026 release practice

- Generate a software bill of materials or dependency inventory for runnable packs.
- Pin build inputs and record artifact hash, size, license, provenance, and verification command.
- Run secret, unsafe-link, schema, Python, and offline HTML checks before packaging.
- Test the download in a clean profile with no author cache or local absolute paths.
- Separate STRUCTURE_COMPLETE, TECHNICALLY_VERIFIED, LEARNER_GREEN, and published state.
- Keep the prior verified artifact and document one-command or one-click rollback.
