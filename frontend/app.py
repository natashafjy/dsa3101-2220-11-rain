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
                # external_stylesheets=[dbc.themes.BOOTSTRAP],
                # use_pages = True,
                # server = server,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                )
def build_sidebar_add_routine():
    '''
    # routine drop down
	Postal-code input
	H4: Running time
	Time input 
	Which-day-of-week select
	Save button

    '''
    sidebar_add_routine = html.Div(
        id = "sidebar_add_routine",
        children = [
            dcc.Dropdown(id = "routine-dropdown",
                        options = [
                            {'label':'routine 1', 'value':"routine_1"},
                            {'label':'routine 2', 'value':'routine_2'},
                        ],
                        value = 'routine_1'
                        ),
            html.Br(),
            html.H4("let's start to write something exciting!")

        ]
    )
    return sidebar_add_routine

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
    # https://medium.com/plotly/5-awesome-tools-to-power-your-geospatial-dash-app-c71ae536750d
    
    return html.H1("Map should appear on this side.")

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
        ],
        width = 6
    ),
    dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds, 2 sec
            n_intervals=50,  # number of times the interval has passed, start at batch 50.
            disabled=True, # counter will no longer update
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