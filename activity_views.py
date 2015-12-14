import datetime
import psycopg2 as dbapi2

from flask import abort
from flask import g
from flask import session

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from activity import Activity
from basicmember import Basicmember

@app.route('/activities', methods=['GET', 'POST'])
def activities_page():
    if request.method == 'GET':
        activities = app.store.get_activities()
        now = datetime.datetime.now()
        return render_template('activities.html', activities=activities,
                               current_time=now.ctime())
    elif  'activities_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('activities_to_delete')
            for key in keys:
                app.store.delete_activity(int(key))
            return redirect(url_for('activities_page'))
        elif  request.form['submit'] == 'Search' :
            keyword=request.form['search']
            activities = app.store.search_activity(keyword)
            now = datetime.datetime.now()
            return render_template('activities.html', activities=activities,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        activity_type = request.form.get('activity_type')
        time = request.form['time']
        place = request.form['place']
        activity_info = request.form['activity_info']
        if 'username' in session:
            name = session['username']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
                founder = cursor.fetchone()[0]
                connection.commit()
            participant_count = 1
            activity = Activity(title, activity_type, founder, participant_count, time, place, activity_info)
            app.store.add_activity(activity)
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = ("INSERT INTO ACTIVITY_MEMBERS (MEMBERID, ACTIVITYID ) VALUES (%s, %s)")
                cursor.execute(query, (founder, app.store.activity_last_key))
                connection.commit()
            return redirect(url_for('activity_page', key=app.store.activity_last_key))
        else:
            return render_template('guest.html')



@app.route('/activity/<int:key>', methods=['GET', 'POST'])
def activity_page(key):
    if request.method == 'GET':
        activity = app.store.get_activity(key)
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT memberid FROM ACTIVITY_MEMBERS WHERE activityid='%s';"%key)
            memberid = cursor.fetchone()
            connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM MEMBERS WHERE memberid='%s';"%memberid)
            members = [(key, Basicmember(name, surname, username, gender, email, password, byear, city, interests, lastlogin, regtime, role))
                      for key, name, surname, username, gender, membertype, email, password, city, interests, score, byear,teamid, lastlogin, regtime, role in cursor]
            connection.commit()
        now = datetime.datetime.now()
        return render_template('activity.html', activity=activity, members = members,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        activity_type = request.form.get('activity_type')
        time = request.form['time']
        place = request.form['place']
        activity_info = request.form['activity_info']
        app.store.update_activity(key, title, activity_type, time, place, activity_info)
        return redirect(url_for('activity_page', key=key))

@app.route('/activities/add')
@app.route('/activity/<int:key>/edit')
def activity_edit_page(key=None):
    activity = app.store.get_activity(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('activity_edit.html', activity=activity,
                           current_time=now.ctime())

@app.route('/activity/<int:key>')
@app.route('/activity/<int:key>/join')
def activity_join_page(key=None):
    if 'username' in session:
        name = session['username']
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
                    connection.commit()
        id = cursor.fetchone()
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = ("INSERT INTO ACTIVITY_MEMBERS (MEMBERID, ACTIVITYID ) VALUES (%s, %s)")
                    cursor.execute(query, (id, key))
                    connection.commit()
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT participant_count FROM ACTIVITY WHERE id='%s';"%key)
                    connection.commit()
        participant_count = cursor.fetchone()
        participant_count = participant_count[0]
        participant_count = participant_count + 1
        with dbapi2.connect(app.config['dsn']) as connection:
                    cursor = connection.cursor()
                    query = ("UPDATE ACTIVITY SET participant_count=%s  WHERE (id=%s)")
                    cursor.execute(query, (participant_count, key))
                    connection.commit()
        now = datetime.datetime.now()
        return redirect(url_for('activity_page', key=key))
    else:
        activity = app.store.get_activity(key) if key is not None else None
        now = datetime.datetime.now()
        return redirect(url_for('activity_page', key=key))


