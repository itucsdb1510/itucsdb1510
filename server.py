import datetime
import os


from flask import render_template
from pip._vendor.requests.packages.urllib3.util.timeout import current_time


from config import app
from store import Store
from team import Team
import team_views

from experience import Experience
import experience_view

from announcement import Announcement
import announcement_views

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




@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


@app.route('/activity')
def activity_page():
    now = datetime.datetime.now();
    return render_template('activity.html', current_time=now.ctime())

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

@app.route('/signup')
def signup_page():
    now = datetime.datetime.now();
    return render_template('signup.html', current_time=now.ctime())

@app.route('/forum')
def forum_page():
    now = datetime.datetime.now();
    return render_template('forum.html', current_time=now.ctime())






if __name__ == '__main__':
    app.store = Store()
    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
    app.run(host='0.0.0.0', port=int(PORT))
