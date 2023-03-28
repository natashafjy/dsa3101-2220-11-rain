import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import app
from apps import results, login, gallery


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


# Update the index
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/login':
        return login.layout
    elif pathname == '/':
    	return login.layout
    elif pathname == '/gallery':
        return gallery.layout
    elif pathname == '/results':
        return results.layout
    else:
        return 'URL not found'


if __name__ == '__main__':
    app.run_server(debug=True)
