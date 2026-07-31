#!/usr/bin/env python3
"""Build full-scale v3 lifetime university HTML with multi-level menus."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURR = ROOT / "curriculum"
sys.path.insert(0, str(CURR))

from generate_lifetime import generate  # noqa: E402

sections, meta = generate()
(CURR / "lifetime_sections.json").write_text(
    json.dumps(sections, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
)
(CURR / "lifetime_meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

OUT = ROOT / "university" / "v3-LIFETIME.html"


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def md_lite(body: str) -> str:
    lines = body.split("\n")
    out: list[str] = []
    in_ul = False
    in_pre = False
    table_rows: list[str] = []

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows:
            return
        out.append('<div class="table-wrap"><table>')
        for i, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            if all(set(c) <= set("-: ") and c for c in cells):
                continue
            tag = "th" if i == 0 else "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
        out.append("</table></div>")
        table_rows = []

    def inline(t: str) -> str:
        t = esc(t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
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
        if line.strip().startswith("|") and line.count("|") >= 2:
            close_ul()
            table_rows.append(line)
            continue
        if table_rows:
            flush_table()
        if line.startswith("### "):
            close_ul()
            out.append(f"<h3>{inline(line[4:])}</h3>")
            continue
        if line.startswith("## "):
            close_ul()
            out.append(f"<h3 class='h2ish'>{inline(line[3:])}</h3>")
            continue
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(line[2:])}</li>")
            continue
        close_ul()
        if not line.strip():
            continue
        out.append(f"<p>{inline(line)}</p>")
    close_ul()
    flush_table()
    if in_pre:
        out.append("</pre>")
    return "\n".join(out)


CSS = r"""
:root{
  --bg:#060914;--card:#10182b;--ink:#EAF0FF;--muted:#8FA0BF;--line:#24314d;--border:#2a3858;
  --a1:#38BDF8;--a2:#A78BFA;--a3:#34D399;--side:320px;
  --font:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  --display:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;
  --shadow:0 12px 40px rgba(0,0,0,.45);
}
html[data-theme=warm]{--bg:#FFF6EB;--card:#fff;--ink:#1A1208;--muted:#7A6548;--line:#F0D4B0;--border:#E8C9A0;--a1:#E8820C;--a2:#8B5CF6;--a3:#159947}
html[data-theme=cobalt]{--bg:#061422;--card:#0c2740;--ink:#E8F3FF;--muted:#8EB6D4;--line:#1a4568;--border:#1e4a6a}
html[data-theme=forest]{--bg:#F2F7F1;--card:#fff;--ink:#14201A;--muted:#5B6E62;--line:#C9D9CE;--border:#C9D9CE;--a1:#2F6F4E;--a2:#3F8F62;--a3:#0F9B8E}
html[data-theme=aurora]{--bg:#0b0818;--card:#16122c;--ink:#F6F1FF;--muted:#A99BC8;--line:#2d2650;--border:#352e5c;--a1:#22D3EE;--a2:#C084FC}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);background:var(--bg);color:var(--ink);line-height:1.55;font-size:14.5px}
a{color:var(--a1);text-decoration:none}
.banner{background:linear-gradient(90deg,#0369a1,#6d28d9,#be185d);color:#fff;text-align:center;padding:8px 10px;font-weight:800;font-size:11px;letter-spacing:.04em}
.top{position:sticky;top:0;z-index:80;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:10px 12px;background:color-mix(in srgb,var(--bg) 90%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--border)}
.brand{font-family:var(--display);font-weight:900;font-size:1rem;background:linear-gradient(90deg,var(--a1),var(--a2));-webkit-background-clip:text;color:transparent}
.brand small{display:block;font-family:var(--font);font-size:10px;font-weight:700;color:var(--muted);-webkit-text-fill-color:var(--muted)}
input[type=search],select,.btn{border:1px solid var(--border);background:var(--card);color:var(--ink);border-radius:10px;padding:7px 10px;font:inherit;font-size:12.5px}
.btn{cursor:pointer;font-weight:700}
.btn:hover{border-color:var(--a1)}
.btn.primary{background:linear-gradient(135deg,var(--a1),var(--a2));border:0;color:#fff}
.btn.mark.done{border-color:var(--a3);color:var(--a3)}
input[type=search]{flex:1;min-width:160px;max-width:360px}
.layout{display:grid;grid-template-columns:var(--side) 1fr;min-height:70vh}
.side{border-right:1px solid var(--border);padding:10px;position:sticky;top:56px;height:calc(100vh - 56px);overflow:auto;background:color-mix(in srgb,var(--card) 45%,var(--bg));font-size:12px}
.side summary{cursor:pointer;font-weight:800;padding:6px 4px;list-style:none;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.side summary::-webkit-details-marker{display:none}
.side .did{color:var(--a1);font-family:var(--mono);font-size:10px}
.side em{color:var(--muted);font-style:normal;font-size:10px;margin-left:auto}
.side .ch{margin-left:6px;border-left:2px solid var(--line);padding-left:6px;margin-bottom:4px}
.side .ch-links{display:flex;flex-direction:column;gap:1px;margin:4px 0 8px}
a.nav{display:block;padding:4px 6px;border-radius:6px;color:var(--ink);font-weight:600;font-size:11.5px}
a.nav:hover,a.nav.on{background:color-mix(in srgb,var(--a1) 16%,transparent);color:var(--a1)}
a.nav.studied{opacity:.65}
a.nav.studied::after{content:" ✓";color:var(--a3)}
.main{padding:16px 16px 80px;max-width:920px}
.hero{background:linear-gradient(145deg,color-mix(in srgb,var(--a1) 20%,var(--card)),color-mix(in srgb,var(--a2) 16%,var(--card)));border:1px solid var(--border);border-radius:20px;padding:22px;box-shadow:var(--shadow);margin-bottom:14px}
.hero h1{font-family:var(--display);font-size:clamp(1.45rem,3vw,2rem);line-height:1.15;margin:6px 0}
.hero p{color:var(--muted);max-width:62ch}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:8px;margin-top:12px}
.stat{background:color-mix(in srgb,var(--card) 85%,transparent);border:1px solid var(--border);border-radius:12px;padding:10px;text-align:center}
.stat b{display:block;font-size:1.25rem;color:var(--a1)}
.stat span{font-size:10px;color:var(--muted);font-weight:800;text-transform:uppercase;letter-spacing:.04em}
.filters{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 14px}
.pill{border:1px solid var(--border);background:var(--card);color:var(--ink);border-radius:999px;padding:5px 9px;font-size:11px;font-weight:800;cursor:pointer}
.pill.on{border-color:var(--a1);color:var(--a1);background:color-mix(in srgb,var(--a1) 14%,var(--card))}
.sec{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;margin-bottom:12px;box-shadow:var(--shadow)}
.sec.hidden{display:none}
.crumb{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px;font-size:11px;font-weight:800}
.crumb span{background:color-mix(in srgb,var(--a1) 10%,transparent);padding:2px 7px;border-radius:999px;color:var(--muted)}
.crumb .lvl{color:var(--a2)}
.crumb .sid{font-family:var(--mono);color:var(--a1)}
.sec h2{font-size:1.15rem;margin-bottom:10px}
.sec .body p,.sec .body li{margin-bottom:8px}
.sec .body h3{margin:12px 0 6px;font-size:0.98rem;color:var(--a1)}
.sec .body ul{margin-left:1.1rem;color:var(--muted)}
.sec .body code{font-family:var(--mono);font-size:.86em;background:color-mix(in srgb,var(--a1) 12%,transparent);padding:1px 5px;border-radius:4px}
.sec .body pre{background:#080d18;color:#dbe7ff;border-radius:10px;padding:10px;overflow:auto;font-family:var(--mono);font-size:11.5px;margin:8px 0;border:1px solid var(--border);white-space:pre-wrap}
.table-wrap{overflow:auto;margin:8px 0;border:1px solid var(--border);border-radius:10px}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.sec-actions{display:flex;gap:8px;margin-top:10px}
.progress{height:7px;background:var(--line);border-radius:99px;overflow:hidden;margin:6px 0}
.progress>i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--a3),var(--a1));transition:width .2s}
.foot{margin-top:24px;padding-top:12px;border-top:1px solid var(--border);color:var(--muted);font-size:11.5px}
.toast{position:fixed;bottom:14px;right:14px;background:var(--card);border:1px solid var(--a3);padding:9px 12px;border-radius:10px;display:none;z-index:99;font-weight:800;font-size:12px;box-shadow:var(--shadow)}
.toc-mini{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;margin-top:12px}
.toc-mini .card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px;font-size:12px}
.toc-mini b{display:block;color:var(--a1);margin-bottom:4px}
body.focus .side{display:none}
body.focus .layout{grid-template-columns:1fr}
@media(max-width:960px){
  .layout{grid-template-columns:1fr}
  .side{position:relative;top:0;height:auto;max-height:280px;border-right:0;border-bottom:1px solid var(--border)}
}
"""

JS = r"""
(function(){
  const STUDY_KEY='ailab-v3-studied';
  const THEME_KEY='ailab-v3-theme';
  let studied=new Set();
  try{JSON.parse(localStorage.getItem(STUDY_KEY)||'[]').forEach(x=>studied.add(x))}catch(e){}
  const themeEl=document.getElementById('theme');
  const saved=localStorage.getItem(THEME_KEY)||'night';
  document.documentElement.setAttribute('data-theme',saved);
  themeEl.value=saved;
  themeEl.onchange=function(){document.documentElement.setAttribute('data-theme',themeEl.value);localStorage.setItem(THEME_KEY,themeEl.value)};

  const toc=document.getElementById('tocMini');
  Object.entries(window.AILAB_V3.divisions).forEach(function(pair){
    var id=pair[0], name=pair[1];
    var el=document.createElement('div');
    el.className='card';
    el.innerHTML='<b>'+id+'</b>'+name;
    el.style.cursor='pointer';
    el.onclick=function(){
      document.querySelectorAll('.pill').forEach(function(p){p.classList.toggle('on', p.dataset.div===id)});
      divFilter=id; apply();
      var first=document.querySelector('article.sec[data-div="'+id+'"]');
      if(first) first.scrollIntoView({behavior:'smooth'});
    };
    toc.appendChild(el);
  });

  function toast(m){var t=document.getElementById('toast');t.textContent=m;t.style.display='block';clearTimeout(window.__tt);window.__tt=setTimeout(function(){t.style.display='none'},1400)}
  function save(){localStorage.setItem(STUDY_KEY,JSON.stringify(Array.from(studied)))}
  function refreshStudy(){
    var tot=window.AILAB_V3.n, n=studied.size, pct=Math.round(n/tot*100);
    document.getElementById('progLabel').textContent=pct+'%';
    document.getElementById('progBar').style.width=pct+'%';
    document.getElementById('progText').textContent=n+' / '+tot;
    document.querySelectorAll('a.nav').forEach(function(a){a.classList.toggle('studied', studied.has(a.dataset.id))});
    document.querySelectorAll('button.mark').forEach(function(b){
      var id=b.dataset.mark; b.classList.toggle('done', studied.has(id));
      b.textContent=studied.has(id)?'Studied ✓':'Mark studied';
    });
  }
  document.querySelectorAll('button.mark').forEach(function(b){b.onclick=function(){
    var id=b.dataset.mark; if(studied.has(id)) studied.delete(id); else studied.add(id);
    save(); refreshStudy(); apply();
  }});
  document.querySelectorAll('button.copy').forEach(function(b){b.onclick=async function(){
    try{await navigator.clipboard.writeText(b.dataset.copy);toast('Copied '+b.dataset.copy)}catch(e){toast(b.dataset.copy)}
  }});

  var divFilter='ALL', onlyTodo=false;
  var levelEl=document.getElementById('level');
  document.querySelectorAll('.pill').forEach(function(p){p.onclick=function(){
    if(p.dataset.todo){onlyTodo=!onlyTodo;p.classList.toggle('on',onlyTodo);apply();return;}
    divFilter=p.dataset.div||'ALL';
    document.querySelectorAll('.pill').forEach(function(x){if(x.dataset.div)x.classList.toggle('on',x.dataset.div===divFilter)});
    apply();
  }});
  levelEl.onchange=apply;
  var q=document.getElementById('q');
  q.addEventListener('input', apply);
  document.addEventListener('keydown',function(e){if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();q.focus();q.select()}});

  function apply(){
    var term=(q.value||'').trim().toLowerCase();
    var lvl=levelEl.value;
    document.querySelectorAll('article.sec').forEach(function(el){
      var ok=true;
      if(divFilter!=='ALL' && el.dataset.div!==divFilter) ok=false;
      if(lvl!=='ALL' && el.dataset.level!==lvl) ok=false;
      if(onlyTodo && studied.has(el.id)) ok=false;
      if(term){
        var hay=(el.dataset.search||'')+' '+el.innerText.toLowerCase();
        if(hay.indexOf(term)===-1) ok=false;
      }
      el.classList.toggle('hidden', !ok);
    });
  }

  document.getElementById('btnTop').onclick=function(){window.scrollTo({top:0,behavior:'smooth'})};
  document.getElementById('btnFocus').onclick=function(){document.body.classList.toggle('focus')};
  document.getElementById('btnExpand').onclick=function(){document.querySelectorAll('.side details').forEach(function(d){d.open=true})};
  document.getElementById('btnRandom').onclick=function(){
    var vis=Array.prototype.slice.call(document.querySelectorAll('article.sec:not(.hidden)'));
    if(!vis.length)return;
    var el=vis[Math.floor(Math.random()*vis.length)];
    el.scrollIntoView({behavior:'smooth',block:'start'});toast(el.id);
  };

  var navs=Array.prototype.slice.call(document.querySelectorAll('a.nav'));
  function syncNav(){
    var cur=null;
    document.querySelectorAll('article.sec').forEach(function(el){
      if(el.classList.contains('hidden'))return;
      if(el.getBoundingClientRect().top<130) cur=el.id;
    });
    navs.forEach(function(a){a.classList.toggle('on', a.dataset.id===cur)});
  }
  window.addEventListener('scroll', syncNav, {passive:true});
  refreshStudy(); apply(); syncNav();
})();
"""


def build() -> tuple[Path, int]:
    div_order: list[str] = []
    div_map: dict = {}
    for s in sections:
        d = s["division"]
        if d not in div_map:
            div_map[d] = {"name": s["division_name"], "chapters": {}}
            div_order.append(d)
        ch = s["chapter"]
        if ch not in div_map[d]["chapters"]:
            div_map[d]["chapters"][ch] = {"name": s["chapter_name"], "items": []}
        div_map[d]["chapters"][ch]["items"].append(s)

    nav_parts: list[str] = []
    for d in div_order:
        info = div_map[d]
        nch = sum(len(c["items"]) for c in info["chapters"].values())
        nav_parts.append(
            f'<details class="div" data-div="{esc(d)}" open><summary>'
            f'<span class="did">{esc(d)}</span> {esc(info["name"])} <em>{nch}</em></summary>'
        )
        for ch, cinfo in info["chapters"].items():
            nav_parts.append(
                f'<details class="ch"><summary>{esc(ch)} · {esc(cinfo["name"])} '
                f'<em>{len(cinfo["items"])}</em></summary><div class="ch-links">'
            )
            for item in cinfo["items"]:
                nav_parts.append(
                    f'<a class="nav" href="#{esc(item["id"])}" data-id="{esc(item["id"])}" '
                    f'data-div="{esc(d)}" data-ch="{esc(ch)}">{esc(item["title"][:42])}</a>'
                )
            nav_parts.append("</div></details>")
        nav_parts.append("</details>")

    cards: list[str] = []
    for s in sections:
        search = (s["id"] + " " + s["title"] + " " + s["tags"] + " " + s["body"])[:900].lower()
        cards.append(
            "<article class=\"sec\" id=\"{id}\" data-div=\"{div}\" data-ch=\"{ch}\" "
            "data-level=\"{lvl}\" data-search=\"{search}\">"
            "<div class=\"crumb\"><span>{div2}</span><span>{ch2}</span>"
            "<span class=\"lvl\">{lvl2}</span><span class=\"sid\">{id2}</span></div>"
            "<h2>{title}</h2><div class=\"body\">{body}</div>"
            "<div class=\"sec-actions\">"
            "<button type=\"button\" class=\"btn mark\" data-mark=\"{id3}\">Mark studied</button>"
            "<button type=\"button\" class=\"btn copy\" data-copy=\"{id4}\">Copy id</button>"
            "</div></article>".format(
                id=esc(s["id"]),
                div=esc(s["division"]),
                ch=esc(s["chapter"]),
                lvl=esc(s["level"]),
                search=esc(search),
                div2=esc(s["division"]),
                ch2=esc(s["chapter"]),
                lvl2=esc(s["level"]),
                id2=esc(s["id"]),
                title=esc(s["title"]),
                body=md_lite(s["body"]),
                id3=esc(s["id"]),
                id4=esc(s["id"]),
            )
        )

    div_pills = "".join(
        f'<button type="button" class="pill" data-div="{esc(d)}">{esc(d)}</button>' for d in div_order
    )
    n = len(sections)
    divisions_json = json.dumps({d: div_map[d]["name"] for d in div_order})
    ids_json = json.dumps([s["id"] for s in sections])

    doc = (
        "<!DOCTYPE html>\n<html lang=\"en\" data-theme=\"night\">\n<head>\n"
        "<meta charset=\"UTF-8\"/>\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\"/>\n"
        f"<meta name=\"description\" content=\"{esc(meta['title'])} {esc(meta['version'])} — {esc(meta['tagline'])}\"/>\n"
        f"<title>{esc(meta['title'])} {esc(meta['version'])} — Lifetime Mastery</title>\n"
        f"<style>\n{CSS}\n</style>\n</head>\n<body>\n"
        f"<div class=\"banner\">FREE LIFETIME MASTERY · v3 · {n} lessons · Divisions · Chapters · Menus · RTMA · Educational only · {esc(meta['author'])}</div>\n"
        "<header class=\"top\">\n"
        f"<div class=\"brand\">{esc(meta['title'])}<small>{esc(meta['version'])} · {n} lessons · multi-level campus</small></div>\n"
        "<input id=\"q\" type=\"search\" placeholder=\"Search all lessons (Cmd/Ctrl+K)\" aria-label=\"Search\"/>\n"
        "<select id=\"theme\" aria-label=\"Theme\">"
        "<option value=\"night\">Night</option><option value=\"cobalt\">Cobalt</option>"
        "<option value=\"aurora\">Aurora</option><option value=\"warm\">Warm</option>"
        "<option value=\"forest\">Forest</option></select>\n"
        "<select id=\"level\" aria-label=\"Level\">"
        "<option value=\"ALL\">All levels</option><option value=\"beginner\">Beginner</option>"
        "<option value=\"intermediate\">Intermediate</option><option value=\"advanced\">Advanced</option></select>\n"
        "<button class=\"btn\" type=\"button\" id=\"btnFocus\">Focus</button>\n"
        "<button class=\"btn\" type=\"button\" id=\"btnRandom\">Random</button>\n"
        "<button class=\"btn\" type=\"button\" id=\"btnExpand\">Expand nav</button>\n"
        "<button class=\"btn primary\" type=\"button\" id=\"btnTop\">Top</button>\n"
        "</header>\n<div class=\"layout\">\n<aside class=\"side\" id=\"side\">\n"
        f"<div style=\"font-size:10px;font-weight:900;color:var(--muted);letter-spacing:.08em;margin:4px 0\">PROGRESS <span id=\"progLabel\">0%</span></div>\n"
        f"<div class=\"progress\"><i id=\"progBar\"></i></div>\n"
        f"<div style=\"font-size:11px;color:var(--muted);margin:4px 0 8px\" id=\"progText\">0 / {n}</div>\n"
        f"{''.join(nav_parts)}\n</aside>\n<main class=\"main\">\n"
        "<section class=\"hero\" id=\"home\">\n"
        "<div style=\"font-size:11px;font-weight:900;color:var(--a3);letter-spacing:.08em\">GENERAL AUDIENCE · FULL-SCALE · LIFETIME</div>\n"
        f"<h1>{esc(meta['tagline'])}</h1>\n"
        f"<p>{esc(meta['subtitle'])}. Built from local Mac Mini vaults (Agentic AI University, DevOps AI, Google AI Arsenal, UC prompt labs, Hermes wiring) + 2026 public AI-engineering roadmaps + ecosystem radar (agents, MCP, Hermes, robotics/physical AI).</p>\n"
        "<div class=\"stats\">\n"
        f"<div class=\"stat\"><b>{n}</b><span>Lessons</span></div>\n"
        f"<div class=\"stat\"><b>{len(div_order)}</b><span>Divisions</span></div>\n"
        "<div class=\"stat\"><b>RTMA</b><span>Evidence</span></div>\n"
        "<div class=\"stat\"><b>0 keys</b><span>Phase-1 labs</span></div>\n"
        "<div class=\"stat\"><b>Hermes</b><span>Agent OS</span></div>\n"
        "<div class=\"stat\"><b>Future</b><span>Robotics track</span></div>\n"
        "</div>\n<div class=\"toc-mini\" id=\"tocMini\"></div>\n"
        "<p style=\"margin-top:12px;font-size:12px;color:var(--muted)\">Runnable proof: <code style=\"color:var(--a1)\">bash scripts/verify_slice.sh</code> · Compact: v1-SLICE · Prior: v2 · Sibling: UC Lab Free University</p>\n"
        "</section>\n"
        f"<div class=\"filters\" id=\"filters\"><button type=\"button\" class=\"pill on\" data-div=\"ALL\">All divisions</button>{div_pills}"
        "<button type=\"button\" class=\"pill\" data-todo=\"1\">Unstudied only</button></div>\n"
        f"{''.join(cards)}\n"
        f"<footer class=\"foot\">{esc(meta['title'])} {esc(meta['version'])} · MIT educational · No warranty<br/>"
        "Sources: local Labs vaults + UC free-share discipline + public 2026 AI engineering discourse + Hermes/MCP/robotics radar.<br/>"
        "Never delete UC pack. Secrets never in git. Permissions are perimeter.</footer>\n"
        "</main>\n</div>\n<div class=\"toast\" id=\"toast\"></div>\n<script>\n"
        f"window.AILAB_V3 = {{n: {n}, divisions: {divisions_json}, ids: {ids_json}}};\n"
        f"{JS}\n</script>\n</body>\n</html>\n"
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    return OUT, n


if __name__ == "__main__":
    path, n = build()
    size = path.stat().st_size
    print(f"Wrote {path}")
    print(f"Lessons: {n}")
    print(f"Size: {size} bytes ({size/1024:.1f} KB)")
