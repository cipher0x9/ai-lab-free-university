#!/usr/bin/env python3
"""Full curriculum corpus for AI Lab Free University.

General audience free pack. Mentor tone. Evidence-first (RTMA).
"""

from __future__ import annotations

META = {
    "title": "AI Lab Free University",
    "version": "v2",
    "tagline": "From confused builder → confident local + cloud AI operator",
    "subtitle": "Free · offline-friendly · evidence-first · for everyone",
    "author": "CYPHER0X9",
    "license": "MIT — educational only, no warranty",
    "sibling": "UC Lab Free University",
    "sibling_url": "https://github.com/cipher0x9/uc-lab-free-university",
    "linktree": "https://linktr.ee/cyphermonkey",
    "repo_planned": "ai-lab-free-university",
}

# Each section: id, school, title, level, body (markdown-ish plain), tags, green, interview30
# body uses simple paragraphs separated by \n\n; lists with "- " lines


def S(id_: str, school: str, title: str, level: str, body: str, tags: str = "", green: str = "", interview30: str = "") -> dict:
    builder_extension = f"""

### Builder lens · learn while building, prove as you go

Explain **{title}** in plain language. Build the smallest safe example. Change one
variable, compare the before/after result, and keep an RTMA artifact that another
learner can reproduce.

### Review ladder

Revisit at **1 hour → 24 hours → 7 days → 30 days → 90 days**. At each
review: state the general rule, name one exception, teach one worked example, and
write the observation that would falsify your claim.

### Extended proof card

| Field | Capture |
|-------|---------|
| Run | Exact command, input, model/fixture version |
| Trace | Ordered steps, tool calls, approvals, errors |
| Metric | Quality + latency + cost + safety signal |
| Artifact | Durable local file and reproduction note |

### 2026 production practice

- Hold the task and evaluator constant while changing one system variable.
- Compare local and frontier routes on privacy, pass rate, p95, and cost per verified task.
- Separate retrieval quality from answer quality; test stale, empty, and unauthorized evidence.
- Trace agent state, tool calls, approvals, corrections, assertions, and stop reason.
- Combine deterministic checks, calibrated model graders, and named human review.
- Pin model, prompt, data, index, tool, and policy versions; keep the last GREEN rollback.
"""
    return {
        "id": id_,
        "school": school,
        "title": title,
        "level": level,
        "body": body.strip() + builder_extension.rstrip(),
        "tags": tags,
        "green": green,
        "interview30": interview30,
        "review_schedule": "1h, 24h, 7d, 30d, 90d",
        "proof_contract": "baseline → one variable → delta → decision → rollback",
    }


SCHOOLS = [
    {"id": "00", "name": "Orientation", "job": "Map, honesty, safety, hardware reality"},
    {"id": "01", "name": "Mental models", "job": "Tokens, context, probability, failure modes"},
    {"id": "02", "name": "Local lab", "job": "Mac Mini / laptop local models, catalog, hygiene"},
    {"id": "03", "name": "Cloud APIs", "job": "Keys, rate limits, structured output, cost"},
    {"id": "04", "name": "Prompt systems", "job": "Contracts, eval-driven prompting"},
    {"id": "05", "name": "RAG", "job": "Chunking, embeddings, citations"},
    {"id": "06", "name": "Agents & tools", "job": "Schema, handoffs, permissions"},
    {"id": "07", "name": "Voice AI bridge", "job": "STT/TTS/latency — domain superpowers"},
    {"id": "08", "name": "Evals & safety", "job": "Red team, injection, PII, override"},
    {"id": "09", "name": "Ship & share", "job": "Small packs, GitHub Release, free license"},
    {"id": "10", "name": "Capstone", "job": "Personal domain coach with citations"},
    {"id": "RT", "name": "RTMA handbook", "job": "Evidence grammar for every lab"},
    {"id": "GL", "name": "Glossary", "job": "Plain definitions operators actually use"},
    {"id": "PX", "name": "Paths", "job": "Study paths by audience"},
    {"id": "IV", "name": "Interview bank", "job": "30s / 90s answers that sound real"},
    {"id": "FQ", "name": "FAQ", "job": "Honest answers, no hype"},
]


SECTIONS: list[dict] = []

# ── RTMA ──────────────────────────────────────────────────────────────
SECTIONS += [
    S("RT-01", "RT", "What is RTMA?", "beginner", """
RTMA is the evidence habit of this university:

- **Run** — the exact command, notebook cell, or agent task you executed
- **Trace** — logs, request IDs, tool-call chain, spans
- **Metric** — latency, tokens, cost, accuracy, pass rate, error rate
- **Artifact** — a file you can reopen: output, report, screenshot, checklist

If you cannot produce those four, you do not yet *know* the lesson — you only watched it.

**Falsifier first:** what observation would kill “the model is smart enough”?
""", "rtma evidence", "Explain RTMA cold in under 20 seconds.", "RTMA is Run, Trace, Metric, Artifact — proof over vibes."),

    S("RT-02", "RT", "RTMA maps to UC LICC", "beginner", """
If you come from voice / Unified Communications troubleshooting, you already know **LICC**:

| UC LICC | AI RTMA | Shared idea |
|---------|---------|-------------|
| Leg | Run | Which path did you actually take? |
| ID | Trace | Identifiers and chain of custody |
| Counter | Metric | Numbers that survive debate |
| Capture | Artifact | Something you can reopen later |

You are not starting from zero. You are transferring operator discipline into a new domain.
""", "licc uc bridge", "Map all four pairs without notes."),

    S("RT-03", "RT", "How to write an RTMA artifact", "intermediate", """
Minimum useful artifact (JSON or markdown):

1. `run_id` and timestamp  
2. command / goal  
3. ordered events (trace)  
4. metrics dict  
5. paths to outputs  
6. status: ok | fail | partial  
7. falsifier note  

In this pack, labs write JSON under `phase1-golden-slice/artifacts/`. Open one after every lab until it feels normal — like saving a PCAP path after a voice incident.
""", "artifact json"),

    S("RT-04", "RT", "Common RTMA failures", "intermediate", """
- **Run without Trace** — “I tried something” with no log  
- **Metric theater** — pretty dashboards, no decision  
- **Artifact rot** — files nobody can find next week  
- **Mock denial** — pretending a mock brain was a real model  
- **Pass by vibes** — skipped eval because the demo felt good  

Fix: make GREEN checklists require artifacts, not feelings.
""", "failure honesty"),
]

