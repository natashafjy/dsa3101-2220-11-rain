import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from dash.dependencies import Input, Output, State
from shared import user_dict
##app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

def add_user(name,pw):
    user_dict[name] = pw

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
                dbc.Button("Back to log-in page", color="primary", id="login-button", n_clicks=0),
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
def validate_login(n_clicks, username, password):
    global user_dict
    if username == '' or not username or password == '' or not password:
            return  html.Div(children=''),before_verify()
    if username not in user_dict:
        user_dict[username] = password
        return html.Div(children=dbc.Alert('Sign-up check pass!', color='success', duration=None)),verify_pass()
    else:
        return html.Div(children=dbc.Alert('Username already exists!', color='danger', duration=None)),before_verify()
    
