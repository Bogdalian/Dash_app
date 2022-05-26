import pandas as pd
import pickle
import plotly.express as px
import plotly
from plotly.subplots import make_subplots
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import numpy as np
import pandas_datareader as web
from jupyter_dash import JupyterDash
import dash_daq as daq
import plotly.graph_objects as go
from io import BytesIO
from jupyter_dash import JupyterDash
import math
from PIL import Image
import json
import random
import dash
from dash import html
import dash_leaflet as dl
from dash import Dash
import pandas as pd
import geojson
from geojson import Feature, FeatureCollection, Point
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Scattermapbox
import mapboxgl as gj
from Dash import progress_bar

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash('12', external_stylesheets=[dbc.themes.BOOTSTRAP])

table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]
row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])
table_body = [html.Tbody([row1, row2, row3, row4])]
table = dbc.Table(table_header + table_body, bordered=True)

app.layout = html.Div(
    [
        table
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True, port='3000')