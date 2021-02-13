from builtins import classmethod

from app import app
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

terrorism = pd.read_csv("gtd_data/globalterrorismdb_0718dist.csv",
                        usecols=['country_txt', 'iyear', 'imonth', 'provstate', 'city', 'suicide', 'attacktype1',
                                 'attacktype1_txt', 'attacktype2', 'targtype1', 'targtype1_txt', 'targsubtype1',
                                 'gname', 'nperps', 'weaptype1_txt', 'weaptype1', 'weapsubtype1', 'nkill', 'nwound',
                                 'property', 'multiple'])
terrorism = terrorism[terrorism['country_txt'] == 'Pakistan']
terrorism = terrorism[terrorism['gname'] != 'Unknown']
terrorism = terrorism.drop(columns='country_txt')


def get_layout():
    return html.Div([
        html.Div(id='global_param', children=[
            json.dumps({
            })
        ], style={'display': 'none'}),
        dbc.Row([
            dbc.Col(html.H1('Select Province/ State/ City:')),
            dbc.Col(html.H1('Select Attack Type:'))
        ]),

        dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='suc_pr_provstate',
                             multi=False,
                             placeholder='Select Province/State/City',
                             options=[{'label': c, 'value': c}
                                      for c in sorted(terrorism['provstate'].unique())],
                             )),
            dbc.Col(
                dcc.Dropdown(id='suc_pr_attacktype',
                             multi=False,
                             placeholder='Select Attack Type',
                             options=[{'label': c, 'value': c}
                                      for c in sorted(terrorism['attacktype1_txt'].unique())],
                             )
            )
        ]),

        dbc.Row([
            dbc.Col(html.H1('Select Target Type:')),
            dbc.Col(html.H1('Select Weapon Type:'))
        ]),

        dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='suc_pr_targettype',
                             multi=False,
                             placeholder='Select Target Type',
                             options=[{'label': c, 'value': c}
                                      for c in sorted(terrorism['targtype1_txt'].unique())],
                             )),
            dbc.Col(
                dcc.Dropdown(id='suc_pr_weapontype',
                             multi=False,
                             placeholder='Select Weapon Type',
                             options=[{'label': c, 'value': c}
                                      for c in sorted(terrorism['weaptype1_txt'].unique())],
                             ))
        ]),

        dbc.Row([
            dbc.Col(html.H1(children=['<prediction>'], id='show_result',
                            style={
                                'margin-left' : '15px',
                                'color': 'red'
                            }))
        ],
            style={'margin-top': '30px'}),
        dbc.Row(dbc.Col(
            dbc.Col(html.Button('Predict Group Responsible', id='predict', className='btn btn-dark'),
                    className='col-lg-3 col-md-4 col-sm-5 col-xs-6')
        ))
    ], className="prediction dropdown")


@app.callback(
    Output('show_result', 'children'),
    [Input('predict', 'n_clicks')],
    [State('suc_pr_provstate', 'value'),
     State('suc_pr_attacktype', 'value'),
     State('suc_pr_targettype', 'value'),
     State('suc_pr_weapontype', 'value')
     ])
def update_output(n_clicks, state, attacktype, targettype, weapontype):
    return run_prediction(state, attacktype, targettype, weapontype)


def run_prediction(provstate, attacktype, targettype, weapontype):
    if provstate == None or attacktype == None or targettype == None or weapontype == None:
        return ['<prediction>']
    if provstate[0] == '' or attacktype[0] == '' or targettype[0] == '' or weapontype[0] == '':
        return ['<prediction>']

    df = pd.read_csv("gtd_data/globalterrorismdb_0718dist.csv",
                     usecols=['country_txt', 'iyear', 'imonth', 'provstate', 'city', 'suicide', 'attacktype1',
                              'attacktype1_txt', 'attacktype2', 'targtype1', 'targtype1_txt', 'targsubtype1', 'gname',
                              'nperps', 'weaptype1_txt', 'weaptype1', 'weapsubtype1', 'nkill', 'nwound', 'property',
                              'multiple'])
    df = df[df['country_txt'] == 'Pakistan']
    df = df[df['gname'] != 'Unknown']

    df = df.drop(columns='country_txt')

    df['provstate_txt'] = df['provstate']
    df['city_txt'] = df['city']
    df['provstate'] = df['provstate'].map({'unknown': 0,
                                           'Islamabad Capital Territory': 1,
                                           'Federally Administered Tribal Areas': 2,
                                           'North-West Frontier Province': 3,
                                           'Khyber Pakhtunkhwa': 3,
                                           'Punjab': 4,
                                           'Sindh': 5,
                                           'SIndh': 5,
                                           'Balochistan': 6,
                                           'Gilgit-Baltistan': 7,
                                           'Azad Kashmir': 8,
                                           })
    df = df.fillna(0)
    df['city'] = df['city'].astype('category').cat.codes
    df['gname_txt'] = df['gname']
    df['gname'] = df['gname'].astype('category').cat.codes

    in_labels = ['provstate', 'multiple', 'suicide', 'attacktype1', 'targtype1', 'weaptype1', 'property']
    out_label = ['gname']
    in_df = df[in_labels]
    out_df = df[out_label]

    X_train, X_test, y_train, y_test = train_test_split(in_df, out_df, test_size=0.1, random_state=30)

    rfc_500 = RandomForestClassifier(n_estimators=500)

    rfts = ['RFC_100', 'RFC_150', 'RFC_250', 'RFC_250_E', 'RFC_500']
    rftscores = pd.DataFrame(index=rfts, columns=['accuracy'])

    rfc_500.fit(X_train, y_train[out_label])
    rft_predictions = rfc_500.predict(X_test)

    ps_num = getNumForLabel('provstate', provstate, df)[0]
    at_num = getNumForLabel('attacktype1', attacktype, df)[0]
    tt_num = getNumForLabel('targtype1', targettype, df)[0]
    wt_num = getNumForLabel('weaptype1', weapontype, df)[0]

    arr = np.array([ps_num, 1.0, 0, at_num, tt_num, wt_num, 1.0])

    arr = arr.reshape(1, -1)
    rft_predictions = rfc_500.predict(arr)

    df1 = df[df['gname'] == rft_predictions[0]]
    return df1['gname_txt'].unique()


def print_uniques(df):
    for i in df:
        print(i + ":\t" + str(df[i].unique()))


def get_uniques(df):
    labels = df.columns.values
    classes = pd.DataFrame(index=labels, columns=['nu', 'u'])
    for i in labels:
        classes.loc[i]['nu'] = df[i].nunique()
        classes.loc[i]['u'] = df[i].unique()
    return classes


def get_stats(df):
    stats = df.describe()
    stats = stats.transpose()
    return stats


def getNumForLabel(label, value, df):
    return df[df[label + "_txt"] == value][label].unique()
