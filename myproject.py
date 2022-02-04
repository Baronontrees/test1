
import numpy as np
import plotly.graph_objects as go  # or plotly.express as px

from mydash import search_bar, PLOTLY_LOGO
from scatterplot import create_callback

N = 100000
r = np.random.uniform(0, 1, N)
theta = np.random.uniform(0, 2*np.pi, N)

fig = go.Figure(data=go.Scatter(
    x = r * np.cos(theta), # non-uniform distribution
    y = r * np.sin(theta), # zoom to see more points at the center
    mode='markers',
    marker=dict(
        color=np.random.randn(N),
        colorscale='Viridis',
        line_width=1
    )
))

fig2 = go.Figure(data=go.Scatter(
    y = np.random.randn(500),
    mode='markers',
    marker=dict(
        size=16,
        color=np.random.randn(500), #set color equal to a variable
        colorscale='Viridis', # one of plotly colorscales
        showscale=True
    )
))

# fig.show()

import dash
from dash import html, Output, Input
import dash_bootstrap_components as dbc

app = dash.Dash()

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        # dbc.Col(dbc.NavbarBrand("", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            html.Div(style={'padding-left': '50px'}),
            dbc.Button("Primary", color="primary", className="me-1", id='mybutton'),
        ]
    ),
    color="dark",
    dark=True,
)

import dash_core_components as dcc

app.layout = html.Div([
    navbar,
    dcc.Graph(figure=fig, id='fig'),
    dcc.Graph(figure=fig2, id= 'fig2'),
    html.Div(id='my-output'),

])

@app.callback(
    Output("my-output", "children"),
    Input("mybutton", "n_clicks"),
)
def update_output_div(n):
    if n:
        return fig
    return fig2

# @app.callback(
#     Output("fig", "children"),
#     Input("fig2", "n_clicks"),
# )
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
#
create_callback(app)

server = app.server

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
