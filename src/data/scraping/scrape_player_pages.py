from bs4 import BeautifulSoup as bs
import codecs
import pandas as pd
from os import listdir

page_dir = "../../../data/external/player_pages/"

filelist = listdir(page_dir)

additional_player_rows_info = []

dict_list = []
test_careers = []
sgids = []
career_stats = []

def parse_player_info(soup):
	player_dict = {}

	#add player name and country to player dict
	player_dict.update({'FullName': soup.find_all("div", "scrumPlayerName")[0].contents[0].strip()})
	player_dict.update({'Country': soup.find_all("div", "scrumPlayerCountry")[0].contents[0].strip()})


	#cycle through scrumPlayerDesc divs and add relevant present facts to player dict
	player_info_div = soup.find_all("div", "scrumPlayerDesc")

	for tag in player_info_div:
		
		if "Full name" in tag.text:
			full_name = tag.find('b').next_sibling.strip()
			player_dict.update({'full_name2': full_name,
								'forename': full_name.split()[0],
								'surname': full_name.split()[-1]
								})
		elif "Born" in tag.text:
			
			born_string = tag.find('b').next_sibling.strip().strip('?')
			print(born_string, flush=True)
			player_dict.update({'born': tag.find('b').next_sibling.strip()})

			born_spl_comma = born_string.split(',')			
			born_spl_space = born_string.split(' ')	

			try:
				if born_spl_space[0] == "(guess:": #special case 
					player_dict.update({'born_where': " ".join(born_spl_space[3:])})

				elif born_spl_space[0] == "date": #case for "date unknown"
					pass

				elif born_spl_space[0] == "circa": #change circa years to years
					player_dict.update({'born_date': born_spl_space[1]})

				elif born_spl_comma[0].isdigit(): # only year is listed, no location
					player_dict.update({'born_date': born_spl_comma[0],
									'born_where': "".join(born_spl_comma[1:])
									}) 
				elif born_spl_space[1].strip(',').isdigit() and born_spl_space[2].strip(',').isdigit(): # full date and location listed
					player_dict.update({'born_date': "".join(born_spl_comma[:2]),
								'born_where': ",".join(born_spl_comma[2:]).strip()
								   })
			except:
				player_dict.update({'born_date': "dateERROR",
								'born_where': "whereERROR"
								   })

		elif "Died" in tag.text:
			player_dict.update({'died': tag.find('b').next_sibling.strip()})
		elif "Major teams" in tag.text:
			player_dict.update({'major_teams': tag.find('b').next_sibling.strip().split(", ")})
		elif "Position" in tag.text:
			player_dict.update({'position': tag.find('b').next_sibling.strip().split(", ")})
		elif "Height" in tag.text:
			player_dict.update({'height': tag.find('b').next_sibling.strip()})
		elif "Weight" in tag.text:
			player_dict.update({'weight': tag.find('b').next_sibling.strip()})



	#find test career table and process
	test_career_tab = soup.find_all(lambda tag:tag.name == "table" and "Test career" in tag.text)
	if len(test_career_tab):
		table_df = pd.read_html(str(test_career_tab[0]), index_col=0)[0]
		test_careers.append(table_df)

	#find career stats table and process
	career_stat_tab = soup.find_all(lambda tag:tag.name == "table" and "Career statistics" in tag.text)
	if len(career_stat_tab):
		for row in career_stat_tab[0].find_all("tr", class_="data2"):
			if "test debut" in row.text.lower():
				player_dict.update({'test_debut': row.find("a").attrs['href'].strip('.html').split('/')[-1]})
				#print(row.find("a").attrs['href'].strip('.html').split('/')[-1])
			if "last test" in row.text.lower():
				player_dict.update({'last_debut': row.find("a").attrs['href'].strip('.html').split('/')[-1]})
				#print(row.find("a").attrs['href'].strip('.html').split('/')[-1])
			if "only test" in row.text.lower():
				player_dict.update({'only_test': row.find("a").attrs['href'].strip('.html').split('/')[-1]})
				#print(row.find("a").attrs['href'].strip('.html').split('/')[-1])	

	#find url to player image and add to dictionary
	player_img_info = soup.find_all("img", alt="player portrait")
	if len(player_img_info):
	    player_dict.update({'ImgURL': player_img_info[0]['src']})

	return player_dict

for file in filelist[:3000]:
	sg_id = int(file.strip(".html"))
	#print(f"Parsing player id {str(sg_id)}", flush=True)
	sgids.append(sg_id)
	page_html = codecs.open(f"{page_dir}{file}", 'r').read()
	soup = bs(page_html, 'html.parser')
	ele_dict = parse_player_info(soup)
	ele_dict.update({'player_sgid': sg_id})
	dict_list.append(ele_dict)



career_df = pd.concat(test_careers, keys=sgids)
career_df.to_csv('../../../data/external/raw_scraped_player_careers.csv')

players_df = pd.DataFrame(dict_list)
players_df.to_csv('../../../data/external/raw_scraped_player_pages_data.csv')