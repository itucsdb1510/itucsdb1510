



from sre_constants import CATEGORY_DIGIT

class Store:
    def __init__(self):
        self.teams = {}

        self.last_key = 0
        self.experiences= {}
        self.exp_key = 0

        self.team_last_key = 0
        self.races = {}
        self.race_last_key = 0
        self.categories={}
        self.category_last_key=0

        self.admins = {}
        self.admin_last_key = 0

        self.announcements={}
        self.announcement_last_key=0

    def add_team(self, team):
        self.team_last_key += 1
        self.teams[self.team_last_key] = team

    def delete_team(self, key):
        del self.teams[key]
        self.team_last_key -= 1

    def get_team(self, key):
        return self.teams[key]

    def get_teams(self):
        return sorted(self.teams.items())

    def addMember(self, key):
        self.teams[key].member_count = 5

    def add_announcement(self, announcement):
        self.announcement_last_key += 1
        self.announcements[self.announcement_last_key] = announcement

    def delete_announcement(self, key):
        del self.announcements[key]
        self.announcement_last_key -= 1

    def get_announcement(self, key):
        return self.announcements[key]

    def get_announcements(self):
        return sorted(self.announcements.items())















    def add_experience(self, experience):

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









    def add_race(self, race):
        self.race_last_key += 1
        self.races[self.race_last_key] = race

    def delete_race(self, key):
        del self.races[key]
        self.race_last_key -= 1

    def get_race(self, key):
        return self.races[key]

    def get_races(self):
        return sorted(self.races.items())

    def count_category(self,category):
        self.category_count+=1

    def add_category(self, category):
        self.category_last_key +=1
        self.categories[self.category_last_key]= category

    def delete_category(self, key):
        del self.categories[key]
        self.category_last_key-=1

    def get_category(self,key):
        return self.categories[key]

    def get_categories(self):
        return sorted(self.categories.items())



    def add_admin(self, admin):
        self.admin_last_key += 1
        self.admins[self.admin_last_key] =admin

    def delete_admin(self, key):
        del self.admins[key]
        self.admin_last_key -= 1

    def get_admin(self, key):
        return self.admins[key]

    def get_admins(self):
        return sorted(self.admins.items())

    def addMember(self, key):
        self.admins[key].member_count = 5

