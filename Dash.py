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
import pandas as pd
import geojson
from geojson import Feature, FeatureCollection, Point
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Scattermapbox
import mapboxgl as gj

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

###################################### Датасет для графика по перевозчикам #############################################
df_podr=pd.read_excel('Перевозчики.xlsx')
pd.to_numeric(df_podr['Всего контейнерных площадок'])
pd.to_numeric(df_podr.iloc[:,1])
df_podr['sum']=df_podr.apply(lambda x: x['Всего контейнерных площадок'] + x['из них с проблемами'], axis=1)
df_podr=df_podr.sort_values(by='sum')
df_podr['Всего контейнерных площадок'].apply(lambda x: "{:,}".format(x).replace(',', ' '))

# График по перевозчикам (с проблемами)---------------------------------------------------------------------------------
fig1=go.Figure()
fig1.add_bar(   x=df_podr['Всего контейнерных площадок'],
                y=df_podr['Название'],
                orientation='h',
                base='relative',
                marker_color=['#4da2f2','#ffc736','#8ad554','#d38dcc'], offsetgroup=2,
                hovertemplate= "Всего контейнерных площадок: %{x}<extra></extra>",
                xhoverformat='.0f',
                text=df_podr['Всего контейнерных площадок'].apply(lambda x: "{:,}".format(x).replace(',', ' ')),
                textposition='outside')

fig1.update_layout( height=250,
                    margin=dict(l=10, r=10, t=10, b=10),
                    plot_bgcolor='#FFFFFF',
                    showlegend=False,
                    hovermode='y unified',
                    modebar_remove=["zoom","pan","autoscale","zoomout","zoomin", "lasso","lasso2d", "resetScale2d", "select"],
                    dragmode=False,
                    hoverlabel_bgcolor='#ffffff',
                    hoverlabel_bordercolor='#bdc2c7',
                    bargap=0.4,
                    bargroupgap=0.1
)

fig1.add_bar(x=df_podr['из них с проблемами'],y=df_podr['Название'],
            orientation='h', base='relative', offsetgroup=2,
            marker_color='#ff3c64',
            width=0.5,
            hovertemplate= "из них с проблемами: %{x}<extra></extra>",
            text=df_podr['из них с проблемами'],
            textposition='auto')
fig1.update_traces(textfont_size=14)

fig1.update_xaxes(visible=False, range=[-400,13000],separatethousands=True, tickformat=",.0f")
fig1.update_yaxes(showline = True,tickfont=dict(color='black', size=16),showspikes=False)

# График по перевозчикам (всего) ---------------------------------------------------------------------------------------
fig2=go.Figure()
fig2.add_bar(x=df_podr['Всего контейнерных площадок'],
             y=df_podr['Название'], orientation='h', base='relative',
             marker_color=['#4da2f2','#ffc736','#8ad554','#d38dcc'], offsetgroup=2,
             hovertemplate= "Всего контейнерных площадок: %{x}<extra></extra>",
             xhoverformat='.0f',
             text=df_podr['Всего контейнерных площадок'].apply(lambda x: "{:,}".format(x).replace(',', ' ')),
             textposition='outside')

fig2.update_layout(height=250,
                   margin=dict(l=10, r=10, t=10, b=10),
                   plot_bgcolor='#FFFFFF',
                   showlegend=False,
                   hovermode='y unified',
                   modebar_remove=["zoom","pan","autoscale","zoomout","zoomin", "lasso","lasso2d", "resetScale2d", "select"],
                   dragmode=False,
                   hoverlabel_bgcolor='#ffffff',
                   hoverlabel_bordercolor='#bdc2c7',
                   bargap=0.4,
                   bargroupgap=0.1)
fig2.update_traces(textfont_size=14)
fig2.update_xaxes(visible=False, range=[-400,13000],separatethousands=True)
fig2.update_yaxes(showline = True,tickfont=dict(color='black', size=16),showspikes=False)


############################################### Датасет для проблем по районам #########################################
df_trash = pd.read_excel('Проблемы.xlsx')
df_trash['Количество'] = df_trash['Количество'].astype(int)
df_cross = pd.crosstab(df_trash['Наименование показателя'],
                       df_trash['Район'],
                       values=df_trash['Количество'],
                       aggfunc='sum').reset_index()

df_cross['color'] = ['#4da2f2', '#ffc736', '#d38dcc', '#8ad554', '#B1B1B1']
df_cross['hover'] = ['количество площадок с жалобами (АО \"Автопарк №1 "Спецтранс\"): %{x}<extra></extra>',
                     'количество площадок с жалобами (АО \"Ресурс АТЭ\"): %{x}<extra></extra>',
                     'количество площадок с жалобами (АО \"Эко Лэнд\"): %{x}<extra></extra>',
                     'количество площадок с жалобами (АО \"ЭкоВаст\"): %{x}<extra></extra>',
                     'количество площадок всего: %{x}<extra></extra>']

