#!/usr/bin/env python3
"""v4 Portfolio full-page campus — stunning multi-feature guide + 1000+ links."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURR = ROOT / "curriculum"
sys.path.insert(0, str(CURR))

from generate_lifetime import generate as gen_lessons  # noqa: E402
from generate_resources import generate as gen_links  # noqa: E402

OUT = ROOT / "university" / "v4-PORTFOLIO.html"

DIV_EMOJI = {
    "D00": "🏛️", "D01": "🧱", "D02": "🗣️", "D03": "📊", "D04": "🧠",
    "D05": "🖥️", "D06": "☁️", "D07": "✍️", "D08": "📚", "D09": "🤖",
    "D10": "🪄", "D11": "🧪", "D12": "🎙️", "D13": "🛠️", "D14": "🦾",
    "D15": "🚀", "D16": "🏆", "D17": "📖",
}
CAT_EMOJI = {
    "Vendors & APIs": "☁️", "Local Lab": "🖥️", "Agents & MCP": "🤖", "RAG & Vectors": "🧲",
    "Evals & Safety": "🛡️", "Learn & Courses": "🎓", "Engineering": "⚙️", "Voice & UC": "📞",
    "Robotics & Physical AI": "🦾", "Datasets & Benchmarks": "📦", "Free Share & Author": "🎁",
    "Model Cards (HF)": "🪪", "Ollama Library": "🦙", "Libraries & Tools": "🧰",
    "Papers & Classics": "📄", "Standards & Protocols": "📜", "Community & News": "📰",
    "Security": "🔐", "Campus Quick Links": "🏠", "Extended Catalog": "🌌",
}

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=Fraunces:opsz,wght@9..144,500;9..144,700&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

:root{
  --bg:#050814; --bg2:#0A1020; --card:rgba(18,26,44,.82); --card2:rgba(24,34,56,.9);
  --ink:#F4F7FF; --muted:#A3B0C8; --faint:#667792;
  --line:rgba(160,180,220,.12); --border:rgba(170,190,240,.2);
  --a1:#6EB6FF; --a2:#C4A1FF; --a3:#45F0B4; --a4:#FF8DC7; --a5:#FFD36A;
  --glow:0 0 100px rgba(110,182,255,.18);
  --shadow:0 24px 70px rgba(0,0,0,.5);
  --radius:24px;
  --font:'Outfit',system-ui,sans-serif;
  --display:'Fraunces',Georgia,serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
  --navw:352px; --rail:76px;
  --shine: linear-gradient(120deg,transparent 30%,rgba(255,255,255,.14) 50%,transparent 70%);
}
html[data-theme=day]{
  --bg:#F4F0E8; --bg2:#EBE5DA; --card:rgba(255,255,255,.88); --card2:rgba(255,252,247,.95);
  --ink:#16120C; --muted:#6F6558; --faint:#9A8F80;
  --line:rgba(22,18,12,.08); --border:rgba(22,18,12,.12);
  --a1:#0A6FCB; --a2:#7C3AED; --a3:#0E9F6E; --a4:#DB2777; --a5:#D97706;
  --glow:0 0 70px rgba(10,111,203,.1); --shadow:0 18px 50px rgba(22,18,12,.08);
}
html[data-theme=rose]{
  --bg:#160812; --bg2:#220E1A; --card:rgba(42,18,32,.88); --card2:rgba(54,24,42,.92);
  --ink:#FFF0F7; --muted:#D4A8BE; --a1:#FF7A9C; --a2:#F0ABFC; --a3:#4ADE80; --a5:#FDE047;
}
html[data-theme=ember]{
  --bg:#130C07; --bg2:#1C130C; --card:rgba(40,24,14,.9); --card2:rgba(52,30,16,.95);
  --ink:#FFF8F0; --muted:#D0AD88; --a1:#FF9F4A; --a2:#FF5C7A; --a3:#A3E635; --a5:#FDE047;
}
html[data-theme=mint]{
  --bg:#041411; --bg2:#081C18; --card:rgba(12,40,34,.88); --card2:rgba(16,52,44,.94);
  --ink:#ECFDF8; --muted:#91C9B8; --a1:#2DD4BF; --a2:#7DD3FC; --a3:#BEF264; --a5:#FBBF24;
}
html[data-theme=paper]{
  --bg:#FAFAF6; --bg2:#F1F0E8; --card:rgba(255,255,255,.92); --card2:#FFFEFA;
  --ink:#0F172A; --muted:#64748B; --a1:#2563EB; --a2:#7C3AED; --a3:#059669; --a5:#D97706;
  --shadow:0 14px 40px rgba(15,23,42,.07);
}
html[data-theme=aurora]{
  --bg:#070616; --bg2:#0E0B24; --card:rgba(22,18,48,.88); --card2:rgba(30,24,62,.94);
  --ink:#F5F3FF; --muted:#B7A8E0; --a1:#22D3EE; --a2:#C084FC; --a3:#4ADE80; --a4:#F472B6; --a5:#FBBF24;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;max-width:100%;overflow:hidden}
body{
  font-family:var(--font); color:var(--ink); line-height:1.55; font-size:15px;
  background:
    radial-gradient(900px 500px at 8% -8%, color-mix(in srgb,var(--a1) 24%, transparent), transparent 60%),
    radial-gradient(800px 480px at 100% 0%, color-mix(in srgb,var(--a2) 20%, transparent), transparent 55%),
    radial-gradient(700px 400px at 50% 110%, color-mix(in srgb,var(--a4) 12%, transparent), transparent 50%),
    var(--bg);
}
body::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.45;
  background-image:
    radial-gradient(1.5px 1.5px at 20px 30px, rgba(255,255,255,.35), transparent),
    radial-gradient(1px 1px at 80px 120px, rgba(255,255,255,.25), transparent),
    radial-gradient(1.2px 1.2px at 160px 80px, rgba(255,255,255,.2), transparent),
    radial-gradient(1px 1px at 240px 200px, rgba(255,255,255,.18), transparent),
    radial-gradient(1.4px 1.4px at 320px 40px, rgba(255,255,255,.22), transparent);
  background-size:360px 260px; animation:drift 80s linear infinite;
}
@keyframes drift{to{background-position:360px 260px}}
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes pulse{0%,100%{opacity:.55}50%{opacity:1}}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
@keyframes pop{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:none}}
@keyframes spin-slow{to{transform:rotate(360deg)}}
@keyframes borderflow{0%{background-position:0% 50%}100%{background-position:200% 50%}}
button,input,select{font:inherit}
a{color:var(--a1)}
.app{position:relative;z-index:1;display:grid;grid-template-columns:var(--rail) var(--navw) 1fr;grid-template-rows:68px 1fr;height:100vh;width:100vw}
.top{
  grid-column:1/-1;display:flex;align-items:center;gap:12px;padding:0 16px;
  border-bottom:1px solid var(--border);
  background:linear-gradient(180deg,color-mix(in srgb,var(--bg) 78%,transparent),color-mix(in srgb,var(--bg) 55%,transparent));
  backdrop-filter:blur(20px) saturate(1.2); z-index:40;
}
.brand{display:flex;align-items:center;gap:12px;min-width:240px}
.logo{
  width:44px;height:44px;border-radius:16px;display:grid;place-items:center;font-size:1.15rem;
  background:conic-gradient(from 180deg,var(--a1),var(--a2),var(--a4),var(--a3),var(--a1));
  color:#fff;font-weight:800;box-shadow:var(--glow); animation:floaty 5s ease-in-out infinite; position:relative;
}
.logo::after{content:"";position:absolute;inset:2px;border-radius:14px;background:color-mix(in srgb,var(--bg) 55%,#111);z-index:-1}
.logo span{position:relative;z-index:1;filter:drop-shadow(0 2px 8px rgba(0,0,0,.35))}
.brand h1{
  font-family:var(--display);font-size:1.35rem;font-weight:700;line-height:1.05;
  background:linear-gradient(90deg,var(--ink),var(--a1),var(--a2));
  -webkit-background-clip:text;color:transparent; background-size:200% auto;
}
.brand small{display:block;color:var(--muted);font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-top:2px}
.search{
  flex:1;display:flex;align-items:center;gap:10px;max-width:680px;
  background:linear-gradient(var(--card),var(--card)) padding-box,
    linear-gradient(90deg,var(--a1),var(--a2),var(--a4),var(--a1)) border-box;
  border:1px solid transparent;border-radius:999px;padding:9px 16px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04), 0 8px 30px rgba(0,0,0,.12);
}
.search .ico{font-size:1rem;filter:grayscale(.2)}
.search input{flex:1;border:0;outline:0;background:transparent;color:var(--ink);font-size:14px}
.search kbd{font-family:var(--mono);font-size:10px;color:var(--faint);border:1px solid var(--border);border-radius:8px;padding:3px 7px;background:color-mix(in srgb,var(--bg) 40%,transparent)}
.top-actions{display:flex;gap:8px;align-items:center;margin-left:auto}
.iconbtn,select.sel{
  border:1px solid var(--border);background:var(--card);color:var(--ink);
  border-radius:14px;padding:8px 12px;cursor:pointer;font-weight:700;font-size:12.5px;
  transition:transform .15s ease, border-color .15s ease, box-shadow .15s ease;
}
.iconbtn:hover,select.sel:hover{border-color:var(--a1);transform:translateY(-1px);box-shadow:0 8px 20px rgba(0,0,0,.15)}
.iconbtn{width:42px;height:42px;display:grid;place-items:center;padding:0;font-size:1.05rem}
.rail{
  border-right:1px solid var(--border);background:linear-gradient(180deg,color-mix(in srgb,var(--bg2) 92%,transparent),color-mix(in srgb,var(--bg) 88%,transparent));
  display:flex;flex-direction:column;align-items:center;gap:10px;padding:14px 8px;z-index:30;
}
.rail button{
  width:52px;height:52px;border-radius:18px;border:1px solid transparent;background:transparent;
  color:var(--muted);cursor:pointer;font-size:1.25rem;display:grid;place-items:center;position:relative;
  transition:all .18s ease;
}
.rail button:hover{background:var(--card);color:var(--ink);transform:translateY(-2px)}
.rail button.on{
  background:linear-gradient(145deg,color-mix(in srgb,var(--a1) 35%,var(--card)),var(--card));
  color:var(--ink);border-color:var(--border);box-shadow:var(--glow);
}
.rail button.on::after{
  content:""; position:absolute; left:-6px; top:50%; transform:translateY(-50%);
  width:4px;height:22px;border-radius:99px;background:linear-gradient(var(--a1),var(--a2));
}
.rail .sp{flex:1}
.rail .orb{
  width:28px;height:28px;border-radius:50%;
  background:conic-gradient(var(--a1),var(--a2),var(--a4),var(--a3),var(--a1));
  animation:spin-slow 12s linear infinite; box-shadow:var(--glow); opacity:.9;
}
.nav{
  border-right:1px solid var(--border);background:color-mix(in srgb,var(--bg2) 90%, transparent);
  overflow:auto;padding:12px;z-index:20;
}
.nav h3{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin:14px 4px 8px;font-weight:800}
.prog{
  background:linear-gradient(160deg,color-mix(in srgb,var(--a1) 12%,var(--card)),var(--card));
  border:1px solid var(--border);border-radius:18px;padding:14px;margin-bottom:12px;position:relative;overflow:hidden;
}
.prog::before{content:"✨";position:absolute;right:10px;top:8px;font-size:1.1rem;opacity:.8;animation:pulse 2.4s ease-in-out infinite}
.prog .row{display:flex;justify-content:space-between;font-size:12px;font-weight:800;margin-bottom:6px}
.bar{height:10px;background:var(--line);border-radius:99px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,.2)}
.bar>i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--a3),var(--a1),var(--a2));background-size:200% 100%;animation:shimmer 3s linear infinite;transition:width .3s}
details.div{border:1px solid var(--border);border-radius:16px;background:var(--card);margin-bottom:9px;overflow:hidden;backdrop-filter:blur(8px)}
details.div>summary{list-style:none;cursor:pointer;padding:11px 12px;font-weight:800;font-size:12.5px;display:flex;gap:8px;align-items:center}
details.div>summary::-webkit-details-marker{display:none}
details.div .did{font-family:var(--mono);font-size:10px;color:var(--a1);background:color-mix(in srgb,var(--a1) 12%,transparent);padding:2px 6px;border-radius:999px}
details.div .emoji{font-size:1rem}
details.div em{margin-left:auto;color:var(--faint);font-style:normal;font-size:11px;font-family:var(--mono)}
.ch{margin:0 8px 8px;border-left:2px solid color-mix(in srgb,var(--a2) 40%,var(--line));padding-left:8px}
.ch>summary{list-style:none;cursor:pointer;padding:6px 4px;font-size:12px;font-weight:700;color:var(--muted)}
.ch>summary::-webkit-details-marker{display:none}
.ch-links{display:flex;flex-direction:column;gap:2px;padding-bottom:6px}
a.navlink{display:block;padding:7px 8px;border-radius:10px;color:var(--ink);text-decoration:none;font-size:12px;font-weight:600;transition:background .12s}
a.navlink:hover,a.navlink.on{background:color-mix(in srgb,var(--a1) 16%,transparent);color:var(--a1)}
a.navlink.studied{opacity:.7}
a.navlink.studied::after{content:" ✓";color:var(--a3)}
.stage{overflow:auto;position:relative}
.stage-inner{min-height:100%;padding:24px 30px 90px;max-width:1480px;margin:0 auto}
.hero{
  position:relative;overflow:hidden;border-radius:32px;padding:40px 34px 34px;
  background:
    radial-gradient(600px 280px at 90% 10%, color-mix(in srgb,var(--a4) 25%, transparent), transparent 60%),
    linear-gradient(135deg, color-mix(in srgb,var(--a1) 24%, var(--card)), color-mix(in srgb,var(--a2) 18%, var(--card2)));
  border:1px solid var(--border); box-shadow:var(--shadow), var(--glow); margin-bottom:20px;
  animation:pop .5s ease both;
}
.hero .badge-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.hero .badge{
  font-size:11px;font-weight:800;letter-spacing:.04em;padding:6px 11px;border-radius:999px;
  background:color-mix(in srgb,var(--card) 70%,transparent);border:1px solid var(--border);backdrop-filter:blur(8px)
}
.hero h2{
  font-family:var(--display);font-size:clamp(2.1rem,4.4vw,3.5rem);font-weight:700;line-height:1.02;margin:8px 0 14px;max-width:16ch;
  text-shadow:0 10px 40px rgba(0,0,0,.18);
}
.hero p{color:var(--muted);max-width:64ch;font-size:1.06rem}
.hero .sparkles{position:absolute;inset:0;pointer-events:none;background:
  radial-gradient(circle at 15% 30%, rgba(255,255,255,.12), transparent 12%),
  radial-gradient(circle at 75% 20%, rgba(255,255,255,.1), transparent 10%),
  radial-gradient(circle at 60% 70%, rgba(255,255,255,.08), transparent 12%)}
.stats{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-top:24px}
.stat{
  background:color-mix(in srgb,var(--card) 75%, transparent);border:1px solid var(--border);
  border-radius:20px;padding:14px 12px;backdrop-filter:blur(10px);position:relative;overflow:hidden;
  transition:transform .18s ease, box-shadow .18s ease;
}
.stat:hover{transform:translateY(-3px);box-shadow:var(--glow)}
.stat .ico{font-size:1.15rem;margin-bottom:4px}
.stat b{
  display:block;font-size:1.55rem;font-weight:800;font-family:var(--display);
  background:linear-gradient(90deg,var(--a1),var(--a2));-webkit-background-clip:text;color:transparent;
}
.stat span{font-size:10.5px;color:var(--muted);font-weight:800;text-transform:uppercase;letter-spacing:.07em}
.panel-grid{display:grid;grid-template-columns:1.35fr .95fr;gap:14px;margin-bottom:18px}
.panel{
  background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  padding:20px;box-shadow:var(--shadow);position:relative;overflow:hidden;backdrop-filter:blur(10px);
  animation:pop .55s ease both;
}
.panel::before{content:"";position:absolute;inset:0 0 auto 0;height:3px;background:linear-gradient(90deg,var(--a1),var(--a2),var(--a4),var(--a3));background-size:200% 100%;animation:borderflow 6s linear infinite}
.panel h3{font-size:1.05rem;margin-bottom:10px;display:flex;gap:8px;align-items:center}
.panel p,.panel li{color:var(--muted);font-size:13.5px}
.panel ul{margin-left:1.15rem}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 16px}
.pill{
  border:1px solid var(--border);background:var(--card);color:var(--ink);border-radius:999px;
  padding:8px 13px;font-size:12px;font-weight:800;cursor:pointer;transition:all .15s ease;
}
.pill:hover{transform:translateY(-1px);border-color:var(--a1)}
.pill.on{border-color:transparent;color:#fff;background:linear-gradient(135deg,var(--a1),var(--a2));box-shadow:0 8px 24px color-mix(in srgb,var(--a1) 35%, transparent)}
.sec{
  background:var(--card);border:1px solid var(--border);border-radius:26px;padding:24px 22px;
  margin-bottom:16px;box-shadow:var(--shadow);position:relative;overflow:hidden;backdrop-filter:blur(8px);
  animation:pop .45s ease both;
}
.sec::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,var(--a1),var(--a2),var(--a4))}
.sec.hidden{display:none}
.sec:hover{border-color:color-mix(in srgb,var(--a1) 45%, var(--border))}
.crumb{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:12px}
.crumb span{
  font-size:11px;font-weight:800;padding:5px 10px;border-radius:999px;
  background:color-mix(in srgb,var(--a1) 12%,transparent);color:var(--muted);border:1px solid var(--line);
}
.crumb .sid{font-family:var(--mono);color:var(--a1)}
.crumb .emoji-pill{background:color-mix(in srgb,var(--a5) 16%,transparent);font-size:13px;padding:4px 9px}
.sec h2{font-family:var(--display);font-size:1.75rem;font-weight:700;line-height:1.12;margin-bottom:12px;letter-spacing:-.01em}
.sec .body p{margin:0 0 10px}
.sec .body h3{margin:16px 0 8px;color:var(--a1);font-size:.98rem;letter-spacing:.02em;display:flex;gap:8px;align-items:center}
.sec .body h3::before{content:"◆";font-size:.7rem;color:var(--a2)}
.sec .body ul{margin:0 0 10px 1.15rem;color:var(--muted)}
.sec .body code{font-family:var(--mono);font-size:.86em;background:color-mix(in srgb,var(--a1) 14%,transparent);padding:2px 7px;border-radius:7px}
.sec .body pre{
  background:linear-gradient(160deg,#070B16,#0D1424);color:#E4EEFF;border-radius:16px;padding:16px;overflow:auto;
  font-family:var(--mono);font-size:12px;margin:12px 0;border:1px solid var(--border);white-space:pre-wrap;
  box-shadow:inset 0 0 40px rgba(91,157,255,.06);
}
html[data-theme=day] .sec .body pre, html[data-theme=paper] .sec .body pre{background:#0F172A;color:#E5E7EB}
.table-wrap{overflow:auto;margin:10px 0;border:1px solid var(--border);border-radius:14px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.btn{
  border:1px solid var(--border);background:var(--card2);color:var(--ink);border-radius:14px;
  padding:10px 14px;cursor:pointer;font-weight:800;font-size:12.5px;transition:all .15s ease;
}
.btn:hover{transform:translateY(-1px);border-color:var(--a1)}
.btn.primary{background:linear-gradient(135deg,var(--a1),var(--a2));border:0;color:#fff;box-shadow:0 10px 28px color-mix(in srgb,var(--a1) 35%, transparent)}
.btn.done{border-color:var(--a3);color:var(--a3);background:color-mix(in srgb,var(--a3) 12%, var(--card))}
.res-head{display:flex;flex-wrap:wrap;gap:10px;align-items:end;justify-content:space-between;margin-bottom:14px}
.res-head h2{font-family:var(--display);font-size:2.2rem;font-weight:700}
.res-meta{color:var(--muted);font-size:13px}
.res-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px}
.res-card{
  display:flex;flex-direction:column;gap:7px;padding:16px;border-radius:18px;
  background:var(--card);border:1px solid var(--border);text-decoration:none;color:inherit;
  transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease; min-height:128px; position:relative;overflow:hidden;
}
.res-card::after{content:"";position:absolute;inset:0;background:var(--shine);background-size:200% 100%;opacity:0;transition:opacity .2s}
.res-card:hover{transform:translateY(-4px) scale(1.01);border-color:var(--a1);box-shadow:var(--glow)}
.res-card:hover::after{opacity:1;animation:shimmer 1.2s linear}
.res-card .cat{font-size:10px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:var(--a2);display:flex;gap:6px;align-items:center}
.res-card .title{font-weight:800;font-size:14.5px;line-height:1.3}
.res-card .note{color:var(--muted);font-size:12px}
.res-card .url{font-family:var(--mono);font-size:10px;color:var(--faint);word-break:break-all}
.view{display:none}
.view.on{display:block;animation:pop .35s ease both}
.guide-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.guide-card{
  border-radius:22px;padding:20px;border:1px solid var(--border);background:var(--card);min-height:170px;
  box-shadow:var(--shadow);position:relative;overflow:hidden;transition:transform .15s ease;
}
.guide-card:hover{transform:translateY(-3px)}
.guide-card .big{font-size:1.6rem;margin-bottom:8px}
.guide-card h4{font-size:1.05rem;margin-bottom:8px}
.guide-card p{color:var(--muted);font-size:13px}
.kbdrow{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.kbdrow span{font-family:var(--mono);font-size:11px;border:1px solid var(--border);border-radius:10px;padding:5px 9px;color:var(--muted);background:color-mix(in srgb,var(--bg) 30%,transparent)}
.toast{
  position:fixed;bottom:20px;right:20px;z-index:99;display:none;
  background:linear-gradient(135deg,var(--card),color-mix(in srgb,var(--a3) 12%,var(--card)));
  border:1px solid var(--a3);color:var(--ink);padding:12px 16px;border-radius:16px;font-weight:800;font-size:13px;box-shadow:var(--shadow);
}
.empty{padding:48px;text-align:center;color:var(--muted);font-size:1.05rem}
.footer-note{margin-top:32px;padding-top:18px;border-top:1px solid var(--border);color:var(--muted);font-size:12px}
.ticker{
  display:flex;gap:18px;overflow:hidden;mask-image:linear-gradient(90deg,transparent,black 8%,black 92%,transparent);
  margin:0 0 16px; white-space:nowrap;
}
.ticker-track{display:flex;gap:18px;animation:marquee 40s linear infinite}
@keyframes marquee{to{transform:translateX(-50%)}}
.ticker span{
  display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;
  background:var(--card);border:1px solid var(--border);font-size:12px;font-weight:700;color:var(--muted);
}
.num-pill{font-family:var(--mono);font-size:10px;padding:2px 7px;border-radius:999px;background:color-mix(in srgb,var(--a5) 18%,transparent);color:var(--a5);font-weight:800}
@media (max-width:1200px){
  .app{grid-template-columns:var(--rail) 290px 1fr}
  .stats{grid-template-columns:repeat(3,1fr)}
  .panel-grid,.guide-grid{grid-template-columns:1fr}
}
@media (max-width:900px){
  html,body{overflow:auto}
  .app{display:block;height:auto}
  .top{position:sticky;top:0}
  .rail{display:flex;flex-direction:row;overflow:auto;border-right:0;border-bottom:1px solid var(--border);padding:8px}
  .nav{max-height:250px;border-right:0;border-bottom:1px solid var(--border)}
  .stage{overflow:visible}
  .stage-inner{padding:14px}
  .stats{grid-template-columns:repeat(2,1fr)}
  .res-grid{grid-template-columns:1fr}
}
body.nav-collapsed{--navw:0px}
body.nav-collapsed .nav{display:none}
body.focus-mode .rail, body.focus-mode .nav{display:none}
body.focus-mode .app{grid-template-columns:1fr}
"""


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def md_lite(body: str) -> str:
    lines = body.split("\n")
    out: list[str] = []
    in_ul = False
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
            out.append(f"<h3>{inline(line[3:])}</h3>")
            continue
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(line[2:])}</li>")
            continue
        close_ul()
        if line.strip():
            out.append(f"<p>{inline(line)}</p>")
    close_ul()
    flush_table()
    return "\n".join(out)


