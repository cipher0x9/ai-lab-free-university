#!/usr/bin/env bash
# Verify AI Lab Free University free-pack quality bar.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLICE="$ROOT/phase1-golden-slice"
cd "$SLICE"

echo "▸ AI Lab Free University — verify free pack"
echo "  root: $ROOT"
echo

python3 lab/01_local_hello.py
echo
python3 lab/02_tool_call.py
echo
python3 lab/03_run_eval.py
echo
python3 lab/04_rtma_quiz.py
echo
python3 lab/05_run_eval_expanded.py
echo
python3 lab/06_rag_ablation.py
echo
python3 lab/07_agent_loop.py
echo
python3 lab/08_voice_latency_budget.py
echo

# Rebuild universities
if [[ -f "$ROOT/scripts/build_university_v4.py" ]]; then
  echo "▸ Building v4 PORTFOLIO university…"
  python3 "$ROOT/scripts/build_university_v4.py"
fi
if [[ -f "$ROOT/scripts/build_university_v3.py" ]]; then
  echo "▸ Building v3 LIFETIME (compat)…"
  python3 "$ROOT/scripts/build_university_v3.py" || true
fi

check_html() {
  local f="$1"
  local label="$2"
  if [[ ! -f "$f" ]]; then
    echo "✗ FAIL: missing $label ($f)"
    return 1
  fi
  local bytes
  bytes=$(wc -c < "$f" | tr -d ' ')
  local mb
  mb=$(python3 -c "print(round($bytes/1024/1024, 3))")
  echo "▸ $label size: ${mb} MB ($bytes bytes)"
  if [[ "$bytes" -gt 20971520 ]]; then
    echo "✗ FAIL: $label exceeds 20 MB free-share budget"
    return 1
  fi
  echo "✓ $label within browser-friendly budget"
}

check_html "$ROOT/university/v4-PORTFOLIO.html" "v4-PORTFOLIO.html"
check_html "$ROOT/university/v1-SLICE.html" "v1-SLICE.html"

# resource count gate
python3 - <<PY
import json
from pathlib import Path
root = Path("$ROOT")
p = root / "curriculum" / "resources_1000.json"
if p.exists():
    n = len(json.loads(p.read_text()))
    print(f"▸ resource links: {n}")
    if n < 1000:
        raise SystemExit(f"need >=1000 links, got {n}")
    print("✓ resource atlas >= 1000")
else:
    print("○ resources_1000.json missing (built inside v4)")
PY

# Zip refresh
mkdir -p "$ROOT/zips"
(
  cd "$ROOT/university"
  zip -9 -q "$ROOT/zips/v4-PORTFOLIO.html.zip" v4-PORTFOLIO.html
  [[ -f v3-LIFETIME.html ]] && zip -9 -q "$ROOT/zips/v3-LIFETIME.html.zip" v3-LIFETIME.html
  [[ -f v2-UNIVERSITY.html ]] && zip -9 -q "$ROOT/zips/v2-UNIVERSITY.html.zip" v2-UNIVERSITY.html
  zip -9 -q "$ROOT/zips/v1-SLICE.html.zip" v1-SLICE.html
)
echo "✓ zips refreshed under zips/"

# Required public surface files
for req in README.md START-HERE.md VISION.md LICENSE CONTRIBUTING.md SECURITY.md DOWNLOADS.md; do
  if [[ ! -f "$ROOT/$req" ]]; then
    echo "✗ FAIL: missing $req"
    exit 1
  fi
done
echo "✓ public surface files present"

# Repository-wide gates: syntax, JSON, HTML balance, local links, offline
# dependencies, English public surface, brand/proof invariants, and byte growth.
VERIFY_ARGS=()
if [[ -f /tmp/ai-lab-before-sizes.txt ]]; then
  VERIFY_ARGS+=(--before-sizes /tmp/ai-lab-before-sizes.txt)
fi
python3 "$ROOT/scripts/verify_repo.py" "${VERIFY_ARGS[@]}"
echo "✓ repository-wide structural and growth gates"

echo
echo "✓ FREE PACK VERIFY COMPLETE"
echo "  Open: university/v4-PORTFOLIO.html"
echo "  Share zip: zips/v4-PORTFOLIO.html.zip"
