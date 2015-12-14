import datetime

import os
import json
import sys
from werkzeug import secure_filename
from flask import send_from_directory
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
from bike import Bike


UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#request.form.get('delete',None)
@app.route('/bikes', methods=['GET', 'POST'])
def bikes_page():
    if 'username' in session:
        if request.method == 'GET':
            bikes = app.store.get_bikes()
            now = datetime.datetime.now()
            return render_template('bikes.html', bikes=bikes,
                                   current_time=now.ctime())

        elif  'bike_to_delete' in request.form or 'search' in request.form:
            if request.form['submit'] == 'Delete':
                keys = request.form.getlist('bikes_to_delete')
                for key in keys:
                    app.store.delete_bike(int(key))
                return redirect(url_for('bikes_page'))

            elif  request.form['submit'] == 'Search' :
                keyword=request.form['search']
                bikes = app.store.search_bike(keyword)
                now = datetime.datetime.now()
                return render_template('bikes.html', bikes=bikes,
                                   current_time=now.ctime())
        else:
                model = request.form['model']
                brand = request.form['brand']
                type = request.form.get('type')
                size = request.form['size']
                year = request.form['year']
                price = request.form['price']
                name = session['username']
                bike = Bike(model,brand,type,size,year,price,name)
                app.store.add_bike(bike)
                image=request.files['file']
                if image:
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/image/bikes/' + str(app.store.bike_last_key) + '.jpg'))

                return redirect(url_for('bike_page', key=app.store.bike_last_key))
    else:
        return redirect(url_for('guest_page'))



@app.route('/bike/<int:key>', methods=['GET', 'POST'])
def bike_page(key):
    if 'username' in session:
        if request.method == 'GET':
            bike = app.store.get_bike(key)
            now = datetime.datetime.now()
            return render_template('bike.html', bike=bike, key = str(key),
                                   current_time=now.ctime())
        else:
            model = request.form['model']
            brand = request.form['brand']
            type = request.form.get('type')
            size = request.form['size']
            year = request.form['year']
            price = request.form['price']
            image=request.files['file']
            if image:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/image/bikes/' + str(key) + '.jpg'))

            app.store.update_bike(key,model,brand,type,size,year,price)
            return redirect(url_for('bike_page', key=key))
    else:
        return redirect(url_for('guest_page'))


@app.route('/bikes/add')
@app.route('/bike/<int:key>/edit')
def bike_edit_page(key=None):
    if 'username' in session:
        if key:
            bike = app.store.get_bike(key) if key is not None else None
            aname = session['username']
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT USERNAME FROM BIKE WHERE id='%s';"%key)
                uname = cursor.fetchone()
                connection.commit()
                if (uname[0]==aname):
                    now = datetime.datetime.now()
                    return render_template('bike_edit.html', bike=bike,
                                           current_time=now.ctime())
                else:
                    return render_template('guest.html')
        else:
            now = datetime.datetime.now()
            return render_template('bike_edit.html',current_time=now.ctime())
    else:
        return redirect(url_for('guest_page'))
