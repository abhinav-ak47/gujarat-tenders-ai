"""
Flask Application – Gujarat Skill Development Tender Eligibility Pilot Engine
Deloitte Skill Development & Livelihoods Practice  |  v3.0 – Fully Responsive
"""

import os
from flask import Flask, jsonify, render_template_string
from tenders_data import TENDERS
from eligibility_engine import COMPANY_PROFILE, check_tender_eligibility

app = Flask(__name__)


def run_engine():
    results = [check_tender_eligibility(t, COMPANY_PROFILE) for t in TENDERS]
    summary = {
        "total":   len(results),
        "passed":  sum(1 for r in results if r["status"] == "PASSED"),
        "failed":  sum(1 for r in results if r["status"] == "FAILED"),
        "manual":  sum(1 for r in results if r["status"] == "MANUAL CHECK"),
    }
    return results, summary


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
<meta name="theme-color" content="#080c18"/>
<meta name="apple-mobile-web-app-capable" content="yes"/>
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
<title>Deloitte | Gujarat Tender Engine</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>

/* ══════════════════════════════════════════════
   DESIGN TOKENS
══════════════════════════════════════════════ */
:root {
  --bg:          #080c18;
  --bg2:         #0d1121;
  --surface:     #111827;
  --surface2:    #1a2035;
  --card:        #141928;
  --card2:       #1e2640;
  --border:      rgba(255,255,255,0.07);
  --border2:     rgba(255,255,255,0.13);

  --deloitte:    #86BC25;
  --deloitte2:   #6fa01e;
  --accent:      #6366f1;
  --accent2:     #818cf8;

  --pass:        #22c55e;
  --pass-dim:    #16a34a;
  --pass-bg:     rgba(34,197,94,0.09);
  --pass-border: rgba(34,197,94,0.22);
  --fail:        #f43f5e;
  --fail-dim:    #e11d48;
  --fail-bg:     rgba(244,63,94,0.09);
  --fail-border: rgba(244,63,94,0.22);
  --manual:      #f59e0b;
  --manual-dim:  #d97706;
  --manual-bg:   rgba(245,158,11,0.09);
  --manual-border:rgba(245,158,11,0.22);

  --text:        #f1f5f9;
  --text2:       #cbd5e1;
  --muted:       #64748b;
  --muted2:      #94a3b8;

  --sidebar-w:   260px;
  --topbar-h:    60px;
  --bottomnav-h: 64px;
  --radius:      14px;
  --radius-sm:   9px;
  --radius-lg:   20px;
  --shadow:      0 8px 32px rgba(0,0,0,0.5);
  --shadow-lg:   0 24px 64px rgba(0,0,0,0.6);
}

/* ══════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════ */
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html { scroll-behavior:smooth; -webkit-tap-highlight-color:transparent; }
body {
  font-family:'Inter',system-ui,sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}

/* ══════════════════════════════════════════════
   SIDEBAR – DESKTOP
══════════════════════════════════════════════ */
.sidebar {
  position:fixed; top:0; left:0; bottom:0;
  width:var(--sidebar-w);
  background:linear-gradient(180deg,#0d1121 0%,#080c18 100%);
  border-right:1px solid var(--border);
  display:flex; flex-direction:column;
  z-index:300;
  transition:transform 0.3s cubic-bezier(.4,0,.2,1);
  overflow-y:auto;
}
.sidebar-logo {
  padding:18px 16px 14px;
  border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:11px;
  flex-shrink:0;
}
.logo-mark {
  width:38px; height:38px; border-radius:10px;
  background:linear-gradient(135deg,var(--deloitte),var(--deloitte2));
  display:flex; align-items:center; justify-content:center;
  font-size:1.1rem; font-weight:900; color:#000; flex-shrink:0;
  box-shadow:0 4px 14px rgba(134,188,37,0.35);
}
.logo-text .l1 { font-size:0.82rem; font-weight:800; color:var(--text); font-family:'Space Grotesk',sans-serif; }
.logo-text .l2 { font-size:0.62rem; color:var(--muted2); margin-top:1px; }
.sidebar-close {
  margin-left:auto; background:none; border:none;
  color:var(--muted); font-size:1.1rem; cursor:pointer;
  display:none; padding:4px; border-radius:6px;
}
.sidebar-close:hover { color:var(--text); background:var(--surface2); }

.sidebar-section { padding:10px 10px 0; }
.sidebar-label {
  font-size:0.6rem; font-weight:700; letter-spacing:1.2px;
  text-transform:uppercase; color:var(--muted);
  padding:8px 8px 4px;
}
.nav-item {
  display:flex; align-items:center; gap:10px;
  padding:10px 11px; border-radius:9px; cursor:pointer;
  transition:all 0.17s; font-size:0.82rem; font-weight:500;
  color:var(--muted2); position:relative;
  user-select:none; margin-bottom:2px;
}
.nav-item:hover { background:var(--surface2); color:var(--text); }
.nav-item.active {
  background:linear-gradient(90deg,rgba(134,188,37,0.13),rgba(134,188,37,0.04));
  color:var(--deloitte); font-weight:600;
}
.nav-item.active::before {
  content:''; position:absolute; left:0; top:22%; bottom:22%;
  width:3px; background:var(--deloitte); border-radius:0 3px 3px 0;
}
.nav-icon { font-size:0.95rem; width:18px; text-align:center; flex-shrink:0; }
.nav-badge {
  margin-left:auto; min-width:22px; height:19px;
  background:var(--surface2); border-radius:10px;
  font-size:0.65rem; font-weight:700; color:var(--muted2);
  display:flex; align-items:center; justify-content:center; padding:0 6px;
}
.nav-badge.g { background:var(--pass-bg);    color:var(--pass);   }
.nav-badge.r { background:var(--fail-bg);    color:var(--fail);   }
.nav-badge.a { background:var(--manual-bg);  color:var(--manual); }

.sidebar-footer {
  margin-top:auto; padding:14px 16px;
  border-top:1px solid var(--border);
  font-size:0.68rem; color:var(--muted); text-align:center;
  flex-shrink:0;
}

/* Overlay for mobile sidebar */
.sidebar-overlay {
  display:none; position:fixed; inset:0;
  background:rgba(0,0,0,0.6); backdrop-filter:blur(4px);
  z-index:250;
}
.sidebar-overlay.show { display:block; }

/* ══════════════════════════════════════════════
   TOP BAR
══════════════════════════════════════════════ */
.topbar {
  position:fixed; top:0; left:var(--sidebar-w); right:0;
  height:var(--topbar-h);
  background:rgba(8,12,24,0.88);
  backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:12px;
  padding:0 20px; z-index:200;
}
.hamburger {
  display:none; background:var(--surface); border:1px solid var(--border2);
  color:var(--text2); width:36px; height:36px; border-radius:8px;
  align-items:center; justify-content:center;
  cursor:pointer; font-size:1.1rem; flex-shrink:0;
}
.topbar-title { font-size:0.88rem; font-weight:700; color:var(--text); font-family:'Space Grotesk',sans-serif; }
.topbar-sub { font-size:0.7rem; color:var(--muted); }
.topbar-right { display:flex; align-items:center; gap:10px; margin-left:auto; }
.search-wrap { position:relative; }
.search-box {
  background:var(--surface); border:1px solid var(--border2);
  color:var(--text); padding:7px 12px 7px 34px;
  border-radius:9px; font-size:0.8rem; width:200px;
  outline:none; font-family:'Inter',sans-serif;
  transition:border-color 0.2s, box-shadow 0.2s;
}
.search-box::placeholder { color:var(--muted); }
.search-box:focus { border-color:var(--deloitte); box-shadow:0 0 0 3px rgba(134,188,37,0.1); }
.search-icon { position:absolute; left:10px; top:50%; transform:translateY(-50%); color:var(--muted); font-size:0.8rem; pointer-events:none; }
.topbar-badge {
  padding:4px 11px; border-radius:20px; font-size:0.68rem; font-weight:700; white-space:nowrap;
}
.pilot-badge { background:rgba(134,188,37,0.12); color:var(--deloitte); border:1px solid rgba(134,188,37,0.28); }
.date-badge  { background:var(--surface); color:var(--muted2); border:1px solid var(--border2); }

/* ══════════════════════════════════════════════
   MAIN CONTENT
══════════════════════════════════════════════ */
.page-content {
  margin-left:var(--sidebar-w);
  margin-top:var(--topbar-h);
  min-height:calc(100vh - var(--topbar-h));
}
.view { display:none; padding:24px 28px 56px; animation:fadeIn 0.22s ease; }
.view.active { display:block; }
@keyframes fadeIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }

/* ══════════════════════════════════════════════
   PAGE HERO
══════════════════════════════════════════════ */
.page-hero {
  background:linear-gradient(135deg,var(--surface) 0%,var(--card2) 100%);
  border:1px solid var(--border); border-radius:var(--radius-lg);
  padding:24px 28px; margin-bottom:24px;
  position:relative; overflow:hidden;
}
.page-hero::before {
  content:''; position:absolute; top:-60px; right:-60px;
  width:180px; height:180px;
  background:radial-gradient(circle,rgba(134,188,37,0.09) 0%,transparent 70%);
  pointer-events:none;
}
.page-hero-title {
  font-size:1.45rem; font-weight:800; color:#fff;
  font-family:'Space Grotesk',sans-serif; margin-bottom:5px;
}
.page-hero-title span { color:var(--deloitte); }
.page-hero-sub { font-size:0.8rem; color:var(--muted2); line-height:1.55; }

/* ══════════════════════════════════════════════
   STAT GRID
══════════════════════════════════════════════ */
.stat-grid {
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:14px; margin-bottom:24px;
}
.stat-card {
  background:var(--card); border:1px solid var(--border);
  border-radius:var(--radius); padding:18px 20px;
  cursor:pointer; position:relative; overflow:hidden;
  transition:all 0.22s cubic-bezier(.4,0,.2,1);
}
.stat-card::after {
  content:''; position:absolute; bottom:0; left:0; right:0;
  height:2px; background:var(--sc-color); transition:height 0.2s;
}
.stat-card:hover { transform:translateY(-3px); box-shadow:var(--shadow); border-color:var(--border2); }
.stat-card:hover::after { height:3px; }
.stat-card.active { border-color:var(--sc-color); box-shadow:0 0 0 1px var(--sc-color),var(--shadow); }
.sc-total  { --sc-color:var(--accent); }
.sc-pass   { --sc-color:var(--pass);   }
.sc-fail   { --sc-color:var(--fail);   }
.sc-manual { --sc-color:var(--manual); }
.sc-icon { font-size:1.4rem; margin-bottom:10px; display:block; }
.sc-num  { font-size:2.2rem; font-weight:900; color:var(--sc-color); font-family:'Space Grotesk',sans-serif; line-height:1; margin-bottom:3px; }
.sc-lbl  { font-size:0.77rem; font-weight:600; color:var(--text2); }
.sc-pct  { font-size:0.68rem; color:var(--muted); margin-top:2px; }
.sc-trend {
  position:absolute; top:14px; right:14px;
  font-size:0.65rem; font-weight:700;
  background:var(--sc-bg,var(--surface2)); color:var(--sc-color);
  padding:3px 7px; border-radius:6px;
}
.sc-pass   .sc-trend { --sc-bg:var(--pass-bg);   }
.sc-fail   .sc-trend { --sc-bg:var(--fail-bg);   }
.sc-manual .sc-trend { --sc-bg:var(--manual-bg); }

/* ══════════════════════════════════════════════
   TOOLBAR
══════════════════════════════════════════════ */
.toolbar {
  display:flex; align-items:center; gap:10px;
  margin-bottom:18px; flex-wrap:wrap;
}
.tab-group {
  display:flex; background:var(--surface);
  border:1px solid var(--border); border-radius:10px;
  padding:4px; gap:3px; flex-wrap:wrap;
}
.tab-btn {
  padding:7px 14px; border-radius:7px; border:none;
  background:transparent; color:var(--muted2);
  cursor:pointer; font-size:0.78rem; font-weight:600;
  transition:all 0.17s; display:flex; align-items:center; gap:5px;
  font-family:'Inter',sans-serif; white-space:nowrap;
}
.tab-btn:hover { color:var(--text); background:var(--surface2); }
.tab-btn.active { background:var(--tb-color); color:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.4); }
.t-all    { --tb-color:var(--accent);     }
.t-pass   { --tb-color:var(--pass-dim);   }
.t-fail   { --tb-color:var(--fail-dim);   }
.t-manual { --tb-color:var(--manual-dim); }
.tab-count { background:rgba(255,255,255,0.18); border-radius:5px; font-size:0.62rem; padding:1px 5px; font-weight:700; }
.sort-sel {
  background:var(--surface); border:1px solid var(--border);
  color:var(--text2); padding:8px 11px; border-radius:9px;
  font-size:0.78rem; outline:none; cursor:pointer; font-family:'Inter',sans-serif;
}
.sort-sel:focus { border-color:var(--deloitte); }
.result-count { margin-left:auto; font-size:0.75rem; color:var(--muted); white-space:nowrap; }
.result-count strong { color:var(--text2); }

/* ══════════════════════════════════════════════
   TENDER CARDS
══════════════════════════════════════════════ */
.tender-list { display:flex; flex-direction:column; gap:10px; }

.t-card {
  background:var(--card); border:1px solid var(--border);
  border-radius:var(--radius); overflow:hidden;
  transition:all 0.2s cubic-bezier(.4,0,.2,1);
}
.t-card:hover { border-color:var(--border2); box-shadow:var(--shadow); }
.t-card.status-PASSED       { border-left:3px solid var(--pass);   }
.t-card.status-FAILED       { border-left:3px solid var(--fail);   }
.t-card.status-MANUAL-CHECK { border-left:3px solid var(--manual); }

.t-header {
  display:grid; grid-template-columns:1fr auto auto;
  align-items:center; gap:12px;
  padding:15px 16px 12px 18px; cursor:pointer;
}
.t-id    { font-size:0.65rem; font-weight:700; color:var(--accent2); letter-spacing:0.5px; text-transform:uppercase; margin-bottom:3px; }
.t-title { font-size:0.9rem; font-weight:700; color:var(--text); line-height:1.3; font-family:'Space Grotesk',sans-serif; transition:color 0.15s; }
.t-card:hover .t-title { color:var(--deloitte); }
.t-dept  { font-size:0.73rem; color:var(--muted2); margin-top:3px; }

.status-pill {
  padding:5px 12px; border-radius:20px;
  font-size:0.67rem; font-weight:700; letter-spacing:0.4px; white-space:nowrap; flex-shrink:0;
}
.pill-PASSED       { background:var(--pass-bg);   color:var(--pass);   border:1px solid var(--pass-border);   }
.pill-FAILED       { background:var(--fail-bg);   color:var(--fail);   border:1px solid var(--fail-border);   }
.pill-MANUAL-CHECK { background:var(--manual-bg); color:var(--manual); border:1px solid var(--manual-border); }

