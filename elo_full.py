# -*- coding: utf-8 -*-
"""
First pass at calculating elo scores for each time throughout the league.

@author: jlain
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import plotly.offline as py
import plotly.graph_objs as go

df = pd.DataFrame.from_csv('full_data.csv')

names = df['eql'].unique()
keys = dict(zip(names,range(0, len(names))))
elo_scores = pd.DataFrame(columns=['ds', 'team', 't', 'j', 'elo'])


for name in names:
    elo_scores = elo_scores.append(
        [{'ds':None, 'team':name, 't':None, 'j':None, 'elo':1500}],
         ignore_index=True
        )

def exp_result(r1, r2):
    return 1.0 / (1 + 10**((r2-r1) / 400))

k = 20

def transform_j(j):
    if (j == 9999):
        return 18
    if (j == 99999):
        return 19
    if (j== 999999):
        return 20
    return j



for i in range(len(df)):
    t, j, eql, eqv, gol, gov, date = df.iloc[i]
    j = transform_j(j)
    result = 0.5
    if (gol > gov):
        result = 1
    if (gol < gov):
        result = 0

    elo_eql = elo_scores[elo_scores['team'] == eql].tail(1)['elo'].iloc[0]
    elo_eqv = elo_scores[elo_scores['team'] == eqv].tail(1)['elo'].iloc[0]

    expl = exp_result(elo_eql, elo_eqv)

    elo_eql = elo_eql + k * (result - expl)
    elo_eqv = elo_eqv + k * (expl - result)

    elo_scores.loc[len(elo_scores)] =\
        {'ds':date, 'team':eql, 't':t, 'j':j, 'elo':elo_eql}
    elo_scores.loc[len(elo_scores)] =\
        {'ds':date, 'team':eqv, 't':t, 'j':j, 'elo':elo_eqv}

elo_scores[elo_scores['ds'].notnull()].to_csv(path_or_buf='elo_scores.csv')

# #PLOT
# title = 'Elo Rankings - Liga MX'
# traces = []
#
# for team in names:
#     to_plot = elo_scores[elo_scores['ds'].notnull()].query("team == '{0}'"\
#         .format(team))
#     traces.append(go.Scatter(
#         x=list((to_plot['ds'])),
#         y=list(to_plot['elo']),
#         mode='lines',
#         connectgaps=False,
#         name=team,
#     ))
#
# layout = dict(title = title,
#               xaxis = dict(title = 'Date'),
#               yaxis = dict(title = 'Elo Score'),
#               )
#
# len(traces)
# fig = dict(data=traces, layout=layout)
# py.iplot(fig, filename='styled-line')
