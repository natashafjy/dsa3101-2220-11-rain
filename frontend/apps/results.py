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
default_map_url = "https://www.google.com/maps/embed/v1/place?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&q=Singapore"

# server = Flask(__name__)
#app = dash.Dash(__name__, 
#                external_stylesheets=[dbc.themes.MORPH],
#                # use_pages = True,
#                # server = server,
#                meta_tags=[{'name': 'viewport',
#                            'content': 'width=device-width, initial-scale=1.0'}],
#                )

load_figure_template('MORPH')

# setting up dataframe
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df_path = os.path.join(APP_PATH, os.path.join("../outputs", "data.csv"))
def update_df():
    new_df = pd.read_csv(df_path)
    return new_df
df = update_df()

# setting up Singapore basemap
map_path = os.path.join(APP_PATH, "Singapore_basemap.json")
with open(map_path,'r',encoding="UTF-8") as f: #3.29 encoding problem solved
    sg_basemap = geojson.load(f)



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
                dbc.ButtonGroup([
                    dbc.Button("M"),
                    dbc.Button("T"),
                    dbc.Button("W"),
                    dbc.Button("T"),
                    dbc.Button("F"),
                    dbc.Button("S"),
                    dbc.Button("S")
                ],
                id = "day-of-week-button",
                size = "sm")
            ]),
            html.Br(),
            html.Br(),

            # save button
            dbc.Button("save", size = "md", style = {"left":"7rem"})
            
            
        ],
        style=SIDEBAR_STYLE
    )
    return sidebar_add_routine

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
            html.H4("Choose running routine and get prediction!"),
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
            
            # precipitation bar plot
            dcc.Graph(id = 'precipitation-bar',
                    figure = plot_precipitation(station_id  = 1),
                    config={'displayModeBar': False}),
            html.Br(),

            # wetness plot
            dcc.Graph(id = 'wetness-plot',
                    figure = plot_wetness(station_id= 1),
                    config = {'displayModeBar':False}),
            html.Br(),
            
            html.Img(id = "weather-icon", src = app.get_asset_url('rainy.png'), style = {'display':'inline', 'height':'10%'}),
            # suggestion bar
            dbc.Badge("Caution, advised not to run!", color = "danger"),
            # tips card 
            dbc.Card([
            ])
            

            # dbc.Table.from_dataframe(df)
            # 
            #dbc.Table.from_dataframe(df.loc[:,["time","wetness"]], np.repeat(1, df.shape[0])], axis = 1), striped=True, bordered=True, hover=True)
    ]
    ,style = SIDEBAR_STYLE
    )
    return sidebar_run_model

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


def build_main_run_model():
    '''
    2 tabs:
    tab 1: local map showing precipitation data on each pin, 
        click each pin to see specific barplots of precipitation and wetness of ground on the left hand side.
    tab 2: dynamic island map showing precipitation across Singapore over the next 30 min window.
    '''
    main_run_model = html.Div(
        id = "main-run-model",
        children = [
            dbc.Tabs(
                        [
                            dbc.Tab(label="route map", tab_id="map-tab-1"),
                            dbc.Tab(label="island dynamic map", tab_id="map-tab-2"),
                        ],
                    id="map-tabs",
                    active_tab="map-tab-1",
                    ),
                html.Div(id="map-content"),
        ]
    )
    return main_run_model

#### sublpots ####
def plot_precipitation(station_id):
    '''
    station_id: int, the id of station for which the plot will be shown
    '''

    precipitation_bar = px.bar(df[df['station']==station_id], x = 'time', y = 'precipitation', color = 'probability',
                        color_continuous_scale="blues",
                        labels={'time':'minutes from now', 'precipitation':'precipitation in mm'},
                        height = 230,
                        title = "precipitation in the next 30 minutes")
    # precipitation_bar.update_layout(paper_bgcolor = '#f8f9fa')
    precipitation_bar.update_layout(margin = dict(t=25, b=0))
    return precipitation_bar

def plot_wetness(station_id):
    '''
    station_id: int, the id of station for which the plot will be shown
    '''
    df["dummy_col"] = np.repeat(1, df.shape[0])
    df["wetness"] = df["wetness"].astype(str)
    wetness_plot = px.bar(df[df['station']==station_id], x = 'time', y = 'dummy_col', color ='wetness',
                        labels = {'time':'minutes from now'},
                        height = 150,
                        title = "wetness level in the next 30 minutes",
                        color_discrete_sequence=['#43CC29','#FFC008','#E52527'])
    wetness_plot.update_layout(margin = dict(t=25, b=0))
    return wetness_plot

#def build_local_map(): deleted in 3.29 by Dongmen since collapse
def build_island_map():
    '''
    the island-wide dynamic map showing rainfall over Singapore for 30-min window,
    returning px graph object
    '''
    px.set_mapbox_access_token(open(".mapbox_token").read())
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


def update_map(n_clicks, start_address, end_address):
    if not start_address or not end_address:
        # Return the default map URL if no addresses are entered
        return default_map_url

    map_url = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&mode=walking&origin={start_address}&destination={end_address}"

    return map_url

#### Layout ####
layout = dbc.Row([
    dbc.Col(
        children = [
            build_sidebar_run_model()
        ],
        width = 3
    ),
    dbc.Col(
        children = [
            build_main_run_model()
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
    

#### callback ####
'''
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'
'''
@app.callback(
    Output("map-content", "children"), [Input("map-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == "map-tab-1": #Dongmen 3.29
        map = html.Div([
        html.Div([
            html.Label('Starting Address'),
            dcc.Input(
                id='start-address-input',
                type='text',
                placeholder='Enter starting address'
        ),
        html.Div(id='start-address-dropdown'),], 
        style={'width': '45%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Ending Address'),
            dcc.Input(
                id='end-address-input',
                type='text',
                placeholder='Enter ending address'
        ),
        html.Div(id='end-address-dropdown'),], 
        style={'width': '45%', 'display': 'inline-block'}),
        html.Button(
            'Submit',
            id='submit-button',
            n_clicks=0),
        html.Div(
            id='map-container',
            children=[
                html.Iframe(
                    id='map-iframe',
                    src=default_map_url,
                    width='190%',
                    height='655'
            )],
            style={
                'width': '50%',
                'float': 'left'}
            )
        ]
    )
        return map
    if active_tab == "map-tab-2":
        return html.Div(id = "map-tab-2-div",
                        children = [
                            dcc.Graph(id="island-map", figure=build_island_map())
                        ])
