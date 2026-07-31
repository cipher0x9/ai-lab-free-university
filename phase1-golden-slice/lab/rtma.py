#!/usr/bin/env python3
"""RTMA helpers — Run · Trace · Metric · Artifact.

Mentor note: this is the AI twin of UC LICC (Leg · ID · Counter · Capture).
Every lab writes one JSON artifact so failures are evidence, not vibes.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SLICE_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = SLICE_ROOT / "artifacts"
REPORTS = SLICE_ROOT / "reports"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_run_id(prefix: str = "run") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


def ensure_dirs() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)


def write_artifact(name: str, payload: dict[str, Any]) -> Path:
    ensure_dirs()
    path = ARTIFACTS / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_report(name: str, text: str) -> Path:
    ensure_dirs()
    path = REPORTS / name
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    return path


class RTMA:
    """Collect one lab step as RTMA evidence."""

    def __init__(self, lab_name: str) -> None:
        self.lab_name = lab_name
        self.run_id = new_run_id(lab_name.replace(" ", "-")[:24])
        self.started = time.perf_counter()
        self.started_at = utc_now()
        self.trace: list[dict[str, Any]] = []
        self.metrics: dict[str, Any] = {}
        self.artifacts: list[str] = []
        self.status = "running"
        self.notes: list[str] = []

    def add_trace(self, event: str, **data: Any) -> None:
        self.trace.append({"t": utc_now(), "event": event, **data})

    def set_metric(self, key: str, value: Any) -> None:
        self.metrics[key] = value

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def finish(self, status: str = "ok") -> dict[str, Any]:
        elapsed_ms = round((time.perf_counter() - self.started) * 1000, 2)
        self.status = status
        self.metrics.setdefault("elapsed_ms", elapsed_ms)
        payload = {
            "schema": "ai-lab-free-university/rtma/v1",
            "lab": self.lab_name,
            "run_id": self.run_id,
            "status": self.status,
            "started_at": self.started_at,
            "finished_at": utc_now(),
            "run": {
                "cwd": str(Path.cwd()),
                "python": os.sys.version.split()[0],
                "host_env": {
                    "OLLAMA_HOST": os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"),
                    "OLLAMA_MODEL": os.environ.get("OLLAMA_MODEL", "llama3.2:3b"),
                },
            },
            "trace": self.trace,
            "metric": self.metrics,
            "artifact": self.artifacts,
            "notes": self.notes,
            "falsifier": (
                "If elapsed_ms is huge, answer is empty, or tool chain is missing — "
                "do not claim 'model is smart enough'."
            ),
        }
        path = write_artifact(f"{self.run_id}.json", payload)
        self.artifacts.append(str(path))
        payload["artifact"] = self.artifacts
        # rewrite with final artifact list
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return payload


def print_rtma_banner(title: str) -> None:
    print()
    print("=" * 64)
    print(f"  {title}")
    print("  RTMA = Run · Trace · Metric · Artifact")
    print("  (AI twin of UC LICC: Leg · ID · Counter · Capture)")
    print("=" * 64)
    print()
