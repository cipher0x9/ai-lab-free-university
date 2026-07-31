#!/usr/bin/env python3
"""Generate lifetime-mastery section corpus from taxonomy + research banks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from taxonomy import DIVISIONS, VENDOR_NOTES  # noqa: E402

OUT_JSON = Path(__file__).resolve().parent / "lifetime_sections.json"
OUT_META = Path(__file__).resolve().parent / "lifetime_meta.json"

RESEARCH_SOURCES = [
    {
        "title": "2026 AI engineer skill discourse (public X)",
        "points": [
            "Context engineering and tool-description quality dominate output quality.",
            "Eval design builds taste; golden sets and judge calibration matter.",
            "Model routing + fallback chains beat defaulting to one frontier model.",
            "Permissions become security perimeter once agents run tools unattended.",
        ],
    },
    {
        "title": "Local vaults on this Mac Mini",
        "points": [
            "Agentic_AI_University layers L0–L7 (foundations → production).",
            "DevOps_AI_Deployment_Mastery L0–L9 for ship discipline.",
            "UC prompts/02: Foundations, Classical ML, DL, GenAI, Agents, Voice, MLOps, Mac Mini, Future, Product.",
            "Hermes wiring: coach + enrich with human PROCEED; never silent rewrite.",
        ],
    },
    {
        "title": "Ecosystem radar",
        "points": [
            "Hermes Agent (Nous Research): persistent memory, skills, local ethos.",
            "Agent frameworks: LangGraph, CrewAI, PydanticAI, AutoGen-style multi-agent.",
            "MCP: standard tool discovery across apps and industrial systems.",
            "Robotics / Physical AI: VLA models, world models, sim-to-real, edge safety.",
        ],
    },
]


def slug(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:48]


def body_for(division: dict, chapter_id: str, chapter_name: str, title: str, level: str, idx: int) -> str:
    did = division["id"]
    dname = division["name"]
    bits = [
        f"**Division:** {did} · {dname}",
        f"**Chapter:** {chapter_id} · {chapter_name}",
        f"**Level:** {level}",
        "",
        f"## {title}",
        "",
    ]

    # Tailored openers by division
    openers = {
        "D00": "This campus lesson builds the operator OS you will reuse for decades.",
        "D01": "Engineering first: AI without solid software habits becomes demo theater.",
        "D02": "Languages — code and human — multiply what models and teams can ship.",
        "D03": "Classical ML thinking still catches bad data and weak metrics under LLM hype.",
        "D04": "Generative systems are powerful stochastic tools — measure them like systems.",
        "D05": "Your Mac Mini (or laptop) is a private classroom and sometimes a production edge.",
        "D06": "Vendors rent brains. You own architecture, cost, and liability.",
        "D07": "Most quality lives in context design and contracts, not mystical wording.",
        "D08": "Knowledge work needs retrieval and memory — with citations and fail-closed defaults.",
        "D09": "Agents are privileged loops. Design permissions before personality.",
        "D10": "Hermes is a personal agent OS candidate: coach, enrich, schedule — with gates.",
        "D11": "Evals and safety are how taste becomes engineering — not vibes.",
        "D12": "Voice is a real-time system: media path + models + human escape hatches.",
        "D13": "Models are components inside products. Ship the product.",
        "D14": "Physical AI raises the cost of mistakes — foresight track, lab carefully.",
        "D15": "Portfolio and free-share discipline turn learning into public good.",
        "D16": "Mastery is a loop measured in quarters, not binge weekends alone.",
        "D17": "Quick reference: say it clean, ship it honest.",
    }
    bits.append(openers.get(did, "Mentor note: mechanisms over hype."))
    bits.append("")

    # Mechanism block
    bits.append("### Mechanism")
    if "token" in title.lower():
        bits.append("A token is a model text chunk. Context window is the shared input/output budget. Count roughly; measure exactly when cost or failures matter.")
    elif "rag" in title.lower() or "retrieval" in title.lower() or "embedding" in title.lower():
        bits.append("Retrieve relevant evidence first, then generate. Separate retrieval metrics from generation metrics. Cite paths/ids or fail closed.")
    elif "hermes" in title.lower():
        bits.append(
            "Treat Hermes as scheduler + coach + enricher against a **source of truth** folder. "
            "Daily artifacts, human PROCEED before publishing rewrites, no outbound messages without approval. "
            "Local ethos: data on your machine when possible."
        )
    elif "mcp" in title.lower():
        bits.append("MCP standardizes how hosts discover and call tools/resources from servers. Trust the server like you trust a plugin: least privilege, audit, pin versions.")
    elif "robot" in title.lower() or "physical" in title.lower() or "vla" in title.lower() or "world model" in title.lower():
        bits.append(
            "Embodied systems close the loop through sensors and actuators. "
            "Sim-to-real gaps, latency, and irreversible actions demand stronger HITL than chatbots."
        )
    elif "ollama" in title.lower() or "local" in title.lower() or "mac mini" in title.lower():
        bits.append("Local runners (Ollama/llama.cpp/MLX) serve private models. Default teaching port for Ollama HTTP is 11434. Disclose mock vs real backends.")
    elif any(v.lower() in title.lower() for v in ("openai", "anthropic", "gemini", "grok", "azure", "bedrock")):
        for v, note in VENDOR_NOTES.items():
            if v.split()[0].lower() in title.lower() or v.lower() in title.lower():
                bits.append(note)
                break
        else:
            bits.append("Pin model ids, log request ids/tokens/cost, validate structured outputs, keep keys out of git.")
    elif "permission" in title.lower() or "yolo" in title.lower() or "approval" in title.lower():
        bits.append(
            "Once an agent can execute tools, **permissions are perimeter**. "
            "Unattended high-privilege mode is an incident design smell. Default deny side effects."
        )
    elif "eval" in title.lower() or "canary" in title.lower() or "golden" in title.lower():
        bits.append("Fixed suites with thresholds beat demo screenshots. Canaries gate releases. Version the suite with the product.")
    elif "prompt" in title.lower() or "context" in title.lower():
        bits.append("Prompts are contracts. Context engineering allocates scarce attention budget across instructions, tools, and retrieved evidence.")
    elif "python" in title.lower() or "git" in title.lower() or "api" in title.lower() or "test" in title.lower():
        bits.append("Software fundamentals: clear modules, tests, retries, and secrets hygiene. AI features inherit these debts.")
    else:
        bits.append(
            f"Focus: **{title}**. Learn the definition, the operator analogy, one minimal experiment, "
            "and the metric that proves you are not guessing."
        )

    bits.append("")
    bits.append("### Minimal experiment")
    bits.append(
        f"1. Read this lesson and restate it in your own words.\n"
        f"2. Run or design a 15–30 minute lab related to **{title}**.\n"
        f"3. Write an RTMA artifact under `phase1-golden-slice/artifacts/` or your notes folder.\n"
        f"4. Mark studied in the university HTML only if you can teach it cold."
    )
    bits.append("")
    bits.append("### Failure modes")
    bits.append(
        f"- Skipping measurement and calling **{title}** 'done'\n"
        "- Confusing fluency with correctness\n"
        "- Leaking secrets into prompts, logs, or git\n"
        "- Copying framework demos without permissions or evals"
    )
    bits.append("")
    bits.append("### RTMA")
    bits.append(
        f"| Element | For this lesson |\n"
        f"|---------|----------------|\n"
        f"| **Run** | Command, notebook, Hermes task, or reading+quiz for *{title}* |\n"
        f"| **Trace** | Logs, tool chain, or notes timeline |\n"
        f"| **Metric** | Latency, pass rate, cost, or checklist completion |\n"
        f"| **Artifact** | File path you can reopen next month |\n"
    )
    bits.append("")
    bits.append("### GREEN")
    bits.append(
        f"You can explain **{title}** without notes, show one artifact, and name one falsifier "
        f"that would kill a false claim of mastery."
    )
    bits.append("")
    bits.append("### Interview 30s")
    bits.append(
        f"{title}: I treat it as an operator skill with RTMA evidence, not a buzzword. "
        f"I can show a metric and an artifact."
    )
    if idx % 7 == 0:
        bits.append("")
        bits.append("### Research braid")
        bits.append(
            "Industry 2026 emphasis: context engineering, eval taste, routing/fallbacks, "
            "and agent permissions-as-perimeter. Local vaults on this machine map L0→production "
            "and UC free-share discipline."
        )
    return "\n".join(bits)


def generate() -> tuple[list[dict], dict]:
    sections: list[dict] = []
    # Research preface sections
    for i, src in enumerate(RESEARCH_SOURCES, 1):
        body = [
            f"# Research note {i}: {src['title']}",
            "",
            "Educational synthesis for curriculum design (not legal/security advice).",
            "",
        ]
        for p in src["points"]:
            body.append(f"- {p}")
        body.append("")
        body.append("### RTMA")
        body.append("Run: read note · Trace: source list · Metric: actions taken · Artifact: this section marked studied.")
        sections.append(
            {
                "id": f"RS-{i:02d}",
                "division": "D00",
                "division_name": "Campus & Operator OS",
                "chapter": "C00.0",
                "chapter_name": "Research braid (living)",
                "title": src["title"],
                "level": "beginner",
                "body": "\n".join(body),
                "tags": "research braid " + src["title"].lower(),
            }
        )

    for div in DIVISIONS:
        for chapter_id, chapter_name, default_level, lessons in div["chapters"]:
            for i, title in enumerate(lessons, 1):
                level = default_level
                sid = f"{chapter_id.replace('.', '')}-{i:02d}"
                # unique id
                sid = f"{div['id']}-{slug(chapter_id)}-{i:02d}"
                sections.append(
                    {
                        "id": sid,
                        "division": div["id"],
                        "division_name": div["name"],
                        "chapter": chapter_id,
                        "chapter_name": chapter_name,
                        "title": title,
                        "level": level,
                        "body": body_for(div, chapter_id, chapter_name, title, level, i),
                        "tags": f"{div['id']} {chapter_id} {title}".lower(),
                    }
                )

    # Expand with numbered deep-dives per major division (lifetime density)
    deep_topics = {
        "D04": [
            "KV cache intuition",
            "Prompt caching economics",
            "Speculative decoding sketch",
            "Mixture of experts intuition",
            "Tokenizer mismatch bugs",
        ],
        "D06": [
            "Comparing latency across vendors",
            "Data retention checklist per vendor",
            "Enterprise VPC private endpoints sketch",
            "Batch APIs vs realtime",
        ],
        "D09": [
            "Tool description writing workshop",
            "Long horizon tasks budgets",
            "Memory write policies",
            "Agent eval harness shape",
            "Browser tool risks",
            "Code execution sandbox risks",
        ],
        "D10": [
            "Morning coach prompt seed",
            "Weekly review prompt seed",
            "Enrichment PR checklist",
            "Hermes + UC pack citations rule",
            "Hermes + AI pack dual enrollment",
        ],
        "D11": [
            "RAGAS style metrics sketch",
            "Guardrails libraries map",
            "Red team prompt library starter",
            "SEV levels for AI incidents",
        ],
        "D14": [
            "Teleoperation vs autonomy",
            "Dataset collection ethics for robots",
            "Digital twin sketch",
            "Firmware update caution",
        ],
        "D01": [
            "Regex for log forensics",
            "Makefile as lab runner",
            "Pre-commit hooks for secrets",
        ],
        "D05": [
            "Model card reading",
            "GGUF vs MLX formats sketch",
            "Multi-model lab routing local",
        ],
        "D08": [
            "Parent document retriever sketch",
            "Graph RAG curiosity",
            "Eval sets for citation faithfulness",
        ],
        "D12": [
            "MOS and latency together",
            "SIP plus AI handoff sketch",
            "Agent assist vs autonomous bot",
        ],
        "D13": [
            "Feature flags for prompts",
            "Cost attribution per tenant",
            "Offline HTML free packs as product",
        ],
        "D15": [
            "Writing public ADRs for AI systems",
            "Open source contribution path",
            "Teaching cohort with pinned zips",
        ],
        "D16": [
            "12-month mastery calendar",
            "Accountability partner protocol",
            "Public build-in-public rules",
        ],
    }

    for did, titles in deep_topics.items():
        div = next(d for d in DIVISIONS if d["id"] == did)
        for i, title in enumerate(titles, 1):
            sections.append(
                {
                    "id": f"{did}-deep-{i:02d}",
                    "division": did,
                    "division_name": div["name"],
                    "chapter": f"{did}.X",
                    "chapter_name": "Deep dives & operator workshops",
                    "title": title,
                    "level": "advanced" if i % 2 == 0 else "intermediate",
                    "body": body_for(div, f"{did}.X", "Deep dives & operator workshops", title, "intermediate", i),
                    "tags": f"{did} deep {title}".lower(),
                }
            )

    # Dedup ids
    seen = set()
    uniq = []
    for s in sections:
        if s["id"] in seen:
            s["id"] = s["id"] + "-b"
        seen.add(s["id"])
        uniq.append(s)

    meta = {
        "title": "AI Lab Free University",
        "version": "v3-lifetime",
        "tagline": "Lifetime mastery: local + cloud AI, agents, evals, Hermes, future stack",
        "subtitle": "Full-scale free university · evidence-first · general audience · Mac Mini ready",
        "author": "CYPHER0X9",
        "sections": len(uniq),
        "divisions": len(DIVISIONS),
        "sources": [r["title"] for r in RESEARCH_SOURCES],
    }
    return uniq, meta


def main() -> None:
    sections, meta = generate()
    OUT_JSON.write_text(json.dumps(sections, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    OUT_META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta, indent=2))
    by = {}
    for s in sections:
        by[s["division"]] = by.get(s["division"], 0) + 1
    print("by_division", by)


if __name__ == "__main__":
    main()
