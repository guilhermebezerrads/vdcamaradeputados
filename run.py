import pandas as pd
### ------***CÓDIGO DO DASHBOARD USANDO PLOTLY DASH***------ ###

frame = pd.read_csv('participacao_percent.csv')
line = pd.read_csv('posicionamento_deputados.csv')
df_gastos_por_ano_deputado = pd.read_csv('gastos_por_deputado.csv', sep=";")
df_gastos_por_ano_categoria = pd.read_csv('gastos_por_categoria.csv', sep=";")
df_gastos_por_ano_partido = pd.read_csv('gastos_por_partido.csv', sep=";")
df_gastos_por_ano_fornecedor = pd.read_csv('gastos_por_fornecedor.csv', sep=";")
df_novos_deputados_por_sexo = pd.read_csv('novos_deputados_por_sexo.csv', sep=";")

import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#Inicialização do plotly dash no tema Slate
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
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
    ),

    dbc.Row([
        dbc.Col([
            html.P(''),
            #Gráfico participação em votação por região
            dcc.Graph(id='line-chart',
                      figure={}
                      )
        ],
        width={'size':8}
        )
    ], justify='center'
    ),

    dbc.Row([
        dbc.Col([
            html.H2("Novos deputados por sexo"),
            dcc.Graph(id='chart_deputados_por_sexo',
                      figure={}
            )
        ],
        width={'size':8}
        )
    ], justify='center'
    ),

    dbc.Container([
        html.H1('Gastos na camara'),
        dcc.Tabs(id="tabs_gastos", value="tab_ano",

            children=[
                dcc.Tab(label="Por ano", value="tab_ano"),
                dcc.Tab(label="Total", value="tab_total"),
            ]
        ),
        html.Div(id="tabs_gastos_content")
    ]),


], fluid=True
)

# Gráfico
@app.callback(
    Output('bar-chart', 'figure'),
    Input('select', 'value')
)
def update_graph(ano):
    dv_2020 = frame[frame['ano'] == ano]
    
    fig = px.bar(
        dv_2020, 
        x='posicionamento', 
        y='voto_norm', 
        category_orders={
            "posicionamento": ["Esquerda", "Centro-esquerda", "Centro", "Centro-direita", "Direita"]
        },
        color='Regiao', 
        barmode='group'
    )
       
    return fig

@app.callback(
    Output('line-chart', 'figure'),
    Input('select', 'value')
)

def grafico_line(dummy):
    c_map = {
        'Centro': '#71c055',
        'Centro-direita': '#40b8ea',
        'Centro-esquerda': '#fba51a',
        'Direita': '#436fb6',
        'Esquerda': '#ed1e24'
    }

    fig = px.line(line, x="Ano", y="Deputados", color='Posicionamento', color_discrete_map=c_map)
    fig.update_layout(
        title_text="Deputados Votantes por Posicionamento",
        title_x=0.5,
    )
       
    return fig

@app.callback(
    Output('chart_deputados_por_sexo', 'figure'),
    Input('select', 'value')
)
def gera_grafico_novos_deputados_por_sexo(_):
    y_m = df_novos_deputados_por_sexo.query("sexo == 'M'")["count"]
    y_f = df_novos_deputados_por_sexo.query("sexo == 'F'")["count"]
    x = df_novos_deputados_por_sexo["anoEleicao"].unique()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, 
        y=y_f, 
        fill='tonexty',
        fillcolor='rgba(255, 60, 49, 0.5)',
        mode='lines+markers',
        line_color='rgba(255, 60, 49, 0.4)',
        name="Mulheres"
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=y_m,
        fill='tonexty',
        fillcolor='rgba(25, 97, 251, 0.5)',
        mode='lines+markers',
        line_color='rgba(25, 97, 251, 0.5)',
        name="Homens"
    ))
    fig.update_layout(
        title_text="Número de <b>novos</b> deputados por sexo em cada eleição de 1890 à 2018",
        title_x=0.5,
        xaxis_title_text = "Eleições",
        xaxis_type = "category",
        xaxis_tickangle = -45,
        yaxis_title_text = "Número de <b>novos</b> deputados"
    )

    return fig


@app.callback(
    Output("tabs_gastos_content", 'children'),
    Input("tabs_gastos", 'value')
)
def gera_tabs_gastos(tab):
    if tab == 'tab_ano':
        return dbc.Row([
            dbc.Col([
                html.P(''),
                dcc.Dropdown(id='id_ano_tipo_gasto',
                            multi=False,
                            value="Gastos por deputados",
                            options=gastos_tipos
                            ),
                dcc.Dropdown(id='id_ano_gasto',
                            multi=False,
                            value= 2021,
                            options=[{'label': str(x), 'value': int(x)} for x in sorted(df_gastos_por_ano_deputado["numAno"].unique())]
                            ),
                dcc.Dropdown(id='id_ano_raking',
                            multi=False,
                            value= 10,
                            options=[{'label': str(x), 'value': int(x)} for x in [3, 4, 5, 6, 8, 10, 12, 15, 20]]
                            ),
                dcc.Graph(id='chart_ano_gastos',
                        figure={}
                        )
                ],
                width={'size':8}
                )
            ], justify='center'
        ),
    elif tab == 'tab_total':
        return dbc.Row([
            dbc.Col([
                html.P(''),
                dcc.Dropdown(id='id_total_tipo_gasto',
                            multi=False,
                            value="Gastos por deputados",
                            options=gastos_tipos
                            ),
                dcc.Dropdown(id='id_total_ranking',
                            multi=False,
                            value= 10,
                            options=[{'label': str(x), 'value': int(x)} for x in [3, 4, 5, 6, 8, 10, 12, 15, 20]]
                            ),
                dcc.Graph(id='chart_total_gastos',
                        figure={}
                        )
                ],
                width={'size':8}
            )], 
            justify='center'
        ),

