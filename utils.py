import pandas as pd
import numpy as np
def sankey (nome_pos, inicial, final):

    A = nome_pos[nome_pos['ano'] == inicial]
    B = nome_pos[nome_pos['ano'] == final]
    C = pd.merge(A, B, how='inner', on=['nome'])
    C['posicionamento_id_y'] = C['posicionamento_id_y'] + 5

    C = C.groupby(
        ['posicionamento_x', 'posicionamento_id_x', 'posicionamento_y', 'posicionamento_id_y']).count().reset_index()[
        ['posicionamento_id_x', 'posicionamento_id_y', 'nome', 'posicionamento_x']]
    C.rename(columns={'posicionamento_id_x': 'Source', 'posicionamento_id_y': 'Target', 'nome': 'Value'}, inplace=True)

    conditions = [
        (C['posicionamento_x'] == 'Esquerda'),
        (C['posicionamento_x'] == 'Centro-esquerda'),
        (C['posicionamento_x'] == 'Centro'),
        (C['posicionamento_x'] == 'Centro-direita'),
        (C['posicionamento_x'] == 'Direita')
    ]
    cor = ['rgba(237, 14, 14, 0.2)', 'rgba(230, 223, 21, 0.2)', 'rgba(18, 227, 22, 0.2)', 'rgba(167, 17, 209, 0.2)',
           'rgba(14, 37, 237, 0.2)']
    C['Link Color'] = np.select(conditions, cor)

    nodes = [['ID', 'Label', 'Color'],
             [0, 'Esquerda', '#cf2b1f'],
             [1, 'Centro-esquerda', '#b5b20d'],
             [2, 'Centro', '#4ab50d'],
             [3, 'Centro-direita', '#ad0db5'],
             [4, 'Direita', '#0d1eb5'],
             [5, 'Esquerda', '#cf2b1f'],
             [6, 'Centro-esquerda', '#b5b20d'],
             [7, 'Centro', '#4ab50d'],
             [8, 'Centro-direita', '#ad0db5'],
             [9, 'Direita', '#0d1eb5']]

    headers = nodes.pop(0)
    df_nodes = pd.DataFrame(nodes, columns=headers)

    return C, df_nodes