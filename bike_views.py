import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from bike import Bike


@app.route('/bikes', methods=['GET', 'POST'])
def bikes_page():
    if request.method == 'GET':
        bikes = app.store.get_bikes()
        now = datetime.datetime.now()
        return render_template('bikes.html', bikes=bikes,
                               current_time=now.ctime())
    elif 'bikes_to_delete' in request.form:
        keys = request.form.getlist('bikes_to_delete')
        for key in keys:
            app.store.delete_bike(int(key))
        return redirect(url_for('bikes_page'))
    else:
        model = request.form['model']
        brand = request.form['brand']
        bike_type = request.form.get('bike_type')
        size = request.form['size']
        year = request.form['year']
        price = request.form['price']
        bike = Bike(model,brand,bike_type,size,year,price)
        app.store.add_bike(bike)
        return redirect(url_for('bike_page', key=app.store.bike_last_key))


@app.route('/bike/<int:key>', methods=['GET', 'POST'])
def bike_page(key):
    if request.method == 'GET':
        bike = app.store.get_bike(key)
        now = datetime.datetime.now()
        return render_template('bike.html', bike=bike,
                               current_time=now.ctime())
    else:
        
        price = request.form['price']
        app.store.update_bike(key,price)
        return redirect(url_for('bike_page', key=app.store.bike_last_key))


@app.route('/bikes/add')
def bike_edit_page():
    now = datetime.datetime.now()
    return render_template('bike_edit.html', current_time=now.ctime())
    