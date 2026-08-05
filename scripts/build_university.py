#!/usr/bin/env python3
"""Build offline university HTML from curriculum corpus.

Produces university/v2-UNIVERSITY.html — general audience free pack.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "curriculum"))
from corpus import META, SCHOOLS, SECTIONS, stats  # noqa: E402

OUT = ROOT / "university" / "v2-UNIVERSITY.html"

NEXT_LEVEL_SPINE = (
    "Learn while building · prove as you go · local → cloud → agents/evals · "
    "review at 1h → 24h → 7d → 30d → 90d"
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def body_to_html(body: str) -> str:
    """Minimal markdown-ish → HTML."""
    lines = body.split("\n")
    out: list[str] = []
    in_ul = False
    in_pre = False
    in_table = False
    table_rows: list[str] = []

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            return
        out.append('<div class="table-wrap"><table>')
        for i, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            tag = "th" if i == 0 else "td"
            # skip separator rows like ---|
            if all(set(c) <= set("-: ") and c for c in cells):
                continue
            out.append("<tr>" + "".join(f"<{tag}>{inline_fmt(c)}</{tag}>" for c in cells) + "</tr>")
        out.append("</table></div>")
        table_rows = []
        in_table = False

    def inline_fmt(t: str) -> str:
        import re

        t = esc(t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
        return t

    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            close_ul()
            flush_table()
            if not in_pre:
                out.append("<pre>")
                in_pre = True
            else:
                out.append("</pre>")
                in_pre = False
            continue
        if in_pre:
            out.append(esc(line) + "\n")
            continue
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            close_ul()
            in_table = True
            table_rows.append(line)
            continue
        else:
            if in_table:
                flush_table()

        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_fmt(line[2:])}</li>")
            continue
        close_ul()
        if not line.strip():
            continue
        # numbered
        import re

        if re.match(r"^\d+\.\s", line):
            if not out or not out[-1].startswith("<ol"):
                # simple: use <p> for numbered to avoid nested state complexity
                out.append(f"<p>{inline_fmt(line)}</p>")
            else:
                out.append(f"<p>{inline_fmt(line)}</p>")
            continue
        out.append(f"<p>{inline_fmt(line)}</p>")

    close_ul()
    flush_table()
    if in_pre:
        out.append("</pre>")
    return "\n".join(out)


def build() -> Path:
    school_name = {s["id"]: s["name"] for s in SCHOOLS}
    school_job = {s["id"]: s["job"] for s in SCHOOLS}

    # nav groups
    nav_html = []
    for sc in SCHOOLS:
        ids = [s for s in SECTIONS if s["school"] == sc["id"]]
        if not ids:
            continue
        nav_html.append(f'<div class="nav-group"><div class="nav-h">{esc(sc["id"])} · {esc(sc["name"])} <span>{len(ids)}</span></div>')
        for s in ids:
            nav_html.append(
                f'<a class="nav" data-id="{esc(s["id"])}" href="#{esc(s["id"])}">{esc(s["id"])} {esc(s["title"])}</a>'
            )
        nav_html.append("</div>")

    cards = []
    for s in SECTIONS:
        green = f'<div class="green"><strong>GREEN:</strong> {esc(s["green"])}</div>' if s.get("green") else ""
        iv = f'<div class="iv"><strong>Interview 30s:</strong> {esc(s["interview30"])}</div>' if s.get("interview30") else ""
        cards.append(
            f'''<article class="sec" id="{esc(s["id"])}" data-school="{esc(s["school"])}" data-level="{esc(s["level"])}" data-search="{esc((s["id"]+" "+s["title"]+" "+s["tags"]+" "+s["body"]).lower()[:800])}">
  <div class="meta"><span class="id">{esc(s["id"])}</span><span class="school">{esc(s["school"])} · {esc(school_name.get(s["school"],""))}</span><span class="lvl">{esc(s["level"])}</span></div>
  <h2>{esc(s["title"])}</h2>
  <div class="body">{body_to_html(s["body"])}</div>
{green}{iv}
  <div class="sec-actions"><button type="button" class="btn mark" data-mark="{esc(s["id"])}">Mark studied</button><button type="button" class="btn copy" data-copy="{esc(s["id"])}">Copy id</button></div>
</article>'''
        )

    school_pills = "".join(
        f'<button type="button" class="pill" data-filter-school="{esc(sc["id"])}">{esc(sc["id"])} {esc(sc["name"])}</button>'
        for sc in SCHOOLS
        if any(s["school"] == sc["id"] for s in SECTIONS)
    )

    st = stats()
    payload = {
        "meta": META,
        "stats": st,
        "schools": SCHOOLS,
        "section_ids": [s["id"] for s in SECTIONS],
        "next_level_spine": NEXT_LEVEL_SPINE,
    }

    doc = f"""<!DOCTYPE html>
