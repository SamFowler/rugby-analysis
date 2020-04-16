from bs4 import BeautifulSoup as bs
import codecs
import pandas as pd

player_page_dir = "../../../data/external/player_pages/"

player_data = pd.read_csv("../../../data/external/scraped_england_player_data.csv")

additional_player_rows_info = []

def parse_player_info(soup):
	player_dict = {}

	#add player name and country to player dict
	player_dict.update({'FullName': soup.find_all("div", "scrumPlayerName")[0].contents[0].strip()})
	player_dict.update({'Country': soup.find_all("div", "scrumPlayerCountry")[0].contents[0].strip()})


	#cycle through scrumPlayerDesc divs and add relevant present facts to player dict
	player_info_div = soup.find_all("div", "scrumPlayerDesc")

	for tag in player_info_div:
	    
	    if "Full name" in tag.text:
	        player_dict.update({'FullName2': tag.find('b').next_sibling.strip()})
	    elif "Born" in tag.text:
	        player_dict.update({'Born': tag.find('b').next_sibling.strip(),
	                        'BornDate': "".join(tag.find('b').next_sibling.strip().split(",")[0:-1]),
	                        'BornWhere': tag.find('b').next_sibling.strip().split(",")[-1].strip()
	                           })
	    elif "Major teams" in tag.text:
	        player_dict.update({'MajorTeams': tag.find('b').next_sibling.strip().split(", ")})
	    elif "Position" in tag.text:
	        player_dict.update({'Position': tag.find('b').next_sibling.strip()})
	    elif "Height" in tag.text:
	        player_dict.update({'Height': tag.find('b').next_sibling.strip()})
	    elif "Weight" in tag.text:
	        player_dict.update({'Weight': tag.find('b').next_sibling.strip()})

	#find url to player image and add to dictionary
	player_img_info = soup.find_all("img", alt="player portrait")
	if len(player_img_info):
	    player_dict.update({'ImgURL': player_img_info[0]['src']})

	return player_dict


for index, row in player_data.iterrows():
	print(f"Parsing player id {row['SG_PlayerID']}", flush=True)

	player_page_html = codecs.open(f"{player_page_dir}{row['SG_PlayerID']}.html", 'r').read()

	player_soup = bs(player_page_html, 'html.parser')

	player_dict = parse_player_info(player_soup)

	additional_player_rows_info.append(player_dict)


players_df = pd.DataFrame(additional_player_rows_info)
players_df.to_csv('../../../data/external/england_additional_player_data.csv')