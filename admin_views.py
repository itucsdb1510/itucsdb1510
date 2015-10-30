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
    elif 'admins_to_delete' in request.form:
        keys = request.form.getlist('admins_to_delete')
        for key in keys:
            app.store.delete_admin(int(key))
        return redirect(url_for('admins_page'))
    else:
        title = request.form['title']
        score = request.form['score']
        founder = request.form['founder']
        year = request.form['year']
        admin = Admin(title, score, founder, year)
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
        app.store.addMember(key)
        return redirect(url_for('admin_page', key=app.store.admin_last_key))

@app.route('/admins/add')
def admin_edit_page():
    now = datetime.datetime.now()
    return render_template('admin_edit.html', current_time=now.ctime())