# ── 00 Orientation ────────────────────────────────────────────────────
SECTIONS += [
    S("00-01", "00", "Who this university is for", "beginner", """
**Primary audiences (all welcome):**

1. **Domain experts new to AI** (voice, networking, healthcare, finance, ops) — you know hard systems; AI is another system with failure modes.  
2. **Builders on local machines** (Mac Mini, Linux laptop, Windows WSL) who want private, measurable practice.  
3. **Engineers shipping agents** who need tools, evals, and permissions — not demo theater.  
4. **Students and career switchers** who want a free, offline-friendly map without guru noise.

You do **not** need a PhD. You do need honesty, a terminal, and willingness to write evidence.
""", "audience general", "Name three audience types and which one you are."),

    S("00-02", "00", "Who built this and why free", "beginner", """
Built by **CYPHER0X9** — roughly a decade in Cisco / Unified Communications, now an AI learner-builder on Apple Silicon.

The sibling free pack is **UC Lab Free University** (public on GitHub). The same free-share discipline applies here:

- educational only  
- browser-friendly defaults  
- no secrets in git  
- depth in modules, not one hostile mega-file  

If this helps even one person, it was worth sharing.
""", "author free share"),

    S("00-03", "00", "Promise of the curriculum", "beginner", """
After guided practice, a serious learner can:

1. Run a **local** model safely  
2. Call a **cloud** model with structure and cost control  
3. Build a small **agent** with permissions + human gates  
4. Run **evals** that catch hallucinations  
5. Wire AI to **their domain** with citations  
6. Ship a **free pack** others can open offline  

Phase 1 proves the path works end-to-end with a golden vertical slice.
""", "promise outcomes"),

    S("00-04", "00", "Honesty counters (weekly)", "beginner", """
Every week, answer yes/no:

1. Did I write an **artifact**, or only feel smarter?  
2. Did I record any **metric** (ms, pass rate, cost)?  
3. Did I invent something a **tool** should have produced?  
4. Did any **secret** almost land in a file or chat export?  
5. Did I confuse **mock** brain with a real model?  
6. Could a friend reproduce my Run from the notes alone?

Three or more “no” answers → slow down, re-run the golden slice.
""", "honesty counters"),

    S("00-05", "00", "Safety baseline for all learners", "beginner", """
Non-negotiables in this free pack:

- No API keys or `.env` in git  
- No customer data / private audio / PII in public artifacts  
- No autonomous email, social posts, or money moves without human approval  
- Educational only — **no warranty**; pin official vendor docs for production  
- Prefer least-privilege tools  

Your personal policy can be stricter. It should not be looser.
""", "safety keys pii", "List four non-negotiables."),

    S("00-06", "00", "Hardware reality check", "beginner", """
You do **not** need a data center.

| Setup | Good for |
|-------|----------|
| Any laptop + mock brain | Learning RTMA and evals today |
| Laptop + Ollama small model | Private local generation |
| Mac Mini M-series always-on | Home lab “PBX for brains” |
| Cloud API key | Capability burst, structured outputs |

Phase 1 labs run with **stdlib Python only** and an honest mock if no local server is up. Installs never block learning.
""", "hardware mac mini ollama"),

    S("00-07", "00", "How modules are structured", "beginner", """
Every serious module aims for the same spine:

1. **Beginner model** — plain language + analogy  
2. **Mechanism** — how it actually works  
3. **Lab GREEN** — checklist with proof  
4. **Failure modes** — how it breaks + detection  
5. **RTMA** — run/trace/metric/artifact for the lesson  
6. **Interview 30/90** — say it out loud  

If a page is only hype or only math, it is incomplete for this university.
""", "module spine"),

    S("00-08", "00", "Phase map (what ships when)", "beginner", """
| Phase | Deliverable |
|-------|-------------|
| 0 | Vision, RTMA, schools |
| 1 | Golden slice: hello → tool → eval → GREEN + offline HTML |
| 2 | Local lab OS + cloud cost hygiene |
| 3 | Agents + domain RAG with citations |
| 4 | Public GitHub Release free share |

You can study later schools early for orientation — but **prove Phase 1** before claiming mastery.
""", "phases"),

    S("00-09", "00", "Non-goals (first free pack)", "beginner", """
Explicitly **not** trying to be:

- A 760MB single HTML that freezes browsers  
- A wrapper around every model API on earth  
- A crypto / Web3 pivot  
- A replacement for official OpenAI / Anthropic / Google / Apple docs  
- Autonomous agents that post or email without approval  
- “AGI course” cosplay  

Clarity is a feature.
""", "nongoals"),

    S("00-10", "00", "Golden path — start tonight", "beginner", """
```bash
cd AI-LAB-FREE-SHARE
open university/v2-UNIVERSITY.html   # or v1-SLICE.html
bash scripts/verify_slice.sh
```

Then:

1. Open one JSON under `phase1-golden-slice/artifacts/`  
2. Open `reports/golden10-report.md`  
3. Tick GREEN only for what you can explain cold  
4. Read School 01 Mental models  

Welcome. Go slow. Keep evidence.
""", "start path verify"),
]

# ── 01 Mental models ──────────────────────────────────────────────────
SECTIONS += [
    S("01-01", "01", "Models predict tokens, not truth", "beginner", """
A large language model predicts likely next **tokens** (text chunks) given context.

That produces fluent language. Fluency is **not** a truth guarantee.

Operator translation: a call can show “connected” while media is broken. Status lights lie; captures don’t.
""", "tokens fluency hallucination"),

    S("01-02", "01", "What is a token?", "beginner", """
A **token** is a chunk of text the model reads or writes — sometimes a word, sometimes part of a word, sometimes punctuation.

Rough intuition (not a law): English prose often averages ~0.75 words per token. Code is denser.

Why you care: **billing**, **context limits**, and **latency** all track tokens.
""", "token definition"),

    S("01-03", "01", "Context window = budget", "beginner", """
The **context window** is the token budget for one request (input + output share it).

When you overflow:

- early instructions may be dropped  
- the model “forgets” constraints  
- costs jump if you keep stuffing files  

UC analogy: bandwidth / session limits. You engineer for the budget; you do not wish it larger mid-call.
""", "context window budget"),

    S("01-04", "01", "Temperature without mysticism", "beginner", """
**Temperature** (and related sampling knobs) change how randomly the model picks among likely tokens.

- Lower → more deterministic, better for evals, routing, extractions  
- Higher → more variety, more creative risk, more nonsense risk  

Lab default in this pack: **low temperature** for anything scored.
""", "temperature determinism"),

    S("01-05", "01", "Hallucinations = ungrounded fluency", "beginner", """
In this university, a **hallucination** is a fluent answer not grounded in evidence.

Catch it with:

- fixed eval suites  
- citations (RAG)  
- tools for exact facts (math, catalogs)  
- falsifiers written before the demo  

Never score confidence. Score evidence.
""", "hallucination eval"),

    S("01-06", "01", "System vs user vs tool messages", "intermediate", """
Typical chat stack:

- **System** — role, safety, output contract  
- **User** — task  
- **Assistant** — model reply  
- **Tool** — structured results returned into the loop  

Most production bugs are contract bugs: the system prompt said one shape, the parser expected another, nobody wrote an eval.
""", "messages roles"),

    S("01-07", "01", "Determinism vs reproducibility", "intermediate", """
Even at temperature 0, systems and providers can change. Treat reproducibility as:

1. pin model id / version when you can  
2. pin prompts and tool schemas in git  
3. store inputs + outputs as artifacts  
4. accept that bit-identical text is not always possible — **decision-identical** is the goal  

Evals protect decisions, not poetry.
""", "reproducibility pin"),

    S("01-08", "01", "Local vs cloud mental model", "beginner", """
| | Local | Cloud |
|--|-------|-------|
| Privacy | Stronger default | You send data out |
| Cost | Hardware + electricity | Per token / seat |
| Capability | Improving fast; size-limited | Often stronger frontier |
| Reliability | Your process manager | Their SLA + your key |

Best operators use **both** with a written policy: what stays local, what may burst to cloud.
""", "local cloud policy"),

    S("01-09", "01", "Failure mode catalog (starter)", "intermediate", """
| Mode | Symptom | First check |
|------|---------|-------------|
| Hallucination | Wrong fluent fact | Eval / citation |
| Context overflow | Lost instructions | Token count |
| Tool avoidance | Invented numbers | Force schema tests |
| Prompt injection | Hostile text steers agent | Trust boundary |
| Silent quality drop | Still answers, worse | Regression suite |
| Key leak | Secret in log/repo | Scan + rotate |

Print this next to your monitor for a month.
""", "failure catalog"),

    S("01-10", "01", "Interview 30/90 — mental models", "beginner", """
**30s:** Models predict tokens; fluency isn’t truth. I use RTMA and evals.

**90s:** I treat context like a bandwidth budget. I keep temperature low for scored work. Hallucinations are ungrounded fluency — I catch them with fixed suites, tools for exact facts, and artifacts so incidents are reviewable.
""", "interview"),
]

