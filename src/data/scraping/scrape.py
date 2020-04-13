from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

"""
Scrape espnscrum statsguru website for England player data
"""


player_tables = []

for page in range(8):
    url = f"http://stats.espnscrum.com/statsguru/rugby/stats/index.html?class=1;filter=advanced;orderby=matches;page={page+1};size=200;spanmin1=27+Mar+1860;spanval1=span;team=1;template=results;type=player"
    page = requests.get(url).text
    soup = bs(page, 'html.parser')
    player_tables.append(soup.find_all("tr", class_="data1"))



player_rows_list = []

for player_table in player_tables:
    for player_entry in player_table:
        player_data = player_entry.find_all("td")

        player_dict = {'Name':player_data[0].contents[0].contents[0],
                      'SG_PlayerID':player_data[0].contents[0]['href'].split(".")[0].split('/')[-1],
                      'StartYr':player_data[1].contents[0][0:4],
                      'EndYr':player_data[1].contents[0][5:10],
                      'Matches':player_data[2].contents[0].contents[0],
                      'Starts':player_data[3].contents[0],
                      'Subs':player_data[4].contents[0],
                      'Pts':player_data[5].contents[0],
                      'Tries':player_data[6].contents[0],
                      'Conv':player_data[7].contents[0],
                      'Pens':player_data[8].contents[0],
                      'Drop':player_data[9].contents[0],
                      'GfM':player_data[10].contents[0],
                      'Won':player_data[11].contents[0],
                      'List':player_data[12].contents[0],
                      'Lost':player_data[13].contents[0],
                      '%':player_data[14].contents[0],
                       'Website':"http://en.espn.co.uk"+player_data[0].contents[0]['href']
                           }
        player_rows_list.append(player_dict)
    players_df = pd.DataFrame(player_rows_list)
    players_df.to_csv('england_player_data.csv')


df = pd.read_csv('../../../data/external/scraped_england_player_data.csv')
df