import json
import requests

class PubgHelper:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_user_matches(self, player_id):
        headers = {
            "accept": "application/vnd.api+json",
            "Authorization": "Bearer {}".format(self.api_key)   
        }
        res = requests.get('https://api.pubg.com/shards/steam/players/{}'.format(player_id), headers=headers)

        res_json = json.loads(res.content)
        matches = res_json["data"]["relationships"]["matches"]["data"]
        return matches

    def get_match(self, match_id):
        headers = {
            "accept": "application/vnd.api+json"
        }
        res = requests.get('https://api.pubg.com/shards/steam/matches/{}'.format(match_id), headers=headers)

        res_json = json.loads(res.content)
        matches = res_json
        return matches 