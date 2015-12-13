import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import time
from config import app
from professionalmember import Professionalmember

@app.route('/professionalmembers', methods=['GET', 'POST'])
def professionalmembers_page():
    if request.method == 'GET':
        professionalmembers = app.store.get_professionalmembers()
        now = datetime.datetime.now()
        return render_template('professionalmembers.html', professionalmembers=professionalmembers,
                               current_time=now.ctime())
    elif 'professionalmembers_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('professionalmembers_to_delete')
            for key in keys:
                app.store.delete_professionalmember(int(key))
            return redirect(url_for('professionalmembers_page'))
        elif  request.form['submit'] == 'search' :
            keyword=request.form['search']
            professionalmembers = app.store.search_professionalmember(keyword)
            now = datetime.datetime.now()
            return render_template('professionalmembers.html', professionalmembers=professionalmembers,
                               current_time=now.ctime())
    else:
        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        gender = request.form.get('gender')
        email = request.form['email']
        password = request.form['password']
        byear = request.form['byear']
        city = request.form['city']
        interests = request.form['interests']


        now = str((datetime.datetime.now()));
        now = now[:-7]
        if (app.store.check_admin(email)):
            role = 'admin'
        else:
            role = 'user'

        professionalmember = Professionalmember(name, surname, username, gender, email,password, byear, city, interests,award_G,award_B, award_S,now, now, role)
        app.store.add_professionalmember(professionalmember)
        return redirect(url_for('professionalmember_page', key=app.store.professionalmember_last_key))



@app.route('/professionalmember/<int:key>', methods=['GET', 'POST'])
def professionalmember_page(key):
    if request.method == 'GET':
        professionalmember = app.store.get_professionalmember(key)
        now = datetime.datetime.now()
        return render_template('professionalmember.html', professionalmember=professionalmember,
                               current_time=now.ctime())
    else:
        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        byear = request.form['byear']
        city = request.form['city']
        interests = request.form['interests']
        gender = request.form.get('gender')
        award_G = request.form.get('award_G')
        award_S = request.form.get('award_S')
        award_B = request.form.get('award_B')
        now = str((datetime.datetime.now()));
        now = now[:-7]
        if (app.store.check_admin(email)):
            role = 'admin'
        else:
            role = 'user'

        app.store.update_professionalmember(key, name, surname, username, gender, email,password, byear, city, interests,award_G,award_B, award_S,now, now, role)
        return redirect(url_for('professionalmember_page', key=key))

@app.route('/professionalmembers/add')
@app.route('/professionalmember/<int:key>/edit')
def professionalmember_edit_page(key=None):
    professionalmember = app.store.get_professionalmember(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('professionalmember_edit.html', professionalmember=professionalmember,
                           current_time=now.ctime())