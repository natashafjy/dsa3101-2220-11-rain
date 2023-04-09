import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from dash.dependencies import Input, Output, State
import requests

def before_verify():
    return dbc.Row([
        dbc.Col([], width=2),
        dbc.Col(
            dbc.Button("Submit", color="primary", id="login-button", n_clicks=0),width=4),
        dbc.Col([], width=2)
    ], justify='center')

def verify_pass():
    return dbc.Row([
        dbc.Col([], width=2),
        dbc.Col(
            dcc.Link(
                dbc.Button("Back to log-in page", color="primary", id="go-button", n_clicks=0),
                href='/'
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
                    html.Div(id = 'signup',children=[
                        before_verify()
                        ]),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div(id='query-results-signup'),
                    ]),
                
            ],
            width={"size": 6, "offset": 3},
            className="mb-3")
        ],
        style={"margin-top": "150px", "margin-bottom": "20px"}
    )
])


@app.callback(
    #[Output('alert-container', 'children'),
    #    Output('url', 'pathname')],

    [Output('query-results-signup','children'),
    Output('signup','children')
    ],
    [Input('login-button', 'n_clicks')],
    [dash.dependencies.State('username', 'value'),
     dash.dependencies.State('password', 'value')]
)
def sign_up(n_clicks, username, password):
    if n_clicks > 0 and (username == '' or not username or password == '' or not password):
        return  html.Div(children=dbc.Alert('Please key in both username and password!', color='danger', duration=None)),before_verify()
    if username == '' or not username or password == '' or not password:
        return  html.Div(children=''),before_verify()
    else:
        url1 = 'http://127.0.0.1:5001/api/signup'
        param1 = {'username': username, 'password':password}
        r1 = requests.post(url1, params=param1).json()
        if not r1['exist']:
            return html.Div(children=dbc.Alert('Sign-up check pass!', color='success', duration=None)),verify_pass()
        else:
            return html.Div(children=dbc.Alert('Username already exists!', color='danger', duration=None)),before_verify()
    
