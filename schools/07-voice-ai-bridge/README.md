# School 07 — Voice AI bridge

**Job:** STT / TTS / latency — braid real-time domain skill with AI.  
**For UC/voice readers this is an unfair advantage; for others it is still a great systems lab.**

## Beginner model
Voice agents add speech recognition and synthesis on top of paths, budgets, and failure isolation you may already know from media systems.

## Mechanism
| Layer | Ask |
|-------|-----|
| Capture | Mic/path quality before blaming the model |
| STT | Partials, endpoints, jargon |
| LLM | Tools add latency |
| TTS | Streaming vs full utterance |
| Session | SIP/media or WebRTC still must complete |

Write a **latency budget**. Measure it. Do not “feel fast.”

## Lab GREEN (later phase)
- [ ] Measure speech→text→reply→speech once  
- [ ] Separate media fault vs model fault in a postmortem  
- [ ] Text agent GREEN before voice front-end  

## Caution
Contact-center AI involves law, consent, PCI/PII, workforce rules. This pack is educational — not a production authorization.

## RTMA
**Run** call scenario · **Trace** stage timestamps · **Metric** p50/p95 per stage · **Artifact** recording path + notes (no PII in public packs).

## Interview 30 / 90
**30s:** I budget STT/LLM/TTS latency and separate media faults from model faults.  
**90s:** Domain vocabulary transfers. Prove text+citations before voice. Production needs legal/vendor rails.

## Measured voice path

```text
capture/VAD → STT partial/final → dialog → LLM/tools
  → TTS first audio → transport → barge-in/human handoff
```

Budget and report p50/p95 for each stage; pair latency with transcription/domain
accuracy and handoff success. Inject noise, jargon, tool timeout, long synthesis,
and transport impairment separately. Never use one total-turn average to hide the
slow leg. Run `lab/08_voice_latency_budget.py` with fixtures, then replace them
with consented measurements and label the difference.

## 2026 multimodal practice

- Correlate audio turn, transcript, model/tool trace, synthesis, transport, and handoff ids.
- Measure time-to-first-partial, final transcript, first token, first audio, and interruption stop.
- Slice accuracy by language, accent, domain term, noise condition, and device path.
- Preserve “unclear input” uncertainty instead of converting it into a confident action.
- Test barge-in, double-talk, tool delay, reconnect, and safe human handoff independently.
- Minimize recordings, capture consent, redact PII, and provide text/caption fallback.