df_cross['Легенда'] = ['АО \"Автопарк №1 "Спецтранс\"',
                       'АО \"Ресурс АТЭ\"',
                       'АО \"Эко Лэнд\"',
                       'АО \"ЭкоВаст\"',
                       'Общее кол-во ТКО']

df_cross['order'] = [3,4,2,5,1]
df_cross = df_cross.sort_values(by='order', ascending=True)
fig_test = make_subplots(rows=9, cols=2, horizontal_spacing=0.10, shared_xaxes=True)
legend_names = []

for j in range(1, len(df_cross.columns) - 4): # пробегаемся по всем районам
    square = df_cross.loc[~df_cross.iloc[:, j].isna(), df_cross.columns[j]].reset_index(drop=True) # данные по конкретному району
    indexies = df_cross.loc[~df_cross.iloc[:, j].isna(), df_cross.columns[j]].index.to_list()

    # порядок размещения графиков (в две колонки)
    if j < 10:
        col = 1
        row = j
    else:
        col = 2
        row = j - 9
    for i, k in zip(range(0, len(square)), indexies):
        if df_cross.loc[k, 'Легенда'] not in legend_names:
            show_legend = True
            legend_names.append(df_cross.loc[k, 'Легенда'])
        else:
            show_legend = False
        fig_test.add_trace(go.Bar(x=[int(square[i])],
                                  y=[df_cross.columns[j]],
                                  orientation="h",
                                  marker_color=df_cross.loc[k, 'color'],
                                  hovertemplate=df_cross.loc[k, 'hover'],
                                  xhoverformat='.0f',
                                  name=df_cross.loc[k, 'Легенда'],
                                  showlegend=show_legend,
                                  legendgroup=df_cross.loc[k, 'Легенда'],
                                  text=["{:,}".format(int(square[i])).replace(',', ' ')],
                                  textposition='outside',
                                  outsidetextfont=dict(size=14)),
                                  row, col)
    fig_test.update_layout(xaxis={'categoryorder': 'total ascending'})

fig_test.update_layout(height=700,
                       margin=dict(l=10, r=10, t=10, b=10),
                       paper_bgcolor='#f6f7fb',

                       plot_bgcolor='#f6f7fb',
                       xaxis=dict(visible=True, showspikes=False, showline=False),
                       hovermode='y unified',
                       modebar_remove=["zoom", "pan", "autoscale", "zoomout", "zoomin",
                                       "lasso", "lasso2d","resetScale2d", "select"],
                       dragmode=False,
                       hoverlabel_bgcolor='#ffffff',
                       hoverlabel_bordercolor='#bdc2c7',
                       bargap=0.01,
                       bargroupgap=0.01,
                       legend=dict(orientation="h", y=1.1, x=0.4, xanchor="center", traceorder="normal")

                       )
fig_test.update_xaxes(visible=False, range=[-200, 3000],
                      separatethousands=True)
fig_test.update_yaxes(tickfont=dict(color='black', size=14),
                      separatethousands=True,
                      showspikes=False, spikecolor='#ffffff',
                      side="left", spikedash="solid", spikesnap="cursor", ticklabelposition="outside left")

#############################################   Датасет для карты ######################################################
TOKEN_MAPBOX = 'pk.eyJ1IjoiYm9nZGFuMTExIiwiYSI6ImNsMW43aGc4NDA5c2gzYnBnOWlza3lsemEifQ.-sas8WK5BnFBL8wEYL8PYg'
df = pd.read_pickle('All_data_on_problem_on_region.pkl')
df_centroid = pd.read_csv(r'C:\Users\b.bulatov\PycharmProjects\Deploy_plotly\Проценты_для_районов.csv')
df_centroid['Центроид'] = df_centroid['Центроид'].apply(lambda x: eval(x))
df_centroid[['lat', 'lon']] = pd.DataFrame(df_centroid['Центроид'].tolist(), columns=['lat', 'lon'])
df_centroid.loc[df_centroid['Класс'] == 1, 'color'] = '#fdde43'
df_centroid.loc[df_centroid['Класс'] == 2, 'color'] = '#fdae25'
df_centroid.loc[df_centroid['Класс'] == 3, 'color'] = '#fd7207'
df_centroid = df_centroid.sort_values(by='Район').reset_index(drop=True)
df.loc[df.loc[:, 'С проблемой'] == 'нет', 'Цвет'] = '#72b246'
df.loc[df.loc[:, 'С проблемой'] == 'да', 'Цвет'] = '#de4362'

df = pd.merge(df, df_centroid[['Район', 'Процент']], how='left', on='Район')
with open('2_5474130071532868438.json', encoding='utf-8') as f:
    geo_json = json.load(f)

