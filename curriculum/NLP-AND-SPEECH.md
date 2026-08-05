# NLP and Speech
## CYPHER0X9 · UC AI Free University · Master Campus Curriculum Pack
### Brand: cipher0x9 · MIT · RTMA proof · Offline-first

> **Course code:** NLP-SP-401 · **Level:** Intermediate→Advanced  
> **Outcome:** Tokenization → embeddings → LMs → classical NLP tasks → ASR/TTS → voice agent pipelines with latency budgets.

---

## 0. Language as Engineering Material

```text
Audio ⇄ Text ⇄ Tokens ⇄ Vectors ⇄ Models ⇄ Actions
```

| Modality | Primary errors |
|----------|----------------|
| Text | ambiguity, entity, style |
| Speech | noise, accents, latency |
| Both | compounding pipeline error |

---

## 1. Tokenization

### 1.1 Algorithms

| Method | Idea | Notes |
|--------|------|-------|
| Word | split whitespace | OOV hell |
| Char | per character | long seq |
| BPE | merge frequent pairs | GPT-style |
| WordPiece | similar, likelihood | BERT-style |
| Unigram LM | prune subwords | SentencePiece |
| Byte-level BPE | bytes as base | multilingual robust |

### 1.2 Why tokenization matters

- Compression → effective context length  
- Multilingual fairness (over-tokenization tax)  
- Code / math performance  
- Privacy (token tricks rarely hide secrets)  

```python
# Conceptual checks
assert tokenizer.encode("hello") == ids
assert tokenizer.decode(ids) == "hello"  # may normalize spaces
print("fertility", len(ids) / n_words)
```

### 1.3 Special tokens

BOS/EOS, PAD, UNK, chat role tokens, tool tokens — must match training.

---

## 2. Embeddings

### 2.1 Static (Word2Vec, GloVe)

One vector per word type; no context.

### 2.2 Contextual (ELMo, BERT, …)

Vector depends on sentence; solves bank/river vs bank/finance.

### 2.3 Sentence / document embeddings

Mean pool, CLS, or dedicated contrastive sentence models for retrieval.

### 2.4 Similarity pitfalls

- Cosine ≠ truth  
- Length/style bias  
- Domain shift from general embedders  

---

## 3. Language Models

### 3.1 Types

| Type | Training | Use |
|------|----------|-----|
| Masked LM | predict mask | understanding, NER fine-tune |
| Causal LM | next token | generation, assistants |
| Seq2seq | enc-dec | translation, summarization |
| Encoder-only | bidirectional | classification |

### 3.2 Decoding (generation)

| Strategy | Behavior |
|----------|----------|
| Greedy | deterministic, dull/local |
| Beam | better for short structured |
| Temperature sampling | diversity |
| Top-k / top-p | truncate tail |
| Min-p | modern alternative |
| Constrained | grammar/JSON |

### 3.3 Evaluation classic + modern

- Perplexity  
- BLEU/ROUGE (overlap)  
- Task accuracy  
- Human prefs / LLM judge  
- Toxicity / bias suites  

---

## 4. Core NLP Tasks

### 4.1 Text classification

Intents, sentiment, toxicity, topic.

```text
baseline: TF-IDF + linear
strong: fine-tuned encoder or LLM few-shot/tools
```

### 4.2 NER & information extraction

```text
BIO tagging → entity spans → link to KB (entity linking)
```

Metrics: entity-level F1 (not only token F1).

### 4.3 Parsing & structure

Dependency/constituency less central in LLM era, still useful for grammar tools and linguistics products.

### 4.4 Summarization

- Extractive vs abstractive  
- Faithfulness critical (see RAG pack)  
- Length control  

### 4.5 Translation

- Supervised parallel data historically  
- Multilingual LLMs few-shot  
- Eval: BLEU + COMET-like + human; domain glossaries  

### 4.6 Dialogue

State tracking, policy, NLG — now often LLM + tools + memory; still need state machines for regulated flows.

---

## 5. Classical → Neural Timeline (teachable)

```text
Rules → Stats (n-gram, HMM, CRF) → Word vectors → RNN/seq2seq
  → Attention → Transformer → Pretrain/finetune → LLMs + tools
```

**CRF + BIO** still a great teaching model for structured prediction.

---

## 6. ASR — Automatic Speech Recognition

### 6.1 Pipeline evolution

```text
Classic: audio → features (MFCC/filterbank) → acoustic model → lexicon → LM → text
Modern end-to-end: audio → encoder → decoder/CTC/RNN-T → text
Whisper-style: encoder-decoder transformer multilingual multi-task
```

### 6.2 Metrics

\[
\mathrm{WER} = \frac{S+D+I}{N}
\]

Also: CER, timestamp quality, proper noun accuracy, inverse text normalization (ITN) quality.

### 6.3 Hard conditions

- Noise, reverb, overlap (cocktail party)  
- Accents, code-switching  
- Domain jargon / rare names → biasing / hotwords  
- Far-field mics  

### 6.4 Streaming ASR

Partial hypotheses with endpointing; trade delay vs accuracy.

```text
partial: "I need to re..."
final:   "I need to reset my router."
```

### 6.5 Practical integration

```python
def transcribe(audio_pcm16, sample_rate=16000):
    # normalize → optional VAD → ASR model → ITN → PII redact?
    return {"text": text, "segments": segments, "confidence": conf}
```

---

## 7. TTS — Text to Speech

### 7.1 Stack

```text
text → normalize/SSML → linguistic feats → acoustic model → vocoder → audio
Neural end-to-end / latent: text → mel/codec tokens → waveform
```

