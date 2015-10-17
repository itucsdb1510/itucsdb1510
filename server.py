import datetime
import os

from flask import Flask
from flask import render_template
from pip._vendor.requests.packages.urllib3.util.timeout import current_time


app = Flask(__name__)


@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/teams')
def teams_page():
    now = datetime.datetime.now();
    return render_template('teams.html', current_time=now.ctime())

@app.route('/topics')
def topics_page():
    now = datetime.datetime.now();
    return render_template('topics.html', current_time=now.ctime())

if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
    app.run(host='0.0.0.0', port=int(PORT))
