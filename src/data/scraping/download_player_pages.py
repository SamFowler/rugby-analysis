from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys
import time

sys.stdout = open('../../../logs/scrape_player_pages_log', 'w')

player_data = pd.read_csv('../../../data/external/scraped_england_player_data.csv')
player_data = player_data[['SG_PlayerID','Website']]

for ind, row in player_data.iterrows():
	
	time.sleep(2)
	if (ind != 0) and (ind % 35 == 0):
		print("Waiting 30 seconds...", flush=True)
		time.sleep(30)

	player_id = row['SG_PlayerID']
	player_url = row['Website']

	response = requests.get(player_url)
	if response:
		print(f'Writing player page {player_id}', flush=True)
		page = response.text
		soup = bs(page, 'html.parser')
		file = open(f"../../../data/external/player_pages/{player_id}.html", "w")
		file.write(soup.prettify())
		file.close()

	else:
		print(f'Player {player_id} does not exist', flush=True)

sys.stdout.close()