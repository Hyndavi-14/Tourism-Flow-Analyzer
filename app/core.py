# core.py

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html
from dash.dependencies import Input, Output

from theme import (
    MAP_H,
    KPI_H,
    CHART_H,
    COLOR_MAP,
    CATEGORY_ORDER,
    MAP_BG,
    CORAL,
    BUBBLE,
)
from src.db import get_engine  # <- IMPORTANT: use src.db, not db

# =========================================================
# DATA  (RDS with local CSV + forecast fallback)
# =========================================================

BASE_DIR = os.path.dirname(__file__)

TABLE_NAME = "parks_visits"

# 1) Try RDS first, otherwise use local CSV
try:
    engine = get_engine()
    parks_df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)
except Exception as e:
    print("WARNING: Could not connect to RDS, using local CSV instead.")
    print("Reason:", repr(e))
    local_csv = os.path.join(BASE_DIR, "all_parks_recreation_visits.csv")
    parks_df = pd.read_csv(local_csv)

# Mark all rows loaded so far as historical (not forecast)
parks_df["IsForecast"] = False

# 2) Load monthly_forecasts.csv and append FUTURE years only
FORECAST_PATH = os.path.join(BASE_DIR, "monthly_forecasts.csv")

if os.path.exists(FORECAST_PATH):
    fc_df = pd.read_csv(FORECAST_PATH)

    # Expected columns (from your screenshots):
    # Park, Best_Model, Forecast_Month, Predicted_Visits,
    # Unit Code, Park Type, Region, State, Year, Month, _source_file

    # If Forecast_Month exists, convert to Year / Month
    if "Forecast_Month" in fc_df.columns:
        fc_df["Forecast_Month"] = pd.to_datetime(
            fc_df["Forecast_Month"],
            dayfirst=True,        # because it's like 01-01-2025
            errors="coerce",
        )
        fc_df["Year"] = fc_df["Forecast_Month"].dt.year
        fc_df["Month"] = fc_df["Forecast_Month"].dt.month

    # Match visit column name
    if "Predicted_Visits" in fc_df.columns:
        fc_df = fc_df.rename(columns={"Predicted_Visits": "Recreation Visits"})

    # Ensure required columns exist
    required_cols = ["Park", "State", "Year", "Month", "Recreation Visits", "Park Type"]
    for col in required_cols:
        if col not in fc_df.columns:
            fc_df[col] = np.nan

    # Keep only years AFTER the last historical year
    hist_latest = pd.to_numeric(parks_df["Year"], errors="coerce").max()
    fc_df = fc_df[pd.to_numeric(fc_df["Year"], errors="coerce") > hist_latest]

    # Mark as forecast
    fc_df["IsForecast"] = True

    # Align columns where possible and append
    common_cols = list(set(parks_df.columns).intersection(fc_df.columns))
    parks_df = pd.concat(
        [parks_df, fc_df[common_cols]],
        ignore_index=True,
        sort=False,
    )

# =========================================================
# CLEANING
# =========================================================

parks_df = parks_df.dropna(
    subset=["State", "Park", "Month", "Year", "Recreation Visits"]
)

parks_df["State"] = parks_df["State"].astype(str).str.strip()
parks_df["Park"] = parks_df["Park"].astype(str).str.strip()
parks_df["Month"] = parks_df["Month"].astype(int)
parks_df["Year"] = parks_df["Year"].astype(int)
parks_df["Recreation Visits"] = parks_df["Recreation Visits"].astype(float)

if "Park Type" not in parks_df.columns:
    parks_df["Park Type"] = "Unknown"

# =========================================================
# CONSTANTS / HELPERS
# =========================================================

state_codes = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN",
    "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV",
    "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN",
    "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC",
]
state_names = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming", "District of Columbia",
]
STATE_NAME_MAP = dict(zip(state_codes, state_names))

REGIONS = {
    "East Coast": [
        "ME", "NH", "MA", "RI", "CT", "NY", "NJ", "PA", "DE",
        "MD", "DC", "VA", "NC", "SC", "GA", "FL",
    ],
    "West": ["CA", "OR", "WA", "AK", "HI"],
    "South": [
        "TX", "OK", "AR", "LA", "MS", "AL", "TN", "KY", "GA", "FL",
        "SC", "NC", "VA", "WV", "MD", "DC", "DE",
    ],
    "Mountain": ["AZ", "NM", "CO", "UT", "NV", "ID", "MT", "WY"],
}

