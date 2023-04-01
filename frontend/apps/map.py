import dash
from dash import html
from dash import dcc
import googlemaps
from datetime import datetime
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

# Default map URL to display on app load
default_map_url = "https://www.google.com/maps/embed/v1/place?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&q=Singapore"

app.layout = html.Div([
    html.Div([
        html.Label('Starting Address'),
        dcc.Input(
            id='start-address-input',
            type='text',
            placeholder='Enter starting address'
        ),
        html.Div(id='start-address-dropdown'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Ending Address'),
        dcc.Input(
            id='end-address-input',
            type='text',
            placeholder='Enter ending address'
        ),
        html.Div(id='end-address-dropdown'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Button(
        'Submit',
        id='submit-button',
        n_clicks=0
    ),
    html.Div(
        id='map-container',
        children=[
            html.Iframe(
                id='map-iframe',
                src=default_map_url,
                width='100%',
                height='655'
            )
        ],
        style={
            'width': '50%',
            'float': 'left'
        }
    )
])

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
            value=''
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
            value='',
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
    [Input('submit-button', 'n_clicks')],
    [State('start-address-dropdown-list', 'value'),
     State('end-address-dropdown-list', 'value')]
)
def update_map(n_clicks, start_address, end_address):
    if not start_address or not end_address:
        # Return the default map URL if no addresses are entered
        return default_map_url

    map_url = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&mode=walking&origin={start_address}&destination={end_address}"

    return map_url

if __name__ == '__main__':
    app.run_server(debug=False)
