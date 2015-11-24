from sre_constants import CATEGORY_DIGIT
from _operator import length_hint
import psycopg2 as dbapi2
from team import Team
from bike import Bike
from cycroute import Cycroute
from experience import Experience
from activity import Activity
from race import Race
from _datetime import date


class Store:
    def __init__(self, app):
        self.app = app
        self.teams = {}
        self.team_last_key = None

        self.experiences = {}
        self.exp_key = 0

        self.races = {}
        self.race_last_key = 0

        self.categories = {}
        self.category_last_key = 0

        self.admins = {}
        self.admin_last_key = 0

        self.cycroutes = {}
        self.cycroute_last_key = 0

        self.bikes = {}
        self.bike_last_key = 0

        self.announcements = {}
        self.announcement_last_key = 0

        self.topics = {}
        self.topic_last_key = 0

        self.basicmembers = {}
        self.basicmember_last_key = 0

        self.professionalmembers = {}
        self.professionalmember_last_key = 0

        self.activities = {}
        self.activity_last_key = None

#TEAM
    def add_team(self, team):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO TEAM (NAME, SCORE, FOUNDER, YEAR) VALUES (%s, %s, %s, %s) RETURNING TEAM.ID"
            cursor.execute(query, (team.title, int(team.score), team.founder, int(team.year)))
            connection.commit()
            self.team_last_key = cursor.fetchone()[0]


    def delete_team(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM TEAM WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_team(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT NAME, SCORE, FOUNDER, YEAR FROM TEAM WHERE (ID = %s)"
            cursor.execute(query, (key,))
            name, score, founder, year = cursor.fetchone()
        return Team(name, score, founder, year)

    def get_teams(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM TEAM ORDER BY ID"
            cursor.execute(query)
            teams = [(key, Team(name, score, founder, year))
                      for key, name, score, founder, year in cursor]
        return teams

    def update_team(self, key, title, score, founder, year):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE TEAM SET NAME = %s, SCORE = %s, FOUNDER = %s, YEAR = %s WHERE (ID = %s)"
            cursor.execute(query, (title, score, founder, year, key))
            connection.commit()

    def addMember(self, key):
        self.teams[key].team_count = 5

#ANNOUNCEMENT
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

#TOPIC
    def add_topic(self, topic):
        self.topic_last_key += 1
        self.topics[self.topic_last_key] = topic

    def delete_topic(self, key):
        del self.topics[key]
        self.topic_last_key -= 1

    def get_topic(self, key):
        return self.topics[key]

    def get_topics(self):
        return sorted(self.topics.items())

#EXPERIENCE
    def add_experience(self, experience):

       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO EXPERIENCE (TITLE, USERNAME, START,FINISH,PERIOD,LENGTH) VALUES (%s, %s, %s, %s, %s, %s) RETURNING EXPERIENCE.ID"
            cursor.execute(query, (experience.title, experience.username, experience.start, experience.finish,float(experience.period), float(experience.length)))
            connection.commit()
            self.exp_key = cursor.fetchone()[0]


    def delete_experience(self, key):
       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM EXPERIENCE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()


    def get_experience(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, USERNAME, START,FINISH,PERIOD,LENGTH FROM EXPERIENCE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title, username, start, finish, period,length = cursor.fetchone()
        return Experience(title, username, start, finish, period,length)


    def get_experiences(self):
          with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM EXPERIENCE ORDER BY ID"
            cursor.execute(query)
            experiences = [(key, Experience(title, username, start, finish, period, length))
                      for key, title, username, start, finish, period, length in cursor]
            return experiences


    def update_experience(self, key, title, username, start, finish, period, length):
       self.experiences[key].title = title
       self.experiences[key].username = username
       self.experiences[key].start = start
       self.experiences[key].finish = finish
       self.experiences[key].period = period
       self.experiences[key].length = length

#RACE
    def add_race(self, race):
       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO RACE (TITLE, RACE_TYPE, FOUNDERID, TIME, CYCROUTEID) VALUES (%s, %s, %s, %s, %s) RETURNING RACE.ID"
            cursor.execute(query, (race.title, race.race_type, int(race.founder), race.time, race.place))
            connection.commit()
            self.race_last_key = cursor.fetchone()[0]

    def delete_race(self, key):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM RACE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_race(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, RACE_TYPE, FOUNDERID, TIME, CYCROUTEID FROM RACE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title, race_type, founder, time, place  = cursor.fetchone()
        return Race(title, race_type, founder, time, place)

    def get_races(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM RACE ORDER BY ID"
            cursor.execute(query)
            races = [(key, Race(title, race_type, founder, time, place))
                      for key, title, race_type, founder, time, place in cursor]
        return races

    def update_race(self, key, title, race_type, founder, time, place):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE RACE SET TITLE = %s, RACE_TYPE = %s, FOUNDERID = %s, TIME = %s, CYCROUTEID = %s WHERE (ID = %s)"
            cursor.execute(query, (title, race_type, founder, time, place, key))
            connection.commit()
#CATEGORY
    def count_category(self, category):
        self.category_count += 1

    def add_category(self, category):
        self.category_last_key += 1
        self.categories[self.category_last_key] = category

    def delete_category(self, key):
        del self.categories[key]
        self.category_last_key -= 1

    def get_category(self, key):
        return self.categories[key]

    def get_categories(self):
        return sorted(self.categories.items())


#ADMIN
    def add_admin(self, admin):
        self.admin_last_key += 1
        self.admins[self.admin_last_key] = admin
        # admin_count +=1

    def delete_admin(self, key):
        del self.admins[key]
        self.admin_last_key -= 1
        # admin_count -= 1

    def get_admin(self, key):
        return self.admins[key]

    def get_admins(self):
        return sorted(self.admins.items())


#CYCROUTE
    def add_cycroute(self, cycroute):

        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO CYCROUTE (TITLE, USERNAME, START,FINISH,LENGTH) VALUES (%s, %s, %s, %s, %s) RETURNING CYCROUTE.ID"
            cursor.execute(query, (cycroute.title, cycroute.username, cycroute.start, cycroute.finish, float(cycroute.length)))
            connection.commit()
            self.cycroute_last_key = cursor.fetchone()[0]

    def delete_cycroute(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM CYCROUTE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_cycroute(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, USERNAME, START, FINISH, LENGTH FROM CYCROUTE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title, username, start, finish,length = cursor.fetchone()
        return Cycroute(title, username, start, finish, length)

    def get_cycroutes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM CYCROUTE ORDER BY ID"
            cursor.execute(query)
            cycroutes = [(key, Cycroute(title, username, start, finish, length))
                      for key, title, username, start, finish, length in cursor]
            return cycroutes


    def update_cycroute(self, key, title, username, start, finish, length):
       self.cycroutes[key].title = title
       self.cycroutes[key].username = username
       self.cycroutes[key].start = start
       self.cycroutes[key].finish = finish
       self.cycroutes[key].length = length

#BIKE
    def add_bike(self, bike):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO BIKE (MODEL, BRAND, TYPE, SIZE, YEAR, PRICE) VALUES (%s, %s, %s, %s, %s, %s) RETURNING BIKE.ID"
            cursor.execute(query, (bike.model, bike.brand ,bike.type ,bike.size ,bike.year ,int(bike.price)))
            connection.commit()
            self.bike_last_key = cursor.fetchone()[0]

    def delete_bike(self, key):
       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BIKE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_bike(self, key):
          with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT MODEL, BRAND, TYPE, SIZE, YEAR, PRICE FROM BIKE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            model,brand, type, size, year, price = cursor.fetchone()
            return Bike(model, brand, type, size, year, price)

    def get_bikes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM BIKE ORDER BY ID"
            cursor.execute(query)
            bikes = [(key, Bike(model,brand, type, size, year, price))
                      for key, model,brand, type, size, year, price in cursor]
        return bikes

    def update_bike(self, key, price):
        self.bikes[key].price = price


# BASIC MEMBER FUNCTIONS
    def add_basicmember(self, basicmember):
        self.basicmember_last_key += 1
        self.basicmembers[self.basicmember_last_key] = basicmember
        # basicmember_count +=1

    def delete_basicmember(self, key):
        del self.basicmembers[key]
        self.basicmember_last_key -= 1
        # basicmember_count -= 1

    def get_basicmember(self, key):
        return self.basicmembers[key]

    def get_basicmembers(self):
        return sorted(self.basicmembers.items())

# PROFESSIONAL MEMBER FUNCTIONS
    def add_professionalmember(self, professionalmember):
        self.professionalmember_last_key += 1
        self.professionalmembers[self.professionalmember_last_key] = professionalmember
        # professionalmember_count +=1

    def delete_professionalmember(self, key):
        del self.professionalmembers[key]
        self.professionalmember_last_key -= 1
        # professionalmember_count -= 1

    def get_professionalmember(self, key):
        return self.professionalmembers[key]

    def get_professionalmembers(self):
        return sorted(self.professionalmembers.items())

#ACTIVITY
    def add_activity(self, activity):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ACTIVITY (TITLE, ACTIVITY_TYPE, FOUNDERID, TIME, PLACE, ACTIVITY_INFO) VALUES (%s, %s, %s, %s, %s, %s) RETURNING ACTIVITY.ID"
            cursor.execute(query, (activity.title, activity.activity_type, int(activity.founder), activity.time, activity.place, activity.activity_info))
            connection.commit()
            self.activity_last_key = cursor.fetchone()[0]


    def delete_activity(self, key):
       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM ACTIVITY WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_activity(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, ACTIVITY_TYPE, FOUNDERID, TIME, PLACE, ACTIVITY_INFO FROM ACTIVITY WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title, activity_type, founder, time, place, activity_info = cursor.fetchone()
        return Activity(title, activity_type, founder, time, place, activity_info)

    def get_activities(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ACTIVITY ORDER BY ID"
            cursor.execute(query)
            activities = [(key, Activity(title, activity_type, founder, time, place, activity_info))
                      for key, title, activity_type, founder, time, place, activity_info in cursor]
        return activities

    def update_activity(self, key, title, activity_type, founder, time, place, activity_info):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE ACTIVITY SET TITLE = %s, ACTIVITY_TYPE = %s, FOUNDERID = %s, TIME = %s, PLACE = %s, ACTIVITY_INFO = %s WHERE (ID = %s)"
            cursor.execute(query, (title, activity_type, founder, time, place, activity_info, key))
            connection.commit()

