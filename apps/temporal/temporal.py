from app import app
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import json
import random
import textwrap
import datetime as dt
import plotly.graph_objs as go
import pandas as pd

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
    {
        'name': 'Monthly Summary',
        'link': '/islamic_monthly',
        'class': 'nav_sublink'
    },
    {
        'name': 'Religious Events',
        'link': '/islamic_events',
        'class': 'nav_sublink'
    },
    {
        'name': 'Prediction',
        'link': '#',
        'class': 'nav_link'
    },
    {
        'name': 'Attacker Prediction',
        'link': '/predict_attacker',
        'class': 'nav_sublink'
    },
    {
        'name': 'Suicide Prediction',
        'link': '/predict_suicide',
        'class': 'nav_sublink'
    },
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
            dbc.NavItem(dbc.NavLink(link['name'], active=True, href=link['link'], className=link['class']))
        )
    return dbc.Nav(
        navigation_links,
        vertical="md",
        className="sidenav"
    )


def get_layout(islamic=False):
    if islamic:
        show_islamic_month_dropdown = 'block'
    else:
        show_islamic_month_dropdown = 'none'

    return html.Div([
        html.Div(id='global_param', children=[
                json.dumps({
                    "is_islamic": islamic,
                })
            ], style={'display': 'none'}),
        dbc.Row([
            dbc.Col(
                html.Div(
                    [
                        dcc.Dropdown(
                            id='temporal_country_dropdown',
                            multi=True,
                            value=[''],
                            placeholder='Select Countries',
                            options=[{'label': c, 'value': c}
                                     for c in sorted(terrorism['country_txt'].unique())],
                            className='dropdown'
                        )
                    ]
                ),
                className="col-lg-6 col-md-6 col-sm-12 col-xs-12"
            ),
            dbc.Col(
                html.Div(
                    [
                        dcc.Dropdown(
                            id='temporal_perpetrators_dropdown',
                            multi=True,
                            placeholder='Select Hostile Groups',
                            value=[''],
                            className='dropdown'
                        )
                    ]
                ),
                className="col-lg-6 col-md-6 col-sm-12 col-xs-12"
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    [
                        dcc.Dropdown(
                            id='temporal_weapons_dropdown',
                            multi=True,
                            placeholder='Select Weapon Types',
                            value=[''],
                            className='dropdown'
                        )
                    ]
                ),
                className="col-lg-6 col-md-6 col-sm-12 col-xs-12"
            ),
            dbc.Col(
                html.Div(
                    [
                        dcc.Dropdown(
                            id='temporal_attack_dropdown',
                            multi=True,
                            placeholder='Select Attack Types',
                            value=[''],
                            className='dropdown'
                        )
                    ]
                ),
                className="col-lg-6 col-md-6 col-sm-12 col-xs-12"
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    [
                        dcc.Dropdown(
                            id='temporal_islamic_month_dropdown',
                            multi=True,
                            placeholder='Select Islamic Months',
                            value=[''],
                            options=[{'label': c, 'value': c}
                                     for c in sorted(terrorism['islamic_month'].unique())],
                            className='dropdown'
                        )
                    ]
                ),
                className="col-lg-12 col-md-12 col-sm-12 col-xs-12",
                style={'display': show_islamic_month_dropdown}
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id='temporal_map',
                    config={'displayModeBar': False},
                ), className='col-lg-auto col-md-auto col-sm-auto col-xm-auto'
            )
        ], className='justify-content-md-center'),
        dbc.Row([
            dbc.Col([
                dcc.RangeSlider(id='temporal_year',
                                min=1970,
                                max=2016,
                                dots=True,
                                value=[2010, 2016],
                                marks={str(yr): "'" + str(yr)[2:] for yr in range(1970, 2017)}),
            ],
                className='col-lg-10 col-md-10 col-sm-10 col-xs-10'
            )
        ], className='justify-content-md-center')
    ])


terrorism = pd.read_csv(
    'gtd_data/terrorism_final.csv',
    encoding='latin-1', low_memory=False,
    usecols=['iyear', 'imonth', 'iday', 'country_txt', 'city', 'longitude', 'latitude',
             'nkill', 'nwound', 'summary', 'target1', 'gname', 'weaptype', 'attacktype','islamic_month']
)

terrorism = terrorism[terrorism['imonth'] != 0]
terrorism['day_clean'] = [15 if x == 0 else x for x in terrorism['iday']]
terrorism['date'] = [pd.datetime(y, m, d) for y, m, d in zip(terrorism['iyear'], terrorism['imonth'], terrorism['day_clean'])]


