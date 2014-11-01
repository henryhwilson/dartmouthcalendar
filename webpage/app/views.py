from flask import render_template, abort, request
from calendar import Calendar
from datetime import date
from app import app
from scrape import get_content, get_event
from datetime import datetime
import urllib

@app.route('/')
@app.route('/index')
def index():
	hourNow = datetime.now().hour
	categories = []
	categories.append('Greek')
	categories.append('Social')
	categories.append('Sports')
	categories.append('Misc')
	events = []
	event1 = {'from':'Beta Alpha Omega','subject':'18s: Dance Show Tonight @ Beta Alpha Omega',
	'category':'Greek','time_event':'7PM','date_event':'today'} 
	events.append(event1)
	event2 = {'from':'Sigma Phi Epsilon','subject':'Fusion @ SigEp Tonight!','category':'Greek','time_event':'10PM','date_event':'today'}
	events.append(event2)
	event3 = {'from':'Collis Governing Board','subject':'HAUNTED HOUSE DANCE','category':'Social','time_event':'8PM 11/4','date_event':'upcoming'}
	events.append(event3)
	event4 = {'from':'Kappa Kappa Kappa','subject':'Tri-Kap Dance Party @ 11:30','category':'Greek','time_event':'11:30PM','date_event':'tomorrow'}
	events.append(event4)
	event5 = {'from':'Dartmouth Classical Ballet Theatre','subject':'open ballet class on Saturday!','category':'Misc','time_event':'10-11:30AM','date_event':'tomorrow'}
	events.append(event5)
	nicknames = {'Delta Delta Delta':'TriDelt','Kappa Kappa Gamma':'KKG','Alpha Delta':'AD',
	'Sigma Phi Epsilon':'SigEp','Alpha Chi Alpha':'AXA','Beta Alpha Omega':'Beta','Chi Heorot':'Heorot',
	'Collis Governing Board':'One Wheelock','Kappa Kappa Kappa':'Tri-Kap'}
	today_total_events = 0
	today_cat_freq = {'Greek':0,'Social':0,'Sports':0,'Misc':0}
	tomorrow_total_events = 0
	tomorrow_cat_freq = {'Greek':0,'Social':0,'Sports':0,'Misc':0}
	upcoming_total_events = 0
	upcoming_cat_freq = {'Greek':0,'Social':0,'Sports':0,'Misc':0}
	for event in events:
		if (event['date_event'] == 'today'):
			today_cat_freq[event['category']] += 1
			today_total_events += 1
		elif (event['date_event'] == 'tomorrow'):
			tomorrow_cat_freq[event['category']] += 1
			tomorrow_total_events += 1
		elif (event['date_event'] == 'upcoming'):
			upcoming_cat_freq[event['category']] += 1
			upcoming_total_events += 1
		if (not event['from'] in nicknames.keys()):
			nicknames[event['from']] = event['from']
	if hourNow < 19 and hourNow > 4: # Display "Tonight" if between 7:00PM and 4:59AM
		isDay = True
	else:
		isDay = False
	return render_template('index.html', is_day=isDay, categories=categories, today_cat_freq=today_cat_freq, 
		tomorrow_cat_freq=tomorrow_cat_freq, upcoming_cat_freq=upcoming_cat_freq,
		events=events, today_total_events=today_total_events, tomorrow_total_events=tomorrow_total_events,
		upcoming_total_events=upcoming_total_events, nicknames=nicknames)

@app.route('/scraper', methods=['GET'])
def scraper():
	url = request.args.get("event_url")
	if (url == None):
		return_data = get_content()
	else:
		return_data = get_event(url)
	return render_template('scrape.html',data=return_data,event_url=url)
