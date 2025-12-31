# app/pages/reports.py
from dash import html, dcc
import dash_bootstrap_components as dbc


def reports_layout():
    return html.Div(
        [
            # ========= HEADER  =========
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "Tourism Analytics Report",
                                className="page-title",
                            ),
                            html.Div(
                                "Executive summary of visitor trends, seasonality and revenue signals derived from the dashboard filters.",
                                className="page-subtitle",
                            ),
                        ],
                        className="page-header-text",
                    ),
                    html.Div(
                        html.Div(
                            [
                                html.Span(
                                    "📑",
                                    style={
                                        "fontSize": "20px",
                                        "marginRight": "6px",
                                    },
                                ),
                                html.Span(
                                    "Report View",
                                    style={"fontWeight": 500},
                                ),
                            ],
                            className="badge-chip",
                        ),
                        className="page-header-pill-wrapper",
                    ),
                ],
                className="header-card",
                
                style={"minHeight": "96px", "padding": "16px 26px"},
            ),

            # ========= OVERVIEW =========
            dbc.Card(
                [
                    html.Div("Overview", className="kpi-title mb-1"),
                    html.Div(
                        "This report presents a concise view of tourism patterns across U.S. destinations. "
                        "It highlights key performance metrics, seasonal peaks, regional behaviour and "
                        "revenue signals that can guide planning, marketing and investment decisions.",
                        className="storyline-text",
                    ),
                ],
                className="soft-card",
                style={"marginTop": "6px"},
            ),

            # ========= KEY METRICS with big clear icons =========
            dbc.Card(
                [
                    html.Div("Key Metrics (Current View)", className="kpi-title mb-2"),
                    dbc.Row(
                        [
                            # Total Visitors
                            dbc.Col(
                                dbc.Card(
                                    [
                                        html.Div(
                                            "Total Visitors",
                                            className="kpi-title mb-1",
                                        ),
                                        html.Div(
                                            [
                                                html.Div("72.5M", className="kpi-value"),
                                                html.Span(
                                                    "👥",
                                                    style={
                                                        "fontSize": "28px",
                                                        "marginLeft": "10px",
                                                        "background": "rgba(148,163,253,.25)",
                                                        "padding": "4px 8px",
                                                        "borderRadius": "999px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                                "gap": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "Across all selected regions",
                                            className="storyline-text",
                                        ),
                                    ],
                                    className="soft-card",
                                ),
                                md=3,
                            ),
                            # YoY Growth
                            dbc.Col(
                                dbc.Card(
                                    [
                                        html.Div(
                                            "YoY Growth",
                                            className="kpi-title mb-1",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "+6.4%",
                                                    className="kpi-value",
                                                    style={"color": "#4ade80"},
                                                ),
                                                html.Span(
                                                    "📈",
                                                    style={
                                                        "fontSize": "28px",
                                                        "marginLeft": "10px",
                                                        "background": "rgba(74,222,128,.25)",
                                                        "padding": "4px 8px",
                                                        "borderRadius": "999px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                                "gap": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "Compared to previous year",
                                            className="storyline-text",
                                        ),
                                    ],
                                    className="soft-card",
                                ),
                                md=3,
                            ),
                            # Peak Season
                            dbc.Col(
                                dbc.Card(
                                    [
                                        html.Div(
                                            "Peak Season",
                                            className="kpi-title mb-1",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "Summer",
                                                    className="kpi-value",
                                                ),
                                                html.Span(
                                                    "☀️",
                                                    style={
                                                        "fontSize": "28px",
                                                        "marginLeft": "10px",
                                                        "background": "rgba(250,204,21,.25)",
                                                        "padding": "4px 8px",
                                                        "borderRadius": "999px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                                "gap": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "Jun – Aug show strongest uplift",
                                            className="storyline-text",
                                        ),
                                    ],
                                    className="soft-card",
                                ),
                                md=3,
                            ),
                            # Avg Trip Length
                            dbc.Col(
                                dbc.Card(
                                    [
                                        html.Div(
                                            "Avg Trip Length",
                                            className="kpi-title mb-1",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    "5.8 days",
                                                    className="kpi-value",
                                                ),
                                                html.Span(
                                                    "🧳",
                                                    style={
                                                        "fontSize": "28px",
                                                        "marginLeft": "10px",
                                                        "background": "rgba(56,189,248,.25)",
                                                        "padding": "4px 8px",
                                                        "borderRadius": "999px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                                "gap": "6px",
                                            },
                                        ),
                                        html.Div(
                                            "Typical visit duration for top parks",
                                            className="storyline-text",
                                        ),
                                    ],
                                    className="soft-card",
                                ),
                                md=3,
                            ),
                        ],
                        className="g-3",
                    ),
                ],
                className="soft-card",
                style={"marginTop": "6px"},
            ),

            # ========= REGIONAL PERFORMANCE TEXT CARD =========
            dbc.Card(
                [
                    html.Div("Regional Performance", className="kpi-title mb-1"),
                    html.Div(
                        "Regional analysis shows how visitor flows differ between East Coast, Mountain, "
                        "South and Western clusters. Use this when explaining why specific regions lead "
                        "or lag for the chosen month and filters.",
                        className="storyline-text",
                    ),
                ],
                className="soft-card",
                style={"marginTop": "6px"},
            ),

            # ========= MID GRID: SEASONAL INSIGHTS =========
            dbc.Row(
                [
                    # Seasonal Insights
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "🗺️",
                                            style={
                                                "fontSize": "28px",
                                                "marginRight": "10px",
                                                "background": "rgba(56,189,248,.25)",
                                                "padding": "4px 8px",
                                                "borderRadius": "999px",
                                            },
                                        ),
                                        html.Div(
                                            "Seasonal Insights",
                                            className="kpi-title mb-0",
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "marginBottom": "4px",
                                    },
                                ),
                                html.Div(
                                    "Map-driven view of how states shift between hotspot, normal "
                                    "and off-season status.",
                                    className="storyline-text",
                                ),
                                html.Ul(
                                    [
                                        html.Li(
                                            "🌞 Summer shows the sharpest spike in visitation for most regions."
                                        ),
                                        html.Li(
                                            "🌱 Spring shoulder season is strong in the South and Mountain regions."
                                        ),
                                        html.Li(
                                            "❄ Winter demand is concentrated in select warm-weather and ski hubs."
                                        ),
                                    ],
                                    className="storyline-text",
                                ),
                            ],
                            className="soft-card",
                        ),
                        md=6,
                    ),

                    # Visitor Behaviour Analysis
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "🚶‍♀️",
                                            style={
                                                "fontSize": "28px",
                                                "marginRight": "10px",
                                                "background": "rgba(251,113,133,.25)",
                                                "padding": "4px 8px",
                                                "borderRadius": "999px",
                                            },
                                        ),
                                        html.Div(
                                            "Visitor Behaviour Analysis",
                                            className="kpi-title mb-0",
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "marginBottom": "4px",
                                    },
                                ),
                                html.Div(
                                    "Behaviour signals inferred from repeat visits, park type mix "
                                    "and monthly activity.",
                                    className="storyline-text",
                                ),
                                html.Ul(
                                    [
                                        html.Li(
                                            "👨‍👩‍👧 Family-oriented parks and scenic routes dominate summer traffic."
                                        ),
                                        html.Li(
                                            "🧳 Short weekend trips cluster around spring and fall long weekends."
                                        ),
                                        html.Li(
                                            "🌆 City destinations recover strongly vs purely rural trips."
                                        ),
                                    ],
                                    className="storyline-text",
                                ),
                            ],
                            className="soft-card",
                        ),
                        md=6,
                    ),
                ],
                className="g-3",
                style={"marginTop": "6px"},
            ),

            # ========= PERFORMANCE + REVENUE =========
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "📍",
                                            style={
                                                "fontSize": "28px",
                                                "marginRight": "10px",
                                                "background": "rgba(248,250,252,.12)",
                                                "padding": "4px 8px",
                                                "borderRadius": "999px",
                                            },
                                        ),
                                        html.Div(
                                            "Park & Attraction Performance",
                                            className="kpi-title mb-0",
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "marginBottom": "4px",
                                    },
                                ),
                                html.Ul(
                                    [
                                        html.Li(
                                            "⭐ Best-performing park: Blue Ridge PKWY (current month)."
                                        ),
                                        html.Li(
                                            "📈 Emerging attractions in Mountain and Pacific Northwest regions."
                                        ),
                                        html.Li(
                                            "🚀 Highest seasonal surge in coastal states during peak summer."
                                        ),
                                        html.Li(
                                            "⚠ Under-utilised off-season parks ripe for targeted campaigns."
                                        ),
                                    ],
                                    className="storyline-text",
                                ),
                            ],
                            className="soft-card",
                        ),
                        md=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "📊",
                                            style={
                                                "fontSize": "28px",
                                                "marginRight": "10px",
                                                "background": "rgba(147,197,253,.25)",
                                                "padding": "4px 8px",
                                                "borderRadius": "999px",
                                            },
                                        ),
                                        html.Div(
                                            "Revenue Summary (Indicative)",
                                            className="kpi-title mb-0",
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "marginBottom": "4px",
                                    },
                                ),
                                html.Ul(
                                    [
                                        html.Li(
                                            "💵 Higher spend per visitor in gateway cities and flagship parks."
                                        ),
                                        html.Li(
                                            "📅 Seasonal peak prediction aligns with school holidays & long weekends."
                                        ),
                                        html.Li(
                                            "🎟 Upsell opportunity: guided tours, bundled passes, local experiences."
                                        ),
                                        html.Li(
                                            "🌪 Risk factors: extreme weather events and access restrictions."
                                        ),
                                    ],
                                    className="storyline-text",
                                ),
                            ],
                            className="soft-card",
                        ),
                        md=6,
                    ),
                ],
                className="g-3",
                style={"marginTop": "6px"},
            ),

            # ========= RECOMMENDATIONS + CONCLUSION =========
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    "✅ Recommendations",
                                    className="kpi-title mb-1",
                                ),
                                html.Ul(
                                    [
                                        html.Li(
                                            "Strengthen promotion in off-season months with bundled offers."
                                        ),
                                        html.Li(
                                            "Focus campaigns on top-growth regions and high-value segments."
                                        ),
                                        html.Li(
                                            "Coordinate with local partners for events in shoulder seasons."
                                        ),
                                    ],
                                    className="storyline-text",
                                ),
                            ],
                            className="soft-card",
                        ),
                        md=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    "📌 Conclusion",
                                    className="kpi-title mb-1",
                                ),
                                html.Div(
                                    "Use this page as a ready-made storyboard slide. It summarises where demand "
                                    "is concentrated, how it moves through the year and which levers can influence it.",
                                    className="storyline-text",
                                ),
                            ],
                            className="soft-card",
                        ),
                        md=6,
                    ),
                ],
                className="g-3",
                style={"marginTop": "6px"},
            ),

            # ========= TOOLS & DATA =========
            dbc.Card(
                [
                    html.Div("Tools & Data", className="kpi-title mb-1"),
                    html.Div(
                        "Quick actions to refresh or share this analysis.",
                        className="storyline-text mb-2",
                    ),
                    dbc.Button(
                        "🔄 Reset All Filters",
                        id="btn-reset-filters",
                        color="info",
                        className="me-2 mb-2",
                    ),
                    dcc.Download(id="download-data"),
                    dbc.Button(
                        "⬇ Download CSV (All Parks)",
                        id="btn-download-csv",
                        color="primary",
                        className="mb-2",
                    ),
                ],
                className="soft-card",
                style={"marginTop": "6px", "marginBottom": "4px"},
            ),
        ],
        className="page-body",
    )
