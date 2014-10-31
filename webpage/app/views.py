from flask import render_template, abort, request
from calendar import Calendar
from datetime import date
from app import app
from scrape import get_content, get_event
from datetime import datetime

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
	'category':'Greek','date_event':'','date_blitzed':''} 
	events.append(event1)
	event2 = {'from':'Sigma Phi Epsilon','subject':'Fusion @ SigEp Tonight!','category':'Greek','date_event':'','date_blitzed':''}
	events.append(event2)
	event3 = {'from':'Collis Governing Board','subject':'HAUNTED HOUSE DANCE','category':'Social','date_event':'','date_blitzed':''}
	events.append(event3)
	nicknames = {'Delta Delta Delta':'TriDelt','Kappa Kappa Gamma':'KKG','Alpha Delta':'AD',
	'Sigma Phi Epsilon':'SigEp','Alpha Chi Alpha':'AXA','Beta Alpha Omega':'Beta','Chi Heorot':'Heorot',
	'Collis Governing Board':'One Wheelock'}
	cat_freq = {'Greek':0,'Social':0,'Sports':0,'Misc':0}
	for event in events:
		cat_freq[event['category']] += 1
	if hourNow < 19 and hourNow > 4: # Display "Tonight" if between 7:00PM and 4:59AM
		isDay = True
	else:
		isDay = False
	return render_template('index.html', is_day=isDay, categories=categories, cat_freq=cat_freq, events=events, nicknames=nicknames)

@app.route('/scraper', methods=['GET'])
def scraper():
	url = request.args.get("event_url")
	if (url == None):
		return_data = get_content()
	else:
		return_data = get_event(url)
	return render_template('scrape.html',data=return_data,event_url=url)
