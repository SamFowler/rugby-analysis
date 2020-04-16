from bs4 import BeautifulSoup as bs
import requests
import sys
import os.path
import codecs
import time

import sgmgmt

#sys.stdout = open('../../../logs/download_match_pages.log', 'w')

url = 'http://stats.espnscrum.com/statsguru/rugby/stats/index.html?class=1;filter=advanced;orderby=date;size=200;template=results;type=team;view=match'
#url = "http://stats.espnscrum.com/statsguru/rugby/stats/index.html?class=1;filter=advanced;orderby=difference;page=1;size=200;spanmin1=27+Mar+1860;spanval1=span;team=1;template=results;type=team;view=match"
path = "../../../data/external/search_pages/"

first_page_url = f"{url};page=1"
filename = sgmgmt.get_filepath(first_page_url)
filepath = path + filename

print("Fetching first page from website")
html = sgmgmt.request_page(first_page_url).text
soup = bs(html, 'html.parser')

num_pages = int(soup.find(lambda tag: tag.name=="span" and "Page" in tag.text).text.split()[-1])

for page_num in range(1,num_pages+1):

	page_url = f"{url};page={page_num}"

	filepath = path + sgmgmt.get_filepath(page_url)
	if not sgmgmt.check_page_saved(filepath):
		print(f"Saving page {page_num} of {num_pages+1} from search", flush=True)
		html = sgmgmt.request_page(page_url).text
		sgmgmt.save_page_html(html, filepath)
		time.sleep(5)
	else:
		print(f"Page already saved for match {page_num}", flush=True)