ALL_MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def map_region_group(state_code: str) -> str:
    for r, lst in REGIONS.items():
        if state_code in lst:
            return r
    return "Other"


parks_df["RegionGroup"] = parks_df["State"].map(map_region_group)

YEARS = sorted(parks_df["Year"].unique())
LATEST_YEAR = max(YEARS) if YEARS else 0

# ===============
# FILTERING
# ===============

def filter_parks(
    month_val=None,
    year_val=None,
    region_val=None,
    dest_val=None,
    park_type_val=None,
):
    """
    Common filter used by ALL charts / KPIs.
    Month + Year + Region + Destination + Park Type.
    """
    df = parks_df.copy()

    if year_val is not None:
        df = df[df["Year"] == int(year_val)]

    if month_val is not None:
        df = df[df["Month"] == int(month_val)]

    if region_val and region_val != "All":
        allowed = set(REGIONS.get(region_val, []))
        df = df[df["State"].isin(allowed)]

    if dest_val == "National Park":
        df = df[df["Park Type"].str.contains("National Park", case=False, na=False)]
    elif dest_val == "City":
        df = df[~df["Park Type"].str.contains("National Park", case=False, na=False)]

    if park_type_val and park_type_val != "All":
        df = df[df["Park Type"] == park_type_val]

    return df

# ==============
# MAP HELPERS
# ==============

def classify_state_status(month_val, year_val, region_val, dest_val, park_type_val):
    df = filter_parks(month_val, year_val, region_val, dest_val, park_type_val)
    if df.empty:
        return {s: "Normal" for s in state_codes}

    grouped = df.groupby("State", as_index=False)["Recreation Visits"].sum()
    q_off = grouped["Recreation Visits"].quantile(0.33)
    q_hot = grouped["Recreation Visits"].quantile(0.66)

    status = {}
    for _, row in grouped.iterrows():
        v = row["Recreation Visits"]
        if v >= q_hot:
            seg = "Hotspot"
        elif v <= q_off:
            seg = "Off-Season"
        else:
            seg = "Normal"
        status[row["State"]] = seg

    for s in state_codes:
        status.setdefault(s, "Normal")

    return status


def build_base_map_df(month_val, year_val, region_val, dest_val, park_type_val):
    status_map = classify_state_status(month_val, year_val, region_val, dest_val, park_type_val)
    df = pd.DataFrame(
        {
            "state": state_codes,
            "state_name": [STATE_NAME_MAP[s] for s in state_codes],
            "lift": [status_map[s] for s in state_codes],
        }
    )
    df["lift"] = pd.Categorical(
        df["lift"], categories=CATEGORY_ORDER["lift"], ordered=True
    )

    df_month = filter_parks(month_val, year_val, region_val, dest_val, park_type_val)
    if df_month.empty:
        df["hover_parks"] = "No park data"
        return df

    grouped = df_month.groupby(["State", "Park"], as_index=False)["Recreation Visits"].sum()
    top_by_state = (
        grouped.sort_values("Recreation Visits", ascending=False)
        .groupby("State")["Park"]
        .apply(list)
        .to_dict()
    )

    hover = []
    for _, row in df.iterrows():
        parks = top_by_state.get(row["state"], [])
        if not parks:
            hover.append("No park data")
        else:
            hover.append(", ".join(parks[:5]))
    df["hover_parks"] = hover
    return df


def _common_layout(fig):
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        hoverlabel=dict(
            bgcolor="#050814",
            font_color="#ffffff",
        ),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showline=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showline=False)
    return fig


def build_map(df):
    fig = px.choropleth(
        df,
        locations="state",
        locationmode="USA-states",
        color="lift",
        custom_data=["lift", "state_name", "hover_parks"],
        color_discrete_map=COLOR_MAP,
        category_orders=CATEGORY_ORDER,
        scope="usa",
        hover_name="state_name",
        hover_data={
            "state": False,
            "state_name": False,
            "lift": True,
            "hover_parks": False,
        },
        labels={"lift": "Status"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            showlakes=False,
            showland=True,
            landcolor="#050811",
        ),
        legend=dict(
            title="Status",
            orientation="v",
            y=0.98,
            yanchor="top",
            x=0.98,
            xanchor="right",
            bgcolor="rgba(5,10,24,.9)",
            font=dict(color="#ffffff"),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        hoverlabel=dict(
            bgcolor="#050814",
            font_color="#ffffff",
        ),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[1]}</b>"
            "<br>Status: %{customdata[0]}"
            "<br>Top parks: %{customdata[2]}<extra></extra>"
        )
    )
    return fig

