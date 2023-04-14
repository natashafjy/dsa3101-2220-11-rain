import dash
import dash_bootstrap_components as dbc
from flask_app import app as flask_app

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.MORPH],
                # use_pages = True,
                server=flask_app, url_base_pathname='/',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                )

app.config.suppress_callback_exceptions = True
app.title = 'my-dash-multi-page-app'