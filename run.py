from gc import callbacks
import pandas as pd
import utils

### ------***CÓDIGO DO DASHBOARD USANDO PLOTLY DASH***------ ###

mudanca = pd.read_csv('csv/mudanca_posicionamento.csv')
frame = pd.read_csv('csv/participacao_percent.csv')
line = pd.read_csv('csv/posicionamento_deputados.csv')
votoOrientacao = pd.read_csv('csv/porcentagem_orientacao.csv')
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
import dash_daq as daq

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
        html.H4("Visualizações"),
        html.Hr(),
        html.A(
            "Participações em Votações por Região", href='#link-participacao'
        ),

        html.Hr(),
        html.A(
            "Mudança de Posicionamento dos Políticos Votantes", href='#link-cordas'
        ),

        html.Hr(),

        html.A(
            "Deputados Votantes por Posicionamento", href='#link-deputados-posicionamento'
        ),

        html.Hr(),

        html.A(
            "Novos Deputados por Sexo", href='#link-sexo'
        ),

        html.Hr(),

        html.A(
            "Quantidade de Votações ao Longo dos Anos", href='#link-votacoes'
        ),

        html.Hr(),

        html.A(
            "Gastos na câmara", href='#link-gastos'
        ),

        html.Hr(),

        html.A(
            "Temas Propostos por Ano", href='#link-propostas'
        ),

        html.Hr(),

        html.A(
            "Porcentagem de Votos Contra ou a Favor da Orientação do Partido", href='#link-orientacao'
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
                html.A(id='link-participacao'),
                #select ano
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
                html.A(id='link-cordas'),
                html.P(''),
                html.Hr(),
                # range ano
                dcc.RangeSlider(2003, 2022, 1, id='range-ano',
                                value=[2003, 2022],
                                marks={i: str(i) for i in range(2003, 2022 + 1)},
                                included=False
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
                html.A(id='link-deputados-posicionamento'),
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
                html.A(id='link-orientacao'),
                html.P(''),
                #Gráfico participação em votação por região
                dcc.Graph(id='votos-orientacao',
                        figure={}
                        ),
            ],
            width={'size':8}
            )
        ], justify='center'
        ),

        dbc.Row([
            dbc.Col([
                html.A(id='link-sexo'),
                html.H2("Novos deputados por sexo"),
                html.P("O gráfico a seguir mostra a diferença gigantesca entre o número de novos deputados "
                    "comparados ao de novas deputadas, que começou a ter um crescimento, mesmo que pequeno, apenas depois do fim "
                    "da ditadura (1985)."
                ),
                html.P("É possível observar também a primeira deputada eleita, Carlota Pereira de Queirós, em 1933. "
                    "Entretanto, mesmo sendo eleita, o período 1933-1982 somam apenas 17 deputadas, enquanto que em 1986 "
                    "houve 24 deputadas eleitas, ou seja, um período de quase 50 anos onde se havia o tardio direito de votar e "
                    "ser eleita, um único ano foi capaz de superá-lo. Infelizmente, ainda é um valor extremamente baixo, expondo "
                    "a falta de abertura para novas mulheres na política."
                ),
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
                html.A(id='link-votacoes'),
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
                dcc.Tabs(id="tabs_temas", value="tab_ano",

                         children=[
                             dcc.Tab(label="Por ano", value="tab_ano"),
                             dcc.Tab(label="Todos", value="tab_total"),
                         ]
                         ),
                html.Div(id="tabs_temas_content")
            ],
                width={'size': 8}
            )
        ], justify="center"
        ),

        dbc.Row([
            dbc.Col([
                html.A(id='link-gastos'),
                html.H1('Gastos na Câmara'),
                html.P('Para ter uma noção dos gastos dos deputados, observando gastos fora do normal, '
                    'abaixo foi proposto um gráfico onde mostra os N deputados que mais gastaram no ano escolhido '
                    'ou de um intervalo de período em [2003, 2022]. O mesmo é possível observar para partidos, categorias '
                    'e o valor pago para fornecedores.'
                ),
                html.P("Alguns fatos interessantes que podem ser observados: O deputado Chico das Verduras (PRP) apresentou "
                    "um gasto totalmente fora do normal nos anos 2013 e 2014. Uma curiosidade é que procurando saber mais sobre o deputado, "
                    "encontramos notícias de sua prisão à mando do STF em julho de 2016."
                ),
                html.P('Outra coisa que pode ser notado é o valor enorme gasto nas categorias "Divulgação de atividade parlamenta" e '
                    '"Passagem área", somando mais de R$1 bilhão de gastos. Dos fornecedores que mais receberam dinheiro '
                    'dos deputados estão as companhias aéreas TAM e GOL.'
                ),
                dcc.Tabs(id="tabs_gastos", value="tab_ano",

                         children=[
                             dcc.Tab(label="Por ano", value="tab_ano"),
                             dcc.Tab(label="Intervalo", value="tab_intervalo"),
                         ]
                         ),
                html.Div(id="tabs_gastos_content")
            ],
                width={'size': 8}
            )
        ], justify="center"
        ),

    ], style = CONTENT_STYLE

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

    fig.update_layout(
        plot_bgcolor="#f5f5f5",
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
    
    fig.update_layout(
        plot_bgcolor="#f5f5f5",
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

    fig.update_layout(
        plot_bgcolor="#f5f5f5",
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

    fig.update_layout(
        width=30,
        plot_bgcolor="#f5f5f5",
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
                            options=gastos_tipos,
                            style={
                                "margin-bottom": '15px',
                            }
                            ),
                daq.NumericInput(id='id_ano_ranking',
                            min=3,
                            max=2000,
                            value= 15,
                            size=100,
                            label="Quantidade no ranking",
                            labelPosition='bottom'
                            ),

                dcc.Graph(id='chart_ano_gastos',
                        figure={}
                        ),
                html.Div(
                    dcc.Slider(id='id_ano_gasto',
                        min=2008,
                        max=2022,
                        included=False,
                        step=None,
                        marks={i:str(i) for i in range(2008, 2022 + 1)},
                        value=2022
                    ),
                    style={
                        "margin-bottom": "20px",
                    }
                )
                        
            ],
        )], justify='center'
    ),
    elif tab == 'tab_intervalo':
        return dbc.Row([
            dbc.Col([
                html.P(''),
                dcc.Dropdown(id='id_total_tipo_gasto',
                            multi=False,
                            value="Gastos por deputados",
                            options=gastos_tipos,
                            style={
                                "margin-bottom": '15px',
                            }
                            ),
                daq.NumericInput(id='id_total_ranking',
                            min=3,
                            max=2000,
                            value= 15,
                            size=100,
                            label="Quantidade no ranking",
                            labelPosition='bottom'
                            ),
                dcc.Graph(id='chart_total_gastos',
                        figure={}
                        ),

                html.Div(
                    dcc.RangeSlider(id='id_ano_gasto_range',
                        min=2008,
                        max=2022,
                        step=None,
                        marks={i:str(i) for i in range(2008, 2022 + 1)},
                        value=[2008, 2022]
                    ),
                    style={
                        "margin-bottom": "20px",
                    }
                )
                ],
            )
        ], justify='center'
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
    Input('id_ano_ranking', 'value')
)
def gera_grafico_gastos_por_ano_(tipo_gasto="Gastos por deputados", ano=2021, ranking=15):
    df = None
    title = ""
    yaxis_title = ""
    xaxis_title = "<b>Valor líquido</b> gasto"

    if tipo_gasto == "Gastos por deputados":
        df = df_gastos_por_ano_deputado
        yaxis_title = "<b>Nome</b> do deputado"
    elif tipo_gasto == "Gastos por partido":
        df = df_gastos_por_ano_partido
        yaxis_title="<b>Nome</b> do partido"
    elif tipo_gasto == "Gastos por categoria":
        df = df_gastos_por_ano_categoria
        yaxis_title = "<b>Nome</b> da categoria"
    elif tipo_gasto == "Recebimento por fornecedores":
        df = df_gastos_por_ano_fornecedor
        yaxis_title = "<b>Nome</b> do fornecedor"
        xaxis_title = "<b>Valor líquido</b> recebido"


    df = df[df["numAno"] == ano]
    len_max = len(df) - 1
    ranking = len_max if ranking > len_max else ranking
    df = df[0:ranking]

    if tipo_gasto == "Gastos por deputados":
        title = f"Gastos dos {ranking} deputados que mais gastaram em {ano}"
    elif tipo_gasto == "Gastos por partido":
        title = f"Gastos dos {ranking} partidos que mais gastaram em {ano}"
    elif tipo_gasto == "Gastos por categoria":
        title = f"Gasto das {ranking} categorias que mais houve gasto em {ano}"
    elif tipo_gasto == "Recebimento por fornecedores":
        title = f"Quantidade de dinheiro que os {ranking} fornecedores que mais receberam em {ano}"

    fig = px.bar(df, x='vlrLiquido', y=map_tipos_y[tipo_gasto], color='vlrLiquido', color_continuous_scale=px.colors.sequential.Tealgrn)
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        title_text= title,
        title_x=0.5,
        xaxis_title_text=xaxis_title,
        yaxis_title_text=yaxis_title,
        legend_title_text="",
    )
    fig.update_yaxes(visible=ranking<=22, showticklabels=ranking<=22)
    fig.update_layout(
        plot_bgcolor="#f5f5f5",
    )
    
    return fig