# =====================
# ANALYTICS FIGURES
# =====================

def build_heatmap_real(month_val, year_val, region_val, dest_val, park_type_val):
    """
    Region–Season heatmap for ALL months in the selected year.
    """
    df = filter_parks(None, year_val, region_val, dest_val, park_type_val)
    if df.empty:
        order_regions = ["East Coast", "Mountain", "South", "West"]
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        pivot = pd.DataFrame(0, index=order_regions, columns=seasons)
    else:
        def month_to_season(m):
            if m in [3, 4, 5]:
                return "Spring"
            if m in [6, 7, 8]:
                return "Summer"
            if m in [9, 10, 11]:
                return "Fall"
            return "Winter"

        df["Season"] = df["Month"].apply(month_to_season)
        agg = df.groupby(["RegionGroup", "Season"], as_index=False)["Recreation Visits"].sum()
        agg = agg[agg["RegionGroup"] != "Other"]

        order_regions = ["East Coast", "Mountain", "South", "West"]
        seasons = ["Spring", "Summer", "Fall", "Winter"]

        pivot = (
            agg.pivot(index="RegionGroup", columns="Season", values="Recreation Visits")
            .reindex(index=order_regions, columns=seasons)
            .fillna(0.0)
        )

    fig = px.imshow(
        pivot,
        color_continuous_scale="Blues",
        aspect="auto",
        labels=dict(color="Visits"),
        text_auto=False,
    )
    fig = _common_layout(fig)
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Visits",
        )
    )
    fig.update_xaxes(title="", type="category")
    fig.update_yaxes(title="", type="category")
    return fig


def build_dashboard_sparkline(year_val, region_val, dest_val, park_type_val):
    df = filter_parks(None, year_val, region_val, dest_val, park_type_val)
    if df.empty:
        visits = np.zeros(12)
    else:
        agg = df.groupby("Month", as_index=False)["Recreation Visits"].sum().set_index("Month")
        visits = [agg["Recreation Visits"].get(m, 0.0) for m in range(1, 13)]

    dfl = pd.DataFrame({"MonthName": ALL_MONTHS, "Visits": visits})
    fig = px.line(dfl, x="MonthName", y="Visits", markers=True)
    fig = _common_layout(fig)
    fig.update_traces(
        mode="lines+markers",
        line=dict(width=2, color="#38bdf8"),
        marker=dict(size=6),
        hovertemplate="<b>%{x}</b><br>Visits: %{y:,.0f}<extra></extra>",
    )
    fig.update_xaxes(title="", showgrid=False, showticklabels=False)
    fig.update_yaxes(title="", showgrid=False, showticklabels=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


def build_yearly_trend_overall(month_val, year_val, region_val, dest_val, park_type_val):
    """
    Yearly visitors trend for the selected MONTH across years.
    """
    df = filter_parks(month_val, None, region_val, dest_val, park_type_val)
    if df.empty:
        agg = pd.DataFrame({"Year": [], "Recreation Visits": []})
    else:
        agg = (
            df.groupby("Year", as_index=False)["Recreation Visits"]
            .sum()
            .sort_values("Year")
        )
        if year_val is not None and len(agg):
            agg = agg[agg["Year"] <= int(year_val)]

    fig = px.line(agg, x="Year", y="Recreation Visits")
    fig = _common_layout(fig)
    fig.update_traces(
        mode="lines",
        line=dict(width=2, color="#38bdf8"),
        hovertemplate="<b>%{x}</b><br>Visits: %{y:,.0f}<extra></extra>",
    )
    fig.update_xaxes(title="Year", showgrid=False)
    fig.update_yaxes(title="Visits", showgrid=False)
    return fig


def build_top5_parks(month_val, year_val, region_val, dest_val, park_type_val):
    df = filter_parks(month_val, year_val, region_val, dest_val, park_type_val)
    if df.empty:
        parks = pd.DataFrame({"Park": ["—"], "Recreation Visits": [0.0]})
    else:
        agg = (
            df.groupby("Park", as_index=False)["Recreation Visits"]
            .sum()
            .sort_values("Recreation Visits", ascending=False)
            .head(5)
        )
        parks = agg

    parks["ParkShort"] = parks["Park"].str.slice(0, 22)
    fig = px.pie(
        parks,
        names="ParkShort",
        values="Recreation Visits",
        hole=0.55,
        custom_data=["Park", "Recreation Visits"],
    )
    fig = _common_layout(fig)
    fig.update_traces(
        textinfo="percent",
        texttemplate="%{percent:.1%}",
        textposition="inside",
        textfont=dict(color="#ffffff", size=12),
        showlegend=True,
        hoverinfo="skip",
        hovertemplate=None,
    )
    fig.update_layout(
        legend_title_text="Park",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


def build_top_states(month_val, year_val, region_val, dest_val, park_type_val):
    """
    Top park per year – AREA chart.
    Uses selected MONTH so month dropdown also affects this.
    """
    df = filter_parks(month_val, None, region_val, dest_val, park_type_val)
    if df.empty:
        yearly = pd.DataFrame(
            {"Year": [0], "Recreation Visits": [0.0], "TopPark": ["—"]}
        )
    else:
        yearly_park = df.groupby(["Year", "Park"], as_index=False)["Recreation Visits"].sum()
        yearly = (
            yearly_park.sort_values("Recreation Visits", ascending=False)
            .groupby("Year", as_index=False)
            .first()
            .sort_values("Year")
        )
        yearly = yearly.rename(columns={"Park": "TopPark"})

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=yearly["Year"],
            y=yearly["Recreation Visits"],
            mode="lines",
            fill="tozeroy",
            line=dict(color=BUBBLE, width=2),
            customdata=yearly["TopPark"],
            hovertemplate=(
                "<b>%{x}</b><br>Top park: %{customdata}"
                "<br>Visits: %{y:,.0f}<extra></extra>"
            ),
            showlegend=False,
        )
    )
    fig = _common_layout(fig)
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Visits")
    return fig


