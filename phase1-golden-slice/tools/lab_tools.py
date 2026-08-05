#!/usr/bin/env python3
"""Phase-1 lab tools — tiny, safe, auditable.

Permission model (mentor):
  Tools that change the outside world need human approval.
  These Phase-1 tools are pure compute / local catalog only.
"""

from __future__ import annotations

import ast
import operator
import re
from typing import Any, Callable

# Safe arithmetic for calculator tool
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    raise ValueError("only simple arithmetic is allowed")


def calc(expression: str) -> dict[str, Any]:
    """Evaluate a simple arithmetic expression safely."""
    expr = expression.strip()
    if not expr or len(expr) > 80:
        return {"ok": False, "error": "expression empty or too long"}
    if not re.fullmatch(r"[0-9+\-*/().% \t]+", expr):
        return {"ok": False, "error": "disallowed characters"}
    try:
        tree = ast.parse(expr, mode="eval")
        value = _eval_node(tree)
        return {"ok": True, "expression": expr, "result": value}
    except Exception as e:
        return {"ok": False, "error": str(e), "expression": expr}


# Tiny UC↔AI glossary (educational, not product docs)
UC_AI_GLOSSARY = {
    "rtma": (
        "Run · Trace · Metric · Artifact — evidence habit for AI labs; "
        "mirrors UC LICC (Leg · ID · Counter · Capture)."
    ),
    "licc": (
        "Leg · ID · Counter · Capture — UC troubleshooting grammar "
        "(path, identifiers, counters/metrics, packet/log capture)."
    ),
    "token": (
        "A token is a model text chunk (not always a full word). "
        "Context window = max tokens for one request."
    ),
    "hallucination": (
        "Fluent model output that is not grounded in evidence. "
        "Detect with evals, citations, and falsifiers."
    ),
    "tool call": (
        "Model requests a structured function instead of inventing the answer. "
        "Schema in → tool runs → result returns → log the chain."
    ),
    "rag": (
        "Retrieval-Augmented Generation: fetch relevant docs, then answer with citations. "
        "UC free pack is a strong first corpus for voice engineers."
    ),
    "ollama": (
        "Popular local LLM runner. Serves models on localhost (default port 11434). "
        "Great for Mac Mini lab privacy and offline practice."
    ),
    "sip": (
        "Session Initiation Protocol — signaling for VoIP sessions. "
        "Your UC superpower domain; later braid with Voice AI (STT/TTS)."
    ),
    "reranker": (
        "A second-stage scorer that reorders retrieved candidates. Compare retrieval quality, "
        "latency, and cost on the same query set before keeping it."
    ),
    "agent loop": (
        "Observe → validate → act → correct → verify under explicit turn, time, cost, "
        "tool, and approval boundaries."
    ),
    "human approval": (
        "A named person authorizes a specific external side effect; the approval id belongs in Trace."
    ),
}


def approval_required(effect: str) -> bool:
    """Default-deny classifier for side effects used in later teaching labs."""
    normalized = effect.strip().lower().replace("_", " ")
    side_effects = ("send", "post", "publish", "delete", "purchase", "trade", "deploy", "message")
    return any(word in normalized for word in side_effects)


def glossary_lookup(term: str) -> dict[str, Any]:
    key = term.strip().lower()
    # normalize mild variants
    key = key.replace("_", " ").replace("-", " ")
    if key in UC_AI_GLOSSARY:
        return {"ok": True, "term": key, "definition": UC_AI_GLOSSARY[key]}
    # fuzzy contains
    for k, v in UC_AI_GLOSSARY.items():
        if key in k or k in key:
            return {"ok": True, "term": k, "definition": v, "matched": "partial"}
    return {
        "ok": False,
        "term": key,
        "error": "unknown term",
        "known_terms": sorted(UC_AI_GLOSSARY.keys()),
    }


TOOL_SPECS: list[dict[str, Any]] = [
    {
        "name": "calc",
        "description": "Safe arithmetic calculator. Use for exact math; do not invent numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Arithmetic like 12*(3+4)/2",
                }
            },
            "required": ["expression"],
        },
        "requires_human_approval": False,
        "handler": "calc",
    },
    {
        "name": "glossary_lookup",
        "description": "Look up Phase-1 AI Lab / UC bridge terms from a fixed local glossary.",
        "parameters": {
            "type": "object",
            "properties": {
                "term": {
                    "type": "string",
                    "description": "Term such as RTMA, token, hallucination, SIP",
                }
            },
            "required": ["term"],
        },
        "requires_human_approval": False,
        "handler": "glossary_lookup",
    },
]


HANDLERS: dict[str, Callable[..., dict[str, Any]]] = {
    "calc": calc,
    "glossary_lookup": glossary_lookup,
}


def run_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name not in HANDLERS:
        return {"ok": False, "error": f"unknown tool: {name}"}
    spec = next(s for s in TOOL_SPECS if s["name"] == name)
    if spec.get("requires_human_approval"):
        return {"ok": False, "error": "human approval required — not auto-run"}
    try:
        return HANDLERS[name](**arguments)
    except TypeError as e:
        return {"ok": False, "error": f"bad arguments: {e}"}
