import pandas as pd
import numpy as np
import plotly.graph_objects as go


def front_page_map():
    pd.options.mode.chained_assignment = None
    # mapbox_access_token = 'pk.eyJ1IjoibWFrcy1zaCIsImEiOiJjajRnMGhyNzcxZGFzMnd1ZnZteHF1YXo3In0.5R_XD1wl8F7ffCjAN1yxLg'
    terror_data = pd.read_csv('gtd_data/globalterrorismdb_0718dist.csv', encoding='ISO-8859-1',
                              usecols=[0, 1, 2, 3, 8, 11, 12, 13, 14, 29, 35, 84, 98, 101])
    terror_data = terror_data.rename(
        columns={'eventid': 'id', 'iyear': 'year', 'imonth': 'month', 'iday': 'day',
                 'country_txt': 'country', 'provstate': 'state', 'city': 'city', 'targtype1_txt': 'target',
                 'weaptype1_txt': 'weapon', 'attacktype1_txt': 'attacktype', 'nkill': 'nkill',
                 'nwound': 'nwound', 'addnotes': 'info'})

    terror_data['nkill'] = terror_data['nkill'].fillna(0).astype(int)
    terror_data['nwound'] = terror_data['nwound'].fillna(0).astype(int)
    terror_data = terror_data.dropna(how='any', subset=['latitude', 'longitude'])

    terror_pak = terror_data[terror_data['country'] == 'Pakistan']
    terror_india = terror_data[terror_data['country'] == 'India']
    terror_afghan = terror_data[terror_data['country'] == 'Afghanistan']

    terror_pak_assassination = terror_pak[terror_pak['attacktype'] == 'Assassination']

    terror_pak.loc[:, 'day'] = terror_pak.apply(lambda row: str(row['id'])[6:8] if row['day'] == 0 else row['day'],
                                                axis=1)
    # terror_pak.loc[:, 'date'] = pd.to_datetime(terror_pak[['day', 'month', 'year']])

    terror_pak = terror_pak.drop_duplicates(['latitude', 'longitude', 'nkill'])
    terror_peryear = np.asarray(terror_pak.groupby('year').year.count())
    terror_years = np.arange(1970, 2016)
    terror_years = np.delete(terror_years, [1])
    trace1 = go.Scattergeo(
        geo='geo3',
        lon=terror_pak[(terror_pak['year'] == 2011)]['longitude'],
        lat=terror_pak[(terror_pak['year'] == 2011)]['latitude'],
        mode='markers',
        marker=go.Marker(size=3, opacity=0.7, color='#A60000', ),
        text=terror_pak[(terror_pak['year'] == 2011)]['country']
    )
    trace2 = go.Scattergeo(
        geo='geo3',
        lon=terror_india[(terror_india['year'] == 2011)]['longitude'],
        lat=terror_india[(terror_india['year'] == 2011)]['latitude'],
        mode='markers',
        marker=go.Marker(size=3, opacity=0.7, color='#B60000', ),
        text=terror_india[(terror_india['year'] == 2011)]['country']
    )

    # data=trace1
    data = [trace1, trace2]
    layout = go.Layout(
        title='Terrorist attacks Occurring in Pakistan & India',
        height=600,
        # width=1000,
        autosize=True,
        dragmode='zoom',
        geo3=dict(
            scope='asia',
            showlakes=True,
            showocean=True,
            # oceancolor='rgb(255, 255, 255)',
            showland=True,
            showcountries=True,
            countrywidth=2,
            countrycolor='rgb(200, 200, 200)',
        )
        # geo3=dict(projection=dict(type='orthographic', ),scope='asia', showlakes=False,showocean=True,showland=True,showcountries=True,)
    )
    fig = go.Figure(data=data, layout=layout)
    return fig


