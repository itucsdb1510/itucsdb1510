

class Store:
    def __init__(self):
        self.teams = {}
        self.last_key = 0
        self.experiences= {}
        self.exp_key = 0

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
        
        
        
     ########################EXPERINCES###########################   
        
        
        
        
    def add_experience(self, team):
        self.exp_key += 1
        self.experiences[self.exp_key] = experience
        
    def delete_experience(self, key):
        del self.experiences[key]
        self.exp_key -= 1
        
    def get_experience(self, key):
        return self.experiences[key]
    
    def get_experiences(self):
        return sorted(self.experiences.items())
    
    
    def update_experience(self, key, title, username, start, finish, period):
       self.experiences[key].title = title
       self.experiences[key].username=username
       self.experiences[key].start=start
       self.experiences[key].finish=finish
       self.experiences[key].period=period





    
    
    