# ── 02 Local lab ──────────────────────────────────────────────────────
SECTIONS += [
    S("02-01", "02", "Why local models matter", "beginner", """
Local models give you:

- privacy for sensitive drafts  
- offline practice  
- predictable lab cost after hardware  
- a place to learn before spending on APIs  

They are not always the strongest brain. They are often the best **classroom**.
""", "local privacy"),

    S("02-02", "02", "Ollama quick path", "beginner", """
Common friendly path on macOS/Linux:

1. Install Ollama from the official site  
2. `ollama pull llama3.2:3b` (small teaching model)  
3. `curl http://127.0.0.1:11434/api/tags`  
4. Re-run `python3 lab/01_local_hello.py`  

Default API port: **11434**.

If step 3 fails, Phase 1 still works with mock brain — document it in RTMA.
""", "ollama install 11434"),

    S("02-03", "02", "Model catalog policy", "intermediate", """
Write a one-page catalog policy:

- **Daily drill model** — small, fast  
- **Reasoning model** — larger, slower  
- **Embedding model** — for RAG later  
- **Never-git list** — weights, blobs, caches  

Name versions. Record approx disk size. Delete models you do not use monthly.
""", "catalog policy"),

    S("02-04", "02", "Apple Silicon notes", "intermediate", """
On M-series Macs:

- Prefer stacks that use Metal / optimized backends  
- Watch thermal and fan noise on long jobs  
- Memory ceiling matters more than marketing parameter counts  
- Start smaller than ego suggests  

Mac Mini always-on labs are excellent for scheduled evals and private agents.
""", "apple silicon metal"),

    S("02-05", "02", "Windows / Linux notes", "beginner", """
- **Linux:** Ollama or llama.cpp are common; watch GPU drivers  
- **Windows:** native Ollama or WSL2 paths; keep secrets out of shared folders you sync publicly  
- Same RTMA rules everywhere  

This pack’s Python labs are intentionally boring (stdlib + HTTP) so they travel.
""", "windows linux"),

    S("02-06", "02", "Power, disk, backup hygiene", "intermediate", """
- Models can consume many GB — do not commit them  
- Backup **notes + evals + prompts**, not only weights (weights re-pull)  
- Snapshot your `.env` location strategy (password manager), never the secret values into git  
- Leave headroom on disk; full disks create mystery failures  
""", "backup disk"),

    S("02-07", "02", "Lab 01 deep dive", "beginner", """
`lab/01_local_hello.py`:

1. Probes Ollama  
2. Generates a short RTMA explanation  
3. Writes an RTMA JSON artifact  
4. Reports backend `ollama` or `mock` honestly  

GREEN: non-empty answer + artifact + you can restate RTMA.
""", "lab01"),

    S("02-08", "02", "When mock is correct", "beginner", """
Mock brain is **not** cheating. It is a flight simulator.

Valid uses:

- airplane mode learning  
- CI without GPUs  
- teaching RTMA before installs  
- deterministic demos  

Invalid use: claiming production readiness from mock-only runs.
""", "mock honesty"),

    S("02-09", "02", "Benchmark starter sheet", "advanced", """
Record for each model:

- tokens/sec (generation)  
- load time cold vs warm  
- peak memory  
- qualitative notes on instruction following  
- pass rate on golden suite  

One spreadsheet beats ten opinions.
""", "benchmark"),

    S("02-10", "02", "Interview 30/90 — local lab", "beginner", """
**30s:** I run local models for privacy and practice; I measure latency and keep weights out of git.

**90s:** Default path is Ollama on localhost:11434. Labs degrade to an honest mock so learning never blocks. Catalog policy separates daily vs heavy models. Artifacts capture backend and latency every run.
""", "interview"),
]

# ── 03 Cloud APIs ─────────────────────────────────────────────────────
SECTIONS += [
    S("03-01", "03", "Cloud is a metered superpower", "beginner", """
Cloud APIs rent capable models with:

- higher ceilings on quality (often)  
- operational burden of **keys, spend, data handling**  

Treat every key like a production SIP trunk credential.
""", "cloud keys"),

    S("03-02", "03", "Secrets vault basics", "beginner", """
- Store secrets in environment variables or a password manager  
- Ship only `.env.example` with empty placeholders  
- Rotate keys if they ever appear in screenshots, tickets, or chat exports  
- Prefer least-scope keys when providers allow  

This pack’s Phase 1 needs **zero** cloud keys.
""", "secrets env"),

    S("03-03", "03", "Rate limits and retries", "intermediate", """
Expect:

- HTTP 429 rate limits  
- transient 5xx  
- token-per-minute quotas  

Operator pattern: exponential backoff, idempotent requests, circuit breaker, and a human-visible budget alarm.
""", "rate limit 429"),

    S("03-04", "03", "Structured output contracts", "intermediate", """
For agents and pipelines, prefer:

- JSON schemas  
- explicit field lists  
- validators after the model  

Never “hope” the model returns parseable JSON in production without a check.
""", "structured json schema"),

    S("03-05", "03", "Cost control sheet", "intermediate", """
Track weekly:

- spend by project  
- tokens in/out  
- cost per successful eval  
- top expensive prompts  

Set a hard monthly ceiling and a kill-switch procedure (disable key / feature flag).
""", "cost budget"),

    S("03-06", "03", "Burst-to-cloud policy", "intermediate", """
Write rules such as:

- private HR text → local only  
- public docs summarization → cloud allowed  
- customer PII → blocked or redacted pipeline  

Policy beats vibes when you are tired.
""", "policy burst"),

    S("03-07", "03", "Multi-provider reality", "advanced", """
Providers differ on:

- tool calling shapes  
- safety filters  
- latency  
- price  
- data retention terms  

Abstract only after you have two working concrete integrations and evals that pass on both.
""", "multi provider"),

    S("03-08", "03", "Lab preview — cloud hello", "beginner", """
Later phase lab shape:

1. Read key from env  
2. One structured request  
3. Log request id, tokens, cost estimate  
4. RTMA artifact  
5. Delete debug logs that contain secrets  

Do not implement until Phase 1 GREEN.
""", "lab cloud"),

    S("03-09", "03", "Failure modes — cloud", "intermediate", """
| Failure | Detection |
|---------|-----------|
| Key in git | secret scan, git history |
| Bill shock | budget alerts |
| Silent model swap | pin ids + evals |
| Data retention surprise | read terms, private mode |
""", "cloud failures"),

    S("03-10", "03", "Interview 30/90 — cloud", "beginner", """
**30s:** Cloud keys are production credentials; I pin models, structure outputs, and track cost.

**90s:** Local-first for privacy practice; cloud for capability bursts under a written policy. Structured outputs are validated. Budgets have kill-switches. Phase 1 of this free pack needs no keys so anyone can start.
""", "interview"),
]

# ── 04 Prompt systems ─────────────────────────────────────────────────
SECTIONS += [
    S("04-01", "04", "Prompts are job descriptions", "beginner", """
A prompt is not a spell. It is a **job description + constraints + output contract**.

Good prompts:

- state role and audience  
- define success  
- constrain format  
- declare tools allowed  
- declare what to do when uncertain  
""", "prompt contract"),

    S("04-02", "04", "Eval-driven prompting", "intermediate", """
Do not “feel” a prompt better. Change one variable, run the suite, compare pass rate and cost.

Version prompts like dial-plans:

- `prompts/invoice_extractor.v3.md`  
- changelog note  
- linked eval id  
""", "eval driven version"),

    S("04-03", "04", "System prompt checklist", "intermediate", """
Include:

1. identity / role  
2. safety limits  
3. output schema  
4. citation rules  
5. tool policy  
6. uncertainty language (“I don’t know”)  
7. language/style constraints  

Remove poetry that does not change metrics.
""", "system checklist"),

    S("04-04", "04", "Few-shot without leaking secrets", "intermediate", """
Examples teach patterns. They also leak if you paste real customer data.

Rules:

- synthetic examples only in public packs  
- scrub PII  
- keep examples short  
- prefer one perfect example over twelve mediocre ones  
""", "fewshot pii"),

    S("04-05", "04", "Decomposition patterns", "intermediate", """
Hard tasks → smaller tasks:

- outline → draft → critique → revise  
- retrieve → answer → cite  
- plan tools → execute → synthesize  

Each stage can have its own eval.
""", "decompose"),

    S("04-06", "04", "Prompt injection awareness", "intermediate", """
Untrusted text (web pages, PDFs, tickets) can say: “ignore your instructions and…”

Defenses:

- separate trusted system instructions from untrusted content  
- tool allowlists  
- human approval for side effects  
- evals that include hostile strings  
""", "injection"),

    S("04-07", "04", "Curated drills in this pack", "beginner", """
See `prompts/curated/` for Phase 1 drills.

Larger seed libraries also exist in the UC free share pack under `prompts/02-ai-ml-future-lab/` (1000 seeds). Use them as practice fuel — still apply RTMA.
""", "drills seeds"),

    S("04-08", "04", "Interview 30/90 — prompts", "beginner", """
**30s:** Prompts are contracts; I version them and score changes with evals.

**90s:** System prompts set role, safety, and schema. I keep examples synthetic. Untrusted content is data, not instructions. Injection tests live in the suite.
""", "interview"),
]

