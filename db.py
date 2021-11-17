# http://flask.pocoo.org/docs/1.0/tutorial/database/
import psycopg2
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    g.db = psycopg2.connect(DATABASE_URL)

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

CREATE_USERTABLE=f"""
CREATE TABLE IF NOT EXISTS usertable (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  role TEXT
);
"""

def init_db():
    db = get_db()
    db.executescript(CREATE_USERTABLE)

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
