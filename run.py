import pandas as pd
import utils

### ------***CÓDIGO DO DASHBOARD USANDO PLOTLY DASH***------ ###

mudanca = pd.read_csv('csv/mudanca_posicionamento.csv')
frame = pd.read_csv('csv/participacao_percent.csv')
line = pd.read_csv('csv/posicionamento_deputados.csv')
df_gastos_por_ano_deputado = pd.read_csv('csv/gastos_por_deputado.csv', sep=";")
df_gastos_por_ano_categoria = pd.read_csv('csv/gastos_por_categoria.csv', sep=";")
df_gastos_por_ano_partido = pd.read_csv('csv/gastos_por_partido.csv', sep=";")
df_gastos_por_ano_fornecedor = pd.read_csv('csv/gastos_por_fornecedor.csv', sep=";")
df_novos_deputados_por_sexo = pd.read_csv('csv/novos_deputados_por_sexo.csv', sep=";")
df_votacoes_por_ano = pd.read_csv('csv/votacoes_por_ano.csv', sep=",")
df_prop_tema_ano = pd.read_csv('csv/quant_tema_ano.csv', sep=";")

import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Inicialização do plotly dash no tema Slate
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    # "margin-left": "5rem",
    # "margin-right": "2rem",
    # "padding": "2rem 1rem",
    # "display": "inline-block"
}

sidebar = html.Div(
    [
        html.H4("Sidebar"),
        html.Hr(),
        html.P(
            "A simple sidebar", className="lead"
        ),
        html.A(
            "grafico de linhas", href='#linhas'
        ),
    ],

    style=SIDEBAR_STYLE,
)

# app.layout = dbc.Container([
maindiv = html.Div(
    id='firstDiv',

    children=[
        # Título
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
                html.Hr(),
                html.P(''),
                html.H4('Participações',
                        className='text-center text-primary, mb-4'),
                html.P(
                    'O objetivo desta primeira parte do trabalho é explorar a participação dos deputados de cada espéctro'
                    'político nas votações realizadas na câmara.'),
                html.P(
                    'As seguintes visualizações mostrarão em uma perspectiva tempora, as participações, sendo que o usuário poderá escolher para'
                    'algumas delas sobre quais anosele gostaria de fazer a análise'),
                # select ano
                dcc.Dropdown(id='select',
                             multi=False,
                             value=2003,
                             options=[{'label': str(x), 'value': int(x)} for x in sorted(frame['ano'].unique())]
                             ),

                # Gráfico participação em votação por região
                dcc.Graph(id='bar-chart',
                          figure={}
                          ),
            ],
                width={'size': 8}
            )
        ], justify='center'
        ),

        dbc.Row([
            dbc.Col([
                html.P(''),
                html.H4('Teste',
                        className='text-center text-primary, mb-4'),
                # range ano
                dcc.RangeSlider(2003, 2022, 1, id='range-ano',
                                value=[2003, 2022],
                                marks={i: str(i) for i in range(2003, 2022 + 1)}
                                ),
                # Gráfico participação em votação por região
                dcc.Graph(id='mudanca',
                          figure={}
                          ),
            ],
                width={'size': 8}
            )
        ], justify='center'
        ),

        dbc.Row([
            dbc.Col([
                html.A(id='linhas'),
                html.P(''),
                # Gráfico participação em votação por região
                dcc.Graph(id='line-chart',
                          figure={}
                          ),
            ],
                width={'size': 8}
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
                width={'size': 8}
            )
        ], justify='center'
        ),

        dbc.Row([
            dbc.Col([
                html.H2("Quantidade de votações ao longo dos anos"),
                dcc.Graph(id='votacoes-por-ano-chart',
                          figure={}
                          )
            ],
                width={'size': 8}
            )
        ], justify='center'
        ),

        dbc.Row([
            dbc.Col([
                html.H2("Temas das propostas por ano"),

                html.P(''),
                #select ano
                dcc.Dropdown(id='select-tema-prop',
                            multi=False,
                            value= 2021,
                            options=[{'label': str(x), 'value': int(x)} for x in sorted(df_prop_tema_ano['Ano'].unique())]
                            ),

                dcc.Graph(id='tema-proposta-por-ano-chart',
                        figure={}
                )
            ],
            width={'size':8}
            )
        ], justify='center'
        ),

        dbc.Row([
            dbc.Col([
                html.H1('Gastos na camara'),
                dcc.Tabs(id="tabs_gastos", value="tab_ano",

                         children=[
                             dcc.Tab(label="Por ano", value="tab_ano"),
                             dcc.Tab(label="Total", value="tab_total"),
                         ]
                         ),
                html.Div(id="tabs_gastos_content")
            ],
                width={'size': 8}
            )
        ], justify="center"
        ),

    ], style=CONTENT_STYLE

)

app.layout = html.Div([sidebar, maindiv])