gastos_tipos = ["Gastos por deputados", "Gastos por partido", "Gastos por categoria", "Recebimento por fornecedores"]
map_tipos_y = {
    "Gastos por deputados": "nomeEsgPartido",
    "Recebimento por fornecedores": "txtFornecedor",
    "Gastos por categoria": "txtDescricao",
    "Gastos por partido": "sgPartido"
}

@app.callback(
    Output('chart_ano_gastos', 'figure'),
    Input('id_ano_tipo_gasto', 'value'),
    Input('id_ano_gasto', 'value'),
    Input('id_ano_raking', 'value')
)
def gera_grafico_gastos_por_ano_(tipo_gasto="Gastos por deputados", ano=2021, ranking=10):
    df = None
    title = ""
    yaxis_title = ""
    xaxis_title = "<b>Valor líquido</b> gasto"

    if tipo_gasto == "Gastos por deputados":
        df = df_gastos_por_ano_deputado
        title = f"Gastos dos {ranking} deputados que mais gastaram em {ano}"
        yaxis_title = "<b>Nome</b> do deputado"

    elif tipo_gasto == "Gastos por partido":
        df = df_gastos_por_ano_partido
        title = f"Gastos dos {ranking} partidos que mais gastaram em {ano}"
        yaxis_title="<b>Nome</b> do partido"

    elif tipo_gasto == "Gastos por categoria":
        df = df_gastos_por_ano_categoria
        title = f"Gasto das {ranking} categorias que mais houve gasto em {ano}"
        yaxis_title = "<b>Nome</b> da categoria"

    elif tipo_gasto == "Recebimento por fornecedores":
        df = df_gastos_por_ano_fornecedor
        title = f"Quantidade de dinheiro que os {ranking} fornecedores que mais receberam em {ano}"
        yaxis_title = "<b>Nome</b> do fornecedor"
        xaxis_title = "<b>Valor líquido</b> recebido"


    df = df[df["numAno"] == ano]
    df = df[0:ranking]
    fig = px.bar(df, x='vlrLiquido', y=map_tipos_y[tipo_gasto])
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        title_text= title,
        title_x=0.5,
        xaxis_title_text=xaxis_title,
        yaxis_title_text=yaxis_title,
        legend_title_text="",
    )
    return fig

@app.callback(
    Output('chart_total_gastos', 'figure'),
    Input('id_total_tipo_gasto', 'value'),
    Input('id_total_ranking', 'value')
)
def gera_grafico_gastos_totais(tipo_gasto="Gastos por deputados", ranking=10):
    df = None
    title = ""
    yaxis_title = ""
    xaxis_title = "<b>Valor líquido</b> gasto"

    if tipo_gasto == "Gastos por deputados":
        df = df_gastos_por_ano_deputado
        title = f"Gastos dos {ranking} deputados que mais gastaram de 2008 até hoje (2022)"
        yaxis_title = "<b>Nome</b> do deputado"

    elif tipo_gasto == "Gastos por partido":
        df = df_gastos_por_ano_partido
        title =  f"Gastos dos {ranking} partidos que mais gastaram de 2008 até hoje (2022)"
        yaxis_title="<b>Nome</b> do partido"

    elif tipo_gasto == "Gastos por categoria":
        df = df_gastos_por_ano_categoria
        title = f"Gasto das {ranking} categorias que mais houve gasto de 2008 até hoje (2022)"
        yaxis_title = "<b>Nome</b> da categoria"

    elif tipo_gasto == "Recebimento por fornecedores":
        df = df_gastos_por_ano_fornecedor
        title = f"Quantidade de dinheiro que os {ranking} fornecedores que mais receberam de 2008 até hoje (2022)"
        yaxis_title = "<b>Nome</b> do fornecedor"
        xaxis_title = "<b>Valor líquido</b> recebido"

    df = df.groupby([map_tipos_y[tipo_gasto]], as_index=False).sum().sort_values(by=["vlrLiquido"], ascending=False)
    df = df[0:ranking]
    fig = px.bar(df, x='vlrLiquido', y=map_tipos_y[tipo_gasto])
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        title_text= title,
        title_x=0.5,
        xaxis_title_text=xaxis_title,
        yaxis_title_text=yaxis_title
    )
    return fig

if __name__ == '__main__':
    app.run_server()