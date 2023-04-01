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
df_path = os.path.join(APP_PATH, os.path.join("../../outputs", "data.csv"))
def update_df():
    new_df = pd.read_csv(df_path)
    return new_df
df = update_df()

# tokens
mapbox_token = 'pk.eyJ1IjoiamVzc2llMTExMTIzMzMiLCJhIjoiY2xmcThma3llMWQyYTNxcXpjazk1cXp5diJ9.Ecuy-mNsqBbFeqgP9pWbcg'
gmap_key = 'AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8'
# Default map URL to display on app load
default_map_url = "https://www.google.com/maps/embed/v1/place?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&q=Singapore"

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
                
                    # postal-code input
                dbc.FormFloating(
                    id = "start-point",
                    children = [
                        dbc.Input(inputmode = "numeric", placeholder="postal code", size = "sm"),
                        dbc.Label("start point"),
                        ]
                    )
            ]),

        html.Br(),
        
        html.H5("ending point"),

        dbc.Row([
                    # postal-code input
                dbc.FormFloating(
                    id = "end-point",
                    children = [
                        dbc.Input(inputmode = "numeric", placeholder="postal code", size = "sm"),
                        dbc.Label("end point"),
                        ]
                    )   
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
                        {"label": "Mon", "value": "M"},
                        {"label": "Tue", "value": "T"},
                        {"label": "Wed", "value": "W"},
                        {"label": "Thu", "value": "Th"},
                        {"label": "Fri", "value": "F"},
                        {"label": "Sat", "value": "Sa"},
                        {"label": "Sun", "value": "Su"},
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
    main_add_routine = html.Div([
    html.Div([
        dcc.Input(
            id='start-address-input',
            type='text',
            placeholder='Enter starting address'
        ),
        html.Div(id='start-address-dropdown'),
    ], style={'width': '45%', 'display': 'inline-block'}),

    html.Div([
        dcc.Input(
            id='end-address-input',
            type='text',
            placeholder='Enter ending address'
        ),
        html.Div(id='end-address-dropdown'),
    ], style={'width': '45%', 'display': 'inline-block'}),

    html.Div(
        id='map-container',
        children=[
            html.Iframe(
                id='map-iframe',
                src=default_map_url,
                width='195%',
                height='695'
            )
        ],
        style={
            'width': '50%',
            'float': 'left',
        }
    )
])
    return main_add_routine

def get_address_options(input_value):
    if not input_value:
        return []
    gmaps = googlemaps.Client(key="AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8")
    address_results = gmaps.places_autocomplete(
        input_value,
        components={'country': 'SG'}
    )
    return [{'label': result['description'], 'value': result['description']} for result in address_results]

def update_start_address_dropdown(input_value):
    return html.Div([
        dcc.Dropdown(
            id='start-address-dropdown-list',
            options=get_address_options(input_value),
            value=""

        )
    ])

def update_end_address_dropdown(input_value):
    return html.Div([
        dcc.Dropdown(
            id='end-address-dropdown-list',
            options=get_address_options(input_value),
            value=""
        )
    ])

def calculate_route(start_address, end_address):
    gmaps = googlemaps.Client(key="AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8")
    directions_result = gmaps.directions(
        start_address,
        end_address,
        mode='walking',
        optimize_waypoints=True,
        departure_time=datetime.now()
    )
    route = directions_result[0]['legs'][0]
    return route

def update_map(start_address, end_address):
    if not start_address or not end_address:
        # Return the default map URL if no addresses are entered
        return default_map_url

    map_url = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&mode=walking&origin={start_address}&destination={end_address}"

    return map_url
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
    
