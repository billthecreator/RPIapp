

import os
import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

appList = [
    {
        "name"  : "First app name",
        "desc"  : "Short description about the first app",
        "url"   : "/firstApp",
        "color" : "blue"
    },
    {
        "name"  : "Second app name",
        "desc"  : "Short description about the second app",
        "url"   : "/secondApp",
        "color" : "green"
    },
    {
        "name"  : "Third app name",
        "desc"  : "Short description about the third app",
        "url"   : "/thirdApp",
        "color" : "yellow"
    },
    {
        "name"  : "Forth app name",
        "desc"  : "Short description about the forth app",
        "url"   : "/fourthApp",
        "color" : "red"
    }
]

DATABASE    = '/tmp/RPIapp.db'
SECRET_KEY  = 'yogurt'

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'RPIapp.db'),
    DEBUG=True,
    SECRET_KEY='yogurt',
    USERNAME='admin',
    PASSWORD='apple'
))
app.config.from_envvar('RPI_APP_SETTINGS', silent=True)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template("index.html", appList=appList)



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if session.get('logged_in'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
