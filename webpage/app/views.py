from flask import render_template
from app import app
from scrape import get_content
import requests

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Keggy'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/scraper')
def scraper():
	return get_content()