from flask import render_template, abort, request
from calendar import Calendar
from datetime import date
from app import app
from scrape import get_content, get_event


@app.route('/', defaults={'year': 2014})
@app.route('/<int:year>/')
@app.route('/index', defaults={'year': 2014})
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

@app.route('/scraper', methods=['GET'])
def scraper():
	url = request.args.get("event_url")
	if (url == None):
		return_data = get_content()
	else:
		return_data = get_event(url)
	return render_template('scrape.html',data=return_data,event_url=url)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html', 
        title = 'Sign In')

@app.route('/account', methods = ['GET', 'POST'])
def account():
    return render_template('account.html', 
        title = 'Sign In')
