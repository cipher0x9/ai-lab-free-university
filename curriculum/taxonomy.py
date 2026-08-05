#!/usr/bin/env python3
"""
AI Lab Free University — Lifetime Mastery Taxonomy (v3)

Sources synthesized (educational; not scraped secrets):
- Local: Agentic_AI_University, DevOps_AI_Deployment_Mastery,
  Agentic_AI_Deployment_Engineer, GOOGLE_AI_ARSENAL, UC prompts 02,
  hermes wiring docs, LANGUAGE_MASTERY patterns
- Public industry roadmaps 2026: context engineering, RAG, agents, MCP,
  evals, LLMOps, model routing, local LLMs
- Ecosystem: Hermes Agent (Nous), agent frameworks, robotics foundation models
- X/public discourse: permissions-as-perimeter, systematic eval taste, fallbacks

RTMA = Run · Trace · Metric · Artifact (required on every lab-grade lesson).
"""

from __future__ import annotations

PRACTICE_DEPTH_2026 = {
    "D00": "Define the learner, task, data boundary, success check, stop budget, and human-only action before choosing a model.",
    "D01": "Contract-test schemas, retries, idempotency, fixtures, and observability before adding probabilistic behavior.",
    "D02": "Evaluate multilingual meaning, typography, tokenization, and cultural context with native-speaker review where risk matters.",
    "D03": "Trace tokenization, context assembly, uncertainty, and model failure separately from product and policy failures.",
    "D04": "Version datasets, record consent and lineage, test leakage and bias, and keep synthetic data labeled as synthetic.",
    "D05": "Benchmark local models by task pass rate, warm/cold p95, memory pressure, privacy boundary, and cost per verified task.",
    "D06": "Keep providers behind adapters; pin versions and compare quality, latency, cost, safety, fallback, and retention policy.",
    "D07": "Version prompts, schemas, examples, and trust boundaries independently; release only through the same regression suite.",
    "D08": "Version parser through index; evaluate hybrid retrieval and reranking before generation, citations, and empty-result behavior.",
    "D09": "Persist agent state, typed tools, approval ids, budgets, corrections, assertions, cancellation, replay, and stop reason.",
    "D10": "Build memory with consent, provenance, expiry, deletion, conflict resolution, and a test for what must never be remembered.",
    "D11": "Combine deterministic, calibrated model-graded, and human evals; slice failures and connect every incident to regression coverage.",
    "D12": "Measure multimodal and voice quality plus p50/p95 per stage; test ambiguity, interruption, consent, and human handoff.",
    "D13": "Correlate traces across model, retrieval, tools, approvals, cost, and artifacts while redacting sensitive payloads.",
    "D14": "Use canaries, shadow traffic, bounded autonomy, secrets controls, supply-chain evidence, and rehearsed rollback.",
    "D15": "Treat robotics and physical AI as safety-critical control: simulate first, constrain action space, and preserve a human stop.",
    "D16": "Route model and system changes through measurable product outcomes, accessibility, risk ownership, and total operating cost.",
    "D17": "Separate scenario from certainty; study quantum/AI, governance, and frontier research through primary evidence and falsifiable claims.",
}

UNIVERSAL_PRACTICE_CHECKS_2026 = [
    "Hold the task and evaluator constant while changing one system variable.",
    "Record quality, p95 latency, cost per verified task, and one safety signal.",
    "Force an empty, malformed, unauthorized, stale, or timeout path as appropriate.",
    "Preserve model, prompt, data, tool, and policy versions in the trace.",
    "Keep a human owner and approval artifact for material side effects.",
    "Retain the last GREEN configuration and prove the rollback path.",
]

# Division → chapters → lesson seeds (title, level, focus tags, body_kind)
# body_kind drives generator templates for consistent mentor quality.

