
#coding: utf-8
ROOT_PLAYER_ID = "account.fe0852919ef34c508b1bc1efef652045"
CHICKEN_DINNER_BONUS = 5

import pdb
from helper.PubgApiHelper import PubgHelper
from helper.MatchDataHelper import MatchDataHelper
from config import API_TOKEN
from players_data import *

api_helper = PubgHelper(API_TOKEN)

matches = api_helper.get_user_matches(ROOT_PLAYER_ID)

player_list = [player_achuan, player_longdd, player_mu, player_lv]
# player_list = [player_achuan, player_sanjia, player_mu, player_ghost]

flight_count = 0
all_zero_count = 0

for match_data in matches:
    match_id = match_data.get("id") 
    if match_id is None:
        continue

    kill_sum = 0
    all_zero = True
    is_chiken_dinner = False 

    match_data = api_helper.get_match(match_id)

    match_helper = MatchDataHelper(ROOT_PLAYER_ID, match_data["included"])
    play_datas = match_helper.get_roster_participant()
    all_in_team = True
    for play_data in play_datas:
        is_chiken_dinner = is_chiken_dinner or play_data.get("winPlace") == 1
        print(play_data)
        in_team = False
        for player in player_list:
            if player.name == play_data["name"]:
                in_team = True
                kill_num = play_data.get('kills')
                all_zero = all_zero and kill_num == 0 
                if play_data.get('deathType') == 'alive':
                    processed_kill_num += CHICKEN_DINNER_BONUS
                processed_kill_num = player.perprocess_kill(kill_num)
                kill_sum += processed_kill_num
                player.current_kill = processed_kill_num
                # continue
        all_in_team = all_in_team and in_team
    if not all_in_team: 
        break
    flight_count += 1
    if all_zero:
        all_zero_count += 1
    for player in player_list:
        player.score += player.current_kill * 4 - kill_sum 
    print(' '.join(["{} :{} ".format(player.avatar, player.score) for player in player_list]))
    print("✈️ :{}  💎💎 :{} ".format(flight_count, all_zero_count))


