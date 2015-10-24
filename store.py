class Store:
    def __init__(self):
        self.teams = {}
        self.last_key = 0

    def add_team(self, team):
        self.last_key += 1
        self.teams[self.last_key] = team

    def delete_team(self, key):
        del self.teams[key]

    def update_team(self, key, title, year):
        self.teams[key].title = title
        self.teams[key].year = year

    def get_team(self, key):
        return self.teams[key]

    def get_teams(self):
        return sorted(self.teams.items())