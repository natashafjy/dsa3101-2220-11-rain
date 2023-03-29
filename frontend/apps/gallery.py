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

import os
import pathlib

from app import app


load_figure_template('MORPH')
# setting up dataframe
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df_path = os.path.join(APP_PATH, os.path.join("../outputs", "data.csv"))

def update_df():
    new_df = pd.read_csv(df_path)
    return new_df
df = update_df()


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
    # Img weather icon
	Rain bar graph -> to-do: change legend to 0, 5, 10..., 30
	Wetness indicator -> to-do: look for plots other than bar plots to visualise this, change legend
	Suggestion-bar -> to-do: adjust spacing in between
	Span: (text) summary, tips etc 

    '''
    sidebar_run_model = html.Div(
        id = "sidebar-run-model",
        children = [
            html.H4("Choose existing rootine or add new routine!"),
            # drop-down to select routine
            dbc.DropdownMenu(
                        id = "routine-dropdown-2",
                        label = "routine",
                        children = [
                            dbc.DropdownMenuItem("Select a routine", header = True),
                            dbc.DropdownMenuItem("Routine 1"),
                            dbc.DropdownMenuItem("Routine 2")
                            ],
                        ),
            html.Br(),
           	
           	dbc.Row([
                # postal-code input
                dbc.FormFloating(
                    id = "postal-code-input",
                    children = [
                        dbc.Input(inputmode = "numeric", placeholder="postal code", size = "sm"),
                        dbc.Label("postal code"),
                        ]
                    )   
            
        
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
            ]),
            html.Br(),

            # which-day-of-the-week button group
            html.Div([
                dbc.Label("running days of the week!"),
                dbc.ButtonGroup([
                    dbc.Button("1"),
                    dbc.Button("2"),
                    dbc.Button("3"),
                    dbc.Button("4"),
                    dbc.Button("5"),
                    dbc.Button("6"),
                    dbc.Button("7")
                ],
                id = "day-of-week-button",
                size = "sm")
            ]),
            html.Br(),
            html.Br(),
            

            # save button

            dcc.Link(dbc.Button("go to current prediction page", size = "md", style = {"left":"1rem"}),href = '/results'),
            html.Br(),
            html.Br(),
            dcc.Link(dbc.Button("add new routine", size = "md", style = {"left":"1rem"}),href = '/add_routine'),

            # tips card 
            dbc.Card([
            ])
            

            # dbc.Table.from_dataframe(df)
            # 
            #dbc.Table.from_dataframe(df.loc[:,["time","wetness"]], np.repeat(1, df.shape[0])], axis = 1), striped=True, bordered=True, hover=True)
    ],
    style = SIDEBAR_STYLE)
    return sidebar_run_model

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
layout = dbc.Row([
    dbc.Col(
        children = [
            build_sidebar_run_model()
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



