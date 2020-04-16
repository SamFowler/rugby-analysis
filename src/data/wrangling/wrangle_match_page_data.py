import pandas as pd
import re
def remove_prefix(text, prefix):
	return text[text.startswith(prefix) and len(prefix):]

def collect_point_scorers(data_row, team):
	scorers_dict = {}
	for item in data_row:
		if "Tries  " in item:
			scorers_dict.update({f'{team}_t_scrs': remove_prefix(", ".join(remove_prefix(item, 'Tries  ').split(', ')), 'none')})
		elif "Cons  " in item:
			scorers_dict.update({f'{team}_c_scrs': remove_prefix(", ".join(remove_prefix(item, 'Cons  ').split(', ')), 'none')})
		elif "Pens  " in item:
			scorers_dict.update({f'{team}_p_scrs': remove_prefix(", ".join(remove_prefix(item, 'Pens  ').split(', ')), 'none')})
		elif "Drops  " in item:
			scorers_dict.update({f'{team}_d_scrs': remove_prefix(", ".join(remove_prefix(item, 'Drops  ').split(', ')), 'none')})
		elif "Goals from a mark  " in item:
			scorers_dict.update({f'{team}_g_scrs': remove_prefix(", ".join(remove_prefix(item, 'Goals from a mark  ').split(', ')), 'none')})
	return scorers_dict

def collect_players_details(data_row, key_prefix):
	players_dict = {}

	## todo: tidy this mess, must be easier way
	positions = re.sub(r"[0-9]", "", data_row.iloc[0].split(': {')[2][:-4]).strip("': ").replace("'", '').replace(': ', '').replace('nan','').replace(',','').strip()
	positions = [position.strip() for position in positions.split()]

	names = re.sub(r"[0-9]", "", data_row.iloc[0].split(': {')[3]).strip("': }").split("', : '")

	numbers_list = []
	for string in data_row.iloc[0].split(': {')[1].split(", ")[:-1]:
		num_str = string.strip('}').split(': ')[1]
		if num_str.isdigit():
			numbers_list.append(num_str)

	players_dict.update({f'{key_prefix}_nums': ", ".join(numbers_list),
						f'{key_prefix}_positions': ", ".join(positions),
						f'{key_prefix}_names': ", ".join(names)
						})

	return players_dict


def collect_notes_details(data_row):
	notes_dict = {}
	for item in data_row:
		if "Ground name  " in item:
			notes_dict.update({'ground_name': item.replace('Ground name  ', '')})
		elif "Attendance  " in item:
			notes_dict.update({'attendance': int(item.replace('Attendance  ', ''))})
		elif "Referee  " in item:
			notes_dict.update({'referee': item.replace('Referee  ', '').split('  (')[0]})
			if len(item.replace('Referee  ', '').split('  (')) > 1:
				notes_dict.update({'referee_from': item.replace('Referee  ', '').split('  (')[1].rstrip(')')})
		elif " points  " in item:
			notes_dict.update({'tour_points': item.split(' points  ')[1]})
		elif "Point scoring rules  " in item:
			notes_dict.update({'scoring_rules': item.replace('Points scoring rules  ', '')})

	return notes_dict

raw_data_path = '../../../data/external/'
data_save_path = '../../../data/processed/'
match_search_data_filename = 'raw_scraped_match_pages.csv'
data_save_filename = 'wrangled_match_pages.csv'

raw_df = pd.read_csv(raw_data_path + match_search_data_filename)

match_ids = raw_df['MatchId'].unique()

match_dicts = []