@app.callback(
    Output('chart_total_gastos', 'figure'),
    Input('id_total_tipo_gasto', 'value'),
    Input('id_total_ranking', 'value'),
    [Input('id_ano_gasto_range', 'value')]
)
def gera_grafico_gastos_totais(tipo_gasto="Gastos por deputados", ranking=15, range_ano=[2008, 2022]):
    df = None
    title = ""
    yaxis_title = ""
    xaxis_title = "<b>Valor líquido</b> gasto"

    if tipo_gasto == "Gastos por deputados":
        df = df_gastos_por_ano_deputado
        yaxis_title = "<b>Nome</b> do deputado"
    elif tipo_gasto == "Gastos por partido":
        df = df_gastos_por_ano_partido
        yaxis_title="<b>Nome</b> do partido"
    elif tipo_gasto == "Gastos por categoria":
        df = df_gastos_por_ano_categoria
        yaxis_title = "<b>Nome</b> da categoria"
    elif tipo_gasto == "Recebimento por fornecedores":
        df = df_gastos_por_ano_fornecedor
        yaxis_title = "<b>Nome</b> do fornecedor"
        xaxis_title = "<b>Valor líquido</b> recebido"

    df = df[df["numAno"] >= range_ano[0]]
    df = df[df["numAno"] <= range_ano[1]]
    df = df.groupby([map_tipos_y[tipo_gasto]], as_index=False).sum().sort_values(by=["vlrLiquido"], ascending=False)
    len_max = len(df) - 1
    ranking = len_max if ranking > len_max else ranking
    df = df[0:ranking]

    if tipo_gasto == "Gastos por deputados":
        title = f"Gastos dos {ranking} deputados que mais gastaram de {range_ano[0]} até {range_ano[1]}"
    elif tipo_gasto == "Gastos por partido":
        title =  f"Gastos dos {ranking} partidos que mais gastaram de {range_ano[0]} até {range_ano[1]}"
    elif tipo_gasto == "Gastos por categoria":
        title = f"Gasto das {ranking} categorias que mais houve gasto de {range_ano[0]} até {range_ano[1]}"
    elif tipo_gasto == "Recebimento por fornecedores":
        title = f"Quantidade de dinheiro que os {ranking} fornecedores que mais receberam de {range_ano[0]} até {range_ano[1]}"

    fig = px.bar(df, x='vlrLiquido', y=map_tipos_y[tipo_gasto], color='vlrLiquido', color_continuous_scale=px.colors.sequential.Tealgrn)
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        title_text= title,
        title_x=0.5,
        xaxis_title_text=xaxis_title,
        yaxis_title_text=yaxis_title
    )
    fig.update_yaxes(visible=ranking<=22, showticklabels=ranking<=22)
    fig.update_layout(
        plot_bgcolor="#f5f5f5",
    )
    
    return fig