def build_active_parks_per_year(month_val, year_val, region_val, dest_val, park_type_val):
    """
    Number of active parks per year for the selected MONTH.
    """
    df = filter_parks(month_val, None, region_val, dest_val, park_type_val)
    if df.empty:
        agg = pd.DataFrame({"Year": [], "ActiveParks": []})
    else:
        agg = (
            df.groupby(["Year"])["Park"]
            .nunique()
            .reset_index(name="ActiveParks")
            .sort_values("Year")
        )
        if year_val is not None and len(agg):
            agg = agg[agg["Year"] <= int(year_val)]

    fig = px.line(agg, x="Year", y="ActiveParks")
    fig = _common_layout(fig)
    fig.update_traces(
        mode="lines",
        line=dict(width=2, color="#a855f7"),
        hovertemplate="<b>%{x}</b><br>Active parks: %{y:.0f}<extra></extra>",
    )
    fig.update_xaxes(title="Year", showgrid=False)
    fig.update_yaxes(title="Active Parks", showgrid=False)
    return fig


def build_avg_spend_per_state(month_val, year_val, region_val, dest_val, park_type_val):
    df = filter_parks(month_val, year_val, region_val, dest_val, park_type_val)
    if df.empty:
        states = pd.DataFrame({"State": ["—"], "Recreation Visits": [0.0]})
    else:
        states = df.groupby("State", as_index=False)["Recreation Visits"].sum()

    if states["Recreation Visits"].max() > 0:
        visits = states["Recreation Visits"]
        norm = (visits - visits.min()) / (visits.max() - visits.min() + 1e-9)
        states["AvgSpend"] = 80 + norm * 120.0  # $80–$200
    else:
        states["AvgSpend"] = 0.0

    states["StateName"] = states["State"].map(STATE_NAME_MAP).fillna(states["State"])
    states = states.sort_values("AvgSpend", ascending=False).head(10)

    fig = px.bar(
        states,
        x="AvgSpend",
        y="StateName",
        orientation="h",
        text="AvgSpend",
    )
    fig = _common_layout(fig)
    fig.update_traces(
        texttemplate="$%{text:.0f}",
        textposition="outside",
        marker=dict(line=dict(width=0)),
        hovertemplate=(
            "<b>%{y}</b><br>Avg spend: $%{x:.0f}"
            "<br>Visits index: %{customdata}<extra></extra>"
        ),
        customdata=states["Recreation Visits"],
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=120, r=40, t=10, b=40),
    )
    fig.update_xaxes(
        title="Avg spend per visitor ($)",
        showgrid=False,
    )
    fig.update_yaxes(title="", showgrid=False)
    return fig

