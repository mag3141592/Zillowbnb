"""
Map application with filters
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
from plotly import graph_objs as go
from  plotly.graph_objs import *

mapbox_access_token = 'pk.eyJ1IjoiYWJsZXciLCJhIjoiY2p2bXlwZzF5MTZscDN6cGg5NDRpYmUyeSJ9.QGIvEgLD8Nv4plUW9P805g'

df = pd.read_csv("listing.csv")
map_data = df[['name', 'listing_url', 'neighbourhood_cleansed',
    'neighbourhood_group_cleansed','latitude','longitude','accommodates','room_type','price']]
neighbourhoods = map_data['neighbourhood_group_cleansed'].unique()
neighbourhoods.sort()

acco = map_data['accommodates']

rtype = map_data['room_type'].unique()
rtype.sort()

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

custom_style = 'mapbox://styles/ablew/cjvn1rtau2uol1cn5u0a3z13i'

layout_map = go.Layout(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size=14),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Seattle Airbnb',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style=custom_style,
        center=dict(
            lon=-122.335167,
            lat=47.608013
        ),
        zoom=10,
    )
)


def gen_map(map_data):
    return{
        "data": [{
                "type": "scattermapbox",
                "lat": list(map_data['latitude']),
                "lon": list(map_data['longitude']),
                "hoverinfo": "text",
                "hovertext": [["Name: {} <br>Type: {} <br>Neighbourhood: {} <br>Price: {}".format(i,j,k,m)]
                                for i,j,k,m in zip(map_data['name'], map_data['room_type'], map_data['neighbourhood_group_cleansed'], map_data['price'])],
                "mode": "markers",
                "name": list(map_data['name']),
                "marker": {
                    "size": 12,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }




app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Neighbourhood'),
            dcc.Dropdown(
                id='neighbourhood',
                options=[{'label': str(nb), 'value': str(nb)} for nb in neighbourhoods],
                value=neighbourhoods[0]
            ),
        html.Label('Accommodates'),
            dcc.Slider(
                id='accommodates',
                min=acco.min(),
                max=acco.max(),
                marks={str(a): str(a) for a in acco.unique()},
                value=10
            ),
        html.Br(),
        html.Label('Room Type'),
            dcc.Checklist(
                id='room-type',
                options=[{'label': str(rt), 'value': str(rt)} for rt in rtype],
                values=[rtype[0], rtype[1]]
            ),
            dcc.Graph(id='map-graph',
                      animate=True,
                      style={'margin-top': '20'})


        ])



    ])
])


@app.callback(
    Output('map-graph', 'figure'),
    [Input('neighbourhood', 'value'),
     Input('room-type', 'values'),
     Input('accommodates','value')])

def map_selection(neighbourhood, type, accommodates):
    map_aux = map_data.copy()

    map_aux = map_aux[map_aux['neighbourhood_group_cleansed'] == neighbourhood]

    map_aux = map_aux[map_aux['room_type'].isin(type)]

    map_aux = map_aux[map_aux['accommodates'] >= accommodates]


    return gen_map(map_aux)


if __name__ == '__main__':
    app.run_server(debug=True)

