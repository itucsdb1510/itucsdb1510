import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from race import Race

@app.route('/races', methods=['GET', 'POST'])
def races_page():
    if request.method == 'GET':
        races = app.store.get_races()
        now = datetime.datetime.now()
        return render_template('races.html', races=races,
                               current_time=now.ctime())
    elif 'races_to_delete' in request.form:
        keys = request.form.getlist('races_to_delete')
        for key in keys:
            app.store.delete_race(int(key))
        return redirect(url_for('races_page'))
    else:
        title = request.form['title']
        race_type = request.form['race_type']
        founder = request.form['founder']
        time = request.form['time']
        place = request.form['place']
        race = Race(title, race_type, founder, time, place)
        app.store.add_race(race)
        return redirect(url_for('race_page', key=app.store.race_last_key))



@app.route('/race/<int:key>', methods=['GET', 'POST'])
def race_page(key):
    if request.method == 'GET':
        race = app.store.get_race(key)
        now = datetime.datetime.now()
        return render_template('race.html', race=race,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        race_type = request.form['race_type']
        founder = request.form['founder']
        time = request.form['time']
        place = request.form['place']
        app.store.update_race(key, title, race_type, founder, time, place)
        return redirect(url_for('race_page', key=key))

@app.route('/races/add')
@app.route('/race/<int:key>/edit')
def race_edit_page(key=None):
    race = app.store.get_race(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('race_edit.html', race=race,
                           current_time=now.ctime())

