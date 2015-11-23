import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from activity import Activity

@app.route('/activities', methods=['GET', 'POST'])
def activities_page():
    if request.method == 'GET':
        activities = app.store.get_activities()
        now = datetime.datetime.now()
        return render_template('activities.html', activities=activities,
                               current_time=now.ctime())
    elif 'activities_to_delete' in request.form:
        keys = request.form.getlist('activities_to_delete')
        for key in keys:
            app.store.delete_activity(int(key))
        return redirect(url_for('activities_page'))
    else:
        title = request.form['title']
        activity_type = request.form['activity_type']
        founder = request.form['founder']
        time = request.form['time']
        place = request.form['place']
        activity_info = request.form['activity_info']
        activity = Activity(title, activity_type, founder, time, place, activity_info)
        app.store.add_activity(activity)
        return redirect(url_for('activity_page', key=app.store.activity_last_key))



@app.route('/activity/<int:key>', methods=['GET', 'POST'])
def activity_page(key):
    if request.method == 'GET':
        activity = app.store.get_activity(key)
        now = datetime.datetime.now()
        return render_template('activity.html', activity=activity,
                               current_time=now.ctime())
    else:
        app.store.addMember(key)
        return redirect(url_for('activity_page', key=app.store.activity_last_key))

@app.route('/activities/add')
def activity_edit_page():
    now = datetime.datetime.now()
    return render_template('activity_edit.html', current_time=now.ctime())