# Отрисовка карты ------------------------------------------------------------------------------------------------------
fig_map = px.choropleth_mapbox(
                                df,
                                geojson=geo_json,
                                opacity=0.2,
                                hover_name="Район",
                                locations="Район",
                                featureidkey="properties.NAME",
                                center={'lat': 59.952616475800596, 'lon': 30.351220848002722},
                                zoom=10,
                                custom_data=['Процент'],
                                hover_data=["Район"]
                               )

# Редактировнае карты
fig_map.update_layout(
                        height=500,
                        margin={"r": 0, "t": 0, "l": 0, "b": 0},
                        mapbox_style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                        mapbox_accesstoken=TOKEN_MAPBOX,
                        mapbox_center={'lat': 59.952616475800596, 'lon': 30.351220848002722},
                        mapbox_zoom=8,
                        modebar_remove=["zoom", "pan", "autoscale", "zoomout",
                                        "zoomin", "lasso", "lasso2d","resetScale2d", "select"]
                      )

fig_map.update_traces(
                        hoverlabel_bordercolor='#bdc2c7',
                        hoverlabel_bgcolor='#ffffff',
                        hoverlabel_font_color='black',
                        hoverlabel_font_family="Open Sans",
                        hoverlabel_font_size=12,
                        showlegend=False,
                        marker_line_color='#000000',
                        marker_line_width=1,
                        colorscale=[[0, '#67645c'], [1, '#67645c']],
                        hovertemplate='Район: <b>%{location}</b> <br>Доля площадок с проблемами: <b>%{customdata[0]} %</b> <br>'
                        )

fig_map.add_scattermapbox(
                        below="''",
                        lat=df_centroid['lat'],
                        lon=df_centroid['lon'],
                        mode='markers+text',
                        textposition="middle center",
                        text=df_centroid['Процент'].apply(lambda x: str(x) + ' %'),
                        textfont={'size': 13, 'color': "#2E4053", 'family': "Droid Sans"},
                        marker_size=df_centroid['Процент'].apply(lambda x: 10 + np.sqrt(x * 1000)),
                        marker_color=df_centroid['color'],
                        hoverinfo='skip'
                    )

########################### Отрисовка таблицы с проблемами по районам в процентах #######################################
table=[]
for i in range(0,len(df_centroid),3):
    rows=[]
    for j in range(i,i+3):
        rows.append(
            html.Div([
            html.Span(df_centroid.loc[j, 'Район'],
                     style={'display':'block',
                            'font-size': '14px'}),
            html.Span(f'''{round(df_centroid.loc[j, 'Процент'])}%''',
                     style={'display':'block',
                            'text-align':'right',
                            'font-size': '28px'
                            })
            ],
                     style={'background-color':df_centroid.loc[j, 'color'],
                            'width':'33.3%',
                            'display': 'inline-block',
                            "border":"0.5px black solid",
                            'padding-right': '15px',
                            'padding-bottom': '10px',
                            'padding-left': '10px',
                            'padding-top': '8px'})
        )
    table.append(html.Div(rows, style={'display':'block'}))

######################################################################################################################
part_problem = 1975
all_square = 26626
problem_percent = int(part_problem * 100 / all_square)
trash_car = 465
tko_out_month = 45.6
tko_out_year = 1245
message = 1245
progress_bar = go.Figure(data=[go.Pie(values=[100 - problem_percent, problem_percent],
                                      hole=0.86,
                                      rotation=3.6 * problem_percent,
                                      showlegend=False,
                                      customdata=[100 - problem_percent, problem_percent],
                                      hovertemplate='%{customdata}%<extra></extra> ',
                                      hoverinfo='none',
                                      textinfo='none',
                                      marker_colors=['#eaebec', '#fbc02d'])],
                         )
progress_bar.update_layout(

    margin=dict(l=0, r=0, t=0, b=8),
    height=75,
    width=75,

    # Added parameter
)

progress_bar.update_traces(hoverlabel_bordercolor='#bdc2c7',
                           hoverlabel_font_color='black',
                           hoverlabel_font_size=12,
                           )

pyLogo = Image.open(r"C:\Users\b.bulatov\PycharmProjects\Deploy_plotly\assets\trash.png")
progress_bar.add_layout_image(
    dict(
        source=pyLogo,
        xref="paper",
        yref="paper",
        x=0.37,
        y=0.66,
        sizex=0.28,
        sizey=0.28,
        sizing="stretch",
        opacity=0.5,
        layer="below")
)

progress_bar.show(config={'displayModeBar': False})