@app.callback(
    [Output('temporal_perpetrators_dropdown', 'options'),
     Output('temporal_weapons_dropdown', 'options'),
     Output('temporal_attack_dropdown', 'options')],
    [Input('temporal_country_dropdown', 'value')],
    [State('global_param', 'children')]
)
def populate_options(countries, parm_dump):
    params = json.loads(parm_dump[0])

    perpetrators = terrorism[terrorism['country_txt'].isin(countries)]['gname'].unique()
    perpetrators = [{'value': perp, 'label': perp} for perp in perpetrators]

    weapons = terrorism[terrorism['country_txt'].isin(countries)]['weaptype'].unique()
    weapons = [{'value': perp, 'label': perp} for perp in weapons]

    attacks = terrorism[terrorism['country_txt'].isin(countries)]['attacktype'].unique()
    attacks = [{'value': perp, 'label': perp} for perp in attacks]

    return perpetrators, weapons, attacks


@app.callback(
    Output('temporal_map', 'figure'),
    [
        Input('temporal_country_dropdown',       'value'),
        Input('temporal_perpetrators_dropdown',  'value'),
        Input('temporal_weapons_dropdown',       'value'),
        Input('temporal_attack_dropdown',        'value'),
        Input('temporal_islamic_month_dropdown', 'value'),
        Input('temporal_year',                   'value')],
    [State('global_param', 'children')]
)
def test_callback(countries, perpetrators, weapons, attacks, islamic_month, years, parm_dump):
    # load parameters
    params = json.loads(parm_dump[0])

    df = terrorism[
        terrorism['country_txt'].isin(countries) &
        terrorism['iyear'].between(years[0], years[1])
    ]

    if params['is_islamic']:
        df = df[df['islamic_month'].isin(islamic_month)]

    if len(perpetrators) != 0:
        if perpetrators[0] != '':
            df = df[terrorism['gname'].isin(perpetrators)]
    if len(weapons) != 0:
        if weapons[0] != '':
            df = df[terrorism['weaptype'].isin(weapons)]

    if len(attacks) != 0:
        if attacks[0] != '':
            df = df[terrorism['attacktype'].isin(attacks)]

    return {
        'data': [go.Scattergeo(lon=[x + random.gauss(0.04, 0.03) for x in df[df['country_txt'] == c]['longitude']],
                               lat=[x + random.gauss(0.04, 0.03) for x in df[df['country_txt'] == c]['latitude']],
                               name=c,
                               hoverinfo='text',
                               marker={'size': 9, 'opacity': 0.65, 'line': {'width': .2, 'color': '#cccccc'}},
                               hovertext=df[df['country_txt'] == c]['city'].astype(str) + ', ' +
                                         df[df['country_txt'] == c]['country_txt'].astype(str) + '<br>' +
                                         [dt.datetime.strftime(d, '%d %b, %Y') for d in
                                          df[df['country_txt'] == c]['date']] + '<br>' +
                                         'Perpetrator: ' + df[df['country_txt'] == c]['gname'].astype(str) + '<br>' +
                                         'Target: ' + df[df['country_txt'] == c]['target1'].astype(str) + '<br>' +
                                         'Deaths: ' + df[df['country_txt'] == c]['nkill'].astype(str) + '<br>' +
                                         'Injured: ' + df[df['country_txt'] == c]['nwound'].astype(str) + '<br><br>' +
                                         ['<br>'.join(textwrap.wrap(x, 40)) if not isinstance(x, float) else '' for x in
                                          df[df['country_txt'] == c]['summary']])
                 for c in countries],
        'layout': go.Layout(
            title='Terrorist Attacks ' + ', '.join(countries) + '  ' + ' - '.join([str(y) for y in years]),
            font={'family': 'Palatino'},
            titlefont={'size': 22},
            paper_bgcolor='#eeeeee',
            plot_bgcolor='#eeeeee',
            autosize=True,
            width=1200,
            height=650,
            geo={'showland': True, 'landcolor': '#eeeeee',
                 'countrycolor': '#cccccc',
                 'showsubunits': True,
                 'subunitcolor': '#cccccc',
                 'subunitwidth': 5,
                 'showcountries': True,
                 'oceancolor': '#eeeeee',
                 'showocean': True,
                 'showcoastlines': True,
                 'showframe': False,
                 'coastlinecolor': '#cccccc',
                 'lonaxis': {'range': [df['longitude'].min() - 1, df['longitude'].max() + 1]},
                 'lataxis': {'range': [df['latitude'].min() - 1, df['latitude'].max() + 1]}
                 })
    }
