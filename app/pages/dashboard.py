from dash import html, dcc
import dash_bootstrap_components as dbc

from core import YEARS, DEFAULT_MONTH, DEFAULT_YEAR, parks_df, init_map


# -----------------------------
# filter dropdowns card
# -----------------------------
def filter_dropdowns_card():
    return dbc.Card(
        [
            html.Div("Filters", className="filters-title"),
            html.Div(
                [
                    # Month
                    html.Div(
                        [
                            html.Div("Month", className="filter-label"),
                            dcc.Dropdown(
                                id="f-month",
                                className="dash-dropdown",
                                options=[
                                    {"label": m, "value": i + 1}
                                    for i, m in enumerate(
                                        [
                                            "January", "February", "March", "April",
                                            "May", "June", "July", "August",
                                            "September", "October", "November", "December",
                                        ]
                                    )
                                ],
                                value=DEFAULT_MONTH,
                                clearable=False,
                            ),
                        ]
                    ),
                    # Year
                    html.Div(
                        [
                            html.Div("Year", className="filter-label"),
                            dcc.Dropdown(
                                id="f-year",
                                className="dash-dropdown",
                                options=[{"label": str(y), "value": int(y)} for y in YEARS],
                                value=DEFAULT_YEAR,
                                clearable=False,
                            ),
                        ]
                    ),
                    # Region
                    html.Div(
                        [
                            html.Div("Region", className="filter-label"),
                            dcc.Dropdown(
                                id="f-region",
                                className="dash-dropdown",
                                options=[
                                    {"label": r, "value": r}
                                    for r in ["All", "East Coast", "West", "South", "Mountain"]
                                ],
                                value="All",
                            ),
                        ]
                    ),
                    # Destination type
                    html.Div(
                        [
                            html.Div("Destination Type", className="filter-label"),
                            dcc.Dropdown(
                                id="f-dest",
                                className="dash-dropdown",
                                options=[
                                    {"label": x, "value": x}
                                    for x in ["State", "City", "National Park"]
                                ],
                                value="State",
                            ),
                        ]
                    ),
                    # Park type
                    html.Div(
                        [
                            html.Div("Park Type", className="filter-label"),
                            dcc.Dropdown(
                                id="f-park-type",
                                className="dash-dropdown",
                                options=(
                                    [{"label": "All", "value": "All"}]
                                    + [
                                        {"label": t, "value": t}
                                        for t in sorted(
                                            parks_df["Park Type"].dropna().unique()
                                        )
                                    ]
                                ),
                                value="All",
                                clearable=False,
                            ),
                        ]
                    ),
                ],
                className="filters-row",
            ),
        ],
        className="soft-card filters-card",
    )


# -----------------------------
# KPI helper cards
# -----------------------------
def kpi_card(title, idv):
    return html.Div(
        dbc.Card(
            [
                html.Div(title, className="kpi-title"),
                html.Div(id=idv, children="—", className="kpi-value"),
            ],
            className="kpi-card-inner",
        )
    )


def extra_kpi_card(title, idv):
    return html.Div(
        dbc.Card(
            [
                html.Div(title, className="kpi-title"),
                html.Div(id=idv, children="—", className="kpi-value"),
            ],
            className="kpi-card-inner",
        )
    )


# -----------------------------
# KPI panel
# -----------------------------
kpi_panel = dbc.Card(
    [
        html.Div("Key Signals", className="kpi-title"),
        html.Div(
            [
                kpi_card("Top Park (Month)", "kpi-top-park-month"),
                kpi_card("Avg Visits / Park", "kpi-avg-park"),
                kpi_card("Total Visitors (Month)", "kpi-total-month"),
                kpi_card("Peak Year", "kpi-peak-year"),
                kpi_card("YoY Growth vs Prev Year", "kpi-yoy"),
                kpi_card("Top Park (Year)", "kpi-top-park-year"),
                extra_kpi_card("Total Visitors (Year)", "kpi-total-year"),
                extra_kpi_card("Most Visited State (Year)", "kpi-top-state-year"),
            ],
            className="kpi-row",
        ),
        html.Div(
            [
                html.Div(
                    "Monthly Pattern (Selected Year)",
                    className="kpi-title",
                    style={"marginTop": "10px"},
                ),
                dcc.Graph(
                    id="dashboard-sparkline",
                    style={"height": "14vh"},
                    config={"displayModeBar": False},
                ),
            ],
            style={"marginTop": "4px"},
        ),
    ],
    className="soft-card kpi-panel",
    style={"height": "100%"},
)

# -----------------------------
# Map + Storyline cards
# -----------------------------
map_card = dbc.Card(
    dcc.Graph(
        id="us-map",
        figure=init_map,
        style={"height": "100%", "backgroundColor": "transparent"},
        config={"displayModeBar": False},
    ),
    className="soft-card map-card",
)

storyline_card = dbc.Card(
    [
        html.Div("Storyline", className="kpi-title"),
        html.Div(
            id="storyline-block",
            className="storyline-text storyline-box",
        ),
    ],
    className="soft-card",
    style={"marginTop": "2px"},
)


# -----------------------------
# Dashboard layout
# -----------------------------
def dashboard_layout():
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "Tourist Flow & Seasonality Analyzer",
                                className="page-title",
                            ),
                            html.Div(
                                "Explore how national parks and destinations move between "
                                "hotspot, normal and off-season across the U.S.",
                                className="page-subtitle",
                            ),
                        ],
                        className="page-header-text",
                    ),
                    html.Div(
                        html.Div(
                            [
                                html.Span(className="badge-dot"),
                                html.Span(
                                    "Live Exploration",
                                    style={"fontWeight": 500},
                                ),
                            ],
                            className="badge-chip",
                        ),
                        className="page-header-pill-wrapper",
                    ),
                ],
                className="header-card",
            ),

            # Filters row
            filter_dropdowns_card(),

            # Main content row
            html.Div(
                [
                    html.Div(kpi_panel),
                    html.Div(
                        [
                            map_card,
                            storyline_card,
                        ],
                        className="map-side-wrapper",
                    ),
                ],
                className="main-row",
            ),
        ],
        className="page-body",
    )
