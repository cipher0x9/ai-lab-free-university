# Research & local vault sources (v3 lifetime build)

Educational synthesis for curriculum design. No secrets. No customer data.

## Local Mac Mini vaults mined (structure + themes)

| Vault | What we took |
|-------|----------------|
| `Labs/Agentic_AI_University` | L0–L7 spine: foundations → single agent → frameworks → memory/RAG → multi-agent → MCP → evals → production |
| `Labs/Agentic_AI_Deployment_Engineer` | Production patterns, evals, powerhouse layout |
| `Labs/DevOps_AI_Deployment_Mastery` | Python/CI/containers/K8s/AI deploy/observability hardening layers |
| `Labs/GOOGLE_AI_ARSENAL` | Tool stack + recipe orientation |
| `UC-LAB-FREE-SHARE/prompts/02-ai-ml-future-lab` | 10 domains × expanded seeds (Foundations…Future stack) |
| `UC-LAB-FREE-SHARE/hermes/` | Coach/enrich patterns, human PROCEED, additive quality rule |
| `~/.hermes` + `dev/hermes-agent` | Existence of local Hermes install surface (configs never published) |

## Public industry themes (2026 discourse)

- Context engineering & tool-description quality  
- Eval design as taste (golden sets, judge calibration)  
- Model routing + fallback chains  
- Agent vs workflow vs single-call decision skill  
- Permissions as security perimeter for tool-using agents  
- RAG beyond naive chat-over-PDF (hybrid, rerank, observe)  
- Portfolio: few serious systems > many toys  

## Ecosystem radar

- **Hermes Agent** (Nous Research): open-source agent with persistent memory / skills; local ethos; education emerging in ecosystem  
- **MCP**: tool discovery standard across hosts/servers (including industrial copilots discourse)  
- **Agent frameworks**: LangGraph, CrewAI, PydanticAI, multi-agent patterns  
- **Physical AI / robotics**: VLA, world models, foundation-model robotics surveys  

## X / social note

Public posts emphasize that unattended high-privilege agent modes turn **permissions into perimeter**. Curriculum encodes this under Agents + Hermes safety chapters.

## Honesty

Vendor capabilities change. Pin official docs for production. This university teaches **mechanisms + RTMA**, not eternal API trivia.

## Primary-source engineering delta (checked 2026-08-05)

| Source | Curriculum binding | Release-sensitive check |
|---|---|---|
| [OpenAI model and migration guidance](https://developers.openai.com/api/docs/guides/latest-model) | Responses-style tools, bounded orchestration, eval before migration | model ids, parameters, pricing |
| [Google Cloud Vertex AI RAG Engine](https://cloud.google.com/blog/products/ai-machine-learning/introducing-vertex-ai-rag-engine/) | parse/chunk/retrieve/rerank, managed versus DIY comparison | regions, quotas, security controls |
| [Google Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/reasoning-engine/overview) | managed runtime, sessions, evaluation, observability | framework support and feature status |
| [xAI function calling](https://docs.x.ai/developers/tools/function-calling) | JSON-schema tools, local execution, returned results, parallel-call caution | supported models and tool behavior |
| [Anthropic sabotage evaluations](https://www.anthropic.com/research/sabotage-evaluations) | code sabotage, oversight, sandbagging, human-decision stress tests | study scope and model versions |

### Safety wording boundary

Controlled sabotage and agentic-misalignment evaluations create fictional or
isolated conditions to measure dangerous behavior. They do **not** establish that
a deployed model independently launched a real-world unsanctioned cyberattack.
The transferable engineering requirement is stronger permissions, sandboxes,
tripwires, audit traces, independent execution policy, and human release gates.

### Retrieval protocol

For every release-sensitive claim record: exact URL, page section, access date,
claim summary, what would falsify it, and which lesson/eval uses it. A router or
index page is a discovery aid, not proof of a product fact.
