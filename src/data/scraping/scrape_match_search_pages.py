from bs4 import BeautifulSoup as bs
from os import listdir
import codecs
import pandas as pd
import re

path = "../../../data/external/search_pages/"

search_pages = []

dfs = []

def get_match_compnent_ids(soup, search_string):
	links = soup.find_all(lambda tag:tag.name == "a" and search_string in tag.text)
	urls = [a['href'] for a in links]
	ids = [url.strip(".html").split('/')[-1] for url in urls]
	return ids

for fn in listdir(path):
	print(f"Processing page {fn.strip('html').split('=')[-1]}", flush=True)
	filepath = path + fn
	html = codecs.open(filepath, 'r').read()
	soup = bs(html, 'html.parser')

	table_df = pd.read_html(str(soup.find_all("table", class_="engineTable")[1]))[0]

	table_df['Opposition'] = table_df['Opposition'].apply(lambda opp: opp[2:])
	table_df.drop('Unnamed: 14', axis=1, inplace=True)

	table_df = table_df.assign(Team1Id = get_match_compnent_ids(soup, "Team home page"),
				Team2Id = get_match_compnent_ids(soup, "Opposition home page"),
				MatchId = get_match_compnent_ids(soup, "Match details"), 
				PitchId = get_match_compnent_ids(soup, "Ground profile"))

	dfs.append(table_df)

search_df = pd.concat(dfs, ignore_index=True, sort=False)
search_df.to_csv("../../../data/external/" + 'raw_all_match_search_pages.csv')