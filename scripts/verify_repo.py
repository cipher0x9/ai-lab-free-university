#!/usr/bin/env python3
"""Repository-wide offline verification for AI Lab Free University.

Checks source syntax, JSON, generated HTML structure, local links, dependency
boundaries, English public surface, brand/proof invariants, and optional
before/after byte growth. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import py_compile
import re
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.external_dependencies: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "script" and values.get("src", "").startswith(("http://", "https://", "//")):
            self.external_dependencies.append(values["src"] or "")
        if tag == "link" and values.get("href", "").startswith(("http://", "https://", "//")):
            self.external_dependencies.append(values["href"] or "")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"unexpected </{tag}>")
            return
        if self.stack[-1] != tag:
            self.errors.append(f"expected </{self.stack[-1]}> before </{tag}>")
            return
        self.stack.pop()


def tracked_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts)


def parse_before_sizes(path: Path) -> dict[str, int]:
    sizes: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        size, raw = line.split(" ", 1)
        key = raw[2:] if raw.startswith("./") else raw
        sizes[key] = int(size)
    return sizes


def strip_code(text: str) -> str:
    """Remove fenced and inline code so Python/JS index syntax is not parsed as MD links."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`\n]+`", "", text)
    return text


def local_link_errors(path: Path, text: str) -> list[str]:
    errors = []
    text = strip_code(text)
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip().strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#", "file:")):
            continue
        clean = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if clean and not (path.parent / clean).resolve().exists():
            errors.append(f"{path.relative_to(ROOT)} -> {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before-sizes", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    files = tracked_files()

    with tempfile.TemporaryDirectory(prefix="ai-lab-pycache-") as cache:
        for path in [p for p in files if p.suffix == ".py"]:
            try:
                py_compile.compile(str(path), cfile=str(Path(cache) / (path.name + ".pyc")), doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(str(exc))

    for path in [p for p in files if p.suffix == ".json"]:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # verification should report path and parser reason
            errors.append(f"JSON {path.relative_to(ROOT)}: {exc}")

    for path in [p for p in files if p.suffix == ".html"]:
        text = path.read_text(encoding="utf-8")
        if len(re.findall(r"<!doctype\s+html", text, flags=re.I)) != 1:
            errors.append(f"DOCTYPE count != 1: {path.relative_to(ROOT)}")
        hp = StructureParser()
        hp.feed(text)
        hp.close()
        if hp.errors or hp.stack:
            errors.append(f"HTML {path.relative_to(ROOT)}: {hp.errors[:3]} open={hp.stack[-5:]}")
        if hp.external_dependencies:
            errors.append(f"external HTML dependency {path.relative_to(ROOT)}: {hp.external_dependencies}")
        if "RTMA" not in text or "CYPHER0X9" not in text:
            errors.append(f"brand/proof invariant missing: {path.relative_to(ROOT)}")

    for path in [p for p in files if p.suffix == ".md"]:
        text = path.read_text(encoding="utf-8")
        errors.extend(local_link_errors(path, text))

    public = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files if p.suffix in {".md", ".html"})
    if re.search(r"[\u0900-\u097f]", public):
        errors.append("Devanagari found on public Markdown/HTML surface")
    for required in ("Run", "Trace", "Metric", "Artifact", "learn while building", "1 hour", "90 days"):
        if required.lower() not in public.lower():
            errors.append(f"public learning invariant missing: {required}")

    if args.before_sizes:
        before = parse_before_sizes(args.before_sizes)
        now = {str(p.relative_to(ROOT)): p.stat().st_size for p in files}
        missing = sorted(set(before) - set(now))
        if missing:
            errors.append(f"original files missing: {missing}")
        shrunk = sorted((name, size, now[name]) for name, size in before.items() if name in now and now[name] < size)
        if shrunk:
            errors.append(f"files shrank: {shrunk}")

    if errors:
        print("VERIFY: RED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VERIFY: GREEN · files={len(files)} · python/json/html/links/offline/brand/growth")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
