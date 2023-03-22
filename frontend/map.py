import dash
from dash import html
from dash import dcc
import googlemaps
import googlemaps.exceptions
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(
        id='address-input',
        type='text',
        placeholder='Enter an address'
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
            'width': '100%',
            'height': '800px'
        }
    )
])


@app.callback(
    dash.dependencies.Output('map-container', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('address-input', 'value')]
)
def update_map(n_clicks, address):
    if not address:
        return []

    load_dotenv(find_dotenv())
    gmaps = googlemaps.Client(key="AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8")
    geocode_result = gmaps.geocode(address)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return [
        html.Iframe(
            id='map',
            srcDoc=f'<iframe src="https://www.google.com/maps/embed/v1/place?q={address}&key=AIzaSyCMhkDTjNOXAlgNL3FijjPIw6c7VGvI0f8&zoom=15 width="100%" height="100%"></iframe>',
            style={'height': '100%', 'width': '100%'}
        )
    ]

if __name__ == '__main__':
    app.run_server(debug=True)
