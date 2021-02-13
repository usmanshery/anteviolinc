import dash
from dash import Dash
import dash_bootstrap_components as dbc

external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
    dbc.themes.BOOTSTRAP,

]

external_scripts = [
    'https://code.jquery.com/jquery-3.4.1.min.js',
]

app: Dash = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

# config
server = app.server
app.config.suppress_callback_exceptions = True

