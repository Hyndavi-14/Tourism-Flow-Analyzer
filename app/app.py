import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


#  APP & THEME

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
app.title = "Tourist Flow & Seasonality Analyzer"

# Equal vertical spacing setup
MAP_H = "45vh"       # Map + filters balanced height
KPI_H = "13vh"       # KPI row height
COLUMN_H = "61vh"    # Adjusted column container height
TITLE_TOP = "14px"
ROW_GAP = "20px"     # Equal gaps between vertical sections


COLOR_MAP = {"Normal": "#60a5fa", "Hotspot": "#ef4444", "Off-Season": "#f59e0b"}
CATEGORY_ORDER = {"lift": ["Normal", "Hotspot", "Off-Season"]}
MAP_BG = "#223542"
CORAL = "#F88379"  # Event Impact bar color


#  PAGE SHELL / CSS

app.index_string = """
<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
      :root{
        --bg1:#0e2b34; --bg2:#233b45;
        --panel:#263d49; --panel-2:#223542;
        --border:rgba(255,255,255,.12);
        --shadow-dark:rgba(6,14,18,.65);
        --shadow-light:rgba(255,255,255,.07);
        --glow:rgba(56,189,248,.18);
        --text:#ffffff; --muted:#cfe1ea;
        --grid:rgba(234,242,246,.045);
      }

      @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600;700&display=swap');

      html, body{
        height:100%; margin:0; overflow:hidden;
        background:
          radial-gradient(1100px 540px at 18% 8%, rgba(108,209,255,.08), transparent 60%),
          radial-gradient(900px 420px at 85% 0%, rgba(108,209,255,.06), transparent 55%),
          linear-gradient(135deg, var(--bg1), var(--bg2));
        color:var(--text);
        font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif;
      }

      .dbc-container{
        background:linear-gradient(180deg, rgba(255,255,255,.02), rgba(0,0,0,.03));
        border-radius:22px;
        box-shadow:
          24px 24px 44px var(--shadow-dark),
          -10px -10px 18px var(--shadow-light),
          inset 0 1px 0 rgba(255,255,255,.06),
          0 0 22px var(--glow);
        padding:10px 12px 12px 12px;
      }

      .soft-card{
        border-radius:18px;
        background:linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
        border:1px solid var(--border);
        box-shadow:
          16px 18px 30px var(--shadow-dark),
          -8px -8px 16px var(--shadow-light),
          inset 0 1px 0 rgba(255,255,255,.04),
          0 0 14px var(--glow);
      }
      .tight{ padding:12px 14px; }

      .map-card{
        background:
          radial-gradient(900px 420px at 50% 28%, #2c4654 0%, var(--panel-2) 70%),
          linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
        box-shadow:
          inset 0 1px 0 rgba(255,255,255,.06),
          16px 18px 30px var(--shadow-dark),
          -8px -8px 16px var(--shadow-light),
          0 0 14px var(--glow);
      }

      .section-title{
        width:100%;
        font-family:"Playfair Display", serif;
        font-size:36px; font-weight:700; letter-spacing:.4px;
        text-align:center;
        background: linear-gradient(180deg,#ffffff,#cfe9ff);
        -webkit-background-clip:text; background-clip:text;
        color:transparent;
        text-shadow:0 2px 3px rgba(0,0,0,.35);
        margin:0;
        transform: translateY(-8px);
      }

      .kpi-title{font-size:12px; color:#ffffff; margin-bottom:6px;}
      .kpi-value{font-weight:700; font-size:22px; margin:0; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
      .kpi-row{display:flex; gap:12px; width:100%;}
      .kpi-col{flex:1 1 0; max-width:none; display:flex;}
      .kpi-col>.card{width:100%;}

      .dash-dropdown .Select-control, .Select-control{
        background:linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%) !important;
        border:1px solid var(--border) !important;
        border-radius:10px !important;
        box-shadow:inset 0 1px 0 rgba(255,255,255,.04) !important;
        color:#ffffff !important;
      }
      .dash-dropdown .Select-value-label,
      .dash-dropdown .Select-placeholder,
      .dash-dropdown .Select-input > input,
      .Select-value-label, .Select-placeholder, .Select-input > input{
        color:#ffffff !important;
      }
      .dash-dropdown .Select-menu-outer, .Select-menu-outer{
        background:var(--panel) !important; border:1px solid var(--border) !important;
      }
      .dash-dropdown .Select-menu-outer .Select-option,
      .Select-menu-outer .Select-option,
      .VirtualizedSelectOption,
      .Select-option{
        color:#ffffff !important; background:transparent !important;
      }
      .dash-dropdown .Select-menu-outer .Select-option.is-focused,
      .Select-menu-outer .Select-option.is-focused,
      .VirtualizedSelectFocusedOption{
        background:rgba(255,255,255,.12) !important; color:#ffffff !important;
      }
      .dash-dropdown .Select-arrow, .dash-dropdown .Select-clear-zone,
      .Select-arrow, .Select-clear-zone{ color:#ffffff !important; fill:#ffffff !important; }

      .js-plotly-plot .plotly, .main-svg{
        font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, sans-serif !important;
      }
    </style>
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
  </body>
</html>
"""


