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

# server = Flask(__name__)
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.MORPH],
                # use_pages = True,
                # server = server,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                )

load_figure_template('MORPH')
# setting up dataframe
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df_path = os.path.join(APP_PATH, os.path.join("../outputs", "data.csv"))

def update_df():
    new_df = pd.read_csv(df_path)
    return new_df
df = update_df()

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
                    figure = plot_precipitation(),
                    config={'displayModeBar': False}),
            html.Br(),

            # wetness plot
            dcc.Graph(id = 'wetness-plot',
                    figure = plot_wetness(),
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
    ],
    style = SIDEBAR_STYLE)
    return sidebar_run_model

def plot_precipitation():
    precipitation_bar = px.bar(df, x = 'time', y = 'precipitation', color = 'probability',
                        color_continuous_scale="blues",
                        labels={'time':'minutes from now', 'precipitation':'precipitation in mm'},
                        height = 230,
                        title = "precipitation in the next 30 minutes")
    # precipitation_bar.update_layout(paper_bgcolor = '#f8f9fa')
    precipitation_bar.update_layout(margin = dict(t=25, b=0))
    return precipitation_bar

def plot_wetness():
    df["dummy_col"] = np.repeat(1, df.shape[0])
    df["wetness"] = df["wetness"].astype(str)
    wetness_plot = px.bar(df, x = 'time', y = 'dummy_col', color ='wetness',
                        labels = {'time':'minutes from now'},
                        height = 150,
                        title = "wetness level in the next 30 minutes",
                        color_discrete_sequence=['#43CC29','#FFC008','#E52527'])
    wetness_plot.update_layout(margin = dict(t=25, b=0))
    return wetness_plot

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
app.layout = dbc.Row([
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




if __name__ == '__main__':
    app.run_server(debug=True) 