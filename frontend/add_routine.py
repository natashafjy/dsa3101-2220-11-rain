import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

import googlemaps
import geojson

import os
import pathlib

from app import *

# server = Flask(__name__)
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.MORPH],
                # use_pages = True,
                # server = server,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                )

load_figure_template('MORPH')

def build_sidebar_add_routine():
    '''
    routine drop down
	Postal-code input -> to do: check format is correct
	H4: Running time
	Time input -> to do: set step to 5-min
	Which-day-of-week select 
	Save button -> to do: how to set horizontal align to center (should be in style?)

    '''

    '''
    @gallery
    routine logic:

    If the user does not have a routine yet -> 
        they can add a routine -> 
        map automatically zooms into their postal code ->
        input info is saved and sent to backend for the user ->
        'Select a routine' dropdown is activated


    If the user has added a routine before -> 
        they can add a routine OR
        they can directly access the routine dropdown and select a routine
    '''


    sidebar_add_routine = html.Div(
        id = "sidebar-add-routine",
        children = [
            html.H4("Set-up your running routine!"),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    # postal-code input
                    dbc.FormFloating(
                        children = [
                            dbc.Input(id="postal-code", inputmode = "numeric", placeholder="postal code", size = "sm"),
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
                            dbc.DropdownMenuItem("Routine 1", href="http://127.0.0.1:3100/")
                            ],
                        )
                ])
            ]),
            
            html.Br(),
            html.Br(),
            # running time input
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
            ]),
            html.Br(),

            # which-day-of-the-week button group
            html.Div([
                dbc.Label("which days of the week?"),
                dbc.Checklist(
                    options=[
                        {"label": "M", "value": "M"},
                        {"label": "T", "value": "T"},
                        {"label": "W", "value": "W"},
                        {"label": "T", "value": "Th"},
                        {"label": "F", "value": "F"},
                        {"label": "S", "value": "Sa"},
                        {"label": "S", "value": "Su"},
                    ],
                    value=["M", "T", "W", "Th", "F", "Sa", "Su"],
                    id="day-of-week-checklist",
                    inline=True
                )
            ]),
            html.Br(),
            html.Br(),

            # save button
            dbc.Button("save", size = "md", style = {"left":"7rem"})
            
            
        ],
        style=SIDEBAR_STYLE
    )
    return sidebar_add_routine

app.layout = dbc.Row([
    dbc.Col(
        children = [
            build_sidebar_add_routine()
        ],
        width = 3
    ),
    # dbc.Col(
    #     children = [
    #         build_main_run_model()
    #     ],

    #     width = 9,
    #     style = {'margin-left':'25rem'}
    # ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=3101)