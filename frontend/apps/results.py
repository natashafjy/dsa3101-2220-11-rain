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
import requests

load_figure_template('MORPH')

'''
# setting up dataframe
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df_path = os.path.join(APP_PATH, os.path.join("../", "data.csv"))
def update_df():
    new_df = pd.read_csv(df_path)
    return new_df
df = update_df()
'''
# setting up Singapore basemap
#map_path = os.path.join(APP_PATH, "Singapore_basemap.json")
#with open(map_path,'r',encoding="UTF-8") as f: #3.29 encoding problem solved
#    sg_basemap = geojson.load(f)

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

### helper empty df to render default view of precipitation plot and wetness plot
empty_df = pd.DataFrame(columns = ['longitude', 'latitude', 'time', 'predicted_rain', 'P(predicted_rain > 0)'])

## layout of sidebar
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
            html.H4(id = 'results-header',
                    children = ["no routine selected"]),
    
            html.Div([
                dbc.Label('For which point?'),
                dbc.RadioItems(
                    options = [
                        {"label":"start point","value":"start"},
                        {"label":"end point", "value":"end"}
                    ],
                    value = [],
                    id = "point-checklist",
                    inline = True,
                )
            ]),

            html.Br(),
            # precipitation plot, default
            dcc.Graph(id = 'precipitation-bar',
                    figure = plot_precipitation(empty_df),
                    config = {'displayModeBar':False}),
            html.Br(),

            # wetness plot, default
            dcc.Graph(id = 'wetness-plot',
                    figure = plot_wetness(empty_df, 0),
                    config = {'displayModeBar':False}),
            html.Br(),
            
            # weather icon, default
            html.Img(id = "weather-icon", src = app.get_asset_url('humidity-2.png'), style = {'display':'inline', 'height':'10%'}),
            
            # suggestion bar, default
            html.Div(id = 'suggestion-div',
                     children = [dbc.Badge("overall suggestion", color = "primary")],
                     style = {'display':'inline-block', 'margin':'20px'}),
            
            # tips card 
            dbc.Card([]),
            html.Br(),
            html.Br(),
            dcc.Link(dbc.Button("back to routine gallery", size = "md", style = {"left":"3rem"}),href='/gallery')
            
    ]
    ,style = SIDEBAR_STYLE
    )
    return sidebar_run_model

