import pandas as pd
import pickle
import plotly.express as px
import plotly
from plotly.subplots import make_subplots
import dash
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
import geojson
from geojson import Feature, FeatureCollection, Point
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Scattermapbox
import mapboxgl as gj
from dash import html
from dash import Dash

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
fig1.add_bar(x=df_podr['Всего контейнерных площадок'],
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
                    bargroupgap=0.1)

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

# пробегаемся по всем районам
for j in range(1, len(df_cross.columns) - 4):
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
                                center={'lat': 59.949547, 'lon': 30.304278}, # 59.949547° 30.304278°
                                zoom=10,
                                custom_data=['Процент'],
                                hover_data=["Район"]
                               )

# Редактировнае карты
fig_map.update_layout(
                        height=800,
                        margin={"r": 0, "t": 0, "l": 8.5, "b": 0},
                        mapbox_style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                        mapbox_accesstoken=TOKEN_MAPBOX,
                        mapbox_center={'lat': 59.949547, 'lon': 30.304278},
                        mapbox_zoom=8.5,
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
########################### Отрисовка таблицы с проблемами по районам в процентах ######################################
table=[]
for i in range(0,len(df_centroid),3):
    rows=[]
    for j in range(i,i+3):
        rows.append(
            html.Div([
            html.Span(df_centroid.loc[j, 'Район'],
                     style={'display':'block',
                            'font-size': '14px'
                            }),
            html.Span(f'''{round(df_centroid.loc[j, 'Процент'])}%''',
                     style={'display':'block',
                            'text-align':'right',
                            'font-size': '28px'
                            })
            ],
                     style={'background-color':df_centroid.loc[j, 'color'],
                            'width':'33.33%',
                            'height':'110px',
                            'display': 'inline-block',
                            "border":"0.5px black solid",
                            'padding-right': '15px',
                            'padding-bottom': '10px',
                            'padding-left': '10px',
                            'padding-top': '8px'})
        )
    table.append(html.Div(rows, style={'display':'block'} ))

############################################   Графики    ##############################################################
legend_color = html.Div([html.Div(['< 4,66%'],
                                  style={'text-align': 'center',
                                         'backgroundColor': '#fdde43',
                                         'width': '30%',
                                         'justify-content': 'center'}),
                         html.Div(['4,66% - 9,33%'],
                                  style={'text-align': 'center',
                                         'backgroundColor': '#fdae25',
                                         'width': '30%',
                                         'justify-content': 'center'}),
                         html.Div(['9,33% - 14%'],
                                  style={'text-align': 'center',
                                         'backgroundColor': '#fd7207',
                                         'width': '30%',
                                         'justify-content': 'center'})],
                        id='color_legend')
part_problem = 1975
all_square = 26626
problem_percent = int(part_problem * 100 / all_square)
trash_car = 465
tko_out_month = 45.6
tko_out_year = 1245
message = 1245
progress_bar =  go.Figure(data=[go.Pie(values=[100 - problem_percent, problem_percent],
                          hole=0.86,
                          rotation=3.6 * problem_percent,
                          showlegend=False,
                          customdata=[100 - problem_percent, problem_percent],
                          hovertemplate='%{customdata}%<extra></extra> ',
                          hoverinfo='none',
                          textinfo='none',
                          marker_colors=['#eaebec', '#fbc02d'])],
                         )
progress_bar.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=100, width=100,)

pyLogo = Image.open(r"C:\Users\b.bulatov\PycharmProjects\Deploy_plotly\assets\trash.png")
progress_bar.add_layout_image(dict(source=pyLogo, xref="paper", yref="paper", x=0.37, y=0.66, sizex=0.28, sizey=0.28,sizing="stretch", opacity=0.5, layer="below"))
progress_bar.update_traces(hoverlabel_bordercolor='#bdc2c7', hoverlabel_font_color='black',hoverlabel_font_size=12)

