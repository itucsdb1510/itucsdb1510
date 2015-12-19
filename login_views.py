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
                query = "SELECT USERNAME, ROLE FROM MEMBERS WHERE email=%s UNION SELECT USERNAME, ROLE FROM ADMIN WHERE email=%s"
                cursor.execute(query,(email,email))
                connection.commit()
           # role,lastlogin,name = cursor.fetchone()
                name, role = cursor.fetchone()
                g.role = role
          #g.lastlogin = lastlogin
                session['username'] = name
                perm=app.store.check_admin(email,password)
                if perm==0:
                    experiences=app.store.get_myexperiences(name)
                    return render_template('home.html',experiences=experiences)

                else:
                   now = datetime.datetime.now()
                   teams=app.store.get_top5team()
                   professionalmembers=app.store.get_top5member()
                   numa=app.store.get_numofadmins()
                   numb=app.store.get_numofbasicmembers()
                   nump=app.store.get_numofprofessionalmembers()
                   return render_template('adminpanel.html',teams=teams,professionalmembers=professionalmembers,numa=numa,numb=numb,nump=nump, current_time=now.ctime())



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
    return redirect(url_for('guest'))
