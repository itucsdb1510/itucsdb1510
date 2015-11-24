import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from admin import Admin

@app.route('/admins', methods=['GET', 'POST'])
def admins_page():
    if request.method == 'GET':
        admins = app.store.get_admins()
        now = datetime.datetime.now()
        return render_template('admins.html', admins=admins,
                               current_time=now.ctime())
    elif  'admins_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('admins_to_delete')
            for key in keys:
                app.store.delete_admin(int(key))
            return redirect(url_for('admins_page'))
        elif  request.form['submit'] == 'search' :
            keyword=request.form['search']
            admins = app.store.search_admin(keyword)
            now = datetime.datetime.now()
            return render_template('admins.html', admins=admins,
                               current_time=now.ctime())
    else:
        name = request.form['name']
        surname = request.form['surname']
        nickname = request.form['nickname']
        email = request.form['email']
        password = request.form['password']
        year = request.form['year']
        admin = Admin(name, surname, nickname, email,password, year)
        app.store.add_admin(admin)
        return redirect(url_for('admin_page', key=app.store.admin_last_key))



@app.route('/admin/<int:key>', methods=['GET', 'POST'])
def admin_page(key):
    if request.method == 'GET':
        admin = app.store.get_admin(key)
        now = datetime.datetime.now()
        return render_template('admin.html', admin=admin,
                               current_time=now.ctime())
    else:
        name = request.form['name']
        surname = request.form['surname']
        nickname = request.form['nickname']
        email = request.form['email']
        password = request.form['password']
        year = request.form['year']
        app.store.update_admin(key,name, surname, nickname, email,password, year)
        return redirect(url_for('admin_page', key=key))

@app.route('/admins/add')
@app.route('/admin/<int:key>/edit')
def admin_edit_page(key=None):
    admin = app.store.get_admin(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('admin_edit.html', admin=admin, current_time=now.ctime())

