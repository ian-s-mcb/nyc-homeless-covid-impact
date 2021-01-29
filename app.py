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


def load_data(geojson_filename, shelter_df_filename):
    '''Loads data from pickle files
    '''
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

# File paths
geojson_filename = './data/geojson.pickle'
shelter_df_filename = './data/shelter_df.pickle'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

geojson, shelter_df = load_data(geojson_filename, shelter_df_filename)
top_figure, bot_figure = create_figures(geojson, shelter_df)
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
        children=dcc.Markdown("""
        #### About
        This visualization was built for a two-semester
        Computer Science class, called Senior Design,
        at the City College of New York, held from Sep
        2020 to May 2021. The class was divided into
        small groups that proposed their own reseach
        topic. The theme of the research topics data
        visualization and the COVID-19 era.

        **Credits**
        * Authors: [Ian S. McBride][ian-s-mcb], [Lifu Tao][lifu], and [Xin Chen][xin]
        * [Source code][src-code]
        * Mentor: [Prof. Ronak Etemadpour][prof]
        * Data sources:
            * https://data.cityofnewyork.us/City-Government/Community-Districts/yfnk-k7r4
            * https://data.cityofnewyork.us/Social-Services/Individual-Census-by-Borough-Community-District-an/veav-vj3r
        [ian-s-mcb]: https://gitlab.com/users/ian-s-mcb/
        [xin]: https://github.com/XinChenCSC
        [lifu]: https://github.com/LifuTao
        [src-code]: https://github.com/ian-s-mcb/nyc-homeless-covid-impact
        [prof]: https://www.ccny.cuny.edu/profiles/ronak-etemadpour
        """)
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)