#  DATA

np.random.seed(7)
state_codes = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY",
               "LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND",
               "OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"]
state_names = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware",
               "Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky",
               "Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi",
               "Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico",
               "New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
               "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont",
               "Virginia","Washington","West Virginia","Wisconsin","Wyoming","District of Columbia"]

df_map = pd.DataFrame({
    "state": state_codes,
    "state_name": state_names,
    "lift": np.random.choice(["Hotspot","Normal","Off-Season"], len(state_codes), p=[0.35,0.45,0.20])
})
kpi_baseline = {"total_visitors": 4_200_000, "avg_spend": 85}

df_month = pd.DataFrame({
    "month": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    "visits": np.round(np.linspace(0.9, 1.6, 12) * 1_000_000, 0)
})

df_heat = (pd.DataFrame(np.random.randint(30, 95, size=(4,4)),
                        index=["Spring","Summer","Fall","Winter"],
                        columns=["Spring","Summer","Fall","Winter"])
           .reset_index().melt(id_vars="index", var_name="Season", value_name="Score")
           .rename(columns={"index":"Season_Row"}))

evt = pd.DataFrame({
    "event":["Mardi Gras","Coachella","Art Basel","SXSW","Thanksgiving"],
    "region":["Louisiana","California","Florida","Texas","Nationwide"],
    "spike":[25,40,40,18,12],
})

REGIONS = {
    "East Coast": ["ME","NH","MA","RI","CT","NY","NJ","PA","DE","MD","DC","VA","NC","SC","GA","FL"],
    "West": ["CA","OR","WA","AK","HI"],
    "South": ["TX","OK","AR","LA","MS","AL","TN","KY","GA","FL","SC","NC","VA","WV","MD","DC","DE"],
    "Mountain": ["AZ","NM","CO","UT","NV","ID","MT","WY"]
}
ALL_MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
YEARS = list(range(2010, 2025))


#  FIGURE BUILDERS

def _common_layout(fig):
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff")
    )
    fig.update_xaxes(gridcolor="var(--grid)", zeroline=False, showline=False)
    fig.update_yaxes(gridcolor="var(--grid)", zeroline=False, showline=False)
    return fig

def build_map(df):
    fig = px.choropleth(
        df, locations="state", locationmode="USA-states", color="lift",
        custom_data=["lift","state_name"], color_discrete_map=COLOR_MAP,
        category_orders=CATEGORY_ORDER, scope="usa",
        hover_name="state_name",
        hover_data={"state": False, "state_name": False, "lift": True},
        labels={"lift": "Status"},
    )
    fig.update_layout(
        paper_bgcolor=MAP_BG,
        plot_bgcolor=MAP_BG,
        geo=dict(bgcolor=MAP_BG, lakecolor=MAP_BG, showlakes=False, showland=True, landcolor=MAP_BG),
        legend=dict(title="Status", orientation="v", y=0.98, yanchor="top", x=0.98, xanchor="right",
                    bgcolor="rgba(0,0,0,0)", font=dict(color="#ffffff")),
        margin=dict(l=0, r=0, t=0, b=0),
        hoverlabel=dict(bgcolor="rgba(10,20,25,.9)", font_color="#ffffff")
    )
    fig.update_traces(hovertemplate="<b>%{customdata[1]}</b><br>Status: %{customdata[0]}<extra></extra>")
    return fig

def build_heatmap(dfh):
    fig = px.density_heatmap(dfh, x="Season", y="Season_Row", z="Score", text_auto=True, color_continuous_scale="Blues")
    fig = _common_layout(fig)
    fig.update_xaxes(title="")
    fig.update_yaxes(title="")
    fig.update_layout(coloraxis_showscale=True,
                      coloraxis_colorbar=dict(title="Score", tickfont=dict(color="#ffffff"), titlefont=dict(color="#ffffff")))
    return fig

