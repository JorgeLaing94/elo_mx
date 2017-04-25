# -*- coding: utf-8 -*-
"""
Scrapes website to get results for every game of the Apertura 2016 season of
Liga MX.

@author: jlain
"""

from lxml import html
import requests
import pandas as pd
import numpy as np

match_days = range(1, 21) + [88, 9999, 99999, 999999]
seasons = range(1, 32) + [55, 57, 66, 70, 80, 82, 92, 96, 105, 110, 120]
# Season 24 and below should also have matchday 88
# Some seasons have matchdays 9999991 and 9999992 (Campeon de campeones)
# Season 16 and below have 

data = []

for s in seasons:
    for i in match_days:
        # Each match day is stored in a different url, so we need to make one
        # request for each match_day.
        url = "http://www.vivoelfutbol.com.mx/jornada.php?to=1&te={0}&jo={1}"\
        .format(s, i)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        games = tree.xpath('/html//div[@class="calendario"]/div[@class="det"]')
       
        for game in games:
            game_dict = {'t':s, 'j': i}
            for dp in game:
                if (dp.attrib['class'] in ['eql', 'eqv']):
                    game_dict[dp.attrib['class']] = dp[0].text
                if (dp.attrib['class'] == 'mar'):
                    gol, gov = dp[0].text.split('-')
                    game_dict['gol'] = int(gol)
                    game_dict['gov'] = int(gov)
            data.append(game_dict)

columns = ['t', 'j', 'eql', 'eqv', 'gol', 'gov']
df = pd.DataFrame.from_records(data, columns=columns)
df.to_csv('full_data.csv')