import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from experience import Experience

@app.route('/experiences', methods=['GET', 'POST'])
def experiences_page():
    if request.method == 'GET':
        experiences = app.store.get_experiences()
        now = datetime.datetime.now()
        return render_template('experiences.html', experiences=experiences,
                               current_time=now.ctime())
    elif 'experiences_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('experiences_to_delete')
            for key in keys:
                app.store.delete_experience(int(key))
            return redirect(url_for('experiences_page'))
        elif  request.form['submit'] == 'search' :
            keyword=request.form['search']
            experiences = app.store.search_experience(keyword)
            now = datetime.datetime.now()
            return render_template('experiences.html', experiences=experiences,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        username = request.form['username']
        start = request.form['start']
        finish = request.form['finish']
        period = request.form['period']
        length=request.form['length']

        experience = Experience(title, username, start, finish,period,length)
        app.store.add_experience(experience)
        return redirect(url_for('experience_page', key=app.store.exp_key))



@app.route('/experience/<int:key>', methods=['GET', 'POST'])
def experience_page(key):
    if request.method == 'GET':
        experience = app.store.get_experience(key)
        now = datetime.datetime.now()
        return render_template('experience.html', experience=experience,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        username = request.form['username']
        start = request.form['start']
        finish = request.form['finish']
        period = request.form['period']
        length=request.form['length']
        app.store.update_experience(key, title,username, start, finish,period,length)
        return redirect(url_for('experience_page', key=key))

@app.route('/experiences/add')
@app.route('/experience/<int:key>/edit')
def experience_edit_page(key=None):
    experience = app.store.get_experience(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('experience_edit.html', experience=experience,current_time=now.ctime())

