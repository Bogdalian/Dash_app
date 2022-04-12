import os
import pandas as pd
from unicodedata import lookup
import plotly.express as px
import re
from dash import Dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

TOKEN_MAPBOX = 'pk.eyJ1IjoiYm9nZGFuMTExIiwiYSI6ImNsMW43aGc4NDA5c2gzYnBnOWlza3lsemEifQ.-sas8WK5BnFBL8wEYL8PYg'
df = pd.read_pickle('All_data_on_problem_on_region.pkl')


fig = px.scatter_mapbox(df,
                        color="С проблемой",
                        lat='Долгота',
                        lon='Широта',
                        #text='Адрес', # текст над точкой (не пропадает)
                        hover_data=['С проблемой','Адрес', 'Перевозчик'],
                        center={'lat':59.952616475800596 , 'lon':30.351220848002722},
                        zoom=9,
                        color_discrete_sequence=['#32CD32','#EF553B'],
                        )

fig.update_layout(#margin={"r":20,"t":20,"l":20,"b":20},
                  mapbox_style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                  mapbox_accesstoken=TOKEN_MAPBOX,
                  )


app = Dash('test_Map', external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'], prevent_initial_callbacks=True)
app.layout = html.Div([
                dcc.Graph(id='gini_year_barchart', figure=fig)
])

if '__main__' == __name__:
    app.run_server(debug=True)
