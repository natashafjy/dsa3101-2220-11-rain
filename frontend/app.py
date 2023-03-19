import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# server = Flask(__name__)
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.MORPH],
                # use_pages = True,
                # server = server,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                )
def build_sidebar_add_routine():
    '''
    routine drop down
	Postal-code input -> to do: check format is correct
	H4: Running time
	Time input -> to do: set step to 5-min
	Which-day-of-week select
	Save button

    '''
    sidebar_add_routine = html.Div(
        id = "sidebar_add_routine",
        children = [
            html.H4("Set-up your running routine!"),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    # postal-code input
                    dbc.FormFloating(
                        id = "postal-code-input",
                        children = [
                            dbc.Input(inputmode = "numeric", placeholder="postal code", size = "sm"),
                            dbc.Label("postal code"),
                            ]
                        )   
                ]),
                dbc.Col([
                    # routine drop-down
                    dbc.DropdownMenu(
                        id = "routine-dropdown",
                        label = "routine",
                        children = [
                            dbc.DropdownMenuItem("Select a routine", header = True),
                            dbc.DropdownMenuItem("Routine 1"),
                            dbc.DropdownMenuItem("Routine 2")
                            ],
                        )
                ])
                
            ]),
            
            html.Br(),
            html.Br(),
            html.H5("Running Time"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Label("start"),
                        dbc.Input(
                            id = "start-time-input",
                            type = "Time")
                        # ,dbc.FormText("starting time")
                    ])
                ]),
                dbc.Col(
                    html.Div([
                        dbc.Label("End"),
                        dbc.Input(
                            id = "end-time-input",
                            type = "Time")
                    ])
                    
                )
            ])
            

        ],
        style=SIDEBAR_STYLE
    )
    return sidebar_add_routine

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem", # rem is "root-em", indicates relative size to the scale of root element
    "padding": "2rem",
    "background-color": "#f8f9fa",
    # "color" : "#4A6FA5"
}

def build_sidebar_run_model():
    '''
    Routine dropdown
	Row
		Img weather icon
		Rain bar graph
	Wetness indicator
	Suggestion-bar
	Span: (text) summary, tips etc 

    '''
def build_map():
    map = html.Div(
        id = "map-div",
        children = [
            html.H4("Map should appear on this side.")
        ],
        style = {"left":0}         
    )
    
    return map

#### Layout ####
app.layout = dbc.Row([
    dbc.Col(
        children = [
            build_sidebar_add_routine()
        ]
    ),
    dbc.Col(
        children = [
            build_map()
        ]
    ),
    dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds, 2 sec
            n_intervals=50,  # number of times the interval has passed, start at batch 50.
            disabled=True, # created for backend model update, now switched off
        )
    ]
)
    

#### callback ####
'''
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'
'''




if __name__ == '__main__':
    app.run_server(debug=True) 