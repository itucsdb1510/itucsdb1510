import datetime
import json
import os
import re

from flask import render_template
from config import app

import psycopg2 as dbapi2
from flask import redirect
from flask.helpers import url_for



from store import Store

from team import Team
import team_views

from experience import Experience
import experience_view

from announcement import Announcement
import announcement_views

from topic import Topic
import topic_views

from race import Race
import race_views
from category import Category
import category_views

from admin import Admin
import admin_views

from cycroute import Cycroute
import cycroute_views

from bike import Bike
import bike_views

from basicmember import Basicmember
import basicmember_views

from professionalmember import Professionalmember
import professionalmember_views

from activity import Activity
import activity_views

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS COUNTER ( N INTEGER )"""
        cursor.execute(query)

        query = "INSERT INTO COUNTER (N) VALUES (0)"
        cursor.execute(query)



    return redirect(url_for('home'))

@app.route('/racecalendar')
def racecalendar_page():
    now = datetime.datetime.now();
    return render_template('racecalendar.html', current_time=now.ctime())


@app.route('/trails')
def trails_page():
    now = datetime.datetime.now();
    return render_template('trails.html', current_time=now.ctime())


@app.route('/scores')
def scores_page():
    now = datetime.datetime.now();
    return render_template('scores.html', current_time=now.ctime())

@app.route('/message')
def message_page():
    now = datetime.datetime.now();
    return render_template('message.html', current_time=now.ctime())

@app.route('/news')
def news_page():
    now = datetime.datetime.now();
    return render_template('news.html', current_time=now.ctime())


@app.route('/login')
def login_page():
    now = datetime.datetime.now();
    return render_template('login.html', current_time=now.ctime())


@app.route('/forum')
def forum_page():
    now = datetime.datetime.now();
    return render_template('forum.html', current_time=now.ctime())

@app.route('/counter')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times" % count

if __name__ == '__main__':
    app.store = Store()
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)