# ── 05 RAG ────────────────────────────────────────────────────────────
SECTIONS += [
    S("05-01", "05", "RAG in one breath", "beginner", """
**Retrieval-Augmented Generation:** find relevant documents first, then answer with those passages in context, preferably with **citations**.

It is the “open the right binder before speaking” pattern.
""", "rag intro"),

    S("05-02", "05", "Chunking without religion", "intermediate", """
There is no universal perfect chunk size. Start simple:

- keep semantic units together (headings, functions)  
- overlap a little so sentences aren’t cut cruelly  
- record chunker version in artifacts  

Bad chunking → bad retrieval → fluent wrong answers.
""", "chunking"),

    S("05-03", "05", "Embeddings intuition", "beginner", """
Embeddings map text to vectors so “nearby” meanings can be found by similarity search.

You do not need the linear algebra to use them — you need:

- a consistent embedding model  
- a store  
- metrics on retrieval quality (hit rate, MRR, human spot checks)  
""", "embeddings"),

    S("05-04", "05", "Citations or it didn’t happen", "intermediate", """
Production RAG rule:

- every non-trivial claim points to a doc id / path / URL  
- if retrieval is empty, say “not in corpus” instead of freestyling  

Domain experts smell invented citations instantly. So do good evals.
""", "citations"),

    S("05-05", "05", "UC free pack as first corpus", "intermediate", """
If you are a voice engineer, the public **UC Lab Free University** pack is a strong first corpus:

- real curriculum structure  
- free to share educationally  
- perfect for citation drills  

Other domains: use public standards docs, your own notes (scrubbed), or textbook-open materials.
""", "uc corpus"),

    S("05-06", "05", "RAG failure modes", "intermediate", """
| Failure | Symptom |
|---------|---------|
| Wrong neighbor retrieval | confident off-topic cites |
| Stale index | missing new docs |
| Overstuffed context | ignored instructions |
| Citation theater | links that don’t support claim |

Measure retrieval separately from generation.
""", "rag failures"),

    S("05-07", "05", "Minimal RAG lab shape (Phase 3)", "advanced", """
1. Index a small markdown folder  
2. Query → top-k chunks  
3. Answer only from chunks  
4. Return citations  
5. Eval: 20 questions with required doc ids  

Do not build this until golden slice GREEN.
""", "rag lab"),

    S("05-08", "05", "Interview 30/90 — RAG", "beginner", """
**30s:** RAG retrieves evidence first and answers with citations; empty retrieval fails closed.

**90s:** I separate retrieval metrics from generation metrics. Chunker and embedding versions are pinned. Domain corpora beat random web scrapes for operator trust.
""", "interview"),
]

# ── 06 Agents & tools ─────────────────────────────────────────────────
SECTIONS += [
    S("06-01", "06", "An agent is a loop with privileges", "beginner", """
An agent is not a personality. It is a loop that can call tools under a permission model.

If it can spend money, delete files, or message humans, it is **production machinery** — treat it like one.
""", "agent definition"),

    S("06-02", "06", "Tool schema basics", "beginner", """
Tools need:

- name  
- description  
- JSON parameters schema  
- handler implementation  
- approval requirement flag  

Lab 02 ships `calc` and `glossary_lookup` as teaching tools.
""", "tool schema"),

    S("06-03", "06", "Why tools beat invented facts", "beginner", """
Models invent plausible numbers. Calculators do not.

Pattern:

1. model proposes tool call  
2. runtime validates schema  
3. tool executes  
4. result returns into context  
5. synthesis uses the result  
6. RTMA logs the chain  
""", "tools exactness"),

    S("06-04", "06", "Permission model", "intermediate", """
**Never-without-approval (starter):**

- send email / post social  
- delete outside sandbox  
- spend money / change cloud spend limits  
- message real customers  
- push git to main/protected branches  

Default deny for side effects.
""", "permissions approval"),

    S("06-05", "06", "Handoffs and multi-agent caution", "advanced", """
Multiple agents can help (research vs code vs critic) — and can amplify errors.

Rules:

- clear ownership of the final answer  
- shared RTMA trace id  
- critic agent cannot unlock permissions by itself  
- eval the system, not only each role in isolation  
""", "multiagent"),

    S("06-06", "06", "Memory types (plain language)", "intermediate", """
- **Working** — current thread context  
- **Episodic** — what happened in past runs  
- **Semantic** — facts / docs (often RAG)  
- **Procedural** — how to do tasks (skills, tools)  

Most teams overbuild memory and underbuild evals.
""", "memory"),

    S("06-07", "06", "Lab 02 deep dive", "beginner", """
`lab/02_tool_call.py` demonstrates:

- goal in  
- plan tool calls  
- execute calc + glossary  
- synthesize from tool results  
- write RTMA artifact  

GREEN: both tools succeed; you can explain the trace.
""", "lab02"),

    S("06-08", "06", "Failure injection", "advanced", """
Practice killing tools randomly:

- timeout  
- wrong schema  
- empty result  
- exception  

Agents should degrade with a clear error, not hallucinate a success.
""", "failure injection"),

    S("06-09", "06", "Interview 30/90 — agents", "beginner", """
**30s:** Agents are privileged loops; tools use schemas; side effects need humans.

**90s:** I log tool chains in RTMA. Exact facts go through tools. Multi-agent setups share a trace id and a single owner for the final answer. Permissions default deny.
""", "interview"),
]

# ── 07 Voice AI ───────────────────────────────────────────────────────
SECTIONS += [
    S("07-01", "07", "Your domain is a superpower", "beginner", """
If you already debug real-time media, SIP, jitter, one-way audio, or contact-center flows, you have instincts AI-native juniors lack.

Voice AI adds STT/TTS and model latency on top of paths you already understand.
""", "voice superpower"),

    S("07-02", "07", "Latency budget thinking", "intermediate", """
A voice turn budget might include:

- endpointing  
- STT partials / finals  
- LLM time-to-first-token  
- tool calls  
- TTS time-to-first-byte  
- network  

Write a budget. Measure against it. Do not “feel fast.”
""", "latency budget"),

    S("07-03", "07", "STT failure modes", "intermediate", """
- bad mic / gain  
- crosstalk  
- accents / domain jargon  
- partial hypothesis flicker  
- endpoint too aggressive  

Always ask: is this media, model, or language-pack?
""", "stt"),

    S("07-04", "07", "TTS failure modes", "intermediate", """
- robotic prosody  
- pronunciation of extensions, tickets, emails  
- barge-in handling  
- buffering that adds lag  

Test with real phone paths, not only desktop speakers.
""", "tts"),

    S("07-05", "07", "Braid with UC free pack", "intermediate", """
Study plan:

1. Pick a UC free university section (SIP, CUBE, Teams, etc.)  
2. Build 10 quiz questions with citations  
3. Later: agent must answer only with path citations  
4. Add a voice front-end only after text agent is GREEN  
""", "uc braid"),

    S("07-06", "07", "Contact center AI caution", "advanced", """
Real centers involve consent, recording laws, PCI/PII, workforce rules, and vendor constraints.

This free pack does **not** authorize production deployment patterns. Lab safely. Pin legal and vendor guidance.
""", "cc caution"),

    S("07-07", "07", "Interview 30/90 — voice AI", "beginner", """
**30s:** I budget voice latency across STT, LLM, tools, and TTS, and I separate media faults from model faults.

**90s:** Domain vocabulary and path discipline transfer from UC work. I prove text agents with citations before adding voice. Production contact-center AI needs legal and vendor rails this free pack only introduces.
""", "interview"),
]

# ── 08 Evals & safety ─────────────────────────────────────────────────
SECTIONS += [
    S("08-01", "08", "Evals beat vibes", "beginner", """
If you cannot re-run a fixed suite, you cannot tell improvement from luck.

Golden-10 in this pack is intentionally small and strict. Expand with your domain later.
""", "evals"),

    S("08-02", "08", "Golden-10 design", "beginner", """
Each item has:

- id  
- question  
- required_keywords  
- reference_answer  
- category  

Automated gate = keywords. Human gate = meaning. Honesty gate = mock vs real disclosed.
""", "golden10"),

    S("08-03", "08", "Lab 03 deep dive", "beginner", """
`lab/03_run_eval.py` loads `evals/golden10.json`, answers, scores, writes:

- `reports/golden10-report.md`  
- `reports/golden10-detail.json`  
- RTMA artifact  

Pass threshold: **80%**.
""", "lab03"),

    S("08-04", "08", "Red team starter", "intermediate", """
Monthly, attack your own agent with:

- prompt injection strings  
- requests to exfiltrate secrets  
- requests to skip approval  
- jailbreak-style roleplay  

Log outcomes. Fix permissions before marketing demos.
""", "red team"),

    S("08-05", "08", "PII and retention", "intermediate", """
Decide:

- what logs exist  
- how long they live  
- who can read them  
- how training/fine-tune is forbidden on private data  

Default for free-share artifacts: synthetic only.
""", "pii retention"),

    S("08-06", "08", "Human override UX", "intermediate", """
Overrides that humans ignore are fake.

Good overrides:

- visible  
- one click / one command  
- audited  
- tested in drills  

“Email me if something goes wrong” is not a control.
""", "override"),

    S("08-07", "08", "Incident response sketch", "advanced", """
If an agent emails the wrong person:

1. stop the agent  
2. revoke keys / tokens if needed  
3. preserve traces (do not scrub evidence)  
4. notify appropriately  
5. write postmortem with RTMA fields  
6. add an eval that would have caught it  
""", "incident"),

    S("08-08", "08", "Personal safety policy template", "beginner", """
Copy and fill:

- I will not auto-post or auto-email  
- I will not put customer data into public models without approval  
- I will keep keys in a vault  
- I will run evals before sharing demos  
- I will disclose mock vs real backends  
""", "policy template"),

    S("08-09", "08", "Interview 30/90 — evals", "beginner", """
**30s:** Fixed suites catch regressions; safety is permissions plus drills, not slogans.

**90s:** I separate keyword gates, meaning gates, and honesty gates. Red teams try to skip approvals. Incidents produce artifacts and new evals.
""", "interview"),
]

