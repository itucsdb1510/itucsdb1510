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
from cycroute import Cycroute

@app.route('/cycroutes', methods=['GET', 'POST'])
def cycroutes_page():
    if 'username' in session:
        if request.method == 'GET':
            cycroutes = app.store.get_cycroutes()
            now = datetime.datetime.now()
            return render_template('cycroutes.html', cycroutes=cycroutes,
                                   current_time=now.ctime())

        elif 'cycroutes_to_delete' in request.form or 'search' in request.form:
            if request.form['submit'] == 'Delete':
                keys = request.form.getlist('cycroutes_to_delete')
                for key in keys:
                    app.store.delete_cycroute(int(key))
                return redirect(url_for('cycroutes_page'))
            elif  request.form['submit'] == 'Search' :
                keyword=request.form['search']
                cycroutes = app.store.search_cycroute(keyword)
                now = datetime.datetime.now()
                return render_template('cycroutes.html', cycroutes=cycroutes,
                                   current_time=now.ctime())
        else:
            title = request.form['title']
            start = request.form['start']
            finish = request.form['finish']
            length=request.form['length']
            name = session['username']
            cycroute = Cycroute(title, name, start, finish,length)
            app.store.add_cycroute(cycroute)
            return redirect(url_for('cycroute_page', key=app.store.cycroute_last_key))
    else:
        return redirect(url_for('guest_page'))


@app.route('/cycroute/<int:key>', methods=['GET', 'POST'])
def cycroute_page(key):
    if request.method == 'GET':
        cycroute = app.store.get_cycroute(key)
        now = datetime.datetime.now()
        return render_template('cycroute.html', cycroute=cycroute,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        start = request.form['start']
        finish = request.form['finish']
        length=request.form['length']
        app.store.update_cycroute(key, title,start, finish,length)
        return redirect(url_for('cycroute_page', key=key))

@app.route('/cycroutes/add')
@app.route('/cycroute/<int:key>/edit')
def cycroute_edit_page(key=None):
    cycroute = app.store.get_cycroute(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('cycroute_edit.html',cycroute=cycroute, current_time=now.ctime())

