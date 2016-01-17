import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash


DATABASE='/rpiapp/RPIapp.db'
DEBUG=True
SECRET_KEY='yogurt'


app = Flask(__name__)
app.config.from_object(__name__)
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


@app.route("/initialize")
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route("/")
def index():
    if not g.user:
        return render_template('login.html')
    return render_template("index.html", appList=query_db('select * from apps'))


@app.route("/signup")
def signup():
    return render_template("register.html")


@app.route("/admin_add_app", methods=['GET', 'POST'])
def admin_add_app():
#    if g.user:
#        return redirect(url_for('index'))
    error = None
    appcolor = request.form['appcolor']

    if request.method == 'POST':
        if not request.form['appname']:
            error = 'You have to enter a name for the app'
        elif not request.form['appurl']:
            error = 'You have to enter a url'
        elif not request.form['description']:
            error = 'You have to enter the description'
        elif not appcolor:
            appcolor='#888'
        else:
            db = get_db()
            db.execute('''insert into apps (name, description, url, color) values (?, ?, ?, ?)''',
              (request.form['appname'],
               request.form['description'],
               request.form['appurl'],
               appcolor))
            db.commit()
            return redirect(url_for('index'))
    return render_template('index.html', error=error)

@app.route("/delete/<appid>")
def deleteApp(appid):
    getUserId = get_user_id('admin')
    if getUserId != session['user_id']:
        return render_template('404.html')
    else:
        db = get_db()
        db.execute('delete from apps where appID=? ', [appid])
        db.commit()
    return redirect(url_for('index'))


@app.route("/edit/<appid>")
def editApp(appid):
    getUserId = get_user_id('admin')
    if getUserId != session['user_id']:
        return render_template('404.html')

    return render_template('editApp.html', app=query_db('select * from apps where appId=?', [appid]))


@app.route("/admin_edit_app", methods=['GET', 'POST'])
def admin_edit_app():
    getUserId = get_user_id('admin')
    if getUserId != session['user_id']:
        return render_template('404.html')

    error = None
    appcolor = request.form['appcolor']

    if request.method == 'POST':
        if not request.form['appname']:
            error = 'You have to enter a name for the app'
        elif not request.form['appurl']:
            error = 'You have to enter a url'
        elif not request.form['description']:
            error = 'You have to enter the description'
        elif not appcolor:
            appcolor='#888'
        else:
            db = get_db()
            db.execute('''update apps set name=?, description=?, url=?, color=? where appId=?'''
              (request.form['appname'],
               request.form['description'],
               request.form['appurl'],
               appcolor,
               int(request.form['appid'])))
            db.commit()
            return redirect(url_for('index'))
    return render_template('editApp.html', app=query_db('select * from apps where appId=?', [appid]), error=error)


@app.route("/app/<appname>")
def runApp(appname):
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if g.user:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db = get_db()
            db.execute('''insert into user (username, email, pw_hash) values (?, ?, ?)''',
              [request.form['username'], request.form['email'],
               generate_password_hash(request.form['password'])])
            db.commit()
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
