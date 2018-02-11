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
import unicodedata as uni
import dateparser

match_days = list(range(1, 21)) + [88, 9999, 99999, 999999]
seasons = list(range(1, 32)) +\
[55, 57, 66, 70, 80, 82, 92, 96, 105, 110, 120, 123, 132]
# Season 24 and below should also have matchday 88
# Some seasons have matchdays 9999991 and 9999992 (Campeon de campeones)
# Season 16 and below have

data = []

for s in seasons:
    print("geting season {0}...".format(s))
    for i in match_days:
        print("  ...match day {0}".format(i))
        # Each match day is stored in a different url, so we need to make one
        # request for each match_day.
        url = "http://www.vivoelfutbol.com.mx/jornada.php?to=1&te={0}&jo={1}"\
        .format(s, i)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        # elements are games and dates
        elements = tree.xpath('/html//div[@class="calendario"]/div[@class="det" or @class="tif"]')
        d = ""

        for el in elements:
            if (el.attrib['class'] == 'tif'):
                # get date
                d =  uni.normalize('NFKD', el.text)\
                     .encode('ascii', 'ignore').strip()
                d = str(d).split(" ", 1)[1]
                # parse and format
                d = dateparser.parse(d)
                d = d.strftime("%Y-%m-%d")
            else:
                game_dict = {'t':s, 'j': i, 'date': d}
                for dp in el:
                    if (dp.attrib['class'] in ['eql', 'eqv']):
                        game_dict[dp.attrib['class']] = dp[0].text
                    if (dp.attrib['class'] == 'mar'):
                        try:
                            gol, gov = dp[0].text.split('-')
                            game_dict['gol'] = int(gol)
                            game_dict['gov'] = int(gov)
                            data.append(game_dict)
                        except ValueError:
                            print("Game has not happened yet!")
                            break

columns = ['t', 'j', 'eql', 'eqv', 'gol', 'gov', 'date']
df = pd.DataFrame.from_records(data, columns=columns)
df.to_csv('full_data.csv')
