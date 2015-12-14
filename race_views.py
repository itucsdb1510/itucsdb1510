import datetime

import psycopg2 as dbapi2

from flask import abort
from flask import g
from flask import session
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from random import randint
import random

from config import app
from race import Race
from basicmember import Basicmember

@app.route('/races', methods=['GET', 'POST'])
def races_page():
    if request.method == 'GET':
        races = app.store.get_races()
        now = datetime.datetime.now()
        return render_template('races.html', races=races,
                               current_time=now.ctime())
    elif  'races_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('races_to_delete')
            for key in keys:
                app.store.delete_race(int(key))
            return redirect(url_for('races_page'))
        elif  request.form['submit'] == 'Search' :
            keyword=request.form['search']
            races = app.store.search_race(keyword)
            now = datetime.datetime.now()
            return render_template('races.html', races=races,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        race_type = request.form.get('race_type')
        time = request.form['time']
        place = request.form.get('place')
        if 'username' in session:
            name = session['username']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
                founder = cursor.fetchone()[0]
                connection.commit()
                participant_count = 1
                race = Race(title, race_type, founder, participant_count, time, place)
                app.store.add_race(race)
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = ("INSERT INTO RACE_RESULTS (MEMBERID, RACEID ) VALUES (%s, %s)")
                cursor.execute(query, (founder, app.store.race_last_key))
                connection.commit()
            return redirect(url_for('race_page', key=app.store.race_last_key))
        else:
            return render_template('guest.html')



@app.route('/race/<int:key>', methods=['GET', 'POST'])
def race_page(key):
    if request.method == 'GET':
        race = app.store.get_race(key)
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT memberid FROM RACE_RESULTS WHERE raceid='%s';"%key)
            memberid = cursor.fetchone()[0]
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM MEMBERS WHERE memberid='%s';"%memberid)
            members = [(key, Basicmember(name, surname, username, gender, email, password, byear, city, interests, lastlogin, regtime, role))
                      for key, name, surname, username, gender, membertype, email, password, city, interests, score, byear,teamid, lastlogin, regtime, role in cursor]
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT RACEID FROM RACE_RESULTS ")
            max_raceid = cursor.fetchall()
            connection.commit()
            for i in max_raceid:
                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT COUNT(ID) FROM RACE_RESULTS WHERE raceid='%s';"%i)
                    countid = cursor.fetchone()[0]
                    connection.commit()
                dizi = [1]
                dizi = randint(1,countid)
                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT id FROM RACE_RESULTS WHERE raceid='%s';"%i)
                    ids = cursor.fetchall()
                    connection.commit()
                for id in ids:
                    ord = 1
                    with dbapi2.connect(app.config['dsn']) as connection:
                        cursor = connection.cursor()
                        query = "UPDATE RACE_RESULTS SET ord=%s  WHERE (raceid=%s)"
                        cursor.execute(query, (ord, i))
                        connection.commit()

        now = datetime.datetime.now()
        return render_template('race.html', race=race, members=members,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        race_type = request.form.get('race_type')
        time = request.form['time']
        place = request.form['place']
        app.store.update_race(key, title, race_type, time, place)
        return redirect(url_for('race_page', key=key))

@app.route('/races/add')
@app.route('/race/<int:key>/edit')
def race_edit_page(key=None):
    race = app.store.get_race(key) if key is not None else None
    now = datetime.datetime.now()
    cycroutes = app.store.get_cycroutes()
    return render_template('race_edit.html', race=race, cycroutes=cycroutes,
                           current_time=now.ctime())

@app.route('/race/<int:key>')
@app.route('/race/<int:key>/join')
def race_join_page(key=None):
    if 'username' in session:
        name = session['username']
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
            id = cursor.fetchone()
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = ("INSERT INTO RACE_RESULTS (MEMBERID, RACEID ) VALUES (%s, %s)")
            cursor.execute(query, (id, key))
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT participant_count FROM RACE WHERE id='%s';"%key)
            participant_count = cursor.fetchone()[0]
            participant_count = participant_count + 1
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = ("UPDATE RACE SET participant_count=%s  WHERE (id=%s)")
            cursor.execute(query, (participant_count, key))
            connection.commit()
        now = datetime.datetime.now()
        return redirect(url_for('race_page', key=key))
    else:
        race = app.store.get_race(key) if key is not None else None
        now = datetime.datetime.now()
        return redirect(url_for('race_page', key=key))
