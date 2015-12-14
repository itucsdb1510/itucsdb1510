import datetime

import os
import json
import sys
from werkzeug import secure_filename
from flask import send_from_directory

import psycopg2 as dbapi2

from flask import abort
from flask import g
from flask import session
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from team import Team
from basicmember import Basicmember

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/teams', methods=['GET', 'POST'])
def teams_page():
    if 'username' in session:
        if request.method == 'GET':
            teams = app.store.get_teams()
            now = datetime.datetime.now()
            return render_template('teams.html', teams=teams,
                                   current_time=now.ctime())
        elif  'teams_to_delete' in request.form or 'search' in request.form:
            if request.form['submit'] == 'Delete':
                keys = request.form.getlist('teams_to_delete')
                for key in keys:
                    app.store.delete_team(int(key))
                return redirect(url_for('teams_page'))
            elif  request.form['submit'] == 'Search' :
                search_name=request.form['search']
                teams = app.store.search_team(search_name)
                now = datetime.datetime.now()
                return render_template('teams.html', teams=teams,
                                   current_time=now.ctime())
        else:
            title = request.form['title']
            score = request.form['score']
            year = request.form['year']
            team_type = request.form.get('team_type')
            location = request.form['location']
            if 'username' in session:
                name = session['username']
                with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
                    founder = cursor.fetchone()
                    founder=founder[0]
                    connection.commit()
                member_count = 1
                team = Team(title, score, founder, member_count, year, team_type, location)
                app.store.add_team(team)
                image=request.files['file']
                if image:
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/image/teams/' + str(app.store.team_last_key) + '.jpg'))
                return redirect(url_for('team_page', key=app.store.team_last_key))

    else:
        return render_template('guest.html')


@app.route('/team/<int:key>', methods=['GET', 'POST'])
def team_page(key):
    if request.method == 'GET':
        team = app.store.get_team(key)
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM MEMBERS WHERE teamid='%s';"%key)
            members = [(key, Basicmember(name, surname, username, gender, email, password, byear, city, interests, lastlogin, regtime, role))
                      for key, name, surname, username, gender, membertype, email, password, city, interests, score, byear,teamid, lastlogin, regtime, role in cursor]
            connection.commit()
        now = datetime.datetime.now()
        return render_template('team.html', team=team, members=members,
                           current_time=now.ctime())
    else:
        title = request.form['title']
        score = request.form['score']
        year = request.form['year']
        team_type = request.form.get('team_type')
        location = request.form['location']
        image=request.files['file']
        if image:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/image/teams/' + str(key) + '.jpg'))
        app.store.update_team(key, title, score, year, team_type, location)
        return redirect(url_for('team_page', key=key))

@app.route('/teams/add')
@app.route('/team/<int:key>/edit')
def team_edit_page(key=None):
    team = app.store.get_team(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('team_edit.html', team=team,
                           current_time=now.ctime())

@app.route('/team/<int:key>')
@app.route('/team/<int:key>/join')
def team_join_page(key=None):
    if 'username' in session:
        name = session['username']
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
            id = cursor.fetchone()
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = ("UPDATE MEMBERS SET teamid=%s  WHERE (memberid=%s)")
            cursor.execute(query, (key, id))
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT member_count FROM TEAM WHERE id='%s';"%key)
            connection.commit()
            member_count = cursor.fetchone()[0]
            member_count = member_count + 1
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = ("UPDATE TEAM SET member_count=%s  WHERE (id=%s)")
            cursor.execute(query, (member_count, key))
            connection.commit()
            now = datetime.datetime.now()
            return redirect(url_for('team_page', key=key))
    else:
        team = app.store.get_team(key) if key is not None else None
        now = datetime.datetime.now()
        return redirect(url_for('team_page', key=key))