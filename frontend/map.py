import dash
from dash import html
from dash import dcc
import googlemaps
from datetime import datetime

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(
        id='start-address-input',
        type='text',
        placeholder='Enter starting address'
    ),
    dcc.Input(
        id='end-address-input',
        type='text',
        placeholder='Enter ending address'
    ),
    html.Button(
        'Submit',
        id='submit-button',
        n_clicks=0
    ),
    html.Div(
        id='map-container',
        children=[],
        style={
            'width': '50%',
            'height': '800px',
            'float': 'left'
        }
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
    dash.dependencies.Output('map-container', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('start-address-input', 'value'),
     dash.dependencies.State('end-address-input', 'value')]
)
def update_map(n_clicks, start_address, end_address):
    if not start_address or not end_address:
        return []

    map_url = f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&mode=walking&origin={start_address}&destination={end_address}"

    return [
        html.Iframe(
            id='map',
            srcDoc=f'<iframe src="{map_url}" width="100%" height="100%" style="border:0"></iframe>',
            style={'height': '100%', 'width': '100%'}
        )


    ]

if __name__ == '__main__':
    app.run_server(debug=True)