.chev-btn {
  background:var(--surface2); border:1px solid var(--border);
  color:var(--muted2); width:28px; height:28px; border-radius:7px;
  display:flex; align-items:center; justify-content:center;
  cursor:pointer; font-size:0.7rem; transition:all 0.18s; flex-shrink:0;
}
.chev-btn:hover { background:var(--surface); color:var(--text); }
.chev-btn.open  { background:var(--deloitte); border-color:var(--deloitte); color:#000; }

.t-meta {
  display:flex; background:rgba(0,0,0,0.22);
  border-top:1px solid var(--border); border-bottom:1px solid var(--border);
  font-size:0.73rem; color:var(--muted2); overflow-x:auto;
  scrollbar-width:none;
}
.t-meta::-webkit-scrollbar { display:none; }
.t-meta-item {
  display:flex; align-items:center; gap:5px;
  padding:8px 14px; border-right:1px solid var(--border);
  white-space:nowrap; flex-shrink:0;
}
.t-meta-item:last-child { border-right:none; }
.t-meta-item .v { font-weight:600; color:var(--text); }

.score-wrap { padding:7px 18px; background:rgba(0,0,0,0.14); }
.score-row  { display:flex; justify-content:space-between; font-size:0.67rem; color:var(--muted); margin-bottom:3px; }
.score-row strong { color:var(--text2); }
.score-track { background:var(--surface); border-radius:6px; height:5px; overflow:hidden; }
.score-fill  { height:100%; border-radius:6px; transition:width 0.7s cubic-bezier(.4,0,.2,1); }

.t-body { display:none; padding:18px 18px 20px; border-top:1px solid var(--border); }
.t-body.open { display:block; animation:slideDown 0.22s ease; }
@keyframes slideDown { from{opacity:0;transform:translateY(-5px)} to{opacity:1;transform:translateY(0)} }

.scope-box {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius-sm); padding:11px 14px;
  font-size:0.78rem; color:var(--muted2); line-height:1.6; margin-bottom:16px;
}
.scope-box strong { color:var(--text2); }

.gates-hdr {
  font-size:0.67rem; font-weight:700; letter-spacing:1px;
  text-transform:uppercase; color:var(--muted); margin-bottom:9px;
  display:flex; align-items:center; gap:8px;
}
.gates-hdr::after { content:''; flex:1; height:1px; background:var(--border); }

.gate-list { display:flex; flex-direction:column; gap:6px; margin-bottom:14px; }

.gate-row {
  display:grid; grid-template-columns:30px 1fr auto;
  align-items:start; gap:10px;
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius-sm); padding:10px 13px;
}
.gate-row.gp { border-left:2px solid var(--pass);   }
.gate-row.gf { border-left:2px solid var(--fail);   }
.gate-row.gm { border-left:2px solid var(--manual); }
.g-icon { width:28px; height:28px; border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:0.85rem; flex-shrink:0; }
.gp .g-icon { background:var(--pass-bg);   }
.gf .g-icon { background:var(--fail-bg);   }
.gm .g-icon { background:var(--manual-bg); }
.g-crit   { font-size:0.79rem; font-weight:600; color:var(--text); margin-bottom:2px; }
.g-reason { font-size:0.72rem; color:var(--muted2); line-height:1.4; }
.g-compare { display:flex; gap:8px; margin-top:5px; flex-wrap:wrap; }
.g-chip {
  font-size:0.66rem; background:var(--surface2); border:1px solid var(--border);
  border-radius:5px; padding:2px 7px; color:var(--muted2);
}
.g-chip strong { color:var(--text2); }
.g-badge {
  font-size:0.64rem; font-weight:700; padding:3px 9px; border-radius:6px;
  white-space:nowrap; flex-shrink:0; align-self:flex-start; margin-top:2px;
}
.gp .g-badge { background:var(--pass-bg);   color:var(--pass);   border:1px solid var(--pass-border);   }
.gf .g-badge { background:var(--fail-bg);   color:var(--fail);   border:1px solid var(--fail-border);   }
.gm .g-badge { background:var(--manual-bg); color:var(--manual); border:1px solid var(--manual-border); }

.reason-panel { border-radius:var(--radius-sm); padding:12px 14px; margin-top:6px; font-size:0.76rem; line-height:1.5; }
.r-fail   { background:var(--fail-bg);   border:1px solid var(--fail-border);   }
.r-manual { background:var(--manual-bg); border:1px solid var(--manual-border); }
.r-title  { font-weight:700; margin-bottom:7px; display:flex; align-items:center; gap:5px; }
.rt-fail   { color:var(--fail);   }
.rt-manual { color:var(--manual); }
.r-item { color:var(--muted2); margin-bottom:3px; display:flex; gap:7px; }
.r-item::before { content:'›'; color:var(--muted); flex-shrink:0; }

/* ══════════════════════════════════════════════
   ANALYTICS
══════════════════════════════════════════════ */
.analytics-grid { display:grid; grid-template-columns:1.7fr 1fr; gap:18px; }
.a-card { background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:20px; }
.a-title { font-size:0.76rem; font-weight:700; color:var(--text2); margin-bottom:16px; font-family:'Space Grotesk',sans-serif; }

