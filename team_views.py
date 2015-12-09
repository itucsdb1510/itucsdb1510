import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from team import Team

@app.route('/teams', methods=['GET', 'POST'])
def teams_page():
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
        founder = request.form['founder']
        year = request.form['year']
        team_type = request.form.get('team_type')
        location = request.form['location']
        team = Team(title, score, founder, year, team_type, location)
        app.store.add_team(team)
        return redirect(url_for('team_page', key=app.store.team_last_key))



@app.route('/team/<int:key>', methods=['GET', 'POST'])
def team_page(key):
    if request.method == 'GET':
        team = app.store.get_team(key)
        now = datetime.datetime.now()
        return render_template('team.html', team=team,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        score = request.form['score']
        founder = request.form['founder']
        year = request.form['year']
        team_type = request.form['team_type']
        location = request.form['location']
        app.store.update_team(key, title, score, founder, year, team_type, location)
        return redirect(url_for('team_page', key=key))

@app.route('/teams/add')
@app.route('/team/<int:key>/edit')
def team_edit_page(key=None):
    team = app.store.get_team(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('team_edit.html', team=team,
                           current_time=now.ctime())