# theme.py

MAP_H   = "45vh"
KPI_H   = "34vh"
CHART_H = "30vh"   

COLOR_MAP = {
    "Hotspot": "#ef4444",
    "Normal": "#60a5fa",
    "Off-Season": "#f59e0b",
}
CATEGORY_ORDER = {"lift": ["Hotspot", "Normal", "Off-Season"]}

MAP_BG = "#223542"
CORAL  = "#F88379"
BUBBLE = "#2aa7d6"

INDEX_STRING = f"""
<!DOCTYPE html>
<html>
  <head>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">

    {{%metas%}}
    <title>{{%title%}}</title>
    {{%favicon%}}
    {{%css%}}
    <style>
    :root{{
        --bg1:#050716;
        --bg2:#060818;
        --card:#020617;
        --card2:#020617;
        --border:rgba(148,163,253,.55);
        --glow:rgba(56,189,248,.18);
        --text:#f7f7ff;
        --muted:#9fb3d9;
        --grid:rgba(234,242,246,.06);
        --accent:#a855f7;
    }}

    *{{ box-sizing:border-box; }}

    body, html{{
        height:100%;
        margin:0;
        padding:0;
        overflow:hidden;
        background:
            radial-gradient(900px 500px at 15% 0%, rgba(94,234,212,.10), transparent 65%),
            radial-gradient(900px 600px at 85% 0%, rgba(129,140,248,.12), transparent 65%),
            linear-gradient(160deg, var(--bg1), var(--bg2));
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color:var(--text);
    }}

    .layout-root{{
        display:flex;
        height:100vh;
        width:100vw;
    }}

    /* =========================
       SIDEBAR
       ========================= */
    .sidebar {{
        width:230px;
        height:100vh;
        background:linear-gradient(180deg,#050814,#050812);
        padding:24px 18px 18px;
        border-right:1px solid rgba(255,255,255,.06);
        display:flex;
        flex-direction:column;
        gap:22px;
    }}

    .sidebar-logo{{
        font-weight:800;
        font-size:22px;
        letter-spacing:.18em;
        text-transform:uppercase;
        color:#e5e7ff;
    }}

    .sidebar-subtitle{{
        font-size:13px;
        color:var(--muted);
        line-height:1.4;
    }}

    .sidebar-nav .nav-link{{
        border-radius:12px;
        margin-bottom:8px;
        padding:9px 11px;
        font-size:14px;
        color:#c7d2fe;
        display:flex;
        align-items:center;
        gap:8px;
        border:1px solid transparent;
        transition:.2s;
    }}

    .sidebar-nav .nav-link .dot{{
        width:7px;
        height:7px;
        border-radius:999px;
        background:rgba(148,163,184,.65);
    }}

    .sidebar-nav .nav-link:hover{{
        background:rgba(148,163,253,.12);
        border-color:rgba(148,163,253,.28);
    }}

    .sidebar-nav .nav-link.active{{
        background:linear-gradient(135deg,#6366f1,#a855f7);
        color:white;
        border-color:transparent;
        box-shadow:0 0 18px rgba(129,140,248,.55);
    }}

    .sidebar-nav .nav-link.active .dot{{ background:white; }}

    .sidebar-footer{{
        margin-top:auto;
        font-size:11px;
        color:var(--muted);
        opacity:.8;
    }}

    /* =========================
       MAIN CONTENT
       ========================= */
    .content-wrapper{{
        flex:1;
        padding:18px 22px 14px;
        overflow:hidden;
        display:flex;
        flex-direction:column;
    }}

    .page-body{{
        height:100%;
        display:flex;
        flex-direction:column;
        gap:16px;
    }}

    /* =========================
       HEADER 
       ========================= */
    .hero-card,
    .header-card{{
        background:
            radial-gradient(circle at 10% 0%, rgba(139,92,246,0.23), transparent 60%),
            radial-gradient(circle at 90% 0%, rgba(45,212,191,0.20), transparent 60%),
            linear-gradient(120deg,#141a2f 0%, #050716 50%, #04141f 100%);
        border-radius:22px;
        padding:10px 22px 12px;
        border:1px solid rgba(125,211,252,.75);
        box-shadow:0 0 22px rgba(56,189,248,.22);
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:18px;
        min-height:68px;     
    }}

    .page-title{{
        font-family:"Playfair Display", "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        font-size:24px;
        font-weight:700;
        letter-spacing:.16em;
        text-transform:uppercase;
        color:#ffffff;
    }}

    .page-subtitle{{
        font-size:13px;
        color:var(--muted);
        margin-top:4px;
        margin-bottom:2px;   
        max-width:520px;
    }}

    .badge-chip{{
        font-size:12px;
        padding:5px 14px;
        border-radius:999px;
        background:#020617;
        border:1px solid rgba(148,163,253,.65);
        display:inline-flex;
        align-items:center;
        gap:6px;
        box-shadow:0 0 16px rgba(56,189,248,.35);
    }}

    .badge-dot{{
        width:7px;
        height:7px;
        border-radius:999px;
        background:#22c55e;
        box-shadow:0 0 12px rgba(34,197,94,.8);
    }}

    /* =========================
       GENERIC SOFT CARD
       ========================= */
    .soft-card{{
        background:#020617;
        border-radius:18px;
        border:1px solid var(--border);
        box-shadow:
            0 0 18px var(--glow),
            inset 0 1px 0 rgba(255,255,255,.04);
        padding:12px 14px;
    }}

    /* =========================
       FILTERS STRIP
       ========================= */
    .filters-card{{ 
        display:flex; 
        flex-direction:column; 
        gap:8px; 
        margin-top:4px; 
    }}

    .filters-title{{ 
        font-size:12px; 
        text-transform:uppercase; 
        letter-spacing:.18em; 
        color:#ffffff; 
    }}

    .filters-row{{ 
        display:grid; 
        grid-template-columns:repeat(5, minmax(0, 1fr)); 
        gap:12px; 
    }}

    .filter-label{{ 
        font-size:11px; 
        color:#ffffff; 
        margin-bottom:4px; 
        letter-spacing:.04em; 
        text-transform:uppercase; 
    }}

    .dash-dropdown .Select-control{{
        background:rgba(5,10,24,.98) !important;
        border:1px solid var(--border) !important;
        border-radius:11px !important;
        min-height:34px;
        font-size:13px;
        color:#ffffff !important;
    }}
    .dash-dropdown .Select-value-label{{ color:#ffffff !important; }}
    .dash-dropdown .Select-placeholder{{ color:#e5e7ff !important; }}
    .dash-dropdown .Select-menu-outer{{
        background:rgba(5,10,24,.98) !important;
        border:1px solid rgba(148,163,253,.35) !important;
        color:#ffffff !important;
        z-index:9999;
    }}
    .dash-dropdown .Select-option{{ color:#ffffff !important; }}

    /* =========================
       DASHBOARD LAYOUT
       ========================= */
    .main-row{{
        display:grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(0, 1.8fr);
        gap:20px;
        min-height:0;
        align-items:stretch;
    }}

    .map-card{{ height:{MAP_H}; }}
    .map-side-wrapper{{ display:flex; flex-direction:column; gap:10px; height:100%; }}

    .kpi-panel{{ display:flex; flex-direction:column; }}

    .kpi-row{{
        display:grid;
        grid-template-columns:repeat(2, minmax(0, 1fr));
        gap:10px;
        margin-top:4px;
    }}

    .kpi-title{{
        font-size:11px;
        color:#ffffff;
        text-transform:uppercase;
        letter-spacing:.11em;
        margin-bottom:3px;
    }}

    .kpi-value{{ 
        font-size:20px; 
        font-weight:600; 
        line-height:1.3; 
        color:#ffffff; 
    }}

    .kpi-card-inner{{
        padding:8px 10px;
        border-radius:14px;
        background:linear-gradient(180deg,#0b1120,#050b15);
        border:1px solid var(--border);
        box-shadow:0 0 20px var(--glow), inset 0 1px 0 rgba(255,255,255,.04);
    }}

    /* =========================
       ANALYTICS CHART GRID
       ========================= */
    .charts-grid{{ 
        display:grid; 
        grid-template-columns: repeat(3, minmax(0, 1fr)); 
        gap:14px; 
        min-height:0; 
    }}

    .chart-card{{ 
        height:{CHART_H}; 
        display:flex; 
        flex-direction:column; 
    }}

    .chart-title{{ 
        font-size:11px; 
        color:#ffffff; 
        text-transform:uppercase; 
        letter-spacing:.11em; 
        margin-bottom:4px; 
    }}

    /* =========================
       STORYLINE
       ========================= */
    .storyline-text{{ 
        font-size:13px; 
        color:#ffffff; 
        margin-top:4px; 
    }}
    .storyline-text div::before{{ 
        content: "🔹 "; 
    }}

    .storyline-box{{
        border-top:1px solid rgba(148,163,253,0.25);
        margin-top:6px;
        padding-top:8px;
        max-height:12vh;
        overflow-y:auto;
    }}

    /* =========================
       RECOMMENDATIONS PAGE
       ========================= */
    .reco-page-body{{
        display:flex;
        flex-direction:column;
        gap:10px;          
        padding-top:4px;   
    }}

    .reco-section-title{{
        font-size:13px;
        letter-spacing:.16em;
        text-transform:uppercase;
        color:var(--muted);
        margin-top:2px;    
        margin-bottom:4px; 
    }}

    /* 2x2 seasons grid */
    .season-grid{{
        display:grid;
        grid-template-columns:repeat(2,minmax(0,1fr));
        column-gap:12px;
        row-gap:10px;
    }}

    .season-card{{
        padding:12px 16px;   
        border-radius:18px;
        border:1px solid var(--border);
        box-shadow:
            0 0 18px var(--glow),
            inset 0 1px 0 rgba(255,255,255,.04);
        background:#020617;
    }}

    .season-header{{
        display:flex;
        align-items:center;
        gap:8px;
        margin-bottom:4px;
    }}

    .season-icon{{ font-size:18px; }}
    .season-name{{ 
        font-size:16px; 
        font-weight:600; 
        color:#ffffff;     /* brighter titles: Spring / Summer / Fall / Winter */
    }}

    .season-months{{
        font-size:12px;
        color:var(--muted);
        margin-bottom:8px;
    }}

    .season-section-title{{
        font-size:12px;
        text-transform:uppercase;
        letter-spacing:.14em;
        color:var(--muted);
        margin-top:4px;
        margin-bottom:2px;
    }}

    .season-list{{
        margin:0;
        padding-left:16px;
        font-size:13px;
        color:var(--text);
    }}

    .mini-reco-row{{
        display:grid;
        grid-template-columns:repeat(2,minmax(0,1fr));
        column-gap:12px;
        row-gap:10px;
    }}

    .mini-reco-card{{ 
        padding:12px 14px;  
    }}

    .reco-subtitle{{
        font-size:14px;
        font-weight:600;
        margin-bottom:6px;
    }}

    /* =========================
       PLOTLY FONT OVERRIDE
       ========================= */
    .js-plotly-plot .plotly, .main-svg{{
        font-family:"Inter", system-ui, sans-serif !important;
    }}
    </style>
  </head>
  <body>
    {{%app_entry%}}
    <footer>
      {{%config%}}
      {{%scripts%}}
      {{%renderer%}}
    </footer>
  </body>
</html>
"""