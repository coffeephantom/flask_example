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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