# Gráfico
@app.callback(
    Output('bar-chart', 'figure'),
    Input('select', 'value')
)
def update_graph(ano):
    dv_ano = frame[frame['ano'] == ano]
    regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=regioes,
        y=dv_ano[dv_ano['posicionamento'] == 'Esquerda']['voto_norm'],
        name='Esquerda',
        marker_color=px.colors.qualitative.Plotly[1]
    ))
    fig.add_trace(go.Bar(
        x=regioes,
        y=dv_ano[dv_ano['posicionamento'] == 'Centro-esquerda']['voto_norm'],
        name='Centro-esquerda',
        marker_color=px.colors.qualitative.Plotly[9]
    ))
    fig.add_trace(go.Bar(
        x=regioes,
        y=dv_ano[dv_ano['posicionamento'] == 'Centro']['voto_norm'],
        name='Centro',
        marker_color='rgb(113, 192, 85)'
    ))
    fig.add_trace(go.Bar(
        x=regioes,
        y=dv_ano[dv_ano['posicionamento'] == 'Centro-direita']['voto_norm'],
        name='Centro-direita',
        marker_color='rgb(64, 184, 234)'
    ))
    fig.add_trace(go.Bar(
        x=regioes,
        y=dv_ano[dv_ano['posicionamento'] == 'Direita']['voto_norm'],
        name='Direita',
        marker_color='rgb(67, 111, 182)'
    ))

    fig.update_layout(
        title=f"Participações em Votações por Região\nem {ano} Separado por Posicionamento ",
        xaxis_title="Região",
        yaxis_title="Número de Participações em Votação em Porcentagem (%)",
        legend_title="Posicionamento"
    )

    return fig


@app.callback(
    Output('mudanca', 'figure'),
    Input('range-ano', 'value')
)
def update_graph(ano):
    inicial = ano[0]
    final = ano[-1]
    links, nodes = utils.sankey(mudanca, inicial, final)
    data_trace = dict(
        type='sankey',
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        orientation="h",
        valueformat=".0f",
        node=dict(
            pad=10,
            # thickness = 30,
            line=dict(
                color="black",
                width=0
            ),
            label=nodes['Label'].dropna(axis=0, how='any'),
            color=nodes['Color']
        ),
        link=dict(
            source=links['Source'].dropna(axis=0, how='any'),
            target=links['Target'].dropna(axis=0, how='any'),
            value=links['Value'].dropna(axis=0, how='any'),
            color=links['Link Color'].dropna(axis=0, how='any'),
        )
    )

    layout = dict(
        title=f"Mudança de posicionamento dos políticos votantes\nentre {inicial} e {final}",
        height=772,
        font=dict(
            size=15), )

    fig = go.Figure(data=data_trace)
    fig.update_layout(layout)
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
        xaxis_title_text="Eleições",
        xaxis_type="category",
        xaxis_tickangle=-45,
        yaxis_title_text="Número de <b>novos</b> deputados"
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
                             value=2021,
                             options=[{'label': str(x), 'value': int(x)} for x in
                                      sorted(df_gastos_por_ano_deputado["numAno"].unique())]
                             ),
                dcc.Dropdown(id='id_ano_raking',
                             multi=False,
                             value=10,
                             options=[{'label': str(x), 'value': int(x)} for x in [3, 4, 5, 6, 8, 10, 12, 15, 20]]
                             ),
                dcc.Graph(id='chart_ano_gastos',
                          figure={}
                          )
            ],
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
                             value=10,
                             options=[{'label': str(x), 'value': int(x)} for x in [3, 4, 5, 6, 8, 10, 12, 15, 20]]
                             ),
                dcc.Graph(id='chart_total_gastos',
                          figure={}
                          )
            ],
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
        yaxis_title = "<b>Nome</b> do partido"

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
        yaxis={'categoryorder': 'total ascending'},
        title_text=title,
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
        title = f"Gastos dos {ranking} partidos que mais gastaram de 2008 até hoje (2022)"
        yaxis_title = "<b>Nome</b> do partido"

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
        yaxis={'categoryorder': 'total ascending'},
        title_text=title,
        title_x=0.5,
        xaxis_title_text=xaxis_title,
        yaxis_title_text=yaxis_title
    )
    return fig


@app.callback(
    Output('votacoes-por-ano-chart', 'figure'),
    Input('select', 'value')
)
def grafico_votacoes_por_ano(dummy):
    fig = px.bar(df_votacoes_por_ano, x="ano", y="idVotacao")
    fig.update_layout(
        plot_bgcolor="white",
        title_x=0.5,
        title_text="Total de votações ao longo dos anos",
        xaxis_title_text="<b>Ano</b>",
        yaxis_title_text="<b>Quantidade de votações</b>",
    )
    fig.update_traces(marker_color='#30ade3')
    fig.update_layout(xaxis = {'type' : 'category'})
       
    return fig

@app.callback(
    Output('tema-proposta-por-ano-chart', 'figure'),
    Input('select-tema-prop', 'value')
)

def tema_proposta_por_ano(ano):

    df = df_prop_tema_ano[df_prop_tema_ano["Ano"] == ano].sort_values(by=["Contagem"], ascending=True)

    fig = px.bar(df, y='Tema', x='Contagem',barmode='group')
    fig.update_traces(marker_color='#30ade3')

    fig.update_layout(
        plot_bgcolor="white",
        title_x=0.5,
        yaxis_title_text="<b>Tema</b>",
        xaxis_title_text="<b>Propostas</b>"
    )
    #fig.update_xaxes(tickangle=45)

       
    return fig

"""
@app.callback(
    Output('ano-proposta-por-tema-chart', 'figure'),
    Input('select-ano-tema', 'value')
)

def ano_proposta_por_tema(tema):

    df = df_prop_tema_ano[df_prop_tema_ano["Tema"] == tema].sort_values(by=["Ano"], ascending=True)

    fig = px.bar(df, y='Ano', x='Contagem',barmode='group')
    fig.update_traces(marker_color='#30ade3')

    fig.update_layout(
        plot_bgcolor="white",
        title_x=0.5,
        yaxis_title_text="<b>Tema</b>",
        xaxis_title_text="<b>Propostas</b>"
    )
    #fig.update_xaxes(tickangle=45)

       
    return fig
"""

if __name__ == '__main__':
    app.run_server()
