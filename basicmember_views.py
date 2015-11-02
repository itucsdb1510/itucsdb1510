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
    elif 'basicmembers_to_delete' in request.form:
        keys = request.form.getlist('basicmembers_to_delete')
        for key in keys:
            app.store.delete_basicmember(int(key))
        return redirect(url_for('basicmembers_page'))
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


        basicmember = Basicmember(name, surname, nickname, gender, email,password, byear, city, interests)
        app.store.add_basicmember(basicmember)
        return redirect(url_for('basicmember_page', key=app.store.basicmember_last_key))



@app.route('/basicmember/<int:key>', methods=['GET', 'POST'])
def basicmember_page(key):
    if request.method == 'GET':
        basicmember = app.store.get_basicmember(key)
        now = datetime.datetime.now()
        return render_template('basicmember.html', basicmember=basicmember,
                               current_time=now.ctime())
    else:
        return redirect(url_for('basicmember_page', key=app.store.basicmember_last_key))

@app.route('/basicmembers/add')
def basicmember_edit_page():
    now = datetime.datetime.now()
    return render_template('basicmember_edit.html', current_time=now.ctime())