.bar-chart { display:flex; flex-direction:column; gap:12px; }
.bar-row   { display:flex; align-items:center; gap:10px; }
.bar-lbl   { font-size:0.7rem; color:var(--muted2); width:145px; flex-shrink:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.bar-track { flex:1; background:var(--surface); border-radius:4px; height:7px; overflow:hidden; display:flex; }
.bar-fill  { height:100%; transition:width 0.8s ease; }
.bar-val   { font-size:0.68rem; font-weight:600; color:var(--fail); width:44px; text-align:right; flex-shrink:0; }

.ring-wrap { display:flex; flex-direction:column; gap:14px; }
.ring-item { display:flex; align-items:center; gap:10px; font-size:0.78rem; }
.ring-dot  { width:9px; height:9px; border-radius:50%; flex-shrink:0; }
.ring-name { flex:1; color:var(--muted2); }
.ring-bg   { width:55px; height:5px; background:var(--surface); border-radius:3px; overflow:hidden; }
.ring-fill { height:100%; border-radius:3px; transition:width 0.8s ease; }
.ring-pct  { font-weight:700; font-size:0.78rem; width:36px; text-align:right; }

.val-table { width:100%; border-collapse:collapse; font-size:0.75rem; }
.val-table th { text-align:left; padding:9px 12px; font-size:0.63rem; font-weight:700; letter-spacing:0.8px; text-transform:uppercase; color:var(--muted); border-bottom:1px solid var(--border); }
.val-table td { padding:9px 12px; border-bottom:1px solid var(--border); color:var(--muted2); }
.val-table tr:hover td { background:var(--surface2); }
.val-table td:first-child { color:var(--text2); font-weight:500; }
.tp { color:var(--pass); }
.tf { color:var(--fail); }
.tm { color:var(--manual); }

.opp-card { text-align:center; padding:16px 0; }
.opp-val  { font-size:2rem; font-weight:900; color:var(--deloitte); font-family:'Space Grotesk',sans-serif; }
.opp-sub  { font-size:0.72rem; color:var(--muted); margin-top:4px; }
.opp-of   { font-size:0.68rem; color:var(--muted2); margin-top:6px; }

/* ══════════════════════════════════════════════
   COMPANY PROFILE
══════════════════════════════════════════════ */
.profile-hero {
  background:linear-gradient(135deg,#0d1a08 0%,var(--card2) 100%);
  border:1px solid rgba(134,188,37,0.2); border-radius:var(--radius-lg);
  padding:26px 28px; margin-bottom:20px;
  display:grid; grid-template-columns:auto 1fr; gap:20px;
  align-items:center; position:relative; overflow:hidden;
}
.profile-hero::before {
  content:''; position:absolute; top:-60px; right:-60px;
  width:200px; height:200px;
  background:radial-gradient(circle,rgba(134,188,37,0.07) 0%,transparent 70%);
}
.co-logo {
  width:64px; height:64px; background:linear-gradient(135deg,var(--deloitte),#5a9a1a);
  border-radius:16px; display:flex; align-items:center; justify-content:center;
  font-size:1.7rem; box-shadow:0 8px 28px rgba(134,188,37,0.28); flex-shrink:0;
}
.co-name    { font-size:1.15rem; font-weight:800; color:#fff; font-family:'Space Grotesk',sans-serif; margin-bottom:5px; }
.co-tag     { font-size:0.76rem; color:var(--muted2); margin-bottom:12px; }
.cert-wrap  { display:flex; flex-wrap:wrap; gap:6px; }
.cert-chip  {
  background:rgba(134,188,37,0.1); border:1px solid rgba(134,188,37,0.24);
  color:var(--deloitte); border-radius:6px; padding:3px 9px;
  font-size:0.68rem; font-weight:600; display:flex; align-items:center; gap:4px;
}
.kpi-grid {
  display:grid; grid-template-columns:repeat(5,1fr);
  gap:12px; margin-bottom:20px;
}
.kpi {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius-sm); padding:14px; text-align:center;
}
.kpi-val { font-size:1.35rem; font-weight:800; color:var(--deloitte); font-family:'Space Grotesk',sans-serif; }
.kpi-lbl { font-size:0.65rem; color:var(--muted); margin-top:3px; }
.profile-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.p-card { background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:20px; }
.p-title {
  font-size:0.67rem; font-weight:700; letter-spacing:1px; text-transform:uppercase;
  color:var(--muted); margin-bottom:14px; display:flex; align-items:center; gap:8px;
}
.p-title::after { content:''; flex:1; height:1px; background:var(--border); }
.p-row { display:flex; justify-content:space-between; align-items:center; padding:9px 0; border-bottom:1px solid var(--border); font-size:0.8rem; }
.p-row:last-child { border-bottom:none; }
.p-row span { color:var(--muted2); }
.p-row strong { color:var(--deloitte); }
.result-box {
  display:flex; justify-content:space-between; align-items:center;
  border-radius:var(--radius-sm); padding:12px 14px; margin-bottom:8px;
  font-size:0.8rem; font-weight:600;
}
.rb-pass   { background:var(--pass-bg);   border:1px solid var(--pass-border);   color:var(--pass);   }
.rb-fail   { background:var(--fail-bg);   border:1px solid var(--fail-border);   color:var(--fail);   }
.rb-manual { background:var(--manual-bg); border:1px solid var(--manual-border); color:var(--manual); }
.rb-num    { font-size:1.35rem; font-weight:900; font-family:'Space Grotesk',sans-serif; }

/* ══════════════════════════════════════════════
   DASHBOARD – QUICK LISTS
══════════════════════════════════════════════ */
.section-hdr {
  font-size:0.68rem; font-weight:700; letter-spacing:1px;
  text-transform:uppercase; color:var(--muted); margin-bottom:10px;
  display:flex; align-items:center; gap:8px;
}
.section-hdr::after { content:''; flex:1; height:1px; background:var(--border); }
.section-link { color:var(--deloitte); cursor:pointer; font-size:0.68rem; }
.quick-item {
  background:var(--card); border:1px solid var(--border);
  border-radius:var(--radius-sm); padding:11px 14px;
  display:flex; align-items:center; gap:12px; margin-bottom:7px;
  cursor:pointer; transition:border-color 0.15s;
}
.quick-item:hover { border-color:var(--border2); }
.qi-id    { font-size:0.63rem; font-weight:700; color:var(--accent2); width:90px; flex-shrink:0; }
.qi-title { font-size:0.8rem; font-weight:600; color:var(--text); flex:1; }
.qi-val   { font-size:0.68rem; padding:3px 9px; border-radius:5px; white-space:nowrap; }
.qi-gates { font-size:0.68rem; color:var(--muted); white-space:nowrap; }

/* ══════════════════════════════════════════════
   BOTTOM NAV (Mobile only)
══════════════════════════════════════════════ */
.bottom-nav {
  display:none; position:fixed; bottom:0; left:0; right:0;
  height:var(--bottomnav-h); background:rgba(13,17,33,0.96);
  backdrop-filter:blur(20px); border-top:1px solid var(--border);
  z-index:300; justify-content:space-around; align-items:center;
  padding:0 4px 4px;
}
.bn-item {
  display:flex; flex-direction:column; align-items:center; gap:3px;
  padding:6px 10px; border-radius:10px; cursor:pointer;
  transition:all 0.17s; flex:1; max-width:72px;
}
.bn-item.active { background:rgba(134,188,37,0.1); }
.bn-icon { font-size:1.2rem; line-height:1; }
.bn-label { font-size:0.58rem; font-weight:600; color:var(--muted); transition:color 0.17s; white-space:nowrap; }
.bn-item.active .bn-label { color:var(--deloitte); }
.bn-badge {
  position:absolute; top:-3px; right:-3px;
  min-width:16px; height:16px; border-radius:8px;
  font-size:0.55rem; font-weight:700; color:#fff;
  display:flex; align-items:center; justify-content:center; padding:0 4px;
}
.bn-badge.g { background:var(--pass-dim); }
.bn-badge.r { background:var(--fail-dim); }
.bn-badge.a { background:var(--manual-dim); }
.bn-icon-wrap { position:relative; }

/* ══════════════════════════════════════════════
   EMPTY STATE
══════════════════════════════════════════════ */
.empty-state { text-align:center; padding:60px 20px; color:var(--muted); }
.empty-icon  { font-size:3rem; margin-bottom:12px; }
.empty-text  { font-size:0.85rem; }

/* ══════════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════════ */
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--surface2); border-radius:3px; }

/* ══════════════════════════════════════════════
   RESPONSIVE – TABLET (≤1024px)
══════════════════════════════════════════════ */
@media(max-width:1024px) {
  .analytics-grid { grid-template-columns:1fr; }
  .kpi-grid { grid-template-columns:repeat(3,1fr); }
  .stat-grid { grid-template-columns:repeat(2,1fr); }
}

/* ══════════════════════════════════════════════
   RESPONSIVE – MOBILE (≤768px)
══════════════════════════════════════════════ */
@media(max-width:768px) {
  :root {
    --sidebar-w:0px;
    --topbar-h:56px;
  }

  /* Hide desktop sidebar, show overlay-based */
  .sidebar {
    transform:translateX(-260px);
    width:260px;
    box-shadow:var(--shadow-lg);
  }
  .sidebar.open { transform:translateX(0); }
  .sidebar-close { display:flex; }

  /* Topbar adjustments */
  .topbar { left:0; padding:0 14px; }
  .hamburger { display:flex; }
  .topbar-title { font-size:0.82rem; }
  .topbar-sub { display:none; }
  .date-badge { display:none; }
  .search-box { width:150px; font-size:0.75rem; }

  /* Content full width */
  .page-content { margin-left:0; margin-bottom:var(--bottomnav-h); }
  .view { padding:16px 14px 16px; }

  /* Bottom nav visible */
  .bottom-nav { display:flex; }

  /* Page hero */
  .page-hero { padding:18px 18px; border-radius:14px; }
  .page-hero-title { font-size:1.15rem; }

  /* Stat grid 2x2 */
  .stat-grid { grid-template-columns:repeat(2,1fr); gap:10px; margin-bottom:16px; }
  .sc-num { font-size:1.8rem; }
  .stat-card { padding:14px 16px; }

  /* Tender card adjustments */
  .t-header { grid-template-columns:1fr auto; gap:10px; padding:13px 14px 10px 16px; }
  .chev-btn { display:none; } /* tap whole header on mobile */
  .t-title { font-size:0.85rem; }
  .t-meta-item { padding:7px 11px; font-size:0.7rem; }
  .gate-row { grid-template-columns:26px 1fr; }
  .g-badge { display:none; } /* badge shown in icon instead */

  /* Profile */
  .profile-hero { grid-template-columns:1fr; text-align:center; }
  .co-logo { margin:0 auto; }
  .cert-wrap { justify-content:center; }
  .kpi-grid { grid-template-columns:repeat(3,1fr); }
  .profile-grid { grid-template-columns:1fr; }

  /* Analytics */
  .analytics-grid { grid-template-columns:1fr; }
  .bar-lbl { width:110px; }

  /* Quick items */
  .quick-item { flex-wrap:wrap; gap:8px; }
  .qi-title { min-width:0; }

  /* Toolbar */
  .toolbar { gap:8px; }
  .tab-group { gap:2px; }
  .tab-btn { padding:6px 10px; font-size:0.73rem; }
  .sort-sel { font-size:0.73rem; padding:7px 9px; }
  .result-count { display:none; }
}

/* ══════════════════════════════════════════════
   RESPONSIVE – SMALL MOBILE (≤420px)
══════════════════════════════════════════════ */
@media(max-width:420px) {
  .tab-btn { padding:6px 8px; font-size:0.68rem; }
  .tab-count { display:none; }
  .search-box { width:120px; }
  .kpi-grid { grid-template-columns:repeat(2,1fr); }
  .stat-grid { grid-template-columns:repeat(2,1fr); gap:8px; }
  .page-hero-title { font-size:1rem; }
  .qi-id { width:80px; }
}
</style>
</head>
<body>

<!-- ████ SIDEBAR ████ -->
<div class="sidebar-overlay" id="overlay" onclick="closeSidebar()"></div>
<aside class="sidebar" id="sidebar">
  <div class="sidebar-logo">
    <div class="logo-mark">D</div>
    <div class="logo-text">
      <div class="l1">Deloitte</div>
      <div class="l2">Tender Eligibility Engine</div>
    </div>
    <button class="sidebar-close" onclick="closeSidebar()">✕</button>
  </div>

  <div class="sidebar-section">
    <div class="sidebar-label">Navigation</div>
    <div class="nav-item active" id="sn-dashboard" onclick="gotoView('dashboard')">
      <span class="nav-icon">📊</span> Dashboard
    </div>
    <div class="nav-item" id="sn-tenders" onclick="gotoView('tenders')">
      <span class="nav-icon">📋</span> All Tenders
      <span class="nav-badge">{{ summary.total }}</span>
    </div>
  </div>

  <div class="sidebar-section" style="margin-top:6px;">
    <div class="sidebar-label">By Status</div>
    <div class="nav-item" id="sn-passed" onclick="gotoView('tenders');setFilter('PASSED')">
      <span class="nav-icon">✅</span> Passed
      <span class="nav-badge g">{{ summary.passed }}</span>
    </div>
    <div class="nav-item" id="sn-failed" onclick="gotoView('tenders');setFilter('FAILED')">
      <span class="nav-icon">❌</span> Failed
      <span class="nav-badge r">{{ summary.failed }}</span>
    </div>
    <div class="nav-item" id="sn-manual" onclick="gotoView('tenders');setFilter('MANUAL CHECK')">
      <span class="nav-icon">⚠️</span> Manual Check
      <span class="nav-badge a">{{ summary.manual }}</span>
    </div>
  </div>

  <div class="sidebar-section" style="margin-top:6px;">
    <div class="sidebar-label">Insights</div>
    <div class="nav-item" id="sn-analytics" onclick="gotoView('analytics')">
      <span class="nav-icon">📈</span> Analytics
    </div>
    <div class="nav-item" id="sn-profile" onclick="gotoView('profile')">
      <span class="nav-icon">🏢</span> Company Profile
    </div>
  </div>

  <div class="sidebar-footer">
    Pilot Engine v3.0 · <strong>Sep 2026</strong><br>
    Gujarat Skill Development Batch
  </div>
</aside>

<!-- ████ TOP BAR ████ -->
<header class="topbar">
  <button class="hamburger" onclick="openSidebar()">☰</button>
  <div>
    <div class="topbar-title">Gujarat Tender Engine</div>
    <div class="topbar-sub">Skill Development · Automated Screening</div>
  </div>
  <div class="topbar-right">
    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input class="search-box" type="text" placeholder="Search…" oninput="onSearch(this.value)" id="gSearch"/>
    </div>
    <span class="topbar-badge date-badge">📅 08 Sep 2026</span>
    <span class="topbar-badge pilot-badge">PILOT v3</span>
  </div>
</header>

<!-- ████ PAGE CONTENT ████ -->
<div class="page-content">

  <!-- ══ DASHBOARD ══ -->
  <div class="view active" id="view-dashboard">
    <div class="page-hero">
      <div class="page-hero-title">Eligibility <span>Results</span></div>
      <div class="page-hero-sub">
        {{ summary.total }} Gujarat Skill Development tenders screened ·
        {{ summary.passed }} passed · {{ summary.failed }} failed · {{ summary.manual }} manual review
      </div>
    </div>

    <div class="stat-grid">
      <div class="stat-card sc-total" onclick="gotoView('tenders');setFilter('all')">
        <span class="sc-icon">🗂️</span>
        <div class="sc-num">{{ summary.total }}</div>
        <div class="sc-lbl">Total Tenders</div>
        <div class="sc-pct">Current batch</div>
      </div>
      <div class="stat-card sc-pass" onclick="gotoView('tenders');setFilter('PASSED')">
        <span class="sc-icon">✅</span>
        <div class="sc-num">{{ summary.passed }}</div>
        <div class="sc-lbl">Passed</div>
        <div class="sc-pct">{{ (summary.passed/summary.total*100)|round(1) }}% eligible</div>
        <div class="sc-trend">Eligible</div>
      </div>
      <div class="stat-card sc-fail" onclick="gotoView('tenders');setFilter('FAILED')">
        <span class="sc-icon">❌</span>
        <div class="sc-num">{{ summary.failed }}</div>
        <div class="sc-lbl">Failed</div>
        <div class="sc-pct">{{ (summary.failed/summary.total*100)|round(1) }}% not eligible</div>
        <div class="sc-trend">Ineligible</div>
      </div>
      <div class="stat-card sc-manual" onclick="gotoView('tenders');setFilter('MANUAL CHECK')">
        <span class="sc-icon">⚠️</span>
        <div class="sc-num">{{ summary.manual }}</div>
        <div class="sc-lbl">Manual Review</div>
        <div class="sc-pct">{{ (summary.manual/summary.total*100)|round(1) }}% borderline</div>
        <div class="sc-trend">Review</div>
      </div>
    </div>

    <!-- Passed tenders quick list -->
    <div class="section-hdr">
      Passed Tenders
      <span class="section-link" onclick="gotoView('tenders');setFilter('PASSED')">View all →</span>
    </div>
    {% for r in results if r.status == 'PASSED' %}
    <div class="quick-item" onclick="gotoView('tenders');setFilter('PASSED')">
      <span class="qi-id">{{ r.tender_id }}</span>
      <span class="qi-title">{{ r.tender_title }}</span>
      <span class="qi-val" style="background:var(--pass-bg);color:var(--pass);border:1px solid var(--pass-border);">₹{{ r.value_lakhs }}L</span>
      <span class="qi-gates">{{ r.pass_count }}/{{ r.checks|length }} gates</span>
    </div>
    {% endfor %}

    {% if summary.manual > 0 %}
    <div class="section-hdr" style="margin-top:20px;">Manual Review Required</div>
    {% for r in results if r.status == 'MANUAL CHECK' %}
    <div class="quick-item" style="border-color:var(--manual-border);">
      <span class="qi-id">{{ r.tender_id }}</span>
      <span class="qi-title">{{ r.tender_title }}</span>
      <span class="qi-val" style="background:var(--manual-bg);color:var(--manual);border:1px solid var(--manual-border);">⚠️ {{ r.manual_count }} gates</span>
      <span class="qi-gates">₹{{ r.value_lakhs }}L</span>
    </div>
    {% endfor %}
    {% endif %}
  </div>

  <!-- ══ ALL TENDERS ══ -->
  <div class="view" id="view-tenders">
    <div class="page-hero">
      <div class="page-hero-title">All <span>Tenders</span></div>
      <div class="page-hero-sub">Gate-by-gate eligibility breakdown · {{ summary.total }} tenders this batch</div>
    </div>

    <div class="toolbar">
      <div class="tab-group">
        <button class="tab-btn t-all active" id="tb-all" onclick="setFilter('all')">
          All <span class="tab-count">{{ summary.total }}</span>
        </button>
        <button class="tab-btn t-pass" id="tb-PASSED" onclick="setFilter('PASSED')">
          ✅ <span class="tab-count">{{ summary.passed }}</span>
        </button>
        <button class="tab-btn t-fail" id="tb-FAILED" onclick="setFilter('FAILED')">
          ❌ <span class="tab-count">{{ summary.failed }}</span>
        </button>
        <button class="tab-btn t-manual" id="tb-MANUAL CHECK" onclick="setFilter('MANUAL CHECK')">
          ⚠️ <span class="tab-count">{{ summary.manual }}</span>
        </button>
      </div>
      <select class="sort-sel" onchange="sortTenders(this.value)">
        <option value="default">Sort: Default</option>
        <option value="value-desc">₹ High → Low</option>
        <option value="value-asc">₹ Low → High</option>
        <option value="deadline">Deadline: Soonest</option>
        <option value="score">Best Score</option>
      </select>
      <div class="result-count" id="rcount">Showing <strong>{{ summary.total }}</strong> tenders</div>
    </div>

    <div class="tender-list" id="tender-list">
      {% for r in results %}
      {% set cls = r.status.replace(' ','-') %}
      <div class="t-card status-{{ cls }}"
           data-status="{{ r.status }}"
           data-value="{{ r.value_lakhs }}"
           data-deadline="{{ r.deadline }}"
           data-score="{{ r.pass_count }}"
           data-search="{{ (r.tender_title+' '+r.department+' '+r.tender_id)|lower }}">

        <div class="t-header" onclick="toggleCard('{{ r.tender_id }}')">
          <div>
            <div class="t-id">{{ r.tender_id }}</div>
            <div class="t-title">{{ r.tender_title }}</div>
            <div class="t-dept">{{ r.department }}</div>
          </div>
          <span class="status-pill pill-{{ cls }}">
            {% if r.status=='PASSED' %}✅ PASS
            {% elif r.status=='FAILED' %}❌ FAIL
            {% else %}⚠️ REVIEW{% endif %}
          </span>
          <div class="chev-btn" id="chev-{{ r.tender_id }}">▼</div>
        </div>

        <div class="t-meta">
          <div class="t-meta-item">💰 <span class="v">₹{{ r.value_lakhs }}L</span></div>
          <div class="t-meta-item">📅 <span class="v">{{ r.deadline }}</span></div>
          <div class="t-meta-item">📍 <span class="v">{{ r.location }}</span></div>
          <div class="t-meta-item">⏱ <span class="v">{{ r.duration_days }}d</span></div>
          <div class="t-meta-item">
            {% if r.status=='PASSED' %}<span style="color:var(--pass)" class="v">All {{ r.checks|length }} gates ✓</span>
            {% elif r.status=='FAILED' %}<span class="v">{{ r.fail_count }} failed / {{ r.checks|length }}</span>
            {% else %}<span class="v">{{ r.manual_count }} review / {{ r.checks|length }}</span>{% endif %}
          </div>
        </div>

        <div class="score-wrap">
          {% set pct = (r.pass_count/r.checks|length*100)|int %}
          <div class="score-row">
            <span>Gate Score <strong>{{ r.pass_count }}/{{ r.checks|length }}</strong></span>
            <strong>{{ pct }}%</strong>
          </div>
          <div class="score-track">
            <div class="score-fill" style="width:{{ pct }}%;background:{% if r.status=='PASSED' %}var(--pass){% elif r.status=='FAILED' %}var(--fail){% else %}var(--manual){% endif %}"></div>
          </div>
        </div>

        <div class="t-body" id="body-{{ r.tender_id }}">
          <div class="scope-box"><strong>📋 Scope: </strong>{{ r.scope }}</div>
          <div class="gates-hdr">Eligibility Gate Analysis</div>
          <div class="gate-list">
            {% for c in r.checks %}
            <div class="gate-row {% if c.status=='pass' %}gp{% elif c.status=='fail' %}gf{% else %}gm{% endif %}">
              <div class="g-icon">{% if c.status=='pass' %}✅{% elif c.status=='fail' %}❌{% else %}⚠️{% endif %}</div>
              <div>
                <div class="g-crit">{{ c.criterion }}</div>
                <div class="g-reason">{{ c.reason }}</div>
                <div class="g-compare">
                  <span class="g-chip">Required: <strong>{{ c.required }}</strong></span>
                  <span class="g-chip">Company: <strong>{{ c.company }}</strong></span>
                </div>
              </div>
              <span class="g-badge">{% if c.status=='pass' %}PASS{% elif c.status=='fail' %}FAIL{% else %}REVIEW{% endif %}</span>
            </div>
            {% endfor %}
          </div>
          {% if r.fail_count > 0 %}
          <div class="reason-panel r-fail">
            <div class="r-title rt-fail">❌ Disqualification Reasons</div>
            {% for x in r.fail_reasons %}<div class="r-item">{{ x }}</div>{% endfor %}
          </div>
          {% endif %}
          {% if r.manual_count > 0 %}
          <div class="reason-panel r-manual" style="margin-top:7px;">
            <div class="r-title rt-manual">⚠️ Manual Review Items</div>
            {% for x in r.manual_reasons %}<div class="r-item">{{ x }}</div>{% endfor %}
          </div>
          {% endif %}
        </div>
      </div>
      {% endfor %}
    </div>
    <div class="empty-state" id="empty-state" style="display:none;">
      <div class="empty-icon">🔎</div>
      <div class="empty-text">No tenders match your filter.</div>
    </div>
  </div>

  <!-- ══ ANALYTICS ══ -->
  <div class="view" id="view-analytics">
    <div class="page-hero">
      <div class="page-hero-title">Eligibility <span>Analytics</span></div>
      <div class="page-hero-sub">Gate failure analysis and opportunity sizing across this batch</div>
    </div>
    <div class="analytics-grid">
      <div>
        <div class="a-card" style="margin-bottom:16px;">
          <div class="a-title">🔴 Gate Failure Frequency</div>
          <div class="bar-chart" id="gate-chart"></div>
        </div>
        <div class="a-card">
          <div class="a-title">💰 Tender Value by Status</div>
          <div style="overflow-x:auto;">
            <table class="val-table">
              <thead><tr><th>Tender</th><th>Value</th><th>Status</th><th>Score</th></tr></thead>
              <tbody>
                {% for r in results|sort(attribute='value_lakhs',reverse=True) %}
                <tr>
                  <td>{{ r.tender_id }}</td>
                  <td><strong style="color:var(--text)">₹{{ r.value_lakhs }}L</strong></td>
                  <td>
                    {% if r.status=='PASSED' %}<span class="tp">✅ Passed</span>
                    {% elif r.status=='FAILED' %}<span class="tf">❌ Failed</span>
                    {% else %}<span class="tm">⚠️ Manual</span>{% endif %}
                  </td>
                  <td>
                    <div style="display:flex;align-items:center;gap:6px;">
                      <div style="width:44px;background:var(--surface);border-radius:3px;height:4px;overflow:hidden;">
                        <div style="height:100%;border-radius:3px;width:{{ (r.pass_count/r.checks|length*100)|int }}%;background:{% if r.status=='PASSED' %}var(--pass){% elif r.status=='FAILED' %}var(--fail){% else %}var(--manual){% endif %}"></div>
                      </div>
                      <span style="font-size:0.67rem;color:var(--muted2);">{{ r.pass_count }}/{{ r.checks|length }}</span>
                    </div>
                  </td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div>
        <div class="a-card" style="margin-bottom:16px;">
          <div class="a-title">📊 Status Breakdown</div>
          <div class="ring-wrap">
            <div class="ring-item">
              <div class="ring-dot" style="background:var(--pass)"></div>
              <div class="ring-name">Passed</div>
              <div class="ring-bg"><div class="ring-fill" style="width:{{ (summary.passed/summary.total*100)|int }}%;background:var(--pass)"></div></div>
              <div class="ring-pct" style="color:var(--pass)">{{ (summary.passed/summary.total*100)|round(1) }}%</div>
            </div>
            <div class="ring-item">
              <div class="ring-dot" style="background:var(--fail)"></div>
              <div class="ring-name">Failed</div>
              <div class="ring-bg"><div class="ring-fill" style="width:{{ (summary.failed/summary.total*100)|int }}%;background:var(--fail)"></div></div>
              <div class="ring-pct" style="color:var(--fail)">{{ (summary.failed/summary.total*100)|round(1) }}%</div>
            </div>
            <div class="ring-item">
              <div class="ring-dot" style="background:var(--manual)"></div>
              <div class="ring-name">Manual</div>
              <div class="ring-bg"><div class="ring-fill" style="width:{{ (summary.manual/summary.total*100)|int }}%;background:var(--manual)"></div></div>
              <div class="ring-pct" style="color:var(--manual)">{{ (summary.manual/summary.total*100)|round(1) }}%</div>
            </div>
          </div>
        </div>

        <div class="a-card" style="margin-bottom:16px;">
          <div class="a-title">💎 Eligible Opportunity</div>
          {% set ev = namespace(v=0) %}{% set tv = namespace(v=0) %}
          {% for r in results %}{% set tv.v = tv.v + r.value_lakhs %}{% endfor %}
          {% for r in results if r.status in ['PASSED','MANUAL CHECK'] %}{% set ev.v = ev.v + r.value_lakhs %}{% endfor %}
          <div class="opp-card">
            <div class="opp-val">₹{{ ev.v|round(1) }}L</div>
            <div class="opp-sub">Eligible + Review tender value</div>
            <div class="opp-of">of ₹{{ tv.v|round(1) }}L total batch</div>
            <div style="margin-top:12px;">
              <div class="score-track"><div class="score-fill" style="width:{{ (ev.v/tv.v*100)|int }}%;background:var(--deloitte)"></div></div>
              <div class="score-row" style="margin-top:4px;">
                <span>Eligible share</span>
                <strong style="color:var(--deloitte)">{{ (ev.v/tv.v*100)|round(1) }}%</strong>
              </div>
            </div>
          </div>
        </div>

        <div class="a-card">
          <div class="a-title">📍 Geographic Split</div>
          <div class="ring-wrap">
            {% set gp=namespace(v=0)%}{% set gf=namespace(v=0)%}{% set pi=namespace(v=0)%}
            {% for r in results %}
              {% if 'Pan' in r.location %}{% set pi.v=pi.v+1 %}
              {% elif r.status=='PASSED' %}{% set gp.v=gp.v+1 %}
              {% else %}{% set gf.v=gf.v+1 %}{% endif %}
            {% endfor %}
            <div class="ring-item">
              <div class="ring-dot" style="background:var(--pass)"></div>
              <div class="ring-name">Gujarat Eligible</div>
              <div class="ring-bg"><div class="ring-fill" style="width:{{ (gp.v/summary.total*100)|int }}%;background:var(--pass)"></div></div>
              <div class="ring-pct" style="color:var(--pass)">{{ gp.v }}</div>
            </div>
            <div class="ring-item">
              <div class="ring-dot" style="background:var(--fail)"></div>
              <div class="ring-name">Gujarat Not Eligible</div>
              <div class="ring-bg"><div class="ring-fill" style="width:{{ (gf.v/summary.total*100)|int }}%;background:var(--fail)"></div></div>
              <div class="ring-pct" style="color:var(--fail)">{{ gf.v }}</div>
            </div>
            <div class="ring-item">
              <div class="ring-dot" style="background:var(--manual)"></div>
              <div class="ring-name">Pan-India Scope</div>
              <div class="ring-bg"><div class="ring-fill" style="width:{{ (pi.v/summary.total*100)|int }}%;background:var(--manual)"></div></div>
              <div class="ring-pct" style="color:var(--manual)">{{ pi.v }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ══ COMPANY PROFILE ══ -->
  <div class="view" id="view-profile">
    <div class="page-hero">
      <div class="page-hero-title">Company <span>Profile</span></div>
      <div class="page-hero-sub">Eligibility gate configuration used for all tender screening</div>
    </div>

    <div class="profile-hero">
      <div class="co-logo">🏢</div>
      <div>
        <div class="co-name">{{ company.name }}</div>
        <div class="co-tag">Est. {{ company.established_year }} · Gujarat Operations · Skill Development</div>
        <div class="cert-wrap">
          {% for c in company.certifications %}<span class="cert-chip">✓ {{ c }}</span>{% endfor %}
        </div>
      </div>
    </div>

    <div class="kpi-grid" style="margin-bottom:18px;">
      <div class="kpi"><div class="kpi-val">₹{{ company.annual_turnover_crores }}Cr</div><div class="kpi-lbl">Turnover</div></div>
      <div class="kpi"><div class="kpi-val">{{ company.years_of_experience }}Y</div><div class="kpi-lbl">Experience</div></div>
      <div class="kpi"><div class="kpi-val">{{ company.daily_training_capacity }}</div><div class="kpi-lbl">Seats/Day</div></div>
      <div class="kpi"><div class="kpi-val">{{ company.similar_projects_completed }}</div><div class="kpi-lbl">Projects</div></div>
      <div class="kpi"><div class="kpi-val">{{ company.certifications|length }}</div><div class="kpi-lbl">Certs</div></div>
    </div>

    <div class="profile-grid">
      <div class="p-card">
        <div class="p-title">Gate Thresholds</div>
        <div class="p-row"><span>💰 Turnover</span><strong>₹{{ company.annual_turnover_crores }}Cr</strong></div>
        <div class="p-row"><span>📅 Experience</span><strong>{{ company.years_of_experience }} Years</strong></div>
        <div class="p-row"><span>🏗️ Capacity</span><strong>{{ company.daily_training_capacity }} / Day</strong></div>
        <div class="p-row"><span>📁 Projects</span><strong>{{ company.similar_projects_completed }} Done</strong></div>
        <div class="p-row"><span>📍 Geography</span><strong>{{ company.geographic_presence|join(', ') }}</strong></div>
      </div>
      <div class="p-card">
        <div class="p-title">Screening Summary</div>
        <div class="result-box rb-pass"><span>✅ Passed</span><span class="rb-num">{{ summary.passed }}</span></div>
        <div class="result-box rb-fail"><span>❌ Failed</span><span class="rb-num">{{ summary.failed }}</span></div>
        <div class="result-box rb-manual"><span>⚠️ Manual Review</span><span class="rb-num">{{ summary.manual }}</span></div>
      </div>
    </div>
  </div>

</div><!-- end page-content -->

<!-- ████ BOTTOM NAV (Mobile) ████ -->
<nav class="bottom-nav" id="bottomnav">
  <div class="bn-item active" id="bn-dashboard" onclick="gotoView('dashboard')">
    <div class="bn-icon-wrap"><span class="bn-icon">📊</span></div>
    <span class="bn-label">Dashboard</span>
  </div>
  <div class="bn-item" id="bn-tenders" onclick="gotoView('tenders')">
    <div class="bn-icon-wrap">
      <span class="bn-icon">📋</span>
      <span class="bn-badge" style="background:var(--accent)">{{ summary.total }}</span>
    </div>
    <span class="bn-label">Tenders</span>
  </div>
  <div class="bn-item" id="bn-analytics" onclick="gotoView('analytics')">
    <div class="bn-icon-wrap"><span class="bn-icon">📈</span></div>
    <span class="bn-label">Analytics</span>
  </div>
  <div class="bn-item" id="bn-profile" onclick="gotoView('profile')">
    <div class="bn-icon-wrap"><span class="bn-icon">🏢</span></div>
    <span class="bn-label">Profile</span>
  </div>
</nav>

<script>
const ALL_RESULTS = {{ results | tojson }};
const SUMMARY     = {{ summary | tojson }};

/* ── Sidebar ── */
function openSidebar()  { document.getElementById('sidebar').classList.add('open'); document.getElementById('overlay').classList.add('show'); }
function closeSidebar() { document.getElementById('sidebar').classList.remove('open'); document.getElementById('overlay').classList.remove('show'); }

/* ── View Navigation ── */
function gotoView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById('view-' + name).classList.add('active');
  // Sidebar nav
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const sn = document.getElementById('sn-' + name);
  if (sn) sn.classList.add('active');
  // Bottom nav
  document.querySelectorAll('.bn-item').forEach(b => b.classList.remove('active'));
  const bn = document.getElementById('bn-' + name);
  if (bn) bn.classList.add('active');
  closeSidebar();
  window.scrollTo(0, 0);
  if (name === 'analytics') setTimeout(buildGateChart, 80);
}

/* ── Filter ── */
let currentFilter = 'all';
let currentSearch = '';
let currentSort   = 'default';

function setFilter(status) {
  currentFilter = status;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  const key = status === 'all' ? 'tb-all' : 'tb-' + status;
  const btn = document.getElementById(key);
  if (btn) btn.classList.add('active');
  renderList();
}

function onSearch(val) {
  currentSearch = val.toLowerCase().trim();
  if (currentSearch) { gotoView('tenders'); setFilter('all'); }
  renderList();
}

function sortTenders(val) {
  currentSort = val;
  renderList();
}

function renderList() {
  const list  = document.getElementById('tender-list');
  if (!list) return;
  const cards = Array.from(list.children);
  let visible = 0;

  // Sort
  const sorted = [...cards].sort((a, b) => {
    if (currentSort === 'value-desc') return parseFloat(b.dataset.value) - parseFloat(a.dataset.value);
    if (currentSort === 'value-asc')  return parseFloat(a.dataset.value) - parseFloat(b.dataset.value);
    if (currentSort === 'deadline')   return a.dataset.deadline.localeCompare(b.dataset.deadline);
    if (currentSort === 'score')      return parseInt(b.dataset.score) - parseInt(a.dataset.score);
    return 0;
  });
  sorted.forEach(c => list.appendChild(c));

  cards.forEach(card => {
    const sm = currentFilter === 'all' || card.dataset.status === currentFilter;
    const qm = !currentSearch || card.dataset.search.includes(currentSearch);
    if (sm && qm) { card.style.display = ''; visible++; }
    else card.style.display = 'none';
  });

  document.getElementById('empty-state').style.display = visible === 0 ? '' : 'none';
  const rc = document.getElementById('rcount');
  if (rc) rc.innerHTML = `Showing <strong>${visible}</strong> of <strong>${SUMMARY.total}</strong>`;
}

/* ── Toggle Card ── */
function toggleCard(id) {
  const body = document.getElementById('body-' + id);
  const chev = document.getElementById('chev-' + id);
  const isOpen = body.classList.contains('open');
  body.classList.toggle('open');
  if (chev) { chev.classList.toggle('open'); chev.textContent = isOpen ? '▼' : '▲'; }
}

/* ── Gate Bar Chart ── */
function buildGateChart() {
  const gates = {};
  ALL_RESULTS.forEach(r => {
    r.checks.forEach(c => {
      if (!gates[c.criterion]) gates[c.criterion] = { fail:0, pass:0, manual:0 };
      gates[c.criterion][c.status]++;
    });
  });
  const chart = document.getElementById('gate-chart');
  if (!chart) return;
  const total = ALL_RESULTS.length;
  const sorted = Object.entries(gates).sort((a,b) => b[1].fail - a[1].fail);
  chart.innerHTML = sorted.map(([name, counts]) => {
    const passPct = Math.round(counts.pass / total * 100);
    const failPct = Math.round(counts.fail / total * 100);
    return `
      <div class="bar-row">
        <div class="bar-lbl" title="${name}">${name}</div>
        <div class="bar-track">
          <div class="bar-fill" style="width:${passPct}%;background:var(--pass);"></div>
          <div class="bar-fill" style="width:${failPct}%;background:var(--fail);"></div>
        </div>
        <div class="bar-val">${counts.fail} fail</div>
      </div>`;
  }).join('');
}

/* ── Score bar animation ── */
function animateBars() {
  document.querySelectorAll('.score-fill').forEach(b => {
    const w = b.style.width; b.style.width='0';
    requestAnimationFrame(() => setTimeout(() => { b.style.width = w; }, 120));
  });
}

/* ── Init ── */
document.addEventListener('DOMContentLoaded', () => {
  animateBars();
  document.getElementById('sn-dashboard').classList.add('active');
});
</script>
</body>
</html>
"""


@app.route("/")
def index():
    results, summary = run_engine()
    return render_template_string(HTML, results=results, summary=summary, company=COMPANY_PROFILE)


@app.route("/api/results")
def api_results():
    results, summary = run_engine()
    return jsonify({"summary": summary, "results": results})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "="*60)
    print("  Deloitte Gujarat Tender Eligibility Engine v3.0")
    print(f"  Running at -> http://127.0.0.1:{port}")
    print("  Fully responsive - works on all devices!")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False)
