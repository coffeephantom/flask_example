import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash


app = Flask(__name__)

# app configure
DATABASE = '/home/coffeephantom/workspace/python/flaskr/static/db'
DEBUG = True
SECRET_KEY = ',\xbc\x9b\x96\xe6`\xfcI\xc8_\xca\x82\n\xa7"\x8dWe\xe38\xa8\xd1\x1c\xbf'
USERNAME = 'admin'
PASSWORD = 'admin'

# load configure
app.config.from_object(__name__)


def connet_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(DATABASE)
    # rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """
    Opens a new database connection if there is none yet for  the current
    application context.
    """
    if not hasattr(g, 'db'):
        g.db = connet_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    """
    Closes the dabase again at the end of the request
    """
    if hasattr(g, 'db'):
        g.db.close()


def init_db():
    #pdb.set_trace()
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def show_entries():
    # pdb.set_trace()
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[0]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    g.db.execute(('insert into entries (title,text) values (?,?)'), [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.methods == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid Username!"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid Password!"
        else:
            session['logged_in'] = True
            flash('You were logged in ...')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You were logged out.")
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)