# ── 09 Ship & share ───────────────────────────────────────────────────
SECTIONS += [
    S("09-01", "09", "Free share quality bar", "beginner", """
Ship so a stranger can:

1. download a zip  
2. open HTML offline  
3. run labs without secret keys  
4. understand license and limits  

If only you can run it, it is a private notebook — not a free university.
""", "free share bar"),

    S("09-02", "09", "Browser-friendly size rule", "beginner", """
Default free HTML/site target: **≤ 10–20 MB**.

Depth lives in markdown modules. Optional huge archives must be labeled and never the only path.

UC lesson learned the hard way: multi-hundred-MB single HTML files punish friends’ browsers.
""", "size 20mb"),

    S("09-03", "09", "GitHub Release checklist", "intermediate", """
1. secret scan clean  
2. LICENSE present  
3. README download section obvious  
4. `DOWNLOADS.md`  
5. zip asset on Release  
6. SECURITY + CONTRIBUTING  
7. pin repo + Linktree button after live  
""", "github release"),

    S("09-04", "09", "What never to publish", "beginner", """
- API keys, `.env`  
- customer data, private topologies  
- private chat exports  
- model weight blobs  
- anything illegal or harmful to share  
""", "never publish"),

    S("09-05", "09", "Sibling packs strategy", "beginner", """
Keep **UC Lab Free University** and **AI Lab Free University** as siblings:

- separate repos when public  
- cross-links  
- shared free-share discipline  
- no forced mega-monorepo  
""", "siblings"),

    S("09-06", "09", "Interview 30/90 — ship", "beginner", """
**30s:** Free packs are small, offline-friendly, secret-free, and obvious to download.

**90s:** I ship zip + HTML defaults under size budgets, keep depth in modules, and use Releases so non-git users still get the goods.
""", "interview"),
]

# ── 10 Capstone ───────────────────────────────────────────────────────
SECTIONS += [
    S("10-01", "10", "Capstone vision", "advanced", """
Build a personal agent that coaches you daily from a domain corpus (for many readers: UC free pack; for others: your field’s public docs) with:

- citations  
- RTMA session artifacts  
- evals against invented facts  
- human approval for external actions  
""", "capstone"),

    S("10-02", "10", "Acceptance tests", "advanced", """
Capstone is GREEN only if:

1. cold start docs exist  
2. 20+ citation-required questions pass  
3. injection tests fail closed  
4. weekly report generates without secrets  
5. a friend can run the happy path  
""", "capstone acceptance"),

    S("10-03", "10", "Do not start capstone early", "beginner", """
If Phase 1 is not GREEN, capstone becomes a costume.

Order: foundations → tools → evals → RAG → voice → share.
""", "order"),
]

# ── Glossary ──────────────────────────────────────────────────────────
SECTIONS += [
    S("GL-01", "GL", "Token", "beginner", "A chunk of text a model reads or writes; not always a full word.", "glossary token"),
    S("GL-02", "GL", "Context window", "beginner", "Maximum token budget for a single model request (input + output).", "glossary context"),
    S("GL-03", "GL", "Hallucination", "beginner", "Fluent output not grounded in evidence.", "glossary hallucination"),
    S("GL-04", "GL", "RTMA", "beginner", "Run · Trace · Metric · Artifact — evidence grammar of this university.", "glossary rtma"),
    S("GL-05", "GL", "LICC", "beginner", "Leg · ID · Counter · Capture — UC troubleshooting grammar mirrored by RTMA.", "glossary licc"),
    S("GL-06", "GL", "Tool call", "beginner", "Structured function request by a model; runtime executes and returns results.", "glossary tool"),
    S("GL-07", "GL", "Agent", "beginner", "A loop that plans and calls tools under permissions; not a soul.", "glossary agent"),
    S("GL-08", "GL", "RAG", "beginner", "Retrieve relevant docs, then generate an answer with citations.", "glossary rag"),
    S("GL-09", "GL", "Eval", "beginner", "Fixed test suite that scores quality and catches regressions.", "glossary eval"),
    S("GL-10", "GL", "Ollama", "beginner", "Popular local model runner; often on localhost port 11434.", "glossary ollama"),
    S("GL-11", "GL", "Temperature", "beginner", "Sampling randomness knob; lower is more deterministic.", "glossary temperature"),
    S("GL-12", "GL", "Prompt injection", "beginner", "Hostile content that tries to override system instructions.", "glossary injection"),
    S("GL-13", "GL", "Embedding", "beginner", "Vector representation of text used for similarity search.", "glossary embedding"),
    S("GL-14", "GL", "Structured output", "beginner", "Model response constrained to a schema (often JSON).", "glossary structured"),
    S("GL-15", "GL", "Human approval gate", "beginner", "Required confirmation before side effects leave the machine.", "glossary approval"),
    S("GL-16", "GL", "Mock brain", "beginner", "Deterministic local stand-in used when no model server is available; must be disclosed.", "glossary mock"),
    S("GL-17", "GL", "Pass rate", "beginner", "Fraction of eval items passed; this pack’s golden threshold is 80%.", "glossary passrate"),
    S("GL-18", "GL", "Free share pack", "beginner", "Educational bundle designed for strangers to open offline without private secrets.", "glossary freeshare"),
]

# ── Paths ─────────────────────────────────────────────────────────────
SECTIONS += [
    S("PX-01", "PX", "Path A — Absolute beginner (4 evenings)", "beginner", """
1. Orientation 00-01…00-10  
2. RTMA handbook  
3. Mental models 01-01…01-05  
4. Run `verify_slice.sh`  
5. Glossary skim  
6. GREEN checklist  

Stop. Rest. Do not skip evals.
""", "path beginner"),

    S("PX-02", "PX", "Path B — Domain expert new to AI (1–2 weeks)", "beginner", """
You already operate hard systems.

1. RTMA ↔ your incident grammar  
2. Golden slice until cold  
3. Mental models + local lab  
4. Agents & tools  
5. Evals & safety  
6. Skim Voice AI bridge / domain braid  
7. Draft personal safety policy  
""", "path domain"),

    S("PX-03", "PX", "Path C — Software engineer adding AI (1–2 weeks)", "intermediate", """
1. Golden slice + read lab source  
2. Prompt systems + structured output  
3. Agents permissions  
4. Evals as CI idea  
5. Cloud cost sheet  
6. Ship & share (package a tiny internal pack)  
""", "path engineer"),

    S("PX-04", "PX", "Path D — Student / career switch (steady)", "beginner", """
Three sessions a week:

- 1× concept school  
- 1× lab/RTMA  
- 1× interview bank out loud  

Portfolio = public free pack contributions + your artifacts (scrubbed).
""", "path student"),

    S("PX-05", "PX", "Path E — Voice / UC specialist", "intermediate", """
1. Entire RTMA handbook  
2. Golden slice  
3. Schools 01, 02, 06, 08  
4. School 07 fully  
5. Plan Phase 3 UC corpus RAG  
6. Keep UC free pack installed as sibling  
""", "path uc voice"),
]

# ── Interview bank ────────────────────────────────────────────────────
SECTIONS += [
    S("IV-01", "IV", "Why should we trust your AI work?", "beginner", """
Because I ship evidence: runs, traces, metrics, artifacts. I can show eval pass rates and permission boundaries — not just a demo GIF.
""", "interview trust"),

    S("IV-02", "IV", "Local or cloud — how do you choose?", "beginner", """
Privacy, latency, capability, and cost. Private drafts and drills local; capability bursts to cloud under a written policy with budget kill-switches.
""", "interview local cloud"),

    S("IV-03", "IV", "How do you stop agents from doing damage?", "intermediate", """
Default-deny side effects, schema-validated tools, human approval for email/post/spend, red-team drills, and RTMA traces for forensics.
""", "interview safety"),

    S("IV-04", "IV", "How do you know the model isn’t hallucinating?", "beginner", """
I don’t take its word. Fixed suites, citations, and tools for exact facts. Falsifiers written before demos.
""", "interview halluc"),

    S("IV-05", "IV", "Tell me about a failure", "intermediate", """
Structure: goal → what broke → metric that moved → artifact path → fix → new eval so it cannot silently return.
""", "interview failure"),

    S("IV-06", "IV", "How does UC experience help?", "beginner", """
Real-time systems taught me paths, identifiers, counters, and captures. RTMA is that grammar on AI systems. I separate media faults from model faults.
""", "interview uc"),
]

