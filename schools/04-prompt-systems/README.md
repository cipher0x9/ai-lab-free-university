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
