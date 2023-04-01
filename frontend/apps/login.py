import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from dash.dependencies import Input, Output, State
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
                        dbc.Input(type="text", id="username",debounce = True),
                    ],
                    className="mr-3",
                ),
                dbc.CardGroup(
                    [
                        dbc.Label("Password"),
                        dbc.Input(type="password", id="password",debounce = True),
                    ],
                    className="mr-3",
                ),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Log in", color="primary", id="login-button",n_clicks=0)
                        ]),
                    dbc.Col([
                        dcc.Link(
                           dbc.Button("Sign up", color="primary", id="signup-button"),
                           href='/signup')
                        ]),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div(id='query-results'),
                    #dcc.Location(id='url', refresh=False)
                    ]),
                
            ],
            width={"size": 6, "offset": 3},
            className="mb-3")
        ],
        style={"margin-top": "150px", "margin-bottom": "20px"}
    )
])

#layout = html.Div([login_layout, html.Div(id="login-result")])

@app.callback(
    #[Output('alert-container', 'children'),
    #    Output('url', 'pathname')],
    Output('query-results','children'),
    [Input('login-button', 'n_clicks')],
    [dash.dependencies.State('username', 'value'),
     dash.dependencies.State('password', 'value')]
)
def validate_login(n_clicks, username, password):
    li = {'amy':'pw'}
    if username == '' or not username or password == '' or not password:
            return  html.Div(children='')
    if username not in li:
        return html.Div(children=dbc.Alert('User name not exists!', color='danger', duration=None))
    if li[username]==password:
        return html.Div(dcc.Link('Access Granted!', href='/gallery'))
    else:
        return html.Div(children=dbc.Alert('Invalid password', color='danger', duration=None))