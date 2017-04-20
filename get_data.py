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

match_days = range(1, 18) + [9999, 99999, 999999]
data = []

for i in match_days:
    # Each match day is stored in a different url, so we need to make one
    # request for each match_day.
    url = "http://www.vivoelfutbol.com.mx/jornada.php?to=1&te=110&jo=" + str(i)
    page = requests.get(url)
    tree = html.fromstring(page.content)
    games = tree.xpath('/html//div[@class="calendario"]/div[@class="det"]')
   
    for game in games:
        game_dict = {'j': i}
        for dp in game:
            if (dp.attrib['class'] in ['eql', 'eqv']):
                game_dict[dp.attrib['class']] = dp[0].text
            if (dp.attrib['class'] == 'mar'):
                gol, gov = dp[0].text.split('-')
                game_dict['gol'] = int(gol)
                game_dict['gov'] = int(gov)
        data.append(game_dict)

columns = ['j', 'eql', 'eqv', 'gol', 'gov']
df = pd.DataFrame.from_records(data, columns=columns)
df.to_csv('apertura_2016.csv')