def build_trend(dfl):
    fig = px.line(dfl, x="month", y="visits", markers=True)
    fig = _common_layout(fig)
    fig.update_xaxes(title="", showgrid=False)
    fig.update_yaxes(title="Tourist inflows", showgrid=False)
    return fig

def build_events(e):
    # Coral-peach bars with guaranteed outside labels using a separate text trace
    e = e.sort_values("spike")
    xmax = float(e["spike"].max())
    pad = xmax * 0.08  # how far to move labels beyond the bar end

    # Base horizontal bars (no text on the bar trace)
    bar = go.Bar(
        x=e["spike"], y=e["event"], orientation="h",
        marker=dict(color=CORAL),
        hovertemplate="<b>%{y}</b><br>Spike: %{x}%<extra></extra>",
        cliponaxis=False, showlegend=False
    )

    # Rounded ends by adding circles at both ends
    left_cap = go.Scatter(
        x=[0]*len(e), y=e["event"], mode="markers",
        marker=dict(color=CORAL, size=18),
        hoverinfo="skip", showlegend=False
    )
    right_cap = go.Scatter(
        x=e["spike"], y=e["event"], mode="markers",
        marker=dict(color=CORAL, size=18),
        hoverinfo="skip", showlegend=False
    )

    # OUTSIDE percentage labels (separate text trace)
    labels = go.Scatter(
        x=e["spike"] + pad, y=e["event"], mode="text",
        text=[f"{v}%" for v in e["spike"]],
        textfont=dict(color="#ffffff"),
        textposition="middle left",
        hoverinfo="skip", showlegend=False,
        cliponaxis=False
    )

    fig = go.Figure([bar, left_cap, right_cap, labels])
    fig = _common_layout(fig)
    fig.update_xaxes(title="Spike", showgrid=False, range=[0, xmax + pad*2.2])
    fig.update_yaxes(title="", showgrid=False)
    fig.update_layout(hoverlabel=dict(bgcolor="rgba(10,20,25,.9)", font_color="#ffffff"))
    return fig


#  COMPONENTS

sidebar_filters = dbc.Card(
    [
        html.Div("Filters", className="kpi-title mb-2"),
        html.Div("Month", className="kpi-title"),
        dcc.Dropdown(
            id="f-month", className="dash-dropdown",
            options=[{"label":m,"value":i+1} for i,m in enumerate(
                ["January","February","March","April","May","June","July","August","September","October","November","December"])],
            value=7, clearable=False
        ),
        html.Div("Region", className="kpi-title mt-2"),
        dcc.Dropdown(
            id="f-region", className="dash-dropdown",
            options=[{"label":r,"value":r} for r in ["All","East Coast","West","South","Mountain"]],
            value="All"
        ),
        html.Div("Destination Type", className="kpi-title mt-2"),
        dcc.Dropdown(
            id="f-dest", className="dash-dropdown",
            options=[{"label":x,"value":x} for x in ["State","City","National Park"]],
            value="State"
        ),
        html.Div("Event Category", className="kpi-title mt-2"),
        dcc.Dropdown(
            id="f-event", className="dash-dropdown",
            options=[{"label":x,"value":x} for x in ["All","Music Festivals","Art Fairs","Sports","Holidays"]],
            value="All"
        ),
    ],
    className="soft-card tight",
    style={"height": MAP_H}
)

def kpi_card(title, idv):
    return html.Div(
        dbc.Card(
            [html.Div(title, className="kpi-title"),
             html.P(id=idv, children="—", className="kpi-value")],
            className="soft-card tight h-100",
        ),
        className="kpi-col"
    )

left_kpis = html.Div(
    [kpi_card("Top Origin Market", "kpi-origin"),
     kpi_card("Avg Hotel Occupancy","kpi-occ")],
    className="kpi-row", style={"height": KPI_H}
)

right_kpis = html.Div(
    [kpi_card("Total Visitors","kpi-visitors"),
     kpi_card("Avg Spend / Visitor","kpi-spend"),
     kpi_card("Peak Year", "kpi-peakyear"),
     kpi_card("YoY Growth","kpi-yoy"),
     kpi_card("Top Event","kpi-event"),
     kpi_card("Top by Impact","kpi-impact")],
    className="kpi-row", style={"height": KPI_H}
)

