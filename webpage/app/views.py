from flask import render_template
from app import app
from scrape import get_content

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Keggy'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/scraper')
def scraper():
	return render_template('scrape.html',links=get_content())