import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from cycroute import Cycroute

@app.route('/cycroutes', methods=['GET', 'POST'])
def cycroutes_page():
    if request.method == 'GET':
        cycroutes = app.store.get_cycroutes()
        now = datetime.datetime.now()
        return render_template('cycroutes.html', cycroutes=cycroutes,
                               current_time=now.ctime())
    elif 'cycroutes_to_delete' in request.form:
        keys = request.form.getlist('cycroutes_to_delete')
        for key in keys:
            app.store.delete_cycroute(int(key))
        return redirect(url_for('cycroutes_page'))
    else:
        title = request.form['title']
        username = request.form['username']
        start = request.form['start']
        finish = request.form['finish']
        length=request.form['length']
        
        cycroute = Cycroute(title, username, start, finish,length)
        app.store.add_cycroute(cycroute)
        return redirect(url_for('cycroute_page', key=app.store.cycroute_last_key))



@app.route('/cycroute/<int:key>', methods=['GET', 'POST'])
def cycroute_page(key):
    if request.method == 'GET':
        cycroute = app.store.get_cycroute(key)
        now = datetime.datetime.now()
        return render_template('cycroute.html', cycroute=cycroute,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        username = request.form['username']
        start = request.form['start']
        finish = request.form['finish']
        length=request.form['length']
        app.store.update_cycroute(key, title,username, start, finish,length)        
        return redirect(url_for('cycroute_page', key=app.store.cycroute_last_key))

@app.route('/cycroutes/add')
def cycroute_edit_page():
    now = datetime.datetime.now()
    return render_template('cycroute_edit.html', current_time=now.ctime())

