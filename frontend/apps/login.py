import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from dash.dependencies import Input, Output, State
import requests

def before_verify():
    return dbc.Row([
        dbc.Col([
            dbc.Button("Log in", color="primary", id="login-button", n_clicks=0),
        ], width=2),
        dbc.Col([
            dcc.Link(
                dbc.Button("Sign up", color="primary", id="signup-button"), href='/signup')
        ], width=2)
    ], justify='center')

def verify_pass():
    return dbc.Row([
        dbc.Col([], width=2),
        dbc.Col(
            dcc.Link(
                dbc.Button("Click me to go!", color="primary", id="go-button", n_clicks=0),
                href='/gallery'
            ),
            width=4
        ),
        dbc.Col([], width=2)
    ], justify='center')


layout = html.Div([
    dbc.Row([
        dbc.Col(html.H2("Welcome to DryRun"),
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
                    html.Div(id = 'login-sign',children=[
                        before_verify()
                        ]),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div(id='query-results'),
                    ]),
                
            ],
            width={"size": 6, "offset": 3},
            className="mb-3")
        ],
        style={"margin-top": "150px", "margin-bottom": "20px"}
    )
])


@app.callback(
    [Output('query-results','children'),
     Output('login-sign','children'),
     Output('user-id','data')
    ],
    [Input('login-button', 'n_clicks')],
    [dash.dependencies.State('username', 'value'),
     dash.dependencies.State('password', 'value')]
)
def validate_login(n_clicks, username, password):
    if n_clicks > 0 and (not username or not password or username.strip() == '' or password.strip() == ''):
        return  html.Div(children=dbc.Alert('Please key in both username and password(without empty space)!', color='danger', duration=None)),before_verify(),""
    if username == '' or not username or password == '' or not password :
        return  html.Div(children=''),before_verify(),""
    else:
        url1 = 'http://127.0.0.1:5001/api/login'
        param1 = {'username': username, 'password':password}
        r1 = requests.get(url1, params=param1).json()
        if not r1['exist']:
            return html.Div(children=dbc.Alert('Username not exists!', color='danger', duration=None)),before_verify(),""
        elif not r1['match']:
            return html.Div(children=dbc.Alert('Invalid password!', color='danger', duration=None)),before_verify(),""
        else:
            return html.Div(children=dbc.Alert('Log-in check pass!', color='success', duration=None)),verify_pass(),username
        