map_card = dbc.Card(
    dcc.Graph(
        id="us-map",
        figure=build_map(df_map),
        style={"height":"100%", "backgroundColor":"transparent"},
        config={"displayModeBar": False}
    ),
    className="soft-card tight map-card",
    style={"height": MAP_H}
)

heat_card = dbc.Card(
    [html.Div("Seasonality Heatmap", className="kpi-title mb-1"),
     dcc.Graph(id="heatmap", figure=build_heatmap(df_heat), style={"height":"24vh"}, config={"displayModeBar": False})],
    className="soft-card tight"
)
trend_card = dbc.Card(
    [html.Div("Drilldown — Tourist Inflows (Latest Year)", className="kpi-title mb-1"),
     dcc.Graph(id="trend", figure=build_trend(df_month), style={"height":"24vh"}, config={"displayModeBar": False})],
    className="soft-card tight"
)
evt_card = dbc.Card(
    [html.Div("Event Impact", className="kpi-title mb-1"),
     dcc.Graph(id="evt", figure=build_events(evt), style={"height":"24vh"}, config={"displayModeBar": False})],
    className="soft-card tight"
)


#  LAYOUT

app.layout = dbc.Container(
    [
        dbc.Row(
            [dbc.Col(html.Div("Tourist Flow & Seasonality Analyzer", className="section-title"), width=12)],
            className="g-0", style={"height": "6vh", "marginTop": TITLE_TOP}
        ),

        dbc.Row(
            [
                dbc.Col([sidebar_filters, html.Div(style={"height": ROW_GAP}), left_kpis],
                        width=4,
                        style={"display":"flex","flexDirection":"column","height": COLUMN_H}),
                dbc.Col([map_card, html.Div(style={"height": ROW_GAP}), right_kpis],
                        width=8,
                        style={"display":"flex","flexDirection":"column","height": COLUMN_H})
            ],
            className="g-3"
        ),

        dbc.Row(
            [dbc.Col(heat_card,  width=4),
             dbc.Col(trend_card, width=5),
             dbc.Col(evt_card,   width=3)],
            className="g-3",  style={"height":"25vh", "marginTop": "5px"}
        ),
    ],
    fluid=True, className="dbc-container pb-3",
    style={"height":"100vh","overflow":"hidden"}
)


#  CALLBACKS — FIGURES

@app.callback(
    [Output("us-map", "figure"),
     Output("heatmap", "figure"),
     Output("trend", "figure"),
     Output("evt", "figure")],
    [Input("f-month", "value"),
     Input("f-region", "value"),
     Input("f-dest", "value"),
     Input("f-event", "value")]
)
def update_all(month_val, region_val, dest_val, event_val):
    seed = (int(month_val or 1) * 1000
            + (hash(region_val) % 1000 if region_val else 0)
            + (hash(dest_val) % 1000 if dest_val else 0)
            + (hash(event_val) % 1000 if event_val else 0))
    rng = np.random.default_rng(seed)

    # MAP
    dfm = df_map.copy()
    if region_val and region_val != "All":
        allowed = set(REGIONS.get(region_val, []))
        sel_mask = dfm["state"].isin(allowed)
    else:
        sel_mask = np.ones(len(dfm), dtype=bool)

    p_hot, p_nrm, p_off = 0.35, 0.45, 0.20
    if dest_val == "National Park":
        p_hot += 0.05; p_nrm -= 0.03; p_off -= 0.02
    if event_val and event_val != "All":
        p_hot += 0.03; p_nrm -= 0.02; p_off -= 0.01
    tot = p_hot + p_nrm + p_off
    probs = [p_hot/tot, p_nrm/tot, p_off/tot]
    dfm.loc[sel_mask, "lift"] = rng.choice(["Hotspot","Normal","Off-Season"], size=sel_mask.sum(), p=probs)
    dfm.loc[~sel_mask, "lift"] = "Normal"
    dfm["lift"] = pd.Categorical(dfm["lift"], categories=CATEGORY_ORDER["lift"], ordered=True)
    map_out = build_map(dfm)

    # HEATMAP
    heat_vals = rng.integers(30, 95, size=(4,4))
    dfh = (pd.DataFrame(heat_vals, index=["Spring","Summer","Fall","Winter"],
                        columns=["Spring","Summer","Fall","Winter"])
           .reset_index().melt(id_vars="index", var_name="Season", value_name="Score")
           .rename(columns={"index":"Season_Row"}))
    heat_out = build_heatmap(dfh)

    # TREND
    base = np.linspace(0.9, 1.6, 12) * 1_000_000
    region_factor = (sel_mask.sum() / len(dfm))
    month_bias = (int(month_val or 1) - 6) / 36.0
    scale = 0.8 + 0.6*region_factor + month_bias
    visits = np.round(base * max(0.5, scale), 0)
    trend_out = build_trend(pd.DataFrame({"month": ALL_MONTHS, "visits": visits}))

    # EVENTS
    ev = evt.copy()
    ev["spike"] = np.clip(ev["spike"] + rng.integers(-6, 7, len(ev)) + int(region_factor*5), 5, 60)
    evt_out = build_events(ev)

    return map_out, heat_out, trend_out, evt_out