# Текст внизу дашборда -------------------------------------------------------------------------------------------------
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
# Дроп даун для выбора района ------------------------------------------------------------------------------------------
dropdown_region = dcc.Dropdown(options=[{'label': 'Все районы', 'value': 'Все районы'}] +
                                       [{'label': name, 'value': name} for name in df_centroid['Район'].sort_values(ascending=True)],
                                style={'display': 'block', 'width':'83%', 'textAlign':'center'}, id='area_dropdown', placeholder="Выберите район")

# Три кнопки со ссылками -----------------------------------------------------------------------------------------------
button_URL = html.Div([
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

            }, id='button_3_test'),

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

            }, id='button_2_test'),

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

            }, id='button_1_test'),
    ], id='buttons_link_test')

# Значения показателей и заголовки для индикаторов ---------------------------------------------------------------------
precent = dcc.Markdown('7%', style={'textAlign': 'start', 'font-size': '40px', "verticalAlign": "down"})
title = html.Span('ДОЛЯ ПЛОЩАДОК С ПРОБЛЕМАМИ', style={'font-size':'14px','font-family':'Roboto','textAlign': 'start'})

# Таблица с индикаторами -----------------------------------------------------------------------------------------------
table_header = [html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))]
row1 = html.Tr([
        html.Td(dbc.Card(
            [
            dbc.CardHeader("ДОЛЯ ПЛОЩАДОК С ПРОБЛЕМАМИ", style={'font-size': '14px'}),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Div(
                                    dcc.Graph(figure=progress_bar, config={'displayModeBar':False, 'staticPlot':False})
                                )
                                        ),
                                dbc.Col([html.Div(precent, style={'margin-top': 0, 'margin-bottom': 0, 'margin-left': 0 }),
                                         dcc.Markdown('1975/ **26626**', style={'textAlign': 'top', 'font-size': '15px',"verticalAlign": "top"})])
                            ],  style={'justify' : 'center'}
                        )
                    ]
                )
            ]
        ), style={"height": "10rem"}
        ),
    html.Td(dbc.Card(
            [
                dbc.CardHeader("МЕСТА НАКОПЛЕНИЯ ТКО", style={'font-size': '14px'}),
                dbc.CardBody(
                    [
                        html.Span(dcc.Markdown('**26626**/ 1975'), style={'font-size': '40px', 'font-family': 'Roboto'}),
                        html.Span(dcc.Markdown('ВСЕГО/ ЗАНЯТО'), style={'font-size': '15px', 'margin-top': 0, 'font-family': 'Roboto'}),
                    ]
                )
            ]
        ), style={"height": "10rem"}
                    ),
        html.Td(dbc.Card(
            [
                dbc.CardHeader("МЕСТА НАКОПЛЕНИЯ ТКО", style={'font-size': '14px'}),
                dbc.CardBody(
                    [
                        html.Span(dcc.Markdown('**26626**/ 1975'),
                                  style={'font-size': '40px', 'font-family': 'Roboto'}),
                        html.Span(dcc.Markdown('ВСЕГО/ ЗАНЯТО'),
                                  style={'font-size': '15px', 'margin-top': 0, 'font-family': 'Roboto'}),
                    ]
                )
            ]
        ), style={"height": "10rem"}
        ),
])
row2 = html.Tr([
        html.Td(dbc.Card([
            dbc.CardHeader("НАКОПЛЕНИЯ ТКО С ПРОБЛЕМАМИ", style={'font-size': '14px'}),
            dbc.CardBody(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Row(
                            [
                                dbc.Col(html.Span('1975', style={'font-size': '40px', 'font-family': 'Roboto','display': 'inline-block', 'vertical-align': 'down','margin-top': '-1.9vw'})),
                                dbc.Col(html.Span('26626', style={'font-size': '25px', 'font-family': 'Roboto','vertical-align': 'down', 'textAlign': 'end','display': 'inline-block', 'margin-top': '-1.9vw'}))
                            ]
                            )
                        )
                    ),
                    dbc.Progress(value=7, color='#ffc736', id='progress_line'),
                ]
            )
        ], style={"height": "11rem"})
        ),
    html.Td(dbc.Card(
        [
            dbc.CardHeader("ВЫВЕЗЕНО ТКО", style={'font-size': '14px'}),
            dbc.CardBody(
                [
                    html.Span(dcc.Markdown('**45.6**/ 1245'),
                              style={'font-size': '40px', 'font-family': 'Roboto'}),
                    html.Span(dcc.Markdown('ВСЕГО/ ЗАНЯТО'),
                              style={'font-size': '15px', 'margin-top': 0, 'font-family': 'Roboto'}),
                ]
            )
        ]
    ), style={"height": "10rem"}
    ),
    html.Td(dbc.Card(
        [
            dbc.CardHeader("СООБЩЕНИЙ НА ПОРТАЛЕ", style={'font-size': '14px'}),
            dbc.CardBody(
                [
                    html.Span(dcc.Markdown('1245'), style={'font-size': '25px'}),
                ]
            )
        ], style={"height": "11rem"}
    )
    )
])
table_body = [html.Tbody([row1, row2], style={'Align':'flex', 'table_layout':'fixed'})]
indicator_table = dbc.Table(table_body, bordered=False)

