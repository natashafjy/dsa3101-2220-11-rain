import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.exceptions import PreventUpdate

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
            html.Div([
                dbc.Label("choose start point of route"),
                dcc.Dropdown(id='start-address-dropdown',
                                     optionHeight=50)
                # address input
                # dbc.FormFloating(
                #     id = "start-point",
                #     children = [
                        # dbc.Input(id = "start-address-input",
                        #           inputmode = "text", 
                        #           # placeholder="postal code", 
                        #           size = "sm"),
                        # 
                        
                        ]
                    ),

            html.Br(),

            html.Div([
                dbc.Label("choose end point of route"),
                dcc.Dropdown(id='end-address-dropdown',
                            optionHeight=50)]),

        # html.Div([
        #         # postal-code input
        #         dbc.FormFloating(
        #             id = "end-point",
        #             children = [
        #                 dbc.Input(id = "end-address-input",
        #                           inputmode = "text", 
        #                           # placeholder="postal code", 
        #                           size = "sm"),
        #                 dbc.Label("choose end point of route"),
        #                 ]
        #             ),
        #         html.Div(id='end-address-dropdown'),
                   
        #     ]),
            
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
    main_add_routine = html.Div(
        id='map-container',
        children=[
            html.Iframe(
                id='map-iframe',
                src=default_map_url,
                width='100%',
                height='850rem'
            )
        ],
        # style={
        #     'width': '50%',
        #     'float': 'left',
        # }
    )

    return main_add_routine

## callback to update *start* address dropdown when filled in
@app.callback(
    Output('start-address-dropdown', 'options'),
    Input('start-address-dropdown', 'search_value')
)
def update_start_address_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in get_address_options(search_value) if search_value.lower() in o["label"].lower()]

## callback to update *end* address dropdown when filled in
@app.callback(
    Output('end-address-dropdown', 'options'),
    Input('end-address-dropdown', 'search_value')
)
def update_end_address_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in get_address_options(search_value) if search_value.lower() in o["label"].lower()]

##>> helper function for the 2 callbacks above: 
def get_address_options(input_value):
    if not input_value:
        return []
    gmaps = googlemaps.Client(key="AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8")
    address_results = gmaps.places_autocomplete(
        input_value,
        components={'country': 'SG'}
    )
    return [{'label': result['description'], 'value': result['description']} for result in address_results]


## callback to update Google map frame once start_address and end_address are filled
@app.callback(
    Output('map-iframe', 'src'),
    [Input('start-address-dropdown', 'value'),
     Input('end-address-dropdown', 'value')]
)
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
    
