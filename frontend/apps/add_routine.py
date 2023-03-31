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

from app import app


load_figure_template('MORPH')

# setting up dataframe
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df_path = os.path.join(APP_PATH, os.path.join("../outputs", "data.csv"))
def update_df():
    new_df = pd.read_csv(df_path)
    return new_df
df = update_df()

# tokens
mapbox_token = 'pk.eyJ1IjoiamVzc2llMTExMTIzMzMiLCJhIjoiY2xmcThma3llMWQyYTNxcXpjazk1cXp5diJ9.Ecuy-mNsqBbFeqgP9pWbcg'
gmap_key = 'AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8'

# styles
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "right" :0,
    "width": "25rem", # rem is "root-em", indicates relative size to the scale of root element
    "padding": "2rem",
    "background-color": "#f8f9fa",
    # "color" : "#4A6FA5"
}

def build_sidebar_add_routine():
    '''
    routine drop down
    Postal-code input -> to do: check format is correct
    H4: Running time
    Time input -> to do: set step to 5-min
    Which-day-of-week select 
    Save button -> to do: how to set horizontal align to center (should be in style?)
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
            dcc.Link(dbc.Button("save", size = "md", style = {"left":"7rem"}),href='/gallery')
            
            
        ],
        style=SIDEBAR_STYLE
    )
    return sidebar_add_routine


def build_main_add_routine():
    '''
    displaying google maps, default shows scale of Singapore,
    zoomed in to user's vicinity when postal code is keyed in. 
    '''
    main_add_routine = html.Div(
        id = "main-add-routine",
        children = [
        
        ]
    )
    return main_add_routine


def build_local_map(start_address, end_address):
    '''
    the map in tab 1 showing rainfall near the specific route
    '''
    map_url = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&mode=walking&origin={start_address}&destination={end_address}"

    map = html.Div(
        id = "map-div",
        children = [
            html.Iframe(
                id='map',
                srcDoc=f'<iframe src="{map_url}" width="100%" height="100%" style="border:0"></iframe>',
                style={'height': '100%', 'width': '100%'}
                )
            ]
       #,style = {"left":0}         
    )
    
    return map

def build_island_map():
    '''
    the island-wide dynamic map showing rainfall over Singapore for 30-min window,
    returning px graph object
    '''
    px.set_mapbox_access_token(mapbox_token)
    map = px.scatter_mapbox(data_frame = df, 
                      #geojson = gj,
                     lat = "latitude",
                     lon = "longtitude",
                     color = "probability",
                     size = "precipitation", 
                     animation_frame = "time",
                     color_continuous_scale="blues",
                     zoom = 10.5,
                     height = 800
                     # hover_name = ,
                     )

    # map.update_geos(fitbounds="locations")       
    return map

#### Layout ####
layout = dbc.Row([
    dbc.Col(
        children = [
            build_sidebar_add_routine()
        ],
        width = 3
    ),
    dbc.Col(
        children = [
            build_main_add_routine()
        ],

        width = 9,
        style = {'margin-left':'25rem'}
    ),
    dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds, 2 sec
            n_intervals=50,  # number of times the interval has passed, start at batch 50.
            disabled=True, # created for backend model update, now switched off
        )
    ]
)
    