@app.callback(
    Output('votacoes-por-ano-chart', 'figure'),
    Input('select', 'value')
)
def grafico_votacoes_por_ano(dummy):
    fig = px.bar(df_votacoes_por_ano, x="ano", y="idVotacao")
    fig.update_layout(
        plot_bgcolor="#f5f5f5",
        title_x=0.5,
        title_text="Total de votações ao longo dos anos",
        xaxis_title_text="<b>Ano</b>",
        yaxis_title_text="<b>Quantidade de votações</b>",
    )
    fig.update_traces(marker_color='#30ade3')
    fig.update_layout(xaxis = {'type' : 'category'})

    return fig

@app.callback(
    Output('votos-orientacao', 'figure'),
    Input('select', 'value')
)

def grafico_orietancao(dummy):
    c_map = {
        'favor': '#436fb6',
        'contra': '#ed1e24'
    }

    order=['Esquerda', 'Centro-esquerda', 'Centro', 'Centro-direita', 'Direita']
    fig = px.bar(votoOrientacao, x="Posicionamento", y="% Votos", color="Orientação", 
                barmode='group', category_orders={'Posicionamento': order}, 
                color_discrete_map=c_map)

    fig.update_layout(
        title_text="Porcentagem de Votos Contra ou a Favor da Orientação do Partido",
        title_x=0.5,
    )
    fig.update_layout(
        plot_bgcolor="#f5f5f5",
    )
       
    return fig