<html lang="en" data-theme="night">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect rx='14' width='64' height='64' fill='%236366F1'/%3E%3Ctext x='32' y='44' text-anchor='middle' font-size='38'%3E%E2%9C%A6%3C/text%3E%3C/svg%3E"/>
<meta name="description" content="{esc(META['title'])} {esc(META['version'])} — {esc(META['tagline'])}. Free offline AI university."/>
<meta name="color-scheme" content="light dark"/>
<title>{esc(META['title'])} {esc(META['version'])} — Offline Free University</title>
<style>
:root{{
  --bg:#070b16;--card:#121a2e;--ink:#EAF0FF;--muted:#8FA0BF;--line:#24314d;--border:#2a3858;
  --a1:#38BDF8;--a2:#A78BFA;--a3:#34D399;--a4:#F472B6;--warn:#FBBF24;--bad:#F87171;
  --shadow:0 12px 40px rgba(0,0,0,.4);--side:300px;
  --font:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  --display:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;
}}
@media print{{article.sec{{break-inside:avoid;counter-increment:page}}article.sec::after{{content:"AI Lab · page " counter(page);color:#6366F1;font-size:10px}}}}
html[data-theme=warm]{{--bg:#FFF6EB;--card:#fff;--ink:#1A1208;--muted:#7A6548;--line:#F0D4B0;--border:#E8C9A0;--a1:#E8820C;--a2:#8B5CF6;--a3:#159947;--a4:#E11D48;--shadow:0 8px 28px rgba(26,18,8,.08)}}
html[data-theme=cobalt]{{--bg:#061422;--card:#0c2740;--ink:#E8F3FF;--muted:#8EB6D4;--line:#1a4568;--border:#1e4a6a;--a1:#38BDF8;--a2:#60A5FA;--a3:#2DD4BF}}
html[data-theme=forest]{{--bg:#F2F7F1;--card:#fff;--ink:#14201A;--muted:#5B6E62;--line:#C9D9CE;--border:#C9D9CE;--a1:#2F6F4E;--a2:#3F8F62;--a3:#0F9B8E;--shadow:0 8px 24px rgba(20,32,26,.08)}}
html[data-theme=aurora]{{--bg:#0b0818;--card:#16122c;--ink:#F6F1FF;--muted:#A99BC8;--line:#2d2650;--border:#352e5c;--a1:#22D3EE;--a2:#C084FC;--a3:#4ADE80}}
html[data-theme=slate]{{--bg:#0f1419;--card:#1a222c;--ink:#E7EEF7;--muted:#9AA8B6;--line:#2a3441;--border:#334155;--a1:#94A3B8;--a2:#38BDF8;--a3:#4ADE80}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{max-width:100%;overflow-x:hidden}}
body{{font-family:var(--font);background:var(--bg);color:var(--ink);line-height:1.55;font-size:15px}}
a{{color:var(--a1)}}
.banner{{background:linear-gradient(90deg,#0284c7,#7c3aed,#db2777);color:#fff;text-align:center;padding:8px 12px;font-weight:800;font-size:12px;letter-spacing:.03em}}
.top{{position:sticky;top:0;z-index:60;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 12px;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--border)}}
.brand{{font-family:var(--display);font-weight:900;font-size:1.05rem;background:linear-gradient(90deg,var(--a1),var(--a2));-webkit-background-clip:text;color:transparent}}
.brand small{{display:block;font-family:var(--font);font-size:11px;font-weight:600;color:var(--muted);-webkit-text-fill-color:var(--muted)}}
.spacer{{flex:1}}
.btn,select,input[type=search]{{border:1px solid var(--border);background:var(--card);color:var(--ink);border-radius:10px;padding:7px 10px;font:inherit;font-size:13px}}
.btn{{cursor:pointer;font-weight:700}}
.btn:hover,.pill:hover{{border-color:var(--a1)}}
.btn.primary{{background:linear-gradient(135deg,var(--a1),var(--a2));border:0;color:#fff}}
.btn.mark.done{{background:color-mix(in srgb,var(--a3) 25%,var(--card));border-color:var(--a3);color:var(--a3)}}
input[type=search]{{min-width:160px;flex:1;max-width:340px}}
.layout{{display:grid;grid-template-columns:var(--side) 1fr;min-height:70vh}}
.side{{border-right:1px solid var(--border);padding:12px;position:sticky;top:58px;height:calc(100vh - 58px);overflow:auto;background:color-mix(in srgb,var(--card) 50%,var(--bg))}}
.nav-h{{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin:12px 0 6px;font-weight:800;display:flex;justify-content:space-between;gap:8px}}
.nav-h span{{color:var(--a1)}}
a.nav{{display:block;padding:6px 8px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:12.5px;font-weight:600;margin-bottom:1px}}
a.nav:hover,a.nav.on{{background:color-mix(in srgb,var(--a1) 16%,transparent);color:var(--a1)}}
a.nav.studied{{opacity:.7}}
a.nav.studied::after{{content:" ✓";color:var(--a3)}}
.main{{padding:18px 18px 90px;max-width:900px}}
.hero{{background:linear-gradient(145deg,color-mix(in srgb,var(--a1) 22%,var(--card)),color-mix(in srgb,var(--a2) 18%,var(--card)));border:1px solid var(--border);border-radius:22px;padding:26px 22px;box-shadow:var(--shadow);margin-bottom:16px}}
.hero h1{{font-family:var(--display);font-size:clamp(1.55rem,3vw,2.15rem);line-height:1.15;margin:6px 0 8px}}
.hero p{{color:var(--muted);max-width:60ch}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-top:14px}}
.stat{{background:color-mix(in srgb,var(--card) 80%,transparent);border:1px solid var(--border);border-radius:14px;padding:12px;text-align:center}}
.stat b{{display:block;font-size:1.4rem;font-weight:900;color:var(--a1)}}
.stat span{{font-size:11px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.05em}}
.filters{{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0 18px}}
.pill{{border:1px solid var(--border);background:var(--card);color:var(--ink);border-radius:999px;padding:6px 10px;font-size:12px;font-weight:700;cursor:pointer}}
.pill.on{{background:color-mix(in srgb,var(--a1) 20%,var(--card));border-color:var(--a1);color:var(--a1)}}
.sec{{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:18px 16px;margin-bottom:14px;box-shadow:var(--shadow)}}
.sec.hidden{{display:none}}
.sec .meta{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px;font-size:12px;font-weight:800}}
.sec .id{{color:var(--a1)}}
.sec .school{{color:var(--muted)}}
.sec .lvl{{background:color-mix(in srgb,var(--a2) 18%,transparent);color:var(--a2);padding:2px 8px;border-radius:999px}}
.sec h2{{font-size:1.2rem;margin-bottom:10px;line-height:1.25}}
.sec .body p{{margin:0 0 10px;color:var(--ink)}}
.sec .body ul{{margin:0 0 10px 1.15rem;color:var(--muted)}}
.sec .body li{{margin-bottom:4px}}
.sec .body code{{font-family:var(--mono);font-size:.88em;background:color-mix(in srgb,var(--a1) 12%,transparent);padding:1px 5px;border-radius:5px}}
.sec .body pre{{background:#080d18;color:#dbe7ff;border-radius:12px;padding:12px;overflow:auto;font-family:var(--mono);font-size:12px;margin:10px 0;border:1px solid var(--border);white-space:pre-wrap}}
html[data-theme=warm] .sec .body pre,html[data-theme=forest] .sec .body pre{{background:#1a1520;color:#f5e9d8}}
.table-wrap{{overflow:auto;margin:10px 0;border:1px solid var(--border);border-radius:12px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.05em}}
.green,.iv{{margin-top:10px;padding:10px 12px;border-radius:12px;font-size:13px}}
.green{{background:color-mix(in srgb,var(--a3) 14%,transparent);border:1px solid color-mix(in srgb,var(--a3) 40%,var(--border))}}
.iv{{background:color-mix(in srgb,var(--a2) 12%,transparent);border:1px solid color-mix(in srgb,var(--a2) 35%,var(--border))}}
.sec-actions{{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}}
.progress-wrap{{margin:10px 0 0}}
.progress{{height:8px;background:var(--line);border-radius:99px;overflow:hidden}}
.progress>i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--a3),var(--a1));transition:width .25s}}
.foot{{margin-top:28px;padding-top:14px;border-top:1px solid var(--border);color:var(--muted);font-size:12px}}
.toast{{position:fixed;bottom:16px;right:16px;background:var(--card);border:1px solid var(--a3);color:var(--ink);padding:10px 14px;border-radius:12px;box-shadow:var(--shadow);display:none;z-index:99;font-weight:700;font-size:13px}}
@media(max-width:900px){{
  .layout{{grid-template-columns:1fr}}
  .side{{position:relative;top:0;height:auto;max-height:220px;border-right:0;border-bottom:1px solid var(--border)}}
}}
body.focus .side{{display:none}}
body.focus .layout{{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="banner">FREE FOR EVERYONE · Offline university · Educational only · No warranty · {esc(META['author'])}</div>
<header class="top">
  <div class="brand">{esc(META['title'])} <small>{esc(META['version'])} · {st['sections']} sections · RTMA · Free share</small></div>
  <input id="q" type="search" placeholder="Search curriculum (Cmd/Ctrl+K)…" aria-label="Search"/>
  <select id="theme" aria-label="Theme">
    <option value="night">Night</option>
    <option value="cobalt">Cobalt</option>
    <option value="aurora">Aurora</option>
    <option value="slate">Slate</option>
    <option value="warm">Warm</option>
    <option value="forest">Forest</option>
  </select>
  <button class="btn" type="button" id="btnFocus">Focus</button>
  <button class="btn" type="button" id="btnRandom">Random</button>
  <button class="btn primary" type="button" id="btnTop">Top</button>
</header>
<div class="layout">
<aside class="side" id="side">
  <div class="nav-h">Progress <span id="progLabel">0%</span></div>
  <div class="progress"><i id="progBar"></i></div>
  <div class="nav-h">Schools</div>
  {''.join(nav_html)}
</aside>
<main class="main" id="main">
  <section class="hero" id="home">
    <div style="font-size:12px;font-weight:900;color:var(--a3);letter-spacing:.06em">GENERAL AUDIENCE · FREE UNIVERSITY</div>
    <h1>{esc(META['tagline'])}</h1>
    <p>{esc(META['subtitle'])}. Mentor tone for domain experts and beginners alike. Evidence-first with <strong>RTMA</strong> (Run · Trace · Metric · Artifact) — the AI twin of UC LICC.</p>
    <div class="stats">
      <div class="stat"><b>{st['sections']}</b><span>Sections</span></div>
      <div class="stat"><b>{len(SCHOOLS)}</b><span>Schools</span></div>
      <div class="stat"><b>3</b><span>Runnable labs</span></div>
      <div class="stat"><b>10</b><span>Golden eval Qs</span></div>
      <div class="stat"><b>0</b><span>Keys required</span></div>
      <div class="stat"><b>MIT</b><span>License</span></div>
    </div>
    <div class="progress-wrap">
      <div style="display:flex;justify-content:space-between;font-size:12px;font-weight:700;color:var(--muted);margin-bottom:4px"><span>Studied (this browser)</span><span id="progText">0 / {st['sections']}</span></div>
      <div class="progress"><i id="progBar2"></i></div>
    </div>
    <p style="margin-top:14px;font-size:13px;color:var(--muted)">Runnable path: <code style="color:var(--a1)">bash scripts/verify_slice.sh</code> · Sibling UC pack stays separate and free · Planned public repo: <strong>{esc(META['repo_planned'])}</strong></p>
  </section>

  <div class="filters" id="filters">
    <button type="button" class="pill on" data-filter-school="ALL">All</button>
    {school_pills}
    <button type="button" class="pill" data-filter-level="beginner">Beginner</button>
    <button type="button" class="pill" data-filter-level="intermediate">Intermediate</button>
    <button type="button" class="pill" data-filter-level="advanced">Advanced</button>
    <button type="button" class="pill" data-filter-studied="todo">Unstudied</button>
  </div>

  {''.join(cards)}

  <footer class="foot">
    {esc(META['title'])} {esc(META['version'])} · {esc(META['license'])}<br/>
    Author: {esc(META['author'])} · Linktree: {esc(META['linktree'])}<br/>
    Sibling: <a href="{esc(META['sibling_url'])}" target="_blank" rel="noopener">{esc(META['sibling'])}</a> — never deleted by this project.<br/>
    Built to be shared with the world. Calm. Structured. Free. Honest about limits.
  </footer>
</main>
</div>
<div class="toast" id="toast"></div>
<script>
window.AILAB_META = {json.dumps(payload)};
(function(){{
  const STUDY_KEY='ailab-v2-studied';
  const THEME_KEY='ailab-v2-theme';
  const ids=window.AILAB_META.section_ids;
  let studied=new Set();
  try{{JSON.parse(localStorage.getItem(STUDY_KEY)||'[]').forEach(x=>studied.add(x))}}catch(e){{}}
  const themeEl=document.getElementById('theme');
  const saved=localStorage.getItem(THEME_KEY)||'night';
  document.documentElement.setAttribute('data-theme',saved);
  themeEl.value=saved;
  themeEl.onchange=()=>{{document.documentElement.setAttribute('data-theme',themeEl.value);localStorage.setItem(THEME_KEY,themeEl.value)}};

  function toast(msg){{
    const t=document.getElementById('toast');
    t.textContent=msg;t.style.display='block';
    clearTimeout(window.__tt);window.__tt=setTimeout(()=>t.style.display='none',1600);
  }}
  function saveStudy(){{localStorage.setItem(STUDY_KEY,JSON.stringify([...studied]))}}
  function refreshStudyUI(){{
    const n=studied.size, tot=ids.length, pct=Math.round((n/tot)*100);
    document.getElementById('progLabel').textContent=pct+'%';
    document.getElementById('progBar').style.width=pct+'%';
    document.getElementById('progBar2').style.width=pct+'%';
    document.getElementById('progText').textContent=n+' / '+tot;
    document.querySelectorAll('a.nav').forEach(a=>{{
      a.classList.toggle('studied', studied.has(a.dataset.id));
    }});
    document.querySelectorAll('button.mark').forEach(b=>{{
      const id=b.dataset.mark;
      b.classList.toggle('done', studied.has(id));
      b.textContent=studied.has(id)?'Studied ✓':'Mark studied';
    }});
  }}
  document.querySelectorAll('button.mark').forEach(b=>b.onclick=()=>{{
    const id=b.dataset.mark;
    if(studied.has(id)) studied.delete(id); else studied.add(id);
    saveStudy();refreshStudyUI();applyFilters();
  }});
  document.querySelectorAll('button.copy').forEach(b=>b.onclick=async()=>{{
    try{{await navigator.clipboard.writeText(b.dataset.copy);toast('Copied '+b.dataset.copy)}}catch(e){{toast(b.dataset.copy)}}
  }});

  // filters
  let school='ALL', level='ALL', onlyTodo=false;
  const pills=[...document.querySelectorAll('.pill')];
  function setPillState(){{
    pills.forEach(p=>{{
      let on=false;
      if(p.dataset.filterSchool){{
        on=(p.dataset.filterSchool==='ALL'&&school==='ALL')||(p.dataset.filterSchool===school);
      }} else if(p.dataset.filterLevel){{
        on=p.dataset.filterLevel===level;
      }} else if(p.dataset.filterStudied){{
        on=onlyTodo;
      }}
      p.classList.toggle('on', on);
    }});
  }}
  pills.forEach(p=>p.onclick=()=>{{
    if(p.dataset.filterSchool){{school=p.dataset.filterSchool;}}
    if(p.dataset.filterLevel){{level = level===p.dataset.filterLevel ? 'ALL' : p.dataset.filterLevel;}}
    if(p.dataset.filterStudied){{onlyTodo=!onlyTodo;}}
    setPillState();applyFilters();
  }});
  setPillState();

  const q=document.getElementById('q');
  function applyFilters(){{
    const term=(q.value||'').trim().toLowerCase();
    document.querySelectorAll('article.sec').forEach(el=>{{
      let ok=true;
      if(school!=='ALL' && el.dataset.school!==school) ok=false;
      if(level!=='ALL' && el.dataset.level!==level) ok=false;
      if(onlyTodo && studied.has(el.id)) ok=false;
      if(term){{
        const hay=(el.dataset.search||'')+' '+el.innerText.toLowerCase();
        if(!hay.includes(term)) ok=false;
      }}
      el.classList.toggle('hidden', !ok);
    }});
  }}
  q.addEventListener('input', applyFilters);
  document.addEventListener('keydown',e=>{{
    if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){{e.preventDefault();q.focus();q.select()}}
  }});

  document.getElementById('btnTop').onclick=()=>window.scrollTo({{top:0,behavior:'smooth'}});
  document.getElementById('btnFocus').onclick=()=>document.body.classList.toggle('focus');
  document.getElementById('btnRandom').onclick=()=>{{
    const visible=[...document.querySelectorAll('article.sec:not(.hidden)')];
    if(!visible.length) return;
    const el=visible[Math.floor(Math.random()*visible.length)];
    el.scrollIntoView({{behavior:'smooth',block:'start'}});
    toast(el.id);
  }};

  // active nav on scroll
  const navs=[...document.querySelectorAll('a.nav')];
  function syncNav(){{
    let cur=null;
    document.querySelectorAll('article.sec').forEach(el=>{{
      if(el.classList.contains('hidden')) return;
      if(el.getBoundingClientRect().top<140) cur=el.id;
    }});
    navs.forEach(a=>a.classList.toggle('on', a.dataset.id===cur));
  }}
  window.addEventListener('scroll', syncNav, {{passive:true}});

  refreshStudyUI();
  applyFilters();
  syncNav();
}})();
</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    return OUT


if __name__ == "__main__":
    path = build()
    st = stats()
    size = path.stat().st_size
    print(f"Wrote {path}")
    print(f"Sections: {st['sections']}")
    print(f"By school: {st['by_school']}")
    print(f"Size: {size} bytes ({size/1024:.1f} KB)")
