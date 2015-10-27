import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from category import Category

@app.route('/categories', methods=['GET', 'POST'])
def categories_page():
    if request.method == 'GET':
        categories = app.store.get_categories()
        now = datetime.datetime.now()
        return render_template('categories.html', categories=categories,
                               current_time=now.ctime())
    elif 'categories_to_delete' in request.form:
        keys = request.form.getlist('categories_to_delete')
        for key in keys:
            app.store.delete_category(int(key))
        return redirect(url_for('categories_page'))
    else:
        title = request.form['title']
        category = Category(title)
        app.store.add_category(category)
        return redirect(url_for('category_page', key=app.store.category_last_key))



@app.route('/category/<int:key>', methods=['GET', 'POST'])
def category_page(key):
    if request.method == 'GET':
        category = app.store.get_category(key)
        now = datetime.datetime.now()
        return render_template('category.html', category=category,
                               current_time=now.ctime())
    else:
        return redirect(url_for('category_page', key=app.store.category_last_key))

@app.route('/categories/add')
def category_edit_page():
    now = datetime.datetime.now()
    return render_template('category_edit.html', current_time=now.ctime())