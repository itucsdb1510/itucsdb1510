import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from announcement import Announcement

@app.route('/announcements', methods=['GET', 'POST', 'SEARCH'])
def announcements_page():
    if request.method == 'GET':
        announcements = app.store.get_announcements()
        now = datetime.datetime.now()
        return render_template('announcements.html', announcements=announcements,
                               current_time=now.ctime())
    elif 'announcements_to_delete' in request.form or 'search' in request.form:
        if request.form['submit'] == 'Delete':
            keys = request.form.getlist('announcements_to_delete')
            for key in keys:
                app.store.delete_announcement(int(key))
            return redirect(url_for('announcements_page'))
        elif  request.form['submit'] == 'search' :
            keyword=request.form['search']
            announcements = app.store.search_announcement(keyword)
            now = datetime.datetime.now()
            return render_template('announcements.html', announcements=announcements,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        text= request.form['text']
        announcement = Announcement(title, text)
        app.store.add_announcement(announcement)
        return redirect(url_for('announcement_page', key=app.store.announcement_last_key))



@app.route('/announcement/<int:key>', methods=['GET', 'POST'])
def announcement_page(key):
    if request.method == 'GET':
        announcement = app.store.get_announcement(key)
        now = datetime.datetime.now()
        return render_template('announcement.html', announcement=announcement,
                               current_time=now.ctime())
    else:
        title = request.form['title']
        text = request.form['text']
        app.store.update_announcement(key, title,text)
        return redirect(url_for('announcement_page', key=app.store.announcement_last_key))

@app.route('/announcements/add')
@app.route('/announcement/<int:key>/edit')
def announcement_edit_page(key=None):
    announcement = app.store.get_announcement(key) if key is not None else None
    now = datetime.datetime.now()
    return render_template('announcement_edit.html', announcement=announcement,
                           current_time=now.ctime())