# ===========
# KPIs
# ===========

def fmt_millions(val: float) -> str:
    if val >= 1e9:
        return f"{val/1e9:.1f}B"
    if val >= 1e6:
        return f"{val/1e6:.1f}M"
    if val >= 1e3:
        return f"{val/1e3:.1f}K"
    return f"{val:.0f}"


def compute_kpis(month_val, year_val, region_val, dest_val, park_type_val):
    month_int = int(month_val)
    year_int = int(year_val)

    df_month = filter_parks(month_int, year_int, region_val, dest_val, park_type_val)
    if df_month.empty:
        top_park_month = "—"
        total_month = 0.0
        avg = 0.0
    else:
        g = (
            df_month.groupby("Park")["Recreation Visits"]
            .sum()
            .sort_values(ascending=False)
        )
        top_park_month = g.index[0]
        total_month = float(g.sum())
        avg = total_month / max(g.size, 1)

    df_all = filter_parks(None, None, region_val, dest_val, park_type_val)
    if df_all.empty:
        peak_year = year_int
        yoy_pct = 0.0
    else:
        yearly = df_all.groupby("Year", as_index=False)["Recreation Visits"].sum()
        peak_row = yearly.sort_values("Recreation Visits", ascending=False).iloc[0]
        peak_year = int(peak_row["Year"])

        curr = yearly[yearly["Year"] == year_int]["Recreation Visits"]
        prev = yearly[yearly["Year"] == (year_int - 1)]["Recreation Visits"]
        if curr.empty or prev.empty or prev.iloc[0] == 0:
            yoy_pct = 0.0
        else:
            yoy_pct = (curr.iloc[0] - prev.iloc[0]) / prev.iloc[0] * 100.0

    df_year = filter_parks(None, year_int, region_val, dest_val, park_type_val)
    if df_year.empty:
        top_park_year = "—"
        total_year = 0.0
        top_state_year = "—"
    else:
        g_year = (
            df_year.groupby("Park")["Recreation Visits"]
            .sum()
            .sort_values(ascending=False)
        )
        top_park_year = g_year.index[0]
        total_year = float(df_year["Recreation Visits"].sum())

        state_year = (
            df_year.groupby("State")["Recreation Visits"]
            .sum()
            .sort_values(ascending=False)
        )
        if len(state_year) == 0:
            top_state_year = "—"
        else:
            top_state_code = state_year.index[0]
            top_state_year = STATE_NAME_MAP.get(top_state_code, top_state_code)

    return {
        "top_park_month": top_park_month,
        "avg_per_park": avg,
        "total_month": total_month,
        "peak_year": peak_year,
        "yoy_pct": yoy_pct,
        "yoy_positive": yoy_pct >= 0,
        "top_park_year": top_park_year,
        "total_year": total_year,
        "top_state_year": top_state_year,
    }

# ==================
# INITIAL FIGURES
# ==================

DEFAULT_MONTH = 7
DEFAULT_YEAR = LATEST_YEAR

