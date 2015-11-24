import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from bike import Bike

#request.form.get('delete',None)
@app.route('/bikes', methods=['GET', 'POST'])
def bikes_page():
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

        elif  request.form['submit'] == 'search' :
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
            bike = Bike(model,brand,type,size,year,price)
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
        model = request.form['model']
        brand = request.form['brand']
        type = request.form.get('type')
        size = request.form['size']
        year = request.form['year']
        price = request.form['price']
        app.store.update_bike(key,model,brand,type,size,year,price)
        return redirect(url_for('bike_page', key=key))


@app.route('/bikes/add')
@app.route('/bike/<int:key>/edit')
def bike_edit_page(key=None):
    bike = app.store.get_bike(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('bike_edit.html', bike=bike,
                           current_time=now.ctime())