############################################  Текст внизу дашборда #####################################################
text1 = '''### Кто обеспечивает вывоз твердых коммунальных отходов\n
### в Санкт‐Петербурге?\n

С 01.01.2022 в соответствии с положениями статей 24.6 и 29.1 Федерального закона от 24.06.1998 No 89-ФЗ «Об отходах производства и потребления» сбор, транспортирование, обработка, утилизация, обезвреживание и захоронение твердых коммунальных отходов, образованных на территории Санкт‐Петербурга, обеспечивает региональный оператор по обращению с ТКО – Акционерное общество «Невский экологический оператор» (далее – АО «НЭО», Региональный оператор).

Статус регионального оператора по обращению с ТКО присвоен АО «НЭО» по результатам проведенного Комитетом по природопользованию, охране окружающей среды и обеспечению экологической безопасности (далее – Комитет) конкурсного отбора.'''

text2 = '''### Контактные данные регионального оператора:\n

Адрес клиентского сервиса: Кондратьевский пр., д. 15, корп. 3, Санкт‐Петербург, 195197 \n
Адрес электронной почты: office@spb-neo.ru, dogovor@spb-neo.ru, dogovordop@spb-neo.ru (для заключения договоров) \n
Почтовый адрес: ул. Арсенальная, д. 1, корп. 2, лит. А, офис 113 \n
БЦ «Арсенальный», Санкт‐Петербург, 195009 
'''

text3 = '''### Телефоны горячих линий:\n  
__8-812-303-80-90__ - клиентская служба (для физических лиц, обслуживается ЕИРЦ Петроэлектросбыт)\n
__8-812-213-07-10__ - дополнительный номер для приема заявок на вывоз ТКО, включая крупногабаритные отходы\n
__8-812-329-17-66__ - диспетчерская служба для управляющих организаций и органов управления многоквартирными домами\n
__8-812-305-06-65__ - клиентская служба (для юридических лиц)\n
__004__ - прием жалоб на ненадлежащее состояние контейнерных площадок'''

########################################################################################################################
FONT_AWESOME = "https://use.fontawesome.com/releases/v6.1.1/css/all.css"
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
               )
