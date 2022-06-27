import pandas as pd
### ------***CÓDIGO DO DASHBOARD USANDO PLOTLY DASH***------ ###

frame = pd.read_csv('participacao_percent.csv')

import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#Inicialização do plotly dash no tema Slate
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

server = app.server


app.layout = dbc.Container([

    #Título
    dbc.Row([
        dbc.Col(html.H1("Câmara dos Deputados - Dados abertos",
                        className='text-center text-primary, mb-4'),
                width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H2("Visualização de Dados",
                        className='text-center text-primary, mb-4'),
                width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.P(''),
            #select ano
            dcc.Dropdown(id='select',
                         multi=False,
                         value= 2003,
                         options=[{'label': str(x), 'value': int(x)} for x in sorted(frame['ano'].unique())]
                         ),

            #Gráfico participação em votação por região
            dcc.Graph(id='bar-chart',
                      figure={}
                      )
        ],
        width={'size':8}
        )
    ], justify='center'
    )

], fluid=True
)

# Gráfico
@app.callback(
    Output('bar-chart', 'figure'),
    Input('select', 'value')
)
def update_graph(ano):
    dv_2020 = frame[frame['ano'] == ano]
    
    fig = px.bar(dv_2020, x='posicionamento', y='voto_norm', color='Regiao', barmode='group')
       
    return fig

if __name__ == '__main__':
    app.run_server()