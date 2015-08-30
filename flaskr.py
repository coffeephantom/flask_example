import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__, instance_relative_config=True)
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connet_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """
    Opens a new database connection if there is none yet for  the current
    application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connet_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """
    Closes the dabase again at the end of the request
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('shema.sql', mode='r') as f:
            db.cursor().executerscript(f.read())
        db.commit()


@app.route('/')
def show_entries():
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
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
