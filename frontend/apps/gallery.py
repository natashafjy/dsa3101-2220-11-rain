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
           	
           	dbc.Row([
                # postal-code input
                dbc.Label("routine postal code"),
                html.Div(
                    id = 'postal-code-output', 
                    children = [])
                    
            
        
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
            html.Div(
                id = "day-of-week-div",
                children = [
                dbc.Label("running days of the week"),
                dbc.ButtonGroup([
                    dbc.Button(id = "mon", children = "1"),
                    dbc.Button(id = "tues", children = "2"),
                    dbc.Button(id = "wed",children = "3"),
                    dbc.Button(id = "thur",children = "4"),
                    dbc.Button(id = "fri",children = "5"),
                    dbc.Button(id = "sat",children = "6"),
                    dbc.Button(id = "sun",children = "7")
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
    return sidebar_gallery

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
            build_sidebar_gallery()
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

# @app.callback(
#     Output(component_id='routine-dropdown-3', component_property='value'),
#     Input(component_id='routine-dropdown-3', component_property='label')
# )
# def update_dropdown_header(input_value):
#     return input_value

@app.callback(
    Output('gallery-title', 'children'),
    Output('postal-code-output', 'children'),
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
    postal_code = " "
    start_time_value = ""
    start_time_disabled = False
    end_time_value = ""
    end_time_disabled = False
    # if there is any routine selected
    if selected_routine != 0:
        gallery_title = f'Current routine selected is {selected_routine}'

    if selected_routine == "1":
        postal_code = "138600, UTown Residence"
        start_time_value = '12:00'
        start_time_disabled = True
        end_time_value = '12:30'
        end_time_disabled = True
    
    if selected_routine == "2":
        postal_code = "141080, Alexandra Canal Linear Park"
        start_time_value = '18:00'
        start_time_disabled = True
        end_time_value = '18:30'
        end_time_disabled = True

    return gallery_title, postal_code, start_time_value, start_time_disabled,end_time_value, end_time_disabled

@app.callback(
    Output("day-of-week-div", 'children'),
    Input('routine-dropdown-3', 'value')
)
def update_weekday_button_group_info(selected_routine):
    if selected_routine == "1":
        return "Days of week: Tuesday, Thursday, Friday"
    if selected_routine == "2":
        return "Days of week: Monday, Wednesday, Friday"