for match_id in match_ids[:1000]:
	match_dict = {}

	print(match_id)
	row = raw_df[raw_df['MatchId'] == match_id]

	#convert and split match page title into tour and stadium names, and date and time
	tour_split = "".join(row['Tour'].iloc[0].split(' - ')[1:]).split(', ')
	match_dict.update({'match_id': match_id,
						'tour': row['Tour'].iloc[0].split(' - ')[0],
						'stadium': tour_split[0],
						'date': tour_split[1]
						})
	if len("".join(row['Tour'].iloc[0].split(' - ')[1:]).split(', ')) > 2:
		match_dict.update({'local_time': tour_split[2].strip(' local'),
						   'gmt_time': tour_split[3].strip(' GMT'),
						})


	# convert and split match page scoreline into team names and full time and half time scores
	if (row['ScoreLine'].iloc[0][:-5].split(' - ')[0][-1] == 'G') or (not '(' in row['ScoreLine'].iloc[0][:-5]):
		#old scoreline (e.g. Ireland 2G - 0G England (FT))
		# OR modern scoreline without any halftime scored (e.g. Scotland 6 - 0 England (FT))
		match_dict.update({'t1_name':  " ".join(row['ScoreLine'].iloc[0][:-5].split(' - ')[0].split(' ')[:-1]),
							't1_ft_sc': row['ScoreLine'].iloc[0][:-5].split(' - ')[0].split(' ')[-1],
							't2_name':  " ".join(row['ScoreLine'].iloc[0][:-5].split(' - ')[1].split(' ')[1:]),
							't2_ft_sc': row['ScoreLine'].iloc[0][:-5].split(' - ')[1].split(' ')[0],
							})

	else:
		#modern scoreline (e.g. England (6) 9 - 16 (3) France (FT))
		match_dict.update({'t1_name':  " ".join(row['ScoreLine'].iloc[0][:-5].split(' - ')[0].split(' ')[:-2]),
							't1_ft_sc': row['ScoreLine'].iloc[0][:-5].split(' - ')[0].split(' ')[-1],
							't1_ht_sc':  row['ScoreLine'].iloc[0][:-5].split(' - ')[0].split(' ')[-2].strip('()'),
							't2_name':  " ".join(row['ScoreLine'].iloc[0][:-5].split(' - ')[1].split(' ')[2:]),
							't2_ft_sc': row['ScoreLine'].iloc[0][:-5].split(' - ')[1].split(' ')[0],
							't2_ht_sc':  row['ScoreLine'].iloc[0][:-5].split(' - ')[1].split(' ')[1].strip('()'),
							})
	
	#convert match page scoring table into try / pen / conv / etc scores for each team
	scorers_dict = collect_point_scorers(row['Team1_scoring'].iloc[0].split("'"), team='t1')
	match_dict.update(scorers_dict)
	scorers_dict = collect_point_scorers(row['Team2_scoring'].iloc[0].split("'"), team='t2')
	match_dict.update(scorers_dict)

	#bring list of player and replacement ids across
	match_dict.update({'t1_player_ids': str(row['Team1_ids'].iloc[0]).strip('[]').replace("'", ''),
					't2_player_ids': str(row['Team2_ids'].iloc[0]).strip('[]').replace("'", ''),
					't1_rep_ids': str(row['Team1_rep_ids'].iloc[0]).strip('[]').replace("'", ''),
					't2_rep_ids': str(row['Team1_rep_ids'].iloc[0]).strip('[]').replace("'", '')
					})

	#list players, replacements, and positions
	match_dict.update(collect_players_details(row['Team1_players'], key_prefix='t1_players'))
	match_dict.update(collect_players_details(row['Team2_players'], key_prefix='t2_players'))

	if row['Team1_rep_players'].any():
		match_dict.update(collect_players_details(row['Team1_rep_players'], key_prefix='t1_rep_plyrs'))
	if row['Team2_rep_players'].any():
		match_dict.update(collect_players_details(row['Team2_rep_players'], key_prefix='t2_rep_plyrs'))


	#wrangle "Notes" tab of match page (for referee, stadium, etc)
	#print(row['Notes'].iloc[0].lstrip("['").rstrip("']").split("', '"))
	match_dict.update(collect_notes_details(row['Notes'].iloc[0].lstrip("['").rstrip("']").replace("\"", "'").split("', '")))

	match_dicts.append(match_dict)
	
#save list of matct dicts to csv 
df = pd.DataFrame(match_dicts)
df.to_csv(data_save_path + data_save_filename)