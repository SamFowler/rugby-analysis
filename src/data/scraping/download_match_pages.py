from bs4 import BeautifulSoup as bs
import requests
import sys
import pandas as pd
import time

import sgmgmt

path = "../../../data/external/"

search_df = pd.read_csv(f"{path}match_search_pages.csv")

match_id_list = search_df['MatchId'].tolist()

for match_id in match_id_list:

	filepath = f"{path}match_pages/{str(match_id)}.html"

	if not sgmgmt.check_page_saved(filepath):
		print(f"Saving match {match_id} from website")
		match_url = f"http://stats.espnscrum.com/statsguru/rugby/match/{match_id}.html?view=scorecard"
		html = sgmgmt.request_page(match_url).text
		sgmgmt.save_page_html(html, filepath)
		time.sleep(0.5)
	else:
		print(f"Page already saved for match {match_id}")	