DIVISIONS = [
    {
        "id": "D00",
        "name": "Campus & Operator OS",
        "blurb": "Enroll, RTMA, honesty, safety, study OS for a lifetime.",
        "chapters": [
            ("C00.1", "Welcome & free-share contract", "beginner", [
                "Who this university is for",
                "Promise and non-goals",
                "Sibling UC Lab Free University",
                "How to open offline HTML",
                "How to run verify_slice",
                "Honesty counters weekly",
                "Personal safety policy template",
                "Emotional contract for beginners",
            ]),
            ("C00.2", "RTMA evidence grammar", "beginner", [
                "RTMA defined",
                "RTMA maps to UC LICC",
                "Writing artifacts that matter",
                "Falsifier-first thinking",
                "RTMA for incidents",
                "RTMA for meetings",
                "RTMA anti-patterns",
                "Team RTMA review ritual",
                "One-page RTMA template",
                "Scorecards not screenshots",
            ]),
            ("C00.3", "Study paths for every audience", "beginner", [
                "Path Absolute beginner",
                "Path Domain expert new to AI",
                "Path Software engineer",
                "Path Student career switch",
                "Path Voice UC specialist",
                "Path Manager lead",
                "Path Teacher mentor",
                "Path Weekend intensive",
                "Path Team lunch and learn",
                "Path Lifetime 12-month map",
            ]),
        ],
    },
    {
        "id": "D01",
        "name": "Engineering Foundations",
        "blurb": "Python, Git, APIs, testing — before agents get interesting.",
        "chapters": [
            ("C01.1", "Python operator toolkit", "beginner", [
                "Python mental model for AI work",
                "Virtual envs and project layout",
                "JSON and structured data",
                "HTTP clients without mystery",
                "Async basics when you need them",
                "Type hints that save evals",
                "Logging without leaking secrets",
                "CLI scripts as lab harnesses",
            ]),
            ("C01.2", "Git & professional hygiene", "beginner", [
                "Git for AI artifacts",
                "Branching for prompt versions",
                "Secret scanning habits",
                "PR discipline for curriculum",
                "Reproducible lab commits",
            ]),
            ("C01.3", "APIs auth retries", "intermediate", [
                "REST mental model",
                "Auth patterns API keys OAuth",
                "Retries backoff circuit breakers",
                "Timeouts and deadlines",
                "Idempotency keys",
                "Webhook and async job patterns",
            ]),
            ("C01.4", "Testing before AI magic", "intermediate", [
                "Unit tests for tools",
                "Contract tests for schemas",
                "Golden fixtures",
                "CI gates for evals",
            ]),
        ],
    },
    {
        "id": "D02",
        "name": "Languages & Polyglot OS",
        "blurb": "Code languages + human languages as leverage for AI systems.",
        "chapters": [
            ("C02.1", "Code languages for AI builders", "beginner", [
                "Python as default AI glue",
                "TypeScript for product UIs and agents",
                "Go for services and CLI tools",
                "Rust when performance and safety bite",
                "Bash and zsh as lab remote hands",
                "SQL as truth interface",
                "When to stay monolingual",
            ]),
            ("C02.2", "Human languages and AI", "beginner", [
                "Multilingual prompting discipline",
                "Translation eval traps",
                "Domain jargon packs",
                "Sanskrit computational curiosity bridge",
                "Voice language packs STT",
            ]),
            ("C02.3", "Reading foreign codebases", "intermediate", [
                "Map before edit",
                "Dependency graphs",
                "Test-first orientation in strange repos",
            ]),
        ],
    },
    {
        "id": "D03",
        "name": "ML & Data Systems",
        "blurb": "Classical ML, evaluation, data pipelines — without math fear.",
        "chapters": [
            ("C03.1", "ML mental models", "beginner", [
                "Prediction vs understanding",
                "Bias variance intuition",
                "Train validate test split",
                "Overfitting as memorization",
                "Features as questions to data",
                "Supervised vs unsupervised vs RL sketch",
            ]),
            ("C03.2", "Data engineering for AI", "intermediate", [
                "Ingestion discipline",
                "Cleaning and consent",
                "PII scrubbing",
                "Dataset versioning",
                "Label quality is destiny",
                "Synthetic data rules",
            ]),
            ("C03.3", "Metrics that matter", "intermediate", [
                "Accuracy is not enough",
                "Precision recall tradeoffs",
                "Calibration",
                "Business metric mapping",
            ]),
        ],
    },
    {
        "id": "D04",
        "name": "Deep Learning & Generative AI",
        "blurb": "Transformers, tokens, generation, fine-tunes at operator altitude.",
        "chapters": [
            ("C04.1", "Neural stack intuition", "beginner", [
                "From linear models to deep nets",
                "What a layer does in plain language",
                "Loss as a coach whistle",
                "GPUs and why they matter",
            ]),
            ("C04.2", "Transformers & LLMs", "beginner", [
                "Tokens and tokenization",
                "Context window as budget",
                "Attention intuition without fear",
                "Next-token prediction",
                "Temperature and sampling",
                "Base vs instruction vs chat models",
                "Hallucination defined operationally",
            ]),
            ("C04.3", "Fine-tuning landscape", "advanced", [
                "When not to fine-tune",
                "LoRA PEFT intuition",
                "DPO RLHF sketch",
                "Eval before and after tune",
                "Catastrophic forgetting watchouts",
            ]),
            ("C04.4", "Multimodal generation", "intermediate", [
                "Vision language models",
                "Image generation ops notes",
                "Audio models STT TTS",
                "Video generation cost traps",
            ]),
        ],
    },
    {
        "id": "D05",
        "name": "Local Lab OS (Mac Mini & beyond)",
        "blurb": "Private models, hardware, Ollama, thermal, backups.",
        "chapters": [
            ("C05.1", "Why local", "beginner", [
                "Privacy first classroom",
                "Offline practice",
                "Cost after hardware",
                "Mock brain honesty",
            ]),
            ("C05.2", "Ollama & runners", "beginner", [
                "Ollama install path",
                "Port 11434 contract",
                "Pull small teaching models",
                "llama.cpp overview",
                "MLX on Apple Silicon",
                "Quantization tradeoffs",
            ]),
            ("C05.3", "Mac Mini lab operations", "intermediate", [
                "Always-on lab patterns",
                "Thermal and noise scheduling",
                "Disk and model catalog policy",
                "Backup notes not only weights",
                "Airgap mode",
                "Smoke test after reboot",
            ]),
            ("C05.4", "Benchmarks", "advanced", [
                "Tokens per second sheet",
                "Cold vs warm load",
                "Concurrent agents stress",
                "Power draw awareness",
            ]),
        ],
    },
    {
        "id": "D06",
        "name": "Cloud Vendors & Model APIs",
        "blurb": "Multi-vendor brain rental: keys, cost, routing, contracts.",
        "chapters": [
            ("C06.1", "Vendor map 2026", "beginner", [
                "OpenAI ecosystem sketch",
                "Anthropic Claude sketch",
                "Google Gemini sketch",
                "xAI Grok sketch",
                "Open-weight hosts Together Fireworks Groq sketch",
                "Azure AWS Bedrock sketch",
                "Apple on-device notes",
                "How to read vendor docs without drowning",
            ]),
            ("C06.2", "Keys cost control", "intermediate", [
                "Secrets vault basics",
                "Staging vs production keys",
                "Rate limits 429 playbook",
                "Token cost sheet",
                "Monthly kill switch",
                "Burst-to-cloud policy",
            ]),
            ("C06.3", "Model routing", "advanced", [
                "Task type classification",
                "Tiered model selection",
                "Fallback chains primary backup cheap cached",
                "Confidence routing to humans",
                "Pinning model ids",
            ]),
            ("C06.4", "Structured outputs", "intermediate", [
                "JSON schema contracts",
                "Validators after the model",
                "Tool calling shapes differ by vendor",
                "Streaming SSE patterns",
            ]),
        ],
    },
    {
        "id": "D07",
        "name": "Prompt & Context Engineering",
        "blurb": "Contracts, versioning, context design — where quality lives.",
        "chapters": [
            ("C07.1", "Prompts as job descriptions", "beginner", [
                "System user tool roles",
                "Success criteria explicit",
                "Uncertainty language",
                "Few-shot without PII",
                "Prompt lint checklist",
            ]),
            ("C07.2", "Context engineering", "intermediate", [
                "Context window budgeting",
                "What to put in vs retrieve",
                "Tool description quality",
                "Instruction hierarchy trust order",
                "Compression loss awareness",
            ]),
            ("C07.3", "Versioning and eval-driven prompts", "intermediate", [
                "Prompt as code",
                "A B testing prompts",
                "Rollback strategy",
                "Critique revise pattern",
                "Injection awareness",
            ]),
        ],
    },
    {
        "id": "D08",
        "name": "RAG Memory & Knowledge",
        "blurb": "Retrieval, embeddings, citations, memory architectures.",
        "chapters": [
            ("C08.1", "RAG core", "beginner", [
                "RAG in one breath",
                "Chunking without religion",
                "Embeddings intuition",
                "Citations or it did not happen",
                "Fail closed empty retrieval",
            ]),
            ("C08.2", "Advanced retrieval", "advanced", [
                "Hybrid search",
                "Reranking",
                "Metadata filters",
                "Caching retrieved contexts",
                "Observability for retrieval",
            ]),
            ("C08.3", "Memory types", "intermediate", [
                "Working memory thread",
                "Episodic memory runs",
                "Semantic memory facts",
                "Procedural memory skills",
                "When not to build memory",
            ]),
            ("C08.4", "Domain corpora", "intermediate", [
                "UC free pack as first corpus",
                "Public standards corpora",
                "Corpus hygiene",
                "Freshness ethics",
            ]),
        ],
    },
    {
        "id": "D09",
        "name": "Agents Tools & MCP",
        "blurb": "Privileged loops, schemas, frameworks, Model Context Protocol.",
        "chapters": [
            ("C09.1", "Agent fundamentals", "beginner", [
                "Agent is a loop with privileges",
                "When not to use an agent",
                "Workflow vs agent vs single call",
                "ReAct pattern sketch",
                "Planner executor critic",
            ]),
            ("C09.2", "Tools", "beginner", [
                "Tool schema basics",
                "Why tools beat invented facts",
                "Idempotent tools",
                "Sandbox filesystems",
                "Allowlists not denylists",
                "Rate limiting your agent",
            ]),
            ("C09.3", "Permissions HITL", "intermediate", [
                "Never without approval list",
                "Human in the loop patterns",
                "Permissions as security perimeter",
                "YOLO mode is an incident",
                "Side effects catalog",
            ]),
            ("C09.4", "MCP protocol", "intermediate", [
                "What MCP is for",
                "MCP client server sketch",
                "Tool discovery via MCP",
                "Trust boundaries with MCP servers",
                "MCP in plant floor and ops examples",
            ]),
            ("C09.5", "Frameworks map", "intermediate", [
                "LangGraph sketch",
                "CrewAI sketch",
                "PydanticAI sketch",
                "AutoGen style multi agent",
                "Pick patterns over brand loyalty",
            ]),
            ("C09.6", "Multi-agent", "advanced", [
                "Supervisor pattern",
                "Handoffs and ownership",
                "Shared trace ids",
                "Debate plus judge",
                "Failure amplification risks",
            ]),
        ],
    },
    {
        "id": "D10",
        "name": "Hermes & Personal Agent OS",
        "blurb": "Wire Hermes as coach/enricher — local Mac Mini agent lifestyle.",
        "chapters": [
            ("C10.1", "Hermes mental model", "beginner", [
                "What Hermes Agent is",
                "Persistent memory idea",
                "Skills and self-improvement loop",
                "Local data stays local ethos",
                "Hermes vs chat tabs",
            ]),
            ("C10.2", "Wire Hermes to free universities", "intermediate", [
                "Source of truth vs scheduler",
                "Morning coach 15 minute pattern",
                "University enrich with human PROCEED",
                "RAG over prompts and sections",
                "Nature mode voice quizzes",
                "Agency mode draft then approve",
            ]),
            ("C10.3", "Safe Hermes operations", "intermediate", [
                "Approval gates always",
                "No outbound without human",
                "Artifact daily files",
                "Config hygiene",
                "Incident if unattended high privilege",
            ]),
            ("C10.4", "Hermes lab on Mac Mini", "advanced", [
                "Install and profiles sketch",
                "Cron style daily drills",
                "Channel directory caution",
                "Backup hermes state carefully",
                "Enrich UC and AI packs additively",
            ]),
        ],
    },
    {
        "id": "D11",
        "name": "Evals Safety & LLMOps",
        "blurb": "Taste as eval design, guardrails, observability, production ops.",
        "chapters": [
            ("C11.1", "Evals as taste", "beginner", [
                "Evals beat vibes",
                "Golden sets",
                "Keyword meaning honesty gates",
                "LLM as judge calibration",
                "Canary prompts",
                "Regression windows",
            ]),
            ("C11.2", "Safety", "intermediate", [
                "Prompt injection catalog",
                "Jailbreak realism",
                "PII retention matrix",
                "Red team monthly",
                "Human override UX",
                "Abuse case brainstorm",
            ]),
            ("C11.3", "Observability", "intermediate", [
                "Traces spans request ids",
                "Latency budgets journey level",
                "Token and cost dashboards",
                "Tool error rates",
                "Phoenix LangSmith style tools sketch",
            ]),
            ("C11.4", "Production LLMOps", "advanced", [
                "Deploy AI behind APIs",
                "Feature flags for models",
                "Shadow traffic",
                "Incident response for agents",
                "On-call for model quality",
            ]),
        ],
    },
    {
        "id": "D12",
        "name": "Voice AI & UC Superpower",
        "blurb": "STT TTS latency — braid Cisco/UC mastery with AI.",
        "chapters": [
            ("C12.1", "Voice path budgets", "intermediate", [
                "Speech to reply chain",
                "Latency budget sheet",
                "Barge-in basics",
                "Turn taking states",
            ]),
            ("C12.2", "STT TTS failure modes", "intermediate", [
                "Mic and media first",
                "Domain lexicon packs",
                "TTS pronunciation tickets emails",
                "Noise AEC reality",
            ]),
            ("C12.3", "Contact center caution", "advanced", [
                "Consent and recording law awareness",
                "PCI PII boundaries",
                "Human emergency handoff",
                "UC free pack citation drills",
            ]),
        ],
    },
    {
        "id": "D13",
        "name": "Code Frameworks & Product Stacks",
        "blurb": "Ship real software around models — Next.js, APIs, data stores.",
        "chapters": [
            ("C13.1", "App shapes", "intermediate", [
                "Chat UI essentials",
                "Streaming partial render",
                "Server actions and API routes sketch",
                "Auth for AI apps",
            ]),
            ("C13.2", "Data stores", "intermediate", [
                "Postgres for system of record",
                "Vector DB map Pinecone Qdrant Milvus pgvector",
                "Redis for cache and rate limits",
                "Object storage for artifacts",
            ]),
            ("C13.3", "DevOps for AI apps", "advanced", [
                "Containers basics",
                "CI with eval gates",
                "Env management",
                "Observability stack glue",
            ]),
        ],
    },
    {
        "id": "D14",
        "name": "Future Stack Robotics & Physical AI",
        "blurb": "Embodied AI, VLA, world models, robotics foundations — foresight track.",
        "chapters": [
            ("C14.1", "Physical AI map", "beginner", [
                "Why embodiment matters",
                "Sensors actuators loop",
                "Sim to real gap",
                "Safety around moving machines",
            ]),
            ("C14.2", "Robotics foundation models", "advanced", [
                "Vision language action sketch",
                "World models intuition",
                "Open research lists to watch",
                "Pi-zero style architectures sketch",
                "Mobile robot navigation models sketch",
            ]),
            ("C14.3", "Industrial AI edge", "intermediate", [
                "Plant floor copilots and MCP",
                "Edge inference constraints",
                "Human override on machinery",
                "Audit trails for physical actions",
            ]),
            ("C14.4", "Futuristic tools radar", "beginner", [
                "How to evaluate hype",
                "Personal radar board weekly",
                "What to ignore this quarter",
                "What to lab this quarter",
            ]),
        ],
    },
    {
        "id": "D15",
        "name": "Product Research & Free Share",
        "blurb": "Portfolio systems, research habits, ship free packs at UC quality bar.",
        "chapters": [
            ("C15.1", "Portfolio that hires", "intermediate", [
                "Three serious systems beat twenty toys",
                "Production RAG project shape",
                "Workflow agent project shape",
                "Observability dashboard project shape",
                "Document failures as portfolio",
            ]),
            ("C15.2", "Research OS", "beginner", [
                "Paper triage method",
                "Reproduce tiny",
                "Note taking with RTMA",
                "Avoid certificate theater",
            ]),
            ("C15.3", "Ship free universities", "beginner", [
                "Browser friendly size rule",
                "README for strangers",
                "GitHub Release checklist",
                "Sibling pack strategy",
                "Linktree after Release",
            ]),
        ],
    },
    {
        "id": "D16",
        "name": "Capstone Lifetime Mastery",
        "blurb": "Multi-year mastery loops, capstones, coaching agents.",
        "chapters": [
            ("C16.1", "Capstone tracks", "advanced", [
                "Capstone domain coach with citations",
                "Capstone personal Hermes coach",
                "Capstone voice UC braid",
                "Capstone robotics curiosity sim",
                "Capstone free pack vNext ship",
            ]),
            ("C16.2", "Lifetime operating system", "beginner", [
                "Quarterly skill review",
                "Weekly canaries forever",
                "Year map beginner to operator",
                "Teaching as mastery multiplier",
                "Keep the loop after any course ends",
            ]),
        ],
    },
    {
        "id": "D17",
        "name": "Glossary Interview FAQ Warroom",
        "blurb": "Quick reference, interview answers, honest FAQ.",
        "chapters": [
            ("C17.1", "Glossary core", "beginner", [
                "Token", "Context window", "Hallucination", "RTMA", "LICC",
                "Tool call", "Agent", "RAG", "Eval", "MCP", "Embedding",
                "Temperature", "Prompt injection", "Structured output",
                "Human approval gate", "Mock brain", "Pass rate", "Quantization",
                "Fallback chain", "Context engineering", "LLMOps", "VLA",
                "World model", "Hermes Agent", "Canary suite", "Fail closed",
                "Side effect", "Sandbox", "Scorecard", "Circuit breaker",
            ]),
            ("C17.2", "Interview bank", "intermediate", [
                "Why trust your AI work",
                "Local vs cloud choice",
                "Stop agent damage",
                "Catch hallucinations",
                "Walk through golden slice",
                "Model upgrade process",
                "Eval a demo",
                "Permissions perimeter story",
                "Explain RTMA to non engineer",
                "Portfolio three systems",
            ]),
            ("C17.3", "FAQ", "beginner", [
                "Is this free",
                "Need Mac Mini",
                "Need Ollama",
                "Only for UC people",
                "Replace official docs",
                "Why not giant HTML",
                "Commercial use MIT",
                "Includes model weights",
                "Certificate",
                "Mock brain cheating",
                "How to contribute",
                "Where is UC pack",
                "Hermes required",
                "Robotics required",
                "How updates work",
            ]),
        ],
    },
]


