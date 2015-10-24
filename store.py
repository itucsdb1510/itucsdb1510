class Store:
    def __init__(self):
        self.teams = {}
        self.last_key = 0

    def add_team(self, team):
        self.last_key += 1
        self.teams[self.last_key] = team

    def delete_team(self, key):
        del self.teams[key]
        self.last_key -= 1

    def get_team(self, key):
        return self.teams[key]

    def get_teams(self):
        return sorted(self.teams.items())

    def addMember(self, key):
        self.teams[key].member_count = 5