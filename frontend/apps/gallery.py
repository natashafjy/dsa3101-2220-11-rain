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
# Default map URL to display on app load
default_map_url = "https://www.google.com/maps/embed/v1/place?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&q=Singapore"
# setting up dataframe
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df_path = os.path.join(APP_PATH, os.path.join("../../outputs", "data.csv"))

def update_df():
    new_df = pd.read_csv(df_path)
    return new_df
df = update_df()


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24.3rem", # rem is "root-em", indicates relative size to the scale of root element #Change to 24.2 to reduce gap 3.31
    "padding": "2rem",
    "background-color": "#f8f9fa"
    # "color" : "#4A6FA5"
}

def build_sidebar_gallery():
    '''
    Routine dropdown 
    # Img weather icon
	Rain bar graph -> to-do: change legend to 0, 5, 10..., 30
	Wetness indicator -> to-do: look for plots other than bar plots to visualise this, change legend
	Suggestion-bar -> to-do: adjust spacing in between
	Span: (text) summary, tips etc 

    '''
    sidebar_gallery = html.Div(
        id = "sidebar-gallery",
        children = [
            html.H4(id = "gallery-title", children = "Choose a existing routine or add a new routine!"),
            # drop-down to select routine
            dbc.Select(
                id = "routine-dropdown-3",
               # value = 'select a routine',
                options = [
                    {'label':'Routine 1', 'value':1},
                    {'label':'Routine 2', 'value':2}
                ],
                value = 0

        
            ),
            # dbc.DropdownMenu(
            #             id = "routine-dropdown-2",
            #             label = "routine",
            #             children = [
            #                 dbc.DropdownMenuItem("Select a routine", header = True),
            #                 dbc.DropdownMenuItem(id = "dropdownItem1",label = "Routine 1"),
            #                 dbc.DropdownMenuItem("Routine 2")
            #                 ],
            #             ),
            html.Br(),
           	
            html.H5("Starting point"),
           	dbc.Row([
                # postal-code input
                #dbc.Label("routine postal code"),
                html.Div(
                    id = 'starting-point', 
                    children = [])
                    
            
        
            ]),

            html.Br(),
            html.H5("Ending point"),
            dbc.Row([
                # postal-code input
                #dbc.Label("routine postal code"),
                html.Div(
                    id = 'ending-point', 
                    children = [])
                    
            
        
            ]),

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
            html.H5("Days of week"),
            html.Div(
                id = "day-of-week-div",
                children = [
                dbc.Label("running days of the week"),
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
    return sidebar_gallery

def build_map(): #Dongmen 3.29
    map = html.Div([
    html.Div([
        html.Label('Starting Address'),
        dcc.Input(
            id='start-address-input',
            type='text',
            placeholder='Enter starting address'
        ),
        html.Div(id='start-address-dropdown'),
    ], style={'width': '45%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Ending Address'),
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

@app.callback(
    Output('start-address-dropdown', 'children'),
    [Input('start-address-input', 'value')]
)
def update_start_address_dropdown(input_value):
    return html.Div([
        dcc.Dropdown(
            id='start-address-dropdown-list',
            options=get_address_options(input_value),
            value=""

        )
    ])

@app.callback(
    Output('end-address-dropdown', 'children'),
    [Input('end-address-input', 'value')]
)
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

@app.callback(
    Output('map-iframe', 'src'),
    [Input('start-address-dropdown-list', 'value'),
     Input('end-address-dropdown-list', 'value')]
)
def update_map(start_address, end_address):
    if not start_address or not end_address:
        # Return the default map URL if no addresses are entered
        return default_map_url

    map_url = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&mode=walking&origin={start_address}&destination={end_address}"

    return map_url
#Dongmen

#### Layout ####
layout = dbc.Row([
    dbc.Col(
        children = [
            build_sidebar_gallery()
        ],
        width = 3 #Adding width to fit the map 3.31

    ),
    dbc.Col(
        children = [
            build_map()
        ],
        width = 9
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

# @app.callback(
#     Output(component_id='routine-dropdown-3', component_property='value'),
#     Input(component_id='routine-dropdown-3', component_property='label')
# )
# def update_dropdown_header(input_value):
#     return input_value

@app.callback(
    Output('gallery-title', 'children'),
    Output('starting-point', 'children'),
    Output('ending-point','children'),
    Output('start-time-input', 'value'),
    Output('start-time-input', 'disabled'),
    Output('end-time-input', 'value'),
    Output('end-time-input', 'disabled'),
    Input('routine-dropdown-3', 'value')
)
def update_routine_info(selected_routine):
    '''
    selected_routine: int, 1,2
    '''
    gallery_title = "Choose an existing routine or add a new routine!"
    start_point = " "
    end_point = " "
    start_time_value = ""
    start_time_disabled = False
    end_time_value = ""
    end_time_disabled = False
    # if there is any routine selected
    if selected_routine != 0:
        gallery_title = f'Current routine selected is {selected_routine}'

    if selected_routine == "1":
        start_point = "138600, UTown Residence"
        end_point = "126754, 103 West Coast Vale"
        start_time_value = '12:00'
        start_time_disabled = True
        end_time_value = '12:30'
        end_time_disabled = True
    
    if selected_routine == "2":
        start_point = "141080, Alexandra Canal Linear Park"
        end_point = "138600, UTown Residence"
        start_time_value = '18:00'
        start_time_disabled = True
        end_time_value = '18:30'
        end_time_disabled = True

    return gallery_title, start_point, end_point,start_time_value, start_time_disabled,end_time_value, end_time_disabled

@app.callback(
    Output("day-of-week-div", 'children'),
    Input('routine-dropdown-3', 'value')
)
def update_weekday_button_group_info(selected_routine):
    if selected_routine == "1":
        return "Tuesday, Thursday, Friday"
    if selected_routine == "2":
        return "Monday, Wednesday, Friday"