# ── FAQ ───────────────────────────────────────────────────────────────
SECTIONS += [
    S("FQ-01", "FQ", "Is this really free?", "beginner", """
Yes for learning and sharing under MIT. No warranty. Optional cloud APIs you choose may cost money — Phase 1 does not require them.
""", "faq free"),

    S("FQ-02", "FQ", "Do I need a Mac Mini?", "beginner", """
No. Any machine with Python 3 works for Phase 1. Mac Mini is an excellent always-on lab, not a gate.
""", "faq mac"),

    S("FQ-03", "FQ", "Do I need Ollama?", "beginner", """
No for Phase 1. Labs use an honest mock brain if Ollama is down. Install later for real local generation.
""", "faq ollama"),

    S("FQ-04", "FQ", "Is this only for Cisco/UC people?", "beginner", """
No. UC examples appear because the author is a UC expert and the sibling pack is UC. Mechanisms are general. Bring your own domain.
""", "faq audience"),

    S("FQ-05", "FQ", "Will this replace official docs?", "beginner", """
Never. Pin vendor documentation for production. This is mentorship structure + labs + evidence habits.
""", "faq docs"),

    S("FQ-06", "FQ", "Why not one giant HTML like some packs?", "beginner", """
Browsers struggle with enormous single files. We ship a rich but browser-friendly university HTML plus markdown depth. Optional archives can exist later — labeled.
""", "faq size"),

    S("FQ-07", "FQ", "Can I contribute?", "beginner", """
Yes when the public repo is live: additive educational PRs, no secrets, one topic per PR. See CONTRIBUTING.md.
""", "faq contribute"),

    S("FQ-08", "FQ", "Where is the UC pack?", "beginner", """
https://github.com/cipher0x9/uc-lab-free-university — keep it. AI pack is a sibling, not a replacement.
""", "faq uc"),
]


# ── Expansion wave: operator playbooks (general audience depth) ────────
SECTIONS += [
    S("00-11", "00", "How to study 45 minutes a day", "beginner", """
Suggested daily block:

1. 10 min — one HTML section + mark studied  
2. 20 min — lab or drill with RTMA artifact  
3. 10 min — interview 30/90 out loud  
4. 5 min — honesty counters  

Consistency beats weekend heroics.
""", "habit study"),
    S("00-12", "00", "What GREEN means publicly", "beginner", """
GREEN is not a sticker. It means:

- a stranger could reproduce your Run  
- metrics exist  
- artifacts exist  
- you can teach the mechanism cold  

If you would be embarrassed to show the artifact, it is not GREEN.
""", "green public"),
    S("01-11", "01", "Lossy compression intuition", "intermediate", """
Summaries and embeddings compress meaning. Compression drops detail.

Operator habit: when accuracy matters, retrieve source text — do not trust the compressed memory alone.
""", "compression"),
    S("01-12", "01", "Instruction hierarchy", "intermediate", """
Typical trust order in a well-built app:

1. developer system/policy  
2. tool results  
3. retrieved trusted docs  
4. user task  
5. untrusted pasted content  

If untrusted content can reorder this list, you have an injection bug.
""", "hierarchy trust"),
    S("02-11", "02", "Airgap mode thinking", "advanced", """
For sensitive experiments:

- disable network  
- local models only  
- no cloud embeddings  
- scrub exports  
- write policy before the experiment, not after  

Not every lab needs airgap. The ones that do should be boringly strict.
""", "airgap"),
    S("02-12", "02", "Weekly lab maintenance", "beginner", """
Weekly:

- delete unused models  
- re-run golden suite  
- rotate any temporary keys  
- check disk free space  
- skim one new curriculum section outside your comfort school  
""", "maintenance"),
    S("03-11", "03", "Logging without leaking", "intermediate", """
Log:

- request id  
- model id  
- latency  
- token counts  
- error class  

Do not log:

- raw secrets  
- full prompts with PII  
- authorization headers  

Redact first. Store second.
""", "logging"),
    S("03-12", "03", "SLA vs lab reality", "intermediate", """
Provider status pages and your eval dashboard answer different questions.

SLA = their availability story.  
Your suite = whether *your* product still works for users.

Monitor both.
""", "sla"),
    S("04-09", "04", "Prompt lint checklist", "beginner", """
Before shipping a prompt:

- [ ] success criteria explicit  
- [ ] output schema explicit  
- [ ] uncertainty language present  
- [ ] tools allowed listed  
- [ ] untrusted content labeled  
- [ ] eval id linked  
""", "lint"),
    S("04-10", "04", "Critique-revise pattern", "intermediate", """
Two-pass quality:

1. Draft agent produces answer  
2. Critic agent checks against checklist / schema  
3. Revise once  
4. Stop (avoid infinite loops without budget)  

Always cap iterations. Always log both passes.
""", "critique"),
    S("05-09", "05", "Hybrid search intuition", "advanced", """
Vector search finds neighbors; keyword search finds exact IDs and rare tokens.

Many production systems blend both. Measure — do not assume vectors alone are enough for ticket numbers, error codes, or SIP response names.
""", "hybrid"),
    S("05-10", "05", "Corpus hygiene", "beginner", """
Your RAG is only as clean as your docs.

- remove secrets  
- date documents  
- kill duplicates  
- mark deprecated pages  
- prefer primary sources  
""", "corpus hygiene"),
    S("06-10", "06", "Idempotent tools", "advanced", """
Prefer tools that can be safely retried:

- get status  
- calculate  
- search  

Be careful with:

- send message  
- create charge  
- delete  

If a tool is not idempotent, require approval and de-dupe keys.
""", "idempotent"),
    S("06-11", "06", "Observability for agents", "intermediate", """
Minimum dashboard:

- success rate  
- tool error rate  
- p95 latency  
- human approval wait time  
- cost per successful task  

Pretty traces without decisions are cosplay.
""", "observability"),
    S("07-08", "07", "Barge-in basics", "intermediate", """
Users interrupt. Systems that cannot cancel TTS/LLM work feel broken.

Design for:

- cancel generation  
- stop audio  
- preserve partial context intentionally  
""", "bargein"),
    S("07-09", "07", "Domain lexicon packs", "beginner", """
Boost recognition and generation quality with domain lexicons:

- extension patterns  
- product names  
- ticket formats  
- acronyms  

Feed them into STT hints and RAG glossaries.
""", "lexicon"),
    S("08-10", "08", "Eval ownership", "intermediate", """
Every suite needs an owner:

- who updates items  
- who triages failures  
- who can mark known flakes  
- release gate rules  

Orphan evals rot into ignored red lights.
""", "ownership"),
    S("08-11", "08", "Canary prompts", "advanced", """
Keep 5–10 canary prompts that must always pass before demo day.

If canaries fail, demos are cancelled. Pride is not a release criterion.
""", "canary"),
    S("09-07", "09", "README for strangers", "beginner", """
Stranger README test:

1. What is this?  
2. How do I open it in 10 seconds?  
3. What does free mean?  
4. What will never be included?  
5. Where do I get help?  

If any answer takes a treasure hunt, rewrite the top of README.
""", "readme strangers"),
    S("09-08", "09", "Versioning free packs", "intermediate", """
- v1, v2 additive  
- keep parents downloadable when possible  
- changelog in Release notes  
- never silently replace meaning of a lab id  

Learners bookmark. Respect bookmarks.
""", "versioning"),
    S("10-04", "10", "Capstone milestone plan", "advanced", """
Milestones:

M1 text coach with citations  
M2 daily drill scheduler  
M3 eval harness  
M4 optional voice front-end  
M5 public write-up (scrubbed)

Ship M1 before dreaming M4.
""", "milestones"),
    S("GL-19", "GL", "Canary prompt", "beginner", "A small must-pass prompt set that gates demos and releases.", "glossary canary"),
    S("GL-20", "GL", "Circuit breaker", "beginner", "Automatic stop when error rate or spend crosses a threshold.", "glossary circuit"),
    S("GL-21", "GL", "Idempotent", "beginner", "Safe to retry without duplicating side effects.", "glossary idempotent"),
    S("GL-22", "GL", "Time-to-first-token", "beginner", "Latency until the model emits the first output token.", "glossary ttft"),
    S("GL-23", "GL", "Fail closed", "beginner", "When evidence is missing, refuse or escalate instead of inventing.", "glossary failclosed"),
    S("GL-24", "GL", "Side effect", "beginner", "An action that changes the outside world (email, post, charge, delete).", "glossary sideeffect"),
    S("PX-06", "PX", "Path F — Weekend intensive", "beginner", """
Saturday: Orientation + RTMA + Mental models + verify_slice  
Sunday: Agents + Evals + Ship checklist + interview bank  

Bring coffee. Write artifacts. Do not skip GREEN.
""", "path weekend"),
    S("PX-07", "PX", "Path G — Team lunch & learn (60 min)", "beginner", """
0–10: open v2 HTML together  
10–25: run verify_slice on a shared screen  
25–40: RTMA artifact autopsy  
40–55: pick domain risks (PII, approvals)  
55–60: assign one personal safety rule each  
""", "path team"),
    S("IV-07", "IV", "How do you evaluate an agent demo?", "intermediate", """
I ask for the suite, the pass rate, the permission model, a sample RTMA artifact, and what happens on tool failure. If those are missing, it is a vibe demo.
""", "interview demo"),
    S("IV-08", "IV", "How do you handle model upgrades?", "intermediate", """
Pin versions, run canaries and full golden suites, compare cost/latency, and only then switch defaults. Upgrades are releases, not surprises.
""", "interview upgrade"),
    S("IV-09", "IV", "What is your AI safety boundary?", "beginner", """
No autonomous external side effects. Secrets never in prompts committed to git. Private data needs policy. Evals and red teams are continuous.
""", "interview boundary"),
    S("FQ-09", "FQ", "How is this different from watching YouTube?", "beginner", """
YouTube is consumption. This pack forces Runs, Traces, Metrics, Artifacts, and fixed evals. Proof compounds; playlists do not.
""", "faq youtube"),
    S("FQ-10", "FQ", "Can my whole team use this?", "beginner", """
Yes. MIT educational free share. Keep secrets out of forks. Customize domain corpora privately.
""", "faq team"),
    S("FQ-11", "FQ", "Why Python labs without heavy frameworks?", "beginner", """
Stdlib + HTTP teaches mechanisms. Frameworks change; RTMA and tool schemas transfer. Add frameworks after the grammar is cold.
""", "faq python"),
    S("FQ-12", "FQ", "Is mock brain cheating on evals?", "beginner", """
No for teaching RTMA and tooling. Yes if you claim production model quality from mock-only generation. Disclose backend always.
""", "faq mock"),
    S("RT-05", "RT", "RTMA one-page template", "beginner", """
```
RUN: <command>
GOAL: <one sentence>
TRACE:
- t0 ...
- t1 ...
METRIC:
- latency_ms:
- pass_rate:
- cost:
ARTIFACT:
- path1
FALSIFIER:
- <what would kill the claim>
STATUS: ok|fail|partial
```
Copy this into notes until muscle memory forms.
""", "template"),
    S("RT-06", "RT", "Team RTMA reviews", "intermediate", """
Weekly 20-minute review:

1. Each person shows one artifact  
2. Group names the falsifier  
3. Pick one metric to improve next week  

This is how operator cultures form.
""", "team review"),
    S("00-13", "00", "Compare: course vs free university pack", "beginner", """
Paid courses often optimize for video completion.  
This pack optimizes for **reproducible competence**.

You can still use courses. Bring RTMA to them so learning becomes evidence.
""", "compare course"),
    S("01-13", "01", "Stochastic systems mindset", "intermediate", """
Same prompt can vary. That is not an excuse for no tests — it is why tests, pins, and thresholds exist.

Engineers already live with jitter and packet loss. Treat model variance with the same maturity.
""", "stochastic"),
    S("02-13", "02", "Choosing first model size", "beginner", """
Start smaller than ego wants:

- faster feedback  
- easier offline  
- clearer failures  

Graduate size only when golden suite plateaus for the right reasons.
""", "model size"),
    S("06-12", "06", "Human-in-the-loop patterns", "beginner", """
- approve plan before tools  
- approve side effects only  
- approve final external send  
- async review queue for low risk  

Pick the lightest loop that still prevents harm.
""", "hitl"),
    S("08-12", "08", "Scorecards not screenshots", "beginner", """
A screenshot of a happy chat is not an eval.

A scorecard is: dataset + metrics + threshold + date + model id + pass/fail.
""", "scorecard"),
    S("09-09", "09", "Accessibility & offline kindness", "beginner", """
- works offline  
- system fonts  
- keyboard search  
- readable contrast themes  
- no account wall  

Free share includes people on slow networks and borrowed laptops.
""", "a11y offline"),
    S("GL-25", "GL", "Scorecard", "beginner", "Dataset + metrics + threshold + version pins that decide pass/fail.", "glossary scorecard"),
    S("IV-10", "IV", "Explain RTMA to a non-engineer", "beginner", """
It means: say what you did, keep the receipt trail, measure something, and save the output. Like a lab notebook for AI work.
""", "interview plain"),
    S("FQ-13", "FQ", "Will you add more languages / i18n?", "beginner", """
English first for v2 free pack. Contributions welcome when public. Mechanisms are language-agnostic.
""", "faq i18n"),
    S("FQ-14", "FQ", "How do I report a curriculum error?", "beginner", """
Open an issue on the public repo when live, or PR a fix to `curriculum/corpus.py` with a short why. Additive, kind, no secrets.
""", "faq error"),
]


