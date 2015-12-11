import datetime

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['txtemail']
        password = request.form['password']

        if(app.store.find_member(email,password)):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login_page'))
    return render_template('login.html')