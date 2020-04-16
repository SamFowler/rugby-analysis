import pandas as pd
import datetime
import calendar

def convert_date(date_string):
	if date_string is '-':
		return 'unknown'
	comps = date_string.split()
	return f"{comps[2]}-{str(list(calendar.month_abbr).index(comps[1]))}-{comps[0]}"

raw_csv_filename = 'raw_all_match_search_pages.csv'
raw_data_path = '../../../data/external/'
data_save_path = '../../../data/processed/'
data_save_filename = 'wrangled_all_matches.csv'

raw_df = pd.read_csv(raw_data_path + raw_csv_filename)

match_ids = raw_df['MatchId'].unique()

pro_dict = {'match_sgid': match_ids}

match_dicts = []

for match_id in match_ids:
	match_dict = {}
	print(f'Processing match_id: {match_id}', flush=True)

	raw_match_rows = raw_df[raw_df['MatchId'] == match_id]
	res = raw_match_rows['Result'].iloc[0]

	match_dict.update({
	'match_id': match_id,
	'date': convert_date(raw_match_rows['Match Date'].to_list()[0]),
	'ground': raw_match_rows['Ground'].iloc[0],
	'ground_sgid': raw_match_rows['PitchId'].iloc[0],
	#'attendence': 'todo',
	#'referee': 'todo',
	#'tourney': 'todo',
	#'tourney_round': 'todo',
	't1_name': raw_match_rows['Team'].iloc[0],
	't1_id': raw_match_rows['Team1Id'].iloc[0],
	#t1_home': 'todo',
	't1_res': ('W' if res=='won' else 'D' if res=='draw' else 'L' if res=='lost' else '-'),
	't1_for': raw_match_rows['For'].iloc[0],
	#'t1_for_half': 'todo',
	't1_aga': raw_match_rows['Aga'].iloc[0],
	't1_diff': raw_match_rows['Diff'].iloc[0],
	't1_tries': raw_match_rows['Tries'].iloc[0],
	#'t1_t_scorers': 'todo',
	't1_convs': raw_match_rows['Conv'].iloc[0],
	#'t1_c_scorers': 'todo',
	't1_pens': raw_match_rows['Pens'].iloc[0],
	#'t1_p_scorers': 'todo',
	't1_drops': raw_match_rows['Drop'].iloc[0],
	#'t1_d_scorers': 'todo',
	't1_gfms': raw_match_rows['GfM'].iloc[0],
	#'t1_gfm_scorers': 'todo',
	#'t1_all_player_ids': 'todo',
	#'t1_starter_ids': 'todo',
	#'t1_replacement_ids': 'todo'
	##todo: t1_stats_(kick conversion rates, scrums, lineouts won etc..)
	})

	if len(raw_match_rows) == 2:
		match_dict.update({
			't2_name': raw_match_rows['Team'].iloc[1],
			't2_id': raw_match_rows['Team1Id'].iloc[1],
			#'t2_home': 'todo',
			't2_res': ('W' if res=='won' else 'D' if res=='draw' else 'L' if res=='lost' else '-'),
			't2_for': raw_match_rows['For'].iloc[1],
			#'t2_for_half': 'todo',
			't2_aga': raw_match_rows['Aga'].iloc[1],
			't2_diff': raw_match_rows['Diff'].iloc[1],
			't2_tries': raw_match_rows['Tries'].iloc[1],
			#'t2_t_scorers': 'todo',
			't2_convs': raw_match_rows['Conv'].iloc[1],
			#'t2_c_scorers': 'todo',
			't2_pens': raw_match_rows['Pens'].iloc[1],
			#'t2_p_scorers': 'todo',
			't2_drops': raw_match_rows['Drop'].iloc[1],
			#'t2_d_scorers': 'todo',
			't2_gfms': raw_match_rows['GfM'].iloc[1],
			#'t2_gfm_scorers': 'todo',
			#'t2_all_player_ids': 'todo',
			#'t2_starter_ids': 'todo',
			#'t2_replacement_ids': 'todo'
			##todo: t2_stats_(kick conversion rates, scrums, lineouts won etc..
		})

	match_dicts.append(match_dict)


processed_df = pd.DataFrame(match_dicts)
processed_df.to_csv(data_save_path + data_save_filename)