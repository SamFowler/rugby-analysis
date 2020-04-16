from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys
import time
import sgmgmt

sys.stdout = open('../../../logs/download_player_pages.log', 'w')

page_type = 'player'
path = f"../../../data/external"
base_url = f"http://stats.espnscrum.com/statsguru/rugby/{page_type}"

#get list of sgids
#id_list = pd.read_csv("../../../data/processed/wrangled_all_matches.csv")['ground_sgid'].unique().tolist()
id_list = range(1000,16000)

for sg_id in id_list:

	if sg_id == 0:
		continue

	filepath = f"{path}/{page_type}_pages/{str(sg_id)}.html"

	if not sgmgmt.check_page_saved(filepath):
		print(f"Saving {page_type} {sg_id} from website")
		match_url = f"{base_url}/{sg_id}.html?view=scorecard"
		if sgmgmt.request_page(match_url):
			html = sgmgmt.request_page(match_url).text
			sgmgmt.save_page_html(html, filepath)
			time.sleep(15)
		else:
			print(f"Could not fetch page {page_type} {sg_id}, skipping")
			continue
		
	else:
		print(f"Page already saved for {page_type} {sg_id}")	