@app.callback(
    Output("tabs_temas_content", 'children'),
    Input("tabs_temas", 'value')
)
def gera_tabs_temas(tab):
    if tab == 'tab_ano':
        return dbc.Row([
            dbc.Col([
                html.A(id='link-propostas'),
                html.H2("Temas das Propostas por Ano"),
                html.P(''),

                dcc.Dropdown(id='select-tema-prop',
                            multi=False,
                            value= 2021,
                            options=[{'label': str(x), 'value': int(x)} for x in sorted(df_prop_tema_ano['Ano'].unique())]
                            ),

                dcc.Graph(id='tema-proposta-por-ano-chart',
                        figure={}
                )
            ],
            )
        ], justify='center'
        )   
    elif tab == 'tab_total':
        return dbc.Row([
            dbc.Col([
                html.A(id='link-propostas'),
                html.H2("Temas das Propostas - Todos os anos"),
                html.P(''),

                dcc.Graph(id='tema-todos-anos-chart',
                        figure={}
                )
            ],
            )
        ], justify='center'
        )

@app.callback(
    Output('tema-proposta-por-ano-chart', 'figure'),
    Input('select-tema-prop', 'value')
)

def tema_proposta_por_ano(ano):

    df = df_prop_tema_ano[df_prop_tema_ano["Ano"] == ano].sort_values(by=["Contagem"], ascending=True)

    fig = px.bar(df, y='Tema', x='Contagem',barmode='group')
    fig.update_traces(marker_color='#30ade3')

    fig.update_layout(
        plot_bgcolor="#f5f5f5",
        title_x=0.5,
        yaxis_title_text="<b>Tema</b>",
        xaxis_title_text="<b>Propostas</b>"
    )
    # fig.update_xaxes(tickangle=45)
       
    return fig

@app.callback(
    Output('tema-todos-anos-chart', 'figure'),
    Input('select', 'value')
)

def tema_todos_anos_anos(dummy):
    fig = px.line(df_prop_tema_ano, x="Ano", y="Contagem", color='Tema')
    fig.update_layout(
        plot_bgcolor="#f5f5f5",
        title_x=0.5,
        yaxis_title_text="<b>Tema</b>",
        xaxis_title_text="<b>Propostas</b>"
    )

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
