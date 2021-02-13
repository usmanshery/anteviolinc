from app import app
from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from .plots import plots

links = [
    {
        'name': 'Temporal Analysis',
        'link': '/temporal',
        'class': 'nav_link'
    },
    {
        'name': 'Islamic Calender',
        'link': '/temporal_islamic',
        'class': 'nav_link'
    },
    # {
    #     'name': 'Monthly Summary',
    #     'link': '/islamic_monthly',
    #     'class': 'nav_sublink'
    # },
    # {
    #     'name': 'Religious Events',
    #     'link': '/islamic_events',
    #     'class': 'nav_sublink'
    # },
    {
        'name': 'Prediction',
        'link': 'predict_attacker',
        'class': 'nav_link'
    },
    # {
    #     'name': 'Attacker Prediction',
    #     'link': '/predict_attacker',
    #     'class': 'nav_sublink'
    # },
    # {
    #     'name': 'Suicide Prediction',
    #     'link': '/predict_suicide',
    #     'class': 'nav_sublink'
    # },
    {
        'name': 'Exploratory Analysis',
        'link': '#',
        'class': 'nav_link'
    },
    {
        'name': 'Correlations',
        'link': '/correlation',
        'class': 'nav_sublink'
    },
]


def get_nav_bar():
    navigation_links = []
    for link in links:
        navigation_links.append(
            dbc.NavItem(
                dbc.NavLink(
                    link['name'],
                    active=True,
                    href=link['link'],
                    className=link['class']
                )
            )
        )
    return dbc.Nav(
        navigation_links,
        vertical="md",
        className="sidenav"
    )


# <ul class="sidenav nav flex-md-column">

#   <li class="nav-item"><a class="nav_link nav-link active" href="/temporal_islamic" n_clicks="0" n_clicks_timestamp="-1">Islamic Calender</a></li><li class="nav-item"><a class="nav_link nav-link active" href="predict_attacker" n_clicks="0" n_clicks_timestamp="-1">Prediction</a></li><li class="nav-item"><a class="nav_link nav-link active" href="#" n_clicks="0" n_clicks_timestamp="-1">Exploratory Analysis</a></li><li class="nav-item"><a class="nav_sublink nav-link active" href="/correlation" n_clicks="0" n_clicks_timestamp="-1">Correlations</a></li></ul>

def get_nav_bar_static():
    side_nav_string = '<ul class="sidenav nav flex-md-column">'
    for link in links:
        nav_link = '''
        <li class="nav-item">
            <a class="%s active" href="%s">
                %s
            </a>
        </li>
        ''' % (link['class'], link['link'], link['name'])
        side_nav_string += nav_link
    side_nav_string += '</ul>'
    return side_nav_string


def get_layout(correlations=False):
    if correlations:
        return html.Div([
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=plots.correlations(), config={'displayModeBar': False})
                    , className="col col-lg-8 col-md-10 col-sm-12 col-xs-12")
            ], className="justify-content-md-center")
        ])
    return html.Div(
        [
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=plots.front_page_map(), config={'displayModeBar': False})
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=plots.bar_chart(), config={'displayModeBar': False}, )
                ),
                dbc.Col(
                    dcc.Graph(figure=plots.table(), config={'displayModeBar': False}, )
                )
            ])
        ]
    )
