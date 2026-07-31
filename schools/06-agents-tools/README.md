# School 06 — Agents & tools

**Job:** Tool schema, handoffs, memory, permissions.

## Beginner model
An agent is a **loop with privileges**, not a personality.

## Mechanism (Lab 02 already ships this)
1. Goal in  
2. Plan tool calls (schema)  
3. Permission check  
4. Execute  
5. Synthesize from tool results when facts matter  
6. RTMA artifact out  

## Tools in this pack
- `calc` — exact arithmetic  
- `glossary_lookup` — fixed local definitions  

## Never-without-approval
Email/post · delete outside sandbox · spend money · message customers · force-push main.

## Lab GREEN
- [ ] Lab 02 passes  
- [ ] Explain tool chain from an artifact JSON  
- [ ] Name three side effects that need humans  

## Failure modes
Invented tool results · missing schemas · multi-agent without owner · permission bypass via prompt.

## RTMA
**Run** goal · **Trace** each tool request/result · **Metric** success count/latency · **Artifact** chain JSON.

## Interview 30 / 90
**30s:** Privileged loops; schema tools; default-deny side effects.  
**90s:** Exact facts via tools; shared trace ids; critic agents cannot self-escalate permissions.
