import datetime
import psycopg2 as dbapi2

from flask import abort
from flask import g
from flask import session
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from experience import Experience


@app.route('/experiences', methods=['GET', 'POST'])
def experiences_page():
    if 'username' in session:
        if request.method == 'GET':
            experiences = app.store.get_experiences()
            now = datetime.datetime.now()
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM TOPMEMBERS")
                connection.commit()
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("(select userid, count(userid) from members inner join experience on(userid=memberid) group by userid limit 5) order by count(userid) desc")
                cr=cursor.fetchall()
                topmembers = [(row[0],row[1] )
                              for row in cr]
                connection.commit()
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                for userid, count in topmembers:
                    query = "INSERT INTO TOPMEMBERS (USERID, COUNT) VALUES ( %s, %s)"
                    cursor.execute(query, (userid, count))
                counter=0
                for userid, count in topmembers:
                    cursor.execute("select username from members where memberid='%s';"%userid)
                    user= cursor.fetchone()
                    topmembers[counter]=user[0],count*10
                    counter=counter+1
                connection.commit()
                return render_template('experiences.html', experiences=experiences,topmembers=topmembers,
                                       current_time=now.ctime())
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""DROP TABLE TOPMEMBERS""")
                connection.commit()


        elif 'experiences_to_delete' in request.form or 'search' in request.form:
            if request.form['submit'] == 'Delete':
                keys = request.form.getlist('experiences_to_delete')
                for key in keys:
                    app.store.delete_experience(int(key))
                return redirect(url_for('experiences_page'))
            elif  request.form['submit'] == 'Search' :
                keyword=request.form['search']
                experiences = app.store.search_experience(keyword)
                now = datetime.datetime.now()
                return render_template('experiences.html', experiences=experiences,
                                   current_time=now.ctime())
        else:

            title = request.form['title']
            start = request.form['start']
            finish = request.form['finish']
            period = request.form['period']
            length=request.form['length']
            name = session['username']
            experience = Experience(title, name, start, finish,period,length)
            app.store.add_experience(experience)
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("UPDATE  MEMBERS SET SCORE=SCORE+10 WHERE username='%s';"%name)
                connection.commit()

            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT memberid FROM MEMBERS WHERE username='%s';"%name)
                id = cursor.fetchone()
                connection.commit()
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = ("UPDATE EXPERIENCE SET userid=%s  WHERE (id=%s)")
                key=app.store.exp_key
                cursor.execute(query, (id[0],key))
                connection.commit()
            now = datetime.datetime.now()
            return redirect(url_for('experience_page', key=app.store.exp_key))
    else:
        return redirect(url_for('guest_page'))



@app.route('/experience/<int:key>', methods=['GET', 'POST'])
def experience_page(key):
    if request.method == 'GET':
        experience = app.store.get_experience(key)
        now = datetime.datetime.now()
        if 'username' in session:
            aname = session['username']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT USERNAME FROM EXPERIENCE WHERE id='%s';"%key)
                uname = cursor.fetchone()
                connection.commit()
                if (uname[0]==aname):
                    visible=1
                else:
                    visible=0
                now = datetime.datetime.now()
                return render_template('experience.html', experience=experience,visible=visible,current_time=now.ctime())
        else:
            return redirect(url_for('guest_page'))

    else:
        title = request.form['title']
        start = request.form['start']
        finish = request.form['finish']
        period = request.form['period']
        length=request.form['length']
        name = session['username']
        app.store.update_experience(key, title,name, start, finish,period,length)
        return redirect(url_for('experience_page', key=key))

@app.route('/experiences/add')
@app.route('/experience/<int:key>/edit')
def experience_edit_page(key=None):
    if 'username' in session:
        #experience = app.store.get_experience(key) if key is not None else None
        if key:
            experience = app.store.get_experience(key)
            aname = session['username']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT USERNAME FROM EXPERIENCE WHERE id='%s';"%key)
                uname = cursor.fetchone()
                connection.commit()
                if (uname[0]==aname):
                    now = datetime.datetime.now()
                    return render_template('experience_edit.html', experience=experience,current_time=now.ctime())
                else:
                    return render_template('guest.html')
        else:
            now = datetime.datetime.now()
            return render_template('experience_edit.html',current_time=now.ctime())
    else:
        return redirect(url_for('guest_page'))


