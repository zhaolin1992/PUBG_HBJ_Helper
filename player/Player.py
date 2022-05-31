class Player:
    def __init__(self, data_json):
        self.name = data_json.get('name')
        self.avatar = data_json.get('avatar')
        self.concede = data_json.get('concede') # if 1=0 the concede is 1
        self.offset_score = data_json.get('offset_score')
        self.score = 0
        self.current_kill = 0
        
        self.kills = 0
        self.damage = 0
        self.walkDistance = 0
        self.headShots = 0
    def perprocess_kill(self, kill_num):
        if kill_num >= self.concede:
            return kill_num - self.concede
        return kill_num