app.layout = html.Div([

    html.Div([
        html.H1('Вывоз мусора с контейнерных площадок по состоянию на 02.03.2022',
                style={'font-size': '24px', 'font-family': 'Roboto, sans-serif'},
                id='inner_title'),
        html.Div([

            html.Div([html.Span(['ДОЛЯ ПЛОЩАДОК С ПРОБЛЕМАМИ'],
                                style={'font-size': '12px',
                                       'color': '#323b43',
                                       'font-family': 'Roboto, sans-serif'},
                                id='subgrid_title1'),

                      dcc.Graph(figure=progress_bar,
                                config={'displayModeBar': False,
                                        'staticPlot': False},
                                id="progress_bar1"),

                      html.Span([f"{'{:,}'.format(problem_percent).replace(',', ' ')}%"],
                                style={'font-size': '40px',
                                       'color': '#ffc736'},
                                id='percent'),

                      html.Div([
                          html.Span(f"{'{:,}'.format(part_problem).replace(',', ' ')}/ ",
                                    style={'font-size': '18px',
                                           'color': '#ffc736'}),

                          html.Span(f"{'{:,}'.format(all_square).replace(',', ' ')}",
                                    style={'font-size': '18px',
                                           'color': '#323b43'})],
                          id='part_problem_down')

                      ], className='part_problem'),

            html.Div([
                html.Span(['МЕСТА НАКОПЛЕНИЯ ТКО'],
                          style={'font-size': '12px',
                                 'color': '#323b43',
                                 'font-family': 'Roboto, sans-serif'},
                          id='subgrid_title2'),

                html.Div([html.Span(f"{'{:,}'.format(all_square).replace(',', ' ')}",
                                    style={'font-size': '40px',
                                           'color': '#323b43'}),

                          html.Span(f"/ {'{:,}'.format(part_problem).replace(',', ' ')}",
                                    style={'font-size': '20px',
                                           'color': '#323b43'})],
                         id='place_tko_top'),

                html.Span('ВСЕГО / ЗАНЯТО', id='place_tko_down',
                          style={'justify-content': 'top',
                                 'text-align': 'top',
                                 'font-size': '12px',
                                 'color': '#323b43',
                                 'font-family': 'Roboto, sans-serif'})],
                className='tko_place'),

            html.Div([
                html.Span(['МУСОРОВОЗОВ НА ЛИНИИ'],
                          style={'font-size': '12px',
                                 'color': '#323b43',
                                 'font-family': 'Roboto, sans-serif'},
                          id='subgrid_title3'),
                html.Div([html.I(className="fa-solid fa-truck-field",
                                 style={'color': '#757576'},
                                 ),

                          html.Span([f" {'{:,}'.format(trash_car).replace(',', ' ')}"],
                                    style={'font-size': '40px',
                                           'color': '#323b43'})],
                         id='trash_car_down')

            ],
                className='trash_car'),

            html.Div([html.Span(['НАКОПЛЕНИЯ ТКО С ПРОБЛЕМАМИ'],
                                style={'font-size': '12px',
                                       'color': '#323b43',
                                       'font-family': 'Roboto, sans-serif'},
                                id='subgrid_title4'),
                      html.Div([
                          html.Div(f"{'{:,}'.format(part_problem).replace(',', ' ')}",
                                   style={'textAlign': 'left',
                                          'font-size': '40px',
                                          'color': '#ffc736'}, id='part_problem_1'),

                          html.Div(f"{'{:,}'.format(all_square).replace(',', ' ')}",
                                   style={'padding-left': '30px',
                                          'font-size': '24px',
                                          'color': '#323b43',
                                          'padding-top': '15px'
                                          })], id='problem_all'),

                      dbc.Progress(value=7, color='#ffc736',
                                   id='progress_line')],
                     className='tko_problem'),

            html.Div([
                html.Span(['ВЫВЕЗЕНО ТКО'],
                          style={'font-size': '12px',
                                 'color': '#323b43',
                                 'font-family': 'Roboto, sans-serif'},
                          id='subgrid_title5'),

                html.Div([
                    html.Span(f"{'{:,}'.format(tko_out_month).replace(',', ' ')}",
                              style={'font-size': '40px',
                                     'color': '#323b43'}),
                    html.Span(f"/ {'{:,}'.format(tko_out_year).replace(',', ' ')}",
                              style={'font-size': '20px',
                                     'color': '#323b43'})],
                    id='day_month'),

                html.Span('СУТКИ / МЕСЯЦ',
                          style={'font-size': '12px',
                                 'color': '#323b43',
                                 'font-family': 'Roboto, sans-serif'},
                          id='day_mont_down')],
                className='tko_out'),

            html.Div([
                html.Span(['СООБЩЕНИЙ НА ПОРТАЛЕ'],
                          style={'font-size': '12px',
                                 'color': '#323b43',
                                 'font-family': 'Roboto, sans-serif'},
                          id='subgrid_title6'),
                html.Div([
                    html.I(className="fa-solid fa-envelope",
                           style={'color': '#757576'}),

                    html.Span([f" {'{:,}'.format(message).replace(',', ' ')}"],
                              style={'font-size': '40px',
                                     'color': '#323b43'})], id='message_icon')
            ],
                className='trash_message'),

        ], className='inner-grid'),

        html.Div([
            html.Div([
                html.Button('ТКО', id="btn_1",
                            n_clicks=0,
                            #                          active=False,
                            className="btn_activated",
                            style={
                                'align-text': 'center',
                                'align-items': 'center',
                                'width': '50%'
                            }
                            ),

                html.Button('ТКО С ПРОБЛЕМАМИ', id="btn_2",
                            n_clicks=0,
                            className="btn",
                            style={
                                'align-text': 'center',
                                'align-items': 'center',
                                'width': '50%'
                            }
                            )],
                id="button",
                style={
                    'justify-content': 'center',
                    'align-items': 'center',
                    "width": "90%",
                    "margin-left": "20px",
                    "margin-bottom": "5px",
                    "margin-right": "20px",
                    'padding-top': '20px',
                    'padding-right': '20px',
                    "margin-left": "20px"}
            ),

            html.H2('Количество мест накопления ТКО АО "Невский экологический оператор"',
                    style={'font-size': '18px', 'padding-top': '20px', "margin-left": "20px", "margin-left": "20px"}),

            html.Div([dcc.Graph(figure=fig2,
                                config={'displayModeBar': False,
                                        'staticPlot': False})],id='graph_chainging')

        ], id='graph1_button', style={"display": 'block',
                                      'justify-content': 'center'})],
           className='left_top'),

    html.Div([

        dcc.Graph(figure=fig_test, animate=True,
                  config={'displayModeBar': False,
                          'staticPlot': False},
                  style={"width": '100%',
                         'align-items': 'center',
                         'justify-content': 'center',
                         "margin-top": "15px",
                         "margin-right": "auto"
                         })], id='graph'),

    html.Div([html.H2('Количество мест накопления ТКО АО "Невский экологический оператор"', id='title_map',
                      style={'font-size': '18px', 'padding-bottom': '20px', 'padding-top': '20px',
                             "margin-left": "20px", "margin-left": "20px"}),

              dcc.Dropdown(
                  options=[{'label': 'Все районы', 'value': 'Все районы'}] + [{'label': name, 'value': name} for name in
                                                                              df_centroid['Район'].sort_values(
                                                                                  ascending=True)],
                  style={'padding-left': '10px', 'display': 'block'}, id='area_dropdown', placeholder="Выберите район"),
              html.Div([html.Button(html.I(className="fa-solid fa-map-location-dot"),
                                    style={'justify-content': 'center'},
                                    n_clicks=0, id='map_button', className='btn_activated'),
                        html.Button(html.I(className="fa-solid fa-table"),
                                    n_clicks=0, id='table_button', style={'justify-content': 'center'},
                                    className='btn')],
                       style={'justify-content': 'right', 'display': 'flex'}, id='map_table_button'),

              html.Div([

                  dcc.Graph(figure=fig_map, id='all',
                            config={'displayModeBar': False,
                                    'staticPlot': False})
              ], id="part",

                  style={"width": '100%',
                         #                "border": "0.5px solid #CCD1D1",
                         'backgroundColor': '#ffffff',
                         'padding-left': '10px',
                         'padding-right': '10px',
                         'padding-top': '10px',
                         'align-items': 'center',
                         'justify-content': 'center',
                         "margin-left": "20px",
                         "margin-right": "auto"
                         }
              ),
              html.Div([html.Div(['< 4,66%'],
                                 style={'text-align': 'center', 'backgroundColor': '#fdde43', 'width': '30%',
                                        'justify-content': 'center'}),
                        html.Div(['4,66% - 9,33%'],
                                 style={'text-align': 'center', 'backgroundColor': '#fdae25', 'width': '30%',
                                        'justify-content': 'center'}),
                        html.Div(['9,33% - 14%'],
                                 style={'text-align': 'center', 'backgroundColor': '#fd7207', 'width': '30%',
                                        'justify-content': 'center'})], id='color_legend')
              ], className='div_map'),

    dcc.Markdown([text1], style={'font-size': '14px',
                                 'font-family': 'Roboto,sans-serif'},
                 id='text1'),

    dcc.Markdown([text2],
                 style={'font-size': '14px',
                        'font-family': 'Roboto,sans-serif',
                        "white-space": "pre"},
                 dedent=False,
                 id='text2'),

    dcc.Markdown(text3, style={'font-size': '14px',
                               'font-family': 'Roboto,sans-serif'},
                 dedent=False,
                 id='text3'),

    html.Div([
        html.Div(
            [dbc.Button("Официальный сайт регионального оператора",

                        external_link=True,
                        target='https://spb-neo.ru/',
                        href='https://spb-neo.ru/',
                        style={"background-color": "#00acc1",
                               "color": "white",
                               "border-radius": "5px",
                               "border": False,
                               "width": "40%",
                               "height": "100%",
                               "fontSize": "12px"
                               })],
            style={
                'align-items': 'left',
                'justify-content': 'left',
                "margin-left": "auto",
                "margin-right": "auto",
                "display": "flex"

            }, id='button_3'),

        html.Div(
            [dbc.Button("Графики вывоза ТКО с контейнерных площадок",

                        external_link=True,
                        href='https://spb-neo.ru/informatsiya-dlya-potrebiteley/grafik-vyvoza-tko/',
                        target='https://spb-neo.ru/informatsiya-dlya-potrebiteley/grafik-vyvoza-tko/',
                        style={
                            "background-color": "#00acc1",
                            "color": "white",
                            "border-radius": "5px",
                            "border": False,
                            "width": "40%",
                            "height": "100%",
                            "fontSize": "12px"
                        })],
            style={
                'padding-top': '5px',
                'align-items': 'center',
                'justify-content': 'left',

                "display": "flex"

            }, id='button_2'),

        html.Div(
            [dbc.Button(
                "Оставить сообщение о невывозе ТКО",

                external_link=True,
                href='https://gorod.gov.spb.ru/problems/add/?city_object=2&reason=250',
                target='https://gorod.gov.spb.ru/problems/add/?city_object=2&reason=250',
                style={"background-color": "#00acc1",
                       "color": "white",
                       "border-radius": "5x",
                       "border": False,
                       "width": "40%",
                       "height": "100%",
                       "fontSize": "12px",
                       }
            )
            ],

            style={
                'padding-top': '5px',
                'align-items': 'right',
                'justify-content': 'left',

                "display": "flex"

            }, id='button_1'),
    ], id='buttons_link')

],
    className='container-grid2'
)


