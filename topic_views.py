import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from topic import Topic

@app.route('/topics', methods=['GET', 'POST', 'SEARCH'])
def topics_page():
    if request.method == 'GET':
        topics = app.store.get_topics()
        now = datetime.datetime.now()
        return render_template('topics.html', topics=topics,
                               current_time=now.ctime())
    elif 'topics_to_delete' in request.form  or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('topics_to_delete')
            for key in keys:
                app.store.delete_topic(int(key))
                return redirect(url_for('topics_page'))
        elif  request.form['submit'] == 'search' :
            keyword=request.form['search']
            topics = app.store.search_topic(keyword)
            now = datetime.datetime.now()
            return render_template('topics.html', topics=topics,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        text= request.form['text']
        time=request.form['time']
        #post=request.form['post']
        #poster=request.form['poster']
        topic = Topic(title, text, time)
        app.store.add_topic(topic)
        return redirect(url_for('topic_page', key=app.store.topic_last_key))



@app.route('/topic/<int:key>', methods=['GET', 'POST'])
def topic_page(key):
    if request.method == 'GET':
        topic = app.store.get_topic(key)
        now = datetime.datetime.now()
        return render_template('topic.html', topic=topic,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        text = request.form['text']
        time=request.form['time']
        #post=request.form['post']
        #poster=request.form['poster']
        app.store.update_topic(key, title,text,time)
        return redirect(url_for('topic_page', key=app.store.topic_last_key))

@app.route('/topics/add')
def topic_edit_page():
    now = datetime.datetime.now()
    return render_template('topic_edit.html', current_time=now.ctime())