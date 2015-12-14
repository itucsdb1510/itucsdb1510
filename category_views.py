import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from category import Category
from topic import Topic

@app.route('/categories', methods=['GET', 'POST', 'SEARCH'])
def categories_page():
    if request.method == 'GET':
        categories = app.store.get_categories()
        now = datetime.datetime.now()
        return render_template('categories.html', categories=categories,
                               current_time=now.ctime())
    elif 'categories_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('categories_to_delete')
            for key in keys:
                app.store.delete_category(int(key))
            return redirect(url_for('categories_page'))
        elif  request.form['submit'] == 'search' :
            keyword=request.form['search']
            categories = app.store.search_category(keyword)
            now = datetime.datetime.now()
            return render_template('categories.html', categories=categories,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        typee = request.form['typee']
        category = Category(title,typee)
        app.store.add_category(category)
        return redirect(url_for('category_page', key=app.store.category_last_key))



@app.route('/category/<int:key>', methods=['GET', 'POST'])
def category_page(key):
    if request.method == 'GET':
        topics = app.store.get_topics()
        category = app.store.get_category(key)
        now = datetime.datetime.now()
        return render_template('category.html', category=category,topics=topics,
                               current_time=now.ctime())
    else:
       title=request.form["title"]
       typee=request.form["typee"]
       app.store.update_category(key,title,typee)
       return redirect(url_for('category_page', key=app.store.category_last_key))

@app.route('/categories/add')
@app.route('/category/<int:key>/edit')
def category_edit_page(key=None):
    category=app.store.get_category(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('category_edit.html', category=category,
                           current_time=now.ctime())
