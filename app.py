# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# with urlopen('https://data.cityofnewyork.us/api/geospatial/yfnk-k7r4?method=export&format=GeoJSON') as response:
#     geojson = json.load(response)
try:
    geojson_filepath = './data/Community Districts.geojson'
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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = px.choropleth_mapbox(
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

app.layout = html.Div(children=[
    html.H1(children='COVID-19 impact on NYC’s homeless population'),
    html.P(children='Authors: Ian S. McBride, Lifu Tao, and Xin Chen. Mentor: Ronak Etemadpour'),

    dcc.Graph(
        id='example-graph',
        figure=fig,
        style={
            'height': '100vh'
        }
    ),
    html.P(children='')
])

if __name__ == '__main__':
    app.run_server(debug=True)