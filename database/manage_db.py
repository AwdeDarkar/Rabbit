"""
manage db
====================================================================================================

Tools to open, create, and interface with the sqlite database.

----------------------------------------------------------------------------------------------------

**Created**
    10.22.18
**Updated**
    10.22.18 by Darkar
**Author**
    Darkar
"""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """ Return a reference to the database connection and create it if it doesn't exist """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

    return g.db

def close_db(err=None): #pylint: disable=unused-argument
    """ Close the connection to the database if it is still open """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """ Clear the existing data and create new tables """
    db = get_db()

    with current_app.open_resource("./database/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    """ Click command to call ``init_db`` """
    init_db()
    click.echo("Database initialized")

def init_app(app):
    """ Initialize the app with the database """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