### 7.2 Quality dimensions

| Dimension | Notes |
|-----------|-------|
| Naturalness | MOS listening tests |
| Intelligibility | task comprehension |
| Latency | first byte audio |
| Prosody | emotion, emphasis |
| Speaker similarity | cloning ethics! |
| Robustness | numbers, URLs, code |

### 7.3 SSML / control

Breaks, rate, pitch, spell-out for IDs — essential for IVR/contact center quality.

### 7.4 Ethics

- Voice clone consent  
- Deepfake misuse  
- Disclosure when bot speaks  

---

## 8. Voice Pipelines (product)

### 8.1 Full duplex conceptual

```text
Mic → VAD → ASR (streaming)
  → NLU / LLM / agent tools
  → response text
  → TTS stream → speaker
  → barge-in handling
```

### 8.2 Latency budget (example contact-center style)

| Stage | p50 target | Notes |
|-------|------------|-------|
| VAD endpoint | 200–400ms | aggressiveness trade |
| ASR finalize | 200–600ms | streaming partials earlier |
| LLM TTFT | 300–800ms | SLM helps |
| Tools | 0–2000ms | cache |
| TTS first audio | 100–300ms | stream |
| **User perceived** | **< ~1.5–2.5s** | context dependent |

### 8.3 Barge-in

User interrupts TTS → cancel synthesis → re-ASR. Hard real-time state machine.

### 8.4 Telephony realities (CYPHER0X9 signal temple adjacent)

- Codecs (G.711, Opus), packet loss  
- Echo cancellation, AGC  
- SIP / WebRTC transport  
- E911 / compliance recording rules  
- **THE CALL MUST ALWAYS CONNECT** — fallbacks over cleverness  

```text
Fallback ladder:
primary ASR → backup ASR → DTMF menu → human agent
primary LLM → scripted template → human
```

---

## 9. Speech-to-Speech & Multimodal Voice

### 9.1 Cascaded vs end-to-end

| Cascaded ASR→LLM→TTS | E2E speech-speech |
|----------------------|-------------------|
| Debuggable, modular | lower latency potential |
| Error compounding | less text inspectability |
| Easy tool use in text | tools harder |

Hybrid often wins: cascaded with streaming + partial processing.

### 9.2 Emotion / style

Prosody carry-over is open research/product space; beware stereotyping.

---

## 10. Safety, Privacy, Compliance

- Call recording consent  
- PII in transcripts (redact storage)  
- Voice biometrics legal basis  
- Prompt injection via speech (“ignore instructions”) — same defenses  
- Child data heightened rules  

---

## 11. Multilingual NLP & Speech

| Issue | Mitigation |
|-------|------------|
| Token tax | better multilingual tokenizers |
| Code-switch | mixed training data |
| ASR language ID | LID front-end |
| Eval gap | per-language slices |

Never report only English metrics for global products.

---

## 12. Building Blocks Code Sketches

### 12.1 NER fine-tune loop (conceptual)

```python
# encode tokens → align wordpiece labels → CE loss on label ids → entity F1 eval
```

### 12.2 Voice agent turn

```python
def handle_turn(audio_stream, agent, tts):
    text, asr_meta = asr.stream_to_final(audio_stream)
    text = pii_redact(text)
    result = agent.run(text, budgets=Budgets(max_turns=4, max_wall_s=8))
    audio_out = tts.stream(result.say)
    return audio_out, result.trace
```

---

## 13. RTMA Labs

### Lab N1 — Tokenizer fertility

- **Run:** compare two tokenizers on EN/code/other lang sample  
- **Metric:** tokens/word  
- **Artifact:** `n1_fertility.csv`

### Lab N2 — Classification baseline vs transformer

- **Run:** TF-IDF vs fine-tune  
- **Metric:** macro-F1 + latency  
- **Artifact:** `n2_clf.md`

### Lab N3 — WER stress

- **Run:** ASR on clean vs noisy set  
- **Metric:** WER delta; proper noun subset  
- **Artifact:** `n3_wer.json`

### Lab N4 — Voice latency budget

- **Run:** instrument ASR/LLM/TTS timings on 20 utterances  
- **Metric:** p50/p95 per stage  
- **Artifact:** `n4_latency.csv`

### Lab N5 — Speech injection

- **Run:** spoken jailbreak attempts  
- **Metric:** ASR  
- **Artifact:** `n5_voice_redteam.md`

---

## 14. Interview Sketch: Voice Support Agent

1. Streaming ASR + endpointing  
2. LLM with tools (order, KB) under 8s budget  
3. TTS barge-in  
4. Human handoff with full transcript  
5. Eval: task success, WER on jargon, latency, safety  
6. Recording retention policy  

---

## 15. Production Checklist

- [ ] Tokenizer/model template parity  
- [ ] Per-language metrics  
- [ ] ASR hotwords for domain  
- [ ] TTS normalization for IDs/URLs  
- [ ] Latency budgets measured  
- [ ] Barge-in / interrupt tested  
- [ ] PII redaction path  
- [ ] Fallback to human  
- [ ] RTMA on pipeline changes  

---

## 16. CYPHER0X9 Proof Seal

```text
PACK: NLP-AND-SPEECH
OWNER: cypher0x9 / cipher0x9
LICENSE: MIT campus materials
PROOF: RTMA labs N1–N5
SIGNAL: voice pipelines · connect first · prove quality
```

**Teach-back:** BPE vs words; WER definition; cascaded voice pipeline latency; when not to use pure E2E speech-speech.

---

*End of pack · UC AI Free University · Language in, action out — with traces.*
