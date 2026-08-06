# Voice AI Production Bridge

**CYPHER0X9 · AI Lab Free University · curriculum pack · MIT**  
**Twins:** RTMA (AI) + LICC (UC) · **Spine:** THE CALL MUST ALWAYS CONNECT

---

## 1) Why voice is harder than chat

| Chat | Voice |
|------|-------|
| Human waits | Human hears silence as failure |
| Edit freely | One-way time |
| Text tokens | STT error + TTS artifact |
| Retry cheap | Retry awkward |

---

## 2) Reference pipeline

```text
Mic → transport → STT → (LLM + tools) → TTS → transport → Speaker
                 ↑ barge-in / endpointing / partials
```

Measure **each stage** (lab 08). Never report only "end-to-end vibes."

---

## 3) Fail-soft rules

1. If LLM times out → play hold / queue / human  
2. If STT confidence low → confirm critical fields  
3. If tools fail → do not invent CRM state  
4. If TTS fails → fallback prompt / agent whisper  

**UC spine applies:** revenue and safety collapse when the call dies.

---

## 4) Contact center patterns

- Agent assist (not autopilot first)  
- Post-call summary with PII scrub  
- IVR intent + handoff with context  
- Supervised automation for narrow intents  

---

## 5) LICC × RTMA joint ticket

| | UC LICC | AI RTMA |
|--|---------|---------|
| Path | SIP/media legs | STT/LLM/TTS stages |
| ID | Call-ID | run_id / trace_id |
| Counter | ASR/NER/MOS | WER/latency/$ |
| Capture | pcap / CDR | stage JSON / audio redacted |

---

## 6) Safety

- Record only with policy  
- Never train on unredacted prod without process  
- Human for irreversible actions  

---

## 7) Sibling

Deep SIP/SBC/CC: [UC Lab Free University](https://github.com/cipher0x9/uc-lab-free-university)

**Educational only · MIT**
