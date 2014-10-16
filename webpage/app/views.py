from flask import render_template, abort
from calendar import Calendar
from datetime import date
from app import app
from scrape import get_content


@app.route('/', defaults={'year': 2014})
@app.route('/<int:year>/')
def index(year):
	user = {'nickname': 'Dartmouth'}  # fake user
	cal = Calendar(0)
	cal.setfirstweekday(6)  # 6 represents Sunday. Sets first weekday to Sunday.
	try:
		if not year:
			year = date.today().year
		cal_list = [cal.monthdatescalendar(year, i+1) for i in xrange(12)]
	except Exception, e:
		abort(404)
	else:
		return render_template('index.html', title='Home', user=user, year=year, cal=cal_list)
	abort(404)

@app.route('/scraper')
def scraper():
	return render_template('scrape.html',links=get_content())