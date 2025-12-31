# recommendations.py

from dash import html
import dash_bootstrap_components as dbc


def _season_card(icon, title, months, regions, why_rows):
    return dbc.Card(
        [
            html.Div(
                [
                    html.Span(
                        icon,
                        className="season-icon",
                        style={
                            "fontSize": "26px",
                            "marginRight": "10px",
                            "background": "rgba(148,163,253,.25)",
                            "padding": "4px 8px",
                            "borderRadius": "999px",
                        },
                    ),
                    html.Span(title, className="season-name"),
                ],
                className="season-header",
            ),
            html.Div(months, className="season-months"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Best Regions", className="season-section-title"),
                            html.Ul([html.Li(r) for r in regions], className="season-list"),
                        ]
                    ),
                    html.Div(
                        [
                            html.Div("Why Go Now", className="season-section-title"),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            html.Span(emoji, style={"marginRight": "6px"}),
                                            text,
                                        ]
                                    )
                                    for (emoji, text) in why_rows
                                ],
                                className="season-list",
                            ),
                        ]
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "minmax(0,1.1fr) minmax(0,1.3fr)",
                    "gap": "12px",
                    "marginTop": "6px",
                },
            ),
        ],
        className="soft-card season-card",
    )


def recommendations_layout():
    return html.Div(
        [
            # HEADER
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Recommendations", className="page-title"),
                            html.Div(
                                "Best places to visit based on seasonality, regional flow patterns and comfort preferences.",
                                className="page-subtitle",
                            ),
                        ],
                        className="page-header-text",
                    ),
                    html.Div(
                        html.Div(
                            [
                                html.Span("💡", style={"fontSize": "20px", "marginRight": "6px"}),
                                html.Span("Insights View", style={"fontWeight": 500}),
                            ],
                            className="badge-chip",
                        )
                    ),
                ],
                className="header-card",
                style={"minHeight": "96px", "padding": "16px 26px"},
            ),

            # MAIN CONTENT
            html.Div(
                [
                    html.Div(
                        "Best Places to Visit Based on Seasonality & Flow Analysis",
                        className="reco-section-title",
                        style={"marginTop": "-4px"},  
                    ),

                    # SEASON GRID
                    html.Div(
                        [
                            _season_card(
                                "🌸",
                                "Spring",
                                "March – May",
                                [
                                    "Northeast U.S. – New York, Vermont, Maine",
                                    "Pacific Northwest – Washington, Oregon",
                                ],
                                [
                                    ("🌼", "Bloom season, mild temperatures."),
                                    ("📸", "Great visibility for scenic drives & photos."),
                                    ("🚶‍♀️", "Crowds still lighter than peak summer."),
                                ],
                            ),
                            _season_card(
                                "☀️",
                                "Summer",
                                "June – August",
                                [
                                    "Alaska National Parks",
                                    "Colorado & Wyoming – Rocky Mountain corridor",
                                ],
                                [
                                    ("🌅", "Longest daylight hours for sightseeing."),
                                    ("🥾", "Stable weather for hikes & outdoor activities."),
                                    ("🎪", "Signature summer events & festivals."),
                                ],
                            ),
                            _season_card(
                                "🍂",
                                "Fall",
                                "September – November",
                                [
                                    "New England – MA, VT, NH, CT",
                                    "Great Smoky Mountains – Tennessee / North Carolina",
                                ],
                                [
                                    ("🍁", "Peak foliage and photography season."),
                                    ("🌤️", "Comfortable daytime temperatures."),
                                    ("🏨", "Lower hotel pressure than summer holidays."),
                                ],
                            ),
                            _season_card(
                                "❄️",
                                "Winter",
                                "December – February",
                                [
                                    "Utah & Colorado ski resorts",
                                    "New York City – holiday season & New Year",
                                ],
                                [
                                    ("⛷️", "Snow sports and winter-only activities."),
                                    ("🎄", "Festive markets, lights and events."),
                                    ("💸", "Off-season discounts in some park towns."),
                                ],
                            ),
                        ],
                        className="season-grid",
                    ),

                    # SECTION LABEL 
                    html.Div(
                        "Recommendations Based on Weather Conditions",
                        className="reco-section-title",
                        style={"marginTop": "6px"},  
                    ),

                    # WEATHER CARDS
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    html.Div(
                                        "Warm Weather Lovers",
                                        className="reco-subtitle",
                                        style={"color": "#ffffff"},  
                                    ),
                                    html.Ul(
                                        [
                                            html.Li("Florida (Oct – Apr)"),
                                            html.Li("Southern California – year-round"),
                                            html.Li("Gulf Coast drives & beaches"),
                                        ],
                                        className="season-list",
                                    ),
                                ],
                                className="soft-card mini-reco-card",
                            ),
                            dbc.Card(
                                [
                                    html.Div(
                                        "Cool Weather Lovers",
                                        className="reco-subtitle",
                                        style={"color": "#ffffff"},
                                    ),
                                    html.Ul(
                                        [
                                            html.Li("Washington & Oregon – Apr–Jun"),
                                            html.Li("Colorado – Sep–Oct shoulder season"),
                                            html.Li("Appalachian Mountains – late spring hikes"),
                                        ],
                                        className="season-list",
                                    ),
                                ],
                                className="soft-card mini-reco-card",
                            ),
                        ],
                        className="mini-reco-row",
                    ),

                    # FINAL SECTION
                    html.Div(
                        "Recommendations Based on Temperature",
                        className="reco-section-title",
                        style={"marginTop": "12px"},
                    ),
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    html.Div("For More Mild Days", className="reco-subtitle"),
                                    html.Ul(
                                        [
                                            html.Li("Spring – Northeast & Mid-Atlantic"),
                                            html.Li("Early Summer – West Coast national parks"),
                                        ],
                                        className="season-list",
                                    ),
                                ],
                                className="soft-card mini-reco-card",
                            ),
                            dbc.Card(
                                [
                                    html.Div("Comfort / Avoid", className="reco-subtitle"),
                                    html.Ul(
                                        [
                                            html.Li("Avoid peak-summer desert heat (AZ, NV, TX)."),
                                            html.Li("Prefer fall or late winter for these regions."),
                                        ],
                                        className="season-list",
                                    ),
                                ],
                                className="soft-card mini-reco-card",
                            ),
                        ],
                        className="mini-reco-row",
                    ),
                ],
                className="reco-page-body",
            ),
        ],
        className="page-body",
    )
