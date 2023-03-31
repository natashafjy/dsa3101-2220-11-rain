import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
##app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])


layout = html.Div([
    dbc.Row([
        dbc.Col(html.H2("Welcome to <app-name>"),
                width={"size": 6, "offset": 3}),
   
        dbc.Col(
            [
                dbc.CardGroup(
                    [
                        dbc.Label("Username"),
                        dbc.Input(type="text", id="username-input"),
                    ],
                    className="mr-3",
                ),
                dbc.CardGroup(
                    [
                        dbc.Label("Password"),
                        dbc.Input(type="password", id="password-input"),
                    ],
                    className="mr-3",
                ),
                html.Br(),
                dcc.Link(
                           dbc.Button("Log in", color="primary", id="submit-button"),
                           href='/gallery'),
            ],
            width={"size": 6, "offset": 3},
            className="mb-3")
        ],
        style={"margin-top": "150px", "margin-bottom": "20px"}
    ),
])
'''
@app.callback(
    dash.dependencies.Output("login-result", "children"),
    [dash.dependencies.Input("submit-button", "n_clicks")],
    [
        dash.dependencies.State("username-input", "value"),
        dash.dependencies.State("password-input", "value"),
    ],
)
def handle_login(n_clicks, username, password):
    if username == "myusername" and password == "mypassword":
        return dbc.Alert("Login successful", color="success")
    else:
        return dbc.Alert("Invalid username or password", color="danger")

layout = html.Div([login_layout, html.Div(id="login-result")])

'''

