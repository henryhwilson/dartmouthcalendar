from flask import render_template, abort, request
from calendar import Calendar
from datetime import date
from app import app
from scrape import get_content, get_event, get_event2, get_content2
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import urllib

@app.route('/add_event')
def add_event():
	return render_template('addevent.html')

@app.route('/unsubscribe')
def unsubscribe():
	return render_template('unsubscribe.html')

@app.route('/faq')
def faq():
	return render_template('faq.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/ajax/blitzMachine')
def blitzMachine():
	hourNow = datetime.now().hour
	categories = []
	categories.append('Greek')
	categories.append('Social')
	categories.append('Sports')
	categories.append('Performances')
	categories.append('Talks and Discussions')
	categories.append('Misc')
	realEvents = get_content2()

	today_total_events = 0
	today_cat_freq = {'Greek':0,'Social':0,'Sports':0,'Performances':0, 'Talks and Discussions':0, 'Misc':0}
	tomorrow_total_events = 0
	tomorrow_cat_freq = {'Greek':0,'Social':0,'Sports':0,'Performances':0,'Talks and Discussions':0,'Misc':0}
	upcoming_total_events = 0
	upcoming_cat_freq = {'Greek':0,'Social':0,'Sports':0,'Performances':0,'Talks and Discussions':0, 'Misc':0}
	for event in realEvents:
		if (event['date_event'] == 'today'):
			today_cat_freq[event['category']] += 1
			today_total_events += 1
		elif (event['date_event'] == 'tomorrow'):
			tomorrow_cat_freq[event['category']] += 1
			tomorrow_total_events += 1
		elif (event['date_event'] == 'upcoming'):
			upcoming_cat_freq[event['category']] += 1
			upcoming_total_events += 1
		event['blitz_date'] = event['blitz_date'].strftime('%A, %b %d %I:%M%p')
		# if (not event['from'] in nicknames.keys()):
		# 	nicknames[event['from']] = event['from'].strip()

	if hourNow < 19 and hourNow > 4: # Display "Tonight" if between 7:00PM and 4:59AM
		isDay = True
	else:
		isDay = False
	return render_template('blitz-machine.html', is_day=isDay, categories=categories, today_cat_freq=today_cat_freq, 
		tomorrow_cat_freq=tomorrow_cat_freq, upcoming_cat_freq=upcoming_cat_freq,
		events=realEvents, today_total_events=today_total_events, tomorrow_total_events=tomorrow_total_events,
		upcoming_total_events=upcoming_total_events)

@app.route('/ajax/getEventHTML', methods=['GET'])
def getEventHTML():
	url = request.args.get("url")
	sender = request.args.get("from")
	date = request.args.get("date")
	if (date == None):
		date = ""
	else:
		date = "Sent " + date
	if url == None:
		return None
	url = ''+urllib.unquote_plus(url)
	r = requests.get(url)
	if "<div id=\"divtagdefaultwrapper\"" in r.text:
		indexOfDiv = r.text.index("<div id=\"divtagdefaultwrapper\"")
		headers = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"><html><head><title>LISTSERV 16.0 - CAMPUS-EVENTS Archives</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"><style type=\"text/css\" style=\"display:none\"><!-- p { margin-top: 0px; margin-bottom: 0px; }--></style></head><body style=\"background-color: white\">"
		headers = headers + "<h2 style=\"font-family: verdana; padding-bottom: 5px; margin-bottom: 0;\">Blitz from <em>" + sender + "</em></h2>"
		headers = headers + "<h4 style=\"font-family: verdana; font-weight: normal; color: grey; padding-top: 0; margin-top: 0;\">" + date + "</h4>"
	elif "</div><meta" in r.text:
		indexOfDiv = r.text.index("</div><meta")+len("</div>")
		headers = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"><html><head><title>LISTSERV 16.0 - CAMPUS-EVENTS Archives</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"><style type=\"text/css\" style=\"display:none\"><!-- p { margin-top: 0px; margin-bottom: 0px; }--></style></head><body style=\"background-color: white\">"
		headers = headers + "<h2 style=\"font-family: verdana; padding-bottom: 5px; margin-bottom: 0;\">Blitz from <em>" + sender + "</em></h2>"
		headers = headers + "<h4 style=\"font-family: verdana; font-weight: normal; color: grey; padding-top: 0; margin-top: 0;\">" + date + "</h4>"
	else:
		headers = "<style>body { background-color: white; }</style>"
		indexOfDiv = 0
	output = headers + r.text[indexOfDiv:]
	while "b-print.png\"" in output:
		indexOfSrc = output.index("b-print.png")+11
		output = output[:indexOfSrc] + '' + output[indexOfSrc+1:]
	while "src=\"/scripts" in output or "src=\"/archives" in output:
		indexOfSrc = output.index("src=\"")+4
		output = output[:indexOfSrc] + 'https://listserv.dartmouth.edu' + output[indexOfSrc+1:]
	return output

@app.route('/scraper', methods=['GET'])
def scraper():
	url = request.args.get("event_url")
	if (url == None):
		return_data = get_content()
	else:
		return_data = get_event(url)
	return render_template('scrape.html',data=return_data,event_url=url)
