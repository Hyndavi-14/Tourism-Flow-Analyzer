
# app.py
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from theme import INDEX_STRING
from pages.dashboard import dashboard_layout
from pages.analytics import analytics_layout
from pages.reports import reports_layout
from pages.recommendations import recommendations_layout
from core import register_callbacks, parks_df

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True,
)
app.title = "Tourist Flow & Seasonality Analyzer"
app.index_string = INDEX_STRING

sidebar = html.Div(
    [
        html.Div("TFSA", className="sidebar-logo"),
        html.Div("Tourist Flow & Seasonality", className="sidebar-subtitle"),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.Span(className="dot"), "Dashboard"],
                    href="/",
                    active="exact",
                    className="nav-link",
                ),
                dbc.NavLink(
                    [html.Span(className="dot"), "Analytics"],
                    href="/analytics",
                    active="exact",
                    className="nav-link",
                ),
                dbc.NavLink(
                    [html.Span(className="dot"), "Reports"],
                    href="/reports",
                    active="exact",
                    className="nav-link",
                ),
                dbc.NavLink(
                    [html.Span(className="dot"), "Recommendations"],
                    href="/recommendations",
                    active="exact",
                    className="nav-link",
                ),
            ],
            vertical=True,
            pills=True,
            className="sidebar-nav",
        ),
        html.Div(
            "Capstone · National Parks Visitor Insights",
            className="sidebar-footer",
        ),
    ],
    className="sidebar",
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(sidebar),
        html.Div(id="page-content", className="content-wrapper"),
    ],
    className="layout-root",
)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def render_page(pathname):
    if pathname in ["/", "/dashboard", None]:
        return dashboard_layout()
    if pathname == "/analytics":
        return analytics_layout()
    if pathname == "/reports":
        return reports_layout()
    if pathname == "/recommendations":
        return recommendations_layout()
    return dashboard_layout()

@app.callback(
    Output("download-data", "data"),
    Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    return dcc.send_data_frame(
        parks_df.to_csv,
        "all_parks_recreation_visits.csv",
        index=False,
    )

register_callbacks(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)