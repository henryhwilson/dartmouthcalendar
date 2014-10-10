import requests
from bs4 import BeautifulSoup

def get_content():
	r = requests.get('https://listserv.dartmouth.edu/scripts/wa.exe?A0=CAMPUS-EVENTS')
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
   							events.append(event.text)
   				iterator = iterator + 1
	return events