def build() -> tuple[Path, int, int]:
    lessons, meta = gen_lessons()
    links = gen_links()
    (CURR / "lifetime_sections.json").write_text(json.dumps(lessons, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (CURR / "resources_1000.json").write_text(json.dumps(links, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # nav structure
    div_order: list[str] = []
    div_map: dict = {}
    for s in lessons:
        d = s["division"]
        if d not in div_map:
            div_map[d] = {"name": s["division_name"], "chapters": {}}
            div_order.append(d)
        ch = s["chapter"]
        if ch not in div_map[d]["chapters"]:
            div_map[d]["chapters"][ch] = {"name": s["chapter_name"], "items": []}
        div_map[d]["chapters"][ch]["items"].append(s)

    nav_parts = []
    for d in div_order:
        info = div_map[d]
        nch = sum(len(c["items"]) for c in info["chapters"].values())
        nav_parts.append(
            f'<details class="div" open><summary><span class="emoji">{DIV_EMOJI.get(d,"✨")}</span><span class="did">{esc(d)}</span> {esc(info["name"])} <em>{nch}</em></summary>'
        )
        for ch, cinfo in info["chapters"].items():
            nav_parts.append(
                f'<details class="ch"><summary>{esc(ch)} · {esc(cinfo["name"])}</summary><div class="ch-links">'
            )
            for item in cinfo["items"]:
                nav_parts.append(
                    f'<a class="navlink" href="#{esc(item["id"])}" data-id="{esc(item["id"])}">{esc(item["title"][:40])}</a>'
                )
            nav_parts.append("</div></details>")
        nav_parts.append("</details>")

    lesson_cards = []
    for s in lessons:
        search = (s["id"] + " " + s["title"] + " " + s["tags"] + " " + s["body"])[:800].lower()
        emo = DIV_EMOJI.get(s["division"], "✨")
        lesson_cards.append(
            "<article class=\"sec\" id=\"{id}\" data-div=\"{div}\" data-level=\"{lvl}\" data-search=\"{search}\">"
            "<div class=\"crumb\"><span class=\"emoji-pill\">{emo}</span><span>{div2}</span><span>{ch}</span>"
            "<span class=\"lvl\">◇ {lvl2}</span><span class=\"sid\">{id2}</span></div>"
            "<h2>{emo} {title}</h2><div class=\"body\">{body}</div>"
            "<div class=\"actions\">"
            "<button type=\"button\" class=\"btn mark\" data-mark=\"{id3}\">✓ Mark studied</button>"
            "<button type=\"button\" class=\"btn copy\" data-copy=\"{id4}\">⧉ Copy id</button>"
            "<button type=\"button\" class=\"btn openres\" data-q=\"{q}\">🔗 Related resources</button>"
            "</div></article>".format(
                id=esc(s["id"]),
                div=esc(s["division"]),
                lvl=esc(s["level"]),
                search=esc(search),
                div2=esc(s["division"]),
                ch=esc(s["chapter"]),
                lvl2=esc(s["level"]),
                id2=esc(s["id"]),
                emo=emo,
                title=esc(s["title"]),
                body=md_lite(s["body"]),
                id3=esc(s["id"]),
                id4=esc(s["id"]),
                q=esc(s["title"][:40]),
            )
        )

    # resource categories
    cats = sorted({x["cat"] for x in links})
    cat_pills = "".join(
        f'<button type="button" class="pill" data-rcat="{esc(c)}">{esc(c)}</button>' for c in cats
    )

    # Embed resources as JSON for client render (faster filter) + SSR first 120 cards for no-JS
    res_json = json.dumps(links, ensure_ascii=False)
    ssr_cards = []
    for x in links[:120]:
        ce = CAT_EMOJI.get(x["cat"], "🔗")
        ssr_cards.append(
            f'<a class="res-card" href="{esc(x["url"])}" target="_blank" rel="noopener" data-cat="{esc(x["cat"])}" data-search="{esc((x["title"]+" "+x["note"]+" "+x["tags"]+" "+x["url"]).lower())}">'
            f'<div class="cat">{ce} {esc(x["cat"])}</div>'
            f'<div class="title">{esc(x["title"])}</div>'
            f'<div class="note">{esc(x["note"])}</div>'
            f'<div class="url">{esc(x["url"][:80])}</div></a>'
        )

    div_pills = "".join(
        f'<button type="button" class="pill" data-div="{esc(d)}">{esc(d)}</button>' for d in div_order
    )

    n_lessons = len(lessons)
    n_links = len(links)
    n_div = len(div_order)

    js = f"""
window.AILAB_V4 = {{
  nLessons: {n_lessons},
  nLinks: {n_links},
  divisions: {json.dumps({d: div_map[d]["name"] for d in div_order})},
  divEmoji: {json.dumps(DIV_EMOJI)},
  catEmoji: {json.dumps(CAT_EMOJI)},
  resources: {res_json}
}};
""" + r"""
(function(){
  const STUDY_KEY='ailab-v4-studied';
  const THEME_KEY='ailab-v4-theme';
  let studied=new Set();
  try{JSON.parse(localStorage.getItem(STUDY_KEY)||'[]').forEach(x=>studied.add(x))}catch(e){}
  const themeEl=document.getElementById('theme');
  const saved=localStorage.getItem(THEME_KEY)||'aurora';
  function applyTheme(v){
    if(v==='night') document.documentElement.removeAttribute('data-theme');
    else document.documentElement.setAttribute('data-theme', v);
  }
  applyTheme(saved);
  themeEl.value = saved;
  themeEl.onchange=function(){
    var v=themeEl.value;
    applyTheme(v);
    localStorage.setItem(THEME_KEY, v);
  };

  function toast(m){var t=document.getElementById('toast'); t.textContent=m; t.style.display='block'; clearTimeout(window.__tt); window.__tt=setTimeout(function(){t.style.display='none'},1500)}
  function save(){localStorage.setItem(STUDY_KEY, JSON.stringify(Array.from(studied)))}
  function refreshStudy(){
    var tot=window.AILAB_V4.nLessons, n=studied.size, pct=Math.round(n/tot*100);
    document.getElementById('progLabel').textContent=pct+'%';
    document.getElementById('progBar').style.width=pct+'%';
    document.getElementById('progText').textContent=n+' / '+tot+' lessons';
    document.getElementById('statStudied').textContent=n;
    document.querySelectorAll('a.navlink').forEach(function(a){a.classList.toggle('studied', studied.has(a.dataset.id))});
    document.querySelectorAll('button.mark').forEach(function(b){
      var id=b.dataset.mark; b.classList.toggle('done', studied.has(id));
      b.textContent=studied.has(id)?'Studied ✓':'Mark studied';
    });
  }

  // views
  var view='campus';
  function setView(v){
    view=v;
    document.querySelectorAll('.view').forEach(function(el){el.classList.toggle('on', el.id==='view-'+v)});
    document.querySelectorAll('.rail button[data-view]').forEach(function(b){b.classList.toggle('on', b.dataset.view===v)});
    if(v==='resources') renderResources();
  }
  document.querySelectorAll('.rail button[data-view]').forEach(function(b){b.onclick=function(){setView(b.dataset.view)}});

  document.getElementById('btnNav').onclick=function(){document.body.classList.toggle('nav-collapsed')};
  document.getElementById('btnFocus').onclick=function(){document.body.classList.toggle('focus-mode')};
  document.getElementById('btnExpand').onclick=function(){document.querySelectorAll('.nav details').forEach(function(d){d.open=true})};
  document.getElementById('btnRandom').onclick=function(){
    if(view!=='campus') setView('campus');
    var vis=Array.prototype.slice.call(document.querySelectorAll('#view-campus article.sec:not(.hidden)'));
    if(!vis.length) return;
    var el=vis[Math.floor(Math.random()*vis.length)];
    el.scrollIntoView({behavior:'smooth', block:'start'}); toast(el.id);
  };
  document.getElementById('btnTop').onclick=function(){document.querySelector('.stage').scrollTo({top:0,behavior:'smooth'})};

  // campus filters
  var divFilter='ALL', onlyTodo=false;
  var levelEl=document.getElementById('level');
  document.querySelectorAll('.pill[data-div]').forEach(function(p){p.onclick=function(){
    divFilter=p.dataset.div; document.querySelectorAll('.pill[data-div]').forEach(function(x){x.classList.toggle('on', x.dataset.div===divFilter)}); applyCampus();
  }});
  document.getElementById('pillTodo').onclick=function(){onlyTodo=!onlyTodo; this.classList.toggle('on', onlyTodo); applyCampus()};
  levelEl.onchange=applyCampus;

  var q=document.getElementById('q');
  q.addEventListener('input', function(){
    if(view==='resources') renderResources();
    else applyCampus();
  });
  document.addEventListener('keydown', function(e){
    if((e.metaKey||e.ctrlKey) && e.key.toLowerCase()==='k'){e.preventDefault(); q.focus(); q.select()}
    if((e.metaKey||e.ctrlKey) && e.key.toLowerCase()==='b'){e.preventDefault(); document.body.classList.toggle('nav-collapsed')}
  });

  function applyCampus(){
    var term=(q.value||'').trim().toLowerCase();
    var lvl=levelEl.value;
    document.querySelectorAll('#view-campus article.sec').forEach(function(el){
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

  document.querySelectorAll('button.mark').forEach(function(b){b.onclick=function(){
    var id=b.dataset.mark; if(studied.has(id)) studied.delete(id); else studied.add(id);
    save(); refreshStudy(); applyCampus();
  }});
  document.querySelectorAll('button.copy').forEach(function(b){b.onclick=async function(){
    try{await navigator.clipboard.writeText(b.dataset.copy); toast('Copied '+b.dataset.copy)}catch(e){toast(b.dataset.copy)}
  }});
  document.querySelectorAll('button.openres').forEach(function(b){b.onclick=function(){
    setView('resources'); q.value=b.dataset.q||''; renderResources();
  }});

  // resources render
  var rcat='ALL';
  document.getElementById('resCats').addEventListener('click', function(e){
    var t=e.target; if(!t.dataset.rcat) return;
    rcat=t.dataset.rcat;
    document.querySelectorAll('#resCats .pill').forEach(function(p){p.classList.toggle('on', p.dataset.rcat===rcat)});
    renderResources();
  });
  function renderResources(){
    var term=(q.value||'').trim().toLowerCase();
    var box=document.getElementById('resGrid');
    var html='', count=0;
    window.AILAB_V4.resources.forEach(function(x){
      if(rcat!=='ALL' && x.cat!==rcat) return;
      var hay=(x.title+' '+x.note+' '+x.tags+' '+x.url+' '+x.cat).toLowerCase();
      if(term && hay.indexOf(term)===-1) return;
      count++;
      var ce=(window.AILAB_V4.catEmoji&&window.AILAB_V4.catEmoji[x.cat])||'🔗';
      html += '<a class="res-card" href="'+x.url+'" target="_blank" rel="noopener">'
        +'<div class="cat">'+ce+' '+x.cat+'</div>'
        +'<div class="title">'+x.title+'</div>'
        +'<div class="note">'+(x.note||'')+'</div>'
        +'<div class="url">'+x.url+'</div></a>';
    });
    box.innerHTML = html || '<div class="empty">No resources match. Clear search or pick All.</div>';
    document.getElementById('resCount').textContent = count + ' shown · ' + window.AILAB_V4.nLinks + ' total';
  }

  // active nav on scroll in stage
  var stage=document.querySelector('.stage');
  var navs=Array.prototype.slice.call(document.querySelectorAll('a.navlink'));
  stage.addEventListener('scroll', function(){
    if(view!=='campus') return;
    var cur=null;
    document.querySelectorAll('#view-campus article.sec').forEach(function(el){
      if(el.classList.contains('hidden')) return;
      var r=el.getBoundingClientRect();
      if(r.top < 140) cur=el.id;
    });
    navs.forEach(function(a){a.classList.toggle('on', a.dataset.id===cur)});
  }, {passive:true});

  refreshStudy(); applyCampus(); setView('campus');
})();
"""

    doc = f"""<!DOCTYPE html>
<html lang="en" data-theme="aurora">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<meta name="description" content="AI Lab Free University v4 Portfolio — lifetime campus, stunning full-page guide, {n_links}+ resource links"/>
<title>AI Lab Free University · v4 Portfolio Campus</title>
<style>{CSS}</style>
</head>
<body>
<div class="app">
  <header class="top">
    <div class="brand">
      <div class="logo"><span>✦</span></div>
      <div>
        <h1>AI Lab Free University</h1>
        <small>✨ v4 portfolio · mesmerizing campus</small>
      </div>
    </div>
    <div class="search">
      <span>⌕</span>
      <input id="q" type="search" placeholder="✨ Search lessons, resources, vendors, Hermes, MCP, robotics…" aria-label="Search"/>
      <kbd>⌘K</kbd>
    </div>
    <div class="top-actions">
      <select id="theme" class="sel" aria-label="Theme">
        <option value="aurora" selected>✦ Aurora Dream (recommended)</option>
        <option value="night">Night Glass</option>
        <option value="day">Day Studio</option>
        <option value="paper">Paper Clean</option>
        <option value="rose">Rose Neon</option>
        <option value="ember">Ember</option>
        <option value="mint">Mint Lab</option>
      </select>
      <select id="level" class="sel" aria-label="Level">
        <option value="ALL">All levels</option>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>
      <button class="iconbtn" id="btnNav" title="Toggle nav">☰</button>
      <button class="iconbtn" id="btnFocus" title="Focus">▣</button>
      <button class="iconbtn" id="btnRandom" title="Random">✦</button>
      <button class="iconbtn" id="btnExpand" title="Expand">⬇</button>
      <button class="iconbtn" id="btnTop" title="Top">↑</button>
    </div>
  </header>

  <nav class="rail" aria-label="Primary">
    <button type="button" data-view="campus" class="on" title="Campus">📚</button>
    <button type="button" data-view="resources" title="Resources 1000+">🔗</button>
    <button type="button" data-view="guide" title="How to use">✦</button>
    <button type="button" data-view="paths" title="Paths">🗺</button>
    <div class="sp"></div>
    <div class="orb" title="Alive"></div>
    <button type="button" data-view="rtma" title="RTMA">R</button>
  </nav>

  <aside class="nav" id="sideNav">
    <div class="prog">
      <div class="row"><span>Progress</span><span id="progLabel">0%</span></div>
      <div class="bar"><i id="progBar"></i></div>
      <div class="row" style="margin-top:8px;color:var(--muted)"><span id="progText">0 lessons</span></div>
    </div>
    <h3>Divisions</h3>
    {''.join(nav_parts)}
  </aside>

  <main class="stage">
    <div class="stage-inner">
      <section class="view on" id="view-campus">
        <div class="hero">
          <div class="sparkles"></div>
          <div class="badge-row">
            <span class="badge">✨ Free forever</span>
            <span class="badge">🌐 Offline-first</span>
            <span class="badge">🧠 Lifetime mastery</span>
            <span class="badge">🎨 Portfolio beauty</span>
            <span class="badge">🔗 1000+ links</span>
          </div>
          <h2>A mesmerizing campus for local + cloud AI operators</h2>
          <p>Lessons, paths, Hermes, MCP, vendors, robotics foresight, and a living resource atlas — open one HTML file and keep learning for years. Evidence grammar: <strong>RTMA</strong> · Run · Trace · Metric · Artifact.</p>
          <div class="stats">
            <div class="stat"><div class="ico">📚</div><b>{n_lessons}</b><span>Lessons</span></div>
            <div class="stat"><div class="ico">🏛️</div><b>{n_div}</b><span>Divisions</span></div>
            <div class="stat"><div class="ico">🔗</div><b>{n_links}</b><span>Resource links</span></div>
            <div class="stat"><div class="ico">✅</div><b id="statStudied">0</b><span>Studied</span></div>
            <div class="stat"><div class="ico">🎨</div><b>7</b><span>Themes</span></div>
            <div class="stat"><div class="ico">🔑</div><b>0</b><span>Keys to start labs</span></div>
          </div>
        </div>
        <div class="ticker" aria-hidden="true"><div class="ticker-track">
          <span>🏛️ Campus</span><span>🤖 Agents</span><span>🪄 Hermes</span><span>🧲 RAG</span><span>🧪 Evals</span><span>🎙️ Voice</span><span>🦾 Robotics</span><span>☁️ Vendors</span><span>🖥️ Local Lab</span><span>RTMA</span>
          <span>🏛️ Campus</span><span>🤖 Agents</span><span>🪄 Hermes</span><span>🧲 RAG</span><span>🧪 Evals</span><span>🎙️ Voice</span><span>🦾 Robotics</span><span>☁️ Vendors</span><span>🖥️ Local Lab</span><span>RTMA</span>
        </div></div>

        <div class="panel-grid">
          <div class="panel">
            <h3>🚀 Start in 3 moves</h3>
            <ul>
              <li>① Browse divisions in the left menu (full chapter tree)</li>
              <li>② Open <strong>🔗 Resources</strong> for {n_links}+ docs & tools</li>
              <li>③ Run <code>bash scripts/verify_slice.sh</code> for proof</li>
            </ul>
          </div>
          <div class="panel">
            <h3>💎 Design principles</h3>
            <ul>
              <li>🖥️ Full viewport portfolio layout</li>
              <li>🎨 Multi-theme visual systems</li>
              <li>⌕ Search lessons + atlas together</li>
              <li>🛡️ Permissions are perimeter · no secrets</li>
            </ul>
          </div>
        </div>

        <div class="filters">
          <button type="button" class="pill on" data-div="ALL">All divisions</button>
          {div_pills}
          <button type="button" class="pill" id="pillTodo">Unstudied only</button>
        </div>
        {''.join(lesson_cards)}
        <div class="footer-note">AI Lab Free University v4 · MIT educational · No warranty · Sibling: UC Lab Free University · Author CYPHER0X9</div>
      </section>

      <section class="view" id="view-resources">
        <div class="res-head">
          <div>
            <h2>🔗 Resource atlas</h2>
            <div class="res-meta" id="resCount">{n_links} curated links · filter & search · open in new tab</div>
          </div>
          <button type="button" class="btn primary" onclick="document.getElementById('q').focus()">Search atlas</button>
        </div>
        <div class="filters" id="resCats">
          <button type="button" class="pill on" data-rcat="ALL">All</button>
          {cat_pills}
        </div>
        <div class="res-grid" id="resGrid">{''.join(ssr_cards)}</div>
        <div class="footer-note">Links are public educational hubs. Pin vendor docs for production. This atlas is a map, not a warranty.</div>
      </section>

      <section class="view" id="view-guide">
        <div class="hero"><div class="eyebrow">Multi-feature guide</div><h2>How to use this campus like a pro</h2>
        <p>Full-page layout: rail modes, collapsible curriculum, themes, search, resource atlas, study progress, focus mode.</p></div>
        <div class="guide-grid">
          <div class="guide-card"><div class="big">📚</div><h4>Rail modes</h4><p>📚 Campus lessons · 🔗 Resource atlas ({n_links}+) · ✦ Guide · 🗺 Paths · R RTMA cheat</p></div>
          <div class="guide-card"><div class="big">⌨️</div><h4>Keyboard</h4><div class="kbdrow"><span>⌘/Ctrl K search</span><span>⌘/Ctrl B nav</span><span>Focus button</span><span>Random ✦</span></div></div>
          <div class="guide-card"><div class="big">🎨</div><h4>Themes</h4><p>Night Glass · Day Studio · Paper Clean · Rose Neon · Ember · Mint Lab — pick what keeps you studying.</p></div>
          <div class="guide-card"><div class="big">🔁</div><h4>Study loop</h4><p>Read → experiment → RTMA artifact → mark studied → open related resources → re-test weekly canaries.</p></div>
          <div class="guide-card"><div class="big">🧪</div><h4>Runnable labs</h4><p><code>bash scripts/verify_slice.sh</code> — zero API keys. Mock brain honest if Ollama is down.</p></div>
          <div class="guide-card"><div class="big">🎁</div><h4>Share</h4><p>Zip <code>v4-PORTFOLIO.html.zip</code> · still browser-friendly vs multi-hundred-MB dumps.</p></div>
        </div>
      </section>

      <section class="view" id="view-paths">
        <div class="hero"><div class="eyebrow">Audience paths</div><h2>Pick a rail. Ignore the rest (for now).</h2></div>
        <div class="guide-grid">
          <div class="guide-card"><div class="big">①</div><h4>A · Beginner</h4><p>D00 → RTMA → D01/D05 → golden slice labs → resource atlas “Local Lab”.</p></div>
          <div class="guide-card"><div class="big">②</div><h4>B · Domain expert</h4><p>RTMA ↔ your incident grammar → agents D09 → evals D11 → domain braid.</p></div>
          <div class="guide-card"><div class="big">③</div><h4>C · Engineer</h4><p>D01 + D07 + D09 + D11 + D13 · read lab source · ship scorecards.</p></div>
          <div class="guide-card"><div class="big">🪄</div><h4>D · Hermes track</h4><p>D10 fully · approval gates · coach patterns · never YOLO unattended high privilege.</p></div>
          <div class="guide-card"><div class="big">🎙️</div><h4>E · Voice/UC</h4><p>D12 + sibling UC free pack · latency budgets · human handoff.</p></div>
          <div class="guide-card"><div class="big">🦾</div><h4>F · Future/robotics</h4><p>D14 foresight · VLA/world models · safety first · sim before real.</p></div>
        </div>
      </section>

      <section class="view" id="view-rtma">
        <div class="hero"><div class="eyebrow">Evidence grammar</div><h2>Run · Trace · Metric · Artifact</h2>
        <p>AI twin of UC LICC. Falsifier first. If you cannot show these four, you do not yet know the lesson.</p></div>
        <div class="guide-grid">
          <div class="guide-card"><div class="big">▶️</div><h4>Run</h4><p>Exact command, notebook, Hermes task, or lab script executed.</p></div>
          <div class="guide-card"><div class="big">🧵</div><h4>Trace</h4><p>Request IDs, logs, tool-call chain, timeline of events.</p></div>
          <div class="guide-card"><div class="big">📏</div><h4>Metric</h4><p>Latency, tokens, cost, pass rate, error rate, approval lag.</p></div>
          <div class="guide-card"><div class="big">📦</div><h4>Artifact</h4><p>File you can reopen: JSON, report, checklist, scrubbed screenshot.</p></div>
          <div class="guide-card"><div class="big">⚡</div><h4>Falsifier</h4><p>What observation would kill “the model is smart enough”?</p></div>
          <div class="guide-card"><div class="big">🛡️</div><h4>Perimeter</h4><p>Permissions are perimeter when agents run tools. No unattended YOLO.</p></div>
        </div>
      </section>
    </div>
  </main>
</div>
<div class="toast" id="toast"></div>
<script>
{js}
</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    return OUT, n_lessons, n_links


if __name__ == "__main__":
    path, nl, nr = build()
    size = path.stat().st_size
    print(f"Wrote {path}")
    print(f"Lessons: {nl}")
    print(f"Links: {nr}")
    print(f"Size: {size} bytes ({size/1024/1024:.2f} MB)")
