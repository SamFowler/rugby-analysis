from bs4 import BeautifulSoup as bs
import requests
import time
import sgmgmt

url = 'http://stats.espnscrum.com/statsguru/rugby/stats/index.html?class=1;filter=advanced;orderby=player;size=200;template=results;type=player;view=match'

save_path = f"../../../data/external/player_stats_by_match_pages"

first_page_url = f"{url};page=1"
filepath = save_path + sgmgmt.get_filepath(first_page_url)

print("Fetching first page from website")
html = sgmgmt.request_page(first_page_url).text

if not sgmgmt.check_page_saved(filepath):
		print(f"Saving page 1 of search", flush=True)
		sgmgmt.save_page_html(html, filepath)
		time.sleep(60)

soup = bs(html, 'html.parser')
num_pages = int(soup.find(lambda tag: tag.name=="span" and "Page" in tag.text).text.split()[-1])

for page_num in range(1,num_pages+1):

	page_url = f"{url};page={page_num}"

	filepath = save_path + sgmgmt.get_filepath(page_url)
	if not sgmgmt.check_page_saved(filepath):
		print(f"Saving page {page_num} of {num_pages+1} from search", flush=True)
		html = sgmgmt.request_page(page_url).text
		sgmgmt.save_page_html(html, filepath)
		time.sleep(90)
	else:
		print(f"Page already saved for search {page_num}", flush=True)