# Extra mechanism banks for richer generated bodies
MECHANISM_BANK = {
    "default": [
        "State the mechanism in one sentence.",
        "Name the failure mode if you skip it.",
        "Write the RTMA fields you would capture.",
        "Define GREEN in observable terms.",
    ],
    "security": [
        "Permissions default deny.",
        "Log without secrets.",
        "Human approval for side effects.",
        "Falsifier: what proves the control works?",
    ],
    "lab": [
        "Minimal experiment this week.",
        "Metric to record.",
        "Artifact path convention.",
        "Rollback if it fails.",
    ],
}

VENDOR_NOTES = {
    "OpenAI": "Strong ecosystem, tools, structured outputs — pin model ids and track cost.",
    "Anthropic": "Long-context and careful tool use patterns popular for agents — still need evals.",
    "Google": "Gemini multimodal + Google cloud glue — watch data residency and quotas.",
    "xAI": "Grok API and agent tooling in the xAI stack — treat like any production vendor.",
    "Local open-weight": "Ollama/llama.cpp/MLX — privacy and offline; capability varies by size.",
}

# Next-level internal curriculum grammar. These labels are implementation aids,
# not decorative public copy: teach the invariant, isolate exceptions, derive a
# working case, then try to disprove it with evidence.
PEDAGOGY_GRAMMAR = {
    "general_rule": "Teach the vendor-neutral mechanism first.",
    "exception": "Name where the rule fails or a provider differs.",
    "derivation": "Walk one input through every state transition.",
    "reason_check": "Reject reasons that have no observable support.",
    "ontology_map": "Separate object, property, relation, event, and evidence.",
    "stack_map": "Move from data and compute through model, context, tools, product, and governance.",
}

MIGRATION_LADDERS = {
    "local_to_cloud": ["deterministic fixture", "local model", "provider adapter", "cloud canary", "routed production"],
    "prompt_system": ["instruction", "template", "structured contract", "versioned suite", "release gate"],
    "rag": ["keyword", "dense retrieval", "hybrid", "reranking", "citation eval", "production monitoring"],
    "agent": ["single tool", "bounded loop", "approval gates", "trace", "eval", "rollback"],
    "voice": ["text", "STT", "LLM/tools", "TTS", "latency budget", "human handoff"],
}

REVIEW_SCHEDULE = ("1h", "24h", "7d", "30d", "90d")