df_map_init = build_base_map_df(DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All")
init_map = build_map(df_map_init)
init_heat = build_heatmap_real(DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All")
init_trend = build_yearly_trend_overall(DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All")
init_top5 = build_top5_parks(DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All")
init_top_states = build_top_states(DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All")
init_yearly = build_active_parks_per_year(DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All")
init_ptype = build_avg_spend_per_state(DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All")
kpi0 = compute_kpis(DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All")

# ============
# CALLBACKS
# ============

def register_callbacks(app):
    # MAP
    @app.callback(
        Output("us-map", "figure"),
        [
            Input("f-month", "value"),
            Input("f-year", "value"),
            Input("f-region", "value"),
            Input("f-dest", "value"),
            Input("f-park-type", "value"),
        ],
    )
    def update_map(month_val, year_val, region_val, dest_val, park_type_val):
        dfm = build_base_map_df(month_val, year_val, region_val, dest_val, park_type_val)
        return build_map(dfm)

    @app.callback(
        Output("dashboard-sparkline", "figure"),
        [
            Input("f-year", "value"),
            Input("f-region", "value"),
            Input("f-dest", "value"),
            Input("f-park-type", "value"),
        ],
    )
    def update_dashboard_sparkline_cb(year_val, region_val, dest_val, park_type_val):
        return build_dashboard_sparkline(year_val, region_val, dest_val, park_type_val)

    # STORYLINE
    @app.callback(
        Output("storyline-block", "children"),
        [
            Input("f-month", "value"),
            Input("f-year", "value"),
            Input("f-region", "value"),
            Input("f-dest", "value"),
            Input("f-park-type", "value"),
        ],
    )
    def update_storyline(month_val, year_val, region_val, dest_val, park_type_val):
        k = compute_kpis(month_val, year_val, region_val, dest_val, park_type_val)
        month_name = ALL_MONTHS[int(month_val) - 1]
        bullets = [
            f"In {month_name} {year_val}, {fmt_millions(k['total_month'])} "
            f"visitors are recorded under the current view.",
            f"Top park this month is {k['top_park_month']} and the yearly leader is {k['top_park_year']}.",
            f"Visitor volume is {k['yoy_pct']:+.1f}% vs previous year, with peak year at {k['peak_year']}.",
        ]
        return [html.Div(text) for text in bullets]

    # ANALYTICS – ALL 6 CHARTS
    @app.callback(
        [
            Output("heatmap-analytics", "figure"),
            Output("trend-analytics", "figure"),
            Output("top5-parks-analytics", "figure"),
            Output("top-states-analytics", "figure"),
            Output("yearly-analytics", "figure"),
            Output("park-type-analytics", "figure"),
        ],
        [
            Input("f-month", "value"),
            Input("f-year", "value"),
            Input("f-region", "value"),
            Input("f-dest", "value"),
            Input("f-park-type", "value"),
        ],
    )
    def update_analytics_charts(month_val, year_val, region_val, dest_val, park_type_val):
        heat_out = build_heatmap_real(month_val, year_val, region_val, dest_val, park_type_val)
        trend_out = build_yearly_trend_overall(month_val, year_val, region_val, dest_val, park_type_val)
        top5_out = build_top5_parks(month_val, year_val, region_val, dest_val, park_type_val)
        states_out = build_top_states(month_val, year_val, region_val, dest_val, park_type_val)
        yearly_out = build_active_parks_per_year(month_val, year_val, region_val, dest_val, park_type_val)
        ptype_out = build_avg_spend_per_state(month_val, year_val, region_val, dest_val, park_type_val)
        return heat_out, trend_out, top5_out, states_out, yearly_out, ptype_out

    # KPIs – mini cards
    @app.callback(
        [
            Output("kpi-top-park-month", "children"),
            Output("kpi-avg-park", "children"),
            Output("kpi-total-month", "children"),
            Output("kpi-peak-year", "children"),
            Output("kpi-yoy", "children"),
            Output("kpi-yoy", "style"),
            Output("kpi-top-park-year", "children"),
            Output("kpi-total-year", "children"),
            Output("kpi-top-state-year", "children"),
        ],
        [
            Input("f-month", "value"),
            Input("f-year", "value"),
            Input("f-region", "value"),
            Input("f-dest", "value"),
            Input("f-park-type", "value"),
        ],
    )
    def update_kpis(month_val, year_val, region_val, dest_val, park_type_val):
        k = compute_kpis(month_val, year_val, region_val, dest_val, park_type_val)
        yoy_text = f"{k['yoy_pct']:+.1f}%"
        yoy_style = {"color": "#4ade80" if k["yoy_positive"] else "#f97373"}
        return (
            k["top_park_month"],
            f"{k['avg_per_park']:,.0f}",
            fmt_millions(k["total_month"]),
            str(k["peak_year"]),
            yoy_text,
            yoy_style,
            k["top_park_year"],
            fmt_millions(k["total_year"]),
            k["top_state_year"],
        )

    # FILTERS BUTTON
    @app.callback(
        [
            Output("f-month", "value"),
            Output("f-year", "value"),
            Output("f-region", "value"),
            Output("f-dest", "value"),
            Output("f-park-type", "value"),
        ],
        Input("btn-reset-filters", "n_clicks"),
        prevent_initial_call=True,
    )
    def reset_filters(n_clicks):
        return DEFAULT_MONTH, DEFAULT_YEAR, "All", "State", "All"