def bar_chart():
    terror_data = pd.read_csv('gtd_data/globalterrorismdb_0718dist.csv', encoding='ISO-8859-1',
                              usecols=[0, 1, 2, 3, 8, 11, 12, 13, 14, 29, 35, 82, 98, 101])
    terror_data = terror_data.rename(
        columns={'eventid': 'id',
                 'iyear': 'year',
                 'imonth': 'month',
                 'iday': 'day',
                 'country_txt': 'country',
                 'provstate': 'state',
                 'targtype1_txt': 'target',
                 'weaptype1_txt': 'weapon',
                 'attacktype1_txt': 'attacktype',
                 'nkill': 'fatalities',
                 'nwound': 'injuries',
                 'addnotes': 'info'})
    terror_data['fatalities'] = terror_data['fatalities'].fillna(0).astype(int)
    terror_data['injuries'] = terror_data['injuries'].fillna(0).astype(int)
    terror_data = terror_data.dropna(how='any', subset=['latitude', 'longitude'])

    terror_pk = terror_data[terror_data['country'].str.lower() == 'pakistan']

    terror_peryear = np.asarray(terror_pk.groupby('year').year.count())
    terror_years = np.arange(1992, 2016)
    terror_years = np.delete(terror_years, [1])

    trace1 = go.Bar(
        x=terror_years,
        y=terror_peryear.cumsum(),
        name='Total number',
        marker=dict(
            color='#009999'
        )
    )

    trace2 = go.Scatter(
        x=terror_years,
        y=terror_peryear,
        name='Per year',
        mode='lines+markers',
        marker=dict(
            size=5,
            symbol='diamond',
            color='#BF3030',
        ),
        line=dict(
            width=2,
            color='#BF3030',
        ),
    )

    layout = go.Layout(
        title='Terrorist Attacks by Timeline in Pakistan (1992-2015)',
        barmode='group',
        xaxis=dict(
            title='Year',
        ),
        yaxis=dict(
            title='Number of attacks',
        ),
        legend=dict(
            x=0,
            y=1
        )
    )

    data = [trace1, trace2]

    fig = dict(data=data, layout=layout)
    return fig


def table():
    terror_data = pd.read_csv('gtd_data/globalterrorismdb_0718dist.csv', encoding='ISO-8859-1',
                              usecols=[0, 1, 2, 3, 8, 11, 12, 13, 14, 29, 35, 84, 98, 101],nrows=100)
    terror_data = terror_data.rename(
        columns={'eventid': 'id', 'iyear': 'year', 'imonth': 'month', 'iday': 'day',
                 'country_txt': 'country', 'provstate': 'state', 'city': 'city', 'targtype1_txt': 'target',
                 'weaptype1_txt': 'weapon', 'attacktype1_txt': 'attacktype', 'nkill': 'nkill',
                 'nwound': 'nwound', 'addnotes': 'info'})

    terror_data['nkill'] = terror_data['nkill'].fillna(0).astype(int)
    terror_data['nwound'] = terror_data['nwound'].fillna(0).astype(int)
    terror_data = terror_data.dropna(how='any', subset=['latitude', 'longitude'])

    table_data = terror_data.head(20)
    columns = list(table_data.columns)
    data = []
    for col in table_data.columns:
        data.append(table_data[col])

    fig = go.Figure(
        data=[go.Table(
            header=dict(values=columns,
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=data,
                       fill_color='lavender',
                       align='left')
        )
    ])
    return fig


def correlations():
    df = pd.read_csv("gtd_data/globalterrorismdb_0718dist.csv",
                     usecols=['country_txt', 'iyear', 'imonth', 'provstate', 'city', 'suicide', 'attacktype1',
                              'attacktype1_txt', 'attacktype2', 'targtype1', 'targtype1_txt', 'targsubtype1', 'gname',
                              'nperps', 'weaptype1_txt', 'weaptype1', 'weapsubtype1', 'nkill', 'nwound', 'property',
                              'multiple'], encoding='latin-1')
    df = df[df['country_txt'] == 'Pakistan']
    df = df[df['gname'] != 'Unknown']

    df = df.drop(columns='country_txt')
    # get_uniques(df)

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

    corr = df.corr()

    # sns.set(font_scale=1.5)
    # sns.heatmap(corr,linewidths=.5,cmap="YlGnBu")

    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv')
    # programmers = ['Alex','Nicole','Sara','Etienne','Chelsea','Jody','Marianne']

    # base = datetime.datetime.today()
    # dates = base - np.arange(180) * datetime.timedelta(days=1)
    # z = np.random.poisson(size=(len(programmers), len(dates)))

    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=list(corr.columns),
        y=list(corr.index),
        colorscale='Viridis'))

    fig.update_layout(
        title='Attribute Correlations',
        xaxis_nticks=36,
        height=800
    )
    return fig