@app.callback(
    Output("area_dropdown", 'style'),
    [Input("table_button", "n_clicks"),
     Input("map_button", "n_clicks")]

)
def hide_dropdown(table_button, map_dropdown):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'table_button' in changed_id:
        return {'display': 'none'}
    elif 'map_button' in changed_id:
        return {'display': 'block'}
    return dash.no_update


@app.callback(
    [Output(f"{i}", "className") for i in ['table_button', 'map_button']],
    [Input(f"{i}", "n_clicks") for i in ['table_button', 'map_button']])
def set_active(*args):
    ctx = dash.callback_context

    if not ctx.triggered or not any(args):
        return ["btn", "btn_activated"]

    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    return [
        "btn_activated" if button_id == f"{i}" else "btn" for i in ['table_button', 'map_button']
    ]


@app.callback(
    #     [Output(f"btn_{i}", "className") for i in range(1, 3)]
    [Output("graph_chainging", 'children')],
    [Input(f"btn_{i}", "n_clicks") for i in range(1, 3)]

)
def update_output(btn_1, btn_2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn_1' in changed_id:
        return [dcc.Graph(figure=fig2,
                          config={'displayModeBar': False,
                                  'staticPlot': False})]

    elif 'btn_2' in changed_id:
        return [dcc.Graph(figure=fig1,
                          config={'displayModeBar': False,
                                  'staticPlot': False})]
    return dash.no_update


@app.callback(
    [Output(f"btn_{i}", "className") for i in range(1, 3)],
    [Input(f"btn_{i}", "n_clicks") for i in range(1, 3)])
def set_active(*args):
    ctx = dash.callback_context

    if not ctx.triggered or not any(args):
        return ["btn_activated", "btn"]

    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    return [
        "btn_activated" if button_id == f"btn_{i}" else "btn" for i in range(1, 3)
    ]


@app.callback(
    Output('all', 'figure'),
    [Input('all', 'clickData'),
     Input('area_dropdown', 'value')]
)
def update_area_by_dropdown(clickData, value):
    area_name = value

    fig = px.choropleth_mapbox(df,
                               geojson=geo_json,
                               opacity=0.2,
                               hover_name="Район",
                               locations="Район",
                               featureidkey="properties.NAME",
                               center={'lat': 59.952616475800596, 'lon': 30.351220848002722},
                               zoom=9,
                               custom_data=['Процент'],
                               hover_data=["Район"]

                               )

    fig.update_traces(hoverlabel_bordercolor='#bdc2c7',
                      hoverlabel_bgcolor='#ffffff',
                      hoverlabel_font_color='black',
                      hoverlabel_font_family="Open Sans",
                      hoverlabel_font_size=12,
                      marker_line_color='#000000',
                      marker_line_width=1,
                      colorscale=[[0, '#67645c'], [1, '#67645c']],
                      hovertemplate='Район: <b>%{location}</b> <br>Доля площадок с проблемами: <b>%{customdata[0]} %</b> <br>'
                      )

    if area_name != 'Все районы':
        fig.add_trace(
            go.Scattermapbox(lat=df.loc[df['Район'] == area_name, 'Долгота'].apply(lambda x: str(x)).to_list(),
                             lon=df.loc[df['Район'] == area_name, 'Широта'].apply(lambda x: str(x)).to_list(),
                             mode='markers',
                             customdata=df.loc[
                                 df['Район'] == area_name, ['С проблемой', 'Район', 'Адрес', 'Перевозчик']],
                             hovertemplate='<b>С проблемой</b>: %{customdata[0]}<br>' +
                                           '<b>Район</b>: %{customdata[1]}<br>' +
                                           '<b>Адрес</b>: %{customdata[2]}<br>' +
                                           '<b>Перевозчик</b>: %{customdata[3]}<extra></extra>',
                             marker={'size': 7, 'color': df.loc[df['Район'] == area_name, 'Цвет']}
                             ))

        fig.update_layout(height=500, mapbox=dict(style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                                                  accesstoken=TOKEN_MAPBOX,
                                                  bearing=0,
                                                  center=dict(lat=df_centroid.loc[
                                                      df_centroid['Район'] == area_name, 'lat'].values[0],
                                                              lon=df_centroid.loc[
                                                                  df_centroid['Район'] == area_name, 'lon'].values[0]),
                                                  pitch=0,
                                                  zoom=10.5)

                          )

    elif area_name == 'Все районы':
        fig.add_trace(go.Scattermapbox(lat=df['Долгота'].apply(lambda x: str(x)).to_list(),
                                       lon=df['Широта'].apply(lambda x: str(x)).to_list(),
                                       mode='markers',

                                       customdata=df[['С проблемой', 'Район', 'Адрес', 'Перевозчик']],
                                       hovertemplate='<b>С проблемой</b>: %{customdata[0]}<br>' +
                                                     '<b>Район</b>: %{customdata[1]}<br>' +
                                                     '<b>Адрес</b>: %{customdata[2]}<br>' +
                                                     '<b>Перевозчик</b>: %{customdata[3]}<extra></extra>',
                                       marker={'size': 7, 'color': df['Цвет']}
                                       ))

        fig.update_layout(height=500, mapbox=dict(style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                                                  accesstoken=TOKEN_MAPBOX,
                                                  bearing=0,
                                                  center=dict(lat=59.952616475800596,
                                                              lon=30.351220848002722),
                                                  pitch=0,
                                                  zoom=8)

                          )

    else:
        return fig_map

    fig.add_scattermapbox(
        below="''",
        customdata=df_centroid['Район'],
        lat=df_centroid['lat'],
        lon=df_centroid['lon'],
        mode='markers+text',
        textposition="middle center",
        text=df_centroid['Процент'].apply(lambda x: str(x) + ' %'),
        textfont={'size': 13, 'color': "#2E4053", 'family': "Droid Sans"},
        marker_size=df_centroid['Процент'].apply(lambda x: 10 + np.sqrt(x * 1000)),
        marker_color=df_centroid['color'],
        hoverinfo='skip'
    )

    fig.update_layout(showlegend=False, margin={"r": 0, "t": 0, "l": 0, "b": 0}),

    return fig

def update_area(clickData, value):
    area_name = clickData['points'][0]['customdata'][1]

    fig = px.choropleth_mapbox(df,
                               geojson=geo_json,
                               opacity=0.2,
                               hover_name="Район",
                               locations="Район",
                               featureidkey="properties.NAME",
                               center={'lat': 59.952616475800596, 'lon': 30.351220848002722},
                               zoom=9,
                               custom_data=['Процент'],
                               hover_data=["Район"]

                               )

    fig.update_traces(hoverlabel_bordercolor='#bdc2c7',
                      hoverlabel_bgcolor='#ffffff',
                      hoverlabel_font_color='black',
                      hoverlabel_font_family="Open Sans",
                      hoverlabel_font_size=12,
                      marker_line_color='#000000',
                      marker_line_width=1,
                      colorscale=[[0, '#67645c'], [1, '#67645c']],
                      hovertemplate='Район: <b>%{location}</b> <br>Доля площадок с проблемами: <b>%{customdata[0]} %</b> <br>'
                      )

    fig.add_trace(go.Scattermapbox(lat=df.loc[df['Район'] == area_name, 'Долгота'].apply(lambda x: str(x)).to_list(),
                                   lon=df.loc[df['Район'] == area_name, 'Широта'].apply(lambda x: str(x)).to_list(),
                                   mode='markers',
                                   customdata=df.loc[
                                       df['Район'] == area_name, ['С проблемой', 'Район', 'Адрес', 'Перевозчик']],
                                   hovertemplate='<b>С проблемой</b>: %{customdata[0]}<br>' +
                                                 '<b>Район</b>: %{customdata[1]}<br>' +
                                                 '<b>Адрес</b>: %{customdata[2]}<br>' +
                                                 '<b>Перевозчик</b>: %{customdata[3]}<extra></extra>',
                                   marker={'size': 7, 'color': df.loc[df['Район'] == area_name, 'Цвет']}
                                   ))

    fig.update_layout(height=500, mapbox=dict(style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                                              accesstoken=TOKEN_MAPBOX,
                                              bearing=0,
                                              center=dict(
                                                  lat=df_centroid.loc[df_centroid['Район'] == area_name, 'lat'].values[
                                                      0],
                                                  lon=df_centroid.loc[df_centroid['Район'] == area_name, 'lon'].values[
                                                      0]),

                                              pitch=0,
                                              zoom=10.5)

                      )

    fig.add_scattermapbox(
        below="''",
        customdata=df_centroid['Район'],
        lat=df_centroid['lat'],
        lon=df_centroid['lon'],
        mode='markers+text',
        textposition="middle center",
        text=df_centroid['Процент'].apply(lambda x: str(x) + ' %'),
        textfont={'size': 13, 'color': "#2E4053", 'family': "Droid Sans"},
        marker_size=df_centroid['Процент'].apply(lambda x: 10 + np.sqrt(x * 1000)),
        marker_color=df_centroid['color'],
        hoverinfo='skip'
    )

    fig.update_layout(showlegend=False, margin={"r": 0, "t": 0, "l": 0, "b": 0}),

    return [dcc.Graph(figure=fig, id='all', config={'displayModeBar': False,
                                                    'staticPlot': False},
                      style={'display': 'block', 'padding-right': '10px'})]


@app.callback(
    Output('part', 'children'),
    [Input('map_button', 'n_clicks'),
     Input('table_button', 'n_clicks')]
)
def map_to_table(map_button, table_button):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'map_button' in changed_id:
        return [
            dcc.Graph(figure=fig_map, id='all',
                      config={'displayModeBar': False,
                              'staticPlot': False})
        ]

    elif 'table_button' in changed_id:
        return [html.Div(table, style={"width": '100%',
                                       'height': '500px'})]
    else:
        return dash.no_update


@app.callback(
    Output('area_dropdown', 'value'),
    Input('all', 'clickData')

)
def update_label_dropdown(clickData):
    area_name = clickData['points'][0]['customdata'][1]
    return area_name


# app.run_server(debug=True, use_reloader=False)


# app.run_server(use_reloader=False)
app.run_server(use_reloader=False)