import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import app
from apps import results, login, gallery, add_routine,signup
from flask_app import app as flask_app



app.layout = html.Div([
    dcc.Store(id='shared-store'),
    dcc.Store(id = 'user-id'),
    dcc.Store(id = 'routine-selected-store', storage_type = 'local'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])



# Update the index
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/signup':
        return signup.layout
    elif pathname == '/gallery':
        return gallery.layout
    elif pathname == '/results':
        return results.layout
    elif pathname == '/add_routine':
        return add_routine.layout
    else:
        return 'URL not found'


if __name__ == '__main__':
    flask_app.run(debug=True, port=5000)
