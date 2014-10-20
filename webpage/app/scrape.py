import requests
import urllib
from bs4 import BeautifulSoup

def get_content():
	r = requests.get('https://listserv.dartmouth.edu/scripts/wa.exe?A1=ind1410C&L=CAMPUS-EVENTS&O=D&H=0&D=1&T=1')
	soup = BeautifulSoup(r.text)
	events = []
	iterator = 0
	for link in soup.find_all('a'):
		if iterator > 0:
			break
		href = link.get('href')
		if href:
			if  '/scripts/wa.exe?A1=' in href:
   				r = requests.get('https://listserv.dartmouth.edu'+href)
   				soup2 = BeautifulSoup(r.text)
   				for event in soup2.find_all('a'):
   					if event.get('href'):
   						if '/scripts/wa.exe?A2=' in event.get('href'):
   							data = []
   							data.append(event.text)
   							data.append(urllib.quote_plus(event.get('href')))
   							events.append(data)
   				iterator = iterator + 1
	return events

def get_event(event_url,event_subject):
	url = ''
	txt = ''
	data = []
	event_url = ''+urllib.unquote_plus(event_url)
	r = requests.get('https://listserv.dartmouth.edu'+event_url)
	soup = BeautifulSoup(r.text)
	for link in soup.find_all('a'):
		if (link.get('href')):
			if (link.text == 'text/plain'):
				url = link.get('href')
				break
	if (url != ''):
		r = requests.get('https://listserv.dartmouth.edu'+url)
		soup = BeautifulSoup(r.text)
		for pre in soup.find_all('pre'):
			txt = pre.text
	data.append(txt)
	data.append(event_subject)
	return data