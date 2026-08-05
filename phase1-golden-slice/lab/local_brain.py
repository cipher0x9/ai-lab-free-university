#!/usr/bin/env python3
"""Local brain client: Ollama if up, else honest mock.

Mentor note:
  In UC, if CUCM is down you still practice LICC with what you have.
  Here: if Ollama is not installed, we use a mock brain so RTMA still trains.
  Never pretend the mock is a real model.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
BACKEND_DECISION_FIELDS = ("privacy", "task_pass_rate", "p50_ms", "p95_ms", "cost_per_passed_task", "fallback")


@dataclass
class BrainReply:
    text: str
    backend: str  # "ollama" | "mock"
    model: str
    latency_ms: float
    raw: dict[str, Any] | None = None
    error: str | None = None

    def scorecard(self) -> dict[str, Any]:
        """Small provider-neutral record for later local/cloud comparisons."""
        return {
            "backend": self.backend,
            "model": self.model,
            "latency_ms": self.latency_ms,
            "answer_chars": len(self.text or ""),
            "has_error": self.error is not None,
            "required_decision_fields": BACKEND_DECISION_FIELDS,
        }


def ollama_alive(host: str = DEFAULT_HOST, timeout: float = 1.5) -> bool:
    try:
        req = urllib.request.Request(f"{host}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def list_models(host: str = DEFAULT_HOST, timeout: float = 3.0) -> list[str]:
    try:
        req = urllib.request.Request(f"{host}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return [m.get("name", "") for m in data.get("models", []) if m.get("name")]
    except Exception:
        return []


def _mock_reply(prompt: str, model: str) -> BrainReply:
    """Deterministic teaching replies for Phase 1 without Ollama."""
    p = prompt.lower()
    if "rtma" in p or "run · trace" in p or "run, trace" in p:
        text = (
            "RTMA means Run, Trace, Metric, Artifact. "
            "It is the AI version of UC LICC (Leg, ID, Counter, Capture). "
            "You prove work with evidence, not vibes."
        )
    elif "hallucin" in p:
        text = (
            "A hallucination is a fluent answer that is not grounded in evidence. "
            "Catch it with evals, citations, and falsifiers — not confidence."
        )
    elif "tool" in p and ("call" in p or "schema" in p):
        text = (
            "A tool call is when the model requests a structured function "
            "instead of inventing the result. Schema in, result out, log the chain."
        )
    elif "token" in p:
        text = (
            "A token is a chunk of text the model reads or writes — "
            "not always a full word. Context window is the token budget for one request."
        )
    elif "rag" in p or "retrieval" in p:
        text = (
            "RAG retrieves approved evidence before generation, carries resolvable citations, "
            "scores retrieval separately, and fails closed when no evidence is found."
        )
    elif "agent" in p or "approval" in p:
        text = (
            "A safe agent is a bounded observe-act-correct-verify loop with typed tools, "
            "hard budgets, traceable approvals, assertions, and an explicit stop reason."
        )
    elif "hello" in p or "ping" in p or "say" in p:
        text = (
            "Hello from the AI Lab Free University mock local brain. "
            "Install Ollama later for a real local model; RTMA practice still counts."
        )
    else:
        text = (
            "Mock local brain: I only answer Phase-1 teaching facts. "
            "Install Ollama for open-ended generation. "
            f"(You asked: {prompt[:120]})"
        )
    return BrainReply(
        text=text,
        backend="mock",
        model=f"mock::{model}",
        latency_ms=0.5,
        raw={"mock": True},
        error=None,
    )


def generate(
    prompt: str,
    *,
    host: str = DEFAULT_HOST,
    model: str = DEFAULT_MODEL,
    system: str | None = None,
    timeout: float = 60.0,
    prefer_mock: bool = False,
) -> BrainReply:
    import time

    if prefer_mock or not ollama_alive(host=host):
        return _mock_reply(prompt, model)

    body: dict[str, Any] = {
        "model": model,
        "prompt": prompt if not system else f"System: {system}\n\nUser: {prompt}",
        "stream": False,
        "options": {"temperature": 0.2},
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{host}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        latency = round((time.perf_counter() - t0) * 1000, 2)
        return BrainReply(
            text=(raw.get("response") or "").strip(),
            backend="ollama",
            model=model,
            latency_ms=latency,
            raw=raw,
            error=None,
        )
    except urllib.error.HTTPError as e:
        latency = round((time.perf_counter() - t0) * 1000, 2)
        # common: model not pulled
        mock = _mock_reply(prompt, model)
        return BrainReply(
            text=mock.text + f"\n[fallback after Ollama HTTP {e.code}]",
            backend="mock",
            model=f"mock::{model}",
            latency_ms=latency,
            raw=None,
            error=f"ollama_http_{e.code}: {e.reason}",
        )
    except Exception as e:
        latency = round((time.perf_counter() - t0) * 1000, 2)
        mock = _mock_reply(prompt, model)
        return BrainReply(
            text=mock.text + f"\n[fallback after error: {type(e).__name__}]",
            backend="mock",
            model=f"mock::{model}",
            latency_ms=latency,
            raw=None,
            error=f"{type(e).__name__}: {e}",
        )