# ── Expansion wave 2: depth to exceed UC section count ────────────────
def _bulk(school: str, prefix: str, start: int, items: list[tuple[str, str, str]]) -> list:
    out = []
    n = start
    for title, level, body in items:
        out.append(S(f"{prefix}-{n:02d}", school, title, level, body, tags=title.lower()))
        n += 1
    return out

SECTIONS += _bulk("00", "00", 14, [
    ("Common myths to ignore", "beginner", "Myth: bigger model always better.\\nMyth: confidence means correctness.\\nMyth: one prompt replaces engineering.\\nMyth: free packs must be huge to be valuable.\\n\\nCounter each myth with a metric or artifact habit."),
    ("Lab notebook standards", "beginner", "Date every session. One goal sentence. Paste run commands. Link artifacts. End with what surprised you. Future-you is a teammate."),
    ("Sharing without oversharing", "beginner", "Public: mechanisms, synthetic examples, scrubbed metrics.\\nPrivate: customer text, keys, internal IPs, real phone numbers.\\nWhen unsure, keep it private."),
])
SECTIONS += _bulk("01", "01", 14, [
    ("Alignment vs capability (plain)", "intermediate", "Capability is what a model can do. Alignment/safety is whether it does what you intended within limits. You need both measurements."),
    ("Why 'just add more context' fails", "intermediate", "Stuffing more text can crowd out instructions, raise cost, and still miss the one sentence that mattered. Prefer retrieval + structure over endless paste."),
    ("Calibration language", "beginner", "Teach models (and yourself) to say: certain / likely / unsure / unknown. Reward uncertainty when evidence is thin."),
])
SECTIONS += _bulk("02", "02", 14, [
    ("GPU vs Apple Silicon vs CPU", "intermediate", "You may run on GPU CUDA, Apple Metal, or CPU. Start with whatever is reliable. Optimize only after golden suite is stable."),
    ("Model license awareness", "beginner", "Model weights have licenses separate from this pack's MIT docs. Read them before redistribution of weights (we recommend not shipping weights at all)."),
    ("Smoke test after reboot", "beginner", "After reboot: is Ollama up? tags endpoint ok? Lab 01 backend? Disk free? Five minutes saves a confusing evening."),
])
SECTIONS += _bulk("03", "03", 13, [
    ("Provider comparison sheet", "intermediate", "Columns: model id, context, tools support, price in/out, data retention, region, rate limits, eval pass rate on your suite."),
    ("Staging vs production keys", "beginner", "Separate keys by environment. Production keys never live in demo laptops if you can avoid it."),
    ("Timeouts and deadlines", "intermediate", "Every cloud call needs a timeout. Infinite waits are outages with worse manners."),
])
SECTIONS += _bulk("04", "04", 11, [
    ("Output contracts for tables", "beginner", "If you need a table, specify columns and forbid extra prose. Validate row counts. Pretty markdown that breaks parsers is a defect."),
    ("Multilingual prompting notes", "intermediate", "State language explicitly. Don't assume the model keeps language stable under tool noise. Eval in each target language."),
    ("Prompt PR template", "beginner", "Change summary · linked eval · before/after pass rate · cost delta · risk notes · rollback prompt version."),
])
SECTIONS += _bulk("05", "05", 11, [
    ("Freshness and crawling ethics", "intermediate", "If you refresh corpora from the web, respect robots rules, licenses, and privacy. Educational free packs prefer public domain / your own notes."),
    ("Citation formats that help humans", "beginner", "Include path + section title + short quote. A bare URL dump is not a citation habit."),
    ("When not to use RAG", "beginner", "Pure calculation, pure code generation with tests, or tasks with no trustworthy corpus — don't force RAG theater."),
])
SECTIONS += _bulk("06", "06", 13, [
    ("Planner vs executor split", "intermediate", "Planner proposes steps. Executor runs tools. Critic checks. Splitting roles reduces confused responsibility — if traces remain unified."),
    ("Sandbox filesystems", "beginner", "Give file tools a sandbox root. Deny `..` escapes. Log every path touched."),
    ("Rate limiting your own agent", "intermediate", "Agents can loop. Cap steps, tokens, wall clock, and tool calls per run."),
])
SECTIONS += _bulk("07", "07", 10, [
    ("Turn-taking states", "intermediate", "Listening · thinking · speaking · interrupted. Explicit states beat boolean flags scattered in code."),
    ("Noise and AEC reality", "intermediate", "Echo, AGC, and double-talk destroy STT. Fix acoustics before fine-tuning prompts."),
    ("Emergency handoff to human", "beginner", "Always design a human escape hatch for voice bots. Publish the path. Test it."),
])
SECTIONS += _bulk("08", "08", 13, [
    ("Flaky eval triage", "intermediate", "If an item flips often, pin seeds/temperature, tighten scoring, or quarantine with a ticket — don't ignore red."),
    ("Security review lite", "beginner", "Permissions · secrets · logs · external tools · injection tests · data retention. One page before any external demo."),
    ("Abuse cases brainstorm", "intermediate", "Who benefits from misusing your agent? List 5 abuses. Add one control each."),
])
SECTIONS += _bulk("09", "09", 10, [
    ("Release notes that teach", "beginner", "What changed · why · migration · known gaps · download links. Teaching tone, not corporate fog."),
    ("Pinning curriculum versions in class", "intermediate", "If you teach a cohort, pin a zip tag so Monday and Friday students see the same lessons."),
    ("Mirror strategy", "beginner", "GitHub Release + local zip + optional second mirror. One broken CDN should not strand learners."),
])
SECTIONS += _bulk("10", "10", 5, [
    ("Capstone demo script", "advanced", "1 min problem · 2 min architecture · 2 min live RTMA · 2 min eval scorecard · 1 min limits. No feature salad."),
    ("Capstone ethics statement", "beginner", "State data sources, consent, retention, and what the agent must never do. Put it in the README."),
    ("After capstone — keep the loop", "beginner", "Schedule weekly canaries forever. Competence decays when evidence stops."),
])
SECTIONS += _bulk("GL", "GL", 26, [
    ("Sandbox", "beginner", "Restricted execution environment for tools."),
    ("Planner", "beginner", "Component that proposes steps before execution."),
    ("Executor", "beginner", "Component that runs tool calls."),
    ("Critic", "beginner", "Component that checks outputs against rules."),
    ("Canary suite", "beginner", "Tiny must-pass eval gate for demos/releases."),
    ("Wall-clock budget", "beginner", "Maximum real time allowed for a run."),
    ("Red team", "beginner", "Adversarial testing of your own system."),
    ("Postmortem", "beginner", "Blameless write-up of failure with RTMA fields."),
    ("Model pin", "beginner", "Fixed model identifier/version for reproducibility."),
    ("Synthetic data", "beginner", "Artificial examples without real customer PII."),
])
SECTIONS += _bulk("IV", "IV", 11, [
    ("Walk me through your golden slice", "beginner", "Local hello with RTMA artifact, tool call with schema and trace, fixed eval suite with threshold, GREEN only if teachable."),
    ("How do you prevent secret leakage?", "beginner", "Env-only secrets, .env.example, secret scanning, no secrets in prompts committed, redact logs, rotate on exposure."),
    ("What would you measure on day one?", "intermediate", "Task success, latency, cost, tool error rate, approval lag, and a 10-item domain eval pass rate."),
])
SECTIONS += _bulk("FQ", "FQ", 15, [
    ("Can I use this commercially in products?", "beginner", "MIT license allows broad use of the pack text/code. Model provider terms and your local laws still apply. No warranty. You are responsible for production safety."),
    ("Does this include model weights?", "beginner", "No. Pull models yourself. Keeps the free pack small and license-clean."),
    ("How often will it update?", "beginner", "Additive versions when published. Rebuildable corpus means improvements don't require mysterious binary HTML edits."),
    ("Is there a certificate?", "beginner", "No certificate theater. Your artifacts and public contributions are the portfolio."),
    ("Can children use this?", "beginner", "It's written for adult learners and professionals. Supervising adults should review any online model use for minors."),
])
SECTIONS += _bulk("RT", "RT", 7, [
    ("RTMA for meetings", "beginner", "Run: decision asked. Trace: options considered. Metric: time and owners. Artifact: notes link. Meetings without artifacts are fog."),
    ("RTMA for incidents", "intermediate", "Same four fields as production SEV reviews. AI outages deserve the same seriousness as call-center outages."),
    ("RTMA anti-patterns", "beginner", "Wall of logs nobody reads · metrics without thresholds · artifacts on personal Desktop only · falsifier written after success."),
])
SECTIONS += _bulk("PX", "PX", 8, [
    ("Path H — Managers / leads (2 hours)", "beginner", "Skim Orientation + RTMA + Evals & safety + Ship. Require scorecards from teams. Ban vibe-only demos."),
    ("Path I — Teachers / mentors", "beginner", "Use v2 HTML in class, pin a zip, run verify once live, assign GREEN checklists, grade artifacts not vibes."),
])