## layout of main content
def build_main_run_model():
    '''
    2 tabs:
    tab 1: local map showing route 
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

#### subplots ####
def plot_precipitation(df):
    '''
    input: 
    df: pd DataFrame (7, 5): longtitide (float), latitude (float), time (int), predicted_rain (float), P(predicted_rain > 0) (float)

    output:
    a px.bar plot

    **** if df = empty_df, renders an empty plot
    
    '''
    

    precipitation_bar = px.bar(df, x = 'time', y = 'predicted_rain', color = 'P(predicted_rain > 0)',
                        color_continuous_scale="blues",
                        labels={'time':'minutes from now', 'P(predicted_rain > 0)':'precipitation in mm'},
                        height = 230,
                        title = "precipitation in the next 30 minutes",
                        hover_data = {'time':False})
    # precipitation_bar.update_layout(paper_bgcolor = '#f8f9fa')
    precipitation_bar.update_layout(margin = dict(t=25, b=0),
                                    hovermode = "x")
    return precipitation_bar

## helper function for plot_wetness
def determine_wetness(last_rain_end, time, predicted_rain):
    '''
    rules to decide wetness for each point of time
    if cur_prep > 0:
        wetness = 2
    else:
        if 0 < (last_rain_end + time) < 30: 2 (wet)
        if 30 < (last_rain_end + time) < 120: 1 (medium)
        if 120 < (last_rain_end + time) : 0 (dry)
    '''
    if predicted_rain > 0:
        wetness = 2
    else:
        cur_last_rain_end = last_rain_end + time
        if cur_last_rain_end <= 30:
            wetness = 2
        elif cur_last_rain_end >30 and cur_last_rain_end <= 120:
            wetness = 1
        else:
            wetness = 0
    return wetness

def plot_wetness(df, last_rain_end):
    '''
    input: 
    df: pd DataFrame (7, 5): longtitide (float), latitude (float), time (int), predicted_rain (float), P(predicted_rain > 0) (float)
    last_rain_end: last-rain-end retrived from backend /results GET request

    output:
    a px.bar plot

    **** if df = empty_df, renders an empty plot
    '''
    df[" "] = np.repeat(1, df.shape[0])
    # adding a wetness column
    
    wetness = []
    for index, row in df.iterrows():
        wetness.append(determine_wetness(last_rain_end, time = row['time'], predicted_rain = row['predicted_rain']))
    df['wetness'] = wetness 
    
    wetness_plot = px.bar(df, x = 'time', y = ' ', color ='wetness',
                        labels = {'time':'minutes from now'},
                        height = 150,
                        title = "wetness level in the next 30 minutes",
                        color_discrete_sequence=['#43CC29','#FFC008','#E52527'],
                        hover_data = {" ":False, 'time': False})
    wetness_plot.update_layout(margin = dict(t=25, b=0), 
                               hovermode = 'x')
    return wetness_plot


def build_island_map(df):
    '''
    input:
    df: pd DataFrame of shape (7*|stations|, 5), same as point pred df format, but for every station

    output:
    a px graph object: the island-wide dynamic map showing rainfall over Singapore for 30-min window,
    '''
    px.set_mapbox_access_token(mapbox_token)
    map = px.scatter_mapbox(data_frame = df, 
                     lat = "latitude",
                     lon = "longitude",
                     size = "predicted_rain",
                     # size_max = 30,
                     animation_frame = "time",
                     color_continuous_scale="blues",
                     zoom = 10.5,
                     height = 800,
                     # hover_name = "station_name",
                     hover_data = {"predicted_rain":':.2f', 
#                                    "P(predicted_rain > 0)": ':.2f',
                                   "P(predicted_rain > 0)": False,
                                   'longitude':False,
                                   'latitude': False
                                   }
                     # hover_name = ,
                     )

    # map.update_geos(fitbounds="locations")       
    return map


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

## callback to send a GET request, and fetch predictions
@app.callback(
    Output('start-pred-json','data'),
    Output('end-pred-json', 'data'),
    Output('island-pred-json','data'),
    Output('last-rain-start', 'data'),
    Output('last-rain-end', 'data'),
    Input('user-id','data'),
    Input('routine-selected-store', 'data'),
)
def fetch_prediction(username, routine_selected):
    if username and routine_selected != 'not selected':
        url_results = 'http://127.0.0.1:5001/api/results'
        routine_num = int(routine_selected[-1])
        param_results = {'username': username,'routine_num':routine_num}
        req = requests.get(url_results, params=param_results)
        req_json = req.json()
        # print(req.json, flush=True)
        return req_json['start_pred'], req_json['last_pred'], req_json['island_pred'], req_json['last_rain_start'], req_json['last_rain_end']
    else:
        return dash.no_update

## callback to switch map views with selected tab
## * for the routine chosen on the gallery page 
## >> using island_pred_json fetched from backend
@app.callback(
    Output("map-content", "children"), 
    Output('results-header', 'children'),
    Input("map-tabs", "active_tab"),
    Input('routine-selected-store', 'data'),
    Input('cur-routine-start', 'data'),
    Input('cur-routine-end', 'data'),
    Input('island-pred-json', 'data')
)

def tab_content(active_tab, routine_num, cur_routine_start, cur_routine_end, island_pred_json):
    
    header = "not selected"
    if routine_num != "not selected":
        header = f"Current routine predicted: {routine_num[-1]}"
        start_address = cur_routine_start
        end_address = cur_routine_end
        map_url = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&mode=walking&origin={start_address}&destination={end_address}"
    else:
        map_url = default_map_url

    if active_tab == "map-tab-1": 
        map = html.Div(
        id='map-container',
        children=[
            html.Iframe(
                id='map-iframe',
                src=map_url,
                width='100%',
                height='850rem'
            )
        ],
    )

        return map, header
    
    island_pred_df = pd.read_json(island_pred_json)

    if active_tab == "map-tab-2":
        return html.Div(id = "map-tab-2-div",
                        children = [
                            dcc.Graph(id="island-map", figure=build_island_map(island_pred_df))
                        ]), header

## helper function to determine weather icon
def update_weather_icon(df):
    '''
    input: point df
    output: 
    img: url of img
    str: (indicating heaviness of rain)
    '''
    if df['predicted_rain'].sum() <= 0.1:
        return app.get_asset_url('sunny.png'), 0
    elif df['predicted_rain'].sum() <= 0.2:
        return app.get_asset_url('windstorm.png'), 1
    elif df['predicted_rain'].sum() > 0.2:
        return app.get_asset_url('rainy.png'), 2

def update_suggestion_div(start_df, end_df):
    '''
    output: dbc.Badge
    '''
    start_icon, start_rain = update_weather_icon(start_df)
    end_icon, end_rain = update_weather_icon(end_df)
    # red alert
    if start_rain == 2 or end_rain == 2:
        return dbc.Badge("Warning, advised not to run!", color = "danger")
    # yellow alert
    elif start_rain == 1 or end_rain == 1:
        return dbc.Badge("Caution, slippery floor!", color = "warning")
    # green alert
    else:
        return dbc.Badge("Great, enjoy your dry run!", color = "success")

    
## callback to update sidebar for selected point
## >> using fetched result from start-pred-json, end-pred-json, last-rain-start, last-rain-end

@app.callback(
    Output(component_id='wetness-plot', component_property='figure'),
    Output(component_id='precipitation-bar', component_property='figure'),
    Output(component_id = 'weather-icon', component_property = 'src'),
    Output(component_id = 'suggestion-div', component_property = 'children'),
    Input(component_id='point-checklist', component_property='value'),
    Input('start-pred-json', 'data'),
    Input('end-pred-json', 'data'),
    Input('last-rain-start', 'data'),
    Input('last-rain-end', 'data')
)
def update_output_div(point_selected, start_pred_json, end_pred_json, last_rain_start, last_rain_end):
    '''
    point_selected: "start" or "end"
    '''
    # if no point selected: (default)
    precipitation_plot = plot_precipitation(empty_df)
    wetness_plot = plot_precipitation(empty_df)
    src = app.get_asset_url('humidity-2.png')
    suggestion_div = dbc.Badge("overall suggestion", color = "primary")
    
    # updating overall suggestion
    start_df = pd.read_json(start_pred_json)
    end_df = pd.read_json(end_pred_json)
    suggestion_div = update_suggestion_div(start_df, end_df)

    # updating plots and weather icon with point selected:
    if point_selected == "start":
        precipitation_plot = plot_precipitation(start_df)
        wetness_plot = plot_wetness(start_df, last_rain_end)
        src, start_heaviness = update_weather_icon(start_df)
    elif point_selected == "end":
        precipitation_plot = plot_precipitation(end_df)
        wetness_plot = plot_wetness(end_df, last_rain_end)
        src, end_heaviness = update_weather_icon(end_df)

    return wetness_plot, precipitation_plot, src, suggestion_div


