# analytics.py

from dash import html, dcc
import dash_bootstrap_components as dbc

from core import (
    DEFAULT_MONTH,
    DEFAULT_YEAR,
    init_heat,
    init_trend,
    init_top5,
    init_top_states,
    init_yearly,
    init_ptype,
)

from pages.dashboard import filter_dropdowns_card


def analytics_layout():
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "Analytics Deep Dive",
                                className="page-title",
                            ),
                            html.Div(
                                "Seasonality patterns, yearly movement and state-level leaders driven by your filters.",
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
                                    "Insights View",
                                    style={"fontWeight": 500},
                                ),
                            ],
                            className="badge-chip",
                        ),
                        className="page-header-pill-wrapper",
                    ),
                ],
                className="hero-card",
            ),

            filter_dropdowns_card(),

            # ===== CHART GRID =====
            html.Div(
                [
                    # 1 – Region–Season heatmap
                    dbc.Card(
                        [
                            html.Div("Region–Season Heat", className="chart-title"),
                            dcc.Graph(
                                id="heatmap-analytics",
                                figure=init_heat,
                                style={"height": "100%"},
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="soft-card chart-card",
                    ),

                    # 2 – Yearly visitors trend
                    dbc.Card(
                        [
                            html.Div("Yearly Visitors Trend", className="chart-title"),
                            dcc.Graph(
                                id="trend-analytics",
                                figure=init_trend,
                                style={"height": "100%"},
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="soft-card chart-card",
                    ),

                    # 3 – Top 5 parks (month)
                    dbc.Card(
                        [
                            html.Div("Top 5 Parks (Month)", className="chart-title"),
                            dcc.Graph(
                                id="top5-parks-analytics",
                                figure=init_top5,
                                style={"height": "100%"},
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="soft-card chart-card",
                    ),

                    # 4 – Top park per year (area)
                    dbc.Card(
                        [
                            html.Div("Top Park per Year (Area)", className="chart-title"),
                            dcc.Graph(
                                id="top-states-analytics",
                                figure=init_top_states,
                                style={"height": "100%"},
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="soft-card chart-card",
                    ),

                    # 5 – Active parks per year
                    dbc.Card(
                        [
                            html.Div("Active Parks per Year", className="chart-title"),
                            dcc.Graph(
                                id="yearly-analytics",
                                figure=init_yearly,
                                style={"height": "100%"},
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="soft-card chart-card",
                    ),

                    # 6 – Avg spend per visitor (top states)
                    dbc.Card(
                        [
                            html.Div(
                                "Avg Spend per Visitor (Top States)",
                                className="chart-title",
                            ),
                            dcc.Graph(
                                id="park-type-analytics",
                                figure=init_ptype,
                                style={"height": "100%"},
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="soft-card chart-card",
                    ),
                ],
                className="charts-grid",
            ),
        ],
        className="page-body",
    )
