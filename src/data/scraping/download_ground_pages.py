from bs4 import BeautifulSoup as bs
import requests
import sys
import pandas as pd
import time

import sgmgmt

page_type = 'ground'
path = f"../../../data/external"
base_url = f"http://stats.espnscrum.com/statsguru/rugby/{page_type}"

#get list of sgids
id_list = pd.read_csv("../../../data/processed/wrangled_all_matches.csv")['ground_sgid'].unique().tolist()

for sg_id in id_list:

	if sg_id == 0:
		continue

	filepath = f"{path}/{page_type}_pages/{str(sg_id)}.html"

	if not sgmgmt.check_page_saved(filepath):
		print(f"Saving {page_type} {sg_id} from website")
		match_url = f"{base_url}/{sg_id}.html?view=scorecard"
		html = sgmgmt.request_page(match_url).text
		sgmgmt.save_page_html(html, filepath)
		time.sleep(15)
	else:
		print(f"Page already saved for {page_type} {sg_id}")	
