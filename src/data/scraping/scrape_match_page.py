from bs4 import BeautifulSoup as bs
import codecs
import pandas as pd
import lxml 
from os import listdir
from sys import stdout

stdout = open('../../../logs/scrape_match_pages.log', 'w')


match_page_dir = "../../../data/external/match_pages/"

filelist = listdir(match_page_dir)
#filelist = ['182003.html', '20866.html']
match_dicts = []



for file in filelist:

	match_id = int(file.strip(".html"))
	print(f'Processing {match_id}', flush=True)

	match_page_html = codecs.open(f"{match_page_dir}{file}", 'r').read()

	soup = bs(match_page_html, 'html.parser')

	match_dict = {}


	overview = soup.find_all(lambda tag: tag.name == 'td' and
									tag.get('class') == ['liveSubNavText'])[0]
	overview = ' '.join(overview.text.split())

	score_line = soup.find_all(lambda tag: tag.name == 'td' and
									tag.get('class') == ['liveSubNavText1'])[0].text
	score_line = ' '.join(score_line.split())

	match_dict.update({'MatchId': match_id,
						'Tour': overview,
						'ScoreLine': score_line
				})

	tabbertabs = soup.find_all("div", class_="tabbertab")

	tab_titles = []
	tab_dicts = {}
	team_stats_found = False

	for tab in tabbertabs:
		tab_title = tab.find("h2").contents[0].strip()
		tab_titles.append(tab_title)

		html = str(tab.table)
		if "Teams" in tab_title:
			table_df = pd.read_html(str(tab.table))[0]
			

			teams = pd.read_html(str(tab.table), match="Team", skiprows=1)

			match_dict.update({'Team1_scoring': table_df.iloc[:,0].to_dict(),
									'Team2_scoring': table_df.iloc[:,1].to_dict(),
									})

			for index, team_div in enumerate(tab.table.find_all('div', class_='divTeams')):
				team_dict = {}

				team = pd.read_html(str(team_div), skiprows=1)
				team_players = team[0].to_dict()

				urls = team_div.find_all('a')
				team_player_ids = [(url.attrs['href'].strip('.html').split('/')[-1]) for url in urls[0:len(team[0])]]
				
				match_dict.update({f'Team{index+1}_players': team_players, 
									f'Team{index+1}_ids': team_player_ids
									})

				if "Replacements" in team_div.text:
					rep_team_players = team[1].to_dict()
					rep_player_ids = [(url.attrs['href'].strip('.html').split('/')[-1]) for url in urls[len(team[0]):]]

					match_dict.update({f'Team{index+1}_rep_players': rep_team_players, 
									f'Team{index+1}_rep_ids': rep_player_ids
									})

		elif "Match stats" in tab_title:
			table_df = pd.read_html(str(tab.table), index_col=1, header=0)[0]		
			match_dict.update({'Match_stats': table_df.to_dict()})
			#print(table_df.to_dict())
			#stat_titles = [f"Team1_{ele}" for ele in table_df.iloc[:,1].tolist()] + [f"Team2_{ele}" for ele in table_df.iloc[:,2].tolist()]
			#stats = table_df.iloc[:,0].tolist() + table_df.iloc[:,2].tolist()
			#match_dict.update(zip(stat_titles, stats))

		elif "Notes" in tab_title:
			table_df = pd.read_html(str(tab.table))[0]
			match_dict.update({'Notes': table_df.iloc[:,0].tolist()})

		elif "stats" in tab_title:
			table_df = pd.read_html(str(tab.table), header=0)[0]
			dict_title = 'Team1_stats' if not team_stats_found else 'Team2_stats'
			team_stats_found = True
			match_dict.update({dict_title: table_df.to_dict()})

		elif 'Timeline' in tab_title:
			table_df = pd.read_html(str(tab.table), header=0, index_col=0)[0]
			match_dict.update({'Timeline': table_df.to_dict()})

		elif 'Summary' in tab_title:
			table_df = pd.read_html(str(tab.table), header=0, index_col=0)[0]
			match_dict.update({'Summary': table_df.to_dict()})

		match_dict.update({'match_tab_titles': tab_titles})


		
	match_dicts.append(match_dict)

match_df = pd.DataFrame(match_dicts)    
match_df.to_csv("../../../data/external/scraped_match_pages.csv")

		