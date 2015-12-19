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
from announcement import Announcement
from category import Category
from admin import Admin
from basicmember import Basicmember
from professionalmember import Professionalmember
import time
from random import randint

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
            query = "INSERT INTO TEAM (NAME, SCORE, FOUNDER, MEMBER_COUNT, YEAR, TEAMTYPE, LOCATION) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING TEAM.ID"
            cursor.execute(query, (team.title, int(team.score), team.founder, team.member_count, int(team.year), team.team_type, team.location))
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
            query = "SELECT NAME, SCORE, FOUNDER, MEMBER_COUNT, YEAR, TEAMTYPE, LOCATION FROM TEAM WHERE (ID = %s)"
            cursor.execute(query, (key,))
            name, score, founder, member_count, year, team_type, location = cursor.fetchone()
        return Team(name, score, founder, member_count, year, team_type, location)

    def get_teams(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM TEAM ORDER BY ID"
            cursor.execute(query)
            teams = [(key, Team(name, score, founder, member_count, year, team_type, location))
                      for key, name, score, founder, member_count, year, team_type, location in cursor]
        return teams

    def search_team(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM TEAM WHERE (NAME ILIKE %s OR LOCATION ILIKE %s)"
            key = '%'+key+'%'
            cursor.execute(query, (key, key))
            teams = [(key, Team(name, score, founder, member_count, year, team_type, location))
                      for key, name, score, founder, member_count, year, team_type, location in cursor]
        return teams

    def update_team(self, key, title, score, year, team_type, location):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE TEAM SET NAME = %s, SCORE = %s, YEAR = %s, TEAMTYPE = %s, LOCATION = %s WHERE (ID = %s)"
            cursor.execute(query, (title, score, year, team_type, location, key))
            connection.commit()

    def addMember(self, key):
        self.teams[key].team_count = 5




#ANNOUNCEMENT
    def add_announcement(self, announcement):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ANNOUNCEMENT (TITLE, TEXT) VALUES (%s, %s) RETURNING ANNOUNCEMENT.ID"
            cursor.execute(query, (announcement.title, announcement.text))
            connection.commit()
            self.announcement_last_key = cursor.fetchone()[0]

    def delete_announcement(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM ANNOUNCEMENT WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_announcement(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, TEXT FROM ANNOUNCEMENT WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title, text = cursor.fetchone()
        return Announcement(title, text)

    def get_announcements(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ANNOUNCEMENT ORDER BY ID"
            cursor.execute(query)
            announcements = [(key, Announcement(title, text))
                      for key, title, text in cursor]
        return announcements
    def update_announcement(self, key, title, text):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE ANNOUNCEMENT SET TITLE = %s, TEXT = %s WHERE (ID = %s)"
            cursor.execute(query, (title, text,key))
            connection.commit()
    def search_announcement(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ANNOUNCEMENT WHERE (TITLE ILIKE %s OR TEXT ILIKE %s)"
            key = '%'+key+'%'
            cursor.execute(query, (key, key))
            announcements = [(key, Announcement(title,text))
                      for key, title, text in cursor]
        return announcements

#CATEGORY

    def add_category(self, category):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO CATEGORY (TITLE,TYPEE) VALUES (%s,%s) RETURNING CATEGORY.ID"
            cursor.execute(query, (category.title, category.typee))
            connection.commit()
            self.category_last_key = cursor.fetchone()[0]

    def delete_category(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM CATEGORY WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_category(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE,TYPEE FROM CATEGORY WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title,typee = cursor.fetchone()
        return Category(title,typee)

    def get_categories(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM CATEGORY ORDER BY ID"
            cursor.execute(query)
            categories = [(key, Category(title, typee))
                      for key, title,typee in cursor]
        return categories
    def update_category(self, key, title,typee):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE CATEGORY SET TITLE = %s, TYPEE= %s WHERE (ID = %s)"
            cursor.execute(query, (title, typee ,key))
            connection.commit()
    def search_category(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM CATEGORY WHERE (TITLE ILIKE %s OR TYPEE ILIKE %s)"
            key = '%'+key+'%'
            cursor.execute(query, (key, key))
            categories = [(key, Category(title, typee))
                      for key, title, typee in cursor]
        return categories



#TOPIC
    def add_topic(self, topic):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO TOPIC (TITLE,TEXT,CURTIME, CATEGORYID) VALUES (%s,%s,%s,%s) RETURNING TOPIC.ID"
            cursor.execute(query, (topic.title, topic.text, topic.time, topic.categoryId ))
            connection.commit()
            self.topic_last_key = cursor.fetchone()[0]


    def delete_topic(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM TOPIC WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_topic(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT TITLE, TEXT, CURTIME,CATEGORYID FROM TOPIC WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title,text,time, categoryId = cursor.fetchone()
        return Topic(title,text,time,categoryId)

    def get_topics(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM TOPIC ORDER BY ID"
            cursor.execute(query)
            topics = [(key, Topic(title,text,time,categoryId))
                      for key, title,text,time,categoryId in cursor]
        return topics
    def update_topic(self, key, title, text, time, categoryId):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE TOPIC SET TITLE = %s, TEXT = %s, CURTIME = %s, CATEGORYID = %s WHERE (ID = %s)"
            cursor.execute(query, (title, text, time,  categoryId, key))
            connection.commit()

    def search_topic(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM TOPIC WHERE (TITLE ILIKE %s OR TEXT ILIKE %s)"
            key = '%'+key+'%'
            cursor.execute(query, (key, key))
            topics = [(key, Topic(title, text, time, categoryId))
                      for key, title, text, time, categoryId in cursor]
        return topics

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
                      for key, title, username, start, finish, period, length,userid,date in cursor]
            return experiences


    def update_experience(self, key, title, username, start, finish, period, length):
       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE EXPERIENCE SET TITLE=%s, USERNAME=%s, START=%s,FINISH=%s,PERIOD=%s,LENGTH=%s WHERE (ID = %s)"
            cursor.execute(query, (title, username, start, finish, period, length, key))
            connection.commit()

    def search_experience(self,keyword):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="SELECT * FROM EXPERIENCE WHERE (TITLE ILIKE %s OR START ILIKE%s OR FINISH ILIKE %s ) ORDER BY ID"
            keyword='%'+keyword+'%'
            cursor.execute(query, (keyword,keyword,keyword))
            experiences = [(key, Experience(title, username, start, finish, period, length))
                      for key, title, username, start, finish, period, length,userid,date in cursor]
        return experiences

#RACE
    def add_race(self, race):
       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO RACE (TITLE, RACE_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, CYCROUTEID) VALUES (%s, %s, %s, %s, %s, %s) RETURNING RACE.ID"
            cursor.execute(query, (race.title, race.race_type, int(race.founder), race.participant_count, race.time, race.place))
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
            query = "SELECT TITLE, RACE_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, CYCROUTEID FROM RACE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title, race_type, founder, participant_count, time, place  = cursor.fetchone()
        return Race(title, race_type, founder, participant_count, time, place)

    def get_races(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM RACE ORDER BY ID"
            cursor.execute(query)
            races = [(key, Race(title, race_type, founder, participant_count, time, place))
                      for key, title, race_type, founder, participant_count, time, place in cursor]
        return races

    def update_race(self, key, title, race_type, time, place):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE RACE SET TITLE = %s, RACE_TYPE = %s, TIME = %s, CYCROUTEID = %s WHERE (ID = %s)"
            cursor.execute(query, (title, race_type, time, place, key))
            connection.commit()

    def search_race(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM RACE WHERE (TITLE ILIKE %s OR RACE_TYPE ILIKE %s)"
            key = '%'+key+'%'
            cursor.execute(query, (key, key))
            races = [(key, Race(title, race_type, founder, participant_count, time, place))
                      for key, title, race_type, founder, participant_count, time, place in cursor]
        return races


#ADMIN
    def add_admin(self, admin):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ADMIN (NAME, SURNAME, USERNAME, EMAIL, PASSWORD, YEAR, ROLE) VALUES (%s, %s, %s, %s, %s, %s,%s) RETURNING ADMIN.ID"
            cursor.execute(query, (admin.name, admin.surname, admin.username, admin.email, admin.password, int(admin.year), 'admin'))
            connection.commit()
            self.admin_last_key = cursor.fetchone()[0]

    def delete_admin(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM ADMIN WHERE (ID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_admin(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT NAME, SURNAME, USERNAME, EMAIL, PASSWORD, YEAR FROM ADMIN WHERE (ID = %s)"
            cursor.execute(query, (key,))
            name, surname, username, email, password, year = cursor.fetchone()
        return Admin(name, surname, username, email, password, year,"admin")


    def get_admins(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ADMIN ORDER BY ID"
            cursor.execute(query)
            admins = [(key, Admin(name, surname, username, email, password, year,role))
                      for key, name, surname, username, email, password, year,role in cursor]
        return admins

    def update_admin(self, key, name, surname, username, email, password, year, role):
       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE ADMIN SET NAME=%s, SURNAME=%s, USERNAME=%s, EMAIL=%s, PASSWORD=%s, YEAR=%s, ROLE=%s  WHERE (ID = %s)"
            cursor.execute(query, (name, surname, username, email, password, year, role, key))
            connection.commit()

    def search_admin(self,keyword):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="SELECT * FROM ADMIN WHERE (NAME ILIKE %s OR USERNAME ILIKE%s ) ORDER BY ID"
            keyword='%'+keyword+'%'
            cursor.execute(query, (keyword,keyword))
            admins = [(key, Admin(name, surname, username, email, password, year, role))
                      for key, name, surname, username, email, password, year,role  in cursor]
        return admins

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
                      for key, title, username, start, finish, length,date in cursor]
            return cycroutes


    def update_cycroute(self, key, title,start, finish, length):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE CYCROUTE SET TITLE=%s,START=%s,FINISH=%s,LENGTH=%s WHERE (ID = %s)"
            cursor.execute(query, (title,start, finish, length, key))
            connection.commit()
    def search_cycroute(self,keyword):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="SELECT * FROM CYCROUTE WHERE (TITLE ILIKE %s OR START ILIKE%s OR FINISH ILIKE %s ) ORDER BY ID"
            keyword='%'+keyword+'%'
            cursor.execute(query, (keyword,keyword,keyword))
            cycroutes = [(key, Cycroute(title, username, start, finish,length))
                      for key, title, username, start, finish, length,date in cursor]
        return cycroutes

#BIKE
    def add_bike(self, bike):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO BIKE (MODEL, BRAND, TYPE, SIZE, YEAR, PRICE,USERNAME) VALUES (%s, %s, %s, %s, %s, %s,%s) RETURNING BIKE.ID"
            cursor.execute(query, (bike.model, bike.brand ,bike.type ,bike.size ,bike.year ,bike.price,bike.username))
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
            query = "SELECT MODEL, BRAND, TYPE, SIZE, YEAR, PRICE,USERNAME FROM BIKE WHERE (ID = %s)"
            cursor.execute(query, (key,))
            model,brand, type, size, year, price,username = cursor.fetchone()
            return Bike(model, brand, type, size, year, price,username)

    def get_bikes(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM BIKE ORDER BY ID"
            cursor.execute(query)
            bikes = [(key, Bike(model,brand, type, size, year, price,username))
                      for key, model,brand, type, size, year, price,username,date in cursor]
        return bikes


    def update_bike(self, key, model,brand, type, size, year, price):
       with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE BIKE SET MODEL=%s, BRAND=%s, TYPE=%s, SIZE=%s, YEAR=%s, PRICE=%s WHERE (ID = %s)"
            cursor.execute(query, (model, brand, type, size, year, price, key))
            connection.commit()

    def search_bike(self,keyword):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="SELECT * FROM BIKE WHERE (MODEL ILIKE %s OR BRAND ILIKE%s OR TYPE ILIKE %s ) ORDER BY ID"
            keyword='%'+keyword+'%'
            cursor.execute(query, (keyword,keyword,keyword))
            bikes = [(key, Bike(model,brand, type, size, year, price,username))
                      for key, model,brand, type, size, year, price,username,date in cursor]
        return bikes



# BASIC MEMBER FUNCTIONS
    def add_basicmember(self, basicmember):
         with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO MEMBERS (NAME, SURNAME, USERNAME, GENDER, MEMBERTYPE,EMAIL,PASSWORD, CITY, YEAR, INTERESTS, LASTLOGIN, REGTIME, ROLE ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING MEMBERS.MEMBERID"
            cursor.execute(query, (basicmember.name, basicmember.surname,basicmember.username, basicmember.gender, 0, basicmember.email,basicmember.password, basicmember.city, int(basicmember.byear), basicmember.interests, basicmember.lastlogin, basicmember.regtime, basicmember.role))
            connection.commit()
            self.basicmember_last_key = cursor.fetchone()[0]


    def delete_basicmember(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM MEMBERS WHERE (MEMBERID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_basicmember(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT NAME, SURNAME, USERNAME, GENDER, MEMBERTYPE,EMAIL, PASSWORD, CITY, INTERESTS,SCORE,YEAR, LASTLOGIN, REGTIME, ROLE  FROM MEMBERS WHERE (MEMBERID = %s)"
            cursor.execute(query, (key,))
            name, surname, username, gender, membertype, email, password, city, interests, score, byear, lastlogin, regtime, role = cursor.fetchone()
        return Basicmember(name, surname, username, gender, email, password, byear, city, interests, lastlogin, regtime, role)

    def get_basicmembers(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM MEMBERS WHERE MEMBERTYPE=0 ORDER BY MEMBERID"
            cursor.execute(query)
            basicmembers = [(key, Basicmember(name, surname, username, gender, email, password, byear, city, interests, lastlogin, regtime, role))
                      for key, name, surname, username, gender, membertype, email, password, city, interests, score, byear, lastlogin, regtime, role,teamid in cursor]
        return basicmembers


    def search_basicmember(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM MEMBERS WHERE (NAME ILIKE %s OR USERNAME ILIKE %s) AND (MEMBERTYPE=0)"
            key = '%'+key+'%'
            cursor.execute(query, (key, key))
            basicmembers = [(key, Basicmember(name, surname, username, gender, email, password, byear, city, interests, lastlogin, regtime, role))
                      for key, name, surname, username, gender, membertype, email, password, city, interests, score, byear, lastlogin, regtime, role,teamid in cursor]
        return basicmembers

    def find_member(self, key1, key2):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT NAME FROM MEMBERS WHERE ((email=%s)and (password=%s)) UNION SELECT NAME FROM ADMIN WHERE ((email=%s)and (password=%s))"
            cursor.execute(query, (key1, key2,key1, key2))
            if cursor.fetchone() is None:
                    return 0
            else:
                    return 1


    def update_basicmember(self, key, name, surname, username, gender, email, password, byear, city, interests,lastlogin, regtime, role):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE MEMBERS SET NAME = %s,SURNAME= %s, USERNAME= %s,  GENDER= %s, EMAIL= %s, PASSWORD= %s, YEAR= %s, CITY= %s, INTERESTS= %s WHERE (MEMBERID = %s)"
            cursor.execute(query, (name, surname, username, gender, email, password, byear, city, interests, key))
            connection.commit()


# PROFESSIONAL MEMBER FUNCTIONS
    def add_professionalmember(self, professionalmember):
         with dbapi2.connect(self.app.config['dsn']) as connection:
             #add member into random team
            cursor = connection.cursor()
            query = "SELECT id FROM team ORDER BY RANDOM()LIMIT 1"
            cursor.execute(query)
            randteamid= cursor.fetchone()
            query = "INSERT INTO MEMBERS (NAME, SURNAME, USERNAME, GENDER,EMAIL,PASSWORD, CITY, YEAR, INTERESTS,MEMBERTYPE,LASTLOGIN, REGTIME, ROLE ,TEAMID ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s,%s,%s) RETURNING MEMBERS.MEMBERID"
            cursor.execute(query, (professionalmember.name, professionalmember.surname,professionalmember.username, professionalmember.gender, professionalmember.email,professionalmember.password, professionalmember.city, int(professionalmember.byear), professionalmember.interests,1,professionalmember.lastlogin, professionalmember.regtime, professionalmember.role,randteamid))
            self.professionalmember_last_key = cursor.fetchone()[0]
            #connection.commit()
           # if professionalmember.award_G ==0 and professionalmember.award_B ==0 and professionalmember.award_S == 0:
             #   currdate=(time.strftime("%Y/%m/%d"))
               # query = "INSERT INTO AWARDS (numofGOLD,numofBRONZE ,numofSILVER, memberid,date ) VALUES (%s, %s, %s, %s,%s)"
               # cursor.execute(query, (professionalmember.award_G,professionalmember.award_B,professionalmember.award_S,self.professionalmember_last_key,currdate))
               # connection.commit()


    def delete_professionalmember(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM MEMBERS WHERE (MEMBERID = %s)"
            cursor.execute(query, (key,))
            connection.commit()

    def get_professionalmember(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT sum(numofGOLD),sum(numofBRONZE), sum(numofSILVER) FROM MEMBERS, AWARDS WHERE( (members.memberid=awards.memberid) and members.memberid=%s )"
            cursor.execute(query, (key,))
            award_G,award_B, award_S= cursor.fetchone()
            query = "SELECT NAME, SURNAME, USERNAME, GENDER, MEMBERTYPE,EMAIL, PASSWORD, CITY, INTERESTS,SCORE,YEAR, LASTLOGIN, REGTIME, ROLE, TEAMID FROM MEMBERS WHERE (MEMBERID =%s)"
            cursor.execute(query, (key,))
            name, surname, username, gender, membertype, email, password, city, interests, score, byear,lastlogin, regtime, role, teamid = cursor.fetchone()
        return Professionalmember(name, surname, username, gender, email, password, byear, city, interests,award_G,award_B, award_S,lastlogin, regtime, role)

    def get_professionalmembers(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM MEMBERS WHERE MEMBERTYPE=1 ORDER BY MEMBERID"
            cursor.execute(query)
            professionalmembers = [(key, Professionalmember(name, surname, username, gender, email, password, byear, city, interests,0,0,0,lastlogin, regtime, role))
                      for key, name, surname, username, gender, membertype, email, password, city, interests, score, byear,lastlogin, regtime, role,teamid in cursor]
        return professionalmembers

    def search_professionalmember(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM MEMBERS WHERE (NAME ILIKE %s OR USERNAME ILIKE %s) AND (MEMBERTYPE=1)"
            key = '%'+key+'%'
            cursor.execute(query, (key, key))
            professionalmembers = [(key,  Professionalmember(name, surname, username, gender, email, password, byear, city, interests,0,0,0,lastlogin, regtime, role))
                      for key, name, surname, username, gender, membertype,email, password, city, interests, score, byear,lastlogin, regtime, role,teamid in cursor]
        return professionalmembers

    def update_professionalmember(self, key, name, surname, username, gender, email, password, byear, city, interests,award_G,award_B, award_S,lastlogin, regtime, role):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE MEMBERS SET NAME = %s,SURNAME= %s, USERNAME= %s,  GENDER= %s, EMAIL= %s, PASSWORD= %s, YEAR= %s, CITY= %s, INTERESTS= %s, LASTLOGIN= %s  WHERE (MEMBERID = %s)"
            cursor.execute(query, (name, surname, username, gender, email, password, byear, city, interests, lastlogin,key))
            connection.commit()

#ACTIVITY
    def add_activity(self, activity):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO ACTIVITY (TITLE, ACTIVITY_TYPE, FOUNDERID, PARTICIPANT_COUNT, TIME, PLACE, ACTIVITY_INFO) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING ACTIVITY.ID"
            cursor.execute(query, (activity.title, activity.activity_type, int(activity.founder), activity.participant_count, activity.time, activity.place, activity.activity_info))
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
            query = "SELECT TITLE, ACTIVITY_TYPE, FOUNDERID, PARTICIPANT_COUNT,  TIME, PLACE, ACTIVITY_INFO FROM ACTIVITY WHERE (ID = %s)"
            cursor.execute(query, (key,))
            title, activity_type, founder, participant_count, time, place, activity_info = cursor.fetchone()
        return Activity(title, activity_type, founder, participant_count, time, place, activity_info)

    def get_activities(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ACTIVITY ORDER BY ID"
            cursor.execute(query)
            activities = [(key, Activity(title, activity_type, founder, participant_count, time, place, activity_info))
                      for key, title, activity_type, founder, participant_count, time, place, activity_info in cursor]
        return activities

    def update_activity(self, key, title, activity_type, time, place, activity_info):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "UPDATE ACTIVITY SET TITLE = %s, ACTIVITY_TYPE = %s, TIME = %s, PLACE = %s, ACTIVITY_INFO = %s WHERE (ID = %s)"
            cursor.execute(query, (title, activity_type, time, place, activity_info, key))
            connection.commit()

    def search_activity(self, key):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM ACTIVITY WHERE (TITLE ILIKE %s OR ACTIVITY_TYPE ILIKE %s OR PLACE ILIKE %s OR ACTIVITY_INFO ILIKE %s)"
            key = '%'+key+'%'
            cursor.execute(query, (key, key, key, key))
            activities = [(key, Activity( title, activity_type, founder, participant_count, time, place, activity_info))
                      for key,  title, activity_type, founder, participant_count, time, place, activity_info in cursor]
        return activities



    def check_admin(self, email,password):
        if email == 'ersogan@itu.edu.tr' and password=='321321':
            return 1
        elif email == 'sertbasn@itu.edu.tr'  and password=='321321':
            return 1
        elif  email == 'tekpinar@itu.edu.tr'  and password=='321321':
             return 1
        elif email == 'ozer@itu.edu.tr'  and password=='321321' :
             return 1
        elif email == 'sasmazel@itu.edu.tr'  and password=='321321':
            return 1
        else:
            return 0


    def get_top5team(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
             cursor = connection.cursor()
             query = "select * from team order by score desc limit 5"
             cursor.execute(query)
             teams = [(key, Team(name, score, founder, member_count, year, team_type, location))
                      for key, name, score, founder, member_count, year, team_type, location in cursor]
        return teams


    def get_top5member(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "select * from members where membertype=1 order by score desc limit 5"
            cursor.execute(query)
            professionalmembers = [(key, Professionalmember(name, surname, username,gender, email, password, byear, city,interests, 0,0,0,lastlogin, regtime, role))
                      for key,name, surname, username, gender, membertype, email, password, city, interests, score, byear,lastlogin, regtime, role,teamid in cursor]
        return professionalmembers

    def get_numofbasicmembers(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "select count(memberid) from members where membertype=0"
            cursor.execute(query)
            numb = cursor.fetchone()
        return numb

    def get_numofprofessionalmembers(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "select count(memberid) from members where membertype=1"
            cursor.execute(query)
            nump = cursor.fetchone()
        return nump

    def get_numofadmins(self):
        with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "select count(id) from admin"
            cursor.execute(query)
            numa = cursor.fetchone()
        return numa

    def get_myexperiences(self,name):
          with dbapi2.connect(self.app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM EXPERIENCE where (username=%s)"
            cursor.execute(query,(name,))
            experiences = [(key, Experience(title, username, start, finish, period, length))
                      for key, title, username, start, finish, period, length,userid,date in cursor]
            return experiences