# Карта ---------------------------------------------------------------------
table_with_region = html.Div([dbc.Row(table),legend_color], id='table_region')
# Таблица по районам --------------------------------------------------------
map_with_container = dcc.Graph(figure=fig_map, style={'height':700}, id = 'all_map')


# Кнопки по ТКО --------------------------------------------------------------------------------------------------------
bottom_TKO = html.Div([
              html.Button('ТКО',
                         n_clicks=0,
                         className="btn_activated",
                         style={
                             'align-text': 'center',
                             'align-items': 'center',
                             'width':'50%'
                         }
                        ),

              html.Button('ТКО С ПРОБЛЕМАМИ',
                         n_clicks=0, className="btn",
#                          active=False,
                         style={
                             'align-text': 'center',
                             'align-items': 'center',
                             'width':'50%'
                         }
                        )],id="button1",style={
                   'justify-content': 'center',
                  'align-items': 'center',
                   #"width": "80%",
                 #  "margin-left": "20px",
                  # "margin-bottom": "5px",
                  # "margin-right": "120px",
                   #'padding-top': '20px',
                   #'padding-right': '20px',
                   "margin-left": "20px"
})
# Кнопки для переключения Карты и таблицы -----------------------------------------------------------------------------
button_map_table = html.Div([
        dbc.Button("", color="primary", className="bi bi-pin-map",  n_clicks=0, id="btn_map"),
        dbc.Button("", color="primary", className="bi bi-table", n_clicks=0, id="btn_table")
    ],style={'justify-content': 'end', 'display': 'flex'}, id='map_table_button__')
