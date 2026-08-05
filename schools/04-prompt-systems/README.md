# School 04 — Prompt systems

**Job:** System prompts, contracts, eval-driven prompting.

## Beginner model
A prompt is a **job description + constraints + output contract**, not a magic spell.

## Mechanism
- System = role, safety, schema, tool policy, uncertainty language  
- User = task  
- Version prompts like dial-plans  
- Change one variable → run suite → compare pass rate & cost  
- Synthetic few-shots only in public packs  

## Lab GREEN
- [ ] Rewrite one failing idea as a contract (role + schema + uncertainty)  
- [ ] Run a curated drill from `prompts/curated/`  
- [ ] Name one injection defense  

## Failure modes
Vague success criteria · schema drift · few-shot PII leaks · injection via pasted web text.

## RTMA
**Run** prompt version id · **Trace** model+params · **Metric** pass_rate/cost · **Artifact** prompt file + eval diff.

## Interview 30 / 90
**30s:** Prompts are contracts I version and score with evals.  
**90s:** System prompts set role, safety, schema. Examples stay synthetic. Untrusted content is data, not instructions.

## Drills
See `prompts/curated/PHASE1-DRILLS.md` and UC pack seed library (sibling) for volume practice.

## Prompt evolution experiment

Compare six stages on the same fixture set: instruction → template → schema →
trusted/untrusted context policy → versioned prompt → release-gated system.

The prompt card must name goal, inputs, constraints, tools, output, uncertainty,
stop budget, success metric, and rollback id. Remove or add one block at a time.
Count a shorter prompt as an improvement only when the same tasks pass with lower
tokens, latency, or cost. Injection fixture: pasted content asks to ignore policy;
expected result is policy preserved and the attempt logged.

## 2026 prompt-system practice

- Version instructions, tool descriptions, schemas, examples, and context policy as separate assets.
- Mark untrusted retrieved text explicitly and prevent it from redefining tool authority.
- Test missing variables, conflicting instructions, multilingual inputs, and schema edge cases.
- Measure prompt-cache behavior without allowing cache optimization to reorder deterministic tools.
- Run the same golden suite across candidate prompts and models before promotion.
- Keep the last GREEN prompt bundle and an immediate rollback id beside every release.