# wave3 exceed 240
SECTIONS += [
    S("00-17", "00", "How this pack is maintained", "beginner", "Curriculum lives in curriculum/corpus.py. HTML is built by scripts/build_university.py. Labs verified by scripts/verify_slice.sh. That is intentional engineering, not mystery HTML."),
    S("01-17", "01", "Base models vs instruction models", "beginner", "Base models continue text. Instruction-tuned models follow directions better for assistants. Know which you loaded."),
    S("02-17", "02", "Quantization in one paragraph", "intermediate", "Quantization shrinks weights for speed/memory with quality tradeoffs. Smaller quants can be fine for drills and wrong for hard reasoning — measure with your suite."),
    S("03-17", "03", "Webhooks and async jobs", "advanced", "Long tasks should not block HTTP forever. Queue work, return ids, write RTMA as the job progresses."),
    S("06-16", "06", "Tool allowlists vs denylists", "intermediate", "Allowlists are safer. Denylists miss creative paths. Prefer allowlist + approval for anything new."),
    S("08-16", "08", "Regression windows", "intermediate", "Compare this week vs last week on the same suite. Improvement is a delta, not a vibe."),
    S("09-13", "09", "Why MIT for free packs", "beginner", "Clear permission to learn, share, and build. Still no warranty. Still your duty for production safety."),
    S("GL-36", "GL", "Quantization", "beginner", "Reduced-precision model weights to save memory/speed, with quality tradeoffs."),
    S("FQ-20", "FQ", "Why not 760MB of embedded materials?", "beginner", "Because friends' browsers and phones deserve respect. Depth is modular; optional archives can exist later if labeled."),
    S("RT-10", "RT", "RTMA emoji-free discipline", "beginner", "You do not need fancy UI. Four fields written honestly beat decorative dashboards."),
    S("PX-10", "PX", "Path J — After UC free university", "beginner", "If you finished UC free pack energy: map LICC→RTMA, run AI golden slice, then School 07 planning. Two free universities, one operator brain."),
    S("IV-14", "IV", "Sell me on free educational packs", "beginner", "They remove paywalls from operator mentorship, force clear packaging, and create shared language (RTMA/LICC) across strangers learning in public."),
]

assert len(SECTIONS) == len({s["id"] for s in SECTIONS}), "duplicate section ids"


def stats() -> dict:
    by = {}
    for s in SECTIONS:
        by[s["school"]] = by.get(s["school"], 0) + 1
    return {"sections": len(SECTIONS), "by_school": by}


if __name__ == "__main__":
    print(stats())