#  CALLBACKS — KPIs (YoY color)

@app.callback(
    [Output("kpi-visitors","children"),
     Output("kpi-spend","children"),
     Output("kpi-occ","children"),
     Output("kpi-yoy","children"),
     Output("kpi-yoy","style"),
     Output("kpi-event","children"),
     Output("kpi-impact","children"),
     Output("kpi-origin","children"),
     Output("kpi-peakyear","children")],
    [Input("f-month","value"),
     Input("f-region","value"),
     Input("f-dest","value"),
     Input("f-event","value")]
)
def update_kpis(month_val, region_val, dest_val, event_val):
    seed = (int(month_val or 1) * 1000
            + (hash(region_val) % 1000 if region_val else 0)
            + (hash(dest_val) % 1000 if dest_val else 0)
            + (hash(event_val) % 1000 if event_val else 0))
    rng = np.random.default_rng(seed)

    dfm = df_map.copy()
    if region_val and region_val != "All":
        allowed = set(REGIONS.get(region_val, []))
        sel_mask = dfm["state"].isin(allowed)
    else:
        sel_mask = np.ones(len(dfm), dtype=bool)
    region_factor = (sel_mask.sum() / len(dfm))

    visitors_num = int(kpi_baseline["total_visitors"] * (0.6 + region_factor*0.8))
    visitors = f"{visitors_num/1_000_000:.1f}M"
    spend = f"${int(kpi_baseline['avg_spend'] * (0.85 + rng.random()*0.4))}"
    occ = f"{int(50 + region_factor*30 + rng.random()*15)}%"

    yoy_val = int(-5 + rng.random()*15)
    yoy_text = f"{yoy_val}%"
    yoy_style = {"color": "#4ade80"} if yoy_val >= 0 else {"color": "#f87171"}

    top_event = evt.sample(1, random_state=rng.integers(0, 10_000))["event"].iloc[0]
    dfm.loc[sel_mask, "lift"] = rng.choice(["Hotspot","Normal","Off-Season"], size=sel_mask.sum(), p=[0.35,0.45,0.20])
    dfm.loc[~sel_mask, "lift"] = "Normal"
    hot = dfm[dfm["lift"]=="Hotspot"]["state_name"]
    top_impact = hot.sample(1, random_state=rng.integers(0, 10_000)).iloc[0] if not hot.empty else "—"
    top_origin = ["California","Texas","Florida","New York","Illinois","Washington","Arizona","Colorado"][rng.integers(0,8)]

    seasonal = np.array([0.8,0.85,0.95,1.05,1.15,1.25,1.30,1.20,1.00,0.95,0.90,0.85])
    m_idx = (int(month_val or 1) - 1) % 12
    month_mult = seasonal[m_idx]
    dest_boost = 1.06 if dest_val == "National Park" else (1.02 if dest_val == "State" else 1.00)
    event_boost = 1.03 if (event_val and event_val != "All") else 1.00
    region_boost = 0.9 + 0.4*region_factor
    year_noise = rng.normal(0.0, 0.06, size=len(YEARS))
    year_trend = np.linspace(0.92, 1.08, len(YEARS))
    visitors_year = (month_mult * dest_boost * event_boost * region_boost) * (1.0 + year_noise) * year_trend
    peak_year = YEARS[int(np.argmax(visitors_year))]

    return visitors, spend, occ, yoy_text, yoy_style, top_event, top_impact, top_origin, str(peak_year)


#  RUN

if __name__ == "__main__":
    app.run(debug=True)

