# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import json
import numpy as np
import pandas as pd
from urllib.request import urlopen

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go


def load_data(geojson_filepath):
    '''Opens or downloads the datasets
    '''
    # Dataset via API call
    # with urlopen('https://data.cityofnewyork.us/api/geospatial/yfnk-k7r4?method=export&format=GeoJSON') as response:
    #     geojson = json.load(response)

    # Dataset via manually downloaded file
    try:
        with open(geojson_filepath, 'r') as f:
            geojson = json.load(f)
    except IOError:
        print(f'Error: data file "{geojson_filepath}" not found')
        exit(1)

    boro_cds = [f['properties']['boro_cd'] for f in geojson['features']]
    vals = np.random.rand((len(boro_cds)))
    df = pd.DataFrame({
        'boro_cd': boro_cds,
        'val': vals,
    })

    return (geojson, df)

def create_figures(geojson, df):
    '''Creates two figures with the provided geojson object and dataframe'''
    top_figure = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='boro_cd',
        featureidkey='properties.boro_cd',
        color='val',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        zoom=10,
        center={'lat': 40.714, 'lon': -74.006},
        opacity=0.5,
    )

    bot_figure = px.bar(
        df,
        x='boro_cd',
        y='val',
        hover_data=['boro_cd', 'val'],
    )

    # Remove excessive figure margin
    margin = {
        'l': 0, #left margin
        'r': 0, #right margin
        'b': 5, #bottom margin
        't': 0, #top margin
    }
    top_figure.layout['margin'] = margin
    bot_figure.layout['margin'] = margin

    return (top_figure, bot_figure)

def create_app(top_figure, bot_figure):
    '''Creates the dash app'''
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(
        __name__,
        external_stylesheets=external_stylesheets
    )
    app.layout = html.Div(children=[
        html.Header(
            children=[
                html.H1(children='COVID-19 impact on NYC’s homeless population'),
            ]
        ),

        dcc.Graph(
            id='graph-map',
            figure=top_figure,
        ),
        dcc.Graph(
            id='graph-bar',
            figure=bot_figure,
        ),
        html.Footer(
            children=[
                html.H3('About this visualization'),
                html.P(children='Authors: Ian S. McBride, Lifu Tao, and Xin Chen. '),
                html.P(children='Mentor: Ronak Etemadpour'),
            ],
        )
    ])

    return app

def main():
    '''Entry point for app execution'''
    geojson_filepath = './data/Community Districts.geojson'
    return create_app(
        *create_figures(
            *load_data(geojson_filepath)
        )
    )

if __name__ == '__main__':
    main().run_server(debug=True)