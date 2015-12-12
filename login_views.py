import datetime

import psycopg2 as dbapi2

from flask import abort
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from config import app

from psycopg2 import IntegrityError
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['txtemail']
        password = request.form['password']
        if(app.store.find_member(email,password)):
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT role, lastlogin, name FROM MEMBERS WHERE email='%s';"%email)
                connection.commit()
            role,lastlogin,name = cursor.fetchone()
            g.role = role
            g.lastlogin = lastlogin
            session['username'] = name
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_page'))
    return render_template('login.html')

@app.route('/profile/<username>')
def profile(username):
        with dbapi2.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT memberid FROM MEMBERS WHERE name='%s';"%username)
            connection.commit()
        key = cursor.fetchone()
        basicmember = app.store.get_basicmember(key)
        return render_template('profile.html', user=basicmember)



@app.route('/logout')
def logout():
    return redirect(url_for('home'))