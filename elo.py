# -*- coding: utf-8 -*-
"""
First pass at calculating elo scores for each time throughout the league.

@author: jlain
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame.from_csv('apertura_2016.csv')

names = df['eql'].unique()
keys = dict(zip(names,range(0, len(names))))

r = np.zeros([18, len(df['j'].unique()) + 1])
r[:, 0] += 1500

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
    j, eql, eqv, gol, gov = df.iloc[i]
    j = transform_j(j)
    result = 0.5
    if (gol > gov):
        result = 1
    if (gol < gov):
        result = 0
    expl = exp_result(r[keys[eql], j-1], r[keys[eqv], j-1])
    r[keys[eql], j] = r[keys[eql], j-1] + k * (result - expl)
    r[keys[eqv], j] = r[keys[eqv], j-1] + k * (expl - result)


# Plot results
fig = plt.figure(1)
for team in keys:
    plt.plot(range(21), r[keys[team]], label=team)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4,
           ncol=4, mode="expand", borderaxespad=0.)
plt.ylim([1400, 1600])
fig.subplots_adjust(top=.8)
plt.grid(True)
plt.show()

