from flask import Flask, g
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing

# database configuration
DATABASE = 'testevents.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
from app import views
from app import scrape
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('db_schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

init_db()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()