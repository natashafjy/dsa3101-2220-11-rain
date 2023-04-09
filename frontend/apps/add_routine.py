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
import requests

from geopy.geocoders import GoogleV3
load_figure_template('MORPH')

# setting up dataframe
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df_path = os.path.join(APP_PATH, os.path.join("../", "data.csv"))
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

api_key = 'AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8'
def get_location(address):
    geolocator = GoogleV3(api_key=api_key)
    location = geolocator.geocode(address, components={'country': 'SG'})
    latitude = location.latitude
    longtitude = location.longitude
    return[latitude,longtitude]

def build_sidebar_add_routine():
    '''
    end-time > start-time
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
                        ]
                    ),

            html.Br(),

            html.Div([
                dbc.Label("choose end point of route"),
                dcc.Dropdown(id='end-address-dropdown',
                            optionHeight=50)]),
            html.Br(),
            # running time input
            html.H5("Running Time"),
            dbc.Row([
                # start-time input
                    html.Div([
                        dbc.Label("start"),
                        dbc.Input(
                            id = "start-time-input",
                            type = "Time",
                            step = 300),
                        dbc.FormText("to the nearest 5-min"),
                        dbc.FormFeedback("start time before end time", type = "valid"),
                        dbc.FormFeedback("start time cannot be later than end time", type = "invalid")
                    ]),
              
                # end-time input
                    html.Div([
                        dbc.Label("End"),
                        dbc.Input(
                            id = "end-time-input",
                            type = "Time",
                            step = 300),
                    ])
                    
            ]),
            html.Br(),

            # which-day-of-the-week button group
            html.Div([
                dbc.Label("which days of the week?"),
                dbc.Checklist(
                    options=[
                        {"label": "Mon", "value": "Mon "},
                        {"label": "Tue", "value": "Tue "},
                        {"label": "Wed", "value": "Wed "},
                        {"label": "Thu", "value": "Thu "},
                        {"label": "Fri", "value": "Fri "},
                        {"label": "Sat", "value": "Sat "},
                        {"label": "Sun", "value": "Sun "},
                    ],
                    value=["Mon ", "Tue ", "Wed ", "Thu ", "Fri ", "Sat ", "Sun "],
                    id="day-of-week-checklist",
                    inline=True
                )
            ]),
            html.Br(),
            html.Br(),

            # save button
            html.Div(id='save-action',children = dbc.Button("save", size = "md", id="save-button", n_clicks=0,style = {"left":"7rem"})),
            html.Br(),
            html.Br(),
            html.Div(id='save-results')
            
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

## callback to update routine_list
@app.callback(
    #[Output('alert-container', 'children'),
    #    Output('url', 'pathname')],

    [
    Output('save-results','children'),
    Output('save-action','children')
    ],
    [Input('save-button', 'n_clicks'),
     Input('user-id', 'data')],

    [dash.dependencies.State('start-address-dropdown', 'value'),
     dash.dependencies.State('end-address-dropdown', 'value'),
     dash.dependencies.State('start-time-input', 'value'),
     dash.dependencies.State('end-time-input', 'value'),
     dash.dependencies.State('day-of-week-checklist', 'value'),]
)

def save_routine(n_clicks,user_name,start_address, end_address, start_time, end_time, days_of_week):
    if n_clicks == 0:
        raise PreventUpdate

    if not (start_address and end_address and start_time and end_time and days_of_week):
        return html.Div(children=dbc.Alert('Please fill in all the inputs!', color='warning', duration=None)), dbc.Button("save", size = "md", id="save-button", n_clicks=0,style = {"left":"7rem"})
    if start_time > end_time or start_time[-1] not in ['0','5'] or end_time[-1] not in ['0','5']:
        return html.Div(children=dbc.Alert('Please check input format', color='warning', duration=None)), dbc.Button("save", size = "md", id="save-button", n_clicks=0,style = {"left":"7rem"})


    start_lat,start_long = get_location(start_address)
    end_lat,end_long = get_location(end_address)        
    param = {'username':user_name,
             'start_address': start_address,
             'start_long':start_long,
             'start_lat':start_lat,
             'end_address': end_address,
             'end_long':end_long,
             'end_lat':end_lat,
             'start_time': start_time,
             'end_time': end_time,
             'days_of_week': days_of_week
             }

    url_add_routine = 'http://127.0.0.1:5001/api/add_routine'
    req = requests.post(url_add_routine, params = param)
    return html.Div(children=dbc.Alert('Save successful!', color='success', duration=None)),dcc.Link(dbc.Button("Click to gallery!", color="primary"),href='/gallery')

## callback to check start-time is before end-time 
@app.callback(
    Output('start-time-input', 'invalid'),
    Output('start-time-input', 'valid'),
    Output('end-time-input', 'invalid'),
    Output('end-time-input', 'valid'),
    Input('start-time-input','value'),
    Input('end-time-input','value')
)
def validate_input_time(start_time, end_time):
    if start_time and end_time: # both has inputs
        start_before_end =  (start_time <= end_time) # = True if start before end
        return not start_before_end, start_before_end, not start_before_end, start_before_end 
    else: 
        return False, False, False, False

        

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
    
