import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from basicmember import Basicmember

@app.route('/basicmembers', methods=['GET', 'POST'])
def basicmembers_page():
    if request.method == 'GET':
        basicmembers = app.store.get_basicmembers()
        now = datetime.datetime.now()
        return render_template('basicmembers.html', basicmembers=basicmembers,
                               current_time=now.ctime())
    elif  'basicmembers_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('basicmembers_to_delete')
            for key in keys:
                app.store.delete_basicmember(int(key))
            return redirect(url_for('basicmembers_page'))
        elif  request.form['submit'] == 'search' :
            keyword=request.form['search']
            basicmembers = app.store.search_basicmember(keyword)
            now = datetime.datetime.now()
            return render_template('basicmembers.html', basicmembers=basicmembers,
                               current_time=now.ctime())
    else:
        name = request.form['name']
        surname = request.form['surname']
        nickname = request.form['nickname']
        email = request.form['email']
        password = request.form['password']
        byear = request.form['byear']
        city = request.form['city']
        interests = request.form['interests']
        gender = request.form.get('gender')

        now = str((datetime.datetime.now()));
        now = now[:-7]
        if (app.store.check_admin(email)):
            role = 'admin'
        else:
            role = 'user'
        basicmember = Basicmember(name, surname, nickname, gender, email,password, byear, city, interests, now, now, role)
        app.store.add_basicmember(basicmember)

        return render_template('login.html')



@app.route('/basicmember/<int:key>', methods=['GET', 'POST'])
def basicmember_page(key):
    if request.method == 'GET':
        basicmember = app.store.get_basicmember(key)
        now = datetime.datetime.now()
        return render_template('basicmember.html', basicmember=basicmember,
                               current_time=now.ctime())
    else:
        name = request.form['name']
        surname = request.form['surname']
        nickname = request.form['nickname']
        email = request.form['email']
        password = request.form['password']
        byear = request.form['byear']
        city = request.form['city']
        interests = request.form['interests']
        gender = request.form.get('gender')
        app.store.update_basicmember(key, name, surname, nickname, gender, email,password, byear, city, interests)
        return redirect(url_for('basicmember_page', key=key))

@app.route('/basicmembers/add')
@app.route('/basicmember/<int:key>/edit')
def basicmember_edit_page(key=None):
    basicmember = app.store.get_basicmember(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('basicmember_edit.html', basicmember=basicmember,
                           current_time=now.ctime())