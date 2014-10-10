import requests
from bs4 import BeautifulSoup

def get_content():
	r = requests.get('https://listserv.dartmouth.edu/scripts/wa.exe?A0=CAMPUS-EVENTS')
	soup = BeautifulSoup(r.text)
	return soup.prettify()