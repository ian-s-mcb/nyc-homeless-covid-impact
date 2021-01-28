# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import json
import numpy as np
import pandas as pd
import pickle

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go


def load_data(geojson_filepath):
    '''Loads data from pickle files
    '''
    geojson_filename = './data/geojson.pickle'
    shelter_df_filename = './data/shelter_df.pickle'
    try:
        with open(geojson_filename, 'rb') as f:
            geojson = pickle.load(f)
        shelter_df = pd.read_pickle(shelter_df_filename)
    except IOError:
        print('Error: pickle files not found.\nRun the explore-2 notebook to generate pickle files')
        exit(1)

    return (geojson, shelter_df)

def create_figures(geojson, shelter_df):
    '''Creates two figures with the provided geojson object and dataframe'''
    top_figure = px.choropleth_mapbox(
        shelter_df.loc['2020-09'],
        geojson=geojson,
        locations='Community District',
        featureidkey='properties.boro_cd',
        color='Shelter Population',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        zoom=10,
        center={'lat': 40.714, 'lon': -74.006},
        opacity=0.5,
    )

    one_cd_df = shelter_df[shelter_df['Community District'] == '109']['2020-03':]

    bot_figure = px.bar(
        one_cd_df,
        x=one_cd_df.index,
        y='Shelter Population',
        hover_data=['Shelter Population'],
    )

    # Remove excessive figure margin
    top_figure.layout['margin'] = {
        'l': 0, #left margin
        'r': 0, #right margin
        'b': 5, #bottom margin
        't': 0, #top margin
    }
    bot_figure.layout['margin'] = {
        'l': 0, #left margin
        'r': 0, #right margin
        'b': 5, #bottom margin
        't': 0, #top margin
    }

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
            children=html.H4(children='Shelter population by CD in Mar 2020')
        ),
        dcc.Graph(
            id='graph-map',
            figure=top_figure,
        ),
        html.H4(children='Shelter population in CD-109 - West Harlem - Manhattan'),
        dcc.Graph(
            id='graph-bar',
            figure=bot_figure,
        ),
        html.Footer(
            children=[
                html.H4(children='About this visualization'),
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