###############################################  Структура дашборда   ##################################################
# Инициализация дашборда -----------------------------------------------------------------------------------------------
app = Dash('test',external_stylesheets=[dbc.themes.BOOTSTRAP,  dbc.icons.BOOTSTRAP])
app.layout = html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H1('Вывоз мусора с контейнерных площадок по состоянию на 02.03.2022',
                                                style={'textAlign':'center', 'font-family': 'Roboto', 'fontSize':'24px'}),

                                        indicator_table,

                                        # Кнопки ТКО/ТКО с проблемами---------------------------------------------------
                                        dbc.Row(
                                            [
                                                bottom_TKO
                                            ]
                                        ),
                                        # График ТКО по операторам -----------------------------------------------------
                                        dbc.Container(
                                            [
                                                dcc.Graph(figure=fig1, config={'displayModeBar': False,'staticPlot': False})
                                            ]
                                        )
                                    ], sm=12,  md=12,  lg=6,  xl=6
                                ), # -----------------------------------------------------------------------------------
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            html.H1('Количество мест накопления ТКО АО "Невский экологический оператор"',
                                                    style={'textAlign':'center', 'font-family': 'Roboto','fontSize':'24px'}),

                                            dbc.Row(
                                                [
                                                    dbc.Col( # выпадающий список районов -------------------------------
                                                    [
                                                        html.Div(dropdown_region),
                                                    ]
                                                ),
                                                dbc.Col(html.Div(
                                                    button_map_table
                                                )
                                                ),
                                            ]
                                                    ),
                                            dbc.Row(# Карта/таблица. По умолчанию в данном контейнере находится карта
                                                [
                                                    dbc.Col(
                                                        [
                                                            map_with_container
                                                        ],  style={'height': '12%', "width": '100%', 'lign':'left'},
                                                        id='area_map_table'
                                                    )

                                                ]
                                            )
                                        ]
                                    ), sm=12,  md=12,  lg=6,  xl=6
                                )
                                ]
                        ),
                        dbc.Row(# Большой график по всем районам--------------------------------------------------------
                            [
                                dcc.Graph(figure=fig_test)
                            ]
                        ),
                        dbc.Row(
                            [ # Текстовая информация в нижней части дашборда -------------------------------------------
                                dbc.Col(
                                    [
                                        dcc.Markdown(text1),
                                        dcc.Markdown(text2)
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Markdown(text3),
                                        button_URL # три кнопки с ссылками в самом низу дашборда------------------------

                                    ]
                                )
                            ]
                        ),
                    ]
)
############################################ Обратный вызов ############################################################
# Управление картой (выпадающий список и нажатие на нужный район) ------------------------------------------------------

# Обновление drop_dawn по клику
@app.callback( Output('area_dropdown', 'value'),
               Input('all_map', 'clickData'))
def update_label_dropdown(clickData):
    if not isinstance(clickData, type(None)):
        area_name = clickData['points'][0]['customdata'][1]
        return area_name

# Обновление карты по drop_dawn
@app.callback(Output('all_map', 'figure'), # all_map - id графического объекта с картой
               [Input('all_map', 'clickData'), # drop_down - id выпадающего списка
                Input('area_dropdown', 'value')])
def update_area_by_dropdown(clickData, value):
    if value is None:
        area_name = clickData['points'][0]['customdata'][1]
    area_name = value
    # area_name = clickData[0]custom_data[1]
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
    # Если выбран какой-то определенный район --------------------------------------------------------------------------
    if area_name in df_centroid['Район'].unique().tolist():
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

        fig.update_layout(
            mapbox=dict(style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                        accesstoken=TOKEN_MAPBOX,
                        bearing=0,
                        center=dict(lat=df_centroid.loc[df_centroid['Район'] == area_name, 'lat'].values[0],
                                    lon=df_centroid.loc[df_centroid['Район'] == area_name, 'lon'].values[0]),
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

        fig.update_layout(mapbox=dict(style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                                                  accesstoken=TOKEN_MAPBOX,
                                                  bearing=0,
                                                  center=dict(lat=59.952616475800596, lon=30.351220848002722),
                                                  pitch=0,
                                                  zoom=8))

    # Карта по умолчанию -----------------------------------------------------------------------------------------------
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

@app.callback([Output('area_map_table', 'children')], # контейнер, где находится карта и таблица
              [Input(f"btn_map", "n_clicks"),
               Input(f"btn_table", "n_clicks")])
def update_output(btn_1, btn_2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn_map' in changed_id:
        return [map_with_container]#[dcc.Graph(figure=fig2, config={'displayModeBar': False, 'staticPlot': False})]
    elif 'btn_table' in changed_id:
        return [table_with_region]#[dcc.Graph(figure=fig1, config={'displayModeBar': False, 'staticPlot': False})]
    return dash.no_update

# sm md lg xl
if __name__ == '__main__':
    #app.run_server(host='192.168.42.40', port='8080', debug=True)
    app.run_server(port='8087')