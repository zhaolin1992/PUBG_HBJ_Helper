import json
import pdb
import dateutil

from soupsieve import match

class MatchDataHelper:
    def __init__(self, root_player_id, match_data):
        self.root_player_id = root_player_id
        self.match_data = match_data.get('included')
        self.match_info = match_data.get('data')
    
    def is_chicken_dinner(self):
        roster = self.get_roster()
        if roster is None:
            return False
        try:
            return roster.get('attributes').get("won") == "true"
        except:
            return False 

    def get_root_player_participant(self):
        try:
            filtered_participant = [ data_item for data_item in self.match_data if data_item['type'] == 'participant' and data_item.get('attributes')['stats']['playerId'] == self.root_player_id]
        except:
            return None 
        if len(filtered_participant) == 1:
            return filtered_participant[0]
        return None

    def get_roster(self):
        participant = self.get_root_player_participant()
        if participant is None:
            return None
        participant_id = participant.get('id')
        if participant_id is not None:
            try:
                filtered_roster = [d for d in self.match_data if d['type'] == 'roster' and participant_id in [pd.get('id') for pd in d.get('relationships').get('participants').get('data')] ]
            except:
                return None 
            if len(filtered_roster) == 1:
                return filtered_roster[0]
        return None 

    def get_roster_participant(self):
        roster = self.get_roster()
        if roster is None:
            return None
        try:
            participant_ids = [pd.get('id') for pd in roster.get('relationships').get('participants').get('data')]
            squad_data = [ data_item.get('attributes').get('stats') for data_item in self.match_data if data_item['type'] == 'participant' and data_item.get('id') in participant_ids]
        except:
            return None
        return squad_data

    def get_match_time(self):
        if self.match_info.get('attributes') is None:
            return None
        if self.match_info.get('attributes').get('createdAt') is None:
            return None
        try:
            return int(dateutil.parser.parse(self.match_info.get('attributes').get('createdAt')).timestamp())
        except:
            return None
