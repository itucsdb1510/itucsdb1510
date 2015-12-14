import datetime
import time
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from category import Category
from config import app
from topic import Topic


@app.route('/topics', methods=['GET', 'POST', 'SEARCH'])
def topics_page():
    if request.method == 'GET':
        topics = app.store.get_topics()
        categories = app.store.get_categories()
        now = datetime.datetime.now()
        return render_template('topics.html', topics=topics,categories=categories,
                               current_time=now.ctime())
    elif 'topics_to_delete' in request.form  or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('topics_to_delete')
            for key in keys:
                app.store.delete_topic(int(key))
                return redirect(url_for('topics_page'))
        elif  request.form['submit'] == 'Search' :
            keyword=request.form['search']
            topics = app.store.search_topic(keyword)
            now = datetime.datetime.now()
            return render_template('topics.html', topics=topics,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        text= request.form['text']
        time=str((datetime.datetime.now()));
        time=time[:-7]
        category_id = request.form.get('categoryId')
        #time=request.form['time']
        topic = Topic(title, text, time, category_id)
        app.store.add_topic(topic)
        return redirect(url_for('topic_page', key=app.store.topic_last_key))



@app.route('/topic/<int:key>', methods=['GET', 'POST'])
def topic_page(key):
    if request.method == 'GET':
        topic = app.store.get_topic(key)
        #category = app.store.get_category(topic.categoryId)
        now = datetime.datetime.now()
        return render_template('topic.html', topic=topic,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        text = request.form['text']
        category_id = request.form['categoryId']
        #time=request.form['time']
        time=str((datetime.datetime.now()));
        time=time[:-7]
        app.store.update_topic(key, title,text,time,category_id)
        return redirect(url_for('topic_page', key=key))

@app.route('/topics/add')
@app.route('/topic/<int:key>/edit')
def topic_edit_page(key=None):
    topic = app.store.get_topic(key) if key is not None else None
    now = datetime.datetime.now()
    categories = app.store.get_categories()
    return render_template('topic_edit.html', topic=topic, categories=categories,
                           current_time=now.ctime())
